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
    add_recipients,
    create_assignment,
    create_pack,
    delete_assignment,
    delete_pack,
    ensure_jianya_tables,
    get_assignment,
    get_draft,
    get_roster,
    get_submission,
    list_all_packs,
    list_assignments,
    list_student_assignments,
    list_student_submissions,
    list_submissions,
    publish_from_packs,
    save_draft,
    save_review,
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
            student_ids=["2025001"],
        )
        self.assertTrue(created["id"].startswith("a"))
        listed = list_assignments(conn)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["title"], "听力专项")
        self.assertEqual(listed[0]["assignedCount"], 1)
        self.assertEqual(listed[0]["studentIds"], ["2025001"])
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
        asg = create_assignment(
            conn, title="t", subject="listening", parts=[PART], student_ids=["2025001"]
        )
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
        asg = create_assignment(
            conn, title="听力作业", subject="listening", parts=[PART], student_ids=["2025001"]
        )
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
        asg = create_assignment(
            conn, title="t", subject="listening", parts=[PART], student_ids=["2025001"]
        )
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
        created = publish_from_packs(
            conn,
            [pack["id"]],
            title_prefix="Week 1",
            created_by="admin",
            student_ids=["2025001", "2025002"],
        )
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

    def test_requires_students_and_hides_unassigned(self) -> None:
        conn = _conn()
        with self.assertRaisesRegex(ValueError, "至少选择一名学生"):
            create_assignment(conn, title="x", subject="listening", parts=[PART], student_ids=[])
        asg = create_assignment(
            conn,
            title="定向作业",
            subject="listening",
            parts=[PART],
            student_ids=["2025001"],
        )
        self.assertEqual(list_student_assignments(conn, "2025001")[0]["id"], asg["id"])
        self.assertEqual(list_student_assignments(conn, "2025002"), [])
        with self.assertRaisesRegex(ValueError, "未布置给你"):
            save_submission(
                conn,
                assignment_id=asg["id"],
                student_id="2025002",
                book_id=21,
                subject="listening",
                s_id=2999,
                answers={"1": "x"},
                correct=0,
                total=10,
                wrong=0,
                blank=10,
                pct=0,
            )

    def test_add_recipients_roster_and_review(self) -> None:
        conn = _conn()
        asg = create_assignment(
            conn,
            title="周练",
            subject="listening",
            parts=[PART],
            student_ids=["2025001"],
        )
        roster = add_recipients(conn, asg["id"], ["2025002"])
        self.assertEqual(roster["assignedCount"], 2)
        self.assertEqual(roster["submittedCount"], 0)
        missing_ids = [row["studentId"] for row in roster["students"] if row["status"] == "missing"]
        self.assertEqual(missing_ids, ["2025001", "2025002"])
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
        roster = get_roster(conn, asg["id"])
        self.assertEqual(roster["submittedCount"], 1)
        by_id = {row["studentId"]: row for row in roster["students"]}
        self.assertEqual(by_id["2025001"]["status"], "submitted")
        self.assertEqual(by_id["2025002"]["status"], "missing")
        review = save_review(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            comment="Part 1 拼写要注意",
            created_by="zhangxiaodong",
        )
        self.assertEqual(review["comment"], "Part 1 拼写要注意")
        mine = list_student_assignments(conn, "2025001")
        self.assertEqual(mine[0]["comment"], "Part 1 拼写要注意")
        self.assertEqual(mine[0]["mySubmittedParts"], 1)
        self.assertEqual(mine[0]["myStatus"], "submitted")
        before = list_student_assignments(conn, "2025002")
        self.assertEqual(before[0]["myStatus"], "missing")

    def test_teacher_sees_own_and_admin_packs_only(self) -> None:
        conn = _conn()
        create_pack(
            conn,
            title="别人的包",
            subject="listening",
            parts=[PART],
            created_by="lisi",
        )
        mine = create_pack(
            conn,
            title="我的包",
            subject="listening",
            parts=[PART],
            created_by="zhangxiaodong",
        )
        admin_pack = create_pack(
            conn,
            title="管理员包",
            subject="listening",
            parts=[PART],
            created_by="admin",
        )
        visible = [
            p["title"]
            for p in list_all_packs(conn, viewer_id="zhangxiaodong")
            if not p.get("builtin")
        ]
        self.assertEqual(visible[0], "管理员包")
        self.assertEqual(set(visible), {"管理员包", "我的包"})
        with self.assertRaisesRegex(ValueError, "自己建立"):
            delete_pack(conn, admin_pack["id"], actor_id="zhangxiaodong")
        delete_pack(conn, mine["id"], actor_id="zhangxiaodong")
        other_asg = create_assignment(
            conn,
            title="别人的作业",
            subject="listening",
            parts=[PART],
            created_by="lisi",
            student_ids=["2025001"],
        )
        mine_asg = create_assignment(
            conn,
            title="我的作业",
            subject="listening",
            parts=[PART],
            created_by="zhangxiaodong",
            student_ids=["2025001"],
        )
        listed = list_assignments(conn, created_by="zhangxiaodong")
        self.assertEqual([row["id"] for row in listed], [mine_asg["id"]])
        with self.assertRaisesRegex(ValueError, "自己布置"):
            delete_assignment(conn, other_asg["id"], actor_id="zhangxiaodong")

    def test_speaking_packs_not_open(self) -> None:
        conn = _conn()
        with self.assertRaisesRegex(ValueError, "即将开放"):
            create_pack(
                conn,
                title="口语包",
                subject="speaking",
                parts=[PART],
                created_by="admin",
            )

    def test_writing_topics_can_be_selected(self) -> None:
        conn = _conn()
        with self.assertRaisesRegex(ValueError, "至少选择一个题目"):
            create_pack(
                conn,
                title="空写作包",
                subject="writing",
                parts=[],
                created_by="admin",
            )
        pack = create_pack(
            conn,
            title="强化段第一课自建",
            subject="writing",
            parts=[{"sId": 1}, {"sId": 22}],
            created_by="admin",
        )
        self.assertEqual(pack["subject"], "writing")
        self.assertEqual(len(pack["parts"]), 2)
        self.assertIn("personal benefits", pack["parts"][0]["prompt"])
        self.assertIn("主体段1", pack["parts"][0]["tips"])
        self.assertEqual(pack["parts"][1]["task"], "task1")
        self.assertEqual(pack["parts"][1]["sPart"], 1)
        builtin = [row for row in list_all_packs(conn) if row["id"] == "wpack-t1"]
        self.assertEqual(len(builtin), 1)
        self.assertEqual(len(builtin[0]["parts"]), 1)
        writing_builtin = [
            row
            for row in list_all_packs(conn)
            if row.get("builtin") and row["subject"] == "writing"
        ]
        self.assertEqual(len(writing_builtin), 29)
        asg = create_assignment(
            conn,
            title="写作作业",
            subject="writing",
            parts=[{"sId": 1}],
            created_by="zhangxiaodong",
            student_ids=["2025001"],
        )
        self.assertEqual(asg["parts"][0]["sId"], 1)
        saved = save_submission(
            conn,
            assignment_id=asg["id"],
            student_id="2025001",
            book_id=asg["parts"][0]["bookId"],
            subject="writing",
            s_id=1,
            answers={
                "outline": "个人健康对个人和社会都重要。",
                "essay": "Health matters for both individuals and society.",
            },
            correct=0,
            total=1,
            wrong=0,
            blank=0,
            pct=0,
            correction={
                "count": 1,
                "checkedAt": "2026-09-11T02:00:00Z",
                "originalEssay": "Health matters for both individuals and society.",
                "errors": [
                    {
                        "id": "e1",
                        "category": "主谓一致",
                        "sentenceIndex": 0,
                        "matchedText": "Health matters",
                        "question": "主谓是否一致？",
                        "hints": ["检查主语单复数"],
                        "explanation": "主语为单数，动词应一致。",
                        "corrected": "Health matters for both individuals and society.",
                    }
                ],
            },
        )
        self.assertEqual(saved["answers"]["essay"][:6], "Health")
        self.assertIn("个人健康", saved["answers"]["outline"])
        self.assertEqual(saved["correction"]["count"], 1)
        self.assertEqual(saved["correction"]["errors"][0]["category"], "主谓一致")
        reloaded = get_submission(
            conn, asg["id"], "2025001", asg["parts"][0]["bookId"], "writing", 1
        )
        self.assertEqual(reloaded["correction"]["count"], 1)


if __name__ == "__main__":
    unittest.main()
