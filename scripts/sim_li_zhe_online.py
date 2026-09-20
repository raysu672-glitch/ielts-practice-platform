"""李哲 30 天学习模拟 · 线上校准版（复现阿里云真实学生的情况）。

与 ``sim_mock_student_30d.py`` 的区别：那份用教师估算的 est_minutes 和画像预测分；
这一份改用**线上 146 名真实学生的实测分布**来驱动，用来回答两个问题：

1. 系统还有没有 bug（做完却仍积压 / 完成后又被重复派发 / 跟读完却不换课…）；
2. 每日任务的练习量是不是太少、est 是不是虚高、练了有没有效果。

线上校准来源：``backups/aliyun_20260920_092000/ielts_local.db``
- 阶段测分数：按模块取线上均值和标准差抽样；
- 跟读识别率：按线上 91 次跟读事件的真实分布抽样（中位 14.8，54.9% < 50）；
- 单元实际用时：按线上近两周 study_sessions 的中位数（不是 est_minutes）。

跑在真实库的**副本**上，不碰 ``data/ielts_local.db``。

用法::

    python scripts/sim_li_zhe_online.py
    python scripts/sim_li_zhe_online.py --days 30 --json-out _sim_online.json
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import task_api as ta  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ONLINE_DB = ROOT / "backups" / "aliyun_20260920_092000" / "ielts_local.db"
SRC_DB = ROOT / "data" / "ielts_local.db"
SID = "2026001"          # 李哲
START = "2026-09-20"
DAYS = 30
SEED = 20260920

# 李哲画像里的可投入时间（周中 / 周末，分钟）
PORTRAIT_BUDGET = {False: 90, False: 90, True: 180}
# 线上近两周人均每日实际时长（分钟），用于第二组对照
ONLINE_DAILY_MINUTES = 43.0

random.seed(SEED)


# --------------------------------------------------------------------------- #
# 线上分布
# --------------------------------------------------------------------------- #
def load_online_stats() -> dict:
    conn = sqlite3.connect(f"file:{ONLINE_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    tests: dict[str, dict] = {}
    for r in conn.execute(
        """
        SELECT module_type, COUNT(*) n, AVG(score) mean, AVG(pass_threshold) thr
        FROM test_records GROUP BY module_type HAVING n >= 5
        """
    ):
        vals = [float(x["score"]) for x in conn.execute(
            "SELECT score FROM test_records WHERE module_type=?", (r["module_type"],))]
        tests[r["module_type"]] = {
            "n": r["n"],
            "mean": statistics.mean(vals),
            "sd": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
            "median": statistics.median(vals),
            "thr": float(r["thr"] or 80),
            "pass_rate": sum(1 for v in vals if v >= float(r["thr"] or 80)) / len(vals),
        }

    gendu = [float(r["score"]) for r in conn.execute(
        "SELECT score FROM gendu_practice_events WHERE score IS NOT NULL")]

    minutes: dict[str, float] = {}
    for r in conn.execute(
        """
        SELECT module_type, duration_seconds/60.0 AS m FROM study_sessions
        WHERE duration_seconds > 60 AND started_at >= '2026-09-05'
        """
    ):
        minutes.setdefault(r["module_type"], []).append(r["m"])
    minutes = {k: statistics.median(v) for k, v in minutes.items()}

    # 线上学生实际是否完成：完成率
    done_rate = []
    for r in conn.execute(
        """
        SELECT SUM(CASE WHEN study_completed=1 THEN 1 ELSE 0 END)*1.0/COUNT(*) AS rate
        FROM plan_items WHERE status='pending' AND item_type='study'
        GROUP BY student_id HAVING COUNT(*) >= 20
        """
    ):
        done_rate.append(float(r["rate"]))

    # 线上学生每日任务条数
    per_day = [float(r["v"]) for r in conn.execute(
        """
        SELECT COUNT(*)*1.0/COUNT(DISTINCT student_id) AS v
        FROM daily_tasks GROUP BY task_date
        """
    )]

    conn.close()
    return {
        "tests": tests,
        "gendu_scores": gendu,
        "gendu_pass_rate": sum(1 for s in gendu if s >= 70) / len(gendu) if gendu else 0,
        "minutes": minutes,
        "done_rate_median": statistics.median(done_rate) if done_rate else 0,
        "items_per_day_median": statistics.median(per_day) if per_day else 0,
    }


# --------------------------------------------------------------------------- #
# 抽样
# --------------------------------------------------------------------------- #
def sample_test_score(stats: dict, mt: str) -> float:
    """按线上同模块的均值和标准差抽样（writing_translate 线上恒为 0）。"""
    if mt == "writing_translate":
        return 0.0
    s = stats["tests"].get(mt)
    if not s:
        return max(0.0, min(100.0, random.gauss(55, 18)))
    v = random.gauss(s["mean"], s["sd"] or 10.0)
    return round(max(0.0, min(100.0, v)), 1)


class GenduStudent:
    """跟读识别率的真实形态：低分平台 + 某天突然跃升。

    线上 91 次事件的形态（见 ``_tmp_gendu_shape``）：绝大多数学生长期卡在 8–15 分
    （几乎全错），练几天后某一天突然跳到 65–80 过关。例如：

    - 2025113：6 天 18 次全是 8–15 分，一次没过，之后放弃；
    - 2025080：13→11→5→2→62→60→53→2→0→72→74→76（第 5 天跃升）；
    - 2025114：11–15 分练 4 天 → 59/69/69 → 74。

    所以不能按「每次独立抽样」，否则一天 3 次就有 53% 概率过关，30 天能刷完 10 课，
    与线上完全不符。这里按「每天一个当日水平、同一天 3 次分数相近」建模。
    """

    def __init__(self, stats: dict, *, surge_p: float = 0.16):
        pool = [s for s in stats["gendu_scores"] if s < 40]
        self.base = statistics.median(pool) if pool else 13.0
        self.surge_p = surge_p
        self.surged = False
        self.surge_level = 0.0
        self.days_on_unit = 0

    def reset_unit(self) -> None:
        """换课后新课文要重新读，回到低分平台。"""
        self.surged = False
        self.days_on_unit = 0

    def day_scores(self, n: int) -> list[float]:
        self.days_on_unit += 1
        if not self.surged and random.random() < self.surge_p:
            self.surged = True
            self.surge_level = random.gauss(73, 4)
        level = self.surge_level if self.surged else self.base
        return [round(max(0.0, min(100.0, level + random.gauss(0, 2.5))), 1)
                for _ in range(n)]


def unit_minutes(stats: dict, mt: str, est: float) -> float:
    """单元实际耗时：优先用线上同模块实测中位数。"""
    return float(stats["minutes"].get(mt, est))


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--student-id", default=SID)
    ap.add_argument("--start", default=START)
    ap.add_argument("--days", type=int, default=DAYS)
    ap.add_argument("--db", type=Path, default=SRC_DB)
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--keep-db", action="store_true")
    ap.add_argument(
        "--trim-to-online",
        action="store_true",
        help="把李哲的清单削成线上典型形态：删掉全部阶段测，周中只留 3 个模块的配额",
    )
    args = ap.parse_args()

    sid, start, days = args.student_id, args.start, args.days
    stats = load_online_stats()

    print("=" * 78)
    print("线上校准参数（来源：aliyun_20260920_092000）")
    print("=" * 78)
    print(f"  跟读识别率：n={len(stats['gendu_scores'])} 中位="
          f"{statistics.median(stats['gendu_scores']):.1f}  过 70 分比例={stats['gendu_pass_rate']*100:.1f}%")
    print(f"  线上每日任务条数中位：{stats['items_per_day_median']:.1f} 条")
    print(f"  线上学生学习单元完成率中位：{stats['done_rate_median']*100:.1f}%")
    print("  阶段测（线上实测）：")
    for mt, s in sorted(stats["tests"].items(), key=lambda kv: -kv[1]["n"]):
        print(f"    {mt:<22} n={s['n']:<4} 均={s['mean']:5.1f} sd={s['sd']:5.1f} "
              f"线={s['thr']:.0f} 线上通过率={s['pass_rate']*100:5.1f}%")
    print("  单元实际用时中位（分钟）：")
    for mt, m in sorted(stats["minutes"].items(), key=lambda kv: -kv[1]):
        print(f"    {mt:<22} {m:5.1f}")

    # ---- 建模拟库 ----
    sim_db = args.db.parent / f"_sim_online_{sid}.db"
    if sim_db.exists():
        sim_db.unlink()
    shutil.copy(args.db, sim_db)
    conn = sqlite3.connect(sim_db)
    conn.row_factory = sqlite3.Row
    ta.ensure_task_tables(conn)
    original_ymd = ta.china_ymd
    gendu_model = GenduStudent(stats)

    # ---- 可选：削成线上典型清单形态 ----
    # 线上 40 名有配额的学生里，只有 2 人排过阶段测（pending 共 1 条），
    # 周中配额模块数中位 3 个。李哲是 9 个模块 + 31 条阶段测，属于重排。
    ONLINE_MODULES = ["dictation", "reading_synonym", "writing_phrase"]
    if args.trim_to_online:
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND plan_item_id IN "
            "(SELECT id FROM plan_items WHERE student_id=? AND item_type='test')",
            (sid, sid),
        )
        n_test = conn.execute(
            "DELETE FROM plan_items WHERE student_id=? AND item_type='test'", (sid,)
        ).rowcount
        conn.execute(
            "UPDATE student_module_daily_quota SET weekday_units=0, weekend_units=0 "
            "WHERE student_id=?", (sid,),
        )
        for mt in ONLINE_MODULES:
            conn.execute(
                "UPDATE student_module_daily_quota SET weekday_units=1, weekend_units=1 "
                "WHERE student_id=? AND module_type=?", (sid, mt),
            )
        conn.execute(
            "UPDATE student_time_profiles SET weekday_minutes=40, weekend_minutes=90 "
            "WHERE student_id=?", (sid,),
        )
        conn.commit()
        print(f"[trim] 已删除 {n_test} 条阶段测；周中配额改为 "
              f"{' / '.join(ONLINE_MODULES)}；跟读保留")

    def patch(day: str):
        ta.china_ymd = lambda now=None, _d=day: _d  # type: ignore[assignment]

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    rows: list[dict] = []
    issues: list[str] = []
    # bug 探针：记录每个 plan_item 首次完成的日期，以及之后是否又被派发
    first_done_day: dict[int, str] = {}
    reissued: list[tuple[int, str, str]] = []   # (pid, 完成日, 再次被派发日)
    gendu_history: list[dict] = []
    dispatched_rows: dict[int, set[str]] = defaultdict(set)
    gendu_prev_unit = None

    for i in range(days):
        day = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        patch(day)
        today = ta.get_today(conn, sid)
        items = today.get("items") or []
        weekend = ta.is_weekend(day)
        todo = [it for it in items
                if it.get("state") not in ("done_study", "done_pass", "done_fail")]

        for it in todo:
            pid = int(it["plan_item_id"])
            dispatched_rows[pid].add(day)
            if pid in first_done_day:
                reissued.append((pid, first_done_day[pid], day))

        # 学生当天可投入时间：前 20 天按画像，后 10 天贴近线上真实（43 分钟）
        budget = PORTRAIT_BUDGET[weekend] if i < 20 else int(ONLINE_DAILY_MINUTES)
        # 「3 天断 1 天」
        skipped = (i + 1) % 3 == 0

        used = 0.0
        did_study = 0
        tests_taken = tests_passed = 0
        gendu_scores: list[float] = []
        stop_reason = ""
        completed_today: list[int] = []

        if skipped:
            stop_reason = "今天没打开 App"
        else:
            remaining = float(budget)
            for it in todo:
                mt = str(it.get("module_type") or "")
                est = float(it.get("est_minutes") or 20)
                cost = unit_minutes(stats, mt, est)
                if cost > remaining:
                    stop_reason = (f"时间不够：剩 {remaining:.0f}′，下一条（{mt}）"
                                   f"实际要 {cost:.0f}′")
                    break
                pid = int(it["plan_item_id"])

                if it.get("item_type") == "test":
                    thr = stats["tests"].get(mt, {}).get("thr") or 80.0
                    for attempt in range(2):
                        sc = sample_test_score(stats, mt)
                        tests_taken += 1
                        res = ta.submit_stage_test(conn, sid, pid, sc, threshold=thr)
                        if res.get("passed"):
                            tests_passed += 1
                            break
                    used += cost
                    remaining -= cost
                    continue

                if mt == ta.GENDU_MODULE:
                    for sc in gendu_model.day_scores(ta.GENDU_DAILY_PRACTICES):
                        try:
                            ta.report_gendu_practice(
                                conn, sid, plan_item_id=pid, score=sc, task_date=day)
                        except ValueError as exc:
                            issues.append(f"{day} 跟读上报失败：{exc}")
                            break
                        gendu_scores.append(sc)
                    try:
                        ta.complete_study(conn, sid, pid,
                                          str(it.get("content_version") or "1"))
                        did_study += 1
                    except ValueError as exc:
                        issues.append(f"{day} 跟读打勾失败：{exc}")
                    used += cost
                    remaining -= cost
                    continue

                unit = conn.execute(
                    "SELECT content_ref FROM task_units WHERE unit_id=?",
                    (it.get("unit_id"),)).fetchone()
                scope_total, _ = ta._scope_for_unit(unit["content_ref"] if unit else {})
                try:
                    ta.complete_study(conn, sid, pid,
                                      str(it.get("content_version") or "1"),
                                      scope_done=scope_total or None)
                except ValueError as exc:
                    issues.append(f"{day} 学习打勾失败（{mt}）：{exc}")
                    used += cost
                    remaining -= cost
                    continue
                did_study += 1
                completed_today.append(pid)
                first_done_day.setdefault(pid, day)
                used += cost
                remaining -= cost

        after = ta.get_today(conn, sid)
        undone = [it for it in (after.get("items") or [])
                  if it.get("state") not in ("done_study", "done_pass", "done_fail")]
        backlog = ta.backlog_plan_item_ids(conn, sid)
        gendu = after.get("gendu_assignment") or {}
        if gendu_prev_unit is not None and gendu.get("current_unit_no") != gendu_prev_unit:
            gendu_model.reset_unit()   # 换课 → 新课文重新读
        gendu_prev_unit = gendu.get("current_unit_no")
        gendu_history.append({
            "day": day,
            "unit": gendu.get("current_unit_no"),
            "passed": gendu.get("passed_current"),
            "best": max(gendu_scores) if gendu_scores else None,
            "practices": len(gendu_scores),
        })

        rows.append({
            "day": day,
            "weekday": "一二三四五六日"[datetime.strptime(day, "%Y-%m-%d").weekday()],
            "weekend": weekend,
            "items": len(items),
            "todo_n": len(todo),
            "est_min": sum(float(x.get("est_minutes") or 20) for x in todo),
            "real_min": sum(unit_minutes(stats, str(x.get("module_type") or ""),
                                         float(x.get("est_minutes") or 20)) for x in todo),
            "budget": budget,
            "used": round(used, 1),
            "skipped": skipped,
            "did_study": did_study,
            "undone": len(undone),
            "backlog": len(backlog),
            "tests_taken": tests_taken,
            "tests_passed": tests_passed,
            "gendu_unit": gendu.get("current_unit_no"),
            "gendu_best": max(gendu_scores) if gendu_scores else None,
            "stop_reason": stop_reason,
            "completed_today": completed_today,
        })

    ta.china_ymd = original_ymd  # type: ignore[assignment]

    # ---------------------- 报告 ---------------------- #
    print("\n" + "=" * 78)
    print(f"模拟区间：{start} 起 {days} 天  ·  学生：{sid}（李哲）")
    print("=" * 78)
    hdr = (f"{'日期':<11}{'周':<3}{'预算':>5}{'实做':>6}{'est':>6}{'实测':>6}"
           f"{'待做':>5}{'完成':>5}{'积压':>5}{'测过':>5}{'跟读课':>7}{'最高':>6}")
    print(hdr)
    print("-" * 78)
    for r in rows:
        gu = r["gendu_unit"] if r["gendu_unit"] is not None else "-"
        gb = f"{r['gendu_best']:.0f}" if r["gendu_best"] is not None else "-"
        print(f"{r['day']:<11}{r['weekday']:<3}"
              f"{(0 if r['skipped'] else r['budget']):>5}{r['used']:>6.0f}"
              f"{r['est_min']:>6.0f}{r['real_min']:>6.0f}"
              f"{r['todo_n']:>5}{r['did_study']:>5}{r['backlog']:>5}"
              f"{r['tests_passed']:>5}{str(gu):>7}{gb:>6}")

    studied = [r for r in rows if not r["skipped"]]
    print("\n== 汇总 ==")
    print(f"  学习日 {len(studied)}/{days} 天（断更 {days-len(studied)} 天）")
    print(f"  30 天实际投入合计：{sum(r['used'] for r in rows)/60:.1f} 小时"
          f"（日均 {sum(r['used'] for r in rows)/days:.0f} 分钟）")
    print(f"  任务表标注（est）合计：{sum(r['est_min'] for r in rows)/60:.1f} 小时"
          f"｜按线上实测口径：{sum(r['real_min'] for r in rows)/60:.1f} 小时")
    print(f"  每天全部做完的天数：{sum(1 for r in studied if r['undone']==0)}/{len(studied)}")
    print(f"  第 {days} 天：待做 {rows[-1]['todo_n']} 条，积压 {rows[-1]['backlog']} 条")
    print(f"  阶段测：参加 {sum(r['tests_taken'] for r in rows)} 次，"
          f"通过 {sum(r['tests_passed'] for r in rows)} 次")
    print(f"  完成学习单元：{len(first_done_day)} 个")

    print("\n== 问题一：bug 探针 ==")
    print(f"  [1] 「已完成却仍被派发」次数：{len(reissued)}")
    for pid, d0, d1 in reissued[:15]:
        row = conn.execute(
            "SELECT module_type, unit_id FROM plan_items WHERE id=?", (pid,)).fetchone()
        print(f"      pid={pid:<6}{str(row['module_type']):<22} 完成于 {d0}，"
              f"又出现在 {d1}")
    if not reissued:
        print("      （无：完成的条目不会被再次派发）")

    # 积压条目是否真的没做完（用最后一天的次日，才算「跨天仍未完成」）
    day_after = (start_dt + timedelta(days=days)).strftime("%Y-%m-%d")
    bl = ta.backlog_plan_item_ids(conn, sid, before_date=day_after)
    fake = []
    for pid in bl:
        row = conn.execute(
            """SELECT p.item_type, p.study_completed, p.test_passed, p.module_type,
                      (SELECT state FROM daily_tasks WHERE student_id=? AND plan_item_id=?
                       ORDER BY task_date DESC LIMIT 1) AS last_state
               FROM plan_items p WHERE p.id=?""",
            (sid, pid, pid)).fetchone()
        done_flag = row["test_passed"] if row["item_type"] == "test" else row["study_completed"]
        if done_flag:
            fake.append((pid, row["module_type"], row["last_state"]))
    print(f"  [2] 截至第 {days} 天结束（{day_after}）积压 {len(bl)} 条，"
          f"其中「其实已完成」的假积压：{len(fake)}")
    for f in fake[:10]:
        print(f"      pid={f[0]} {f[1]} 最后状态={f[2]}")

    # [3] 已完成条目在 daily_tasks 里残留 todo 行 —— 「做完却还挂着」的数据证据
    residue_rows = conn.execute(
        """
        SELECT d.plan_item_id, d.task_date, p.module_type, p.item_type,
               p.study_completed, p.last_completed_at
        FROM daily_tasks d JOIN plan_items p ON p.id=d.plan_item_id
        WHERE d.student_id=? AND d.state='todo'
          AND (p.study_completed=1 OR p.test_passed=1)
        ORDER BY d.task_date
        """, (sid,)).fetchall()
    print(f"  [3] 已完成条目的残留 todo 行：{len(residue_rows)} 行")
    for r in residue_rows[:12]:
        print(f"      {r['task_date']}  pid={r['plan_item_id']:<6}{r['module_type']:<22}"
              f"完成于 {str(r['last_completed_at'])[:10]}")

    # [3b] 这些残留行会不会让学生端/教师端误报「昨日未完成」
    ghost_days = []
    for r in residue_rows:
        d = r["task_date"]
        tot = conn.execute(
            "SELECT COUNT(*) c FROM daily_tasks WHERE student_id=? AND task_date=?",
            (sid, d)).fetchone()["c"]
        done = conn.execute(
            "SELECT COUNT(*) c FROM daily_tasks WHERE student_id=? AND task_date=? "
            "AND state IN ('done_study','done_pass')", (sid, d)).fetchone()["c"]
        if done < tot:
            ghost_days.append((d, done, tot,
                               sum(1 for x in residue_rows if x["task_date"] == d)))
    print(f"  [3b] 受影响的日期（看板会显示「昨日未完成」）：{len(ghost_days)} 天")
    for d, done, tot, n in ghost_days[:12]:
        print(f"      {d}  完成 {done}/{tot}，其中 {n} 行是已完成条目的残留"
              f"  → 真实完成率 {(done + n)}/{tot}")

    print("\n== 问题二：练习量与效果 ==")
    todo_all = [r for r in rows if not r["skipped"]]
    if todo_all:
        print(f"  todo 表标注 est 合计日均："
              f"{sum(r['est_min'] for r in todo_all)/len(todo_all):.0f} 分钟")
        print(f"  按线上实测口径日均："
              f"{sum(r['real_min'] for r in todo_all)/len(todo_all):.0f} 分钟")
        print(f"  学生实际做完日均：{sum(r['used'] for r in todo_all)/len(todo_all):.0f} 分钟")
    print(f"  跟读：练过 {sum(1 for r in rows if r['gendu_best'] is not None)} 天，"
          f"最高 {max([r['gendu_best'] for r in rows if r['gendu_best'] is not None], default=0):.0f}，"
          f"第 {days} 天仍在第 {rows[-1]['gendu_unit']} 课")
    print("  跟读轨迹（每 5 天取一次）：")
    for h in gendu_history[::5]:
        print(f"    {h['day']} 第 {h['unit']} 课  当日练 {h['practices']} 次  "
              f"最高 {h['best'] if h['best'] is None else round(h['best'])}  "
              f"passed={h['passed']}")

    # 模块进度
    print("\n== 计划进度（第 %d 天）==" % days)
    prog = rows[-1].get("progress") if rows else None
    for r in conn.execute(
        """
        SELECT module_type,
               SUM(CASE WHEN study_completed=1 THEN 1 ELSE 0 END) done, COUNT(*) total
        FROM plan_items WHERE student_id=? AND status='pending' AND item_type='study'
        GROUP BY module_type ORDER BY total DESC
        """, (sid,)):
        print(f"  {r['module_type']:<22} {r['done']:>3}/{r['total']:<4} "
              f"= {r['done']/r['total']*100:5.1f}%")

    # 看板
    print("\n== 助教看板（最后一天）==")
    try:
        ov = ta.class_overview(conn, task_date=rows[-1]["day"])
        for row in ov.get("students") or []:
            if str(row.get("student_id")) != sid:
                continue
            for k in ("today_total", "today_done", "yesterday_done", "yesterday_total",
                      "yesterday_incomplete", "backlog", "test_fail", "row_status",
                      "plan_progress_brief", "today_minutes"):
                if k in row:
                    print(f"  {k}: {row[k]}")
    except Exception as exc:
        print("  看板读取失败：", exc)

    if issues:
        print("\n== 报错 ==")
        for m in issues[:30]:
            print("  -", m)

    cfg = {
        "study_items": conn.execute(
            "SELECT COUNT(*) c FROM plan_items WHERE student_id=? AND item_type='study' "
            "AND status='pending'", (sid,)).fetchone()["c"],
    }
    conn.close()
    if args.json_out:
        payload = {
            "student_id": sid, "start": start, "days": days,
            "trim_to_online": bool(args.trim_to_online),
            "config": cfg,
            "online_stats": {
                "gendu_pass_rate": stats["gendu_pass_rate"],
                "gendu_median": statistics.median(stats["gendu_scores"]),
                "items_per_day_median": stats["items_per_day_median"],
                "done_rate_median": stats["done_rate_median"],
                "minutes": stats["minutes"],
                "tests": stats["tests"],
            },
            "rows": rows,
            "gendu_history": gendu_history,
            "reissued": [{"pid": p, "done": d0, "again": d1} for p, d0, d1 in reissued],
            "residue_rows": len(residue_rows),
            "ghost_days": [{"day": d, "done": do, "total": t, "residue": n}
                           for d, do, t, n in ghost_days],
            "fake_backlog": len(fake),
            "backlog_final": len(bl),
            "completed_units": len(first_done_day),
        }
        args.json_out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n[json] 已写入 {args.json_out}")
    if not args.keep_db and sim_db.exists():
        sim_db.unlink()
    elif args.keep_db:
        print(f"[keep] 模拟库：{sim_db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
