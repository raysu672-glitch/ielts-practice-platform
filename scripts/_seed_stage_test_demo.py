"""把阶段测的 11 种情形灌进一个独立的演示库，供真实教师端截图用。

跑法：python scripts/_seed_stage_test_demo.py
产出：data/_stage_test_demo.db（不动 data/ielts_local.db）
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
DST = ROOT / "data" / "_stage_test_demo.db"

TODAY = ta.china_ymd()
YDAY = ta._prev_ymd(TODAY)
BACKDATE = "2026-08-01T00:00:00.000Z"

shutil.copyfile(SRC, DST)
conn = sqlite3.connect(DST)
conn.row_factory = sqlite3.Row
ta.ensure_task_tables(conn)
ta.seed_mvp_units(conn)

# 清掉原有学生数据，只留教师账号（zhangxiaodong / 123456）
for t in (
    "students",
    "plan_items",
    "plan_items_draft",
    "plan_draft_meta",
    "daily_tasks",
    "task_unit_progress",
    "student_time_profiles",
    "student_module_daily_quota",
    "student_plan_pause",
    "student_gendu_assignment",
    "gendu_practice_events",
    "test_records",
    "study_sessions",
    "activity_events",
    "student_attention_events",
    "student_attention_state",
):
    conn.execute(f"DELETE FROM {t}")
conn.commit()

NOTES: list[tuple[str, str]] = []


def new_student(sid: str, name: str, *, units: int = 6, tests: int = 0) -> None:
    conn.execute(
        "INSERT INTO students (student_id, name, password, is_password_changed, "
        "target_score, status, created_at, updated_at) "
        "VALUES (?, ?, 'x', 1, 6.5, 'active', datetime('now'), datetime('now'))",
        (sid, name),
    )
    ta.put_plan_draft(
        conn,
        sid,
        [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, units + 1)
        ],
    )
    for k in range(tests):
        ta.insert_stage_test(
            conn,
            sid,
            unit_ids=[f"reading_synonym_u{i:02d}" for i in range(k * 2 + 1, k * 2 + 3)],
        )
    ta.apply_draft_to_live(conn, sid)
    ta.put_time_profile(
        conn,
        sid,
        {
            "pack_mode": ta.PACK_MODE_UNITS_PER_DAY,
            "module_quotas": [
                {"module_type": "reading_synonym", "weekday_units": 2, "weekend_units": 2}
            ],
            "effective": "today",
        },
    )
    conn.execute("UPDATE plan_items SET created_at=? WHERE student_id=?", (BACKDATE, sid))
    conn.commit()


def study_ids(sid: str, n: int) -> list[int]:
    return [
        int(r["id"])
        for r in conn.execute(
            "SELECT id FROM plan_items WHERE student_id=? AND item_type='study' "
            "ORDER BY sort_order LIMIT ?",
            (sid, n),
        ).fetchall()
    ]


def test_ids(sid: str) -> list[int]:
    return [
        int(r["id"])
        for r in conn.execute(
            "SELECT id FROM plan_items WHERE student_id=? AND item_type='test' "
            "ORDER BY sort_order",
            (sid,),
        ).fetchall()
    ]


def put_day(sid: str, day: str, pids: list[int]) -> None:
    for i, pid in enumerate(pids):
        conn.execute(
            """
            INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked, forced)
            VALUES (?, ?, ?, 'fresh', ?, 'todo', 1, 0)
            """,
            (sid, day, pid, i),
        )
    conn.commit()


def finish_day(sid: str, day: str, keep: list[int] | None = None) -> None:
    """把某天的学习行标成完成（阶段测行不动）。"""
    keep = keep or []
    keep_clause = ""
    params: list[object] = [sid, day, sid]
    if keep:
        keep_clause = " AND plan_item_id NOT IN (%s)" % ",".join("?" * len(keep))
        params.extend(keep)
    conn.execute(
        """
        UPDATE daily_tasks SET state='done_study'
        WHERE student_id=? AND task_date=? AND plan_item_id IN (
            SELECT id FROM plan_items WHERE student_id=? AND item_type='study'
        )
        """
        + keep_clause,
        tuple(params),
    )
    conn.commit()


def note(sid: str, text: str) -> None:
    NOTES.append((sid, text))


# 1 甲：排了测但从没考过；昨天学习任务做完
new_student("2099101", "甲·欠测未考", units=6, tests=2)
put_day("2099101", YDAY, study_ids("2099101", 2))
finish_day("2099101", YDAY)
note("2099101", "欠 2 个阶段测从没考；昨天学习任务全做完 → 绿")

# 2 乙：昨天只排了阶段测、没考
new_student("2099102", "乙·昨天只排测", units=4, tests=1)
put_day("2099102", YDAY, test_ids("2099102"))
note("2099102", "昨天只派 1 个阶段测没考 → 测不算任务量，0/0 绿；欠账在「待通过阶段测」列")

# 3 丙：今天考 1 次没过
new_student("2099103", "丙·今天考1次", units=4, tests=1)
put_day("2099103", YDAY, study_ids("2099103", 2))
finish_day("2099103", YDAY)
put_day("2099103", TODAY, test_ids("2099103"))
ta.submit_stage_test(conn, "2099103", test_ids("2099103")[0], 40, threshold=80)
note("2099103", "今天考 40 分没过，不限次数可继续考")

# 4 丁：今天连考 3 次没过 → 多次未过
new_student("2099104", "丁·多次未过", units=4, tests=1)
put_day("2099104", YDAY, study_ids("2099104", 2))
finish_day("2099104", YDAY)
put_day("2099104", TODAY, test_ids("2099104"))
ta.submit_stage_test(conn, "2099104", test_ids("2099104")[0], 40, threshold=80)
ta.submit_stage_test(conn, "2099104", test_ids("2099104")[0], 55, threshold=80)
ta.submit_stage_test(conn, "2099104", test_ids("2099104")[0], 60, threshold=80)
note("2099104", "今天连考 3 次（40/55/60）没过 → 「多次未过」，仍可继续考")

# 5 戊：今天考过了
new_student("2099105", "戊·今天考过了", units=4, tests=1)
put_day("2099105", YDAY, study_ids("2099105", 2))
finish_day("2099105", YDAY)
put_day("2099105", TODAY, test_ids("2099105"))
ta.submit_stage_test(conn, "2099105", test_ids("2099105")[0], 90, threshold=80)
note("2099105", "今天 90 分过关 → 待通过里消失")

# 6 己：过关后又考砸，不降级
new_student("2099106", "己·过完又考砸", units=4, tests=1)
put_day("2099106", YDAY, study_ids("2099106", 2))
finish_day("2099106", YDAY)
put_day("2099106", TODAY, test_ids("2099106"))
ta.submit_stage_test(conn, "2099106", test_ids("2099106")[0], 88, threshold=80)
ta.submit_stage_test(conn, "2099106", test_ids("2099106")[0], 30, threshold=80)
note("2099106", "88 过关后又考 30 砸了 → test_passed 仍为 1")

# 7 庚：排 10 个阶段测全没考
new_student("2099107", "庚·欠10个测", units=22, tests=10)
put_day("2099107", YDAY, study_ids("2099107", 2))
finish_day("2099107", YDAY)
note("2099107", "欠 10 个阶段测，但昨天任务做完 → 绿灯")

# 8 辛：昨天做一半
new_student("2099108", "辛·昨天做一半", units=4, tests=1)
s = study_ids("2099108", 2)
put_day("2099108", YDAY, s)
finish_day("2099108", YDAY, keep=[s[1]])
note("2099108", "昨天 2 条学习只做 1 条 → 1/2 黄灯")

# 9 壬：昨天一条没做
new_student("2099109", "壬·昨天没做", units=4, tests=1)
put_day("2099109", YDAY, study_ids("2099109", 2))
note("2099109", "昨天一条没做 → 0/2 红灯")

# 10 癸：昨天没考测，今天补考过
new_student("2099110", "癸·今天补考过", units=4, tests=1)
put_day("2099110", YDAY, study_ids("2099110", 1) + test_ids("2099110"))
finish_day("2099110", YDAY)
put_day("2099110", TODAY, test_ids("2099110"))
ta.submit_stage_test(conn, "2099110", test_ids("2099110")[0], 85, threshold=80)
note("2099110", "昨天欠的测试今天补考过关 → 回写成完成")

# 11 子：自然装箱
new_student("2099111", "子·自然装箱", units=4, tests=1)
note("2099111", "不手工干预，让打包器自己排")

# 给每个学生补上今天/昨天的自动装箱
for sid, _ in NOTES:
    ta.ensure_active_plan_daily_tasks(conn, sid, TODAY, lookback_days=1)

conn.commit()

print(f"演示库已生成：{DST}")
print(f"今天={TODAY}  昨天={YDAY}\n")
data = ta.class_overview(conn, task_date=TODAY)
label = {"red": "红", "yellow": "黄", "green": "绿", "none": "无"}
for r in data["students"]:
    y = (
        f"{r['yesterday_done']}/{r['yesterday_total']}"
        if r["yesterday_total"]
        else "—"
    )
    print(
        f"  {r['student_id']} {r['name']:<14} 灯={label[r['row_status']]:<3}"
        f"昨天={y:<6} 积压={r['backlog']:<3}"
        f"待通过={r['stage_test_pending']:<3}多次未过={r['stage_test_needs_attention']:<3}"
        f"今天={r['today_done']}/{r['today_total']}"
    )
print()
print("顶部统计：", data["stats"])
print()
for sid, text in NOTES:
    print(f"  {sid}  {text}")
conn.close()
