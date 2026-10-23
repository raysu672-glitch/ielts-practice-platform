"""Find real students: plan age > 30 days and still executing tasks recently."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

DB = Path(sys.argv[1] if len(sys.argv) > 1 else "backups/aliyun_20261022_140428/ielts_local.db")


def main() -> None:
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    print("db:", DB)
    print("has daily_tasks:", "daily_tasks" in tables, "plan_items:", "plan_items" in tables)

    rows = conn.execute(
        """
        WITH plan_span AS (
            SELECT
                student_id,
                MIN(substr(created_at, 1, 10)) AS plan_start,
                COUNT(*) AS plan_n
            FROM plan_items
            WHERE status != 'removed'
            GROUP BY student_id
        ),
        recent_daily AS (
            SELECT
                student_id,
                MAX(task_date) AS last_task_date,
                COUNT(DISTINCT task_date) AS active_days_30,
                SUM(CASE WHEN state IN ('done_study', 'done_pass') THEN 1 ELSE 0 END) AS done_n,
                COUNT(*) AS daily_n
            FROM daily_tasks
            WHERE task_date >= date('now', '-30 day')
            GROUP BY student_id
        ),
        recent_study AS (
            SELECT
                student_id,
                COUNT(*) AS sessions_14,
                COALESCE(SUM(duration_seconds), 0) AS secs_14
            FROM study_sessions
            WHERE created_at >= datetime('now', '-14 day')
            GROUP BY student_id
        )
        SELECT
            s.student_id,
            s.name,
            s.status,
            s.target_score,
            p.plan_start,
            CAST(julianday('now') - julianday(p.plan_start) AS INT) AS plan_days,
            d.last_task_date,
            d.active_days_30,
            d.done_n,
            d.daily_n,
            COALESCE(rs.sessions_14, 0) AS sessions_14,
            CAST(ROUND(COALESCE(rs.secs_14, 0) / 60.0) AS INT) AS mins_14
        FROM students s
        JOIN plan_span p ON p.student_id = s.student_id
        JOIN recent_daily d ON d.student_id = s.student_id
        LEFT JOIN recent_study rs ON rs.student_id = s.student_id
        WHERE s.status = 'active'
          AND s.student_id NOT LIKE '2099%'
          AND s.name NOT LIKE '%测试%'
          AND s.name NOT LIKE '%QA%'
          AND CAST(julianday('now') - julianday(p.plan_start) AS INT) >= 30
          AND d.last_task_date >= date('now', '-7 day')
          AND d.done_n >= 1
        ORDER BY plan_days DESC, d.done_n DESC, mins_14 DESC
        LIMIT 15
        """
    ).fetchall()

    print(
        "student_id\tname\tplan_start\tplan_days\tlast_task\t"
        "days30\tdone30\tsessions14\tmins14"
    )
    for r in rows:
        print(
            f"{r['student_id']}\t{r['name']}\t{r['plan_start']}\t{r['plan_days']}\t"
            f"{r['last_task_date']}\t{r['active_days_30']}\t{r['done_n']}\t"
            f"{r['sessions_14']}\t{r['mins_14']}"
        )
    if not rows:
        print("(no matches — relaxing filters...)")
        rows2 = conn.execute(
            """
            WITH plan_span AS (
                SELECT student_id, MIN(substr(created_at, 1, 10)) AS plan_start
                FROM plan_items WHERE status != 'removed'
                GROUP BY student_id
            ),
            recent_daily AS (
                SELECT student_id, MAX(task_date) AS last_task_date,
                       SUM(CASE WHEN state IN ('done_study','done_pass') THEN 1 ELSE 0 END) AS done_n
                FROM daily_tasks
                WHERE task_date >= date('now', '-14 day')
                GROUP BY student_id
            )
            SELECT s.student_id, s.name, p.plan_start,
                   CAST(julianday('now') - julianday(p.plan_start) AS INT) AS plan_days,
                   d.last_task_date, d.done_n
            FROM students s
            JOIN plan_span p ON p.student_id = s.student_id
            JOIN recent_daily d ON d.student_id = s.student_id
            WHERE s.status='active'
              AND s.student_id NOT LIKE '2099%'
              AND CAST(julianday('now') - julianday(p.plan_start) AS INT) >= 30
            ORDER BY d.last_task_date DESC, plan_days DESC
            LIMIT 20
            """
        ).fetchall()
        for r in rows2:
            print(
                f"{r['student_id']}\t{r['name']}\t{r['plan_start']}\t"
                f"{r['plan_days']}\t{r['last_task_date']}\t{r['done_n']}"
            )
    conn.close()


if __name__ == "__main__":
    main()
