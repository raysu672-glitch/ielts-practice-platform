"""Teacher-scoped API helpers (session identity is enforced by the caller)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Optional


from password_utils import (
    STUDENT_INITIAL_PASSWORD,
    TEACHER_INITIAL_PASSWORD,
    hash_password,
)

PASSWORD_RESET_ACTION = "student.password_reset"

# Tables whose student_id column can be remapped with a plain UPDATE.
_SIMPLE_STUDENT_ID_TABLES = (
    ("test_records", "student_id"),
    ("study_sessions", "student_id"),
    ("gendu_practice_events", "student_id"),
    ("mock_speaking_exams", "student_id"),
    ("daily_tasks", "student_id"),
    ("plan_items", "student_id"),
    ("plan_items_draft", "student_id"),
    ("student_debug_events", "student_id"),
)

# Tables with UNIQUE/PK including student_id: remap when no conflict, else drop source.
_UNIQUE_STUDENT_ID_TABLES = (
    ("word_mastery", "student_id"),
    ("wrong_words", "student_id"),
    ("wrong_items", "student_id"),
    ("speaking_best_scores", "student_id"),
    ("student_time_profiles", "student_id"),
    ("student_module_daily_quota", "student_id"),
    ("plan_draft_meta", "student_id"),
    ("task_unit_progress", "student_id"),
    ("student_plan_pause", "student_id"),
    ("student_gendu_assignment", "student_id"),
    ("jianya_submissions", "student_id"),
    ("jianya_drafts", "student_id"),
    ("jianya_recipients", "student_id"),
    ("jianya_reviews", "student_id"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _utc_days_ago(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    )[:-3] + "Z"


def _table_exists(conn: Any, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return bool(row)


def parse_details(item: dict[str, Any]) -> None:
    details = item.get("details")
    if isinstance(details, str):
        try:
            item["details"] = json.loads(details)
        except json.JSONDecodeError:
            pass


def public_student_row(row: dict[str, Any]) -> dict[str, Any]:
    out = {
        "student_id": row.get("student_id"),
        "name": row.get("name"),
        "is_password_changed": bool(row.get("is_password_changed")),
        "target_score": row.get("target_score"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }
    if "resets_7d" in row:
        out["resets_7d"] = int(row.get("resets_7d") or 0)
    return out


def password_reset_counts_7d(conn: Any) -> dict[str, int]:
    """Map student_id -> password reset count in the last 7 days."""
    if not _table_exists(conn, "activity_events"):
        return {}
    cutoff = _utc_days_ago(7)
    rows = conn.execute(
        """
        SELECT target_student_id AS sid, COUNT(*) AS c
        FROM activity_events
        WHERE action = ?
          AND created_at >= ?
          AND target_student_id IS NOT NULL
          AND target_student_id != ''
        GROUP BY target_student_id
        """,
        (PASSWORD_RESET_ACTION, cutoff),
    ).fetchall()
    return {str(row["sid"]): int(row["c"] or 0) for row in rows}


def public_teacher_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "teacher_id": row.get("teacher_id"),
        "name": row.get("name"),
        "position": row.get("position") or "",
        "subjects": row.get("subjects") or "",
        "status": row.get("status"),
        "is_password_changed": bool(row.get("is_password_changed")),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "is_admin": row.get("teacher_id") == "admin",
    }


def list_students(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM students ORDER BY created_at DESC"
        ).fetchall()
    ]
    reset_map = password_reset_counts_7d(conn)
    result: list[dict[str, Any]] = []
    for item in rows:
        item["resets_7d"] = reset_map.get(str(item.get("student_id") or ""), 0)
        result.append(public_student_row(item))
    return result


def lookup_student_by_id(conn: Any, student_id: str) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """Public lookup for login name confirmation. No password fields."""
    sid = str(student_id or "").strip()
    if not sid:
        return None, "请输入学号"
    row = conn.execute(
        "SELECT student_id, name, status FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学号不存在"
    item = dict(row)
    return {
        "student_id": item.get("student_id"),
        "name": item.get("name") or "",
        "status": item.get("status") or "active",
    }, None


def _student_activity_stats(conn: Any, student_id: str) -> dict[str, Any]:
    sid = str(student_id or "").strip()
    stats = {
        "test_records": 0,
        "study_sessions": 0,
        "last_login_at": "",
    }
    if _table_exists(conn, "test_records"):
        stats["test_records"] = int(
            conn.execute(
                "SELECT COUNT(*) AS c FROM test_records WHERE student_id = ?",
                (sid,),
            ).fetchone()["c"]
            or 0
        )
    if _table_exists(conn, "study_sessions"):
        stats["study_sessions"] = int(
            conn.execute(
                "SELECT COUNT(*) AS c FROM study_sessions WHERE student_id = ?",
                (sid,),
            ).fetchone()["c"]
            or 0
        )
    if _table_exists(conn, "activity_events"):
        row = conn.execute(
            """
            SELECT created_at FROM activity_events
            WHERE action = 'auth.login'
              AND (
                target_student_id = ?
                OR (actor_role = 'student' AND actor_id = ?)
              )
            ORDER BY created_at DESC LIMIT 1
            """,
            (sid, sid),
        ).fetchone()
        if row:
            stats["last_login_at"] = str(row["created_at"] or "")
    return stats


def list_duplicate_name_groups(conn: Any) -> list[dict[str, Any]]:
    """Groups of students sharing the same trimmed name (2+ accounts)."""
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT student_id, name, status, target_score, is_password_changed,
                   created_at, updated_at
            FROM students
            ORDER BY name COLLATE NOCASE, created_at
            """
        ).fetchall()
    ]
    by_name: dict[str, list[dict[str, Any]]] = {}
    for item in rows:
        key = str(item.get("name") or "").strip()
        if not key:
            continue
        by_name.setdefault(key, []).append(item)
    groups: list[dict[str, Any]] = []
    for name, members in by_name.items():
        if len(members) < 2:
            continue
        enriched = []
        for m in members:
            pub = public_student_row(m)
            pub.update(_student_activity_stats(conn, str(m["student_id"])))
            enriched.append(pub)
        groups.append({"name": name, "count": len(enriched), "students": enriched})
    groups.sort(key=lambda g: (-int(g["count"]), str(g["name"])))
    return groups


