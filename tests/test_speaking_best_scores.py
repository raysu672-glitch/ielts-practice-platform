# -*- coding: utf-8 -*-
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from student_api import (  # noqa: E402
    insert_test_record,
    load_speaking_best_scores,
    norm_speaking_question_key,
    upsert_speaking_best_score,
)


class SpeakingBestScoresTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.conn = sqlite3.connect(self.tmp.name)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE students (student_id TEXT PRIMARY KEY);
            INSERT INTO students(student_id) VALUES ('2025001');
            CREATE TABLE test_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                module_type TEXT,
                module_name TEXT,
                test_type TEXT,
                score REAL,
                correct_count INTEGER,
                total_count INTEGER,
                is_passed INTEGER,
                pass_threshold REAL,
                duration_seconds INTEGER,
                details TEXT,
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT
            );
            CREATE TABLE speaking_best_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                question_key TEXT NOT NULL,
                question_text TEXT NOT NULL DEFAULT '',
                part TEXT NOT NULL DEFAULT 'p1',
                best_score REAL NOT NULL,
                updated_at TEXT,
                UNIQUE(student_id, question_key)
            );
            """
        )

    def tearDown(self):
        self.conn.close()
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_norm_key(self):
        self.assertEqual(
            norm_speaking_question_key("Have you ever got a watch as a gift?"),
            "haveyouevergotawatchasagift",
        )

    def test_upsert_keeps_higher(self):
        upsert_speaking_best_score(self.conn, "2025001", "Do you wear a watch?", 5.5)
        upsert_speaking_best_score(self.conn, "2025001", "Do you wear a watch?", 6.0)
        upsert_speaking_best_score(self.conn, "2025001", "Do you wear a watch?", 5.0)
        scores = load_speaking_best_scores(self.conn, "2025001")
        key = norm_speaking_question_key("Do you wear a watch?")
        self.assertEqual(scores[key], 6.0)

    def test_insert_test_record_updates_best(self):
        insert_test_record(
            self.conn,
            "2025001",
            {
                "module_type": "speaking",
                "test_type": "speaking_ai_score",
                "score_percent": 6.5,
                "details": [
                    {
                        "question": "Have you ever got a watch as a gift?",
                        "overall": 6.5,
                    }
                ],
            },
        )
        scores = load_speaking_best_scores(self.conn, "2025001")
        key = norm_speaking_question_key("Have you ever got a watch as a gift?")
        self.assertEqual(scores[key], 6.5)


if __name__ == "__main__":
    unittest.main()
