"""以「真实学生」节奏跑一遍模拟学生，看每天到底能不能做完。

默认跑李哲（2026001，大一，高考英语 100/150，雅思起点 4.5）30 天。

模拟口径（贴近真人，不是「全勤机器人」）：
- 每天可用时间 = 画像里的 90 分钟（周中）/ 180 分钟（周末）；
- 断更习惯：每 3 天完全不学 1 天；
- 做题顺序按系统给的今日顺序，一条做不动就停下（不硬撑），剩下的变成积压；
- 阶段测分数按他的真实水平抽样，不照达标线给分，所以大概率过不了；
- 跟读按真实识别率（约 40 分）抽样，过关线 70。

在真实库的**副本**上跑，不碰 ``data/ielts_local.db``。

用法::

    python scripts/sim_mock_student_30d.py
    python scripts/sim_mock_student_30d.py --student-id 2026001 --days 30 --start 2026-09-19
"""
from __future__ import annotations

import argparse
import random
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import task_api as ta  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SID = "2026001"
START = "2026-09-19"
DAYS = 30
SEED = 20260919
SRC_DB = ROOT / "data" / "ielts_local.db"
SIM_DB = ROOT / "data" / "_sim_li_zhe.db"
KEEP_DB = False

# 他现在的真实水平（来自学生档案的起点预测）
LEVEL = {
    "dictation": 58.0,
    "listening_basic": 62.0,
    "listening_synonym": 32.0,
    "reading_synonym": 35.0,
    "sentence": 30.0,
    "writing_phrase": 18.0,
    "writing_translate": 22.0,
    "speaking_p1": 4.0,       # band
    "speaking_complex": 4.0,  # band
    "listening_p4_speed": 40.0,
}
BAND_MODULES = {"speaking_p1", "speaking_complex"}
DEFAULT_THRESHOLD = 80.0

random.seed(SEED)


def _thresholds(conn: sqlite3.Connection) -> dict[str, float]:
    out: dict[str, float] = {}
    for r in conn.execute(
        "SELECT module_type, score_6_5 FROM pass_standards WHERE is_active=1"
    ):
        out[str(r["module_type"])] = float(r["score_6_5"])
    return out


def _level(mt: str) -> float:
    return LEVEL.get(mt, 50.0)


def _sample_study_score(mt: str) -> float:
    base = _level(mt)
    if mt in BAND_MODULES:
        return round(max(3.0, min(7.0, base + random.gauss(0, 0.15))), 1)
    return max(0.0, min(100.0, base + random.gauss(0, 5.5)))


def _weekday_cn(ymd: str) -> str:
    return "一二三四五六日"[datetime.strptime(ymd, "%Y-%m-%d").weekday()]


