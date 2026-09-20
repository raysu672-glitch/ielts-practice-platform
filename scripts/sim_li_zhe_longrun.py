"""长期学习模拟（可用于 6 个月）：复现学生真实习惯，观察长期问题。

与 ``sim_li_zhe_online.py``（30 天、bug 探针为主）的区别：这一份关注**长期**，
重点看清单耗尽、积压长期走势、测试重考次数、跟读到期、空窗期等结构性问题。

习惯设定（李哲画像）：
- 每 3 天断 1 天（第 3 天不打开 App）；
- 周中可投入 90 分钟、周末 180 分钟；
- 时间不够就停，不硬塞。

跑在真实库的**副本**上，不碰 ``data/ielts_local.db``，更不碰阿里云。

用法::

    python scripts/sim_li_zhe_longrun.py --student-id 2026001 --days 180
    python scripts/sim_li_zhe_longrun.py --student-id 2025001 --days 60
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
from sim_li_zhe_online import (  # noqa: E402
    GenduStudent,
    load_online_stats,
    sample_test_score,
    unit_minutes,
)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC_DB = ROOT / "data" / "ielts_local.db"
START = "2026-09-20"
SEED = 20260920

# 习惯：每 3 天断 1 天（第 3 天不开 App）
SKIP_EVERY_N = 3

random.seed(SEED)


def portrait_budget(conn: sqlite3.Connection, sid: str, day: str) -> int:
    row = conn.execute(
        "SELECT weekday_minutes, weekend_minutes FROM student_time_profiles "
        "WHERE student_id=?", (sid,)
    ).fetchone()
    if not row:
        return 90
    wd = int(row["weekday_minutes"] or 90)
    we = int(row["weekend_minutes"] or 90)
    return we if ta.is_weekend(day) else wd


def simulate(
    conn: sqlite3.Connection,
    sid: str,
    start: str,
    days: int,
    stats: dict,
    *,
    skip_every: int = SKIP_EVERY_N,
    verbose: bool = True,
) -> dict:
    original_ymd = ta.china_ymd
    gendu_model = GenduStudent(stats)

    print(f"\n{'=' * 92}")
    print(f"模拟：学生 {sid} · {start} 起 {days} 天 · 每 {skip_every} 天断 1 天")
    print("=" * 92)
    hdr = (f"{'日期':<11}{'周':<3}{'预算':>5}{'实做':>6}{'待做':>5}{'新':>4}{'完成':>5}"
           f"{'积压':>5}{'积压龄':>7}{'测过':>5}{'测过率':>7}{'跟读':>5}")
    print(hdr)
    print("-" * 92)

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    rows: list[dict] = []
    issues: list[str] = []
    first_done_day: dict[int, str] = {}
    first_dispatch_day: dict[int, str] = {}
    test_attempts: dict[int, int] = defaultdict(int)
    test_attempts_pass: dict[int, int] = defaultdict(int)
    reissued: list[tuple[int, str, str]] = []
    gendu_history: list[dict] = []
    gendu_prev_unit = None
    plan_exhausted_day: str | None = None
    empty_dispatch_days: list[str] = []

    def patch(day: str):
        ta.china_ymd = lambda now=None, _d=day: _d  # type: ignore[assignment]

    for i in range(days):
        day = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        patch(day)
        today = ta.get_today(conn, sid)
        items = today.get("items") or []
        weekend = ta.is_weekend(day)
        todo = [
            it for it in items
            if it.get("state") not in ("done_study", "done_pass", "done_fail")
        ]

        fresh_n = sum(1 for it in todo if it.get("priority_class") == "fresh")
        for it in todo:
            pid = int(it["plan_item_id"])
            first_dispatch_day.setdefault(pid, day)
            if pid in first_done_day:
                reissued.append((pid, first_done_day[pid], day))

        budget = portrait_budget(conn, sid, day)
        skipped = (i + 1) % skip_every == 0

        used = 0.0
        did_study = 0
        tests_taken = tests_passed = 0
        gendu_scores: list[float] = []
        stop_reason = ""

        if not items:
            empty_dispatch_days.append(day)
            pending_left = conn.execute(
                "SELECT COUNT(*) c FROM plan_items WHERE student_id=? AND status='pending' "
                "AND ((item_type='study' AND study_completed=0) "
                "     OR (item_type='test' AND test_passed=0))", (sid,)
            ).fetchone()["c"]
            if pending_left == 0 and plan_exhausted_day is None:
                plan_exhausted_day = day
            stop_reason = f"当天无任务（清单剩余未完成 {pending_left} 条）"

        if skipped:
            stop_reason = "今天没打开 App"
        else:
            remaining = float(budget)
            for it in todo:
                mt = str(it.get("module_type") or "")
                est = float(it.get("est_minutes") or 20)
                cost = unit_minutes(stats, mt, est)
                if cost > remaining:
                    stop_reason = (f"时间不够：剩 {remaining:.0f}′，"
                                   f"下一条（{mt}）要 {cost:.0f}′")
                    break
                pid = int(it["plan_item_id"])

                if it.get("item_type") == "test":
                    thr = stats["tests"].get(mt, {}).get("thr") or 80.0
                    for _attempt in range(2):
                        sc = sample_test_score(stats, mt)
                        tests_taken += 1
                        test_attempts[pid] += 1
                        res = ta.submit_stage_test(conn, sid, pid, sc, threshold=thr)
                        if res.get("passed"):
                            tests_passed += 1
                            test_attempts_pass[pid] += 1
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
                first_done_day.setdefault(pid, day)
                used += cost
                remaining -= cost

        after = ta.get_today(conn, sid)
        undone = [
            it for it in (after.get("items") or [])
            if it.get("state") not in ("done_study", "done_pass", "done_fail")
        ]
        backlog_ids = ta.backlog_plan_item_ids(conn, sid)
        # 看板口径：当天没做完的（不含阶段测）。与打包用的 backlog_ids 刻意不同。
        board_backlog = ta.day_unfinished_count(conn, sid, ta._prev_ymd(day))
        stage_pending = len(ta.stage_tests_pending(conn, sid))
        gendu = after.get("gendu_assignment") or {}
        if gendu_prev_unit is not None and gendu.get("current_unit_no") != gendu_prev_unit:
            gendu_model.reset_unit()
        gendu_prev_unit = gendu.get("current_unit_no")
        gendu_history.append({
            "day": day,
            "unit": gendu.get("current_unit_no"),
            "passed": gendu.get("passed_current"),
            "best": max(gendu_scores) if gendu_scores else None,
            "practices": len(gendu_scores),
            "active": bool(gendu.get("active")),
        })

        # 积压「年龄」：最老的积压条目第一次被派发距今多少天
        ages = []
        for pid in backlog_ids:
            d0 = first_dispatch_day.get(int(pid))
            if d0:
                ages.append((datetime.strptime(day, "%Y-%m-%d")
                             - datetime.strptime(d0, "%Y-%m-%d")).days)
        oldest = max(ages) if ages else 0

        rows.append({
            "day": day,
            "weekday": "一二三四五六日"[datetime.strptime(day, "%Y-%m-%d").weekday()],
            "weekend": weekend,
            "items": len(items),
            "todo_n": len(todo),
            "fresh_n": fresh_n,
            "budget": budget,
            "used": round(used, 1),
            "skipped": skipped,
            "did_study": did_study,
            "undone": len(undone),
            "backlog": len(backlog_ids),
            "board_backlog": board_backlog,
            "stage_pending": stage_pending,
            "backlog_oldest": oldest,
            "tests_taken": tests_taken,
            "tests_passed": tests_passed,
            "gendu_unit": gendu.get("current_unit_no"),
            "gendu_best": max(gendu_scores) if gendu_scores else None,
            "stop_reason": stop_reason,
        })

        if verbose and (i < 14 or i % 10 == 0 or i == days - 1):
            gu = rows[-1]["gendu_unit"] if rows[-1]["gendu_unit"] is not None else "-"
            gb = f"{rows[-1]['gendu_best']:.0f}" if rows[-1]["gendu_best"] is not None else "-"
            print(f"{day:<11}{rows[-1]['weekday']:<3}"
                  f"{(0 if skipped else budget):>5}{used:>6.0f}"
                  f"{len(todo):>5}{fresh_n:>4}{did_study:>5}{len(backlog_ids):>5}"
                  f"{oldest:>7}{tests_taken:>5}{tests_passed:>7}{gu:>5}({gb})")

    ta.china_ymd = original_ymd  # type: ignore[assignment]

    studied = [r for r in rows if not r["skipped"]]
    total_dispatched = sum(r["fresh_n"] for r in rows)
    result = {
        "student_id": sid,
        "start": start,
        "days": days,
        "rows": rows,
        "plan_exhausted_day": plan_exhausted_day,
        "empty_dispatch_days": len(empty_dispatch_days),
        "first_empty_day": empty_dispatch_days[0] if empty_dispatch_days else None,
        "study_days": len(studied),
        "skip_days": len(rows) - len(studied),
        "total_minutes": sum(r["used"] for r in rows),
        "total_study_units": sum(r["did_study"] for r in rows),
        "tests_taken": sum(r["tests_taken"] for r in rows),
        "tests_passed": sum(r["tests_passed"] for r in rows),
        "test_retry_max": max(test_attempts.values()) if test_attempts else 0,
        "test_retry_never_pass": sum(
            1 for pid, n in test_attempts.items() if n >= 4 and test_attempts_pass.get(pid, 0) == 0
        ),
        "backlog_final": rows[-1]["backlog"],
        "backlog_peak": max((r["backlog"] for r in rows), default=0),
        "backlog_oldest_final": rows[-1]["backlog_oldest"],
        # 看板口径（新）：当天没做完的条数；当天全做完即为 0。
        "board_backlog_peak": max((r["board_backlog"] for r in rows), default=0),
        "board_backlog_final": rows[-1]["board_backlog"],
        "board_backlog_days_positive": sum(1 for r in rows if r["board_backlog"] > 0),
        "stage_pending_final": rows[-1]["stage_pending"],
        "reissued": len(reissued),
        "gendu_history": gendu_history,
        "issues": issues,
        "first_done_day": first_done_day,
        "first_dispatch_day": first_dispatch_day,
    }
    return result


def summarize(conn: sqlite3.Connection, res: dict) -> None:
    sid, days, rows = res["student_id"], res["days"], res["rows"]
    print(f"\n== 汇总（{sid} · {days} 天）==")
    print(f"  学习 {res['study_days']}/{days} 天（断更 {res['skip_days']} 天）")
    print(f"  实际投入 {res['total_minutes'] / 60:.1f} 小时"
          f"（日均 {res['total_minutes'] / days:.0f} 分钟）")
    print(f"  完成学习单元 {res['total_study_units']} 个"
          f"；派发新单元累计 {sum(r['fresh_n'] for r in rows)} 条")
    print(f"  阶段测：提交 {res['tests_taken']} 次，通过 {res['tests_passed']} 次"
          f"（通过率 {res['tests_passed'] / res['tests_taken'] * 100 if res['tests_taken'] else 0:.1f}%）")
    print(f"  积压：峰值 {res['backlog_peak']} 条，期末 {res['backlog_final']} 条"
          f"，最老积压龄 {res['backlog_oldest_final']} 天")
    print(f"  看板积压（当天没做完，新口径）：峰值 {res['board_backlog_peak']} 条"
          f"，期末 {res['board_backlog_final']} 条"
          f"，出现过积压的天数 {res['board_backlog_days_positive']}/{days}")
    print(f"  待通过阶段测：期末 {res['stage_pending_final']} 项（单独跟踪，不计入积压）")

    print("\n  阶段划分：")
    if res["plan_exhausted_day"]:
        d0 = datetime.strptime(res["start"], "%Y-%m-%d")
        dx = datetime.strptime(res["plan_exhausted_day"], "%Y-%m-%d")
        n = (dx - d0).days
        print(f"    第 {n} 天（{res['plan_exhausted_day']}）清单全部完成"
              f"；此后 {days - n} 天没有任何任务可派")
    else:
        print("    模拟结束时清单仍未做完")
    print(f"    首次出现「当天零任务」的日期：{res['first_empty_day']}"
          f"（共 {res['empty_dispatch_days']} 天）")

    print("\n  长期问题探针：")
    print(f"    [A] 已完成却仍被派发：{res['reissued']} 次")
    print(f"    [B] 单个阶段测最大重考次数：{res['test_retry_max']} 次")
    print(f"    [C] 重考 ≥4 次且一次没过：{res['test_retry_never_pass']} 个")

    # 每个学生未派发过的条目
    never = conn.execute(
        """
        SELECT COUNT(*) c FROM plan_items p
        WHERE p.student_id=? AND p.status='pending'
          AND ((p.item_type='study' AND p.study_completed=0)
               OR (p.item_type='test' AND p.test_passed=0))
          AND NOT EXISTS (SELECT 1 FROM daily_tasks d
                          WHERE d.plan_item_id=p.id AND d.student_id=p.student_id)
        """, (sid,)
    ).fetchone()["c"]
    print(f"    [D] 从未出现在任何一天任务里的未完成条目：{never} 条")

    # 仍被卡住的条目（派发过但没完成）
    stuck = conn.execute(
        """
        SELECT p.module_type, COUNT(*) c FROM plan_items p
        WHERE p.student_id=? AND p.status='pending'
          AND ((p.item_type='study' AND p.study_completed=0)
               OR (p.item_type='test' AND p.test_passed=0))
          AND EXISTS (SELECT 1 FROM daily_tasks d
                      WHERE d.plan_item_id=p.id AND d.student_id=p.student_id)
        GROUP BY p.module_type ORDER BY c DESC
        """, (sid,)
    ).fetchall()
    print(f"    [E] 期末仍未完成的条目（按模块）：")
    for r in stuck:
        print(f"        {str(r['module_type']):<24}{r['c']} 条")

    # 跟读长期轨迹
    gh = res["gendu_history"]
    if gh:
        active = [h for h in gh if h["active"]]
        print(f"\n  跟读：活跃 {len(active)} 天 / 共 {len(gh)} 天")
        units = [h["unit"] for h in active if h["unit"] is not None]
        if units:
            print(f"    课文推进：第 {units[0]} 课 → 第 {units[-1]} 课（共换 {len(set(units))} 课）")
        practiced = sum(1 for h in gh if h["practices"])
        print(f"    实际练习天数：{practiced}")
        last_active = active[-1]["day"] if active else None
        print(f"    最后一次活跃：{last_active}")
        # 到期后是否还有任务
        if last_active and last_active != gh[-1]["day"]:
            print(f"    到期后仍有 {sum(1 for h in gh if h['day'] > last_active)} 天"
                  f"（跟读不再出现）")
        # 每 15 天取一次轨迹
        print("    轨迹（每 15 天）：")
        for h in gh[::15]:
            print(f"      {h['day']} 第 {h['unit']} 课 练 {h['practices']} 次 "
                  f"最高 {h['best'] if h['best'] is None else round(h['best'])} "
                  f"active={h['active']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--student-id", default="2026001")
    ap.add_argument("--start", default=START)
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--db", type=Path, default=SRC_DB)
    ap.add_argument("--skip-every", type=int, default=SKIP_EVERY_N)
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--keep-db", action="store_true")
    args = ap.parse_args()

    sid, start, days = args.student_id, args.start, args.days
    stats = load_online_stats()

    sim_db = args.db.parent / f"_sim_long_{sid}.db"
    if sim_db.exists():
        sim_db.unlink()
    shutil.copy(args.db, sim_db)

    conn = sqlite3.connect(sim_db)
    conn.row_factory = sqlite3.Row
    ta.ensure_task_tables(conn)

    res = simulate(conn, sid, start, days, stats,
                   skip_every=args.skip_every, verbose=True)
    summarize(conn, res)

    # 期末看板
    print("\n  助教看板（最后一天）：")
    try:
        ov = ta.class_overview(conn, task_date=res["rows"][-1]["day"])
        for row in ov.get("students") or []:
            if str(row.get("student_id")) != sid:
                continue
            for k in ("today_total", "today_done", "yesterday_done", "yesterday_total",
                      "yesterday_incomplete", "backlog", "test_fail", "row_status",
                      "today_minutes"):
                if k in row:
                    print(f"    {k}: {row[k]}")
    except Exception as exc:
        print("    看板读取失败：", exc)

    if res["issues"]:
        print("\n  运行期报错：")
        seen = Counter(res["issues"])
        for m, n in seen.most_common(10):
            print(f"    {m}  ×{n}")

    conn.close()
    if args.json_out:
        payload = {k: v for k, v in res.items()
                   if k not in ("first_done_day", "first_dispatch_day")}
        args.json_out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  [json] 已写入 {args.json_out}")
    if not args.keep_db and sim_db.exists():
        sim_db.unlink()
    elif args.keep_db:
        print(f"\n  [keep] 模拟库：{sim_db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
