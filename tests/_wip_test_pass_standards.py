import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from teacher_api import (  # noqa: E402
    list_standards,
    seed_pass_standards,
    update_standard,
)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE pass_standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_type TEXT UNIQUE NOT NULL,
            module_name TEXT NOT NULL,
            score_6 REAL DEFAULT 70,
            score_6_5 REAL DEFAULT 80,
            score_7 REAL DEFAULT 95,
            is_active INTEGER DEFAULT 1,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )
    return conn


class PassStandardTests(unittest.TestCase):
    def test_seed_adds_reading_and_listening_parts_as_counts(self) -> None:
        conn = _connect()
        seed_pass_standards(conn)
        rows = {item["module_type"]: item for item in list_standards(conn)}
        self.assertEqual(rows["reading_p1"]["module_name"], "阅读Part1")
        self.assertEqual(rows["reading_p1"]["score_6"], 9)
        self.assertEqual(rows["reading_p1"]["score_6_5"], 11)
        self.assertEqual(rows["reading_p1"]["score_7"], 12)
        self.assertEqual(rows["listening_p4"]["score_6"], 4)
        self.assertEqual(rows["listening_p4"]["score_7"], 7)

    def test_percent_leftovers_are_reset_to_counts(self) -> None:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO pass_standards (module_type, module_name, score_6, score_6_5, score_7)
            VALUES ('reading_p1', '第一篇阅读', 70, 80, 90)
            """
        )
        conn.commit()
        seed_pass_standards(conn)
        row = conn.execute(
            "SELECT module_name, score_6, score_6_5, score_7 FROM pass_standards WHERE module_type = 'reading_p1'"
        ).fetchone()
        self.assertEqual(row["module_name"], "阅读Part1")
        self.assertEqual(row["score_6"], 9)
        self.assertEqual(row["score_6_5"], 11)
        self.assertEqual(row["score_7"], 12)

    def test_teacher_edits_on_count_modules_are_kept(self) -> None:
        conn = _connect()
        seed_pass_standards(conn)
        err = update_standard(conn, "listening_p1", {"score_6": 7, "score_6_5": 8, "score_7": 9})
        self.assertIsNone(err)
        seed_pass_standards(conn)
        row = conn.execute(
            "SELECT score_6 FROM pass_standards WHERE module_type = 'listening_p1'"
        ).fetchone()
        self.assertEqual(row["score_6"], 7)


if __name__ == "__main__":
    unittest.main()
