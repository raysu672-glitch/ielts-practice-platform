"""List students with enough activity for a meaningful checkup."""
from __future__ import annotations

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data" / "ielts_local.db"


def main() -> None:
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT
            s.student_id,
            s.name,
            s.status,
            s.target_score,
            (SELECT COUNT(*) FROM study_sessions ss WHERE ss.student_id = s.student_id) AS sessions,
            (SELECT COUNT(*) FROM test_records tr WHERE tr.student_id = s.student_id) AS tests,
            (SELECT COALESCE(SUM(duration_seconds), 0)
             FROM study_sessions ss WHERE ss.student_id = s.student_id) AS secs,
            (SELECT COUNT(*) FROM activity_events ae
             WHERE ae.target_student_id = s.student_id
                OR (ae.actor_role = 'student' AND ae.actor_id = s.student_id)) AS events
        FROM students s
        WHERE s.student_id NOT LIKE '2099%'
          AND s.name NOT LIKE '%测试%'
          AND s.name NOT LIKE '%测%'
        ORDER BY events DESC, sessions DESC, tests DESC
        LIMIT 20
        """
    ).fetchall()
    print("student_id\tname\tstatus\ttarget\tsessions\ttests\tmins\tevents")
    for r in rows:
        mins = int(round((r["secs"] or 0) / 60.0))
        print(
            f"{r['student_id']}\t{r['name']}\t{r['status']}\t{r['target_score']}\t"
            f"{r['sessions']}\t{r['tests']}\t{mins}\t{r['events']}"
        )
    conn.close()


if __name__ == "__main__":
    main()
