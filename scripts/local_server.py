#!/usr/bin/env python3
"""Local static server plus SQLite API for the IELTS practice platform.

This keeps the current front-end database style intact through
`sources/tinglidanciceshi/local_db_client.js`, while storing data in SQLite.
It is suitable for local testing and later Debian deployment.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import closing
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ai_config import ai_settings, load_ai_env  # noqa: E402
from cors_utils import cors_headers_for_origin  # noqa: E402
from password_utils import authenticate_row_password, hash_password, is_password_hashed  # noqa: E402
from session_auth import (  # noqa: E402
    SESSION_COOKIE_NAME,
    build_session_cookie,
    cookie_name_for_role,
    issue_session_token,
    load_session_secret,
    parse_session_token,
    public_student,
    public_teacher,
    read_cookie_header,
)


from student_api import (  # noqa: E402
    apply_wrong_item_results,
    apply_wrong_word_results,
    change_password as student_change_password,
    insert_study_session,
    insert_test_record,
    load_progress,
    load_speaking_best_scores,
    load_standards,
    load_test_records,
    load_word_mastery,
    load_wrong_book_items,
    load_wrong_words,
    upsert_speaking_best_score,
    upsert_word_mastery,
)
DEFAULT_STATIC_DIR = ROOT / "sources"

from teacher_api import (  # noqa: E402
    create_student,
    create_students_batch,
    create_teacher,
    list_standards as list_teacher_standards,
    list_students,
    list_teachers,
    list_test_records as list_teacher_test_records,
    load_overview,
    load_student_detail,
    reset_student_password,
    reset_teacher_password,
    toggle_student_status,
    toggle_teacher_status,
    update_standard,
    update_student,
    update_teacher,
)
from task_api import (  # noqa: E402
    class_overview as task_class_overview,
    clear_gendu_assignment as task_clear_gendu_assignment,
    clear_plan_pause as task_clear_plan_pause,
    complete_study as task_complete_study,
    ensure_task_tables,
    get_gendu_assignment as task_get_gendu_assignment,
    get_plan as task_get_plan,
    get_time_profile as task_get_time_profile,
    get_today as task_get_today,
    insert_stage_test as task_insert_stage_test,
    list_units as task_list_units,
    normalize_stage_test_positions,
    preview_daily_pack as task_preview_daily_pack,
    preview_daily_pack_items as task_preview_daily_pack_items,
    put_gendu_assignment as task_put_gendu_assignment,
    put_plan_draft as task_put_plan_draft,
    put_plan_pause as task_put_plan_pause,
    put_time_profile as task_put_time_profile,
    clear_daily_schedule as task_clear_daily_schedule,
    report_gendu_practice as task_report_gendu_practice,
    seed_mvp_units,
    submit_stage_test as task_submit_stage_test,
    update_scope_progress as task_update_scope_progress,
)
DEFAULT_DB_PATH = ROOT / "data" / "ielts_local.db"
DEFAULT_P4_ASR_BASE = "https://p4.oyenglish.com.cn"
DEFAULT_WRITING_API_BASE = "http://127.0.0.1:8080"
WRITING_BACKEND_DIR = ROOT / "sources" / "xiezuopigai" / "ielts-writing-backend"

ALLOWED_TABLES = {
    "teacher_config",
    "teachers",
    "students",
    "pass_standards",
    "test_records",
    "study_sessions",
    "word_mastery",
    "wrong_words",
}

JSON_COLUMNS = {"details"}
BOOL_COLUMNS = {"is_password_changed", "is_active", "is_passed", "is_mastered", "last_result"}


def is_safe_identifier(value: str) -> bool:
    return bool(value) and value.replace("_", "").isalnum()


def now_sql() -> str:
    return "strftime('%Y-%m-%dT%H:%M:%fZ','now')"


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate_teachers_username_to_teacher_id(conn: sqlite3.Connection) -> None:
    """Rebuild legacy teachers(id, username, ...) into teachers(teacher_id PK, ...)."""
    tables = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    # Resume a failed mid-migration if the new table is empty but legacy remains.
    if "teachers_legacy" in tables and "teachers" in tables:
        new_cols = {r[1] for r in conn.execute("PRAGMA table_info(teachers)").fetchall()}
        row_count = conn.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
        if "teacher_id" in new_cols and row_count == 0:
            conn.execute("DROP TABLE teachers")
            tables.discard("teachers")
            # fall through to rebuild from teachers_legacy below after rename skip
        elif "teacher_id" in new_cols and row_count > 0:
            conn.execute("DROP TABLE IF EXISTS teachers_legacy")
            return

    source = None
    if "teachers" in tables:
        columns = {r[1] for r in conn.execute("PRAGMA table_info(teachers)").fetchall()}
        if "teacher_id" in columns:
            return
        if "username" not in columns:
            return
        conn.execute("ALTER TABLE teachers RENAME TO teachers_legacy")
        source = "teachers_legacy"
    elif "teachers_legacy" in tables:
        columns = {
            r[1] for r in conn.execute("PRAGMA table_info(teachers_legacy)").fetchall()
        }
        if "username" not in columns:
            return
        source = "teachers_legacy"
    else:
        return

    columns = {r[1] for r in conn.execute(f"PRAGMA table_info({source})").fetchall()}
    is_password_changed_expr = (
        "COALESCE(is_password_changed, 0)"
        if "is_password_changed" in columns
        else "0"
    )
    position_expr = "COALESCE(position, '')" if "position" in columns else "''"
    subjects_expr = "COALESCE(subjects, '')" if "subjects" in columns else "''"

    conn.executescript(
        f"""
        CREATE TABLE teachers (
            teacher_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            is_password_changed INTEGER DEFAULT 0,
            position TEXT DEFAULT '',
            subjects TEXT DEFAULT '',
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
            created_at TEXT DEFAULT ({now_sql()}),
            updated_at TEXT DEFAULT ({now_sql()})
        );
        INSERT INTO teachers (
            teacher_id, name, password,
            is_password_changed, position, subjects, status,
            created_at, updated_at
        )
        SELECT
            username,
            name,
            password,
            {is_password_changed_expr},
            {position_expr},
            {subjects_expr},
            CASE WHEN status IN ('active', 'inactive') THEN status ELSE 'active' END,
            created_at,
            updated_at
        FROM {source};
        DROP TABLE {source};
        """
    )


def migrate_teachers_profile_columns(conn: sqlite3.Connection) -> None:
    """Add profile fields to teachers for existing databases."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='teachers'"
    ).fetchone()
    if not row:
        return
    columns = {r[1] for r in conn.execute("PRAGMA table_info(teachers)").fetchall()}
    alterations = []
    if "position" not in columns:
        alterations.append("ALTER TABLE teachers ADD COLUMN position TEXT DEFAULT ''")
    if "subjects" not in columns:
        alterations.append("ALTER TABLE teachers ADD COLUMN subjects TEXT DEFAULT ''")
    if "is_password_changed" not in columns:
        alterations.append(
            "ALTER TABLE teachers ADD COLUMN is_password_changed INTEGER DEFAULT 0"
        )
    for sql in alterations:
        conn.execute(sql)


