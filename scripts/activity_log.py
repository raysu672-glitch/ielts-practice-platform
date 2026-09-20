"""Activity event log: who did what at which second (90-day retention)."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")
RETENTION_DAYS = 90

# Allowed action prefixes for client-reported events (students).
STUDENT_ACTION_PREFIXES = (
    "task.",
    "module.",
    "study.",
    "test.",
    "synonym.",
    "listening.",
    "lsyn.",
    "sentence.",
    "phrase.",
    "translate.",
    "gendu.",
    "speaking.",
)


def ensure_activity_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            actor_id TEXT NOT NULL,
            actor_name TEXT NOT NULL DEFAULT '',
            action TEXT NOT NULL,
            module_type TEXT NOT NULL DEFAULT '',
            target_student_id TEXT NOT NULL DEFAULT '',
            plan_item_id INTEGER,
            unit_id TEXT NOT NULL DEFAULT '',
            summary TEXT NOT NULL DEFAULT '',
            detail_json TEXT NOT NULL DEFAULT '{}',
            ip TEXT NOT NULL DEFAULT ''
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_activity_created
        ON activity_events(created_at DESC)
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_activity_actor
        ON activity_events(actor_role, actor_id, created_at DESC)
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_activity_target_student
        ON activity_events(target_student_id, created_at DESC)
        """
    )
    conn.commit()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def prune_old_activity_events(
    conn: sqlite3.Connection, *, retention_days: int = RETENTION_DAYS
) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=max(1, int(retention_days)))
    cutoff_iso = cutoff.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    cur = conn.execute(
        "DELETE FROM activity_events WHERE created_at < ?", (cutoff_iso,)
    )
    conn.commit()
    return int(cur.rowcount or 0)