def _remap_student_id_simple(conn: Any, table: str, column: str, keep_id: str, drop_id: str) -> int:
    if not _table_exists(conn, table):
        return 0
    cur = conn.execute(
        f"UPDATE {table} SET {column} = ? WHERE {column} = ?",
        (keep_id, drop_id),
    )
    return int(cur.rowcount or 0)


def _remap_student_id_unique(conn: Any, table: str, column: str, keep_id: str, drop_id: str) -> int:
    """Move rows from drop_id to keep_id; on UNIQUE conflict keep keep_id and drop source."""
    if not _table_exists(conn, table):
        return 0
    moved = 0
    # First delete source rows that would collide with keep_id on any unique constraint.
    # Safer approach: try update one-by-one via rowid when available.
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    has_rowid = "rowid" not in {c.lower() for c in cols}
    if has_rowid:
        rows = conn.execute(
            f"SELECT rowid AS _rid FROM {table} WHERE {column} = ?",
            (drop_id,),
        ).fetchall()
        for row in rows:
            rid = row["_rid"]
            try:
                conn.execute(
                    f"UPDATE {table} SET {column} = ? WHERE rowid = ?",
                    (keep_id, rid),
                )
                moved += 1
            except Exception:
                conn.execute(f"DELETE FROM {table} WHERE rowid = ?", (rid,))
        return moved
    # No rowid path: bulk update then delete leftovers.
    try:
        cur = conn.execute(
            f"UPDATE {table} SET {column} = ? WHERE {column} = ?",
            (keep_id, drop_id),
        )
        return int(cur.rowcount or 0)
    except Exception:
        cur = conn.execute(f"DELETE FROM {table} WHERE {column} = ?", (drop_id,))
        return -int(cur.rowcount or 0)


