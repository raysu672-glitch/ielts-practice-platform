#!/usr/bin/env python3
"""本地验证：听力组数动态计算 + 越界单元自愈清理（用临时库，不动 data/ielts_local.db）。"""
from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\ielts-practice-platform")
sys.path.insert(0, str(ROOT / "scripts"))
import task_api as T  # noqa: E402


def main() -> int:
    print("== 词库 → 组数 ==")
    print(f"listening.html 词数 = {T._count_listening_words('listening.html')}")
    print(f"listening_basic.html 词数 = {T._count_listening_words('listening_basic.html')}")
    print(f"DICTATION_GROUP_COUNT = {T.DICTATION_GROUP_COUNT}（期望 48）")
    print(f"LISTENING_BASIC_GROUP_COUNT = {T.LISTENING_BASIC_GROUP_COUNT}（期望 41）")

    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, name TEXT)")
    T.ensure_task_tables(conn)
    T.seed_mvp_units(conn)

    print("\n== seed 后的各模块单元（is_active=1）==")
    for r in conn.execute(
        "SELECT module_type, COUNT(*) c, MAX(unit_no) m FROM task_units WHERE is_active=1 GROUP BY module_type ORDER BY module_type"
    ):
        print(f"  {r['module_type']:22s} 单元={r['c']:3d} 最大 unit_no={r['m']}")
    print(f"  存在越界单元？ {T._has_excess_units(conn)}")

    print("\n== 模拟历史遗留 dictation_u49 + 学生排课 ==")
    conn.execute(
        "INSERT INTO task_units (unit_id, module_type, parent_module, unit_no, title, is_active)"
        " VALUES ('dictation_u49','dictation','dictation',49,'第49组',1)"
    )
    conn.execute("INSERT INTO students (student_id, name) VALUES ('2025001','测试生')")
    pid = conn.execute(
        "INSERT INTO plan_items (student_id, sort_order, item_type, unit_id, module_type, status)"
        " VALUES ('2025001', 9, 'study', 'dictation_u49', 'dictation', 'pending')"
    ).lastrowid
    conn.execute(
        "INSERT INTO daily_tasks (student_id, task_date, plan_item_id, state) VALUES ('2025001', ?, ?, 'todo')",
        (T.china_ymd(), pid),
    )
    conn.commit()
    u49_active = conn.execute("SELECT is_active FROM task_units WHERE unit_id='dictation_u49'").fetchone()[0]
    pi_status = conn.execute("SELECT status FROM plan_items WHERE id=?", (pid,)).fetchone()[0]
    dt_rows = conn.execute("SELECT COUNT(*) FROM daily_tasks WHERE plan_item_id=?", (pid,)).fetchone()[0]
    print(f"  注入后 has_excess = {T._has_excess_units(conn)}")
    print(f"  seed 前：u49 is_active = {u49_active}")
    print(f"  seed 前：plan_items 状态 = {pi_status}")
    print(f"  seed 前：daily_tasks 行数 = {dt_rows}")

    T.seed_mvp_units(conn)

    u49_active = conn.execute("SELECT is_active FROM task_units WHERE unit_id='dictation_u49'").fetchone()[0]
    pi_status = conn.execute("SELECT status FROM plan_items WHERE id=?", (pid,)).fetchone()[0]
    dt_rows = conn.execute("SELECT COUNT(*) FROM daily_tasks WHERE plan_item_id=?", (pid,)).fetchone()[0]
    print("\n== seed 后 ==")
    print(f"  u49 is_active = {u49_active}")
    print(f"  plan_items 状态 = {pi_status}")
    print(f"  daily_tasks 行数 = {dt_rows}")
    print(f"  has_excess = {T._has_excess_units(conn)}")
    print(f"  各模块单元数 = {dict((r['module_type'], r['c']) for r in conn.execute('SELECT module_type, COUNT(*) c FROM task_units WHERE is_active=1 GROUP BY module_type'))}")
    conn.close()
    Path(db).unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
