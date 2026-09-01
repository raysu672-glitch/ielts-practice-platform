"""Task system API helpers (MVP).

Caller enforces session identity. All dates use Asia/Shanghai calendar days.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")
DEFAULT_WEEKDAY_MINUTES = 40
DEFAULT_WEEKEND_MINUTES = 90
PACK_TOLERANCE = 1.15

READING_SETS = [
    (1, "入门基础篇"),
    (2, "学术核心篇"),
    (3, "阅读高频篇"),
    (4, "动词进阶篇"),
    (5, "形容词扩展篇"),
    (6, "名词辨析篇"),
    (7, "副词强化篇"),
    (8, "因果逻辑篇"),
    (9, "对比转折篇"),
    (10, "程度修饰篇"),
    (11, "时间序列篇"),
    (12, "数量比例篇"),
    (13, "情感态度篇"),
    (14, "科技学术篇"),
    (15, "环境生态篇"),
    (16, "社会文化篇"),
    (17, "经济商业篇"),
    (18, "教育学习篇"),
    (19, "健康医疗篇"),
    (20, "法律政治篇"),
    (21, "艺术媒体篇"),
    (22, "自然科学篇"),
    (23, "综合提升篇"),
]

# Hearing 1000-word bank: 1000 words / 20 per group → 50 units (MVP seed).
DICTATION_GROUP_COUNT = 50


def china_ymd(now: Optional[datetime] = None) -> str:
    dt = now or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d")


def is_weekend(ymd: str) -> bool:
    d = datetime.strptime(ymd, "%Y-%m-%d").date()
    return d.weekday() >= 5


def default_effective_from(now: Optional[datetime] = None) -> str:
    """Default pending/draft effective date: tomorrow (Asia/Shanghai)."""
    today = datetime.strptime(china_ymd(now), "%Y-%m-%d").date()
    return (today + timedelta(days=1)).strftime("%Y-%m-%d")


def normalize_effective_from(raw: Any, *, now: Optional[datetime] = None) -> str:
    today = china_ymd(now)
    if raw is None or raw == "":
        return default_effective_from(now)
    if not isinstance(raw, str):
        raise ValueError("生效日期格式应为 YYYY-MM-DD")
    try:
        datetime.strptime(raw, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("生效日期格式应为 YYYY-MM-DD") from exc
    if raw < today:
        raise ValueError("生效日期不能早于今天")
    return raw


def _row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return dict(row)


def ensure_task_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS task_units (
            unit_id TEXT PRIMARY KEY,
            module_type TEXT NOT NULL,
            parent_module TEXT NOT NULL,
            unit_no INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_ref TEXT NOT NULL DEFAULT '{}',
            est_minutes INTEGER NOT NULL DEFAULT 15,
            content_version TEXT NOT NULL DEFAULT '1',
            completion_rule TEXT NOT NULL DEFAULT '',
            study_url TEXT NOT NULL DEFAULT '',
            test_url TEXT NOT NULL DEFAULT '',
            is_active INTEGER NOT NULL DEFAULT 1,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS student_time_profiles (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            weekday_minutes INTEGER NOT NULL DEFAULT 40,
            weekend_minutes INTEGER NOT NULL DEFAULT 90,
            stage_test_every_n INTEGER NOT NULL DEFAULT 3,
            pending_weekday_minutes INTEGER,
            pending_weekend_minutes INTEGER,
            pending_stage_test_every_n INTEGER,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS plan_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            sort_order INTEGER NOT NULL DEFAULT 0,
            item_type TEXT NOT NULL CHECK (item_type IN ('study', 'test')),
            unit_id TEXT,
            module_type TEXT NOT NULL DEFAULT '',
            test_unit_ids TEXT NOT NULL DEFAULT '[]',
            test_title TEXT NOT NULL DEFAULT '',
            est_minutes INTEGER,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paused', 'removed')),
            study_completed INTEGER NOT NULL DEFAULT 0,
            study_completed_version TEXT,
            test_passed INTEGER NOT NULL DEFAULT 0,
            test_attempt_count_today INTEGER NOT NULL DEFAULT 0,
            test_attempt_ymd TEXT,
            need_refresh INTEGER NOT NULL DEFAULT 0,
            last_completed_at TEXT,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_plan_items_student
            ON plan_items(student_id, sort_order);

        CREATE TABLE IF NOT EXISTS plan_items_draft (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            sort_order INTEGER NOT NULL DEFAULT 0,
            item_type TEXT NOT NULL CHECK (item_type IN ('study', 'test')),
            unit_id TEXT,
            module_type TEXT NOT NULL DEFAULT '',
            test_unit_ids TEXT NOT NULL DEFAULT '[]',
            test_title TEXT NOT NULL DEFAULT '',
            est_minutes INTEGER,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paused', 'removed')),
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_plan_items_draft_student
            ON plan_items_draft(student_id, sort_order);

        CREATE TABLE IF NOT EXISTS daily_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            task_date TEXT NOT NULL,
            plan_item_id INTEGER NOT NULL REFERENCES plan_items(id),
            priority_class TEXT NOT NULL DEFAULT 'fresh'
                CHECK (priority_class IN ('content_refresh', 'carry_over', 'fresh')),
            sort_in_day INTEGER NOT NULL DEFAULT 0,
            state TEXT NOT NULL DEFAULT 'todo'
                CHECK (state IN ('todo', 'in_progress', 'done_study',
                                 'done_pass', 'done_fail')),
            locked INTEGER NOT NULL DEFAULT 1,
            forced INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            UNIQUE(student_id, task_date, plan_item_id)
        );
        CREATE INDEX IF NOT EXISTS idx_daily_tasks_student_date
            ON daily_tasks(student_id, task_date);

        CREATE TABLE IF NOT EXISTS plan_draft_meta (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            saved_ymd TEXT NOT NULL,
            effective_from TEXT,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS task_unit_progress (
            student_id TEXT NOT NULL,
            plan_item_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            scope_done INTEGER NOT NULL DEFAULT 0,
            scope_total INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            PRIMARY KEY (student_id, plan_item_id)
        );
        """
    )
    _migrate_task_effective_columns(conn)
    conn.commit()


def _migrate_task_effective_columns(conn: sqlite3.Connection) -> None:
    tables = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if "student_time_profiles" in tables:
        cols = {
            r[1]
            for r in conn.execute("PRAGMA table_info(student_time_profiles)").fetchall()
        }
        if "pending_effective_from" not in cols:
            conn.execute(
                "ALTER TABLE student_time_profiles ADD COLUMN pending_effective_from TEXT"
            )
    if "plan_draft_meta" in tables:
        cols = {
            r[1] for r in conn.execute("PRAGMA table_info(plan_draft_meta)").fetchall()
        }
        if "effective_from" not in cols:
            conn.execute(
                "ALTER TABLE plan_draft_meta ADD COLUMN effective_from TEXT"
            )


