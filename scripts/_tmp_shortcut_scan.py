#!/usr/bin/env python3
"""扫描近段真实操作：各模块活动量 + 已知捷径信号（不含翻译抄答案细节）。"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "backups" / "aliyun_20261019_155050" / "ielts_local.db"
OUT = ROOT / "_sim_out" / "shortcut_scan_oct19.md"
SH = ZoneInfo("Asia/Shanghai")
UTC = timezone.utc
FROM = "2026-10-09T16:00:00.000Z"  # 10-10 CST
TO = "2026-10-19T16:00:00.000Z"  # 截止备份


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
    names = {r["student_id"]: r["name"] for r in conn.execute("SELECT student_id, name FROM students")}

    lines = [
        "# 捷径扫描（真实操作）",
        "",
        f"- 库：`{DB.name}`（备份 2026-10-19）",
        "- 窗口：约 2026-10-10 ~ 2026-10-19（CST）",
        "- 目标：翻译以外还有哪些模块容易走捷径；用行为证据支撑",
        "",
    ]

    # ---- activity volume ----
    rows = conn.execute(
        """
        SELECT action, COUNT(*) n
        FROM activity_events
        WHERE created_at >= ? AND created_at < ?
        GROUP BY action ORDER BY n DESC
        """,
        (FROM, TO),
    ).fetchall()
    lines += ["## 一、活动类型量级", ""]
    for r in rows[:35]:
        lines.append(f"- `{r['action']}`: {r['n']}")
    lines.append("")

    # ---- daily task modules done ----
    lines += ["## 二、任务完成按模块（done_*）", ""]
    for r in conn.execute(
        """
        SELECT module_key, state, COUNT(*) n
        FROM daily_tasks
        WHERE task_date >= '2026-10-10' AND task_date <= '2026-10-19'
          AND state IN ('done_study','done_pass')
        GROUP BY 1,2 ORDER BY 1,2
        """
    ):
        lines.append(f"- `{r['module_key']}` / {r['state']}: {r['n']}")
    lines.append("")

    # ---- synonym bursts ----
    syn = conn.execute(
        """
        SELECT created_at, actor_id, detail_json
        FROM activity_events
        WHERE action IN ('synonym.group_done','synonym.combo_done','tongyitihuan.group_done')
           OR action LIKE '%synonym%' OR action LIKE '%tongyi%'
          AND created_at >= ? AND created_at < ?
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    # broaden: any action containing tongyi / synonym / replace
    syn = conn.execute(
        """
        SELECT created_at, actor_id, action, detail_json
        FROM activity_events
        WHERE created_at >= ? AND created_at < ?
          AND (
            action LIKE '%synonym%' OR action LIKE '%tongyi%'
            OR action LIKE '%replace%' OR page LIKE '%tongyi%'
          )
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    syn_actions = Counter(r["action"] for r in syn)
    lines += ["## 三、同义替换相关 action", ""]
    for a, n in syn_actions.most_common(20):
        lines.append(f"- `{a}`: {n}")
    lines.append("")

    # burst: consecutive same-sid events within 3s, streaks of >=5
    by_sid = defaultdict(list)
    for r in syn:
        by_sid[r["actor_id"]].append(parse_iso(r["created_at"]))
    bursts = []
    for sid, dts in by_sid.items():
        i = 0
        while i < len(dts):
            j = i + 1
            while j < len(dts) and (dts[j] - dts[j - 1]).total_seconds() <= 5:
                j += 1
            if j - i >= 5:
                span = (dts[j - 1] - dts[i]).total_seconds()
                bursts.append((sid, china_day(dts[i]), j - i, span, dts[i], dts[j - 1]))
            i = j
    bursts.sort(key=lambda x: (x[3] / max(x[2], 1), -x[2]))
    lines += ["### 同义相关连刷段（≥5 事件，相邻≤5秒）", ""]
    for sid, day, n, span, a, b in bursts[:25]:
        avg = span / max(n - 1, 1)
        lines.append(
            f"- {names.get(sid, sid)}({sid}) {day}: {n}次/{span:.0f}s，均间隔{avg:.1f}s "
            f"({a.astimezone(SH).strftime('%H:%M:%S')}–{b.astimezone(SH).strftime('%H:%M:%S')})"
        )
    if not bursts:
        lines.append("- （无）")
    lines.append("")

    # ---- gendu low scores count-as-done ----
    lines += ["## 四、跟读：凑次数（当天≥3次且均分很低/含极低分）", ""]
    gendu = conn.execute(
        """
        SELECT created_at, actor_id, action, summary, detail_json
        FROM activity_events
        WHERE created_at >= ? AND created_at < ?
          AND (
            action LIKE '%gendu%' OR action LIKE '%shadow%'
            OR action LIKE '%asr%' OR page LIKE '%gendu%'
            OR page LIKE '%p4%'
          )
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    g_actions = Counter(r["action"] for r in gendu)
    for a, n in g_actions.most_common(15):
        lines.append(f"- action `{a}`: {n}")
    lines.append("")

    # try extract scores from detail
    day_scores = defaultdict(list)  # (sid,day) -> scores
    for r in gendu:
        d = jload(r["detail_json"])
        score = None
        for k in ("score", "overall", "asr_score", "pronunciation", "total_score"):
            if k in d and d[k] is not None:
                try:
                    score = float(d[k])
                    break
                except Exception:
                    pass
        if score is None and "result" in d and isinstance(d["result"], dict):
            for k in ("score", "overall"):
                if k in d["result"]:
                    try:
                        score = float(d["result"][k])
                        break
                    except Exception:
                        pass
        if score is None:
            continue
        # normalize if 0-100 or 0-1
        if 0 < score <= 1:
            score *= 100
        day_scores[(r["actor_id"], china_day(parse_iso(r["created_at"])))].append(
            (score, parse_iso(r["created_at"]), r["action"])
        )

    pad_days = []
    for (sid, day), items in day_scores.items():
        if len(items) < 3:
            continue
        scores = [x[0] for x in items]
        low = sum(1 for s in scores if s < 10)
        avg = sum(scores) / len(scores)
        if low >= 2 or (avg < 35 and low >= 1):
            span = (items[-1][1] - items[0][1]).total_seconds()
            pad_days.append((sid, day, scores, avg, span, items[0][2]))
    pad_days.sort(key=lambda x: x[3])
    for sid, day, scores, avg, span, act in pad_days[:30]:
        lines.append(
            f"- {names.get(sid, sid)}({sid}) {day}: scores={[round(s,1) for s in scores]} "
            f"均分{avg:.0f} 跨度{span:.0f}s action={act}"
        )
    if not pad_days:
        lines.append("- （按 score 字段未检出；见下方 speaking_records）")
    lines.append("")

    # speaking / asr tables?
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    lines += [f"## 五、相关表（库内）", "", f"- tables: {', '.join(tables)}", ""]

    for t in tables:
        if any(k in t.lower() for k in ("speak", "gendu", "asr", "shadow", "synonym", "phrase", "write", "dictat")):
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({t})")]
            n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            lines.append(f"- `{t}` ({n} rows): {cols[:12]}")
    lines.append("")

    # speaking_best_scores / test_records style
    for t in ("speaking_attempts", "speaking_records", "gendu_records", "asr_records", "study_sessions"):
        if t not in tables:
            continue
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({t})")]
        sample = conn.execute(f"SELECT * FROM {t} ORDER BY rowid DESC LIMIT 2").fetchall()
        lines.append(f"### sample `{t}` cols={cols}")
        for s in sample:
            lines.append(f"- {dict(s)}")
        lines.append("")

    # study_sessions: done with ~0 duration for modules
    if "study_sessions" in tables:
        lines += ["## 六、完成任务但会话时长≈0（按模块）", ""]
        # join daily_tasks done with sessions same day
        zero = conn.execute(
            """
            SELECT d.module_key, COUNT(*) n
            FROM daily_tasks d
            WHERE d.task_date >= '2026-10-10' AND d.task_date <= '2026-10-19'
              AND d.state IN ('done_study','done_pass')
              AND NOT EXISTS (
                SELECT 1 FROM study_sessions s
                WHERE s.student_id = d.student_id
                  AND date(s.started_at, '+8 hours') = d.task_date
                  AND COALESCE(s.duration_sec,0) >= 60
                  AND (
                    s.module_key = d.module_key
                    OR s.page LIKE '%' || replace(d.module_key, '_', '%') || '%'
                  )
              )
            GROUP BY 1 ORDER BY n DESC
            """
        ).fetchall()
        # simpler: sessions with duration 0 and module
        cols = [r[1] for r in conn.execute("PRAGMA table_info(study_sessions)")]
        lines.append(f"study_sessions cols: {cols}")
        try:
            for r in conn.execute(
                """
                SELECT COALESCE(module_key, page, '') mk,
                       COUNT(*) n,
                       SUM(CASE WHEN COALESCE(duration_sec,0) < 30 THEN 1 ELSE 0 END) short_n,
                       AVG(COALESCE(duration_sec,0)) avg_sec
                FROM study_sessions
                WHERE started_at >= ? AND started_at < ?
                GROUP BY 1 ORDER BY n DESC LIMIT 25
                """,
                (FROM, TO),
            ):
                lines.append(
                    f"- `{r['mk']}`: n={r['n']} short<30s={r['short_n']} avg={r['avg_sec']:.0f}s"
                )
        except Exception as e:
            lines.append(f"- query fail: {e}")
            # dump colnames and try duration_minutes
            lines.append(f"- cols={cols}")
        lines.append("")

    # phrase / writing / dictation fast completes via activity
    lines += ["## 七、其他模块 action 抽查", ""]
    for prefix in (
        "phrase",
        "xiezuo",
        "writing",
        "dictat",
        "listening",
        "kouyu",
        "jianya",
        "vocab",
        "cihuo",
        "fanyi",
        "translate",
    ):
        sub = [r for r in rows if prefix in r["action"].lower()]
        if sub:
            lines.append(f"### *{prefix}*")
            for r in sub[:12]:
                lines.append(f"- `{r['action']}`: {r['n']}")
            lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"actions={len(rows)} synonym_bursts={len(bursts)} pad_days={len(pad_days)}")


if __name__ == "__main__":
    main()
