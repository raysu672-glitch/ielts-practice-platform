# -*- coding: utf-8 -*-
"""Per-student AI checkup digest (no live AI calls)."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from activity_log import (  # noqa: E402
    build_student_activity_summary_for_ai,
    ensure_activity_tables,
    log_activity,
)
from teacher_api import (  # noqa: E402
    build_student_checkup_digest,
    format_student_checkup_prompt,
)


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
    ensure_activity_tables(conn)
    return conn


class StudentCheckupDigestTests(unittest.TestCase):
    def test_student_activity_summary_filters_by_student(self) -> None:
        conn = _connect()
        log_activity(
            conn,
            actor_role="student",
            actor_id="2025001",
            action="task.open",
            target_student_id="2025001",
            module_type="sentence",
            summary="开任务",
            prune_occasionally=False,
        )
        log_activity(
            conn,
            actor_role="student",
            actor_id="2025002",
            action="task.open",
            target_student_id="2025002",
            summary="其他人",
            prune_occasionally=False,
        )
        summary = build_student_activity_summary_for_ai(conn, "2025001", days=14)
        self.assertEqual(summary["total_events"], 1)
        self.assertEqual(summary["top_actions"][0]["action"], "task.open")
        self.assertTrue(any("2025001" in line for line in summary["sample_lines"]))
        self.assertFalse(any("2025002" in line for line in summary["sample_lines"]))
        conn.close()

    def test_build_and_format_checkup_digest(self) -> None:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO students (
                student_id, name, password, target_score, status
            ) VALUES ('2025001', '测试生', 'x', 6.5, 'active')
            """
        )
        conn.execute(
            """
            INSERT INTO test_records (
                student_id, module_type, module_name, test_type,
                score, correct_count, total_count, is_passed,
                duration_seconds, created_at
            ) VALUES (
                '2025001', 'sentence', '句型', 'unit_test',
                80, 8, 10, 1, 600, '2026-10-01T01:00:00.000Z'
            )
            """
        )
        conn.execute(
            """
            INSERT INTO study_sessions (
                student_id, module_type, session_kind, duration_seconds, created_at
            ) VALUES ('2025001', 'sentence', 'study', 1800, '2026-10-01T02:00:00.000Z')
            """
        )
        conn.execute(
            """
            INSERT INTO wrong_words (
                student_id, module_type, word, is_mastered, last_tested
            ) VALUES ('2025001', 'listening', 'harbour', 0, '2026-10-01')
            """
        )
        log_activity(
            conn,
            actor_role="student",
            actor_id="2025001",
            action="sentence.open",
            target_student_id="2025001",
            module_type="sentence",
            summary="打开句型",
            prune_occasionally=False,
        )
        conn.commit()

        digest, err = build_student_checkup_digest(conn, "2025001", days=14)
        self.assertIsNone(err)
        assert digest is not None
        self.assertEqual(digest["student"]["student_id"], "2025001")
        self.assertEqual(digest["study"]["test_count"], 1)
        self.assertEqual(digest["study"]["pass_count"], 1)
        self.assertEqual(digest["study"]["total_minutes"], 30)
        self.assertEqual(digest["study"]["unmastered_wrong_words"], 1)
        self.assertEqual(digest["activity"]["total_events"], 1)

        prompt = format_student_checkup_prompt(digest)
        self.assertIn("2025001", prompt)
        self.assertIn("测试生", prompt)
        self.assertIn("sentence.open", prompt)
        self.assertIn("任务看板", prompt)

        missing, missing_err = build_student_checkup_digest(conn, "9999999", days=7)
        self.assertIsNone(missing)
        self.assertEqual(missing_err, "学生不存在")
        conn.close()


if __name__ == "__main__":
    unittest.main()
