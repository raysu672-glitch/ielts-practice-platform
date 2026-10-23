"""Simulate teacher assigning tasks to 2 students over 7 calendar days.

Student A: completes every daily task each day.
Student B: completes nothing (carry-over / backlog).

Patches china_ymd so get_today / complete_study see the simulated day.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import task_api as ta  # noqa: E402
from task_api import (  # noqa: E402
    PACK_MODE_UNITS_PER_DAY,
    SHANGHAI,
    apply_draft_to_live,
    backlog_plan_item_ids,
    class_overview,
    complete_study,
    ensure_task_tables,
    get_today,
    preview_daily_pack_items,
    put_plan_draft,
    put_time_profile,
    seed_mvp_units,
    update_scope_progress,
)


START = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)  # Tue
DAYS = 7
STU_A = "S_DONE"
STU_B = "S_SKIP"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL DEFAULT 'x',
            target_score REAL DEFAULT 6.5,
            status TEXT DEFAULT 'active'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE test_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT DEFAULT 'dictation',
            module_name TEXT DEFAULT '',
            test_type TEXT NOT NULL DEFAULT 'module_test',
            score REAL NOT NULL,
            correct_count INTEGER NOT NULL DEFAULT 0,
            total_count INTEGER NOT NULL DEFAULT 0,
            is_passed INTEGER NOT NULL,
            pass_threshold REAL NOT NULL,
            duration_seconds INTEGER DEFAULT 0,
            details TEXT DEFAULT '[]',
            started_at TEXT,
            ended_at TEXT,
            created_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT NOT NULL,
            module_name TEXT,
            session_kind TEXT DEFAULT 'study',
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
            created_at TEXT
        )
        """
    )
    for sid, name in ((STU_A, "全勤生"), (STU_B, "拖延生")):
        conn.execute(
            "INSERT INTO students (student_id, name) VALUES (?, ?)", (sid, name)
        )
    ensure_task_tables(conn)
    seed_mvp_units(conn)
    return conn


def _plan_items() -> list[dict[str, Any]]:
    # Enough for 7 days with weekday 1+1+1 and weekend 2+2+2
    items: list[dict[str, Any]] = []
    for i in range(1, 15):
        items.append({"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"})
    for i in range(1, 15):
        items.append({"item_type": "study", "unit_id": f"dictation_u{i:02d}"})
    for i in range(1, 15):
        items.append({"item_type": "study", "unit_id": f"listening_synonym_u{i:02d}"})
    return items


def _quotas() -> list[dict[str, Any]]:
    return [
        {"module_type": "reading_synonym", "weekday_units": 1, "weekend_units": 2},
        {"module_type": "dictation", "weekday_units": 1, "weekend_units": 2},
        {"module_type": "listening_synonym", "weekday_units": 1, "weekend_units": 2},
    ]


def _teacher_assign(conn: sqlite3.Connection, student_id: str, day0: str) -> None:
    put_time_profile(
        conn,
        student_id,
        {
            "pack_mode": PACK_MODE_UNITS_PER_DAY,
            "module_quotas": _quotas(),
            "effective_from": day0,
        },
    )
    put_plan_draft(conn, student_id, _plan_items(), effective_from=day0)
    apply_draft_to_live(conn, student_id)


def _patch_today(ymd: str):
    ta.china_ymd = lambda now=None: ymd  # type: ignore[assignment]


def _expected_quota(ymd: str) -> int:
    # 3 modules × (2 weekend / 1 weekday)
    return 6 if ta.is_weekend(ymd) else 3


def _complete_all_today(conn: sqlite3.Connection, student_id: str, today: dict) -> int:
    n = 0
    for item in today.get("items") or []:
        if item.get("item_type") != "study":
            continue
        if item.get("state") in ("done_study", "done_pass"):
            continue
        pid = int(item["plan_item_id"])
        unit = conn.execute(
            "SELECT content_version, module_type, content_ref FROM task_units WHERE unit_id=?",
            (item.get("unit_id"),),
        ).fetchone()
        ver = str(unit["content_version"] if unit else "1")
        if unit and unit["module_type"] == "reading_synonym":
            total, _ = ta._scope_for_unit(unit["content_ref"])
            update_scope_progress(conn, student_id, pid, scope_done=total or 10)
        complete_study(conn, student_id, pid, ver)
        n += 1
    return n


