#!/usr/bin/env python3
"""Analyze which modules students study most (from a prod DB backup)."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

NAMES = {
    "dictation": "听力1000词",
    "listening_basic": "听力基础词汇",
    "reading_synonym": "阅读同义替换",
    "writing_phrase": "写作词伙",
    "sentence": "长难句分析",
    "listening_synonym": "听力同义替换/答案句",
    "writing_translate": "写作句子翻译",
    "writing_correction": "作文批改",
    "listening_p4_speed": "听力跟读",
    "speaking": "口语练习",
    "vocab": "单词FSRS",
    "writing_words": "小初单词",
    "highschool_words": "高中单词",
    "ielts_core": "雅思核心800词",
    "grammar": "基础语法",
    "placement": "入学摸底",
    "reading_p1": "阅读P1",
    "reading_p2": "阅读P2",
    "reading_p3": "阅读P3",
    "listening_p1": "听力P1",
    "listening_p2": "听力P2",
    "listening_p3": "听力P3",
    "listening_p4": "听力P4",
}


def label(m: str | None) -> str:
    m = (m or "").strip() or "(empty)"
    base = m.replace("_learn", "").replace("_test", "")
    return NAMES.get(base, NAMES.get(m, m))


def report(conn: sqlite3.Connection, where: str, title: str) -> None:
    print(f"\n==== {title} ====")
    rows = conn.execute(
        f"""
        SELECT module_type,
               COUNT(*) AS sessions,
               COUNT(DISTINCT student_id) AS students,
               ROUND(SUM(COALESCE(duration_seconds,0))/3600.0, 1) AS hours,
               ROUND(AVG(COALESCE(duration_seconds,0))/60.0, 1) AS avg_min
        FROM study_sessions
        WHERE {where}
        GROUP BY module_type
        ORDER BY hours DESC, sessions DESC
        """
    ).fetchall()
    total_h = sum((r["hours"] or 0) for r in rows) or 1.0
    print(f"{'模块':<24} {'学生':>5} {'次数':>6} {'时长h':>8} {'占比':>7} {'均分m':>6}")
    for r in rows:
        name = label(r["module_type"])
        pct = 100 * (r["hours"] or 0) / total_h
        print(
            f"{name:<24} {r['students']:5} {r['sessions']:6} "
            f"{r['hours']:8.1f} {pct:6.1f}% {r['avg_min']:6.1f}"
        )


def main() -> None:
    db = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else r"D:\ielts-practice-platform\backups\aliyun_20261015_104613\ielts_local.db"
    )
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    print(f"DB: {db}")
    print(f"size_mb: {db.stat().st_size / 1024 / 1024:.1f}")
    n = conn.execute("SELECT COUNT(*) FROM study_sessions").fetchone()[0]
    dr = conn.execute(
        "SELECT MIN(started_at), MAX(started_at) FROM study_sessions"
    ).fetchone()
    print(f"study_sessions: {n}")
    print(f"date_range: {dr[0]} -> {dr[1]}")

    report(conn, "1=1", "学习会话 全量（按时长）")
    report(
        conn,
        "datetime(started_at) >= datetime('now', '-30 days')",
        "学习会话 近30天",
    )
    report(
        conn,
        "datetime(started_at) >= datetime('now', '-7 days')",
        "学习会话 近7天",
    )

    print("\n==== 学生个人最爱板块（每人时长最高的模块，全量）====")
    fav = conn.execute(
        """
        WITH per AS (
          SELECT student_id, module_type,
                 SUM(COALESCE(duration_seconds,0)) AS secs
          FROM study_sessions
          GROUP BY student_id, module_type
        ), ranked AS (
          SELECT *, ROW_NUMBER() OVER (
            PARTITION BY student_id ORDER BY secs DESC
          ) AS rn
          FROM per
          WHERE secs > 0
        )
        SELECT module_type, COUNT(*) AS n
        FROM ranked WHERE rn = 1
        GROUP BY module_type
        ORDER BY n DESC
        """
    ).fetchall()
    for r in fav:
        print(f"{label(r['module_type']):<24} {r['n']:4} 人把它学得最多")

    print("\n==== 测试提交次数（全量）====")
    for r in conn.execute(
        """
        SELECT module_type, COUNT(*) AS tests,
               COUNT(DISTINCT student_id) AS students
        FROM test_records
        GROUP BY 1
        ORDER BY tests DESC
        """
    ):
        print(
            f"{label(r['module_type']):<24} students={r['students']:4} "
            f"tests={r['tests']:5}"
        )

    conn.close()


if __name__ == "__main__":
    main()
