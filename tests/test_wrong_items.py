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

    def test_official_mix_and_master_then_reenter(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [
                {"item_key": "1", "title": "InBook", "is_correct": False},
                {"item_key": "2", "title": "AlsoIn", "is_correct": False},
            ],
        )
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [{"item_key": "1", "title": "InBook", "is_correct": True}],
        )
        # 外面大测试：本里做对连对+1、本里做错清零、新题做错入本、新题做对不入本
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [
                {"item_key": "1", "title": "InBook", "is_correct": True},
                {"item_key": "2", "title": "AlsoIn", "is_correct": False},
                {"item_key": "3", "title": "NewWrong", "is_correct": False},
                {"item_key": "4", "title": "NewRight", "is_correct": True},
            ],
        )
        book = {
            it["item_key"]: it
            for it in load_wrong_book_items(conn, "s1", "sentence", unmastered_only=False)
        }
        self.assertEqual(book["1"]["correct_streak"], 2)
        self.assertFalse(book["1"]["is_mastered"])
        self.assertEqual(book["2"]["correct_streak"], 0)
        self.assertIn("3", book)
        self.assertNotIn("4", book)
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "InBook", "is_correct": True}]
        )
        left = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True)
        self.assertEqual(sorted(it["item_key"] for it in left), ["2", "3"])
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "InBook", "is_correct": False}]
        )
        back = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True)
        keys = [it["item_key"] for it in back]
        self.assertIn("1", keys)
        self.assertEqual(
            [it["correct_streak"] for it in back if it["item_key"] == "1"][0],
            0,
        )

    def test_skip_breaks_streak_but_does_not_add(self) -> None:
        conn = _connect()
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": False}]
        )
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": True}]
        )
        apply_wrong_word_results(
            conn,
            "s1",
            "dictation",
            [
                {"word": "apple", "is_correct": False, "skipped": True},
                {"word": "banana", "is_correct": False, "skipped": True},
            ],
        )
        items = load_wrong_book_items(conn, "s1", "dictation", unmastered_only=True)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_key"], "apple")
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

    def test_empty_results_and_blank_keys_do_nothing(self) -> None:
        conn = _connect()
        apply_wrong_item_results(conn, "s1", "sentence", [])
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [{"item_key": "", "title": "Nope", "is_correct": False}],
        )
        self.assertEqual(load_wrong_book_items(conn, "s1", "sentence"), [])
        self.assertEqual(load_wrong_book_counts(conn, "s1"), {})

    def test_streak_zero_stays_in_book(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "A", "is_correct": False}]
        )
        items = load_wrong_book_items(conn, "s1", "sentence")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["correct_streak"], 0)
        self.assertFalse(items[0]["is_mastered"])
        counts = load_wrong_book_counts(conn, "s1")
        self.assertEqual(counts["sentence"], 1)

    def test_item_skip_resets_in_book_and_does_not_add(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "writing_phrase", [{"item_key": "en1", "title": "中文", "is_correct": False}]
        )
        apply_wrong_item_results(
            conn, "s1", "writing_phrase", [{"item_key": "en1", "title": "中文", "is_correct": True}]
        )
        apply_wrong_item_results(
            conn,
            "s1",
            "writing_phrase",
            [
                {"item_key": "en1", "title": "中文", "is_correct": False, "skipped": True},
                {"item_key": "en2", "title": "新题", "is_correct": False, "skipped": True},
            ],
        )
        items = load_wrong_book_items(conn, "s1", "writing_phrase", unmastered_only=True)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_key"], "en1")
        self.assertEqual(items[0]["correct_streak"], 0)
        self.assertEqual(items[0]["wrong_count"], 1)

    def test_skip_mastered_does_not_reenter(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "A", "is_correct": False}]
        )
        for _ in range(3):
            apply_wrong_item_results(
                conn, "s1", "sentence", [{"item_key": "1", "title": "A", "is_correct": True}]
            )
        self.assertEqual(load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True), [])
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [{"item_key": "1", "title": "A", "is_correct": False, "skipped": True}],
        )
        self.assertEqual(load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True), [])

    def test_dictation_official_mix(self) -> None:
        conn = _connect()
        apply_wrong_word_results(
            conn,
            "s1",
            "dictation",
            [
                {"word": "apple", "is_correct": False},
                {"word": "banana", "is_correct": False},
            ],
        )
        apply_wrong_word_results(
            conn, "s1", "dictation", [{"word": "apple", "is_correct": True}]
        )
        apply_wrong_word_results(
            conn,
            "s1",
            "dictation",
            [
                {"word": "apple", "is_correct": True},
                {"word": "banana", "is_correct": False},
                {"word": "cherry", "is_correct": False},
                {"word": "date", "is_correct": True},
            ],
        )
        book = {
            it["item_key"]: it
            for it in load_wrong_book_items(conn, "s1", "dictation", unmastered_only=False)
        }
        self.assertEqual(book["apple"]["correct_streak"], 2)
        self.assertFalse(book["apple"]["is_mastered"])
        self.assertEqual(book["banana"]["correct_streak"], 0)
        self.assertIn("cherry", book)
        self.assertNotIn("date", book)

    def test_unattempted_not_in_payload_keeps_streak(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "InBook", "is_correct": False}]
        )
        apply_wrong_item_results(
            conn, "s1", "sentence", [{"item_key": "1", "title": "InBook", "is_correct": True}]
        )
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [{"item_key": "9", "title": "AttemptedNew", "is_correct": False}],
        )
        book = {
            it["item_key"]: it
            for it in load_wrong_book_items(conn, "s1", "sentence", unmastered_only=True)
        }
        self.assertEqual(book["1"]["correct_streak"], 1)
        self.assertIn("9", book)

    def test_same_batch_wrong_then_correct_counts_once_each(self) -> None:
        conn = _connect()
        apply_wrong_item_results(
            conn,
            "s1",
            "sentence",
            [
                {"item_key": "1", "title": "A", "is_correct": False},
                {"item_key": "1", "title": "A", "is_correct": True},
            ],
        )
        items = load_wrong_book_items(conn, "s1", "sentence", unmastered_only=False)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["correct_streak"], 1)
        self.assertEqual(items[0]["wrong_count"], 1)


if __name__ == "__main__":
    unittest.main()
