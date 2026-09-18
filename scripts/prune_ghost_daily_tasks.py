# -*- coding: utf-8 -*-
"""清理「幽灵每日任务」：某条计划条目（plan_items）创建之前的日期上却排了它。

成因（2026-09-18 修复）：跟读（listening_p4_speed）过关后换课时机错误——
回填「昨日」时误触发换课，把当天尚未布置的新课塞进了过去的日期：
  - 学生当天根本没这批任务 → 假积压，且一直标红；
  - 同时按当前课覆盖了当天已完成的旧课记录。

先 dry-run（默认只打印），确认后加 --apply 真正删除。
    python scripts/prune_ghost_daily_tasks.py [db_path]
    python scripts/prune_ghost_daily_tasks.py data/ielts_local.db --apply
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")
DEFAULT_DB = "data/ielts_local.db"

SELECT_GHOSTS = """
SELECT d.id AS daily_id, d.student_id, d.task_date, d.plan_item_id,
       d.priority_class, d.sort_in_day, d.state, d.created_at AS row_created,
       p.unit_id, p.module_type, p.item_type, p.status, p.created_at AS item_created
FROM daily_tasks d
JOIN plan_items p ON p.id = d.plan_item_id
ORDER BY d.student_id, d.task_date, d.sort_in_day
"""


def _shanghai_ymd(raw: str | None) -> str | None:
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        ymd = str(raw)[:10]
        return ymd if len(ymd) == 10 else None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d")


def find_ghosts(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    out: list[sqlite3.Row] = []
    for r in conn.execute(SELECT_GHOSTS).fetchall():
        item_day = _shanghai_ymd(r["item_created"])
        if item_day and str(r["task_date"]) < item_day:
            out.append(r)
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--apply"]
    apply = "--apply" in sys.argv[1:]
    db_path = args[0] if args else DEFAULT_DB
    if not Path(db_path).exists():
        print(f"数据库不存在: {db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ghosts = find_ghosts(conn)
    print(f"库: {db_path}")
    print(f"幽灵行数: {len(ghosts)}")
    by_student: dict[str, list[sqlite3.Row]] = {}
    for r in ghosts:
        by_student.setdefault(str(r["student_id"]), []).append(r)
    for sid, rows in sorted(by_student.items()):
        print(f"\n  学号 {sid}: {len(rows)} 行")
        for r in rows:
            print(
                f"    日期 {r['task_date']} | {r['module_type']} {r['unit_id']}"
                f" | state={r['state']} | 计划条目创建 {str(r['item_created'])[:19]}Z"
            )
    if not ghosts:
        return 0
    if not apply:
        print("\n（dry-run）确认无误后加 --apply 执行删除。")
        return 0
    conn.executemany(
        "DELETE FROM daily_tasks WHERE id=?", [(int(r["daily_id"]),) for r in ghosts]
    )
    conn.commit()
    print(f"\n已删除 {len(ghosts)} 行幽灵每日任务。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