def log_activity(
    conn: sqlite3.Connection,
    *,
    actor_role: str,
    actor_id: str,
    action: str,
    actor_name: str = "",
    module_type: str = "",
    target_student_id: str = "",
    plan_item_id: Optional[int] = None,
    unit_id: str = "",
    summary: str = "",
    detail: Optional[dict[str, Any]] = None,
    ip: str = "",
    created_at: Optional[str] = None,
    prune_occasionally: bool = True,
) -> int:
    ensure_activity_tables(conn)
    action = str(action or "").strip()[:120]
    if not action:
        raise ValueError("缺少 action")
    actor_role = str(actor_role or "").strip()[:20] or "unknown"
    actor_id = str(actor_id or "").strip()[:64]
    if not actor_id:
        raise ValueError("缺少 actor_id")
    detail_json = json.dumps(detail or {}, ensure_ascii=False)
    if len(detail_json) > 4000:
        detail_json = detail_json[:3990] + "…"
    cur = conn.execute(
        """
        INSERT INTO activity_events (
            created_at, actor_role, actor_id, actor_name, action,
            module_type, target_student_id, plan_item_id, unit_id,
            summary, detail_json, ip
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at or _utc_now_iso(),
            actor_role,
            actor_id,
            str(actor_name or "")[:80],
            action,
            str(module_type or "")[:64],
            str(target_student_id or "")[:64],
            int(plan_item_id) if plan_item_id is not None else None,
            str(unit_id or "")[:80],
            str(summary or "")[:240],
            detail_json,
            str(ip or "")[:64],
        ),
    )
    conn.commit()
    event_id = int(cur.lastrowid or 0)
    # Cheap retention: prune about once per ~50 writes
    if prune_occasionally and event_id and event_id % 50 == 0:
        prune_old_activity_events(conn)
    return event_id


def _action_allowed_for_student(action: str) -> bool:
    a = str(action or "")
    return any(a.startswith(p) for p in STUDENT_ACTION_PREFIXES)


def log_student_client_events(
    conn: sqlite3.Connection,
    *,
    student_id: str,
    student_name: str = "",
    events: list[dict[str, Any]],
    ip: str = "",
) -> dict[str, Any]:
    """Accept a batch of client-reported key actions from the student app."""
    ensure_activity_tables(conn)
    if not isinstance(events, list) or not events:
        raise ValueError("events 不能为空")
    if len(events) > 50:
        raise ValueError("单次最多 50 条")
    saved = 0
    for raw in events:
        if not isinstance(raw, dict):
            continue
        action = str(raw.get("action") or "").strip()
        if not _action_allowed_for_student(action):
            continue
        detail = raw.get("detail")
        if detail is not None and not isinstance(detail, dict):
            detail = {"value": detail}
        log_activity(
            conn,
            actor_role="student",
            actor_id=student_id,
            actor_name=student_name,
            action=action,
            module_type=str(raw.get("module_type") or ""),
            target_student_id=student_id,
            plan_item_id=raw.get("plan_item_id"),
            unit_id=str(raw.get("unit_id") or ""),
            summary=str(raw.get("summary") or ""),
            detail=detail if isinstance(detail, dict) else {},
            ip=ip,
            prune_occasionally=False,
        )
        saved += 1
    if saved:
        prune_old_activity_events(conn)
    return {"saved": saved}


def _china_day_utc_bounds(ymd: str) -> tuple[str, str]:
    """Return [start, end) UTC ISO bounds for a China calendar day YYYY-MM-DD."""
    day = datetime.strptime(str(ymd).strip()[:10], "%Y-%m-%d").replace(tzinfo=SHANGHAI)
    start_utc = day.astimezone(timezone.utc)
    end_utc = (day + timedelta(days=1)).astimezone(timezone.utc)
    return (
        start_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        end_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    )


def list_student_activity(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    limit: int = 200,
    before_id: Optional[int] = None,
    action_prefix: str = "",
    on_date: str = "",
    page: int = 1,
    page_size: int = 30,
    paginate: bool = False,
) -> dict[str, Any]:
    """List activity for a student.

    Empty on_date = all retained events (newest first).
    Teacher timeline should pass paginate=True for stable OFFSET paging.
    """
    ensure_activity_tables(conn)
    sid = str(student_id or "").strip()
    empty = {
        "events": [],
        "total": 0,
        "page": 1,
        "page_size": page_size,
        "on_date": str(on_date or ""),
    }
    if not sid:
        return empty

    params: list[Any] = [sid, sid]
    where = "(target_student_id = ? OR (actor_role = 'student' AND actor_id = ?))"
    if on_date:
        try:
            start_iso, end_iso = _china_day_utc_bounds(on_date)
        except ValueError as exc:
            raise ValueError("日期格式应为 YYYY-MM-DD") from exc
        where += " AND created_at >= ? AND created_at < ?"
        params.extend([start_iso, end_iso])
    if before_id is not None:
        where += " AND id < ?"
        params.append(int(before_id))
    if action_prefix:
        where += " AND action LIKE ?"
        params.append(str(action_prefix) + "%")

    total = int(
        conn.execute(
            f"SELECT COUNT(*) AS c FROM activity_events WHERE {where}",
            params,
        ).fetchone()["c"]
    )

    # Paged mode: teacher UI, date filter, or explicit page>1. Cursor (before_id) keeps limit mode.
    use_page = before_id is None and (paginate or bool(on_date) or page > 1)
    if use_page:
        page = max(1, int(page or 1))
        page_size = max(1, min(int(page_size or 30), 100))
        offset = (page - 1) * page_size
        rows = conn.execute(
            f"""
            SELECT id, created_at, actor_role, actor_id, actor_name, action,
                   module_type, target_student_id, plan_item_id, unit_id,
                   summary, detail_json, ip
            FROM activity_events
            WHERE {where}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            params + [page_size, offset],
        ).fetchall()
    else:
        limit = max(1, min(int(limit or 200), 500))
        page = 1
        page_size = limit
        rows = conn.execute(
            f"""
            SELECT id, created_at, actor_role, actor_id, actor_name, action,
                   module_type, target_student_id, plan_item_id, unit_id,
                   summary, detail_json, ip
            FROM activity_events
            WHERE {where}
            ORDER BY id DESC
            LIMIT ?
            """,
            params + [limit],
        ).fetchall()

    out: list[dict[str, Any]] = []
    for r in rows:
        item = dict(r)
        try:
            item["detail"] = json.loads(item.pop("detail_json") or "{}")
        except json.JSONDecodeError:
            item["detail"] = {}
            item.pop("detail_json", None)
        else:
            item.pop("detail_json", None)
        item["created_at_cn"] = _to_china_display(item.get("created_at") or "")
        out.append(item)
    return {
        "events": out,
        "total": total,
        "page": page,
        "page_size": page_size,
        "on_date": str(on_date or ""),
    }


def _to_china_display(iso: str) -> str:
    if not iso:
        return ""
    try:
        text = iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return iso
