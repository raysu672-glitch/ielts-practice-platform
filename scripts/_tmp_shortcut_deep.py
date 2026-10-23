#!/usr/bin/env python3
"""深挖：同义 group_done 连刷、长难句 translate、完成日总时长。"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "backups" / "aliyun_20261019_155050" / "ielts_local.db"
OUT = ROOT / "_sim_out" / "shortcut_deep_oct19.md"
SH = ZoneInfo("Asia/Shanghai")
UTC = timezone.utc
FROM, TO = "2026-10-09T16:00:00.000Z", "2026-10-19T16:00:00.000Z"
D0, D1 = "2026-10-10", "2026-10-19"


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


def jload(raw: str) -> dict:
    try:
        d = json.loads(raw or "{}")
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def main() -> None:
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    names = {r["student_id"]: r["name"] for r in conn.execute("SELECT student_id,name FROM students")}
    L = ["# 捷径深挖（对齐完成事件）", ""]

    # synonym.group_done bursts
    rows = conn.execute(
        """
        SELECT created_at, actor_id, detail_json, summary
        FROM activity_events
        WHERE action='synonym.group_done' AND created_at>=? AND created_at<?
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    by = defaultdict(list)
    for r in rows:
        by[r["actor_id"]].append((parse_iso(r["created_at"]), jload(r["detail_json"]), r["summary"]))

    bursts = []
    for sid, items in by.items():
        i = 0
        while i < len(items):
            j = i + 1
            while j < len(items) and (items[j][0] - items[j - 1][0]).total_seconds() <= 8:
                j += 1
            n = j - i
            if n >= 5:
                span = (items[j - 1][0] - items[i][0]).total_seconds()
                avg = span / max(n - 1, 1)
                bursts.append((avg, n, span, sid, china_day(items[i][0]), items[i][0], items[j - 1][0]))
            i = j
    bursts.sort()
    L += [f"## 同义 synonym.group_done 连刷（≥5组，邻组≤8s）共 {len(bursts)} 段", ""]
    for avg, n, span, sid, day, a, b in bursts[:30]:
        L.append(
            f"- {names.get(sid,sid)}({sid}) {day}: {n}组/{span:.0f}s 均间隔{avg:.1f}s "
            f"({a.astimezone(SH).strftime('%H:%M:%S')}–{b.astimezone(SH).strftime('%H:%M:%S')})"
        )
    L.append("")

    # per-day: groups and span when complete_ok same day
    L += ["## 同义：完成日「组数/总跨度」偏快", ""]
    completes = conn.execute(
        """
        SELECT actor_id, created_at FROM activity_events
        WHERE action='task.complete_ok' AND module_type='reading_synonym'
          AND created_at>=? AND created_at<?
        """,
        (FROM, TO),
    ).fetchall()
    day_groups = defaultdict(list)
    for sid, items in by.items():
        for dt, d, _ in items:
            day_groups[(sid, china_day(dt))].append(dt)
    fast_days = []
    for r in completes:
        sid = r["actor_id"]
        day = china_day(parse_iso(r["created_at"]))
        dts = sorted(day_groups.get((sid, day), []))
        if len(dts) < 5:
            continue
        span = (dts[-1] - dts[0]).total_seconds()
        per = span / max(len(dts) - 1, 1)
        if per < 20 or (len(dts) >= 8 and span < 180):
            fast_days.append((per, len(dts), span, sid, day))
    fast_days.sort()
    for per, n, span, sid, day in fast_days[:25]:
        L.append(
            f"- {names.get(sid,sid)}({sid}) {day}: 当天{n}组跨度{span:.0f}s 均{per:.1f}s/组（有 complete_ok）"
        )
    L.append("")

    # sentence: translate_submit then analysis quickly / empty-ish
    L += ["## 长难句：translate_submit 与 analysis_open", ""]
    tr = conn.execute(
        """
        SELECT created_at, actor_id, action, detail_json, summary
        FROM activity_events
        WHERE module_type='sentence' AND created_at>=? AND created_at<?
          AND action IN ('sentence.translate_submit','sentence.analysis_open','sentence.unit_done')
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    # look for translate with very short text
    short_tr = 0
    samples = []
    for r in tr:
        if r["action"] != "sentence.translate_submit":
            continue
        d = jload(r["detail_json"])
        text = (d.get("translation") or d.get("text") or d.get("answer") or d.get("user_text") or "")
        if isinstance(text, str) and 0 < len(text.strip()) <= 8:
            short_tr += 1
            if len(samples) < 15:
                samples.append(
                    (names.get(r["actor_id"], r["actor_id"]), china_day(parse_iso(r["created_at"])), text, d)
                )
    L.append(f"- translate_submit 中译文长度≤8：{short_tr} / "
             f"{sum(1 for r in tr if r['action']=='sentence.translate_submit')}")
    for name, day, text, d in samples:
        L.append(f"  - {name} {day}: 「{text}」 keys={list(d.keys())[:8]}")
    L.append("")

    # listening_basic: complete_ok days vs session sum duration
    L += ["## 基础词/听写/词伙：完成日会话合计时长", ""]
    for mod, label in [
        ("listening_basic", "基础词"),
        ("dictation", "听写"),
        ("writing_phrase", "词伙"),
        ("listening_synonym", "听力答案句同义"),
        ("sentence", "长难句"),
        ("listening_p4_speed", "跟读"),
    ]:
        comps = conn.execute(
            """
            SELECT actor_id, created_at FROM activity_events
            WHERE action='task.complete_ok' AND module_type=?
              AND created_at>=? AND created_at<?
            """,
            (mod, FROM, TO),
        ).fetchall()
        short_complete = []
        for r in comps:
            sid = r["actor_id"]
            day = china_day(parse_iso(r["created_at"]))
            dur = conn.execute(
                """
                SELECT COALESCE(SUM(duration_seconds),0) s, COUNT(*) n
                FROM study_sessions
                WHERE student_id=? AND module_type=?
                  AND started_at>=? AND started_at<?
                  AND date(started_at, '+8 hours')=?
                """,
                (sid, mod, FROM, TO, day),
            ).fetchone()
            total = int(dur["s"] or 0)
            if total < 180:
                short_complete.append((total, dur["n"], sid, day))
        short_complete.sort()
        L.append(f"### {label} (`{mod}`) complete_ok={len(comps)}，当日会话合计<3′：{len(short_complete)}")
        for total, n, sid, day in short_complete[:12]:
            L.append(
                f"- {names.get(sid,sid)}({sid}) {day}: 会话合计{total}s / {n}段"
            )
        L.append("")

    # gendu score histogram
    L += ["## 跟读分数直方（近10天全部事件）", ""]
    scores = [
        float(r[0])
        for r in conn.execute(
            "SELECT score FROM gendu_practice_events WHERE task_date BETWEEN ? AND ?",
            (D0, D1),
        )
    ]
    bins = [(0, 10), (10, 40), (40, 70), (70, 100.01)]
    for a, b in bins:
        c = sum(1 for s in scores if a <= s < b)
        L.append(f"- [{a},{b}): {c} ({c/max(len(scores),1):.0%})")
    L.append(f"- 总计 {len(scores)} 次")
    L.append("")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT} bursts={len(bursts)} fast_days={len(fast_days)}")


if __name__ == "__main__":
    main()