def _draft_meta_effective_from(meta: Optional[dict[str, Any]], today: str) -> Optional[str]:
    if not meta:
        return None
    if meta.get("effective_from"):
        return str(meta["effective_from"])
    saved = meta.get("saved_ymd")
    if not saved:
        return default_effective_from()
    if saved < today:
        return today
    saved_day = datetime.strptime(saved, "%Y-%m-%d").date()
    return (saved_day + timedelta(days=1)).strftime("%Y-%m-%d")


def _profile_pending_due(row: dict[str, Any], task_date: str) -> bool:
    has_pending = any(
        row.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
        )
    )
    if not has_pending:
        return False
    eff = row.get("pending_effective_from")
    if eff:
        return str(eff) <= task_date
    updated = (row.get("updated_at") or "")[:10]
    if updated and updated >= task_date:
        return False
    return True


def _pending_effective_from_summary(
    conn: sqlite3.Connection, student_id: str, *, pending_plan_change: bool
) -> Optional[str]:
    if not pending_plan_change:
        return None
    today = china_ymd()
    dates: list[str] = []
    draft_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=?", (student_id,)
    ).fetchone()["c"]
    if draft_n:
        meta = conn.execute(
            "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
            (student_id,),
        ).fetchone()
        eff = _draft_meta_effective_from(dict(meta) if meta else None, today)
        if eff:
            dates.append(eff)
    tp = ensure_time_profile(conn, student_id)
    if any(
        tp.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
        )
    ):
        eff = tp.get("pending_effective_from")
        if eff:
            dates.append(str(eff))
        else:
            dates.append(default_effective_from())
    return min(dates) if dates else default_effective_from()


def seed_mvp_units(conn: sqlite3.Connection) -> None:
    """Idempotent seed for reading_synonym (23) + dictation (50)."""
    for set_id, name in READING_SETS:
        unit_id = f"reading_synonym_u{set_id:02d}"
        scope_total = 5 if set_id == 23 else 10
        content_ref = json.dumps({"setId": set_id, "scope_total": scope_total}, ensure_ascii=False)
        study_url = f"../tongyitihuan/index.html?unit={set_id}"
        conn.execute(
            """
            INSERT INTO task_units (
                unit_id, module_type, parent_module, unit_no, title,
                content_ref, est_minutes, content_version, completion_rule,
                study_url, is_active
            ) VALUES (?, 'reading_synonym', 'reading_synonym', ?, ?, ?, 15, '1',
                      'all_subgroups_once', ?, 1)
            ON CONFLICT(unit_id) DO UPDATE SET
                title=excluded.title,
                content_ref=excluded.content_ref,
                study_url=excluded.study_url
            """,
            (unit_id, set_id, f"单元{set_id} · {name}", content_ref, study_url),
        )

    for i in range(DICTATION_GROUP_COUNT):
        unit_no = i + 1
        unit_id = f"dictation_u{unit_no:02d}"
        content_ref = json.dumps({"groupIndex": i, "scope_total": 20}, ensure_ascii=False)
        study_url = f"listening.html?group={i}"
        conn.execute(
            """
            INSERT INTO task_units (
                unit_id, module_type, parent_module, unit_no, title,
                content_ref, est_minutes, content_version, completion_rule,
                study_url, is_active
            ) VALUES (?, 'dictation', 'dictation', ?, ?, ?, 25, '1',
                      'four_stage_completed', ?, 1)
            ON CONFLICT(unit_id) DO UPDATE SET
                title=excluded.title,
                content_ref=excluded.content_ref,
                study_url=excluded.study_url
            """,
            (unit_id, unit_no, f"第{unit_no}组", content_ref, study_url),
        )
    conn.commit()


