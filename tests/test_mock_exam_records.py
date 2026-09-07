# -*- coding: utf-8 -*-
"""模拟考成绩写入 test_records 后可从进度接口读回。"""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from student_api import insert_test_record, load_progress, load_test_records  # noqa: E402


class MockExamRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.conn = sqlite3.connect(self.tmp.name)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                target_score REAL DEFAULT 6.5
            );
            INSERT INTO students(student_id, target_score) VALUES ('2025001', 6.5);
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
            CREATE TABLE study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                module_type TEXT,
                module_name TEXT,
                session_kind TEXT,
                words_tested INTEGER,
                initial_correct INTEGER,
                initial_wrong INTEGER,
                groups_completed INTEGER,
                score_percent REAL,
                duration_seconds INTEGER,
                details TEXT,
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT
            );
            CREATE TABLE wrong_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                module_type TEXT,
                is_mastered INTEGER DEFAULT 0,
                last_tested TEXT
            );
            """
        )

    def tearDown(self) -> None:
        self.conn.close()
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_mock_set_roundtrip(self) -> None:
        details = [
            {
                "kind": "jianya_mock",
                "source": "mock",
                "subject": "reading",
                "pct": 80,
                "correct": 32,
                "total": 40,
                "durationSeconds": 3600,
                "typeStats": {"判断题（T/F/NG）": {"correct": 8, "total": 10, "wrong": 2, "blank": 0}},
                "parts": [
                    {
                        "bookId": 12,
                        "subject": "reading",
                        "sId": 101,
                        "sPart": 1,
                        "label": "C12 Test 1 Part 1",
                        "correct": 11,
                        "total": 13,
                        "pct": 85,
                        "durationSeconds": 1200,
                        "answers": {"1": "TRUE"},
                        "items": [{"number": 1, "status": "correct"}],
                    }
                ],
            }
        ]
        saved = insert_test_record(
            self.conn,
            "2025001",
            {
                "module_type": "mock_reading",
                "module_name": "阅读模拟考",
                "test_type": "mock_exam",
                "score": 80,
                "correct_count": 32,
                "total_count": 40,
                "duration_seconds": 3600,
                "details": details,
            },
        )
        self.assertTrue(saved["id"])
        rows = load_test_records(self.conn, "2025001")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["test_type"], "mock_exam")
        self.assertEqual(rows[0]["module_type"], "mock_reading")
        self.assertEqual(rows[0]["details"][0]["kind"], "jianya_mock")
        self.assertEqual(rows[0]["details"][0]["parts"][0]["sId"], 101)
        progress = load_progress(self.conn, "2025001")
        self.assertEqual(progress["test_records"][0]["correct_count"], 32)
        self.assertEqual(json.loads(json.dumps(progress["test_records"][0]["details"]))[0]["subject"], "reading")

    def test_reading_part_stores_correct_count(self) -> None:
        saved = insert_test_record(
            self.conn,
            "2025001",
            {
                "module_type": "reading_p1",
                "module_name": "阅读Part1模拟考",
                "test_type": "mock_exam",
                "score": 25,
                "correct_count": 8,
                "total_count": 13,
                "details": [
                    {
                        "kind": "jianya_paper",
                        "source": "mock",
                        "bookId": 12,
                        "subject": "reading",
                        "sId": 101,
                        "sPart": 1,
                        "correct": 8,
                        "total": 13,
                    }
                ],
            },
        )
        self.assertEqual(saved["score"], 8)
        self.assertEqual(saved["correct_count"], 8)
        self.assertEqual(saved["total_count"], 13)
        self.assertEqual(saved["pass_threshold"], 11)
        self.assertFalse(saved["is_passed"])
        passed = insert_test_record(
            self.conn,
            "2025001",
            {
                "module_type": "reading_p1",
                "module_name": "阅读Part1模拟考",
                "test_type": "mock_exam",
                "correct_count": 11,
                "total_count": 13,
            },
        )
        self.assertEqual(passed["score"], 11)
        self.assertTrue(passed["is_passed"])


if __name__ == "__main__":
    unittest.main()
