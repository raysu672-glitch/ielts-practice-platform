import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "repair_tracking_data.py"
SPEC = importlib.util.spec_from_file_location("repair_tracking_data", SCRIPT_PATH)
repair = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(repair)


class RepairTrackingDataTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE study_sessions (
                id INTEGER PRIMARY KEY,
                student_id TEXT,
                module_type TEXT,
                session_kind TEXT,
                duration_seconds INTEGER,
                words_tested INTEGER,
                initial_correct INTEGER,
                initial_wrong INTEGER,
                groups_completed INTEGER,
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT
            );
            CREATE TABLE test_records (
                id INTEGER PRIMARY KEY,
                student_id TEXT,
                module_type TEXT,
                test_type TEXT,
                score REAL,
                correct_count INTEGER,
                total_count INTEGER,
                duration_seconds INTEGER,
                details TEXT,
                started_at TEXT,
                created_at TEXT
            );
            """
        )

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_plan_removes_test_sessions_and_keeps_child_study_report(self):
        self.conn.executemany(
            "INSERT INTO study_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (1, "s1", "reading_synonym", "test", 60, 40, 4, 36, 0, "2026-07-10T00:00:00Z", "2026-07-10T00:01:00Z", "2026-07-10T00:01:00Z"),
                (2, "s1", "dictation", "study", 33, 0, 0, 0, 0, "2026-07-10T00:02:00Z", "2026-07-10T00:02:33Z", "2026-07-10T00:02:33Z"),
                (3, "s1", "dictation", "study", 20, 20, 0, 0, 0, None, "2026-07-10T00:02:33Z", "2026-07-10T00:02:33Z"),
            ],
        )
        plan = repair.build_repair_plan(self.conn)
        self.assertEqual(plan["test_session_ids"], [1])
        self.assertEqual(plan["duplicate_study_ids"], [2])

    def test_plan_removes_legacy_exit_cluster_but_keeps_completed_attempt(self):
        self.conn.executemany(
            "INSERT INTO test_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (10, "s1", "reading_synonym", "module_test", 0, 0, 40, 3, "[]", "2026-07-10T00:00:00Z", "2026-07-10T00:00:03Z"),
                (11, "s1", "reading_synonym", "module_test", 0, 0, 40, 4, "[]", None, "2026-07-10T00:00:04Z"),
                (12, "s1", "reading_synonym", "module_test", 0, 0, 40, 4, "[]", None, "2026-07-10T00:00:04Z"),
                (13, "s1", "reading_synonym", "module_test", 11, 4, 38, 28, "[]", "2026-07-10T00:05:00Z", "2026-07-10T00:05:28Z"),
            ],
        )
        plan = repair.build_repair_plan(self.conn)
        self.assertEqual(plan["legacy_incomplete_test_ids"], [10, 11, 12])

    def test_apply_repair_is_idempotent(self):
        self.conn.execute(
            "INSERT INTO study_sessions VALUES (1, 's1', 'reading_synonym', 'test', 10, 1, 0, 1, 0, NULL, NULL, '2026-07-10T00:00:00Z')"
        )
        first_plan = repair.build_repair_plan(self.conn)
        repair.apply_repair(self.conn, first_plan)
        second_plan = repair.build_repair_plan(self.conn)
        self.assertEqual(second_plan, {
            "test_session_ids": [],
            "duplicate_study_ids": [],
            "legacy_incomplete_test_ids": [],
        })


if __name__ == "__main__":
    unittest.main()