def _titles(items: list[dict]) -> list[str]:
    return [str(x.get("title") or x.get("unit_id")) for x in items]


def _check_day(
    conn: sqlite3.Connection,
    ymd: str,
    issues: list[str],
    log: list[str],
) -> None:
    wd = "周末" if ta.is_weekend(ymd) else "工作日"
    expect = _expected_quota(ymd)
    log.append(f"\n=== {ymd}（{wd}，期望新发约 {expect} 条/人，拖延生可能含积压）===")

    for sid, label, mode in (
        (STU_A, "全勤生", "complete"),
        (STU_B, "拖延生", "skip"),
    ):
        today = get_today(conn, sid)
        items = today.get("items") or []
        titles = _titles(items)
        backlog = backlog_plan_item_ids(conn, sid)
        states = [x.get("state") for x in items]
        carry = sum(1 for x in items if x.get("priority_class") == "carry_over")
        fresh = sum(1 for x in items if x.get("priority_class") == "fresh")

        # Teacher schedule day0 vs student today
        live_rows = [
            dict(r)
            for r in conn.execute(
                """
                SELECT item_type, unit_id, module_type, test_unit_ids, test_title, status
                FROM plan_items WHERE student_id=? AND status='pending' ORDER BY sort_order
                """,
                (sid,),
            ).fetchall()
        ]
        teacher = preview_daily_pack_items(
            conn,
            sid,
            live_rows,
            pack_mode=PACK_MODE_UNITS_PER_DAY,
            module_quotas=_quotas(),
            effective_from=ymd,
        )
        t_day0 = (teacher.get("schedule") or [{}])[0]
        t_titles = _titles(t_day0.get("items") or [])
        teacher_match = set(titles) == set(t_titles) and len(titles) == len(t_titles)

        # Upcoming day0 should not overlap today's unfinished if completer...
        upcoming = today.get("upcoming_schedule") or []
        up0_titles = _titles((upcoming[0].get("items") if upcoming else []) or [])

        log.append(
            f"  [{label}] 今日 {len(items)} 条 (fresh={fresh}, carry={carry}) "
            f"积压ID数={len(backlog)} | "
            f"教师今日对齐={'OK' if teacher_match else 'FAIL'} | "
            f"任务={titles}"
        )

        # --- invariants ---
        if len(set(titles)) != len(titles):
            issues.append(f"{ymd} {label}: 今日任务标题重复 {titles}")

        pids = [x.get("plan_item_id") for x in items]
        if len(set(pids)) != len(pids):
            issues.append(f"{ymd} {label}: 今日 plan_item_id 重复 {pids}")

        if not teacher_match:
            issues.append(
                f"{ymd} {label}: 教师排程今日 ≠ 学生今日 "
                f"教师={t_titles} 学生={titles}"
            )

        if mode == "complete":
            # Full completer: no carry_over expected on a fresh day after finishing yesterday
            if carry:
                issues.append(f"{ymd} {label}: 全勤生仍有 carry_over={carry}")
            if len(items) != expect:
                issues.append(
                    f"{ymd} {label}: 全勤生今日条数 {len(items)} ≠ 期望配额 {expect}"
                )
            # After complete, check
            n = _complete_all_today(conn, sid, today)
            after = get_today(conn, sid)
            undone = [
                x
                for x in (after.get("items") or [])
                if x.get("state") not in ("done_study", "done_pass", "done_fail")
            ]
            log.append(f"    → 完成 {n} 条；完成后未完成剩余 {len(undone)}")
            if undone:
                issues.append(
                    f"{ymd} {label}: 完成后仍有未完成 "
                    f"{_titles(undone)}"
                )
            # Completer backlog should be empty after finishing today
            if backlog_plan_item_ids(conn, sid):
                # backlog includes items that appeared in daily and unfinished —
                # after complete today should be empty
                issues.append(
                    f"{ymd} {label}: 完成后仍有 backlog="
                    f"{backlog_plan_item_ids(conn, sid)}"
                )
            # Upcoming should not repeat today's titles (ideal progress)
            if upcoming and set(titles) & set(up0_titles):
                issues.append(
                    f"{ymd} {label}: 后续第1天与今日任务重叠 "
                    f"{set(titles) & set(up0_titles)}"
                )
        else:
            # Skipper: first day = quota; later days capped by today's quota (backlog first)
            if len(items) != expect:
                issues.append(
                    f"{ymd} {label}: 拖延生今日 {len(items)} ≠ 当日配额 {expect}"
                )
            if ymd == START.strftime("%Y-%m-%d"):
                if carry:
                    issues.append(f"{ymd} {label}: 首日不应有 carry_over")
            elif len(backlog) > expect and not carry and fresh:
                issues.append(
                    f"{ymd} {label}: 有积压但今日无 carry_over"
                )

            log.append(
                f"    → 不完成；states={states}; upcoming0={up0_titles[:6]}..."
            )

    # Class overview lights
    noon = datetime.strptime(ymd, "%Y-%m-%d").replace(
        hour=12, tzinfo=SHANGHAI
    )
    overview = class_overview(conn, task_date=ymd, now=noon)
    by_id = {r["student_id"]: r for r in overview.get("students") or []}
    for sid, label, expect_incomplete in (
        (STU_A, "全勤生", False),
        (STU_B, "拖延生", True),
    ):
        row = by_id.get(sid) or {}
        log.append(
            f"  [看板 {label}] total={row.get('today_total')} done={row.get('today_done')} "
            f"backlog={row.get('backlog')} status={row.get('row_status')} "
            f"yesterday_incomplete={row.get('yesterday_incomplete')}"
        )
        if sid == STU_A and row.get("today_total") and row.get("today_done") != row.get(
            "today_total"
        ):
            # A completed during the day — overview after complete should be all done
            if row.get("today_done", 0) < row.get("today_total", 0):
                issues.append(
                    f"{ymd} 看板全勤生未全完成 done={row.get('today_done')}/"
                    f"{row.get('today_total')}"
                )
        if sid == STU_B and ymd > START.strftime("%Y-%m-%d"):
            if not row.get("backlog") and row.get("today_total", 0) <= expect:
                # After day1, skipper should show backlog or swollen today
                pass