def main() -> int:
    global SID, START, DAYS, SRC_DB, KEEP_DB, SIM_DB

    parser = argparse.ArgumentParser(description="以真实学生节奏模拟每日任务完成情况")
    parser.add_argument("--student-id", default=SID)
    parser.add_argument("--start", default=START, help="起始日期 YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=DAYS)
    parser.add_argument("--db", type=Path, default=SRC_DB, help="源库（只读复制）")
    parser.add_argument("--keep-db", action="store_true", help="保留模拟库副本以便排查")
    parser.add_argument("--json-out", type=Path, default=None, help="把逐日明细写成 JSON")
    args = parser.parse_args()

    SID = args.student_id
    START = args.start
    DAYS = args.days
    SRC_DB = args.db
    KEEP_DB = args.keep_db
    SIM_DB = SRC_DB.parent / f"_sim_{SID}.db"

    if SIM_DB.exists():
        SIM_DB.unlink()
    shutil.copy(SRC_DB, SIM_DB)
    conn = sqlite3.connect(SIM_DB)
    conn.row_factory = sqlite3.Row
    ta.ensure_task_tables(conn)

    thresholds = _thresholds(conn)
    original_ymd = ta.china_ymd

    def patch(day: str):
        ta.china_ymd = lambda now=None, _d=day: _d  # type: ignore[assignment]

    # 学习增益：每完成一个该科单元，水平涨一点（封顶 +15 / +0.8 band）
    gain: dict[str, float] = {k: 0.0 for k in LEVEL}

    rows_log: list[dict] = []
    issues: list[str] = []
    completed_units: list[tuple[str, str, str]] = []

    def _snapshot() -> dict:
        row = conn.execute(
            """
            SELECT
              (SELECT COUNT(*) FROM plan_items
                WHERE student_id=? AND item_type='study' AND study_completed=1) AS study_done,
              (SELECT COUNT(*) FROM plan_items
                WHERE student_id=? AND item_type='test' AND test_passed=1) AS test_passed,
              (SELECT COUNT(*) FROM plan_items
                WHERE student_id=? AND item_type='test') AS test_total
            """,
            (SID, SID, SID),
        ).fetchone()
        return {
            "study_done": int(row["study_done"]),
            "test_passed": int(row["test_passed"]),
            "test_total": int(row["test_total"]),
            "backlog": len(ta.backlog_plan_item_ids(conn, SID)),
        }

    before = _snapshot()
    after: dict = {}

    start_dt = datetime.strptime(START, "%Y-%m-%d")
    for i in range(DAYS):
        day = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        patch(day)
        today = ta.get_today(conn, SID)
        items = today.get("items") or []
        budget = int(today.get("budget_minutes") or 0)
        weekend = ta.is_weekend(day)

        todo = [
            it for it in items
            if it.get("state") not in ("done_study", "done_pass", "done_fail")
        ]
        planned_min = sum(int(it.get("est_minutes") or 20) for it in todo)

        def _split(seq):
            st = [x for x in seq if x.get("item_type") == "study"]
            te = [x for x in seq if x.get("item_type") == "test"]
            return len(st), len(te), sum(int(x.get("est_minutes") or 20) for x in st)

        fresh = [x for x in todo if x.get("priority_class") == "fresh"]
        carry = [x for x in todo if x.get("priority_class") != "fresh"]
        f_st, f_te, f_min = _split(fresh)
        c_st, c_te, c_min = _split(carry)

        # 「3 天断 1 次」：每第 3 天完全不学
        skipped = (i + 1) % 3 == 0

        used = 0
        did_study = 0
        tests_taken = 0
        tests_passed = 0
        tests_failed = 0
        gendu_practices = 0
        gendu_best = None
        stop_reason = ""

        if skipped:
            stop_reason = "今天没打开 App"
        else:
            remaining = budget
            for it in todo:
                mt = str(it.get("module_type") or "")
                cost = int(it.get("est_minutes") or 20)
                if cost > remaining:
                    stop_reason = f"时间不够（剩 {remaining} 分钟，下一条要 {cost} 分钟）"
                    break
                pid = int(it["plan_item_id"])
                if it.get("item_type") == "test":
                    thr = thresholds.get(mt, DEFAULT_THRESHOLD)
                    best = None
                    for attempt in range(2):  # 一天最多两次机会
                        score = _sample_study_score(mt)
                        tests_taken += 1
                        res = ta.submit_stage_test(
                            conn, SID, pid, score, threshold=thr
                        )
                        if res.get("passed"):
                            tests_passed += 1
                            best = score
                            break
                        tests_failed += 1
                        best = score
                        if attempt == 1:
                            break
                    remaining -= cost
                    used += cost
                    continue

                if mt == ta.GENDU_MODULE:
                    for _ in range(ta.GENDU_DAILY_PRACTICES):
                        sc = max(
                            0.0,
                            min(100.0, _level(mt) + gain[mt] * 6 + random.gauss(0, 5)),
                        )
                        try:
                            ta.report_gendu_practice(
                                conn, SID, plan_item_id=pid, score=sc, task_date=day
                            )
                        except ValueError as exc:
                            issues.append(f"{day} 跟读上报失败：{exc}")
                            break
                        gendu_practices += 1
                        gendu_best = sc if gendu_best is None else max(gendu_best, sc)
                    try:
                        ta.complete_study(conn, SID, pid, str(it.get("content_version") or "1"))
                        did_study += 1
                    except ValueError as exc:
                        issues.append(f"{day} 跟读打勾失败：{exc}")
                    remaining -= cost
                    used += cost
                    continue

                unit = conn.execute(
                    "SELECT content_ref FROM task_units WHERE unit_id=?", (it.get("unit_id"),)
                ).fetchone()
                scope_total, _ = ta._scope_for_unit(unit["content_ref"] if unit else {})
                try:
                    ta.complete_study(
                        conn, SID, pid, str(it.get("content_version") or "1"),
                        scope_done=scope_total or None,
                    )
                except ValueError as exc:
                    issues.append(f"{day} 学习打勾失败（{mt}）：{exc}")
                    continue
                did_study += 1
                if it.get("item_type") == "study" and mt != ta.GENDU_MODULE:
                    completed_units.append((day, mt, str(it.get("unit_id"))))
                remaining -= cost
                used += cost
                if mt in gain:
                    gain[mt] = min(gain[mt] + 1.0, 15.0 if mt not in BAND_MODULES else 0.8)

        after = ta.get_today(conn, SID)
        undone = [
            it for it in (after.get("items") or [])
            if it.get("state") not in ("done_study", "done_pass", "done_fail")
        ]
        backlog = ta.backlog_plan_item_ids(conn, SID)
        gendu = after.get("gendu_assignment") or {}

        rows_log.append({
            "day": day,
            "weekday": _weekday_cn(day),
            "weekend": weekend,
            "items": len(items),
            "planned_min": planned_min,
            "fresh_st": f_st,
            "fresh_te": f_te,
            "fresh_min": f_min,
            "carry_st": c_st,
            "carry_te": c_te,
            "carry_min": c_min,
            "budget": budget,
            "used": used,
            "skipped": skipped,
            "did_study": did_study,
            "undone": len(undone),
            "backlog": len(backlog),
            "tests": f"{tests_passed}/{tests_taken}",
            "gendu_best": gendu_best,
            "gendu_unit": gendu.get("current_unit_no"),
            "stop_reason": stop_reason,
            "progress": after.get("progress") or {},
        })

        if not skipped:
            if not undone:
                pass
            elif undone:
                pass

    ta.china_ymd = original_ymd  # type: ignore[assignment]
    after = _snapshot()

    # ---------- 报告 ----------
    print(f"模拟区间：{START} 起 {DAYS} 天（真实库副本，未改动 data/ielts_local.db）")
    print(f"画像预算：周中 {rows_log[0]['budget'] if not rows_log[0]['weekend'] else '?'} "
          f"/ 周末 {rows_log[0]['budget']} 分钟；行为假设：每 3 天断 1 天\n")
    hdr = (f"{'日期':<11}{'周':<3}{'类型':<5}{'新学':>4}{'新测':>4}{'新发分':>7}"
           f"{'积学':>4}{'积测':>4}{'积压分':>7}{'实做分':>7}{'剩':>4}{'积压':>5}{'测过/测':>9}{'跟读课':>7}")
    print(hdr)
    print("-" * 110)
    for r in rows_log:
        kind = "周末" if r["weekend"] else "周中"
        gu = str(r["gendu_unit"]) if r["gendu_unit"] is not None else "-"
        print(
            f"{r['day']:<11}{r['weekday']:<3}{kind:<5}{r['fresh_st']:>4}{r['fresh_te']:>4}"
            f"{r['fresh_min']:>7}{r['carry_st']:>4}{r['carry_te']:>4}{r['carry_min']:>7}"
            f"{r['used']:>7}{r['undone']:>4}{r['backlog']:>5}{r['tests']:>9}{gu:>7}"
        )

    print("\n== 明细：每天为什么停下 ==")
    for r in rows_log:
        if r["stop_reason"]:
            print(f"  {r['day']}：{r['stop_reason']}")

    # 汇总
    studied = [r for r in rows_log if not r["skipped"]]
    over = [r for r in studied if r["planned_min"] > r["budget"]]
    print("\n== 汇总 ==")
    print(f"  学习日 {len(studied)}/{DAYS} 天（断更 {DAYS-len(studied)} 天）")
    print(f"  计划量超预算的天数：{len(over)}/{len(studied)}"
          f"（平均超 {sum(r['planned_min']-r['budget'] for r in over)/max(1,len(over)):.0f} 分钟）")
    base_over = [r for r in studied if (r["fresh_min"] + 20) > r["budget"]]
    print(f"  仅「新发任务」就超预算的天数：{len(base_over)}/{len(studied)}"
          f"（周中新发含跟读约 {studied[0]['fresh_min']+20 if studied else 0} 分钟 vs 预算 90）")
    print(f"  学习日全部做完的天数：{sum(1 for r in studied if r['undone']==0)}/{len(studied)}")
    print(f"  30 天累计实际投入：{sum(r['used'] for r in rows_log)/60:.1f} 小时")
    print(f"  30 天累计计划（按日累加）：{sum(r['planned_min'] for r in rows_log)/60:.1f} 小时")
    print(f"  第 30 天积压：{rows_log[-1]['backlog']} 条")
    tp = sum(int(r["tests"].split("/")[0]) for r in rows_log)
    tt = sum(int(r["tests"].split("/")[1]) for r in rows_log)
    print(f"  阶段测：参加 {tt} 次，通过 {tp} 次")
    print(f"  30 天完成的新学习单元：{len(completed_units)} 个"
          f"（清单共 91 个学习单元）")
    gs = [r["gendu_best"] for r in rows_log if r["gendu_best"] is not None]
    print(f"  跟读：练过 {len(gs)} 天，最高识别率 {max(gs):.0f}" if gs else "  跟读：未练过")
    print(f"  跟读结束仍在第 {rows_log[-1]['gendu_unit']} 课")

    print("\n== 计划进度（第 30 天）==")
    prog = rows_log[-1]["progress"]
    for mod, p in sorted(prog.items()):
        print(f"  {mod:<22} {p}")

    print("\n== 核对：DB 里 study_completed=1 的计划条目 ==")
    for r in conn.execute(
        """
        SELECT module_type, COUNT(*) AS n FROM plan_items
        WHERE student_id=? AND item_type='study' AND study_completed=1
        GROUP BY module_type ORDER BY module_type
        """,
        (SID,),
    ):
        print(f"  {r['module_type']:<22} {r['n']}")
    print(f"  （本次模拟调用 complete_study 成功 {len(completed_units)} 次，去重 "
          f"{len(set(u[2] for u in completed_units))} 个单元）")
    dupes = {}
    for day, mt, uid in completed_units:
        dupes.setdefault(uid, []).append(day)
    repeated = {k: v for k, v in dupes.items() if len(v) > 1}
    if repeated:
        print(f"  重复完成的单元 {len(repeated)} 个：")
        for uid, days in list(repeated.items())[:15]:
            print(f"    {uid}: {days}")

    print("\n== 助教看板（第 30 天）==")
    try:
        ov = ta.class_overview(conn, task_date=rows_log[-1]["day"])
        for row in ov.get("students") or []:
            if str(row.get("student_id")) != SID:
                continue
            for k in ("today_total", "today_done", "backlog", "content_refresh",
                      "test_fail", "row_status", "yesterday_incomplete",
                      "plan_progress_brief"):
                if k in row:
                    print(f"  {k}: {row[k]}")
    except Exception as exc:  # pragma: no cover
        print("  看板读取失败：", exc)

    print("\n== 按周：新发学习单元 vs 积压阶段测（槽位被谁占了）==")
    print(f"  {'周次':<16}{'新发学习':>9}{'新发阶段测':>11}{'积压学习':>9}{'积压阶段测':>11}"
          f"{'完成学习单元':>13}{'阶段测通过/参加':>16}")
    for w in range((DAYS + 6) // 7):
        chunk = rows_log[w * 7:(w + 1) * 7]
        if not chunk:
            continue
        d0, d1 = chunk[0]["day"], chunk[-1]["day"]
        span = f"{d0[5:]}~{d1[5:]}"
        done_units = sum(1 for day, _mt, _uid in completed_units if d0 <= day <= d1)
        tp_w = sum(int(r["tests"].split("/")[0]) for r in chunk)
        tt_w = sum(int(r["tests"].split("/")[1]) for r in chunk)
        print(
            f"  {span:<16}{sum(r['fresh_st'] for r in chunk):>9}"
            f"{sum(r['fresh_te'] for r in chunk):>11}"
            f"{sum(r['carry_st'] for r in chunk):>9}"
            f"{sum(r['carry_te'] for r in chunk):>11}"
            f"{done_units:>13}"
            f"{f'{tp_w}/{tt_w}':>16}"
        )

    if issues:
        print("\n== 报错 / 异常 ==")
        for msg in issues[:40]:
            print("  -", msg)

    conn.close()
    if args.json_out:
        import json as _json

        weekly = []
        for w in range((DAYS + 6) // 7):
            chunk = rows_log[w * 7:(w + 1) * 7]
            if not chunk:
                continue
            d0, d1 = chunk[0]["day"], chunk[-1]["day"]
            weekly.append({
                "span": f"{d0[5:]}~{d1[5:]}",
                "fresh_study": sum(r["fresh_st"] for r in chunk),
                "fresh_test": sum(r["fresh_te"] for r in chunk),
                "carry_study": sum(r["carry_st"] for r in chunk),
                "carry_test": sum(r["carry_te"] for r in chunk),
                "done_units": sum(1 for d, _m, _u in completed_units if d0 <= d <= d1),
                "tests_pass": sum(int(r["tests"].split("/")[0]) for r in chunk),
                "tests_taken": sum(int(r["tests"].split("/")[1]) for r in chunk),
            })
        args.json_out.write_text(
            _json.dumps(
                {
                    "student_id": SID,
                    "start": START,
                    "days": DAYS,
                    "rows": rows_log,
                    "weekly": weekly,
                    "before": before,
                    "after": after,
                    "clean": {
                        "weekday_items": 6,
                        "weekday_minutes": 117,
                        "weekday_budget": 90,
                        "weekend_items": 10,
                        "weekend_minutes": 207,
                        "weekend_budget": 180,
                        "note": "无积压时的新发任务量，取自未完成任何任务的库副本",
                    },
                    "completed_units": len(completed_units),
                },
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )
        print(f"\n[json] 逐日明细已写入 {args.json_out}")
    if not KEEP_DB and SIM_DB.exists():
        SIM_DB.unlink()
    elif KEEP_DB:
        print(f"\n[keep] 模拟库保留在 {SIM_DB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