def list_units(conn: sqlite3.Connection, module_type: Optional[str] = None) -> list[dict[str, Any]]:
    if module_type:
        rows = conn.execute(
            "SELECT * FROM task_units WHERE is_active=1 AND module_type=? ORDER BY unit_no",
            (module_type,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM task_units WHERE is_active=1 ORDER BY module_type, unit_no"
        ).fetchall()
    out = []
    for row in rows:
        d = dict(row)
        try:
            d["content_ref"] = json.loads(d.get("content_ref") or "{}")
        except json.JSONDecodeError:
            d["content_ref"] = {}
        out.append(d)
    return out


def ensure_time_profile(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM student_time_profiles WHERE student_id=?", (student_id,)
    ).fetchone()
    if row:
        return dict(row)
    conn.execute(
        """
        INSERT INTO student_time_profiles (student_id, weekday_minutes, weekend_minutes)
        VALUES (?, ?, ?)
        """,
        (student_id, DEFAULT_WEEKDAY_MINUTES, DEFAULT_WEEKEND_MINUTES),
    )
    conn.commit()
    return dict(
        conn.execute(
            "SELECT * FROM student_time_profiles WHERE student_id=?", (student_id,)
        ).fetchone()
    )


def apply_pending_profile(conn: sqlite3.Connection, student_id: str, task_date: str) -> None:
    """Merge pending minutes into live fields (call on first access of a new day)."""
    row = ensure_time_profile(conn, student_id)
    updates = []
    params: list[Any] = []
    if row.get("pending_weekday_minutes") is not None:
        updates.append("weekday_minutes=?")
        params.append(row["pending_weekday_minutes"])
        updates.append("pending_weekday_minutes=NULL")
    if row.get("pending_weekend_minutes") is not None:
        updates.append("weekend_minutes=?")
        params.append(row["pending_weekend_minutes"])
        updates.append("pending_weekend_minutes=NULL")
    if row.get("pending_stage_test_every_n") is not None:
        updates.append("stage_test_every_n=?")
        params.append(row["pending_stage_test_every_n"])
        updates.append("pending_stage_test_every_n=NULL")
    if updates:
        params.append(student_id)
        conn.execute(
            f"UPDATE student_time_profiles SET {', '.join(updates)}, "
            f"updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE student_id=?",
            params,
        )


def get_time_profile(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    return ensure_time_profile(conn, student_id)


def put_time_profile(
    conn: sqlite3.Connection, student_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Write pending values; effective_from defaults to tomorrow."""
    ensure_time_profile(conn, student_id)
    weekday = payload.get("weekday_minutes")
    weekend = payload.get("weekend_minutes")
    every_n = payload.get("stage_test_every_n")
    effective_from = normalize_effective_from(payload.get("effective_from"))
    conn.execute(
        """
        UPDATE student_time_profiles SET
            pending_weekday_minutes = COALESCE(?, pending_weekday_minutes),
            pending_weekend_minutes = COALESCE(?, pending_weekend_minutes),
            pending_stage_test_every_n = COALESCE(?, pending_stage_test_every_n),
            pending_effective_from = ?,
            updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id = ?
        """,
        (weekday, weekend, every_n, effective_from, student_id),
    )
    today = china_ymd()
    if payload.get("effective") == "today" or effective_from <= today:
        apply_pending_profile(conn, student_id, today)
        conn.execute(
            "UPDATE student_time_profiles SET pending_effective_from=NULL WHERE student_id=?",
            (student_id,),
        )
        # Always rebuild today's pack when duration takes effect immediately.
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, today),
        )
    conn.commit()
    return get_time_profile(conn, student_id)


def _parse_json_list(raw: Any) -> list[Any]:
    if isinstance(raw, list):
        return raw
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _plan_progress(conn: sqlite3.Connection, student_id: str) -> dict[str, dict[str, int]]:
    """module_type -> {study_x, study_y, pass_a, pass_b}."""
    rows = conn.execute(
        """
        SELECT module_type, item_type, status, study_completed, test_passed
        FROM plan_items WHERE student_id=? AND status!='removed'
        """,
        (student_id,),
    ).fetchall()
    prog: dict[str, dict[str, int]] = {}
    for row in rows:
        mt = row["module_type"] or ""
        if mt not in prog:
            prog[mt] = {"study_x": 0, "study_y": 0, "pass_a": 0, "pass_b": 0}
        if row["item_type"] == "study":
            prog[mt]["study_y"] += 1
            if row["study_completed"]:
                prog[mt]["study_x"] += 1
        elif row["item_type"] == "test":
            prog[mt]["pass_b"] += 1
            if row["test_passed"]:
                prog[mt]["pass_a"] += 1
    return prog


def effective_plan_status(conn: sqlite3.Connection, student_id: str) -> str:
    """none | all_paused | active (D28)."""
    rows = conn.execute(
        "SELECT status FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchall()
    if not rows:
        return "none"
    if all(r["status"] == "paused" for r in rows):
        return "all_paused"
    if any(r["status"] == "pending" for r in rows):
        return "active"
    return "all_paused"


def get_plan(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    maybe_apply_pending_for_today(conn, student_id, china_ymd())
    live = [
        dict(r)
        for r in conn.execute(
            """
            SELECT p.*, u.title AS unit_title, u.content_ref, u.content_version,
                   u.study_url, u.est_minutes AS unit_est_minutes
            FROM plan_items p
            LEFT JOIN task_units u ON u.unit_id = p.unit_id
            WHERE p.student_id=? AND p.status!='removed'
            ORDER BY p.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    draft = [
        dict(r)
        for r in conn.execute(
            """
            SELECT d.*, u.title AS unit_title
            FROM plan_items_draft d
            LEFT JOIN task_units u ON u.unit_id = d.unit_id
            WHERE d.student_id=? AND d.status!='removed'
            ORDER BY d.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    for item in live + draft:
        item["test_unit_ids"] = _parse_json_list(item.get("test_unit_ids"))
        if item.get("content_ref"):
            try:
                item["content_ref"] = json.loads(item["content_ref"])
            except (json.JSONDecodeError, TypeError):
                pass
    tp = get_time_profile(conn, student_id)
    pending_change = bool(draft) or _profile_has_real_pending(tp)
    draft_order_issues = _stage_test_order_issues(draft) if draft else []
    today = china_ymd()
    meta_row = conn.execute(
        "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
        (student_id,),
    ).fetchone()
    meta = dict(meta_row) if meta_row else None
    draft_effective_from = (
        _draft_meta_effective_from(meta, today) if draft else None
    )
    pending_profile_effective_from = (
        tp.get("pending_effective_from")
        if _profile_has_real_pending(tp)
        else None
    )
    return {
        "live": live,
        "draft": draft,
        "draft_pending": bool(draft),
        "progress": _plan_progress(conn, student_id),
        "plan_status": effective_plan_status(conn, student_id),
        "pending_plan_change": pending_change,
        "draft_effective_from": draft_effective_from,
        "pending_profile_effective_from": pending_profile_effective_from,
        "pending_effective_from": _pending_effective_from_summary(
            conn, student_id, pending_plan_change=pending_change
        ),
        "draft_order_issues": draft_order_issues,
        "time_profile": tp,
    }


def _profile_has_real_pending(tp: dict[str, Any]) -> bool:
    if tp.get("pending_weekday_minutes") is not None:
        if int(tp["pending_weekday_minutes"]) != int(tp.get("weekday_minutes") or 0):
            return True
    if tp.get("pending_weekend_minutes") is not None:
        if int(tp["pending_weekend_minutes"]) != int(tp.get("weekend_minutes") or 0):
            return True
    if tp.get("pending_stage_test_every_n") is not None:
        if int(tp["pending_stage_test_every_n"]) != int(tp.get("stage_test_every_n") or 0):
            return True
    return False


def _study_unit_ids_in_plan(conn: sqlite3.Connection, student_id: str, table: str) -> set[str]:
    rows = conn.execute(
        f"""
        SELECT unit_id FROM {table}
        WHERE student_id=? AND item_type='study' AND status!='removed' AND unit_id IS NOT NULL
        """,
        (student_id,),
    ).fetchall()
    return {r["unit_id"] for r in rows if r["unit_id"]}


def put_plan_draft(
    conn: sqlite3.Connection,
    student_id: str,
    items: list[dict[str, Any]],
    *,
    effective_from: Optional[str] = None,
) -> dict[str, Any]:
    """Replace draft list. Enforces D26 unique unit_id for study items."""
    seen: set[str] = set()
    for it in items:
        if it.get("item_type") == "study" and it.get("status", "pending") != "removed":
            uid = it.get("unit_id")
            if not uid:
                raise ValueError("study 条目必须有 unit_id")
            if uid in seen:
                raise ValueError(f"该单元已在计划中: {uid}")
            seen.add(uid)
            unit = conn.execute(
                "SELECT unit_id, module_type FROM task_units WHERE unit_id=?", (uid,)
            ).fetchone()
            if not unit:
                raise ValueError(f"未知单元: {uid}")

    items = normalize_stage_test_positions(items)
    conn.execute("DELETE FROM plan_items_draft WHERE student_id=?", (student_id,))
    for idx, it in enumerate(items):
        item_type = it.get("item_type") or "study"
        unit_id = it.get("unit_id")
        module_type = it.get("module_type") or ""
        if item_type == "study" and unit_id:
            u = conn.execute(
                "SELECT module_type, est_minutes FROM task_units WHERE unit_id=?", (unit_id,)
            ).fetchone()
            if u:
                module_type = u["module_type"]
        status = it.get("status") or "pending"
        conn.execute(
            """
            INSERT INTO plan_items_draft (
                student_id, sort_order, item_type, unit_id, module_type,
                test_unit_ids, test_title, est_minutes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                idx,
                item_type,
                unit_id,
                module_type,
                json.dumps(it.get("test_unit_ids") or [], ensure_ascii=False),
                it.get("test_title") or "",
                it.get("est_minutes"),
                status,
            ),
        )
    eff_ymd = normalize_effective_from(effective_from)
    conn.execute(
        """
        INSERT INTO plan_draft_meta (student_id, saved_ymd, effective_from)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            saved_ymd=excluded.saved_ymd,
            effective_from=excluded.effective_from,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        """,
        (student_id, china_ymd(), eff_ymd),
    )
    # First plan (live empty): apply immediately so student is not stuck a day with no tasks.
    live_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchone()["c"]
    today = china_ymd()
    if live_n == 0 or eff_ymd <= today:
        apply_draft_to_live(conn, student_id)
        conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
        if eff_ymd == today and live_n > 0:
            conn.execute(
                "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
                (student_id, today),
            )
    conn.commit()
    # Belt-and-suspenders: due drafts/profile must merge even if caller skipped the branch.
    maybe_apply_pending_for_today(conn, student_id, today)
    return get_plan(conn, student_id)


def apply_draft_to_live(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    """Promote draft → live. Preserves completion state for matching unit_id study items."""
    draft = conn.execute(
        "SELECT * FROM plan_items_draft WHERE student_id=? ORDER BY sort_order",
        (student_id,),
    ).fetchall()
    if not draft:
        return get_plan(conn, student_id)

    old = {
        r["unit_id"]: dict(r)
        for r in conn.execute(
            """
            SELECT * FROM plan_items
            WHERE student_id=? AND item_type='study' AND unit_id IS NOT NULL
            """,
            (student_id,),
        ).fetchall()
        if r["unit_id"]
    }

    # Soft-remove live rows not in draft (keep history for backlog refs: mark removed)
    conn.execute(
        "UPDATE plan_items SET status='removed', updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') "
        "WHERE student_id=? AND status!='removed'",
        (student_id,),
    )

    for idx, d in enumerate(draft):
        d = dict(d)
        unit_id = d.get("unit_id")
        prev = old.get(unit_id) if d["item_type"] == "study" and unit_id else None
        conn.execute(
            """
            INSERT INTO plan_items (
                student_id, sort_order, item_type, unit_id, module_type,
                test_unit_ids, test_title, est_minutes, status,
                study_completed, study_completed_version, test_passed,
                need_refresh
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                student_id,
                idx,
                d["item_type"],
                unit_id,
                d["module_type"],
                d.get("test_unit_ids") or "[]",
                d.get("test_title") or "",
                d.get("est_minutes"),
                d.get("status") or "pending",
                (prev or {}).get("study_completed") or 0,
                (prev or {}).get("study_completed_version"),
                0 if d["item_type"] == "test" else 0,
            ),
        )

    conn.execute("DELETE FROM plan_items_draft WHERE student_id=?", (student_id,))
    conn.commit()
    return get_plan(conn, student_id)


def maybe_apply_pending_for_today(conn: sqlite3.Connection, student_id: str, task_date: str) -> None:
    """On first access of task_date: merge profile/draft pending if effective_from is due."""
    row = ensure_time_profile(conn, student_id)
    # Drop stale pending_* that equal live (avoids false「待生效」banner).
    if not _profile_has_real_pending(row) and any(
        row.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
            "pending_effective_from",
        )
    ):
        conn.execute(
            """
            UPDATE student_time_profiles SET
                pending_weekday_minutes=NULL,
                pending_weekend_minutes=NULL,
                pending_stage_test_every_n=NULL,
                pending_effective_from=NULL,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE student_id=?
            """,
            (student_id,),
        )
        row = ensure_time_profile(conn, student_id)
    if _profile_pending_due(row, task_date):
        old_wd = int(row["weekday_minutes"])
        old_we = int(row["weekend_minutes"])
        apply_pending_profile(conn, student_id, task_date)
        conn.execute(
            "UPDATE student_time_profiles SET pending_effective_from=NULL WHERE student_id=?",
            (student_id,),
        )
        merged = ensure_time_profile(conn, student_id)
        # Budget change must unlock today's pack so student/teacher previews match.
        if int(merged["weekday_minutes"]) != old_wd or int(merged["weekend_minutes"]) != old_we:
            conn.execute(
                "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
                (student_id, task_date),
            )
    draft_count = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=?", (student_id,)
    ).fetchone()["c"]
    if not draft_count:
        # Orphan meta without draft rows
        conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
        conn.commit()
        return
    meta = conn.execute(
        "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
        (student_id,),
    ).fetchone()
    eff = _draft_meta_effective_from(dict(meta) if meta else None, task_date)
    if not eff or eff > task_date:
        conn.commit()
        return
    apply_draft_to_live(conn, student_id)
    conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
    if eff == task_date:
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, task_date),
        )
    conn.commit()


def _budget_minutes(
    profile: dict[str, Any],
    task_date: str,
    *,
    weekday_override: Optional[int] = None,
    weekend_override: Optional[int] = None,
    prefer_pending: bool = False,
) -> int:
    """Resolve daily pack budget; overrides (teacher form) win over pending/live."""
    weekend = is_weekend(task_date)
    if weekend:
        if weekend_override is not None:
            return max(0, int(weekend_override))
        if prefer_pending and profile.get("pending_weekend_minutes") is not None:
            return int(profile["pending_weekend_minutes"])
        return int(profile["weekend_minutes"])
    if weekday_override is not None:
        return max(0, int(weekday_override))
    if prefer_pending and profile.get("pending_weekday_minutes") is not None:
        return int(profile["pending_weekday_minutes"])
    return int(profile["weekday_minutes"])


def _est_minutes(conn: sqlite3.Connection, plan_item: dict[str, Any]) -> int:
    if plan_item.get("est_minutes"):
        return int(plan_item["est_minutes"])
    if plan_item.get("unit_id"):
        u = conn.execute(
            "SELECT est_minutes FROM task_units WHERE unit_id=?", (plan_item["unit_id"],)
        ).fetchone()
        if u:
            return int(u["est_minutes"])
    return 15 if plan_item.get("item_type") == "study" else 20


def _item_done(item: dict[str, Any]) -> bool:
    if item.get("item_type") == "study":
        return bool(item.get("study_completed"))
    return bool(item.get("test_passed"))


def backlog_plan_item_ids(conn: sqlite3.Connection, student_id: str) -> list[int]:
    """D23: items that appeared in some daily_tasks and are still unfinished."""
    rows = conn.execute(
        """
        SELECT DISTINCT d.plan_item_id
        FROM daily_tasks d
        JOIN plan_items p ON p.id = d.plan_item_id
        WHERE d.student_id=?
          AND p.status != 'removed'
          AND (
            (p.item_type='study' AND p.study_completed=0)
            OR (p.item_type='test' AND p.test_passed=0)
          )
        ORDER BY d.task_date, d.sort_in_day
        """,
        (student_id,),
    ).fetchall()
    return [r["plan_item_id"] for r in rows]


def _session_study_date_expr() -> str:
    return "date(COALESCE(ended_at, created_at), '+8 hours')"


def sum_today_study_seconds(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
) -> int:
    try:
        row = conn.execute(
            f"""
            SELECT COALESCE(SUM(duration_seconds), 0) AS total
            FROM study_sessions
            WHERE student_id=?
              AND session_kind='study'
              AND {_session_study_date_expr()} = ?
            """,
            (student_id, task_date),
        ).fetchone()
        return int(row["total"] or 0) if row else 0
    except sqlite3.OperationalError:
        return 0


def sum_today_study_by_plan_item(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
) -> dict[int, int]:
    try:
        rows = conn.execute(
            f"""
            SELECT plan_item_id, COALESCE(SUM(duration_seconds), 0) AS total
            FROM study_sessions
            WHERE student_id=?
              AND session_kind='study'
              AND plan_item_id IS NOT NULL
              AND {_session_study_date_expr()} = ?
            GROUP BY plan_item_id
            """,
            (student_id, task_date),
        ).fetchall()
        return {int(r["plan_item_id"]): int(r["total"]) for r in rows}
    except sqlite3.OperationalError:
        return {}


def _minutes_from_seconds(seconds: int) -> float:
    return round(max(0, int(seconds)) / 60, 1)


def _interleave_by_module(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Round-robin across module_type; preserve sort_order within each module.

    When only one module is present, return global sort_order (unchanged behavior).
    Module cycle order = order each subject first appears in the plan (sort_order).
    """
    if not items:
        return []
    by_mod: dict[str, list[dict[str, Any]]] = {}
    mod_first: dict[str, int] = {}
    for item in items:
        mt = str(item.get("module_type") or "other")
        if mt not in by_mod:
            by_mod[mt] = []
            mod_first[mt] = int(item.get("sort_order") or 0)
        by_mod[mt].append(item)
    if len(by_mod) <= 1:
        return sorted(items, key=lambda x: int(x.get("sort_order") or 0))
    module_keys = sorted(by_mod.keys(), key=lambda m: mod_first[m])
    queues = {m: list(by_mod[m]) for m in module_keys}
    out: list[dict[str, Any]] = []
    while True:
        progressed = False
        for m in module_keys:
            if not queues[m]:
                continue
            out.append(queues[m].pop(0))
            progressed = True
        if not progressed:
            break
    return out


def normalize_stage_test_positions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Place each stage test after the last study unit it covers; drop exact duplicates."""
    out = [dict(x) for x in items if x.get("item_type") != "test"]
    tests = [dict(x) for x in items if x.get("item_type") == "test"]
    seen_cov: set[frozenset[str]] = set()
    unique_tests: list[dict[str, Any]] = []
    for test in tests:
        covers = frozenset(_parse_json_list(test.get("test_unit_ids")) or [])
        if not covers or covers in seen_cov:
            continue
        seen_cov.add(covers)
        unique_tests.append(test)

    keyed: list[tuple[int, int, int, dict[str, Any]]] = []
    for test in unique_tests:
        covers = set(_parse_json_list(test.get("test_unit_ids")) or [])
        indices = [
            i
            for i, st in enumerate(out)
            if st.get("item_type") == "study" and st.get("unit_id") in covers
        ]
        if not indices:
            keyed.append((len(out), 0, 0, test))
            continue
        keyed.append((max(indices), min(indices), len(covers), test))

    keyed.sort(key=lambda row: (row[0], row[1], row[2]))
    for last_si, _first_si, _n, test in reversed(keyed):
        out.insert(last_si + 1, test)
    return out


def _stage_test_order_issues(items: list[dict[str, Any]]) -> list[str]:
    """Human-readable warnings when a test appears before units it covers."""
    issues: list[str] = []
    study_seen: set[str] = set()
    for idx, it in enumerate(items):
        if it.get("item_type") == "study" and it.get("unit_id"):
            study_seen.add(it["unit_id"])
        elif it.get("item_type") == "test":
            covers = set(_parse_json_list(it.get("test_unit_ids")) or [])
            missing = [u for u in covers if u not in study_seen]
            if missing:
                title = it.get("test_title") or "阶段测"
                issues.append(f"第{idx + 1}条「{title}」排在部分学习单元之前")
    return issues


def _plan_items_from_draft_rows(rows: list) -> list[dict[str, Any]]:
    plan_items: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        d = dict(row)
        d["id"] = -(i + 1)
        d["study_completed"] = 0
        d["test_passed"] = 0
        d["need_refresh"] = 0
        d["test_unit_ids"] = _parse_json_list(d.get("test_unit_ids"))
        plan_items.append(d)
    return plan_items


def _plan_items_from_payload(
    conn: sqlite3.Connection, items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    plan_items: list[dict[str, Any]] = []
    for i, it in enumerate(items):
        if it.get("status") == "removed":
            continue
        d = dict(it)
        d["id"] = -(i + 1)
        d["study_completed"] = 0
        d["test_passed"] = 0
        d["need_refresh"] = 0
        d["test_unit_ids"] = _parse_json_list(d.get("test_unit_ids"))
        if d.get("item_type") == "study" and d.get("unit_id"):
            u = conn.execute(
                "SELECT title, est_minutes, module_type FROM task_units WHERE unit_id=?",
                (d["unit_id"],),
            ).fetchone()
            if u:
                d["unit_title"] = u["title"]
                d["unit_est_minutes"] = u["est_minutes"]
                if not d.get("module_type"):
                    d["module_type"] = u["module_type"]
        plan_items.append(d)
    return plan_items


def _simulate_daily_pack(
    conn: sqlite3.Connection,
    plan_items: list[dict[str, Any]],
    backlog_items: list[dict[str, Any]],
    budget: int,
    tolerance: float,
) -> dict[str, Any]:
    result: list[dict[str, Any]] = []
    used = 0.0
    in_result: set[int] = set()

    def _try_add(item: dict[str, Any], prio: str) -> bool:
        nonlocal used
        pid = int(item["id"])
        if pid in in_result:
            return False
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            return False
        if used == 0 and est > budget:
            result.append({"item": item, "priority_class": prio})
            in_result.add(pid)
            return True
        result.append({"item": item, "priority_class": prio})
        in_result.add(pid)
        used += est
        return True

    for item in _interleave_by_module(backlog_items):
        if used >= tolerance:
            break
        _try_add(item, "carry_over")

    fresh = [it for it in plan_items if not _item_done(it) and int(it["id"]) not in in_result]
    for item in _interleave_by_module(fresh):
        if used >= tolerance:
            break
        pid = int(item["id"])
        if pid in in_result:
            continue
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            break
        if used == 0 and est > budget:
            result.append({"item": item, "priority_class": "fresh"})
            in_result.add(pid)
            break
        result.append({"item": item, "priority_class": "fresh"})
        in_result.add(pid)
        used += est
        if used >= tolerance:
            break

    modules = {r["item"].get("module_type") for r in result if r["item"].get("module_type")}
    out_items = []
    for r in result:
        it = r["item"]
        title = it.get("unit_title") or it.get("test_title") or it.get("unit_id") or "任务"
        if it.get("item_type") == "test":
            title = it.get("test_title") or title
        out_items.append(
            {
                "title": title,
                "module_type": it.get("module_type"),
                "item_type": it.get("item_type"),
                "est_minutes": _est_minutes(conn, it),
                "priority_class": r["priority_class"],
            }
        )
    return {
        "est_total_minutes": sum(x["est_minutes"] for x in out_items),
        "rotated": len(modules) > 1,
        "items": out_items,
    }


def preview_daily_pack_items(
    conn: sqlite3.Connection,
    student_id: str,
    items: list[dict[str, Any]],
    task_date: Optional[str] = None,
    *,
    weekday_minutes: Optional[int] = None,
    weekend_minutes: Optional[int] = None,
) -> dict[str, Any]:
    """Preview packing for a draft item list (saved or unsaved).

    Teacher form may pass weekday/weekend overrides so the edit preview tracks
    the duration inputs even before「保存时长」.
    """
    task_date = task_date or china_ymd()
    profile = ensure_time_profile(conn, student_id)
    budget = _budget_minutes(
        profile,
        task_date,
        weekday_override=weekday_minutes,
        weekend_override=weekend_minutes,
        prefer_pending=weekday_minutes is None and weekend_minutes is None,
    )
    tolerance = budget * PACK_TOLERANCE
    plan_items = _plan_items_from_payload(conn, items)
    sim = _simulate_daily_pack(conn, plan_items, [], budget, tolerance)
    return {
        "source": "draft_items",
        "task_date": task_date,
        "budget_minutes": budget,
        **sim,
    }


def preview_daily_pack(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
    *,
    source: str = "live",
) -> dict[str, Any]:
    """Simulate daily boxing (multi-module rotation). Live + existing daily → actual today."""
    task_date = task_date or china_ymd()
    # Keep teacher live preview in sync with student (merge due pending first).
    maybe_apply_pending_for_today(conn, student_id, task_date)
    profile = ensure_time_profile(conn, student_id)
    budget = _budget_minutes(profile, task_date)
    tolerance = budget * PACK_TOLERANCE

    if source == "live":
        existing = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, task_date),
        ).fetchone()
        if existing and int(existing["c"]) > 0:
            daily = _enrich_daily(conn, student_id, task_date)
            modules = {d.get("module_type") for d in daily if d.get("module_type")}
            return {
                "source": "live_locked",
                "task_date": task_date,
                "budget_minutes": budget,
                "est_total_minutes": sum(d.get("est_minutes") or 0 for d in daily),
                "rotated": len(modules) > 1,
                "items": [
                    {
                        "title": d.get("title"),
                        "module_type": d.get("module_type"),
                        "item_type": d.get("item_type"),
                        "est_minutes": d.get("est_minutes"),
                        "priority_class": d.get("priority_class"),
                    }
                    for d in daily
                ],
            }

    if source == "draft":
        rows = conn.execute(
            """
            SELECT d.*, u.title AS unit_title, u.est_minutes AS unit_est_minutes
            FROM plan_items_draft d
            LEFT JOIN task_units u ON u.unit_id = d.unit_id
            WHERE d.student_id=? AND d.status='pending'
            ORDER BY d.sort_order
            """,
            (student_id,),
        ).fetchall()
        plan_items = _plan_items_from_draft_rows(rows)
        backlog_items = []
        budget = _budget_minutes(profile, task_date, prefer_pending=True)
        tolerance = budget * PACK_TOLERANCE
    else:
        plan_items = [
            dict(r)
            for r in conn.execute(
                """
                SELECT * FROM plan_items
                WHERE student_id=? AND status='pending'
                ORDER BY sort_order
                """,
                (student_id,),
            ).fetchall()
        ]
        backlog_items = []
        for pid in backlog_plan_item_ids(conn, student_id):
            item_row = conn.execute("SELECT * FROM plan_items WHERE id=?", (pid,)).fetchone()
            if item_row and item_row["status"] == "pending":
                item = dict(item_row)
                if not _item_done(item):
                    backlog_items.append(item)

    sim = _simulate_daily_pack(conn, plan_items, backlog_items, budget, tolerance)
    return {
        "source": source if source != "live" else "live",
        "task_date": task_date,
        "budget_minutes": budget,
        **sim,
    }


def build_daily_tasks(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    task_date = task_date or china_ymd()
    maybe_apply_pending_for_today(conn, student_id, task_date)
    profile = ensure_time_profile(conn, student_id)
    budget = (
        int(profile["weekend_minutes"])
        if is_weekend(task_date)
        else int(profile["weekday_minutes"])
    )
    tolerance = budget * PACK_TOLERANCE

    existing = conn.execute(
        """
        SELECT * FROM daily_tasks WHERE student_id=? AND task_date=?
        ORDER BY sort_in_day
        """,
        (student_id, task_date),
    ).fetchall()
    if existing:
        # Already materialized for today — return as-is (MVP locked)
        return _enrich_daily(conn, student_id, task_date)

    result: list[tuple[int, str, bool]] = []  # plan_item_id, priority, forced
    used = 0.0
    in_result: set[int] = set()

    # 1) content refresh
    refresh_rows = conn.execute(
        """
        SELECT * FROM plan_items
        WHERE student_id=? AND status='pending' AND item_type='study'
          AND need_refresh=1 AND study_completed=0
        ORDER BY sort_order
        """,
        (student_id,),
    ).fetchall()
    for row in refresh_rows:
        item = dict(row)
        pid = item["id"]
        if pid in in_result:
            continue
        result.append((pid, "content_refresh", True))
        in_result.add(pid)
        used += _est_minutes(conn, item)

    # 2) backlog carry-over (interleave when multiple subjects)
    backlog_items: list[dict[str, Any]] = []
    for pid in backlog_plan_item_ids(conn, student_id):
        if pid in in_result:
            continue
        item_row = conn.execute("SELECT * FROM plan_items WHERE id=?", (pid,)).fetchone()
        if not item_row or item_row["status"] != "pending":
            continue
        item = dict(item_row)
        if _item_done(item):
            continue
        backlog_items.append(item)
    for item in _interleave_by_module(backlog_items):
        pid = item["id"]
        if pid in in_result:
            continue
        result.append((pid, "carry_over", False))
        in_result.add(pid)
        used += _est_minutes(conn, item)

    # 3) pack fresh items — multi-subject plans rotate by module (not strict global queue)
    live = conn.execute(
        """
        SELECT * FROM plan_items
        WHERE student_id=? AND status='pending'
        ORDER BY sort_order
        """,
        (student_id,),
    ).fetchall()
    fresh_candidates: list[dict[str, Any]] = []
    for row in live:
        item = dict(row)
        if _item_done(item):
            continue
        if item["id"] in in_result:
            continue
        fresh_candidates.append(item)
    for item in _interleave_by_module(fresh_candidates):
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            break
        if used == 0 and est > budget:
            result.append((item["id"], "fresh", False))
            in_result.add(item["id"])
            break
        result.append((item["id"], "fresh", False))
        in_result.add(item["id"])
        used += est
        if used >= tolerance:
            break

    for sort_i, (pid, prio, forced) in enumerate(result):
        conn.execute(
            """
            INSERT INTO daily_tasks (
                student_id, task_date, plan_item_id, priority_class,
                sort_in_day, state, locked, forced
            ) VALUES (?, ?, ?, ?, ?, 'todo', 1, ?)
            """,
            (student_id, task_date, pid, prio, sort_i, 1 if forced else 0),
        )

    conn.commit()
    return _enrich_daily(conn, student_id, task_date)


def _scope_for_unit(content_ref: Any) -> tuple[int, str]:
    ref = content_ref
    if isinstance(ref, str):
        try:
            ref = json.loads(ref)
        except json.JSONDecodeError:
            ref = {}
    if not isinstance(ref, dict):
        ref = {}
    total = int(ref.get("scope_total") or 0)
    if not total and "setId" in ref:
        total = 5 if int(ref["setId"]) == 23 else 10
    if not total and "groupIndex" in ref:
        total = 20
    unit = "组"
    if "groupIndex" in ref:
        unit = "词"
    return total, unit


def _enrich_daily(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT d.*, p.item_type, p.unit_id, p.module_type, p.test_title,
               p.test_unit_ids, p.study_completed, p.test_passed, p.need_refresh,
               p.est_minutes AS plan_est,
               u.title AS unit_title, u.content_ref, u.content_version, u.study_url,
               u.est_minutes AS unit_est
        FROM daily_tasks d
        JOIN plan_items p ON p.id = d.plan_item_id
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE d.student_id=? AND d.task_date=?
        ORDER BY d.sort_in_day
        """,
        (student_id, task_date),
    ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        scope_total, scope_unit = _scope_for_unit(item.get("content_ref"))
        prog = conn.execute(
            """
            SELECT scope_done, scope_total FROM task_unit_progress
            WHERE student_id=? AND plan_item_id=?
            """,
            (student_id, item["plan_item_id"]),
        ).fetchone()
        scope_done = int(prog["scope_done"]) if prog else 0
        if prog and prog["scope_total"]:
            scope_total = int(prog["scope_total"])
        study_url = item.get("study_url") or ""
        if study_url and item.get("id"):
            sep = "&" if "?" in study_url else "?"
            study_url = (
                f"{study_url}{sep}task_id={item['id']}"
                f"&plan_item_id={item['plan_item_id']}"
            )
        title = item.get("unit_title") or item.get("test_title") or "任务"
        if item.get("need_refresh"):
            title = f"{title}（内容已更新）"
        out.append(
            {
                "daily_task_id": item["id"],
                "plan_item_id": item["plan_item_id"],
                "task_date": task_date,
                "item_type": item["item_type"],
                "unit_id": item.get("unit_id"),
                "module_type": item.get("module_type"),
                "title": title,
                "state": item["state"],
                "priority_class": item["priority_class"],
                "forced": bool(item["forced"]),
                "content_version": item.get("content_version") or "1",
                "content_ref": (
                    json.loads(item["content_ref"])
                    if isinstance(item.get("content_ref"), str) and item.get("content_ref")
                    else item.get("content_ref")
                ),
                "scope_label": "本单元",
                "scope_done": scope_done,
                "scope_total": scope_total,
                "scope_unit": scope_unit,
                "study_url": study_url,
                "est_minutes": item.get("plan_est") or item.get("unit_est") or 15,
            }
        )
    return out


def get_today(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    task_date = china_ymd()
    items = build_daily_tasks(conn, student_id, task_date)
    profile = ensure_time_profile(conn, student_id)
    budget = (
        int(profile["weekend_minutes"])
        if is_weekend(task_date)
        else int(profile["weekday_minutes"])
    )
    plan = get_plan(conn, student_id)
    status = plan["plan_status"]
    actual_seconds = sum_today_study_seconds(conn, student_id, task_date)
    by_item_seconds = sum_today_study_by_plan_item(conn, student_id, task_date)
    for item in items:
        pid = item.get("plan_item_id")
        if pid is not None:
            item["actual_minutes"] = _minutes_from_seconds(by_item_seconds.get(int(pid), 0))
        else:
            item["actual_minutes"] = 0.0
    empty_msg = None
    if not items:
        if status == "none":
            empty_msg = "今日暂无任务，请联系助教"
        elif status == "all_paused":
            empty_msg = "计划已暂停，请联系助教"
        else:
            empty_msg = "今日暂无任务，请联系助教"
    return {
        "task_date": task_date,
        "budget_minutes": budget,
        "est_total_minutes": sum(i.get("est_minutes") or 0 for i in items),
        "actual_total_minutes": _minutes_from_seconds(actual_seconds),
        "items": items,
        "progress": plan["progress"],
        "plan_status": status,
        "pending_plan_change": plan["pending_plan_change"],
        "pending_effective_from": plan.get("pending_effective_from"),
        "empty_message": empty_msg,
    }


def update_scope_progress(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    *,
    scope_done: Optional[int] = None,
    delta: Optional[int] = None,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    unit = None
    if item["unit_id"]:
        unit = conn.execute(
            "SELECT * FROM task_units WHERE unit_id=?", (item["unit_id"],)
        ).fetchone()
    scope_total, _ = _scope_for_unit(unit["content_ref"] if unit else {})
    existing = conn.execute(
        "SELECT * FROM task_unit_progress WHERE student_id=? AND plan_item_id=?",
        (student_id, plan_item_id),
    ).fetchone()
    current = int(existing["scope_done"]) if existing else 0
    if scope_done is not None:
        current = max(0, int(scope_done))
    elif delta is not None:
        current = max(0, current + int(delta))
    if scope_total:
        current = min(current, scope_total)
    conn.execute(
        """
        INSERT INTO task_unit_progress (student_id, plan_item_id, unit_id, scope_done, scope_total)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id, plan_item_id) DO UPDATE SET
            scope_done=excluded.scope_done,
            scope_total=excluded.scope_total,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        """,
        (student_id, plan_item_id, item["unit_id"] or "", current, scope_total),
    )
    conn.commit()
    return {"scope_done": current, "scope_total": scope_total}


def complete_study(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    content_version: str,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    if item["item_type"] != "study":
        raise ValueError("非学习条目")
    unit = conn.execute(
        "SELECT * FROM task_units WHERE unit_id=?", (item["unit_id"],)
    ).fetchone()
    if unit and str(unit["content_version"]) != str(content_version):
        raise ValueError("内容版本已更新，请刷新后重学")

    scope_total = 0
    if unit:
        scope_total, _ = _scope_for_unit(unit["content_ref"])
    if scope_total and unit and unit["module_type"] == "reading_synonym":
        prog = conn.execute(
            "SELECT scope_done FROM task_unit_progress WHERE student_id=? AND plan_item_id=?",
            (student_id, plan_item_id),
        ).fetchone()
        done = int(prog["scope_done"]) if prog else 0
        if done < scope_total:
            raise ValueError(f"请先完成本单元全部 {scope_total} 组练习（当前 {done}/{scope_total}）")

    conn.execute(
        """
        UPDATE plan_items SET
            study_completed=1,
            study_completed_version=?,
            need_refresh=0,
            last_completed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE id=?
        """,
        (content_version, plan_item_id),
    )
    today = china_ymd()
    conn.execute(
        """
        UPDATE daily_tasks SET state='done_study'
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (student_id, today, plan_item_id),
    )
    if unit:
        scope_total, _ = _scope_for_unit(unit["content_ref"])
        update_scope_progress(
            conn, student_id, plan_item_id, scope_done=scope_total or 1
        )
    conn.commit()
    return get_today(conn, student_id)


def submit_stage_test(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    score: float,
    *,
    threshold: float,
    details: Any = None,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    if item["item_type"] != "test":
        raise ValueError("非测试条目")

    today = china_ymd()
    attempts = int(item["test_attempt_count_today"] or 0)
    if item["test_attempt_ymd"] != today:
        attempts = 0
    if attempts >= 2 and not item["test_passed"]:
        raise ValueError("今日重测次数已用尽，请联系助教")

    passed = score >= threshold
    attempts += 1
    conn.execute(
        """
        UPDATE plan_items SET
            test_passed=?,
            test_attempt_count_today=?,
            test_attempt_ymd=?,
            last_completed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE id=?
        """,
        (1 if passed else 0, attempts, today, plan_item_id),
    )
    state = "done_pass" if passed else "done_fail"
    conn.execute(
        """
        UPDATE daily_tasks SET state=?
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (state, student_id, today, plan_item_id),
    )
    # D21: write test_records with stage_test kind
    conn.execute(
        """
        INSERT INTO test_records (
            student_id, module_type, module_name, test_type,
            score, correct_count, total_count, is_passed, pass_threshold,
            details
        ) VALUES (?, ?, ?, 'stage_test', ?, 0, 0, ?, ?, ?)
        """,
        (
            student_id,
            item["module_type"] or "reading_synonym",
            item["test_title"] or "阶段测",
            float(score),
            1 if passed else 0,
            float(threshold),
            json.dumps(details if details is not None else {}, ensure_ascii=False),
        ),
    )
    conn.commit()
    return {
        "passed": passed,
        "score": score,
        "threshold": threshold,
        "attempts_today": attempts,
        "today": get_today(conn, student_id),
    }


def insert_stage_test(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    unit_ids: list[str],
    after_sort_order: Optional[int] = None,
    test_title: str = "",
) -> dict[str, Any]:
    """Insert a stage test into draft, immediately after the last covered study unit."""
    if not unit_ids:
        raise ValueError("unit_ids 不能为空")
    units = []
    for uid in unit_ids:
        u = conn.execute("SELECT * FROM task_units WHERE unit_id=?", (uid,)).fetchone()
        if not u:
            raise ValueError(f"未知单元: {uid}")
        units.append(dict(u))
    module_types = {u["module_type"] for u in units}
    if len(module_types) > 1:
        raise ValueError("阶段测只能覆盖同一科目，请勿跨科勾选")
    module_type = units[0]["module_type"]
    title = test_title or (
        f"{units[0]['title']}–{units[-1]['title']} 阶段测"
        if len(units) > 1
        else f"{units[0]['title']} 阶段测"
    )

    plan = get_plan(conn, student_id)
    source = plan["draft"] if plan["draft"] else plan["live"]
    items = []
    for it in source:
        items.append(
            {
                "item_type": it["item_type"],
                "unit_id": it.get("unit_id"),
                "module_type": it.get("module_type"),
                "test_unit_ids": it.get("test_unit_ids") or [],
                "test_title": it.get("test_title") or "",
                "est_minutes": it.get("est_minutes"),
                "status": it.get("status") or "pending",
            }
        )

    unit_id_set = set(unit_ids)
    last_idx = -1
    found: set[str] = set()
    for i, it in enumerate(items):
        if it.get("item_type") == "study" and it.get("unit_id") in unit_id_set:
            last_idx = i
            found.add(it["unit_id"])
    missing = unit_id_set - found
    if missing:
        raise ValueError("请先将所有覆盖单元加入清单后再插测")

    # Reject duplicate test covering exact same units
    for it in items:
        if it.get("item_type") != "test":
            continue
        existing = set(_parse_json_list(it.get("test_unit_ids")) or [])
        if existing == unit_id_set:
            raise ValueError("已有相同范围的阶段测，请勿重复插入")

    insert_at = last_idx + 1
    if after_sort_order is not None:
        insert_at = min(int(after_sort_order) + 1, len(items))

    items.insert(
        insert_at,
        {
            "item_type": "test",
            "unit_id": None,
            "module_type": module_type,
            "test_unit_ids": unit_ids,
            "test_title": title,
            "est_minutes": 20,
            "status": "pending",
        },
    )
    items = normalize_stage_test_positions(items)
    return put_plan_draft(conn, student_id, items)


def plan_status_for_parent(conn: sqlite3.Connection, student_id: str, parent_module: str) -> str:
    rows = conn.execute(
        """
        SELECT p.id, u.parent_module, p.module_type
        FROM plan_items p
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE p.student_id=? AND p.status!='removed'
        """,
        (student_id,),
    ).fetchall()
    for r in rows:
        pm = r["parent_module"] or r["module_type"]
        if r["module_type"] and r["module_type"].startswith("speaking"):
            pm = "speaking"
        if pm == parent_module:
            return "in_plan"
    return "not_in_plan"