def merge_students(
    conn: Any,
    *,
    keep_student_id: str,
    merge_student_ids: list[str],
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """Merge duplicate accounts into keep_student_id; deactivate merged-away rows."""
    keep_id = str(keep_student_id or "").strip()
    drop_ids = [
        str(x or "").strip()
        for x in (merge_student_ids or [])
        if str(x or "").strip() and str(x or "").strip() != keep_id
    ]
    # de-dupe preserving order
    seen: set[str] = set()
    ordered_drops: list[str] = []
    for sid in drop_ids:
        if sid in seen:
            continue
        seen.add(sid)
        ordered_drops.append(sid)
    if not keep_id:
        return None, "请选择保留学号"
    if not ordered_drops:
        return None, "请选择要合并的学号"
    keep_row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (keep_id,),
    ).fetchone()
    if not keep_row:
        return None, "保留学号不存在"
    for sid in ordered_drops:
        if not conn.execute(
            "SELECT 1 FROM students WHERE student_id = ?", (sid,)
        ).fetchone():
            return None, f"学号不存在：{sid}"

    remapped: dict[str, int] = {}
    for drop_id in ordered_drops:
        for table, column in _SIMPLE_STUDENT_ID_TABLES:
            remapped[table] = remapped.get(table, 0) + _remap_student_id_simple(
                conn, table, column, keep_id, drop_id
            )
        for table, column in _UNIQUE_STUDENT_ID_TABLES:
            n = _remap_student_id_unique(conn, table, column, keep_id, drop_id)
            remapped[table] = remapped.get(table, 0) + abs(n)
        if _table_exists(conn, "activity_events"):
            conn.execute(
                """
                UPDATE activity_events
                SET target_student_id = ?
                WHERE target_student_id = ?
                """,
                (keep_id, drop_id),
            )
            conn.execute(
                """
                UPDATE activity_events
                SET actor_id = ?
                WHERE actor_role = 'student' AND actor_id = ?
                """,
                (keep_id, drop_id),
            )
        keep_name = str(dict(keep_row).get("name") or "")
        conn.execute(
            """
            UPDATE students
            SET status = 'inactive',
                name = ?,
                updated_at = ?
            WHERE student_id = ?
            """,
            (
                f"[已合并到{keep_id}] {keep_name}".strip()[:80],
                utc_now(),
                drop_id,
            ),
        )

    # If keep was inactive, reactivate it.
    conn.execute(
        """
        UPDATE students
        SET status = 'active', updated_at = ?
        WHERE student_id = ? AND status != 'active'
        """,
        (utc_now(), keep_id),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (keep_id,),
    ).fetchone()
    return {
        "keep": public_student_row(dict(updated)),
        "merged_ids": ordered_drops,
        "remapped": remapped,
    }, None


