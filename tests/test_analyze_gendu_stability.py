import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from analyze_gendu_stability import (  # noqa: E402
    adjacent_swings,
    build_report,
    load_events,
    summarize_scores,
)


class GenduStabilityTests(unittest.TestCase):
    def test_summarize_counts_low_and_pass(self) -> None:
        stats = summarize_scores([0, 20, 50, 80, 90])
        self.assertEqual(stats["n"], 5)
        self.assertEqual(stats["lt30"], 2)
        self.assertEqual(stats["ge70"], 2)
        self.assertEqual(stats["zero"], 1)
        self.assertEqual(stats["median"], 50)

    def test_adjacent_swings(self) -> None:
        self.assertEqual(adjacent_swings([80, 30, 75, 70]), 2)
        self.assertEqual(adjacent_swings([60, 70, 65]), 0)

    def test_report_flags_only_wide_recent_swings(self) -> None:
        events = [
            {"task_date": "2026-10-24", "score": s, "student_id": "A", "unit_id": "C4T1S4",
             "created_at": f"2026-10-24T0{i}:00:00Z", "name": "甲"}
            for i, s in enumerate([20, 85, 30, 90])
        ]
        events += [
            {"task_date": "2026-10-24", "score": s, "student_id": "B", "unit_id": "C4T1S4",
             "created_at": f"2026-10-24T1{i}:00:00Z", "name": "乙"}
            for i, s in enumerate([70, 72, 74, 76])
        ]
        report = build_report(events, [], {"available": False, "rows": 0, "by_action": {}})
        ids = [row["student_id"] for row in report["unstable"]]
        self.assertEqual(ids, ["A"])
        self.assertEqual(report["after"]["n"], 8)

    def test_script_reads_sqlite(self) -> None:
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE students (student_id TEXT, name TEXT)")
        conn.execute("CREATE TABLE gendu_practice_events (task_date TEXT, score REAL, student_id TEXT, unit_id TEXT, created_at TEXT)")
        conn.execute("INSERT INTO students VALUES ('2025001', '测试')")
        conn.execute(
            "INSERT INTO gendu_practice_events VALUES ('2026-11-01', 40, '2025001', 'C4T1S4', '2026-11-01T01:00:00Z')"
        )
        conn.commit()
        rows = load_events(conn, "2026-10-08")
        self.assertEqual(rows[0]["name"], "测试")
        self.assertEqual(rows[0]["score"], 40)
