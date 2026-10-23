#!/usr/bin/env python3
"""基于最新线上备份，用真实操作印证各模块捷径。"""
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
OUT = ROOT / "_sim_out" / "shortcut_behavior_oct19.md"
SH = ZoneInfo("Asia/Shanghai")
UTC = timezone.utc
D0, D1 = "2026-10-10", "2026-10-19"
FROM = "2026-10-09T16:00:00.000Z"
TO = "2026-10-19T16:00:00.000Z"


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
    names = {
        r["student_id"]: r["name"]
        for r in conn.execute("SELECT student_id, name FROM students")
    }

    L: list[str] = [
        "# 其他训练捷径：真实操作分析（2026-10-10 ~ 10-19）",
        "",
        f"数据：`{DB.parent.name}/ielts_local.db`",
        "句子翻译已改，本报告聚焦其余模块。",
        "",
    ]

    # ---- module mix of done tasks ----
    L += ["## 1. 近10天完成任务按模块", ""]
    done_mod_rows = conn.execute(
        """
        SELECT COALESCE(u.module_type, pi.module_type, '(unknown)') mt,
               COALESCE(u.completion_rule, '') rule,
               d.state, COUNT(*) n
        FROM daily_tasks d
        LEFT JOIN plan_items pi ON pi.id = d.plan_item_id
        LEFT JOIN task_units u ON u.unit_id = pi.unit_id
        WHERE d.task_date BETWEEN ? AND ?
          AND d.state IN ('done_study','done_pass')
        GROUP BY 1,2,3 ORDER BY n DESC
        """,
        (D0, D1),
    ).fetchall()
    for r in done_mod_rows:
        L.append(f"- `{r['mt']}` rule=`{r['rule']}` {r['state']}: {r['n']}")
    L.append("")

    # ---- gendu: score distribution on done days ----
    L += ["## 2. 跟读：完成日分数分布（有真实证据）", ""]
    # days with count>=3 from gendu_practice_events
    g_rows = conn.execute(
        """
        SELECT student_id, task_date, score, created_at, unit_id
        FROM gendu_practice_events
        WHERE task_date BETWEEN ? AND ?
        ORDER BY student_id, task_date, created_at
        """,
        (D0, D1),
    ).fetchall()
    by_day = defaultdict(list)
    for r in g_rows:
        by_day[(r["student_id"], r["task_date"])].append(float(r["score"] or 0))

    pad = []
    ok = []
    for (sid, day), scores in by_day.items():
        if len(scores) < 3:
            continue
        avg = sum(scores) / len(scores)
        low = sum(1 for s in scores if s < 10)
        hi = max(scores)
        item = (sid, day, [round(s, 1) for s in scores], round(avg, 1), low, hi)
        if low >= 2 or (avg < 40 and low >= 1):
            pad.append(item)
        elif avg >= 70:
            ok.append(item)

    L.append(f"- 跟读事件日（≥3次）：{sum(1 for v in by_day.values() if len(v)>=3)} 天次")
    L.append(f"- 疑似凑次数（≥2次<10分，或均分<40且含极低分）：**{len(pad)}** 天次")
    L.append(f"- 均分≥70：{len(ok)} 天次")
    L.append("")
    L.append("### 凑次数样例（按均分升序，最多20）")
    for sid, day, scores, avg, low, hi in sorted(pad, key=lambda x: x[3])[:20]:
        L.append(
            f"- {names.get(sid,sid)}({sid}) {day}: {scores} 均分{avg} 极低分×{low} 最高{hi}"
        )
    L.append("")

    # how many done_study gendu days with avg <40
    L += ["### 任务状态 vs 跟读分", ""]
    done_gendu = conn.execute(
        """
        SELECT d.student_id, d.task_date, d.state, d.gendu_practice_count, d.gendu_best_score,
               COALESCE(u.module_type, pi.module_type) AS module_type
        FROM daily_tasks d
        LEFT JOIN plan_items pi ON pi.id = d.plan_item_id
        LEFT JOIN task_units u ON u.unit_id = pi.unit_id
        WHERE d.task_date BETWEEN ? AND ?
          AND d.state IN ('done_study','done_pass')
          AND (COALESCE(u.module_type, pi.module_type) LIKE '%gendu%'
               OR COALESCE(u.module_type, pi.module_type) LIKE '%p4%'
               OR d.gendu_practice_count >= 3)
        """,
        (D0, D1),
    ).fetchall()
    L.append(f"- daily 跟读相关 done 行：{len(done_gendu)}")
    low_best = [r for r in done_gendu if (r["gendu_best_score"] or 0) < 40]
    L.append(f"- 其中 best_score<40：{len(low_best)}")
    for r in sorted(low_best, key=lambda x: x["gendu_best_score"] or 0)[:15]:
        L.append(
            f"  - {names.get(r['student_id'],r['student_id'])} {r['task_date']} "
            f"count={r['gendu_practice_count']} best={r['gendu_best_score']} "
            f"mod={r['module_type']}"
        )
    L.append("")

    # ---- synonym speed via activity ----
    L += ["## 3. 同义替换：完成速度（activity）", ""]
    syn_actions = conn.execute(
        """
        SELECT action, COUNT(*) n FROM activity_events
        WHERE created_at >= ? AND created_at < ?
          AND (action LIKE '%synonym%' OR action LIKE '%tongyi%'
               OR module_type LIKE '%synonym%' OR module_type LIKE '%tongyi%'
               OR action LIKE '%replace%')
        GROUP BY 1 ORDER BY n DESC
        """,
        (FROM, TO),
    ).fetchall()
    for r in syn_actions:
        L.append(f"- `{r['action']}`: {r['n']}")
    if not syn_actions:
        L.append("- （无 synonym 字样 action，改查 module_type / summary）")
        for r in conn.execute(
            """
            SELECT action, module_type, COUNT(*) n FROM activity_events
            WHERE created_at >= ? AND created_at < ?
              AND (module_type LIKE '%synonym%' OR module_type LIKE '%reading%'
                   OR summary LIKE '%同义%' OR summary LIKE '%替换%')
            GROUP BY 1,2 ORDER BY n DESC LIMIT 20
            """,
            (FROM, TO),
        ):
            L.append(f"- `{r['action']}` / {r['module_type']}: {r['n']}")
    L.append("")

    # study_sessions for reading_synonym / tongyi
    L += ["### study_sessions 同义相关时长", ""]
    for r in conn.execute(
        """
        SELECT module_type, COUNT(*) n,
               AVG(duration_seconds) avg_s,
               SUM(CASE WHEN duration_seconds < 60 THEN 1 ELSE 0 END) lt60,
               SUM(CASE WHEN duration_seconds < 180 THEN 1 ELSE 0 END) lt180,
               AVG(groups_completed) avg_g,
               AVG(score_percent) avg_score
        FROM study_sessions
        WHERE started_at >= ? AND started_at < ?
          AND (module_type LIKE '%synonym%' OR module_type LIKE '%tongyi%'
               OR module_name LIKE '%同义%' OR module_name LIKE '%替换%')
        GROUP BY 1
        """,
        (FROM, TO),
    ):
        L.append(
            f"- `{r['module_type']}`: n={r['n']} avg={r['avg_s']:.0f}s "
            f"<60s={r['lt60']} <180s={r['lt180']} avg_groups={r['avg_g']} "
            f"avg_score={r['avg_score']}"
        )
    L.append("")

    # burst: sessions with many groups in short time
    L += ["### 同义会话：组数多且时长短", ""]
    fast_syn = conn.execute(
        """
        SELECT student_id, module_type, groups_completed, duration_seconds,
               score_percent, started_at, details
        FROM study_sessions
        WHERE started_at >= ? AND started_at < ?
          AND (module_type LIKE '%synonym%' OR module_type LIKE '%tongyi%'
               OR module_name LIKE '%同义%')
          AND COALESCE(groups_completed,0) >= 5
          AND COALESCE(duration_seconds,0) > 0
          AND duration_seconds / CAST(groups_completed AS REAL) < 15
        ORDER BY duration_seconds / CAST(groups_completed AS REAL)
        LIMIT 25
        """,
        (FROM, TO),
    ).fetchall()
    for r in fast_syn:
        per = r["duration_seconds"] / max(r["groups_completed"], 1)
        L.append(
            f"- {names.get(r['student_id'],r['student_id'])}({r['student_id']}) "
            f"{china_day(parse_iso(r['started_at']))}: "
            f"{r['groups_completed']}组/{r['duration_seconds']}s "
            f"({per:.1f}s/组) score={r['score_percent']} `{r['module_type']}`"
        )
    if not fast_syn:
        L.append("- （无：阈值≥5 且 <15s/组）")
    L.append("")

    # ---- phrase / dictation / listening sessions ----
    L += ["## 4. 词伙 / 听写 / 基础词：短时完成", ""]
    for kw, label in [
        ("%phrase%", "写作词伙"),
        ("%cihuo%", "词伙"),
        ("%dictat%", "听写"),
        ("%listening_basic%", "基础词"),
        ("%basic%", "basic"),
        ("%daanju%", "答案句"),
        ("%synonym_listen%", "听力同义"),
        ("%sentence%", "长难句"),
        ("%complex%", "复杂句"),
        ("%speaking%", "口语"),
    ]:
        rows = conn.execute(
            """
            SELECT student_id, module_type, module_name, duration_seconds,
                   words_tested, groups_completed, score_percent, started_at
            FROM study_sessions
            WHERE started_at >= ? AND started_at < ?
              AND (module_type LIKE ? OR module_name LIKE ?)
              AND COALESCE(duration_seconds,0) BETWEEN 1 AND 120
            ORDER BY duration_seconds
            LIMIT 8
            """,
            (FROM, TO, kw, kw),
        ).fetchall()
        if not rows:
            continue
        L.append(f"### {label}（时长 1–120s 样例）")
        for r in rows:
            L.append(
                f"- {names.get(r['student_id'],r['student_id'])} "
                f"{china_day(parse_iso(r['started_at']))}: "
                f"{r['duration_seconds']}s words={r['words_tested']} "
                f"groups={r['groups_completed']} score={r['score_percent']} "
                f"`{r['module_type']}`/{r['module_name']}"
            )
        L.append("")

    # module duration distribution for done-ish
    L += ["## 5. 各 module_type 会话时长分布（近10天）", ""]
    for r in conn.execute(
        """
        SELECT module_type, COUNT(*) n,
               AVG(duration_seconds) avg_s,
               SUM(CASE WHEN duration_seconds < 60 THEN 1 ELSE 0 END) lt60,
               SUM(CASE WHEN duration_seconds BETWEEN 60 AND 299 THEN 1 ELSE 0 END) m5,
               SUM(CASE WHEN duration_seconds >= 300 THEN 1 ELSE 0 END) ge5,
               SUM(CASE WHEN duration_seconds = 0 OR duration_seconds IS NULL THEN 1 ELSE 0 END) zero
        FROM study_sessions
        WHERE started_at >= ? AND started_at < ?
        GROUP BY 1
        ORDER BY n DESC
        """,
        (FROM, TO),
    ):
        L.append(
            f"- `{r['module_type']}`: n={r['n']} avg={r['avg_s']:.0f}s "
            f"0s={r['zero']} <1′={r['lt60']} 1–5′={r['m5']} ≥5′={r['ge5']}"
        )
    L.append("")

    # ---- activity top actions ----
    L += ["## 6. activity_events 高频 action", ""]
    for r in conn.execute(
        """
        SELECT action, module_type, COUNT(*) n
        FROM activity_events
        WHERE created_at >= ? AND created_at < ?
        GROUP BY 1,2 ORDER BY n DESC LIMIT 40
        """,
        (FROM, TO),
    ):
        L.append(f"- `{r['action']}` / {r['module_type']}: {r['n']}")
    L.append("")

    # translate still for context but brief
    L += ["## 7. 对照：翻译错后速改（仍可见，已做防粘贴）", ""]
    tr = conn.execute(
        """
        SELECT created_at, actor_id, detail_json FROM activity_events
        WHERE action='translate.step_submit'
          AND created_at >= ? AND created_at < ?
        ORDER BY actor_id, created_at
        """,
        (FROM, TO),
    ).fetchall()
    by = defaultdict(list)
    for r in tr:
        by[r["actor_id"]].append(r)
    copy_stats = []
    for sid, evs in by.items():
        last_wrong = {}
        hits = 0
        total = 0
        for r in evs:
            d = jload(r["detail_json"])
            total += 1
            key = (d.get("sentence_id"), d.get("step"))
            dt = parse_iso(r["created_at"])
            if not d.get("correct"):
                last_wrong[key] = dt
            else:
                prev = last_wrong.get(key)
                if prev and 0 <= (dt - prev).total_seconds() <= 20:
                    hits += 1
        if total >= 30 and hits / total >= 0.3:
            copy_stats.append((sid, hits, total, hits / total))
    copy_stats.sort(key=lambda x: -x[3])
    L.append(f"- 仍命中「错后≤20s改对 ≥30%且≥30次」：**{len(copy_stats)}** 人（防粘贴上线前窗口）")
    for sid, hits, total, ratio in copy_stats[:8]:
        L.append(
            f"  - {names.get(sid,sid)}({sid}): {hits}/{total}={ratio:.0%}"
        )
    L.append("")

    # ---- synthesis ----
    L += [
        "## 8. 结论（操作证据 × 产品机制）",
        "",
        "### 证据最硬（建议优先堵）",
        "1. **跟读 P4**：库内 `gendu_practice_events` 明确存在「一天三次、多次接近 0 分仍完成」。完成条件是次数不是分数。",
        "2. **同义替换**：存在「多组 / 极短时长」会话；机制上点参照词确认可整组认领，错了还 Reveal 答案。",
        "3. **听写/基础词 / 词伙**：代码层无质量门槛；短时会话在会话表里可见（需结合模块名核对）。",
        "",
        "### 机制风险大、日志证据偏弱",
        "4. **口语 P2 素材**：自点「已过」即可，无录音门槛。",
        "5. **长难句**：任意翻译可开解析计进度。",
        "6. **口语 P1**：≥1 秒录音即计一题。",
        "7. **通用 API**：`scope-progress` 只认数字，理论上可灌进度（日志未必区分）。",
        "",
        "### 相对难走过场",
        "8. **口语复杂句三步**：跟读/脱口需 ASR 分词全对（仍可听音频跟读）。",
        "",
    ]

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"gendu_pad_days={len(pad)} fast_syn={len(fast_syn)} translate_copy={len(copy_stats)}")


if __name__ == "__main__":
    main()
