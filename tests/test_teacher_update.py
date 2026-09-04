import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from teacher_api import (  # noqa: E402
    create_student,
    create_teacher,
    update_student,
    update_teacher,
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
        CREATE TABLE teachers (
            teacher_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            is_password_changed INTEGER DEFAULT 0,
            position TEXT DEFAULT '',
            subjects TEXT DEFAULT '',
            status TEXT DEFAULT 'active',
            created_at TEXT,
            updated_at TEXT
        );
        """
    )
    return conn


class TeacherUpdateTests(unittest.TestCase):
    def test_update_student_name_and_target(self) -> None:
        conn = _connect()
        student, err, _pwd = create_student(conn, name="张三", target_score=6.5)
        self.assertIsNone(err)
        sid = student["student_id"]
        updated, err = update_student(
            conn, student_id=sid, name="李四", target_score=7
        )
        self.assertIsNone(err)
        self.assertEqual(updated["name"], "李四")
        self.assertEqual(updated["target_score"], 7)
        self.assertEqual(updated["student_id"], sid)

    def test_update_missing_student(self) -> None:
        conn = _connect()
        row, err = update_student(conn, student_id="nope", name="甲", target_score=6)
        self.assertIsNone(row)
        self.assertEqual(err, "学生不存在")

    def test_update_teacher_profile(self) -> None:
        conn = _connect()
        teacher, err, _pwd = create_teacher(
            conn, teacher_id="wang", name="王老师", position="助教", subjects="听力"
        )
        self.assertIsNone(err)
        updated, err = update_teacher(
            conn,
            teacher_id="wang",
            name="王晓",
            position="教研",
            subjects="阅读、写作",
        )
        self.assertIsNone(err)
        self.assertEqual(updated["name"], "王晓")
        self.assertEqual(updated["position"], "教研")
        self.assertEqual(updated["subjects"], "阅读、写作")
        self.assertEqual(updated["teacher_id"], "wang")

    def test_cannot_update_admin_teacher(self) -> None:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO teachers (
                teacher_id, name, password, position, subjects, status
            ) VALUES ('admin', '管理员', 'x', '', '', 'active')
            """
        )
        conn.commit()
        row, err = update_teacher(
            conn, teacher_id="admin", name="改名", position="x", subjects="y"
        )
        self.assertIsNone(row)
        self.assertEqual(err, "不能修改管理员账号")


if __name__ == "__main__":
    unittest.main()
