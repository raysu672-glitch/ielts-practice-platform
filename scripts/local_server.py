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
DEFAULT_STATIC_DIR = ROOT / "sources"
DEFAULT_DB_PATH = ROOT / "data" / "ielts_local.db"
DEFAULT_P4_ASR_BASE = "https://p4.oyenglish.com.cn"
DEFAULT_WRITING_API_BASE = "http://127.0.0.1:8080"
WRITING_BACKEND_DIR = ROOT / "sources" / "xiezuopigai" / "ielts-writing-backend"

ALLOWED_TABLES = {
    "teacher_config",
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


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(db_path)) as conn:
        conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS teacher_config (
                id INTEGER PRIMARY KEY DEFAULT 1,
                access_password TEXT NOT NULL DEFAULT 'sjdh4405',
                school_name TEXT DEFAULT '藕叶英语',
                updated_at TEXT DEFAULT ({now_sql()})
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                default_password TEXT DEFAULT '123456',
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
                word TEXT NOT NULL,
                wrong_count INTEGER DEFAULT 1,
                correct_streak INTEGER DEFAULT 0,
                last_tested TEXT DEFAULT ({now_sql()}),
                is_mastered INTEGER DEFAULT 0,
                UNIQUE(student_id, word)
            );

            CREATE INDEX IF NOT EXISTS idx_test_records_student_id ON test_records(student_id);
            CREATE INDEX IF NOT EXISTS idx_test_records_created_at ON test_records(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_test_records_module_type ON test_records(module_type);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_student_id ON study_sessions(student_id);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_module_type ON study_sessions(module_type);
            CREATE INDEX IF NOT EXISTS idx_study_sessions_created_at ON study_sessions(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);
            CREATE INDEX IF NOT EXISTS idx_word_mastery_student_id ON word_mastery(student_id);
            """
        )

        conn.execute(
            """
            INSERT INTO teacher_config (id, access_password, school_name)
            VALUES (1, 'sjdh4405', '藕叶英语')
            ON CONFLICT(id) DO NOTHING
            """
        )

        standards = [
            ("dictation", "听力1000词", 70, 80, 90),
            ("reading_synonym", "阅读同义替换", 70, 80, 90),
            ("writing_phrase", "写作词伙", 50, 70, 90),
            ("sentence", "长难句分析", 60, 80, 80),
            ("listening_synonym", "听力同义替换", 70, 80, 90),
            ("writing_translate", "写作句子翻译", 50, 70, 90),
            ("listening_p4_speed", "听力P4跟读倍速", 70, 80, 90),
            ("writing_correction", "作文批改", 1, 1, 1),
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
                student_id, name, password, default_password,
                is_password_changed, target_score, status
            )
            VALUES ('2025001', '测试学生', '123456', '123456', 0, 6.5, 'active')
            ON CONFLICT(student_id) DO NOTHING
            """
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

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path.startswith("/api/health"):
            self.send_json(
                {
                    "ok": True,
                    "db": str(self.db_path),
                    "p4_asr_base": self.p4_asr_base,
                    "writing_api_base": self.writing_api_base,
                }
            )
            return
        if self.path.startswith("/api/writing"):
            self.proxy_writing_api("GET")
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/writing"):
            self.proxy_writing_api("POST")
            return
        if not self.path.startswith("/api/db"):
            self.send_error(HTTPStatus.NOT_FOUND, "API not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            result = query_db(self.db_path, payload)
            self.send_json(result)
        except Exception as exc:
            self.send_json({"data": None, "error": {"message": str(exc)}}, status=500)

    def proxy_writing_api(self, method: str) -> None:
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

    def send_json(self, data: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def writing_backend_healthy(base_url: str) -> bool:
    try:
        with urllib.request.urlopen(base_url.rstrip("/") + "/api/health", timeout=2) as resp:
            return getattr(resp, "status", 200) == 200
    except Exception:
        return False


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
    print(f"Starting writing backend at {base_url} ...")
    proc = subprocess.Popen(
        [
            sys.executable,
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
        help="P4 ASR base URL reported by /api/health",
    )
    args = parser.parse_args(argv)

    static_dir = resolve_configured_path(args.static_dir)
    db_path = resolve_configured_path(args.db)
    init_db(db_path)

    writing_api_base = str(args.writing_api_base).rstrip("/")
    writing_proc = maybe_start_writing_backend(
        writing_api_base,
        auto_start=not args.no_writing_backend,
    )

    LocalHandler.static_dir = static_dir
    LocalHandler.db_path = db_path
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
