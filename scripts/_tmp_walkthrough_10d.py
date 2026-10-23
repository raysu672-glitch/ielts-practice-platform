#!/usr/bin/env python3
"""近10天走过场排查：翻译抄答案、同义替换连刷、跟读凑次数。"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB = Path(__file__).resolve().parents[1] / "backups" / "aliyun_20261016_143940" / "ielts_local.db"
OUT = Path(__file__).resolve().parents[1] / "_sim_out"
SH = ZoneInfo("Asia/Shanghai")
UTC = timezone.utc

# 以备份库最新业务日为终点，向前 10 天（含首尾）
TO_DATE = "2026-10-16"
FROM_DATE = "2026-10-07"
FROM_UTC = datetime(2026, 10, 6, 16, 0, 0, tzinfo=UTC)  # 10-07 00:00 CST
TO_UTC = datetime(2026, 10, 16, 16, 0, 0, tzinfo=UTC)  # 10-17 00:00 CST


def parse_iso(s: str) -> datetime:
    s = (s or "").strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def china_day(dt: datetime) -> str:
    return dt.astimezone(SH).strftime("%Y-%m-%d")


def load_json(raw: str) -> dict:
    try:
        d = json.loads(raw or "{}")
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def main() -> None:
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    names = {
        r["student_id"]: r["name"]
        for r in conn.execute("SELECT student_id, name FROM students")
    }

    # ---------- 1) 翻译：错后≤20秒改对 ----------
    rows = conn.execute(
        """
        SELECT created_at, actor_id, actor_name, summary, detail_json
        FROM activity_events
        WHERE action='translate.step_submit'
          AND created_at >= ? AND created_at < ?
        ORDER BY actor_id, created_at, id
        """,
        (FROM_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z"), TO_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
    ).fetchall()

    translate_stats = {}  # sid -> stats
    # also spam: same second many wrongs
    spam_by_sid = defaultdict(list)

    by_sid = defaultdict(list)
    for r in rows:
        by_sid[r["actor_id"]].append(r)

    for sid, events in by_sid.items():
        total = 0
        copy_hits = []  # (day, gap)
        last_wrong = {}  # (sid_sentence_step) -> dt
        # spam detection: group by second
        wrong_sec = defaultdict(int)
        for r in events:
            d = load_json(r["detail_json"])
            dt = parse_iso(r["created_at"])
            day = china_day(dt)
            correct = bool(d.get("correct"))
            sent = d.get("sentence_id")
            step = d.get("step")
            key = (sent, step)
            total += 1
            if not correct:
                last_wrong[key] = dt
                sec = dt.astimezone(SH).strftime("%Y-%m-%d %H:%M:%S")
                wrong_sec[sec] += 1
            else:
                prev = last_wrong.get(key)
                if prev is not None:
                    gap = (dt - prev).total_seconds()
                    if 0 <= gap <= 20:
                        copy_hits.append((day, gap, sent, step))
                    last_wrong.pop(key, None)
        spam_days = sorted({sec[:10] for sec, n in wrong_sec.items() if n >= 4})
        spam_max = max(wrong_sec.values()) if wrong_sec else 0
        if spam_max >= 4:
            spam_by_sid[sid] = (spam_max, spam_days)
        if total >= 20 and copy_hits:
            ratio = len(copy_hits) / total
            by_day = defaultdict(int)
            for day, gap, *_ in copy_hits:
                by_day[day] += 1
            translate_stats[sid] = {
                "name": names.get(sid) or events[0]["actor_name"],
                "total": total,
                "copy_n": len(copy_hits),
                "ratio": ratio,
                "avg_gap": sum(g for _, g, *_ in copy_hits) / len(copy_hits),
                "by_day": dict(sorted(by_day.items())),
            }

    # sentence_done speed: translate.sentence_done intervals / day
    sent_done = conn.execute(
        """
        SELECT created_at, actor_id, actor_name, detail_json
        FROM activity_events
        WHERE action='translate.sentence_done'
          AND created_at >= ? AND created_at < ?
        ORDER BY actor_id, created_at
        """,
        (FROM_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z"), TO_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
    ).fetchall()
    translate_fast_days = []  # list of findings
    by_sid_sd = defaultdict(list)
    for r in sent_done:
        by_sid_sd[r["actor_id"]].append(r)
    for sid, evs in by_sid_sd.items():
        by_day = defaultdict(list)
        for r in evs:
            dt = parse_iso(r["created_at"])
            by_day[china_day(dt)].append(dt)
        for day, dts in by_day.items():
            if len(dts) < 4:
                continue
            span = (dts[-1] - dts[0]).total_seconds()
            if span <= 0:
                continue
            per = span / len(dts)
            # 完成≥4句且平均≤60秒/句，且当天有较多抄答案
            copy_day = (translate_stats.get(sid) or {}).get("by_day", {}).get(day, 0)
            if per <= 60 and (copy_day >= 8 or len(dts) >= 6 and per <= 45):
                translate_fast_days.append(
                    {
                        "sid": sid,
                        "name": names.get(sid) or evs[0]["actor_name"],
                        "day": day,
                        "n": len(dts),
                        "span": span,
                        "per": per,
                        "copy_day": copy_day,
                    }
                )

    # ---------- 2) 同义替换连刷 ----------
    syn = conn.execute(
        """
        SELECT created_at, actor_id, actor_name, detail_json
        FROM activity_events
        WHERE action='synonym.group_done'
          AND created_at >= ? AND created_at < ?
        ORDER BY actor_id, created_at
        """,
        (FROM_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z"), TO_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
    ).fetchall()
    synonym_findings = []
    by_sid_sy = defaultdict(list)
    for r in syn:
        by_sid_sy[r["actor_id"]].append(r)
    for sid, evs in by_sid_sy.items():
        # burst: consecutive group_done with avg gap very small
        dts = [parse_iso(r["created_at"]) for r in evs]
        i = 0
        while i < len(dts):
            j = i + 1
            gaps = []
            while j < len(dts):
                g = (dts[j] - dts[j - 1]).total_seconds()
                if g > 30:  # break burst
                    break
                gaps.append(g)
                j += 1
            n = j - i
            if n >= 5 and gaps:
                span = (dts[j - 1] - dts[i]).total_seconds()
                avg = sum(gaps) / len(gaps)
                # 严重：≥6组且均间隔≤5秒；关注：≥5组且均间隔≤15秒
                sev = "severe" if (n >= 6 and avg <= 5) or (n >= 8 and avg <= 8) else (
                    "watch" if avg <= 15 else None
                )
                if sev:
                    synonym_findings.append(
                        {
                            "sid": sid,
                            "name": names.get(sid) or evs[0]["actor_name"],
                            "day": china_day(dts[i]),
                            "n": n,
                            "span": span,
                            "avg": avg,
                            "sev": sev,
                            "t0": dts[i].astimezone(SH).strftime("%H:%M:%S"),
                            "t1": dts[j - 1].astimezone(SH).strftime("%H:%M:%S"),
                        }
                    )
            i = max(j, i + 1)

    # ---------- 3) 跟读凑次数 ----------
    gendu_rows = conn.execute(
        """
        SELECT student_id, task_date, score, created_at, unit_id
        FROM gendu_practice_events
        WHERE task_date >= ? AND task_date <= ?
        ORDER BY student_id, task_date, created_at
        """,
        (FROM_DATE, TO_DATE),
    ).fetchall()
    gendu_findings = []
    by_sd = defaultdict(list)
    for r in gendu_rows:
        by_sd[(r["student_id"], r["task_date"])].append(r)
    for (sid, day), evs in by_sd.items():
        if len(evs) < 3:
            continue
        # take first 3 of the day (task completion threshold)
        first3 = evs[:3]
        scores = [float(x["score"] or 0) for x in first3]
        low = sum(1 for s in scores if s < 10)
        avg = sum(scores) / len(scores)
        span = (parse_iso(first3[-1]["created_at"]) - parse_iso(first3[0]["created_at"])).total_seconds()
        # 凑次数：至少2次接近0，或均分很低且有0分
        if low >= 2 or (avg < 30 and min(scores) < 5):
            gendu_findings.append(
                {
                    "sid": sid,
                    "name": names.get(sid, sid),
                    "day": day,
                    "scores": scores,
                    "avg": avg,
                    "span": span,
                    "n_day": len(evs),
                    "unit": first3[0]["unit_id"],
                }
            )

    # ---------- 4) 任务完成但几乎无学习时长 ----------
    # done_study with study_sessions sum for that day/module very low
    done = conn.execute(
        """
        SELECT dt.student_id, dt.task_date, dt.state, dt.plan_item_id,
               pi.module_type, pi.unit_id, pi.est_minutes
        FROM daily_tasks dt
        JOIN plan_items pi ON pi.id = dt.plan_item_id
        WHERE dt.task_date >= ? AND dt.task_date <= ?
          AND dt.state IN ('done_study','done_pass','done')
        """,
        (FROM_DATE, TO_DATE),
    ).fetchall()
    # study minutes by student/day/module
    sess = conn.execute(
        """
        SELECT student_id, module_type, started_at, duration_seconds
        FROM study_sessions
        WHERE started_at >= ? AND started_at < ?
        """,
        (FROM_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z"), TO_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
    ).fetchall()
    minutes = defaultdict(float)
    for r in sess:
        day = china_day(parse_iso(r["started_at"]))
        minutes[(r["student_id"], day, r["module_type"])] += (r["duration_seconds"] or 0) / 60.0

    zero_dur = []
    for r in done:
        m = minutes.get((r["student_id"], r["task_date"], r["module_type"]), 0.0)
        est = float(r["est_minutes"] or 0)
        # 完成但当日该模块会话总时长 < 1 分钟，且预估≥10分钟
        # 听力基础等可能有记录路径问题，先标关注
        if m < 1.0 and est >= 10:
            zero_dur.append(
                {
                    "sid": r["student_id"],
                    "name": names.get(r["student_id"], r["student_id"]),
                    "day": r["task_date"],
                    "module": r["module_type"],
                    "title": r["unit_id"],
                    "est": est,
                    "actual": round(m, 2),
                    "state": r["state"],
                }
            )

    # ---------- 汇总可疑分 ----------
    findings_by_sid = defaultdict(lambda: {"severe": [], "watch": [], "name": ""})

    for sid, st in translate_stats.items():
        findings_by_sid[sid]["name"] = st["name"]
        level = "severe" if st["ratio"] >= 0.35 and st["copy_n"] >= 25 else (
            "watch" if st["ratio"] >= 0.30 and st["copy_n"] >= 15 else None
        )
        if level:
            day_txt = "；".join(f"{d}有{n}次" for d, n in st["by_day"].items())
            findings_by_sid[sid][level].append(
                f"句子翻译疑似「先错再看答案抄」：近10天{st['total']}次步骤提交中，"
                f"约{st['copy_n']}次（{st['ratio']*100:.0f}%）是「错误后≤20秒内改对」，"
                f"平均改对间隔{st['avg_gap']:.1f}秒。分布：{day_txt}"
            )
        if sid in spam_by_sid:
            mx, days = spam_by_sid[sid]
            findings_by_sid[sid]["watch"].append(
                f"翻译步骤出现连点空交/乱交：同一秒内连续错误≥4次（最多连错{mx}次），"
                f"日期 {', '.join(days)}"
            )

    for f in translate_fast_days:
        findings_by_sid[f["sid"]]["name"] = f["name"]
        findings_by_sid[f["sid"]]["severe"].append(
            f"{f['day']} 翻译：完成{f['n']}句仅用{f['span']:.0f}秒"
            f"（约{f['per']:.0f}秒/句），且当天有{f['copy_day']}次「看答案后改对」"
        )

    for f in synonym_findings:
        findings_by_sid[f["sid"]]["name"] = f["name"]
        if f["sev"] == "severe":
            findings_by_sid[f["sid"]]["severe"].append(
                f"{f['day']} 同义替换连刷：{f['n']}组在{f['span']:.0f}秒内完成"
                f"（{f['t0']}–{f['t1']}），平均组间隔{f['avg']:.1f}秒。"
                f"正常认真做一组通常远不止这个速度。"
            )
        else:
            findings_by_sid[f["sid"]]["watch"].append(
                f"{f['day']} 同义替换偏快：{f['n']}组/{f['span']:.0f}秒，"
                f"均间隔{f['avg']:.1f}秒（可能熟记后快刷，也可能走过场，需结合课堂表现）"
            )

    for f in gendu_findings:
        findings_by_sid[f["sid"]]["name"] = f["name"]
        findings_by_sid[f["sid"]]["severe"].append(
            f"{f['day']} 跟读疑似凑满3次：分数{[round(s,1) for s in f['scores']]}，"
            f"均分{f['avg']:.0f}，跨度{f['span']:.0f}秒。系统按次数完成任务，低分/0分也算次数。"
        )

    # zero duration: only flag if not known path issues for listening_basic alone
    # group and only report students with multiple or non-listening_basic
    zd_by = defaultdict(list)
    for z in zero_dur:
        zd_by[z["sid"]].append(z)
    for sid, zs in zd_by.items():
        non_basic = [z for z in zs if z["module"] != "listening_basic"]
        show = non_basic if non_basic else zs
        if len(show) >= 2 or (non_basic and any(z["actual"] == 0 for z in non_basic)):
            findings_by_sid[sid]["name"] = names.get(sid, sid)
            for z in show[:5]:
                findings_by_sid[sid]["watch"].append(
                    f"{z['day']} {z['module']}（{z['title']}）状态{z['state']}，"
                    f"预估{z['est']:.0f}′但当日会话仅{z['actual']}′"
                    f"（可能走过场，也可能记录路径问题，需核对）"
                )

    # rank
    ranked = []
    for sid, pack in findings_by_sid.items():
        if not pack["severe"] and not pack["watch"]:
            continue
        score = len(pack["severe"]) * 3 + len(pack["watch"])
        ranked.append((score, len(pack["severe"]), sid, pack))
    ranked.sort(reverse=True)

    active = conn.execute(
        """
        SELECT COUNT(DISTINCT actor_id) FROM activity_events
        WHERE actor_role='student' AND created_at >= ? AND created_at < ?
        """,
        (FROM_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z"), TO_UTC.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
    ).fetchone()[0]

    lines = []
    lines.append(f"# 近10天走过场排查（{FROM_DATE} ~ {TO_DATE}）")
    lines.append("")
    lines.append(f"数据来源：线上库备份 `{DB.parent.name}`（库内活动截止约 2026-10-16；今天是 10-19，缺 10-17~19）。")
    lines.append(f"有活动学生约 {active} 人；下列为行为证据较明确者。")
    lines.append("")
    lines.append("判定口径（不是看总时长，而是看「完成方式」）：")
    lines.append("1. **翻译看答案**：答错后页面会显示正确答案；若大量「错误后很快改对」，高度像抄答案过关。")
    lines.append("2. **同义替换连刷**：连续多组完成间隔短到不像在阅读选项。")
    lines.append("3. **跟读凑次数**：当天打满3次但多次接近0分/极低分。")
    lines.append("")
    lines.append("说明：总练习时长长，也可能在其他模块认真做，而某一科走过场；反之亦然。")
    lines.append("")

    high = [x for x in ranked if x[1] >= 1]
    mid = [x for x in ranked if x[1] == 0]

    lines.append("## 一、高可疑（建议优先约谈/抽查）")
    lines.append("")
    if not high:
        lines.append("（本窗口未检出达到「严重」阈值的学生。）")
    for i, (_sc, _sev_n, sid, pack) in enumerate(high, 1):
        lines.append(f"### {i}. {pack['name']}（学号 {sid}）")
        for msg in pack["severe"]:
            lines.append(f"- [**严重**] {msg}")
        for msg in pack["watch"]:
            lines.append(f"- [关注] {msg}")
        lines.append("")

    lines.append("## 二、中等可疑（建议抽查课堂/录音）")
    lines.append("")
    if not mid:
        lines.append("（无仅「关注」级别、无严重项的学生。）")
    for i, (_sc, _sev_n, sid, pack) in enumerate(mid, 1):
        lines.append(f"### {i}. {pack['name']}（学号 {sid}）")
        for msg in pack["watch"]:
            lines.append(f"- {msg}")
        lines.append("")

    lines.append("## 三、补充说明")
    lines.append("")
    lines.append("- 仅「短退出」很多的学生：多数总时长并不短，更像反复进出页面，**单独不足以认定走过场**。")
    lines.append("- 「完成但会话时长≈0」若集中在 listening_basic，需先排除记录路径问题再定罪。")
    lines.append(f"- 翻译抄答案候选（ratio≥30%且次数够）：{len(translate_stats)} 人扫描命中阈值逻辑。")
    lines.append(f"- 同义替换爆发段：{len(synonym_findings)} 段；跟读凑次数日：{len(gendu_findings)} 天次。")

    OUT.mkdir(parents=True, exist_ok=True)
    report = OUT / "walkthrough_10d_report_oct16.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = {
        "window": {"from": FROM_DATE, "to": TO_DATE},
        "active_students": active,
        "high": [
            {"sid": sid, "name": pack["name"], "severe": pack["severe"], "watch": pack["watch"]}
            for _, _, sid, pack in high
        ],
        "mid": [
            {"sid": sid, "name": pack["name"], "watch": pack["watch"]}
            for _, _, sid, pack in mid
        ],
        "translate_stats_top": sorted(
            (
                {"sid": s, **st}
                for s, st in translate_stats.items()
            ),
            key=lambda x: (-x["ratio"], -x["copy_n"]),
        )[:20],
        "gendu_findings": gendu_findings,
        "synonym_findings": synonym_findings,
    }
    (OUT / "walkthrough_10d_oct16.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(report.read_text(encoding="utf-8"))
    print(f"\n[wrote] {report}")
    print(f"[wrote] {OUT / 'walkthrough_10d_oct16.json'}")


if __name__ == "__main__":
    main()