def main() -> int:
    conn = _connect()
    day0 = START.strftime("%Y-%m-%d")
    _patch_today(day0)
    _teacher_assign(conn, STU_A, day0)
    _teacher_assign(conn, STU_B, day0)

    issues: list[str] = []
    log: list[str] = [
        f"模拟开始：教师于 {day0} 给 {STU_A}/{STU_B} 下发相同清单",
        f"配额：工作日每科1、周末每科2（阅读+听写+听力同义 → 日3/周末6）",
        f"{STU_A}=每天做完；{STU_B}=从不做",
    ]

    for i in range(DAYS):
        day = (START + timedelta(days=i)).strftime("%Y-%m-%d")
        _patch_today(day)
        _check_day(conn, day, issues, log)

    # Final summary stats
    log.append("\n=== 7 天后库存 ===")
    for sid, label in ((STU_A, "全勤生"), (STU_B, "拖延生")):
        remaining = conn.execute(
            """
            SELECT COUNT(*) AS c FROM plan_items
            WHERE student_id=? AND status='pending' AND study_completed=0
            """,
            (sid,),
        ).fetchone()["c"]
        done = conn.execute(
            """
            SELECT COUNT(*) AS c FROM plan_items
            WHERE student_id=? AND status!='removed' AND study_completed=1
            """,
            (sid,),
        ).fetchone()["c"]
        daily_n = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=?", (sid,)
        ).fetchone()["c"]
        log.append(
            f"  [{label}] 已完成单元={done} 未完成pending={remaining} "
            f"daily_tasks行数={daily_n} backlog={len(backlog_plan_item_ids(conn, sid))}"
        )

    print("\n".join(log))
    print("\n======== 问题清单 ========")
    if not issues:
        print("未发现异常。")
        return 0
    for i, msg in enumerate(issues, 1):
        print(f"{i}. {msg}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
