#!/usr/bin/env python3
"""Summarize recent shadow-reading scores. Read-only.

  python scripts/analyze_gendu_stability.py --db data/ielts_local.db
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

CHINA = timezone(timedelta(hours=8))
# 上传上限和 64kbps 录音在北京时间 2026-10-22 20:56 左右上线。
DEPLOY_DATE = "2026-10-23"


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def _num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _quantile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    idx = int(round((len(sorted_values) - 1) * p))
    idx = max(0, min(len(sorted_values) - 1, idx))
    return sorted_values[idx]


def summarize_scores(scores: list[float]) -> dict:
    if not scores:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "p10": None,
            "p90": None,
            "std": None,
            "lt30": 0,
            "ge70": 0,
            "zero": 0,
        }
    ordered = sorted(scores)
    mean = sum(ordered) / len(ordered)
    std = statistics.pstdev(ordered) if len(ordered) > 1 else 0.0
    return {
        "n": len(ordered),
        "mean": round(mean, 1),
        "median": round(_quantile(ordered, 0.5), 1),
        "p10": round(_quantile(ordered, 0.1), 1),
        "p90": round(_quantile(ordered, 0.9), 1),
        "std": round(std, 1),
        "lt30": sum(1 for x in ordered if x < 30),
        "ge70": sum(1 for x in ordered if x >= 70),
        "zero": sum(1 for x in ordered if x <= 0),
    }


def adjacent_swings(scores_in_order: list[float], gap: float = 40) -> int:
    swings = 0
    for prev, cur in zip(scores_in_order, scores_in_order[1:]):
        if abs(cur - prev) >= gap:
            swings += 1
    return swings


def parse_details(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    if not raw or not isinstance(raw, str):
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _pct(part: int, whole: int) -> float:
    if not whole:
        return 0.0
    return round(100.0 * part / whole, 1)


def load_events(conn: sqlite3.Connection, since: str) -> list[dict]:
    if not _table_exists(conn, "gendu_practice_events"):
        return []
    rows = conn.execute(
        """
        SELECT e.task_date, e.score, e.student_id, e.unit_id, e.created_at,
               COALESCE(s.name, '') AS name
        FROM gendu_practice_events e
        LEFT JOIN students s ON s.student_id = e.student_id
        WHERE e.task_date >= ?
        ORDER BY e.created_at
        """,
        (since,),
    ).fetchall()
    return [
        {
            "task_date": row[0] or "",
            "score": _num(row[1]),
            "student_id": row[2] or "",
            "unit_id": row[3] or "",
            "created_at": row[4] or "",
            "name": row[5] or "",
        }
        for row in rows
    ]


def load_records(conn: sqlite3.Connection, since: str) -> list[dict]:
    if not _table_exists(conn, "test_records"):
        return []
    rows = conn.execute(
        """
        SELECT student_id, score, correct_count, total_count, details, created_at
        FROM test_records
        WHERE module_type = 'listening_p4_speed' AND created_at >= ?
        ORDER BY created_at
        """,
        (since,),
    ).fetchall()
    out = []
    for row in rows:
        detail = parse_details(row[4])
        text = str(detail.get("recognizedText") or detail.get("recognized_text") or "")
        out.append(
            {
                "student_id": row[0] or "",
                "score": _num(row[1]),
                "matched": int(row[2] or 0),
                "total": int(row[3] or 0),
                "created_at": row[5] or "",
                "text_len": len(text.strip()),
                "word_count": len(text.split()),
                "empty_text": not text.strip(),
                "lesson": str(detail.get("lessonId") or detail.get("lessonTitle") or ""),
            }
        )
    return out


def load_error_counts(conn: sqlite3.Connection) -> dict:
    if not _table_exists(conn, "student_debug_events"):
        return {"available": False, "rows": 0, "by_action": {}}
    rows = conn.execute(
        """
        SELECT action, COUNT(*)
        FROM student_debug_events
        WHERE page LIKE '%gendu%'
           OR page LIKE '%P4gendu%'
           OR detail_json LIKE '%413%'
           OR detail_json LIKE '%识别失败%'
           OR detail_json LIKE '%Request Entity Too Large%'
        GROUP BY action
        ORDER BY COUNT(*) DESC
        LIMIT 20
        """
    ).fetchall()
    return {
        "available": True,
        "rows": sum(r[1] for r in rows),
        "by_action": {r[0]: r[1] for r in rows},
    }


def build_report(events: list[dict], records: list[dict], errors: dict) -> dict:
    before = [e for e in events if e["task_date"] < DEPLOY_DATE]
    after = [e for e in events if e["task_date"] >= DEPLOY_DATE]
    by_day: dict[str, list[float]] = defaultdict(list)
    by_student: dict[str, list[dict]] = defaultdict(list)
    by_unit_after: dict[str, list[float]] = defaultdict(list)
    for event in events:
        by_day[event["task_date"]].append(event["score"])
        by_student[event["student_id"]].append(event)
        if event["task_date"] >= DEPLOY_DATE:
            by_unit_after[event["unit_id"]].append(event["score"])

    unstable = []
    for student_id, attempts in by_student.items():
        recent = [a for a in attempts if a["task_date"] >= DEPLOY_DATE]
        if len(recent) < 4:
            continue
        scores = [a["score"] for a in recent]
        stats = summarize_scores(scores)
        span = max(scores) - min(scores)
        swings = adjacent_swings(scores)
        if span < 35 and stats["std"] < 18 and swings < 2:
            continue
        unstable.append(
            {
                "student_id": student_id,
                "name": recent[0]["name"],
                "n": len(recent),
                "min": round(min(scores), 1),
                "max": round(max(scores), 1),
                "span": round(span, 1),
                "std": stats["std"],
                "mean": stats["mean"],
                "swings40": swings,
                "lt30": stats["lt30"],
                "units": sorted({a["unit_id"] for a in recent}),
                "scores": [round(s, 1) for s in scores[-8:]],
            }
        )
    unstable.sort(key=lambda item: (-item["span"], -item["swings40"], item["student_id"]))

    unit_rows = []
    for unit_id, scores in by_unit_after.items():
        if len(scores) < 8:
            continue
        stats = summarize_scores(scores)
        unit_rows.append({"unit_id": unit_id, **stats, "lt30_pct": _pct(stats["lt30"], stats["n"])})
    unit_rows.sort(key=lambda item: item["mean"] if item["mean"] is not None else 999)

    rec_before = [r for r in records if r["created_at"][:10] < DEPLOY_DATE]
    rec_after = [r for r in records if r["created_at"][:10] >= DEPLOY_DATE]

    def text_stats(rows: list[dict]) -> dict:
        if not rows:
            return {"n": 0}
        empty = sum(1 for r in rows if r["empty_text"])
        short = sum(1 for r in rows if r["word_count"] < 8)
        low_and_short = sum(1 for r in rows if r["score"] < 40 and r["word_count"] < 15)
        high = [r for r in rows if r["score"] >= 70]
        low = [r for r in rows if r["score"] < 40]
        return {
            "n": len(rows),
            "empty_text": empty,
            "empty_pct": _pct(empty, len(rows)),
            "short_text": short,
            "low_and_short": low_and_short,
            "low_mean_words": round(sum(r["word_count"] for r in low) / len(low), 1) if low else None,
            "high_mean_words": round(sum(r["word_count"] for r in high) / len(high), 1) if high else None,
            "mean_score": round(sum(r["score"] for r in rows) / len(rows), 1),
        }

    day_rows = []
    for day in sorted(by_day):
        stats = summarize_scores(by_day[day])
        day_rows.append(
            {
                "date": day,
                "n": stats["n"],
                "mean": stats["mean"],
                "std": stats["std"],
                "lt30_pct": _pct(stats["lt30"], stats["n"]),
                "ge70_pct": _pct(stats["ge70"], stats["n"]),
            }
        )
    return {
        "deploy_date": DEPLOY_DATE,
        "events": len(events),
        "before": summarize_scores([e["score"] for e in before]),
        "after": summarize_scores([e["score"] for e in after]),
        "days": day_rows,
        "unstable": unstable[:20],
        "unstable_students": len(unstable),
        "students_after": len({e["student_id"] for e in after}),
        "hard_units": unit_rows[:8],
        "easy_units": list(reversed(unit_rows[-5:])) if unit_rows else [],
        "text_before": text_stats(rec_before),
        "text_after": text_stats(rec_after),
        "errors": errors,
    }


def format_block(title: str, stats: dict) -> str:
    if not stats or not stats.get("n"):
        return f"{title}：没有记录"
    return (
        f"{title}：{stats['n']} 次，平均 {stats['mean']}，中位 {stats['median']}，"
        f"标准差 {stats['std']}，低于 30 分 {stats['lt30']} 次（{_pct(stats['lt30'], stats['n'])}%），"
        f"达到 70 分 {stats['ge70']} 次（{_pct(stats['ge70'], stats['n'])}%），0 分 {stats['zero']} 次"
    )


def render(report: dict) -> str:
    lines = [
        format_block(f"{DEPLOY_DATE} 之前", report["before"]),
        format_block(f"{DEPLOY_DATE} 之后", report["after"]),
        f"上线后有跟读记录的学生 {report['students_after']} 人，其中波动明显的 {report['unstable_students']} 人",
        "",
        "按日：",
    ]
    for day in report["days"]:
        lines.append(
            f"  {day['date']}  n={day['n']}  均分={day['mean']}  标准差={day['std']}  "
            f"<30%={day['lt30_pct']}  ≥70%={day['ge70_pct']}"
        )
    lines.append("")
    lines.append("上线后波动最大的学生（至少 4 次，极差≥35 或相邻两次差≥40）：")
    if not report["unstable"]:
        lines.append("  无")
    for row in report["unstable"]:
        lines.append(
            f"  {row['student_id']} {row['name']}  n={row['n']}  {row['min']}–{row['max']}  "
            f"极差={row['span']}  标准差={row['std']}  相邻大跳={row['swings40']}  "
            f"<30={row['lt30']}  课文={','.join(row['units'])}  最近={row['scores']}"
        )
    lines.append("")
    lines.append("上线后样本不少于 8 次、均分最低的课文：")
    for row in report["hard_units"]:
        lines.append(
            f"  {row['unit_id']}  n={row['n']}  均分={row['mean']}  标准差={row['std']}  <30%={row['lt30_pct']}"
        )
    lines.append("")
    lines.append(f"识别文本（测试记录）上线前：{json.dumps(report['text_before'], ensure_ascii=False)}")
    lines.append(f"识别文本（测试记录）上线后：{json.dumps(report['text_after'], ensure_ascii=False)}")
    lines.append(f"调试日志：{json.dumps(report['errors'], ensure_ascii=False)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--since", default="2026-10-08")
    args = parser.parse_args()
    conn = sqlite3.connect(f"file:{Path(args.db)}?mode=ro", uri=True)
    try:
        report = build_report(
            load_events(conn, args.since),
            load_records(conn, args.since),
            load_error_counts(conn),
        )
    finally:
        conn.close()
    print(render(report))
    print("\n---JSON---")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
