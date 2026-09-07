"""剑雅作业 SQLite API。"""

from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from jianya_api import (  # noqa: E402
    create_assignment,
    create_pack,
    delete_assignment,
    delete_pack,
    ensure_jianya_tables,
    get_assignment,
    get_draft,
    get_submission,
    list_all_packs,
    list_assignments,
    list_student_submissions,
    list_submissions,
    publish_from_packs,
    save_draft,
    save_submission,
)


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    ensure_jianya_tables(conn)
    return conn


PART = {
    "bookId": 21,
    "subject": "listening",
    "sId": 2999,
    "testNo": 1,
    "sPart": 1,
    "label": "C21 Test 1 Part 1",
    "questionCount": 10,
}


class JianyaApiTests(unittest.TestCase):
    def test_create_list_delete_assignment(self) -> None:
        conn = _conn()
        created = create_assignment(
            conn,
            title="听力专项",
            subject="listening",
            parts=[PART],
            created_by="zhangxiaodong",
        )
        self.assertTrue(created["id"].startswith("a"))
        listed = list_assignments(conn)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["title"], "听力专项")
        self.assertEqual(get_assignment(conn, created["id"])["parts"][0]["sId"], 2999)
        delete_assignment(conn, created["id"])
        self.assertEqual(list_assignments(conn), [])

    def test_rejects_mixed_subject_parts(self) -> None:
        conn = _conn()
        mixed = dict(PART)
        mixed["subject"] = "reading"
        with self.assertRaisesRegex(ValueError, "同一科目"):
            create_assignment(conn, title="x", subject="listening", parts=[PART, mixed])

    def test_submission_locked_after_first_save(self) -> None:
        conn = _conn()
        asg = create_assignment(conn, title="t", subject="listening", parts=[PART])
        first = save_submission(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "club"},
            correct=8,
            total=10,
            wrong=1,
            blank=1,
            pct=80,
        )
        second = save_submission(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "changed"},
            correct=1,
            total=10,
            wrong=9,
            blank=0,
            pct=10,
        )
        self.assertEqual(second["answers"]["1"], "club")
        self.assertEqual(first["pct"], 80)
        mine = list_submissions(conn, asg["id"], student_id="2025001")
        all_subs = list_submissions(conn, asg["id"])
        self.assertEqual(len(mine), 1)
        self.assertEqual(len(all_subs), 1)

    def test_list_student_submissions_includes_part(self) -> None:
        conn = _conn()
        asg = create_assignment(conn, title="听力作业", subject="listening", parts=[PART])
        save_submission(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "club"},
            correct=8,
            total=10,
            wrong=1,
            blank=1,
            pct=80,
        )
        rows = list_student_submissions(conn, "2025001")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["sPart"], 1)
        self.assertEqual(rows[0]["assignmentTitle"], "听力作业")
        self.assertEqual(list_student_submissions(conn, "other"), [])

    def test_draft_then_submit(self) -> None:
        conn = _conn()
        asg = create_assignment(conn, title="t", subject="listening", parts=[PART])
        save_draft(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "bay"},
        )
        self.assertEqual(get_draft(conn, asg["id"], "2025001", 21, "listening", 2999)["1"], "bay")
        save_submission(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "bay"},
            correct=1,
            total=10,
            wrong=0,
            blank=9,
            pct=10,
        )
        save_draft(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=21,
            subject="listening",
            s_id=2999,
            answers={"1": "hacked"},
        )
        self.assertEqual(get_draft(conn, asg["id"], "2025001", 21, "listening", 2999)["1"], "bay")
        self.assertIsNotNone(get_submission(conn, asg["id"], "2025001", 21, "listening", 2999))

    def test_custom_pack_and_publish(self) -> None:
        conn = _conn()
        pack = create_pack(
            conn,
            title="自建包",
            subject="listening",
            parts=[PART],
            created_by="admin",
        )
        created = publish_from_packs(conn, [pack["id"]], title_prefix="Week 1", created_by="admin")
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0]["title"], "Week 1 · 自建包")
        self.assertEqual(created[0]["packId"], pack["id"])
        delete_pack(conn, pack["id"])
        with self.assertRaisesRegex(ValueError, "不可删除"):
            delete_pack(conn, pack["id"])

    def test_builtin_packs_from_file(self) -> None:
        conn = _conn()
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "assignment-packs.json"
            path.write_text(
                json.dumps(
                    {
                        "packs": [
                            {
                                "id": "c21-l-t1",
                                "title": "C21 听力 Test 1",
                                "subject": "listening",
                                "parts": [PART],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            packs = list_all_packs(conn, packs_path=path)
            self.assertEqual(packs[0]["id"], "c21-l-t1")
            self.assertTrue(packs[0]["builtin"])


if __name__ == "__main__":
    unittest.main()
