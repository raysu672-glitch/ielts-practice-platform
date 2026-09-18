#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理「计划生效日之前」的幽灵 daily_tasks 行（一次性维护脚本）。

背景
----
`ensure_active_plan_daily_tasks` 在 2026-09-17 之前没有回填下限，
把刚上线学生的队首单元塞进了早于计划创建日的日期（例如计划 9/17 11:45
创建，9/16 却凭空出现 3 条任务）。这些行既不是真实布置的任务，又被
`backlog_plan_item_ids` 计入积压，导致「昨日任务 3/3 · 100%」却显示
「积压 3」并标红。

`scripts/task_api.py` 已加下限（commit 81b2f5b）并在计算侧忽略幽灵行，
本脚本用来把库里已经产生的历史脏数据删掉。

用法
----
    python3 scripts/prune_preplan_daily_tasks.py --db data/ielts_local.db            # 预览
    python3 scripts/prune_preplan_daily_tasks.py --db data/ielts_local.db --apply     # 执行
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from task_api import _plan_effective_start  # noqa: E402


def find_ghost_rows(conn: sqlite3.Connection) -> list[tuple[str, str, int]]:
    """返回 [(student_id, task_date, row_count)]，按学生、日期排序。"""
    out: list[tuple[str, str, int]] = []
    students = conn.execute(
        "SELECT student_id FROM students ORDER BY student_id"
    ).fetchall()
    for s in students:
        sid = str(s["student_id"])
        plan_start = _plan_effective_start(conn, sid)
        if not plan_start:
            continue
        rows = conn.execute(
            """
            SELECT task_date, COUNT(*) AS c FROM daily_tasks
            WHERE student_id=? AND task_date < ?
            GROUP BY task_date ORDER BY task_date
            """,
            (sid, plan_start),
        ).fetchall()
        for r in rows:
            out.append((sid, str(r["task_date"]), int(r["c"])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="清理计划生效日之前的幽灵 daily_tasks")
    ap.add_argument("--db", default="data/ielts_local.db", help="SQLite 路径")
    ap.add_argument("--apply", action="store_true", help="真正删除（默认仅预览）")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        print(f"数据库不存在: {args.db}")
        return 1

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    try:
        ghosts = find_ghost_rows(conn)
        if not ghosts:
            print("没有幽灵行，无需清理。")
            return 0

        print(f"发现幽灵行：{len(ghosts)} 组")
        total = 0
        for sid, tdate, n in ghosts:
            print(f"  {sid} {tdate} x{n}")
            total += n
        print(f"合计 {total} 行")

        if not args.apply:
            print("\n（预览模式，未删除。加 --apply 执行）")
            return 0

        deleted = 0
        for sid, tdate, _n in ghosts:
            cur = conn.execute(
                "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
                (sid, tdate),
            )
            deleted += cur.rowcount
        conn.commit()
        print(f"\n已删除 {deleted} 行，提交完成。")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
