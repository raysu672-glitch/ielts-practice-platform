# -*- coding: utf-8 -*-
"""Teacher student-detail payload includes mock exams and wrong-book counts."""

from __future__ import annotations

import json
import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from teacher_api import load_student_detail  # noqa: E402


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            is_password_changed INTEGER DEFAULT 0,
            target_score REAL DEFAULT 6.5,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            updated_at TEXT
        );
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
            word TEXT,
            is_mastered INTEGER DEFAULT 0,
            last_tested TEXT
        );
        CREATE TABLE wrong_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT,
            item_key TEXT,
            is_mastered INTEGER DEFAULT 0,
            last_tested TEXT
        );
        """
    )
    return conn


class StudentDetailTests(unittest.TestCase):
    def test_load_student_detail_includes_mock_and_wrong_counts(self) -> None:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO students (
                student_id, name, password, target_score, status
            ) VALUES ('2025001', '测试生', 'x', 6.5, 'active')
            """
        )
        details = json.dumps(
            [
                {
                    "kind": "jianya_mock",
                    "subject": "reading",
                    "parts": [{"label": "C12 Test 1", "sId": 101}],
                }
            ],
            ensure_ascii=False,
        )
        conn.execute(
            """
            INSERT INTO test_records (
                student_id, module_type, module_name, test_type,
                score, correct_count, total_count, is_passed,
                duration_seconds, details, created_at
            ) VALUES (
                '2025001', 'mock_reading', '阅读模拟考', 'mock_exam',
                80, 32, 40, 1, 3600, ?, '2026-09-04T01:00:00.000Z'
            )
            """,
            (details,),
        )
        conn.execute(
            """
            INSERT INTO test_records (
                student_id, module_type, module_name, test_type,
                score, correct_count, total_count, is_passed,
                duration_seconds, details, created_at
            ) VALUES (
                '2025001', 'dictation', '听写测试', 'formal',
                90, 18, 20, 1, 600, '[]', '2026-09-03T01:00:00.000Z'
            )
            """
        )
        conn.execute(
            """
            INSERT INTO wrong_words (student_id, module_type, word, is_mastered)
            VALUES ('2025001', 'dictation', 'apple', 0)
            """
        )
        conn.execute(
            """
            INSERT INTO wrong_items (student_id, module_type, item_key, is_mastered)
            VALUES ('2025001', 'sentence', 's1', 0)
            """
        )
        conn.commit()

        payload, err = load_student_detail(conn, "2025001")
        self.assertIsNone(err)
        assert payload is not None
        self.assertEqual(payload["student"]["name"], "测试生")
        self.assertEqual(len(payload["test_records"]), 2)
        self.assertEqual(len(payload["mock_exams"]), 1)
        self.assertEqual(payload["mock_exams"][0]["module_type"], "mock_reading")
        self.assertEqual(payload["mock_exams"][0]["details"][0]["kind"], "jianya_mock")
        self.assertEqual(payload["wrong_book_counts"].get("dictation"), 1)
        self.assertEqual(payload["wrong_book_counts"].get("sentence"), 1)
        self.assertIn("task_overview", payload)

    def test_missing_student(self) -> None:
        conn = _connect()
        payload, err = load_student_detail(conn, "nope")
        self.assertIsNone(payload)
        self.assertEqual(err, "学生不存在")


if __name__ == "__main__":
    unittest.main()
