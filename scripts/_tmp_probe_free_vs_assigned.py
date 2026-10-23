#!/usr/bin/env python3
"""Split study time: teacher-assigned (plan_item) vs free practice."""
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
    "placement": "入学摸底",
}


def label(m: str | None) -> str:
    m = (m or "").strip() or "(empty)"
    base = m.replace("_learn", "").replace("_test", "")
    return NAMES.get(base, NAMES.get(m, m))


def dump_group(conn: sqlite3.Connection, where: str, title: str) -> None:
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
    total = sum((r["hours"] or 0) for r in rows) or 1.0
    print(f"{'模块':<24} {'学生':>5} {'次数':>6} {'时长h':>8} {'占比':>7}")
    for r in rows:
        pct = 100 * (r["hours"] or 0) / total
        print(
            f"{label(r['module_type']):<24} {r['students']:5} {r['sessions']:6} "
            f"{r['hours']:8.1f} {pct:6.1f}%"
        )
    print(f"合计时长 h = {total:.1f}" if rows else "（无数据）")


def main() -> None:
    db = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else r"D:\ielts-practice-platform\backups\aliyun_20261015_103936\ielts_local.db"
    )
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    print(f"DB: {db.name}")

    print("\n---- session_kind 分布 ----")
    for r in conn.execute(
        """
        SELECT COALESCE(session_kind,'(null)') AS k,
               COUNT(*) AS n,
               ROUND(SUM(COALESCE(duration_seconds,0))/3600.0,1) AS h
        FROM study_sessions
        GROUP BY 1 ORDER BY h DESC
        """
    ):
        print(f"  {r['k']:<20} sessions={r['n']:5} hours={r['h']}")

    assigned = (
        "plan_item_id IS NOT NULL AND TRIM(CAST(plan_item_id AS TEXT)) != ''"
    )
    free = (
        "plan_item_id IS NULL OR TRIM(CAST(plan_item_id AS TEXT)) = ''"
    )

    n_a, h_a = conn.execute(
        f"SELECT COUNT(*), ROUND(SUM(COALESCE(duration_seconds,0))/3600.0,1) "
        f"FROM study_sessions WHERE {assigned}"
    ).fetchone()
    n_f, h_f = conn.execute(
        f"SELECT COUNT(*), ROUND(SUM(COALESCE(duration_seconds,0))/3600.0,1) "
        f"FROM study_sessions WHERE {free}"
    ).fetchone()
    print(f"\n有 plan_item_id（任务关联）: sessions={n_a} hours={h_a}")
    print(f"无 plan_item_id（偏自由练）: sessions={n_f} hours={h_f}")

    dump_group(conn, assigned, "任务关联学习（有 plan_item_id）全量")
    dump_group(conn, free, "非任务学习（无 plan_item_id）全量")
    dump_group(
        conn,
        f"({assigned}) AND datetime(started_at) >= datetime('now','-30 days')",
        "任务关联 · 近30天",
    )
    dump_group(
        conn,
        f"({free}) AND datetime(started_at) >= datetime('now','-30 days')",
        "非任务 · 近30天",
    )

    # Teacher assignment volume from plan_items / daily_tasks if present
    tables = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    for t in sorted(tables):
        if "plan" in t or "task" in t or "daily" in t:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({t})")]
            print(f"\n表 {t} cols: {cols}")

    # Prefer plan_items module distribution
    if "plan_items" in tables:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(plan_items)")]
        mod_col = None
        for c in ("module_type", "module", "module_id"):
            if c in cols:
                mod_col = c
                break
        if mod_col:
            print(f"\n==== 教师计划项 plan_items 按 {mod_col} ====")
            status_filter = ""
            if "status" in cols:
                # show all, but also print status breakdown
                for r in conn.execute(
                    "SELECT status, COUNT(*) n FROM plan_items GROUP BY 1"
                ):
                    print(f"  status={r['status']}: {r['n']}")
            q = f"""
                SELECT {mod_col} AS module_type, COUNT(*) AS n,
                       COUNT(DISTINCT student_id) AS students
                FROM plan_items
                GROUP BY 1 ORDER BY n DESC
            """
            try:
                rows = conn.execute(q).fetchall()
            except sqlite3.Error:
                # maybe no student_id
                q = f"""
                    SELECT {mod_col} AS module_type, COUNT(*) AS n
                    FROM plan_items GROUP BY 1 ORDER BY n DESC
                """
                rows = conn.execute(q).fetchall()
            for r in rows:
                stu = r["students"] if "students" in r.keys() else "-"
                print(
                    f"  {label(r['module_type']):<24} items={r['n']:5} "
                    f"students={stu}"
                )

    if "daily_tasks" in tables:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(daily_tasks)")]
        mod_col = next(
            (c for c in ("module_type", "module", "module_id") if c in cols),
            None,
        )
        if mod_col:
            print(f"\n==== daily_tasks 按 {mod_col} ====")
            try:
                rows = conn.execute(
                    f"""
                    SELECT {mod_col} AS module_type, COUNT(*) AS n,
                           COUNT(DISTINCT student_id) AS students
                    FROM daily_tasks GROUP BY 1 ORDER BY n DESC
                    """
                ).fetchall()
            except sqlite3.Error:
                rows = conn.execute(
                    f"""
                    SELECT {mod_col} AS module_type, COUNT(*) AS n
                    FROM daily_tasks GROUP BY 1 ORDER BY n DESC
                    """
                ).fetchall()
            for r in rows:
                stu = r["students"] if "students" in r.keys() else "-"
                print(
                    f"  {label(r['module_type']):<24} tasks={r['n']:5} "
                    f"students={stu}"
                )

    # Free-study personal favorite
    print("\n==== 非任务学习：每人时长最高模块 ====")
    fav = conn.execute(
        f"""
        WITH per AS (
          SELECT student_id, module_type,
                 SUM(COALESCE(duration_seconds,0)) AS secs
          FROM study_sessions
          WHERE {free}
          GROUP BY student_id, module_type
        ), ranked AS (
          SELECT *, ROW_NUMBER() OVER (
            PARTITION BY student_id ORDER BY secs DESC
          ) AS rn
          FROM per WHERE secs > 0
        )
        SELECT module_type, COUNT(*) AS n
        FROM ranked WHERE rn=1
        GROUP BY module_type ORDER BY n DESC
        """
    ).fetchall()
    for r in fav:
        print(f"  {label(r['module_type']):<24} {r['n']:4} 人")

    conn.close()


if __name__ == "__main__":
    main()
