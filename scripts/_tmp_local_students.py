"""临时：查看本地各学生清单构成与状态（用完即删）。"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(ROOT / "data" / "ielts_local.db")
conn.row_factory = sqlite3.Row

for sid in ("2025001", "2026001", "2099006", "2099014"):
    print("=" * 70)
    print(f"学生 {sid}")
    print("=" * 70)
    r = conn.execute(
        "SELECT COUNT(*) n, "
        "SUM(CASE WHEN item_type='study' THEN 1 ELSE 0 END) study, "
        "SUM(CASE WHEN item_type='test' THEN 1 ELSE 0 END) test, "
        "SUM(CASE WHEN item_type='study' AND study_completed=1 THEN 1 ELSE 0 END) study_done, "
        "SUM(CASE WHEN item_type='test' AND test_passed=1 THEN 1 ELSE 0 END) test_pass "
        "FROM plan_items WHERE student_id=? AND status='pending'", (sid,)
    ).fetchone()
    print(f"  待办 {r['n']} 条 = 学习 {r['study']}（完成 {r['study_done']}）"
          f" + 阶段测 {r['test']}（通过 {r['test_pass']}）")

    print("  按模块：")
    for x in conn.execute(
        """
        SELECT module_type,
               SUM(CASE WHEN item_type='study' THEN 1 ELSE 0 END) study,
               SUM(CASE WHEN item_type='test' THEN 1 ELSE 0 END) test,
               SUM(CASE WHEN item_type='study' AND study_completed=1 THEN 1 ELSE 0 END) done
        FROM plan_items WHERE student_id=? AND status='pending'
        GROUP BY module_type ORDER BY study DESC
        """, (sid,)
    ):
        print(f"    {str(x['module_type']):<22}学 {x['study']:>3}（完成 {x['done']:>2}）"
              f"  测 {x['test']:>2}")

    print("  配额：")
    for x in conn.execute(
        "SELECT module_type, weekday_units wd, weekend_units we "
        "FROM student_module_daily_quota WHERE student_id=? ORDER BY module_type", (sid,)
    ):
        print(f"    {str(x['module_type']):<22}周中 {x['wd']} / 周末 {x['we']}")

    prof = conn.execute(
        "SELECT * FROM student_time_profiles WHERE student_id=?", (sid,)).fetchone()
    if prof:
        print(f"  画像：周中 {prof['weekday_minutes']} 分 / 周末 {prof['weekend_minutes']} 分"
              f" · 装箱 {prof['pack_mode']}")

    asg = conn.execute(
        "SELECT * FROM student_gendu_assignment WHERE student_id=?", (sid,)).fetchone()
    print(f"  跟读：{dict(asg) if asg else '无'}")
    dt = conn.execute(
        "SELECT COUNT(*) n, MIN(task_date) mn, MAX(task_date) mx FROM daily_tasks "
        "WHERE student_id=?", (sid,)).fetchone()
    print(f"  已生成日任务：{dt['n']} 条（{dt['mn']} ~ {dt['mx']}）")
    print()
