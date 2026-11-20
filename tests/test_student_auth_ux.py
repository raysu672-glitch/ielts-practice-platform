import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from activity_log import ensure_activity_tables, log_activity  # noqa: E402
from password_utils import hash_password  # noqa: E402
from teacher_api import (  # noqa: E402
    PASSWORD_RESET_ACTION,
    list_duplicate_name_groups,
    list_students,
    lookup_student_by_id,
    merge_students,
    password_reset_counts_7d,
    reset_student_password,
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
            score REAL,
            correct_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0,
            is_passed INTEGER DEFAULT 0,
            pass_threshold REAL DEFAULT 0,
            created_at TEXT
        );
        CREATE TABLE study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT,
            duration_seconds INTEGER DEFAULT 0,
            created_at TEXT
        );
        CREATE TABLE word_mastery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            word TEXT NOT NULL,
            status TEXT DEFAULT 'learning',
            UNIQUE(student_id, word)
        );
        """
    )
    ensure_activity_tables(conn)
    return conn


def _add_student(conn: sqlite3.Connection, sid: str, name: str, status: str = "active") -> None:
    conn.execute(
        """
        INSERT INTO students (
            student_id, name, password, is_password_changed,
            target_score, status, created_at, updated_at
        ) VALUES (?, ?, ?, 1, 6.5, ?, '2026-01-01T00:00:00.000Z', '2026-01-01T00:00:00.000Z')
        """,
        (sid, name, hash_password("secret"), status),
    )
    conn.commit()


class StudentAuthUxTests(unittest.TestCase):
    def test_lookup_existing_and_missing(self) -> None:
        conn = _connect()
        _add_student(conn, "2025001", "张三")
        row, err = lookup_student_by_id(conn, "2025001")
        self.assertIsNone(err)
        self.assertEqual(row["name"], "张三")
        self.assertEqual(row["status"], "active")
        missing, err = lookup_student_by_id(conn, "2099999")
        self.assertIsNone(missing)
        self.assertEqual(err, "学号不存在")

    def test_password_reset_counts_in_list_students(self) -> None:
        conn = _connect()
        _add_student(conn, "2025001", "张三")
        _add_student(conn, "2025002", "李四")
        log_activity(
            conn,
            actor_role="teacher",
            actor_id="admin",
            actor_name="管理员",
            action=PASSWORD_RESET_ACTION,
            target_student_id="2025001",
            summary="重置",
        )
        log_activity(
            conn,
            actor_role="teacher",
            actor_id="admin",
            actor_name="管理员",
            action=PASSWORD_RESET_ACTION,
            target_student_id="2025001",
            summary="重置",
        )
        counts = password_reset_counts_7d(conn)
        self.assertEqual(counts.get("2025001"), 2)
        students = {s["student_id"]: s for s in list_students(conn)}
        self.assertEqual(students["2025001"]["resets_7d"], 2)
        self.assertEqual(students["2025002"]["resets_7d"], 0)

    def test_reset_student_password_still_works(self) -> None:
        conn = _connect()
        _add_student(conn, "2025001", "张三")
        pwd, err = reset_student_password(conn, "2025001")
        self.assertIsNone(err)
        self.assertTrue(pwd)

    def test_list_duplicate_name_groups(self) -> None:
        conn = _connect()
        _add_student(conn, "2025052", "郭思彤")
        _add_student(conn, "2025053", "郭思彤")
        _add_student(conn, "2025001", "独苗")
        conn.execute(
            "INSERT INTO test_records (student_id, module_type, score) VALUES ('2025052', 'dictation', 80)"
        )
        conn.commit()
        groups = list_duplicate_name_groups(conn)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["name"], "郭思彤")
        self.assertEqual(groups[0]["count"], 2)
        by_id = {s["student_id"]: s for s in groups[0]["students"]}
        self.assertEqual(by_id["2025052"]["test_records"], 1)
        self.assertEqual(by_id["2025053"]["test_records"], 0)

    def test_merge_students_remaps_and_deactivates(self) -> None:
        conn = _connect()
        _add_student(conn, "2025052", "郭思彤")
        _add_student(conn, "2025053", "郭思彤")
        conn.execute(
            "INSERT INTO test_records (student_id, module_type, score) VALUES ('2025053', 'dictation', 70)"
        )
        conn.execute(
            "INSERT INTO study_sessions (student_id, module_type) VALUES ('2025053', 'dictation')"
        )
        conn.execute(
            "INSERT INTO word_mastery (student_id, word) VALUES ('2025052', 'apple')"
        )
        conn.execute(
            "INSERT INTO word_mastery (student_id, word) VALUES ('2025053', 'apple')"
        )
        conn.execute(
            "INSERT INTO word_mastery (student_id, word) VALUES ('2025053', 'banana')"
        )
        conn.commit()
        result, err = merge_students(
            conn,
            keep_student_id="2025052",
            merge_student_ids=["2025053"],
        )
        self.assertIsNone(err)
        self.assertEqual(result["merged_ids"], ["2025053"])
        tests = conn.execute(
            "SELECT COUNT(*) AS c FROM test_records WHERE student_id='2025052'"
        ).fetchone()["c"]
        self.assertEqual(tests, 1)
        leftover = conn.execute(
            "SELECT COUNT(*) AS c FROM test_records WHERE student_id='2025053'"
        ).fetchone()["c"]
        self.assertEqual(leftover, 0)
        words = {
            r["word"]
            for r in conn.execute(
                "SELECT word FROM word_mastery WHERE student_id='2025052'"
            ).fetchall()
        }
        self.assertEqual(words, {"apple", "banana"})
        drop = dict(
            conn.execute(
                "SELECT status, name FROM students WHERE student_id='2025053'"
            ).fetchone()
        )
        self.assertEqual(drop["status"], "inactive")
        self.assertIn("已合并到2025052", drop["name"])


if __name__ == "__main__":
    unittest.main()
