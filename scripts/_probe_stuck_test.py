"""探针：阶段测永远考不过时，学生每天还能拿到什么任务？

场景：reading_synonym 配额 2/天，清单 = 学u1..u4 + 一个覆盖 u1-u2 的阶段测。
学生每天都把学习做完，但阶段测一直考不过（模拟「过不去」）。
看 12 天里每天派下来的任务，以及「学习单元还能不能进来」。

跑法：python scripts/_probe_stuck_test.py
产出：data/_probe_stuck.db
"""
from __future__ import annotations

import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import task_api as ta  # noqa: E402

SRC = ROOT / "data" / "ielts_local.db"
DST = ROOT / "data" / "_probe_stuck.db"

shutil.copyfile(SRC, DST)
conn = sqlite3.connect(DST)
conn.row_factory = sqlite3.Row
ta.ensure_task_tables(conn)
ta.seed_mvp_units(conn)

for t in (
    "students", "plan_items", "plan_items_draft", "plan_draft_meta", "daily_tasks",
    "task_unit_progress", "student_time_profiles", "student_module_daily_quota",
    "student_plan_pause", "student_gendu_assignment", "gendu_practice_events",
    "test_records", "study_sessions", "activity_events",
):
    conn.execute(f"DELETE FROM {t}")
conn.commit()

SID = "2099201"
conn.execute(
    "INSERT INTO students (student_id, name, password, is_password_changed, "
    "target_score, status, created_at, updated_at) "
    "VALUES (?, '探针·测不过', 'x', 1, 6.5, 'active', datetime('now'), datetime('now'))",
    (SID,),
)

ta.put_plan_draft(conn, SID, [
    {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 5)
])
ta.insert_stage_test(conn, SID, unit_ids=["reading_synonym_u01", "reading_synonym_u02"])
ta.apply_draft_to_live(conn, SID)
ta.put_time_profile(conn, SID, {
    "pack_mode": ta.PACK_MODE_UNITS_PER_DAY,
    "module_quotas": [
        {"module_type": "reading_synonym", "weekday_units": 2, "weekend_units": 2}
    ],
    "effective": "today",
})
conn.execute("UPDATE plan_items SET created_at='2026-08-01T00:00:00.000Z' WHERE student_id=?", (SID,))
conn.commit()


def title_of(row) -> str:
    it = conn.execute(
        "SELECT p.item_type, p.unit_id, p.test_title, u.title AS unit_title "
        "FROM plan_items p LEFT JOIN task_units u ON u.unit_id=p.unit_id WHERE p.id=?",
        (row["plan_item_id"],),
    ).fetchone()
    if not it:
        return f"#{row['plan_item_id']}"
    if it["item_type"] == "test":
        return f"测[{it['test_title'] or it['unit_id']}]"
    return f"学[{it['unit_title'] or it['unit_id']}]"


start = datetime.strptime("2026-08-10", "%Y-%m-%d").date()
print("=" * 78)
print("阶段测永远考不过 —— 每天派下来的任务")
print("=" * 78)

for d in range(14):
    day = (start + timedelta(days=d)).strftime("%Y-%m-%d")
    conn.execute("DELETE FROM daily_tasks WHERE student_id=? AND task_date>=?", (SID, day))
    conn.commit()
    rows = ta.build_daily_tasks(conn, SID, day)
    label = " ".join(title_of(r) for r in rows) or "(空)"
    # 学生：把这一天的学习都做完，阶段测考 3 次（全不过）
    for r in rows:
        it = conn.execute(
            "SELECT item_type FROM plan_items WHERE id=?", (r["plan_item_id"],)
        ).fetchone()
        if it and it["item_type"] == "study":
            pid = int(r["plan_item_id"])
            unit = conn.execute(
                "SELECT content_version FROM task_units WHERE unit_id=("
                "SELECT unit_id FROM plan_items WHERE id=?)",
                (pid,),
            ).fetchone()
            try:
                ta.complete_study(
                    conn, SID, pid, str(unit["content_version"]), scope_done=1000
                )
            except Exception as exc:  # noqa: BLE001
                print(f"      complete_study err: {exc}")
        elif it and it["item_type"] == "test":
            for _ in range(3):
                try:
                    ta.submit_stage_test(
                        conn, SID, int(r["plan_item_id"]), 30.0, threshold=80.0
                    )
                except Exception as exc:  # noqa: BLE001
                    print(f"      第{_+1}次提交被拒: {exc}")
                    break
    pending = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND status='pending'",
        (SID,),
    ).fetchone()["c"]
    done_study = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND item_type='study' "
        "AND study_completed=1",
        (SID,),
    ).fetchone()["c"]
    print(f"{day}  剩余pending={pending} 已学完={done_study}/4   日任务: {label}")

print()
print("=" * 78)
print("结论区：清单里所有学习都做完后，还剩哪些 pending")
print("=" * 78)
for r in conn.execute(
    "SELECT id, item_type, unit_id, test_title, study_completed, test_passed, status "
    "FROM plan_items WHERE student_id=? ORDER BY sort_order",
    (SID,),
).fetchall():
    print(
        f"  #{r['id']:<3} {r['item_type']:<5} 学完={r['study_completed']} "
        f"测过={r['test_passed']} {r['status']:<7} {r['test_title'] or r['unit_id']}"
    )
conn.close()