def next_student_id(conn: Any) -> str:
    row = conn.execute(
        "SELECT student_id FROM students ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    if not row:
        return "2025001"
    try:
        return str(int(row["student_id"]) + 1)
    except (TypeError, ValueError):
        return "2025001"


def create_student(
    conn: Any,
    *,
    name: str,
    target_score: float = 6.5,
    student_id: Optional[str] = None,
) -> tuple[Optional[dict[str, Any]], Optional[str], Optional[str]]:
    name = str(name or "").strip()
    if not name:
        return None, "请输入姓名", None
    try:
        target = float(target_score)
    except (TypeError, ValueError):
        return None, "目标分无效", None
    if target not in (6, 6.5, 7):
        return None, "目标分仅支持 6 / 6.5 / 7", None
    sid = str(student_id or "").strip() or next_student_id(conn)
    exists = conn.execute(
        "SELECT 1 FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if exists:
        return None, "学号已存在", None
    initial_password = STUDENT_INITIAL_PASSWORD
    now = utc_now()
    conn.execute(
        """
        INSERT INTO students (
            student_id, name, password,
            is_password_changed, target_score, status, created_at, updated_at
        ) VALUES (?, ?, ?, 0, ?, 'active', ?, ?)
        """,
        (sid, name, hash_password(initial_password), target, now, now),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    return public_student_row(dict(row)), None, initial_password


def update_student(
    conn: Any,
    *,
    student_id: str,
    name: str,
    target_score: float = 6.5,
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    name = str(name or "").strip()
    if not sid:
        return None, "缺少学号"
    if not name:
        return None, "请输入姓名"
    try:
        target = float(target_score)
    except (TypeError, ValueError):
        return None, "目标分无效"
    if target not in (6, 6.5, 7):
        return None, "目标分仅支持 6 / 6.5 / 7"
    row = conn.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    conn.execute(
        """
        UPDATE students
        SET name = ?, target_score = ?, updated_at = ?
        WHERE student_id = ?
        """,
        (name, target, utc_now(), sid),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    return public_student_row(dict(updated)), None


def create_students_batch(
    conn: Any,
    items: list[dict[str, Any]],
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    if not items:
        return None, "没有有效的学生数据"
    start_id = int(next_student_id(conn))
    created: list[dict[str, Any]] = []
    offset = 0
    for item in items:
        name = str((item or {}).get("name") or "").strip()
        if not name:
            continue
        target = (item or {}).get("target_score", (item or {}).get("targetScore", 6.5))
        student, err, _initial_password = create_student(
            conn,
            name=name,
            target_score=target,
            student_id=str(start_id + offset),
        )
        if err:
            return None, err
        created.append(student or {})
        offset += 1
    if not created:
        return None, "没有有效的学生数据"
    return {"count": len(created), "students": created}, None


def reset_student_password(conn: Any, student_id: str) -> tuple[Optional[str], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    initial_password = STUDENT_INITIAL_PASSWORD
    conn.execute(
        """
        UPDATE students
        SET password = ?, is_password_changed = 0, updated_at = ?
        WHERE student_id = ?
        """,
        (hash_password(initial_password), utc_now(), sid),
    )
    conn.commit()
    return initial_password, None


def toggle_student_status(
    conn: Any, student_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    item = dict(row)
    new_status = "inactive" if item.get("status") == "active" else "active"
    conn.execute(
        "UPDATE students SET status = ?, updated_at = ? WHERE student_id = ?",
        (new_status, utc_now(), sid),
    )
    conn.commit()
    item["status"] = new_status
    return public_student_row(item), None


def list_test_records(conn: Any, limit: int = 1000) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT r.*, s.name AS student_name
            FROM test_records r
            LEFT JOIN students s ON s.student_id = r.student_id
            ORDER BY r.created_at DESC
            LIMIT ?
            """,
            (max(1, min(int(limit), 5000)),),
        ).fetchall()
    ]
    for item in rows:
        parse_details(item)
        item["is_passed"] = bool(item.get("is_passed"))
        item["students"] = {"name": item.get("student_name")} if item.get("student_name") else None
    return rows


def load_overview(conn: Any) -> dict[str, Any]:
    students = list_students(conn)
    records = [dict(row) for row in conn.execute("SELECT * FROM test_records").fetchall()]
    sessions = [dict(row) for row in conn.execute("SELECT * FROM study_sessions").fetchall()]
    for item in records:
        parse_details(item)
        item["is_passed"] = bool(item.get("is_passed"))
    for item in sessions:
        parse_details(item)
    return {
        "students": students,
        "test_records": records,
        "study_sessions": sessions,
    }


def load_student_detail(
    conn: Any, student_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    records = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM test_records WHERE student_id = ? ORDER BY created_at DESC",
            (sid,),
        ).fetchall()
    ]
    sessions = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM study_sessions WHERE student_id = ? ORDER BY created_at DESC",
            (sid,),
        ).fetchall()
    ]
    wrong_words = [
        dict(r)
        for r in conn.execute(
            """
            SELECT * FROM wrong_words
            WHERE student_id = ? AND is_mastered = 0
            ORDER BY last_tested DESC
            """,
            (sid,),
        ).fetchall()
    ]
    for item in records + sessions:
        parse_details(item)
    for item in records:
        item["is_passed"] = bool(item.get("is_passed"))
    for item in wrong_words:
        item["is_mastered"] = bool(item.get("is_mastered"))

    student = public_student_row(dict(row))
    mock_exams = [
        r
        for r in records
        if str(r.get("test_type") or "") == "mock_exam"
        and str(r.get("module_type") or "") in ("mock_reading", "mock_listening")
    ]

    wrong_book_counts: dict[str, int] = {}
    try:
        from student_api import load_wrong_book_counts

        wrong_book_counts = load_wrong_book_counts(conn, sid)
    except Exception:
        wrong_book_counts = {}

    task_overview: Optional[dict[str, Any]] = None
    try:
        from task_api import student_task_snapshot

        task_overview = student_task_snapshot(
            conn, sid, str(student.get("name") or "")
        )
    except Exception:
        task_overview = None

    return {
        "student": student,
        "test_records": records,
        "study_sessions": sessions,
        "wrong_words": wrong_words,
        "wrong_book_counts": wrong_book_counts,
        "mock_exams": mock_exams,
        "task_overview": task_overview,
    }, None


def list_standards(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM pass_standards WHERE is_active = 1 ORDER BY module_type"
        ).fetchall()
    ]
    for item in rows:
        item["is_active"] = bool(item.get("is_active"))
    return rows


def update_standard(
    conn: Any,
    module_type: str,
    payload: dict[str, Any],
) -> Optional[str]:
    module_type = str(module_type or "").strip()
    if not module_type:
        return "缺少模块类型"
    row = conn.execute(
        "SELECT * FROM pass_standards WHERE module_type = ?",
        (module_type,),
    ).fetchone()
    if not row:
        return "模块标准不存在"
    fields: dict[str, Any] = {}
    for key in ("score_6", "score_6_5", "score_7"):
        if key in payload and payload[key] is not None:
            try:
                fields[key] = float(payload[key])
            except (TypeError, ValueError):
                return f"{key} 无效"
    if not fields:
        return "没有可更新的字段"
    fields["updated_at"] = utc_now()
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(
        f"UPDATE pass_standards SET {sets} WHERE module_type = ?",
        list(fields.values()) + [module_type],
    )
    conn.commit()
    return None


def list_teachers(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM teachers ORDER BY created_at DESC"
        ).fetchall()
    ]
    return [public_teacher_row(item) for item in rows]


def create_teacher(
    conn: Any,
    *,
    teacher_id: str,
    name: str,
    position: str = "",
    subjects: str = "",
) -> tuple[Optional[dict[str, Any]], Optional[str], Optional[str]]:
    tid = str(teacher_id or "").strip().lower()
    name = str(name or "").strip()
    if not name:
        return None, "请输入姓名", None
    if not tid:
        return None, "请输入登录账号", None
    if tid == "admin":
        return None, "不能使用保留账号 admin", None
    if not all(ch.isalnum() or ch == "_" for ch in tid) or tid != tid.lower():
        return None, "账号仅支持小写字母、数字、下划线", None
    exists = conn.execute(
        "SELECT 1 FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if exists:
        return None, "账号已存在", None
    now = utc_now()
    initial_password = TEACHER_INITIAL_PASSWORD
    conn.execute(
        """
        INSERT INTO teachers (
            teacher_id, name, password,
            is_password_changed, position, subjects, status, created_at, updated_at
        ) VALUES (?, ?, ?, 0, ?, ?, 'active', ?, ?)
        """,
        (
            tid,
            name,
            hash_password(initial_password),
            position or "",
            subjects or "",
            now,
            now,
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    return public_teacher_row(dict(row)), None, initial_password


def update_teacher(
    conn: Any,
    *,
    teacher_id: str,
    name: str,
    position: str = "",
    subjects: str = "",
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    tid = str(teacher_id or "").strip().lower()
    name = str(name or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能修改管理员账号"
    if not name:
        return None, "请输入姓名"
    row = conn.execute(
        "SELECT teacher_id FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    conn.execute(
        """
        UPDATE teachers
        SET name = ?, position = ?, subjects = ?, updated_at = ?
        WHERE teacher_id = ?
        """,
        (name, position or "", subjects or "", utc_now(), tid),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    return public_teacher_row(dict(updated)), None


def reset_teacher_password(conn: Any, teacher_id: str) -> tuple[Optional[str], Optional[str]]:
    tid = str(teacher_id or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能重置管理员密码"
    row = conn.execute(
        "SELECT teacher_id FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    initial_password = TEACHER_INITIAL_PASSWORD
    conn.execute(
        """
        UPDATE teachers
        SET password = ?, is_password_changed = 0, updated_at = ?
        WHERE teacher_id = ?
        """,
        (hash_password(initial_password), utc_now(), tid),
    )
    conn.commit()
    return initial_password, None


def toggle_teacher_status(
    conn: Any, teacher_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    tid = str(teacher_id or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能禁用管理员"
    row = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    item = dict(row)
    new_status = "inactive" if item.get("status") == "active" else "active"
    conn.execute(
        "UPDATE teachers SET status = ?, updated_at = ? WHERE teacher_id = ?",
        (new_status, utc_now(), tid),
    )
    conn.commit()
    item["status"] = new_status
    return public_teacher_row(item), None
