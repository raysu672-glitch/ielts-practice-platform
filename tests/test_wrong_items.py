import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from student_api import (  # noqa: E402
    WRONG_STREAK_TO_MASTER,
    apply_wrong_item_results,
    apply_wrong_word_results,
    load_wrong_book_counts,
    load_wrong_book_items,
)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE wrong_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT NOT NULL DEFAULT 'dictation',
            word TEXT NOT NULL,
            wrong_count INTEGER DEFAULT 1,
            correct_streak INTEGER DEFAULT 0,
            last_tested TEXT,
            is_mastered INTEGER DEFAULT 0,
            UNIQUE(student_id, module_type, word)
        );
        CREATE TABLE wrong_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT NOT NULL,
            item_key TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            payload TEXT NOT NULL DEFAULT '{}',
            wrong_count INTEGER DEFAULT 1,
            correct_streak INTEGER DEFAULT 0,
            last_tested TEXT,
            is_mastered INTEGER DEFAULT 0,
            UNIQUE(student_id, module_type, item_key)
        );
        """
    )
    return conn


class WrongBookTests(unittest.TestCase):
    def test_streak_three_to_master(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "Hello", "is_correct": False}]
        )
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [
                {"item_key": "1", "title": "Hello", "is_correct": True},
                {"item_key": "1", "title": "Hello", "is_correct": True},
            ],
        )
        items = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=False)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["correct_streak"], 2)
        self.assertFalse(items[0]["is_mastered"])
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "Hello", "is_correct": True}]
        )
        items = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=False)
        self.assertTrue(items[0]["is_mastered"])
        self.assertEqual(WRONG_STREAK_TO_MASTER, 3)
        left = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True)
        self.assertEqual(left, [])

    def test_wrong_resets_streak(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "writing_phrase", [{"item_key": "en1", "title": "中文", "is_correct": False}]
        )
        apply_wrong_item_results(
            conn, "s1", "writing_phrase", [{"item_key": "en1", "title": "中文", "is_correct": True}]
        )
        apply_wrong_item_results(
            conn, "s1", "writing_phrase", [{"item_key": "en1", "title": "中文", "is_correct": False}]
        )
        items = load_wrong_book_items(conn, "s1", "writing_phrase")
        self.assertEqual(items[0]["correct_streak"], 0)
        self.assertEqual(items[0]["wrong_count"], 2)
        self.assertFalse(items[0]["is_mastered"])

    def test_correct_outside_book_does_nothing(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "listening_synonym", [{"item_key": "9", "title": "Hi", "is_correct": True}]
        )
        self.assertEqual(load_wrong_book_items(conn, "s1", "listening_synonym"), [])

    def test_dictation_wrong_no_longer_masters_on_fail(self) -> None:
        conn = _connect()
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": False}]
        )
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": True}]
        )
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": True}]
        )
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": False}]
        )
        items = load_wrong_book_items(conn, "s1", "dictation")
        self.assertEqual(len(items), 1)
        self.assertFalse(items[0]["is_mastered"])
        self.assertEqual(items[0]["correct_streak"], 0)

    def test_counts(self) -> None:
        conn = _connect()
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "a", "is_correct": False}]
        )
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "2", "title": "S", "is_correct": False}]
        )
        counts = load_wrong_book_counts(conn, "s1")
        self.assertEqual(counts["dictation"], 1)
        self.assertEqual(counts["sentence"], 1)


if __name__ == "__main__":
    unittest.main()
