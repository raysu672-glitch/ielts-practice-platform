#!/usr/bin/env python3
"""Assign today's speaking_complex_pattern_p1 task to student 2025001 for local test."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task_api import (  # noqa: E402
    china_ymd,
    ensure_task_tables,
    ensure_active_plan_daily_tasks,
    seed_mvp_units,
)

DB = ROOT / "data" / "ielts_local.db"
SID = "2025001"
UNIT = "speaking_complex_pattern_p1"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    ensure_task_tables(conn)
    seed_mvp_units(conn)

    stu = conn.execute("SELECT student_id, name FROM students WHERE student_id=?", (SID,)).fetchone()
    if not stu:
        raise SystemExit(f"missing student {SID}")
    print("student", dict(stu))

    unit = conn.execute("SELECT unit_id, study_url, content_ref FROM task_units WHERE unit_id=?", (UNIT,)).fetchone()
    print("unit", dict(unit) if unit else None)

    item = conn.execute(
        "SELECT * FROM plan_items WHERE student_id=? AND unit_id=?",
        (SID, UNIT),
    ).fetchone()
    if not item:
        max_sort = conn.execute(
            "SELECT COALESCE(MAX(sort_order),0) FROM plan_items WHERE student_id=?",
            (SID,),
        ).fetchone()[0]
        conn.execute(
            """
            INSERT INTO plan_items (
                student_id, sort_order, item_type, unit_id, module_type,
                est_minutes, status, study_completed, created_at, updated_at
            ) VALUES (?, ?, 'study', ?, 'speaking_complex', 25, 'pending', 0,
                      strftime('%Y-%m-%dT%H:%M:%fZ','now'),
                      strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            """,
            (SID, int(max_sort) + 1, UNIT),
        )
        conn.commit()
        item = conn.execute(
            "SELECT * FROM plan_items WHERE student_id=? AND unit_id=?",
            (SID, UNIT),
        ).fetchone()
        print("created plan_item", dict(item))
    else:
        # reset completion for clean test
        conn.execute(
            """
            UPDATE plan_items SET study_completed=0, study_completed_version=NULL,
              last_completed_at=NULL, need_refresh=0, refresh_reason=NULL,
              status='pending',
              updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE id=?
            """,
            (item["id"],),
        )
        conn.execute(
            "DELETE FROM task_unit_progress WHERE student_id=? AND plan_item_id=?",
            (SID, item["id"]),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM plan_items WHERE id=?", (item["id"],)).fetchone()
        print("reset plan_item", dict(item))

    today = china_ymd()
    conn.execute(
        "DELETE FROM daily_tasks WHERE student_id=? AND task_date=? AND plan_item_id=?",
        (SID, today, item["id"]),
    )
    # clear other todays optional? keep them
    conn.execute(
        """
        INSERT INTO daily_tasks (
            student_id, task_date, plan_item_id, priority_class, sort_in_day,
            state, locked, forced, created_at
        ) VALUES (?, ?, ?, 'fresh', 0, 'todo', 0, 1,
                  strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        """,
        (SID, today, item["id"]),
    )
    conn.commit()

    # also call ensure for packing sanity
    try:
        ensure_active_plan_daily_tasks(conn, SID, today)
        conn.commit()
    except Exception as e:
        print("ensure_active_plan_daily_tasks warn:", e)

    row = conn.execute(
        """
        SELECT d.id, d.task_date, d.state, d.plan_item_id, p.unit_id, p.study_completed
        FROM daily_tasks d JOIN plan_items p ON p.id=d.plan_item_id
        WHERE d.student_id=? AND d.task_date=? AND p.unit_id=?
        """,
        (SID, today, UNIT),
    ).fetchone()
    print("daily", dict(row) if row else None)
    print("OK assign", SID, UNIT, "date", today, "plan_item_id", item["id"])
    conn.close()


if __name__ == "__main__":
    main()
