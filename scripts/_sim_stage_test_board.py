"""教师端「阶段测」各种情况的本地模拟。

造一批学生，每人对应一种阶段测情形，然后调用真实的 class_overview /
stage_tests_pending 接口，打印教师端会看到的东西（状态灯、昨日任务、积压、
待通过阶段测）。

跑法：python scripts/_sim_stage_test_board.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 同时写一份带 BOM 的 UTF-8 到文件，避免 Windows 控制台/读取工具判错编码。
_LOG_PATH = ROOT / "_sim_out" / "stage_test_board.txt"
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
_LOG = open(_LOG_PATH, "w", encoding="utf-8-sig")


class _Tee:
    def __init__(self, *streams):
        self._streams = streams

    def write(self, text):
        for s in self._streams:
            s.write(text)
        return len(text)

    def flush(self):
        for s in self._streams:
            s.flush()


sys.stdout = _Tee(sys.__stdout__, _LOG)

import task_api as ta  # noqa: E402
from test_task_api import _connect  # noqa: E402

TODAY = ta.china_ymd()
YDAY = ta._prev_ymd(TODAY)
BACKDATE = "2026-08-01"

conn = _connect()
conn.execute("DELETE FROM students")

SCENARIOS: list[tuple[str, str]] = []


def _note(sid: str, label: str) -> None:
    SCENARIOS.append((sid, label))


def new_student(sid: str, name: str, *, units: int = 6, tests: int = 0) -> None:
    """建一个学生：reading 计划 units 个学习单元 + 每 2 单元插 1 个阶段测。"""
    conn.execute(
        "INSERT INTO students (student_id, name, target_score, status) "
        "VALUES (?, ?, 6.5, 'active')",
        (sid, name),
    )
    put = ta.put_plan_draft(
        conn,
        sid,
        [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, units + 1)
        ],
    )
    for k in range(tests):
        covered = [f"reading_synonym_u{i:02d}" for i in range(k * 2 + 1, k * 2 + 3)]
        ta.insert_stage_test(conn, sid, unit_ids=covered)
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
    conn.execute(
        "UPDATE plan_items SET created_at=? WHERE student_id=?", (BACKDATE + "T00:00:00.000Z", sid)
    )
    conn.commit()


def study_ids(sid: str) -> list[int]:
    return [
        int(r["id"])
        for r in conn.execute(
            "SELECT id FROM plan_items WHERE student_id=? AND item_type='study' "
            "ORDER BY sort_order",
            (sid,),
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


def put_day(sid: str, day: str, pids: list[int], state: str = "todo") -> None:
    for i, pid in enumerate(pids):
        conn.execute(
            """
            INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked, forced)
            VALUES (?, ?, ?, 'fresh', ?, ?, 1, 0)
            """,
            (sid, day, pid, i, state),
        )
    conn.commit()


def finish_day(sid: str, day: str, keep: list[int] | None = None) -> None:
    """把某天的学习行标成完成（阶段测行不管）。

    注意：``keep`` 为空时不能写成 ``NOT IN (NULL)``——SQL 里那是 NULL，恒不成立，
    会导致一行都更新不了。
    """
    keep = keep or []
    keep_clause = ""
    params: list[object] = [sid, day, sid]
    if keep:
        keep_clause = " AND plan_item_id NOT IN (%s)" % ",".join("?" * len(keep))
        params.extend(keep)
    conn.execute(
        """
        UPDATE daily_tasks SET state='done_study'
        WHERE student_id=? AND task_date=? AND plan_item_id NOT IN (
            SELECT id FROM plan_items WHERE student_id=? AND item_type='test'
        )
        """
        + keep_clause,
        tuple(params),
    )
    conn.commit()


def mark_done(sid: str, pid: int) -> None:
    conn.execute(
        "UPDATE plan_items SET study_completed=1 WHERE id=?", (pid,)
    )
    conn.commit()


# ---------------------------------------------------------------- 场景搭建

# 1. 阶段测从没考过（排在队尾，还没轮到）
new_student("2099101", "甲·没考过", units=6, tests=2)
put_day("2099101", YDAY, study_ids("2099101")[:2])
finish_day("2099101", YDAY)
_note("2099101", "排了 2 个阶段测但从没考过；昨天学习任务全做完")

# 2. 昨天只派了阶段测、没考（不考就完不成的那种天）
new_student("2099102", "乙·昨天只排测", units=4, tests=1)
put_day("2099102", YDAY, test_ids("2099102"))
_note("2099102", "昨天只派了 1 个阶段测、没考 → 测不算任务量，昨天 0/0 绿；测欠账在「待通过阶段测」列")

# 3. 今天考了 1 次没过
new_student("2099103", "丙·今天考1次没过", units=4, tests=1)
put_day("2099103", YDAY, study_ids("2099103")[:2])
finish_day("2099103", YDAY)
put_day("2099103", TODAY, test_ids("2099103"))
tid = test_ids("2099103")[0]
ta.submit_stage_test(conn, "2099103", tid, 40, threshold=80)
_note("2099103", "今天考了 1 次，40 分（没过）")

# 4. 今天连考多次都没过（不限重测次数 → 只是触发「多次未过」提示）
new_student("2099104", "丁·今天连考多次没过", units=4, tests=1)
put_day("2099104", YDAY, study_ids("2099104")[:2])
finish_day("2099104", YDAY)
put_day("2099104", TODAY, test_ids("2099104"))
tid = test_ids("2099104")[0]
ta.submit_stage_test(conn, "2099104", tid, 40, threshold=80)
ta.submit_stage_test(conn, "2099104", tid, 55, threshold=80)
ta.submit_stage_test(conn, "2099104", tid, 60, threshold=80)
_note("2099104", "今天连考 3 次（40/55/60）都没过 → 「多次未过」提示助教（仍可继续考）")

# 5. 今天考过了
new_student("2099105", "戊·今天考过了", units=4, tests=1)
put_day("2099105", YDAY, study_ids("2099105")[:2])
finish_day("2099105", YDAY)
put_day("2099105", TODAY, test_ids("2099105"))
tid = test_ids("2099105")[0]
ta.submit_stage_test(conn, "2099105", tid, 90, threshold=80)
_note("2099105", "今天考了 90 分 → 过关")

# 6. 过了之后又考失败（验证「不降级」）
new_student("2099106", "己·过完又考砸", units=4, tests=1)
put_day("2099106", YDAY, study_ids("2099106")[:2])
finish_day("2099106", YDAY)
put_day("2099106", TODAY, test_ids("2099106"))
tid = test_ids("2099106")[0]
ta.submit_stage_test(conn, "2099106", tid, 88, threshold=80)
ta.submit_stage_test(conn, "2099106", tid, 30, threshold=80)
_note("2099106", "先 88 分过关，之后再考 30 分砸了")

# 7. 排了一堆阶段测，从没考过（看会不会一直飘红）
new_student("2099107", "庚·10条没考", units=22, tests=10)
put_day("2099107", YDAY, study_ids("2099107")[:2])
finish_day("2099107", YDAY)
_note("2099107", "排了 10 个阶段测、从没考过；昨天学习任务全做完")

# 8. 昨天没做完 + 有阶段测待通过
new_student("2099108", "辛·昨天做一半", units=4, tests=1)
put_day("2099108", YDAY, study_ids("2099108")[:2])
finish_day("2099108", YDAY, keep=[study_ids("2099108")[1]])
_note("2099108", "昨天 2 条学习任务只做了 1 条")

# 9. 昨天一条没做 + 有阶段测待通过
new_student("2099109", "壬·昨天没做", units=4, tests=1)
put_day("2099109", YDAY, study_ids("2099109")[:2])
_note("2099109", "昨天 2 条学习任务一条没做")

# 10. 昨天阶段测没考、今天补考过了
new_student("2099110", "癸·今天补考过", units=4, tests=1)
put_day("2099110", YDAY, study_ids("2099110")[:1] + test_ids("2099110"))
finish_day("2099110", YDAY)
put_day("2099110", TODAY, test_ids("2099110"))
tid = test_ids("2099110")[0]
ta.submit_stage_test(conn, "2099110", tid, 85, threshold=80)
_note("2099110", "昨天没考阶段测，今天补考 85 分过关")

# 11. 自然装箱（不手工塞任务）：看会不会出现「某天只有阶段测」
new_student("2099111", "子·自然装箱", units=4, tests=1)
_note("2099111", "不手工干预，让打包器自己排（看有没有「某天只有阶段测」）")

# ---------------------------------------------------------------- 跑教师端接口

data = ta.class_overview(conn, task_date=TODAY)
rows = {r["student_id"]: r for r in data["students"]}

print("=" * 108)
print("教师端「班级总览」——阶段测各种情况的反应")
print("=" * 108)
print(f"task_date={TODAY}   昨天={YDAY}")
print()
hdr = (
    f"{'学号':<9}{'灯':<5}{'昨天完成':<10}{'积压':<6}"
    f"{'待通过测':<9}{'多次未过':<10}{'今天':<9}"
)
print(hdr)
print("-" * 108)
label = {"red": "红", "yellow": "黄", "green": "绿", "none": "无"}
for sid, note in SCENARIOS:
    r = rows[sid]
    y = (
        f"{r['yesterday_done']}/{r['yesterday_total']}"
        if r["yesterday_total"]
        else "— 无任务"
    )
    t = (
        f"{r['today_done']}/{r['today_total']}"
        if r["today_total"]
        else "— 无任务"
    )
    ex = r["stage_test_needs_attention"]
    print(
        f"{sid:<9}{label[r['row_status']]:<5}{y:<10}{r['backlog']:<6}"
        f"{r['stage_test_pending']:<9}{(ex if ex else '—'):<10}{t:<9}"
    )
print()
print("学生 → 情形")
print("-" * 108)
for sid, note in SCENARIOS:
    print(f"  {rows[sid]['name']:<16}{note}")

print()
print("=" * 108)
print("「待通过阶段测」明细（点开那一列看到的内容）")
print("=" * 108)
for sid, note in SCENARIOS:
    pend = ta.stage_tests_pending(conn, sid)
    if not pend:
        continue
    print(f"\n{rows[sid]['name']}（{sid}）")
    for p in pend:
        last = "从没考过" if p["never_attempted"] else f"已考 {p['attempts']} 次"
        best = f"{p['best_score']:.0f}" if p["best_score"] is not None else "—"
        flag = "  ← 多次未过，建议助教介入" if p["needs_attention"] else ""
        print(
            f"    {p['module_type']:<18}{p['title']:<28}"
            f"{last:<12}最高 {best:<5}今天已考 {p['attempted_today']} 次{flag}"
        )

print()
print("=" * 108)
print("顶部统计 + 筛选（教师端第一眼看到的东西）")
print("=" * 108)
st = data["stats"]
print(f"  共 {st['total']} 人 · 昨日未完成 {st['yesterday_incomplete']} · "
      f"今日已全完成 {st['today_all_done']} · 需关注 {st['need_attention']} · 无计划 {st['no_plan']}")
print(f"  筛选「有阶段测待通过」命中 {sum(1 for r in rows.values() if r['stage_test_pending'] > 0)} 人")
print(f"  筛选「需关注」(红灯) 命中 {st['need_attention']} 人")

print()
print("=" * 108)
print("「已过关又考砸」的库内真相（验证「一旦过关不降级」）")
print("=" * 108)
tid6 = test_ids("2099106")[0]
p6 = conn.execute(
    "SELECT test_passed, test_attempt_count_today, test_attempt_ymd "
    "FROM plan_items WHERE id=?",
    (tid6,),
).fetchone()
print(f"  plan_items.test_passed          = {p6['test_passed']}   ← 仍是 1（没被打回 0）")
print(f"  plan_items.test_attempt_count_today = {p6['test_attempt_count_today']}")
print("  test_records（每次都如实记录）：")
for r in conn.execute(
    "SELECT score, is_passed, pass_threshold FROM test_records "
    "WHERE student_id='2099106' ORDER BY id"
):
    flag = "过关" if r["is_passed"] else "没过"
    print(f"      {r['score']:.0f} 分 / 达标线 {r['pass_threshold']:.0f} → {flag}")
print("  教师端「待通过阶段测」里已看不到它（=0）")

print()
print("=" * 108)
print("自然装箱：清单学完后会不会只剩一条考不过的测（以及重学有没有接上）")
print("=" * 108)
sid = "2099111"


def _finish(day: str, items: list[dict]) -> None:
    """按学生真实会做的动作推进：学习打勾、阶段测考 40 分（不过）。"""
    for it in items:
        pid = int(it["plan_item_id"])
        if it.get("item_type") == "study":
            u = conn.execute(
                "SELECT content_version FROM task_units WHERE unit_id=("
                "SELECT unit_id FROM plan_items WHERE id=?)",
                (pid,),
            ).fetchone()
            try:
                ta.complete_study(conn, sid, pid, str(u["content_version"]), scope_done=1000)
            except Exception:  # noqa: BLE001
                pass
        else:
            ta.submit_stage_test(conn, sid, pid, 40, threshold=80)


base = ta.china_ymd()
_import_dt = __import__("datetime").datetime
d0 = _import_dt.strptime(base, "%Y-%m-%d").date()
for k in range(-1, 8):
    day = (d0 + __import__("datetime").timedelta(days=k)).strftime("%Y-%m-%d")
    items = ta.build_daily_tasks(conn, sid, day)
    kinds = ["测" if i.get("item_type") == "test" else "学" for i in items]
    tag = ""
    if kinds and all(x == "测" for x in kinds):
        tag = "   ← 只剩阶段测挂着（2026-09-20 决议：不重排科目任务，学生从学习进度自己进）"
    refresh_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND item_type='study' "
        "AND need_refresh=1 AND study_completed=0",
        (sid,),
    ).fetchone()["c"]
    print(
        f"  {day}（{'昨天' if k == -1 else '今天' if k == 0 else f'+{k}'}）  "
        f"{len(items)} 条：{''.join(kinds) or '—'}"
        f"   待换题重学 {refresh_n}{tag}"
    )
    _finish(day, items)

conn.close()