def _drop_default_password_column(conn: sqlite3.Connection, table: str) -> None:
    columns = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if "default_password" not in columns:
        return
    try:
        conn.execute(f"ALTER TABLE {table} DROP COLUMN default_password")
        return
    except sqlite3.OperationalError:
        pass
    conn.execute("PRAGMA foreign_keys=OFF")
    try:
        if table == "students":
            conn.execute("DROP TABLE IF EXISTS students_new")
            conn.executescript(
                f"""
                CREATE TABLE students_new (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_password_changed INTEGER DEFAULT 0,
                    target_score REAL DEFAULT 6.5 CHECK (target_score IN (6, 6.5, 7)),
                    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
                    created_at TEXT DEFAULT ({now_sql()}),
                    updated_at TEXT DEFAULT ({now_sql()})
                );
                INSERT INTO students_new (
                    student_id, name, password, is_password_changed,
                    target_score, status, created_at, updated_at
                )
                SELECT
                    student_id,
                    name,
                    password,
                    is_password_changed,
                    CASE
                        WHEN target_score IN (6, 6.5, 7) THEN target_score
                        ELSE 6.5
                    END,
                    CASE
                        WHEN status IN ('active', 'inactive') THEN status
                        ELSE 'active'
                    END,
                    created_at,
                    updated_at
                FROM students;
                DROP TABLE students;
                ALTER TABLE students_new RENAME TO students;
                """
            )
        elif table == "teachers":
            conn.execute("DROP TABLE IF EXISTS teachers_new")
            conn.executescript(
                f"""
                CREATE TABLE teachers_new (
                    teacher_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_password_changed INTEGER DEFAULT 0,
                    position TEXT DEFAULT '',
                    subjects TEXT DEFAULT '',
                    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
                    created_at TEXT DEFAULT ({now_sql()}),
                    updated_at TEXT DEFAULT ({now_sql()})
                );
                INSERT INTO teachers_new (
                    teacher_id, name, password, is_password_changed,
                    position, subjects, status, created_at, updated_at
                )
                SELECT
                    teacher_id,
                    name,
                    password,
                    is_password_changed,
                    COALESCE(position, ''),
                    COALESCE(subjects, ''),
                    CASE
                        WHEN status IN ('active', 'inactive') THEN status
                        ELSE 'active'
                    END,
                    created_at,
                    updated_at
                FROM teachers;
                DROP TABLE teachers;
                ALTER TABLE teachers_new RENAME TO teachers;
                """
            )
    finally:
        conn.execute("PRAGMA foreign_keys=ON")


def migrate_study_sessions_task_columns(conn: sqlite3.Connection) -> None:
    """Add plan_item_id / unit_id for per-task study duration (task system)."""
    tables = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if "study_sessions" not in tables:
        return
    cols = {r[1] for r in conn.execute("PRAGMA table_info(study_sessions)").fetchall()}
    if "plan_item_id" not in cols:
        conn.execute("ALTER TABLE study_sessions ADD COLUMN plan_item_id INTEGER")
    if "unit_id" not in cols:
        conn.execute("ALTER TABLE study_sessions ADD COLUMN unit_id TEXT")
    conn.commit()


def migrate_password_storage(conn: sqlite3.Connection) -> None:
    """Hash legacy plaintext passwords and remove default_password columns."""
    for table, id_column in (("students", "student_id"), ("teachers", "teacher_id")):
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,),
        ).fetchone()
        if not row:
            continue
        rows = conn.execute(
            f"SELECT {id_column}, password FROM {table}"
        ).fetchall()
        for item in rows:
            stored = str(item["password"] or "")
            if stored and not is_password_hashed(stored):
                conn.execute(
                    f"UPDATE {table} SET password = ? WHERE {id_column} = ?",
                    (hash_password(stored), item[id_column]),
                )
        _drop_default_password_column(conn, table)
    conn.commit()


def migrate_wrong_words_module_type(conn: sqlite3.Connection) -> None:
    """Ensure wrong_words is scoped by module_type for parallel dictation banks."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='wrong_words'"
    ).fetchone()
    if not row:
        return
    columns = [r[1] for r in conn.execute("PRAGMA table_info(wrong_words)").fetchall()]
    if "module_type" in columns:
        return
    conn.executescript(
        f"""
        ALTER TABLE wrong_words RENAME TO wrong_words_legacy;
        CREATE TABLE wrong_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            module_type TEXT NOT NULL DEFAULT 'dictation',
            word TEXT NOT NULL,
            wrong_count INTEGER DEFAULT 1,
            correct_streak INTEGER DEFAULT 0,
            last_tested TEXT DEFAULT ({now_sql()}),
            is_mastered INTEGER DEFAULT 0,
            UNIQUE(student_id, module_type, word)
        );
        INSERT INTO wrong_words (
            id, student_id, module_type, word, wrong_count,
            correct_streak, last_tested, is_mastered
        )
        SELECT
            id, student_id, 'dictation', word, wrong_count,
            correct_streak, last_tested, is_mastered
        FROM wrong_words_legacy;
        DROP TABLE wrong_words_legacy;
        CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);
        CREATE INDEX IF NOT EXISTS idx_wrong_words_module_type ON wrong_words(module_type);
        """
    )


def ensure_wrong_items_table(conn: sqlite3.Connection) -> None:
    conn.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS wrong_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            module_type TEXT NOT NULL,
            item_key TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            payload TEXT NOT NULL DEFAULT '{{}}',
            wrong_count INTEGER DEFAULT 1,
            correct_streak INTEGER DEFAULT 0,
            last_tested TEXT DEFAULT ({now_sql()}),
            is_mastered INTEGER DEFAULT 0,
            UNIQUE(student_id, module_type, item_key)
        );
        CREATE INDEX IF NOT EXISTS idx_wrong_items_student_id ON wrong_items(student_id);
        CREATE INDEX IF NOT EXISTS idx_wrong_items_module_type ON wrong_items(module_type);
        """
    )


