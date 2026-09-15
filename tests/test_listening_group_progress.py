# -*- coding: utf-8 -*-
"""Tests for listening group green-bar progress persistence."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from student_api import (  # noqa: E402
    ensure_listening_group_progress_table,
    load_listening_group_progress,
    upsert_listening_group_progress,
)


class ListeningGroupProgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "t.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                name TEXT
            )
            """
        )
        self.conn.execute("INSERT INTO students (student_id, name) VALUES ('2025001', '测')")
        self.conn.commit()
        ensure_listening_group_progress_table(self.conn)

    def tearDown(self) -> None:
        self.conn.close()
        self.tmp.cleanup()

    def test_upsert_and_load(self) -> None:
        data = upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening",
                "groups": [
                    {
                        "group_index": 10,
                        "first_correct": 7,
                        "first_total": 20,
                        "status": "pending",
                    }
                ],
            },
        )
        self.assertEqual(data["book_key"], "listening")
        self.assertEqual(len(data["groups"]), 1)
        g = data["groups"][0]
        self.assertEqual(g["group_index"], 10)
        self.assertEqual(g["first_correct"], 7)
        self.assertEqual(g["first_total"], 20)
        self.assertEqual(g["status"], "pending")

        upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening",
                "groups": [{"group_index": 10, "status": "completed"}],
            },
        )
        loaded = load_listening_group_progress(self.conn, "2025001", "listening")
        g2 = loaded["groups"][0]
        self.assertEqual(g2["first_correct"], 7)
        self.assertEqual(g2["first_total"], 20)
        self.assertEqual(g2["status"], "completed")

    def test_completed_not_downgraded(self) -> None:
        upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening",
                "group_index": 0,
                "first_correct": 20,
                "first_total": 20,
                "status": "completed",
            },
        )
        upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening",
                "group_index": 0,
                "first_correct": 5,
                "first_total": 20,
                "status": "pending",
            },
        )
        g = load_listening_group_progress(self.conn, "2025001", "listening")["groups"][0]
        self.assertEqual(g["status"], "completed")
        self.assertEqual(g["first_correct"], 5)

    def test_books_isolated(self) -> None:
        upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening",
                "group_index": 1,
                "first_correct": 10,
                "first_total": 20,
                "status": "completed",
            },
        )
        upsert_listening_group_progress(
            self.conn,
            "2025001",
            {
                "book_key": "listening_basic",
                "group_index": 1,
                "first_correct": 40,
                "first_total": 50,
                "status": "pending",
            },
        )
        a = load_listening_group_progress(self.conn, "2025001", "listening")["groups"]
        b = load_listening_group_progress(self.conn, "2025001", "listening_basic")["groups"]
        self.assertEqual(a[0]["first_total"], 20)
        self.assertEqual(b[0]["first_total"], 50)

    def test_invalid_book(self) -> None:
        with self.assertRaises(ValueError):
            upsert_listening_group_progress(
                self.conn,
                "2025001",
                {"book_key": "other", "group_index": 0, "first_total": 1, "first_correct": 1},
            )


if __name__ == "__main__":
    unittest.main()
