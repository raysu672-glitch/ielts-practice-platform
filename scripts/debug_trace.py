"""Student debug trace: every client action and student API result.

Stored apart from ``activity_events``. The teacher timeline must not read this
table. Retention is 30 days. Passwords are never stored.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

RETENTION_DAYS = 30
MAX_BATCH = 40
_ACTION_RE = re.compile(r"^[a-zA-Z0-9._:-]{1,40}$")
_SECRET_KEYS = ("password", "passwd", "token", "secret", "cookie", "authorization")


def ensure_debug_trace_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS student_debug_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            client_at TEXT NOT NULL DEFAULT '',
            student_id TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'client',
            action TEXT NOT NULL,
            page TEXT NOT NULL DEFAULT '',
            target TEXT NOT NULL DEFAULT '',
            detail_json TEXT NOT NULL DEFAULT '{}'
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_debug_student_id
        ON student_debug_events(student_id, id DESC)
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_debug_created
        ON student_debug_events(created_at)
        """
    )
    conn.commit()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _clip(value: Any, limit: int) -> str:
    text = str(value or "").replace("\x00", "").strip()
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def _scrub(value: Any, depth: int = 0) -> Any:
    if depth > 4:
        return None
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in list(value.items())[:30]:
            name = str(key)
            if any(word in name.lower() for word in _SECRET_KEYS):
                out[name] = ""
                continue
            out[_clip(name, 40)] = _scrub(item, depth + 1)
        return out
    if isinstance(value, list):
        return [_scrub(item, depth + 1) for item in value[:20]]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return _clip(value, 200)


def prune_debug_events(
    conn: sqlite3.Connection, *, retention_days: int = RETENTION_DAYS
) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=max(1, int(retention_days)))
    cutoff_iso = cutoff.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    cur = conn.execute(
        "DELETE FROM student_debug_events WHERE created_at < ?", (cutoff_iso,)
    )
    conn.commit()
    return int(cur.rowcount or 0)


def log_student_debug_events(
    conn: sqlite3.Connection,
    *,
    student_id: str,
    events: list[dict[str, Any]],
    source: str = "client",
) -> dict[str, Any]:
    """Append a batch. Unknown shapes are skipped, not raised, so a bad
    client event cannot fail the student's real request path."""
    ensure_debug_trace_tables(conn)
    sid = _clip(student_id, 64)
    if not sid:
        raise ValueError("缺少学生")
    if not isinstance(events, list) or not events:
        raise ValueError("events 不能为空")
    source_name = "server" if source == "server" else "client"
    saved = 0
    for raw in events[:MAX_BATCH]:
        if not isinstance(raw, dict):
            continue
        action = str(raw.get("action") or "").strip()
        if not _ACTION_RE.match(action):
            continue
        detail = raw.get("detail")
        if not isinstance(detail, dict):
            detail = {}
        detail_json = json.dumps(_scrub(detail), ensure_ascii=False)
        if len(detail_json) > 2000:
            detail_json = detail_json[:1990] + "…"
        conn.execute(
            """
            INSERT INTO student_debug_events (
                created_at, client_at, student_id, source, action, page, target, detail_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _utc_now_iso(),
                _clip(raw.get("t") or raw.get("client_at") or "", 40),
                sid,
                source_name,
                action,
                _clip(raw.get("page") or "", 240),
                _clip(raw.get("target") or "", 160),
                detail_json,
            ),
        )
        saved += 1
    conn.commit()
    if saved:
        row = conn.execute("SELECT MAX(id) AS id FROM student_debug_events").fetchone()
        if row and int(row["id"] or 0) % 50 == 0:
            prune_debug_events(conn)
    return {"saved": saved}


def list_student_debug_events(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """For tests and offline diagnosis. Not used by the teacher timeline."""
    ensure_debug_trace_tables(conn)
    limit = max(1, min(int(limit or 200), 500))
    rows = conn.execute(
        """
        SELECT id, created_at, client_at, student_id, source, action, page, target, detail_json
        FROM student_debug_events
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (_clip(student_id, 64), limit),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        try:
            item["detail"] = json.loads(item.pop("detail_json") or "{}")
        except json.JSONDecodeError:
            item["detail"] = {}
            item.pop("detail_json", None)
        out.append(item)
    return out