def init_db(db_path: Path, *, bind_host: str = "127.0.0.1") -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(db_path)) as conn:
        # teacher_config.access_password：历史遗留字段，教师登录已改用 teachers 表
        conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS teacher_config (
                id INTEGER PRIMARY KEY DEFAULT 1,
                access_password TEXT NOT NULL DEFAULT '',
                school_name TEXT DEFAULT '藕叶英语',
                updated_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                is_password_changed INTEGER DEFAULT 0,
                position TEXT DEFAULT '',
                subjects TEXT DEFAULT '',
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
                created_at TEXT DEFAULT ({now_sql()}),
                updated_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                is_password_changed INTEGER DEFAULT 0,
                target_score REAL DEFAULT 6.5 CHECK (target_score IN (6, 6.5, 7)),
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
                created_at TEXT DEFAULT ({now_sql()}),
                updated_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS pass_standards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_type TEXT UNIQUE NOT NULL,
                module_name TEXT NOT NULL,
                score_6 REAL DEFAULT 70,
                score_6_5 REAL DEFAULT 80,
                score_7 REAL DEFAULT 95,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT ({now_sql()}),
                updated_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS test_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT DEFAULT 'dictation',
                module_name TEXT DEFAULT '听力1000词',
                test_type TEXT NOT NULL DEFAULT 'module_test',
                score REAL NOT NULL,
                correct_count INTEGER NOT NULL,
                total_count INTEGER NOT NULL,
                is_passed INTEGER NOT NULL,
                pass_threshold REAL NOT NULL,
                duration_seconds INTEGER DEFAULT 0,
                details TEXT DEFAULT '[]',
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT NOT NULL,
                module_name TEXT,
                session_kind TEXT DEFAULT 'study' CHECK (session_kind IN ('study', 'test')),
                words_tested INTEGER DEFAULT 0,
                initial_correct INTEGER DEFAULT 0,
                initial_wrong INTEGER DEFAULT 0,
                groups_completed INTEGER DEFAULT 0,
                plan_item_id INTEGER,
                unit_id TEXT,
                score_percent REAL,
                duration_seconds INTEGER NOT NULL DEFAULT 0,
                details TEXT DEFAULT '[]',
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS word_mastery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                word TEXT NOT NULL,
                status TEXT DEFAULT 'learning' CHECK (status IN ('new', 'learning', 'mastered')),
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0,
                is_initial_correct INTEGER DEFAULT 0,
                last_result INTEGER,
                last_practiced_at TEXT DEFAULT ({now_sql()}),
                created_at TEXT DEFAULT ({now_sql()}),
                updated_at TEXT DEFAULT ({now_sql()}),
                UNIQUE(student_id, word)
            );

            CREATE TABLE IF NOT EXISTS wrong_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT NOT NULL DEFAULT 'dictation',
                word TEXT NOT NULL,
                wrong_count INTEGER DEFAULT 1,
                correct_streak INTEGER DEFAULT 0,
                last_tested TEXT DEFAULT ({now_sql()}),
                is_mastered INTEGER DEFAULT 0,
                UNIQUE(student_id, module_type, word)
            );

            CREATE TABLE IF NOT EXISTS speaking_best_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                question_key TEXT NOT NULL,
                question_text TEXT NOT NULL DEFAULT '',
                part TEXT NOT NULL DEFAULT 'p1',
                best_score REAL NOT NULL,
                updated_at TEXT DEFAULT ({now_sql()}),
                UNIQUE(student_id, question_key)
            );

            CREATE INDEX IF NOT EXISTS idx_test_records_student_id ON test_records(student_id);
            CREATE INDEX IF NOT EXISTS idx_test_records_created_at ON test_records(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_test_records_module_type ON test_records(module_type);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_student_id ON study_sessions(student_id);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_module_type ON study_sessions(module_type);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_created_at ON study_sessions(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);
            CREATE INDEX IF NOT EXISTS idx_word_mastery_student_id ON word_mastery(student_id);
            CREATE INDEX IF NOT EXISTS idx_speaking_best_scores_student_id ON speaking_best_scores(student_id);

            CREATE TABLE IF NOT EXISTS wrong_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT NOT NULL,
                item_key TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT '',
                payload TEXT NOT NULL DEFAULT '{{}}',
                wrong_count INTEGER DEFAULT 1,
                correct_streak INTEGER DEFAULT 0,
                last_tested TEXT DEFAULT ({now_sql()}),
                is_mastered INTEGER DEFAULT 0,
                UNIQUE(student_id, module_type, item_key)
            );
            CREATE INDEX IF NOT EXISTS idx_wrong_items_student_id ON wrong_items(student_id);
            CREATE INDEX IF NOT EXISTS idx_wrong_items_module_type ON wrong_items(module_type);
            """
        )

        # Existing DBs may still lack module_type; migrate before indexing that column.
        migrate_wrong_words_module_type(conn)
        migrate_teachers_username_to_teacher_id(conn)
        migrate_teachers_profile_columns(conn)
        migrate_password_storage(conn)
        migrate_study_sessions_task_columns(conn)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wrong_words_module_type ON wrong_words(module_type)"
        )
        ensure_wrong_items_table(conn)
        ensure_task_tables(conn)
        seed_mvp_units(conn)

        conn.execute(
            """
            INSERT INTO teacher_config (id, access_password, school_name)
            VALUES (1, '', '藕叶英语')
            ON CONFLICT(id) DO NOTHING
            """
        )

        admin_password = os.environ.get("IELTS_ADMIN_PASSWORD", "").strip()
        if admin_password:
            conn.execute(
                """
                INSERT INTO teachers (
                    teacher_id, name, password,
                    is_password_changed, position, subjects, status
                )
                VALUES (
                    'admin', '管理员', ?, 1, '系统管理员', '', 'active'
                )
                ON CONFLICT(teacher_id) DO NOTHING
                """,
                (hash_password(admin_password),),
            )
        else:
            print("警告：未设置 IELTS_ADMIN_PASSWORD 环境变量，未创建 admin 账号")

        if bind_host == "127.0.0.1":
            conn.execute(
                """
                INSERT INTO teachers (
                    teacher_id, name, password,
                    is_password_changed, position, subjects, status
                )
                VALUES (
                    'zhangxiaodong', '张晓东', ?, 0, '教研校长', '阅读、写作', 'active'
                )
                ON CONFLICT(teacher_id) DO NOTHING
                """,
                (hash_password("123456"),),
            )

        if admin_password:
            conn.execute(
                """
                UPDATE teachers
                SET position = '系统管理员',
                    is_password_changed = 1,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
                WHERE teacher_id = 'admin'
                  AND (position IS NULL OR position = '')
                """
            )

        standards = [
            ("dictation", "听力1000词", 70, 80, 90),
            ("listening_basic", "听力基础词汇", 70, 80, 90),
            ("reading_synonym", "阅读同义替换", 70, 80, 90),
            ("writing_phrase", "写作词伙", 50, 70, 90),
            ("sentence", "长难句分析", 60, 80, 80),
            ("listening_synonym", "听力同义替换", 70, 80, 90),
            ("writing_translate", "写作句子翻译", 50, 70, 90),
            ("listening_p4_speed", "听力P4跟读倍速", 70, 80, 90),
            ("writing_correction", "作文批改", 1, 1, 1),
            ("speaking", "口语练习", 5.5, 6, 6.5),
            ("dictation_learn", "听力单词学习", 70, 80, 90),
        ]
        conn.executemany(
            """
            INSERT INTO pass_standards (module_type, module_name, score_6, score_6_5, score_7)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(module_type) DO UPDATE SET
                module_name = excluded.module_name,
                score_6 = excluded.score_6,
                score_6_5 = excluded.score_6_5,
                score_7 = excluded.score_7,
                updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
            """,
            standards,
        )

        conn.execute(
            """
            INSERT INTO students (
                student_id, name, password,
                is_password_changed, target_score, status
            )
            VALUES ('2025001', '测试学生', ?, 0, 6.5, 'active')
            ON CONFLICT(student_id) DO NOTHING
            """,
            (hash_password("123456"),),
        )
        conn.commit()


def normalise_value(column: str, value: Any) -> Any:
    if column in JSON_COLUMNS and not isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if column in BOOL_COLUMNS and isinstance(value, bool):
        return 1 if value else 0
    return value


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    for key in list(item.keys()):
        if key in JSON_COLUMNS and isinstance(item[key], str):
            try:
                item[key] = json.loads(item[key])
            except json.JSONDecodeError:
                pass
        if key in BOOL_COLUMNS and item[key] is not None:
            item[key] = bool(item[key])
    return item


def selected_columns(select_expr: str) -> str:
    expr = (select_expr or "*").strip()
    if expr == "*" or "students(" in expr:
        return "*"
    columns = [part.strip() for part in expr.split(",") if part.strip()]
    safe = [col for col in columns if is_safe_identifier(col)]
    return ", ".join(safe) if safe else "*"


def build_where(filters: list[dict[str, Any]]) -> tuple[str, list[Any]]:
    clauses = []
    params: list[Any] = []
    for filt in filters or []:
        col = str(filt.get("column", ""))
        if not is_safe_identifier(col):
            continue
        op = filt.get("operator", "eq")
        if op != "eq":
            continue
        clauses.append(f"{col} = ?")
        params.append(normalise_value(col, filt.get("value")))
    return (" WHERE " + " AND ".join(clauses), params) if clauses else ("", params)


def attach_students(conn: sqlite3.Connection, table: str, select_expr: str, rows: list[dict[str, Any]]) -> None:
    if table != "test_records" or "students(" not in (select_expr or ""):
        return
    for item in rows:
        student_id = item.get("student_id")
        student = conn.execute("SELECT name FROM students WHERE student_id = ?", (student_id,)).fetchone()
        item["students"] = {"name": student["name"]} if student else None


def query_db(db_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    table = str(payload.get("table", ""))
    if table not in ALLOWED_TABLES:
        return {"data": None, "error": {"message": f"Table not allowed: {table}"}}

    action = payload.get("action")
    with closing(connect(db_path)) as conn:
        if action == "select":
            select_expr = str(payload.get("select") or "*")
            cols = selected_columns(select_expr)
            where_sql, params = build_where(payload.get("filters") or [])
            sql = f"SELECT {cols} FROM {table}{where_sql}"
            order = payload.get("order")
            if order:
                col = str(order.get("column", ""))
                if is_safe_identifier(col):
                    direction = "ASC" if order.get("ascending", True) else "DESC"
                    sql += f" ORDER BY {col} {direction}"
            limit = payload.get("limit")
            if isinstance(limit, int) and limit > 0:
                sql += f" LIMIT {limit}"
            rows = [row_to_dict(row) for row in conn.execute(sql, params).fetchall()]
            attach_students(conn, table, select_expr, rows)
            if payload.get("single"):
                if rows:
                    return {"data": rows[0], "error": None}
                return {"data": None, "error": {"message": "No rows found"}}
            return {"data": rows, "error": None}

        if action == "insert":
            records = payload.get("data")
            if isinstance(records, dict):
                records = [records]
            if not isinstance(records, list) or not records:
                return {"data": None, "error": {"message": "Insert data is empty"}}
            inserted: list[dict[str, Any]] = []
            for raw in records:
                record = {
                    str(k): normalise_value(str(k), v)
                    for k, v in dict(raw).items()
                    if is_safe_identifier(str(k))
                }
                if not record:
                    return {"data": None, "error": {"message": "No valid insert columns"}}
                columns = list(record.keys())
                placeholders = ", ".join(["?"] * len(columns))
                sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
                cur = conn.execute(sql, [record[col] for col in columns])
                inserted.append({"id": cur.lastrowid, **dict(raw)})
            conn.commit()
            return {"data": inserted, "error": None}

        if action == "update":
            updates = payload.get("data") or {}
            if not isinstance(updates, dict) or not updates:
                return {"data": None, "error": {"message": "Update data is empty"}}
            set_parts = []
            params: list[Any] = []
            for key, value in updates.items():
                col = str(key)
                if not is_safe_identifier(col):
                    continue
                set_parts.append(f"{col} = ?")
                params.append(normalise_value(col, value))
            where_sql, where_params = build_where(payload.get("filters") or [])
            if not set_parts:
                return {"data": None, "error": {"message": "No valid update columns"}}
            if not where_sql:
                return {"data": None, "error": {"message": "Update requires filters"}}
            sql = "UPDATE " + table + " SET " + ", ".join(set_parts) + where_sql
            conn.execute(sql, params + where_params)
            conn.commit()
            return {"data": [], "error": None}

    return {"data": None, "error": {"message": f"Unsupported action: {action}"}}


class LocalHandler(SimpleHTTPRequestHandler):
    static_dir: Path = DEFAULT_STATIC_DIR
    db_path: Path = DEFAULT_DB_PATH
    writing_api_base: str = DEFAULT_WRITING_API_BASE
    p4_asr_base: str = DEFAULT_P4_ASR_BASE
    session_secret: bytes = b""

    def end_headers(self) -> None:
        for name, value in cors_headers_for_origin(self.headers.get("Origin")).items():
            self.send_header(name, value)
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_PUT(self) -> None:
        """MVP task plan / time-profile updates (also accepted via POST)."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path.startswith("/api/task/students/") and path.endswith("/plan-pause"):
            self.handle_task_plan_pause_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/gendu-assignment"):
            self.handle_task_gendu_assignment_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/plan"):
            self.handle_task_student_plan_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/time-profile"):
            self.handle_task_student_time_profile_put()
            return
        self.send_json({"data": None, "error": {"message": "Not Found"}}, status=404)

    def do_DELETE(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path.startswith("/api/task/students/") and path.endswith("/plan-pause"):
            self.handle_task_plan_pause_delete()
            return
        if path.startswith("/api/task/students/") and path.endswith("/gendu-assignment"):
            self.handle_task_gendu_assignment_delete()
            return
        self.send_json({"data": None, "error": {"message": "Not Found"}}, status=404)

    def current_session(self, role: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Read role-scoped session cookie.

        Student and teacher now use separate cookies so logging into one role
        no longer overwrites the other. Legacy ``ielts_session`` is still
        accepted as a fallback for the matching role.
        """
        if not self.session_secret:
            return None
        cookie_header = self.headers.get("Cookie", "")

        def _from_names(names: list[str], expect_role: str) -> Optional[dict[str, Any]]:
            for name in names:
                raw = read_cookie_header(cookie_header, name)
                if not raw:
                    continue
                session = parse_session_token(raw, self.session_secret)
                if session and session.get("role") == expect_role:
                    return session
            return None

        if role in ("student", "teacher"):
            return _from_names(
                [cookie_name_for_role(role), SESSION_COOKIE_NAME],
                role,
            )
        # Either role (prefer teacher so teacher console keeps working when both exist)
        return self.current_session("teacher") or self.current_session("student")

    def use_secure_cookies(self) -> bool:
        proto = (
            self.headers.get("X-Forwarded-Proto")
            or self.headers.get("x-forwarded-proto")
            or ""
        ).split(",")[0].strip().lower()
        return proto == "https"

    def session_cookie(
        self,
        token: str = "",
        *,
        clear: bool = False,
        role: Optional[str] = None,
        name: Optional[str] = None,
    ) -> str:
        return build_session_cookie(
            token,
            clear=clear,
            secure=self.use_secure_cookies(),
            role=role,
            name=name,
        )

    def clear_session_cookies(self, role: Optional[str] = None) -> list[str]:
        """Clear role cookie(s) plus legacy shared cookie."""
        secure = self.use_secure_cookies()
        out: list[str] = []
        if role in ("student", "teacher"):
            out.append(build_session_cookie("", clear=True, secure=secure, role=role))
        else:
            out.append(build_session_cookie("", clear=True, secure=secure, role="student"))
            out.append(build_session_cookie("", clear=True, secure=secure, role="teacher"))
        out.append(build_session_cookie("", clear=True, secure=secure, name=SESSION_COOKIE_NAME))
        return out

    def login_set_cookies(self, role: str, token: str) -> list[str]:
        """Set role cookie and drop legacy shared cookie (do not touch the other role)."""
        return [
            self.session_cookie(token, role=role),
            self.session_cookie(clear=True, name=SESSION_COOKIE_NAME),
        ]

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        data = json.loads(raw or "{}")
        return data if isinstance(data, dict) else {}

    def send_json(
        self,
        data: dict[str, Any],
        status: int = 200,
        set_cookies: Optional[list[str]] = None,
    ) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for item in set_cookies or []:
            self.send_header("Set-Cookie", item)
        self.end_headers()
        self.wfile.write(body)

    def require_logged_in_session(self) -> Optional[dict[str, Any]]:
        session = self.current_session()
        if not session or session.get("role") not in ("student", "teacher"):
            self.send_json({"data": None, "error": {"message": "需要登录"}}, status=401)
            return None
        return session

    def handle_public_config(self) -> None:
        settings = ai_settings()
        self.send_json(
            {
                "ai_configured": bool(settings["api_key"]),
                "ai_model": settings["model"],
                "p4_asr_base": self.p4_asr_base,
                "transcribe_path": "/api/p4/transcribe",
            }
        )

    def handle_ai_messages(self) -> None:
        session = self.require_logged_in_session()
        if not session:
            return
        settings = ai_settings()
        if not settings["api_key"]:
            self.send_json(
                {"error": {"message": "AI 未配置，请在 config/ai.env 设置 AI_API_KEY"}},
                status=503,
            )
            return
        payload = self.read_json_body()
        messages = payload.get("messages")
        if not isinstance(messages, list) or not messages:
            self.send_json(
                {"error": {"message": "messages 必须是非空数组"}},
                status=400,
            )
            return
        upstream_body: dict[str, Any] = {
            "model": settings["model"],
            "max_tokens": int(payload.get("max_tokens") or 4000),
            "messages": messages,
            "temperature": float(payload.get("temperature", 0.3)),
        }
        if payload.get("system"):
            upstream_body["system"] = payload["system"]
        body_bytes = json.dumps(upstream_body, ensure_ascii=False).encode("utf-8")
        target = settings["base_url"].rstrip("/") + "/anthropic/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": settings["api_key"],
            "anthropic-version": "2023-06-01",
        }
        try:
            req = urllib.request.Request(
                target, data=body_bytes, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read()
                status = getattr(resp, "status", 200)
                content_type = resp.headers.get(
                    "Content-Type", "application/json; charset=utf-8"
                )
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            self.send_response(exc.code)
            self.send_header(
                "Content-Type",
                exc.headers.get("Content-Type", "application/json; charset=utf-8"),
            )
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except Exception as exc:
            self.send_json(
                {"error": {"message": f"AI 服务不可用：{exc}"}},
                status=502,
            )

    def handle_auth_me(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        want_role = str((qs.get("role") or [""])[0] or "").strip().lower()
        if want_role in ("student", "teacher"):
            session = self.current_session(want_role)
        else:
            session = self.current_session()
        if not session:
            self.send_json({"data": None, "error": {"message": "未登录"}}, status=401)
            return
        with closing(connect(self.db_path)) as conn:
            if session["role"] == "student":
                row = conn.execute(
                    "SELECT * FROM students WHERE student_id = ?",
                    (session["id"],),
                ).fetchone()
                if not row or row["status"] != "active":
                    self.send_json(
                        {"data": None, "error": {"message": "会话已失效"}},
                        status=401,
                        set_cookies=self.clear_session_cookies("student"),
                    )
                    return
                self.send_json(
                    {
                        "data": {
                            "role": "student",
                            "student": public_student(row_to_dict(row)),
                        },
                        "error": None,
                    }
                )
                return
            row = conn.execute(
                "SELECT * FROM teachers WHERE teacher_id = ?",
                (session["id"],),
            ).fetchone()
            if not row or row["status"] != "active":
                self.send_json(
                    {"data": None, "error": {"message": "会话已失效"}},
                    status=401,
                    set_cookies=self.clear_session_cookies("teacher"),
                )
                return
            self.send_json(
                {
                    "data": {
                        "role": "teacher",
                        "teacher": public_teacher(row_to_dict(row)),
                    },
                    "error": None,
                }
            )

    def handle_student_login(self) -> None:
        payload = self.read_json_body()
        student_id = str(payload.get("student_id") or "").strip()
        password = str(payload.get("password") or "")
        if not student_id or not password:
            self.send_json({"data": None, "error": {"message": "请输入学号和密码"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            row = authenticate_row_password(
                conn,
                table="students",
                id_column="student_id",
                row_id=student_id,
                password=password,
            )
            if not row:
                self.send_json({"data": None, "error": {"message": "学号或密码错误"}}, status=401)
                return
            item = row_to_dict(row)
            if item.get("status") != "active":
                self.send_json({"data": None, "error": {"message": "账号已被禁用"}}, status=403)
                return
            token = issue_session_token(
                role="student",
                subject_id=student_id,
                secret=self.session_secret,
            )
            self.send_json(
                {"data": {"role": "student", "student": public_student(item)}, "error": None},
                set_cookies=self.login_set_cookies("student", token),
            )

    def handle_teacher_login(self) -> None:
        payload = self.read_json_body()
        teacher_id = str(payload.get("teacher_id") or "").strip()
        password = str(payload.get("password") or "")
        if not teacher_id or not password:
            self.send_json({"data": None, "error": {"message": "请输入账号和密码"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            row = authenticate_row_password(
                conn,
                table="teachers",
                id_column="teacher_id",
                row_id=teacher_id,
                password=password,
            )
            if not row:
                self.send_json({"data": None, "error": {"message": "账号或密码错误"}}, status=401)
                return
            item = row_to_dict(row)
            if item.get("status") != "active":
                self.send_json({"data": None, "error": {"message": "账号已被禁用"}}, status=403)
                return
            token = issue_session_token(
                role="teacher",
                subject_id=teacher_id,
                secret=self.session_secret,
            )
            self.send_json(
                {"data": {"role": "teacher", "teacher": public_teacher(item)}, "error": None},
                set_cookies=self.login_set_cookies("teacher", token),
            )

    def handle_logout(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        role = str((qs.get("role") or [""])[0] or "").strip().lower()
        if role not in ("student", "teacher"):
            role = None
        self.send_json(
            {"data": {"ok": True}, "error": None},
            set_cookies=self.clear_session_cookies(role),
        )

    def require_teacher_session(self) -> Optional[dict[str, Any]]:
        session = self.current_session("teacher")
        if not session or session.get("role") != "teacher":
            self.send_json({"data": None, "error": {"message": "需要教师登录"}}, status=401)
            return None
        return session

    def require_admin_session(self) -> Optional[dict[str, Any]]:
        session = self.require_teacher_session()
        if not session:
            return None
        if session.get("id") != "admin":
            self.send_json({"data": None, "error": {"message": "仅管理员可操作"}}, status=403)
            return None
        return session

    def handle_teacher_students_get(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": list_students(conn), "error": None})

    def handle_teacher_students_create(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err, initial_password = create_student(
                conn,
                name=payload.get("name") or "",
                target_score=payload.get("target_score", payload.get("targetScore", 6.5)),
                student_id=payload.get("student_id"),
            )
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json(
                {"data": {**(row or {}), "password": initial_password}, "error": None}
            )

    def handle_teacher_students_batch(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        items = payload.get("students") or payload.get("items") or []
        if not isinstance(items, list):
            self.send_json({"data": None, "error": {"message": "students 必须是数组"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            result, err = create_students_batch(conn, items)
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": result, "error": None})

    def handle_teacher_students_reset_password(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            initial_password, err = reset_student_password(conn, payload.get("student_id") or "")
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json(
                {"data": {"ok": True, "password": initial_password}, "error": None}
            )

    def handle_teacher_students_toggle_status(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err = toggle_student_status(conn, payload.get("student_id") or "")
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": row, "error": None})

    def handle_teacher_students_update(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err = update_student(
                conn,
                student_id=payload.get("student_id") or "",
                name=payload.get("name") or "",
                target_score=payload.get("target_score", payload.get("targetScore", 6.5)),
            )
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": row, "error": None})

    def handle_teacher_test_records_get(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        try:
            limit = int((qs.get("limit") or ["1000"])[0])
        except ValueError:
            limit = 1000
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": list_teacher_test_records(conn, limit=limit), "error": None})

    def handle_teacher_overview(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": load_overview(conn), "error": None})

    def handle_teacher_student_detail(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        student_id = (qs.get("student_id") or [None])[0]
        with closing(connect(self.db_path)) as conn:
            data, err = load_student_detail(conn, student_id or "")
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=404)
                return
            self.send_json({"data": data, "error": None})

    def handle_teacher_standards_get(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": list_teacher_standards(conn), "error": None})

    def handle_teacher_standards_update(self) -> None:
        session = self.require_teacher_session()
        if not session:
            return
        payload = self.read_json_body()
        module_type = payload.get("module_type") or payload.get("moduleType") or ""
        with closing(connect(self.db_path)) as conn:
            err = update_standard(conn, module_type, payload)
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": {"ok": True}, "error": None})

    def handle_teacher_teachers_get(self) -> None:
        session = self.require_admin_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": list_teachers(conn), "error": None})

    def handle_teacher_teachers_create(self) -> None:
        session = self.require_admin_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err, initial_password = create_teacher(
                conn,
                teacher_id=payload.get("teacher_id") or payload.get("account") or "",
                name=payload.get("name") or "",
                position=payload.get("position") or "",
                subjects=payload.get("subjects") or "",
            )
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json(
                {
                    "data": {"teacher": row, "password": initial_password},
                    "error": None,
                }
            )

    def handle_teacher_teachers_reset_password(self) -> None:
        session = self.require_admin_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            initial_password, err = reset_teacher_password(conn, payload.get("teacher_id") or "")
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json(
                {"data": {"ok": True, "password": initial_password}, "error": None}
            )

    def handle_teacher_teachers_toggle_status(self) -> None:
        session = self.require_admin_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err = toggle_teacher_status(conn, payload.get("teacher_id") or "")
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": row, "error": None})

    def handle_teacher_teachers_update(self) -> None:
        session = self.require_admin_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row, err = update_teacher(
                conn,
                teacher_id=payload.get("teacher_id") or payload.get("account") or "",
                name=payload.get("name") or "",
                position=payload.get("position") or "",
                subjects=payload.get("subjects") or "",
            )
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            self.send_json({"data": row, "error": None})


    def require_student_session(self) -> Optional[dict[str, Any]]:
        session = self.current_session("student")
        if not session or session.get("role") != "student":
            self.send_json({"data": None, "error": {"message": "需要学生登录"}}, status=401)
            return None
        return session

    def handle_student_progress(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": load_progress(conn, session["id"]), "error": None})

    def handle_student_test_records_get(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": load_test_records(conn, session["id"]), "error": None})

    def handle_student_speaking_best_scores_get(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            scores = load_speaking_best_scores(conn, session["id"])
            self.send_json({"data": {"scores": scores}, "error": None})

    def handle_student_speaking_best_scores_post(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        question = payload.get("question") or payload.get("q") or payload.get("question_text") or ""
        score = payload.get("score")
        if score is None:
            score = payload.get("overall") or payload.get("best_score")
        part = payload.get("part") or "p1"
        try:
            with closing(connect(self.db_path)) as conn:
                row = upsert_speaking_best_score(
                    conn,
                    session["id"],
                    str(question),
                    float(score),
                    part=str(part or "p1"),
                )
            self.send_json({"data": row, "error": None})
        except (TypeError, ValueError) as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_student_standards(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            self.send_json({"data": load_standards(conn), "error": None})

    def handle_student_wrong_words_get(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        module_type = (qs.get("module_type") or [None])[0]
        unmastered = (qs.get("unmastered") or ["0"])[0] in ("1", "true", "yes")
        with closing(connect(self.db_path)) as conn:
            rows = load_wrong_words(
                conn,
                session["id"],
                module_type=module_type,
                unmastered_only=unmastered,
            )
            self.send_json({"data": rows, "error": None})

    def handle_student_word_mastery_get(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            rows = load_word_mastery(conn, session["id"])
            for item in rows:
                item["last_tested"] = item.get("last_practiced_at")
            self.send_json({"data": rows, "error": None})

    def handle_student_change_password(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        password = payload.get("password") or payload.get("new_password") or ""
        with closing(connect(self.db_path)) as conn:
            err = student_change_password(conn, session["id"], password)
            if err:
                self.send_json({"data": None, "error": {"message": err}}, status=400)
                return
            row = conn.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (session["id"],),
            ).fetchone()
            self.send_json(
                {
                    "data": {"student": public_student(row_to_dict(row)) if row else None},
                    "error": None,
                }
            )

    def handle_student_study_sessions_post(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row = insert_study_session(conn, session["id"], payload)
            self.send_json({"data": row, "error": None})

    def handle_student_test_records_post(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            row = insert_test_record(conn, session["id"], payload)
            self.send_json({"data": row, "error": None})

    def handle_student_wrong_items_get(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        module_type = str((qs.get("module_type") or [""])[0] or "").strip()
        unmastered = (qs.get("unmastered") or ["1"])[0] in ("1", "true", "yes")
        if not module_type:
            self.send_json({"data": None, "error": {"message": "缺少 module_type"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            rows = load_wrong_book_items(
                conn,
                session["id"],
                module_type,
                unmastered_only=unmastered,
            )
            self.send_json({"data": rows, "error": None})

    def handle_student_wrong_items_apply(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        module_type = str(payload.get("module_type") or payload.get("moduleType") or "").strip()
        results = payload.get("results") or []
        if not module_type:
            self.send_json({"data": None, "error": {"message": "缺少 module_type"}}, status=400)
            return
        if not isinstance(results, list):
            self.send_json({"data": None, "error": {"message": "results 必须是数组"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            summary = apply_wrong_item_results(conn, session["id"], module_type, results)
            self.send_json({"data": summary, "error": None})

    def handle_student_wrong_words_apply(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        module_type = str(payload.get("module_type") or payload.get("moduleType") or "dictation")
        results = payload.get("results") or []
        if not isinstance(results, list):
            self.send_json({"data": None, "error": {"message": "results 必须是数组"}}, status=400)
            return
        with closing(connect(self.db_path)) as conn:
            summary = apply_wrong_word_results(conn, session["id"], module_type, results)
            self.send_json({"data": summary, "error": None})

    def handle_student_word_mastery_post(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        try:
            with closing(connect(self.db_path)) as conn:
                row = upsert_word_mastery(conn, session["id"], payload)
            self.send_json({"data": row, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    # ── Task system (MVP) ──────────────────────────────────────────────

    def handle_task_class_overview(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        task_date = (qs.get("date") or [None])[0]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            try:
                data = task_class_overview(conn, task_date=task_date or None)
            except ValueError as exc:
                self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)
                return
            self.send_json({"data": data, "error": None})

    def handle_task_units_get(self) -> None:
        if not self.require_logged_in_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query or "")
        module_type = str((qs.get("module_type") or [""])[0] or "").strip() or None
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            seed_mvp_units(conn)
            self.send_json({"data": task_list_units(conn, module_type), "error": None})

    def handle_task_me_today(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            seed_mvp_units(conn)
            self.send_json({"data": task_get_today(conn, session["id"]), "error": None})

    def handle_task_me_complete_study(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        plan_item_id = payload.get("plan_item_id")
        content_version = str(payload.get("content_version") or "1")
        if plan_item_id is None:
            self.send_json({"data": None, "error": {"message": "缺少 plan_item_id"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                data = task_complete_study(
                    conn, session["id"], int(plan_item_id), content_version
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_me_gendu_practice(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        plan_item_id = payload.get("plan_item_id")
        if plan_item_id is None:
            self.send_json({"data": None, "error": {"message": "缺少 plan_item_id"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                seed_mvp_units(conn)
                data = task_report_gendu_practice(
                    conn,
                    session["id"],
                    plan_item_id=int(plan_item_id),
                    score=payload.get("score"),
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_gendu_assignment_get(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            seed_mvp_units(conn)
            data = task_get_gendu_assignment(conn, student_id)
            self.send_json({"data": data, "error": None})

    def handle_task_gendu_assignment_put(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                seed_mvp_units(conn)
                data = task_put_gendu_assignment(conn, student_id, payload)
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_gendu_assignment_delete(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            data = task_clear_gendu_assignment(conn, student_id)
            self.send_json({"data": data, "error": None})

    def handle_task_me_scope_progress(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        plan_item_id = payload.get("plan_item_id")
        if plan_item_id is None:
            self.send_json({"data": None, "error": {"message": "缺少 plan_item_id"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                data = task_update_scope_progress(
                    conn,
                    session["id"],
                    int(plan_item_id),
                    scope_done=payload.get("scope_done"),
                    delta=payload.get("delta"),
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_me_submit_test(self) -> None:
        session = self.require_student_session()
        if not session:
            return
        payload = self.read_json_body()
        plan_item_id = payload.get("plan_item_id")
        if plan_item_id is None:
            self.send_json({"data": None, "error": {"message": "缺少 plan_item_id"}}, status=400)
            return
        try:
            score = float(payload.get("score"))
            threshold = float(payload.get("threshold", 80))
        except (TypeError, ValueError):
            self.send_json({"data": None, "error": {"message": "score/threshold 无效"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                data = task_submit_stage_test(
                    conn,
                    session["id"],
                    int(plan_item_id),
                    score,
                    threshold=threshold,
                    details=payload.get("details"),
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def _task_student_id_from_path(self, prefix: str) -> Optional[str]:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if not path.startswith(prefix):
            return None
        rest = path[len(prefix) :].lstrip("/")
        if not rest:
            return None
        return rest.split("/")[0]

    def handle_task_student_plan_get(self) -> None:
        if not self.require_teacher_session():
            return
        student_id = self._task_student_id_from_path("/api/task/students/")
        if not student_id or student_id.endswith("plan"):
            # path like /api/task/students/2025001/plan
            parsed = urllib.parse.urlparse(self.path)
            parts = [p for p in parsed.path.split("/") if p]
            # ['api','task','students', sid, 'plan']
            if len(parts) >= 5 and parts[3]:
                student_id = parts[3]
            else:
                self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
                return
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            seed_mvp_units(conn)
            self.send_json({"data": task_get_plan(conn, student_id), "error": None})

    def handle_task_pack_preview_get(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        qs = urllib.parse.parse_qs(parsed.query)
        source = (qs.get("source") or ["live"])[0]
        if source not in ("live", "draft"):
            source = "live"
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            seed_mvp_units(conn)
            data = task_preview_daily_pack(conn, student_id, source=source)
            self.send_json({"data": data, "error": None})

    def handle_task_pack_preview_post(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        items = payload.get("items")
        if not isinstance(items, list):
            self.send_json({"data": None, "error": {"message": "items 必须是数组"}}, status=400)
            return
        try:
            raw_wd = payload.get("weekday_minutes")
            raw_we = payload.get("weekend_minutes")
            wd = None if raw_wd in (None, "") else int(raw_wd)
            we = None if raw_we in (None, "") else int(raw_we)
        except (TypeError, ValueError):
            self.send_json({"data": None, "error": {"message": "时长须为数字"}}, status=400)
            return
        pack_mode = payload.get("pack_mode")
        module_quotas = payload.get("module_quotas")
        if pack_mode is not None and pack_mode not in ("time_budget", "units_per_day"):
            self.send_json(
                {"data": None, "error": {"message": "pack_mode 无效"}},
                status=400,
            )
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                seed_mvp_units(conn)
                data = task_preview_daily_pack_items(
                    conn,
                    student_id,
                    items,
                    weekday_minutes=wd,
                    weekend_minutes=we,
                    pack_mode=pack_mode,
                    module_quotas=module_quotas if isinstance(module_quotas, list) else None,
                    effective_from=payload.get("effective_from"),
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_student_plan_put(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        items = payload.get("items")
        if not isinstance(items, list):
            self.send_json({"data": None, "error": {"message": "items 必须是数组"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                seed_mvp_units(conn)
                data = task_put_plan_draft(
                    conn, student_id, items, effective_from=payload.get("effective_from")
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=409)

    def handle_task_student_time_profile_get(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            self.send_json({"data": task_get_time_profile(conn, student_id), "error": None})

    def handle_task_student_time_profile_put(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            data = task_put_time_profile(conn, student_id, payload)
            self.send_json({"data": data, "error": None})

    def handle_task_clear_daily_schedule(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            data = task_clear_daily_schedule(conn, student_id)
            self.send_json({"data": data, "error": None})

    def handle_task_plan_pause_put(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                seed_mvp_units(conn)
                data = task_put_plan_pause(conn, student_id, payload)
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def handle_task_plan_pause_delete(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        with closing(connect(self.db_path)) as conn:
            ensure_task_tables(conn)
            data = task_clear_plan_pause(conn, student_id)
            self.send_json({"data": data, "error": None})

    def handle_task_insert_stage_test(self) -> None:
        if not self.require_teacher_session():
            return
        parsed = urllib.parse.urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        # api/task/students/:id/plan/insert-stage-test
        if len(parts) < 5:
            self.send_json({"data": None, "error": {"message": "缺少 student_id"}}, status=400)
            return
        student_id = parts[3]
        payload = self.read_json_body()
        unit_ids = payload.get("unit_ids") or []
        if not isinstance(unit_ids, list):
            self.send_json({"data": None, "error": {"message": "unit_ids 必须是数组"}}, status=400)
            return
        try:
            with closing(connect(self.db_path)) as conn:
                ensure_task_tables(conn)
                data = task_insert_stage_test(
                    conn,
                    student_id,
                    unit_ids=unit_ids,
                    after_sort_order=payload.get("after_sort_order"),
                    test_title=str(payload.get("test_title") or ""),
                )
                self.send_json({"data": data, "error": None})
        except ValueError as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=400)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/health"):
            self.send_json(
                {
                    "ok": True,
                    "db": str(self.db_path),
                    "p4_asr_base": self.p4_asr_base,
                    "writing_api_base": self.writing_api_base,
                }
            )
            return
        if parsed.path.rstrip("/") == "/api/auth/me":
            self.handle_auth_me()
            return
        if parsed.path.rstrip("/") == "/api/student/progress":
            self.handle_student_progress()
            return
        if parsed.path.rstrip("/") == "/api/student/test-records":
            self.handle_student_test_records_get()
            return
        if parsed.path.rstrip("/") == "/api/student/speaking-best-scores":
            self.handle_student_speaking_best_scores_get()
            return
        if parsed.path.rstrip("/") == "/api/student/standards":
            self.handle_student_standards()
            return
        if parsed.path.rstrip("/") == "/api/student/wrong-words":
            self.handle_student_wrong_words_get()
            return
        if parsed.path.rstrip("/") == "/api/student/wrong-items":
            self.handle_student_wrong_items_get()
            return
        if parsed.path.rstrip("/") == "/api/student/word-mastery":
            self.handle_student_word_mastery_get()
            return
        if parsed.path.rstrip("/") == "/api/task/class-overview":
            self.handle_task_class_overview()
            return
        if parsed.path.rstrip("/") == "/api/task/units":
            self.handle_task_units_get()
            return
        if parsed.path.rstrip("/") == "/api/task/me/today":
            self.handle_task_me_today()
            return
        if parsed.path.startswith("/api/task/students/") and parsed.path.rstrip("/").endswith(
            "/gendu-assignment"
        ):
            self.handle_task_gendu_assignment_get()
            return
        if parsed.path.startswith("/api/task/students/") and parsed.path.rstrip("/").endswith(
            "/pack-preview"
        ):
            self.handle_task_pack_preview_get()
            return
        if parsed.path.startswith("/api/task/students/") and parsed.path.rstrip("/").endswith(
            "/plan"
        ):
            self.handle_task_student_plan_get()
            return
        if parsed.path.startswith("/api/task/students/") and parsed.path.rstrip("/").endswith(
            "/time-profile"
        ):
            self.handle_task_student_time_profile_get()
            return
        if parsed.path.rstrip("/") == "/api/teacher/students":
            self.handle_teacher_students_get()
            return
        if parsed.path.rstrip("/") == "/api/teacher/test-records":
            self.handle_teacher_test_records_get()
            return
        if parsed.path.rstrip("/") == "/api/teacher/overview":
            self.handle_teacher_overview()
            return
        if parsed.path.rstrip("/") == "/api/teacher/student-detail":
            self.handle_teacher_student_detail()
            return
        if parsed.path.rstrip("/") == "/api/teacher/standards":
            self.handle_teacher_standards_get()
            return
        if parsed.path.rstrip("/") == "/api/teacher/teachers":
            self.handle_teacher_teachers_get()
            return
        if parsed.path.startswith("/api/config"):
            self.handle_public_config()
            return
        if parsed.path.startswith("/api/writing"):
            if not self.require_logged_in_session():
                return
            self.proxy_writing_api("GET")
            return
        if parsed.path.startswith("/api/p4"):
            if not self.require_logged_in_session():
                return
            self.proxy_p4_api("GET")
            return

        # /tinglidanciceshi → /tinglidanciceshi/ ，避免相对脚本解析到站点根目录导致 DB 客户端 404
        path = parsed.path
        if path and not path.endswith("/"):
            candidate = (self.static_dir / Path(urllib.parse.unquote(path.lstrip("/")))).resolve()
            static_root = self.static_dir.resolve()
            try:
                candidate.relative_to(static_root)
                in_tree = True
            except ValueError:
                in_tree = False
            if in_tree and candidate.is_dir() and (candidate / "index.html").is_file():
                target = path + "/"
                if parsed.query:
                    target += "?" + parsed.query
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", target)
                self.end_headers()
                return

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if parsed.path.startswith("/api/writing"):
            if not self.require_logged_in_session():
                return
            self.proxy_writing_api("POST")
            return
        if parsed.path.startswith("/api/p4"):
            if not self.require_logged_in_session():
                return
            self.proxy_p4_api("POST")
            return
        if path == "/api/ai/messages":
            self.handle_ai_messages()
            return
        if path == "/api/auth/student/login":
            self.handle_student_login()
            return
        if path == "/api/auth/teacher/login":
            self.handle_teacher_login()
            return
        if path == "/api/auth/logout":
            self.handle_logout()
            return
        if path == "/api/student/change-password":
            self.handle_student_change_password()
            return
        if path == "/api/student/study-sessions":
            self.handle_student_study_sessions_post()
            return
        if path == "/api/student/test-records":
            self.handle_student_test_records_post()
            return
        if path == "/api/student/speaking-best-scores":
            self.handle_student_speaking_best_scores_post()
            return
        if path == "/api/student/wrong-words/apply":
            self.handle_student_wrong_words_apply()
            return
        if path == "/api/student/wrong-items/apply":
            self.handle_student_wrong_items_apply()
            return
        if path == "/api/student/word-mastery":
            self.handle_student_word_mastery_post()
            return
        if path == "/api/task/me/complete-study":
            self.handle_task_me_complete_study()
            return
        if path == "/api/task/me/gendu-practice":
            self.handle_task_me_gendu_practice()
            return
        if path == "/api/task/me/scope-progress":
            self.handle_task_me_scope_progress()
            return
        if path == "/api/task/me/submit-test":
            self.handle_task_me_submit_test()
            return
        if path.startswith("/api/task/students/") and path.endswith("/plan/insert-stage-test"):
            self.handle_task_insert_stage_test()
            return
        if path.startswith("/api/task/students/") and path.endswith("/pack-preview"):
            self.handle_task_pack_preview_post()
            return
        if path.startswith("/api/task/students/") and path.endswith("/gendu-assignment/clear"):
            self.handle_task_gendu_assignment_delete()
            return
        if path.startswith("/api/task/students/") and path.endswith("/gendu-assignment"):
            self.handle_task_gendu_assignment_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/plan-pause"):
            self.handle_task_plan_pause_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/plan-pause/clear"):
            self.handle_task_plan_pause_delete()
            return
        if path.startswith("/api/task/students/") and path.endswith("/clear-daily-schedule"):
            self.handle_task_clear_daily_schedule()
            return
        if path.startswith("/api/task/students/") and path.endswith("/plan"):
            self.handle_task_student_plan_put()
            return
        if path.startswith("/api/task/students/") and path.endswith("/time-profile"):
            self.handle_task_student_time_profile_put()
            return
        if path == "/api/teacher/students":
            self.handle_teacher_students_create()
            return
        if path == "/api/teacher/students/batch":
            self.handle_teacher_students_batch()
            return
        if path == "/api/teacher/students/reset-password":
            self.handle_teacher_students_reset_password()
            return
        if path == "/api/teacher/students/toggle-status":
            self.handle_teacher_students_toggle_status()
            return
        if path == "/api/teacher/students/update":
            self.handle_teacher_students_update()
            return
        if path == "/api/teacher/standards/update":
            self.handle_teacher_standards_update()
            return
        if path == "/api/teacher/teachers":
            self.handle_teacher_teachers_create()
            return
        if path == "/api/teacher/teachers/reset-password":
            self.handle_teacher_teachers_reset_password()
            return
        if path == "/api/teacher/teachers/toggle-status":
            self.handle_teacher_teachers_toggle_status()
            return
        if path == "/api/teacher/teachers/update":
            self.handle_teacher_teachers_update()
            return
        if parsed.path.startswith("/api/db"):
            # P2: generic /api/db is closed; use role-scoped APIs.
            self.send_json(
                {
                    "data": None,
                    "error": {
                        "message": "通用 /api/db 已关闭，请使用 /api/student/* 或 /api/teacher/*"
                    },
                },
                status=403,
            )
            return
        self.send_error(HTTPStatus.NOT_FOUND, "API not found")

    def proxy_p4_api(self, method: str) -> None:
        """Proxy /api/p4/* to the P4 ASR upstream (e.g. /api/p4/transcribe -> /transcribe)."""
        # Caller must verify session before invoking.
        parsed = urllib.parse.urlparse(self.path)
        rest = parsed.path[len("/api/p4") :] or "/"
        if not rest.startswith("/"):
            rest = "/" + rest
        if parsed.query:
            rest += "?" + parsed.query
        target = self.p4_asr_base.rstrip("/") + rest
        body = None
        headers: dict[str, str] = {"Accept": "application/json"}
        if method == "POST":
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length > 0 else b""
            content_type = self.headers.get("Content-Type")
            if content_type:
                headers["Content-Type"] = content_type
        try:
            req = urllib.request.Request(target, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read()
                status = getattr(resp, "status", 200)
                content_type = resp.headers.get("Content-Type", "application/json; charset=utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except Exception as exc:
            self.send_json(
                {
                    "error": f"P4 ASR 服务不可用（{exc}）。请确认 {self.p4_asr_base} 可访问。",
                    "recognizedText": "",
                    "text": "",
                },
                status=502,
            )

    def proxy_writing_api(self, method: str) -> None:
        # Caller must verify session before invoking.
        parsed = urllib.parse.urlparse(self.path)
        rest = parsed.path[len("/api/writing") :] or "/"
        if not rest.startswith("/"):
            rest = "/" + rest
        upstream_path = "/api" + rest
        if parsed.query:
            upstream_path += "?" + parsed.query
        target = self.writing_api_base.rstrip("/") + upstream_path
        body = None
        headers = {"Accept": "application/json"}
        if method == "POST":
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length > 0 else b"{}"
            headers["Content-Type"] = self.headers.get(
                "Content-Type", "application/json; charset=utf-8"
            )
        try:
            req = urllib.request.Request(target, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read()
                status = getattr(resp, "status", 200)
                content_type = resp.headers.get("Content-Type", "application/json; charset=utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except Exception as exc:
            message = (
                f"作文批改服务不可用（{exc}）。"
                "请先启动：cd sources/xiezuopigai/ielts-writing-backend && "
                "python -m uvicorn main:app --host 127.0.0.1 --port 8080"
            )
            self.send_json({"success": False, "message": message}, status=502)

    def translate_path(self, path: str) -> str:
        path = urllib.parse.urlparse(path).path
        rel = Path(urllib.parse.unquote(path.lstrip("/")))
        full = (self.static_dir / rel).resolve()
        static_root = self.static_dir.resolve()
        if static_root not in full.parents and full != static_root:
            return str(static_root)
        if full.is_dir():
            return str(full / "index.html")
        return str(full)

    def guess_type(self, path: str) -> str:
        if path.endswith(".js"):
            return "application/javascript"
        return mimetypes.guess_type(path)[0] or "application/octet-stream"


def writing_backend_healthy(base_url: str) -> bool:
    try:
        with urllib.request.urlopen(base_url.rstrip("/") + "/api/health", timeout=2) as resp:
            return getattr(resp, "status", 200) == 200
    except Exception:
        return False


def resolve_writing_python() -> str:
    """Prefer project venv so Debian/PEP 668 hosts can run writing AI deps."""
    for candidate in (
        ROOT / ".venv" / "bin" / "python",
        ROOT / ".venv" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate)
    return sys.executable


def maybe_start_writing_backend(base_url: str, auto_start: bool) -> Optional[subprocess.Popen]:
    if writing_backend_healthy(base_url):
        return None
    if not auto_start:
        print(
            "Writing backend not running. Start manually:\n"
            f"  cd {WRITING_BACKEND_DIR}\n"
            "  python -m uvicorn main:app --host 127.0.0.1 --port 8080"
        )
        return None
    if not (WRITING_BACKEND_DIR / "main.py").exists():
        print(f"Writing backend missing at {WRITING_BACKEND_DIR}")
        return None
    python_bin = resolve_writing_python()
    print(f"Starting writing backend at {base_url} with {python_bin} ...")
    proc = subprocess.Popen(
        [
            python_bin,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8080",
        ],
        cwd=str(WRITING_BACKEND_DIR),
    )
    for _ in range(30):
        time.sleep(0.5)
        if writing_backend_healthy(base_url):
            print("Writing backend is ready.")
            return proc
    print("Writing backend did not become healthy in time.")
    return proc


def resolve_configured_path(raw_path: str) -> Path:
    normalised = os.path.normpath(str(raw_path))
    return Path(normalised).expanduser().absolute()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=49182)
    parser.add_argument("--static-dir", default=str(DEFAULT_STATIC_DIR))
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    parser.add_argument(
        "--writing-api-base",
        default=DEFAULT_WRITING_API_BASE,
        help="Upstream writing FastAPI base URL used by /api/writing/* proxy",
    )
    parser.add_argument(
        "--no-writing-backend",
        action="store_true",
        help="Do not auto-start the writing FastAPI backend",
    )
    parser.add_argument(
        "--p4-asr-base",
        default=DEFAULT_P4_ASR_BASE,
        help="P4 ASR base URL for /api/p4/* proxy and /api/health",
    )
    args = parser.parse_args(argv)

    static_dir = resolve_configured_path(args.static_dir)
    db_path = resolve_configured_path(args.db)
    init_db(db_path, bind_host=args.host)

    ai_env = load_ai_env()
    if ai_env:
        print(f"AI config loaded: {ai_env}")
    else:
        print(f"AI config missing: {ROOT / 'config' / 'ai.env'} (AI features may be disabled)")

    writing_api_base = str(args.writing_api_base).rstrip("/")
    writing_proc = maybe_start_writing_backend(
        writing_api_base,
        auto_start=not args.no_writing_backend,
    )

    LocalHandler.static_dir = static_dir
    LocalHandler.db_path = db_path
    LocalHandler.session_secret = load_session_secret()
    LocalHandler.writing_api_base = writing_api_base
    LocalHandler.p4_asr_base = str(args.p4_asr_base).rstrip("/")
    server = ThreadingHTTPServer((args.host, args.port), LocalHandler)
    print(f"Serving {static_dir} on http://{args.host}:{args.port}")
    print(f"SQLite database: {db_path}")
    print(f"Writing API proxy target: {LocalHandler.writing_api_base}")
    try:
        server.serve_forever()
    finally:
        if writing_proc and writing_proc.poll() is None:
            writing_proc.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
