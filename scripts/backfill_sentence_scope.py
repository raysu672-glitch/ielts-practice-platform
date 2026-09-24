#!/usr/bin/env python3
"""按活动日志补回长难句进度，做满的单元直接打勾。

页面曾经只记「这次打开做了几句」，退出再进会把服务器上的进度盖小。
sentence.analysis_open 里仍有真实句号。本脚本用这些句号覆盖进度；
只有活动里的句数不少于当前进度时才写，避免把进度改小。
做满 scope_total 的学习条目会调用 complete_study 打勾。
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task_api import complete_study, ensure_task_tables, replace_scope_keys  # noqa: E402


def _sentence_nums(conn: sqlite3.Connection, student_id: str, plan_item_id: int) -> list[str]:
    rows = conn.execute(
        """
        SELECT detail_json FROM activity_events
        WHERE plan_item_id=? AND target_student_id=?
          AND action='sentence.analysis_open'
        """,
        (plan_item_id, student_id),
    ).fetchall()
    nums: list[str] = []
    for row in rows:
        try:
            detail = json.loads(row["detail_json"] or "{}")
        except json.JSONDecodeError:
            continue
        num = detail.get("sentence_num")
        if num is None:
            continue
        try:
            nums.append(str(int(num)))
        except (TypeError, ValueError):
            continue
    return nums


def main() -> None:
    db = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data" / "ielts_local.db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    ensure_task_tables(conn)
    if not conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='activity_events'"
    ).fetchone():
        print("没有 activity_events，跳过")
        return
    rows = conn.execute(
        """
        SELECT pi.id AS plan_item_id, pi.student_id, pi.unit_id, u.content_version
        FROM plan_items pi
        JOIN task_units u ON u.unit_id = pi.unit_id
        WHERE pi.module_type='sentence' AND pi.item_type='study'
          AND COALESCE(pi.study_completed, 0)=0
        """
    ).fetchall()
    updated = 0
    completed = 0
    for row in rows:
        nums = _sentence_nums(conn, row["student_id"], int(row["plan_item_id"]))
        if not nums:
            continue
        prev = conn.execute(
            """
            SELECT scope_done FROM task_unit_progress
            WHERE student_id=? AND plan_item_id=?
            """,
            (row["student_id"], int(row["plan_item_id"])),
        ).fetchone()
        prev_done = int(prev["scope_done"]) if prev else 0
        if len(set(nums)) < prev_done:
            print(
                f"  跳过 {row['student_id']} {row['unit_id']}："
                f"活动 {len(set(nums))} 句 < 已记 {prev_done}"
            )
            continue
        prog = replace_scope_keys(
            conn, row["student_id"], int(row["plan_item_id"]), nums
        )
        updated += 1
        print(
            f"  {row['student_id']} {row['unit_id']} -> "
            f"{prog['scope_done']}/{prog['scope_total']} {prog['scope_keys']}"
        )
        if prog["scope_total"] and prog["scope_done"] >= prog["scope_total"]:
            complete_study(
                conn,
                row["student_id"],
                int(row["plan_item_id"]),
                str(row["content_version"] or "1"),
                scope_done=int(prog["scope_total"]),
            )
            completed += 1
            print("    已打勾")
    print(f"updated={updated} completed={completed}")


if __name__ == "__main__":
    main()
