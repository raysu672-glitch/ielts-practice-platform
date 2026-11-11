"""新版学习路线 /api/v2/progress/me 的原始事实。"""

from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from task_api import (  # noqa: E402
    apply_draft_to_live,
    ensure_task_tables,
    put_plan_draft,
    seed_mvp_units,
    submit_stage_test,
)
from v2_progress_api import build_route_facts  # noqa: E402


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY, name TEXT NOT NULL,
            password TEXT NOT NULL DEFAULT 'x', target_score REAL DEFAULT 6.5,
            status TEXT DEFAULT 'active'
        );
        CREATE TABLE test_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            module_type TEXT DEFAULT 'dictation', module_name TEXT DEFAULT '',
            test_type TEXT NOT NULL DEFAULT 'module_test', score REAL NOT NULL,
            correct_count INTEGER NOT NULL DEFAULT 0, total_count INTEGER NOT NULL DEFAULT 0,
            is_passed INTEGER NOT NULL, pass_threshold REAL NOT NULL,
            duration_seconds INTEGER DEFAULT 0, details TEXT DEFAULT '[]',
            started_at TEXT, ended_at TEXT,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE TABLE study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            module_type TEXT NOT NULL, module_name TEXT, session_kind TEXT DEFAULT 'study',
            plan_item_id INTEGER, unit_id TEXT, duration_seconds INTEGER NOT NULL DEFAULT 0,
            created_at TEXT
        );
        INSERT INTO students (student_id, name) VALUES ('s1', '测试生');
        """
    )
    ensure_task_tables(conn)
    seed_mvp_units(conn)
    return conn


def _plan(conn: sqlite3.Connection, units: list[str], tests: list[list[str]]) -> None:
    items = [{"item_type": "study", "unit_id": u} for u in units]
    for covered in tests:
        items.append({"item_type": "test", "test_unit_ids": covered, "module_type": "dictation"})
    put_plan_draft(conn, "s1", items)


class RouteFactsTest(unittest.TestCase):
    def test_empty_plan(self) -> None:
        conn = _connect()
        facts = build_route_facts(conn, "s1")
        self.assertEqual(facts["source"], "platform_db")
        self.assertEqual(facts["plan_items"], [])
        self.assertEqual(facts["student"]["name"], "测试生")

    def test_plan_and_stage_attempts(self) -> None:
        conn = _connect()
        _plan(conn, ["dictation_u01", "dictation_u02"], [["dictation_u01"], ["dictation_u01", "dictation_u02"]])
        test_items = [
            r for r in conn.execute(
                "SELECT id, test_unit_ids FROM plan_items WHERE student_id='s1' AND item_type='test' ORDER BY sort_order"
            )
        ]
        single = next(r["id"] for r in test_items if r["test_unit_ids"].count("dictation") == 1)
        submit_stage_test(conn, "s1", single, 90, threshold=80)
        submit_stage_test(conn, "s1", single, 50, threshold=80)
        conn.execute(
            "INSERT INTO test_records (student_id, module_type, module_name, score, is_passed, pass_threshold) "
            "VALUES ('s1', 'dictation', '听力1000词', 95, 1, 80)"
        )

        facts = build_route_facts(conn, "s1")
        study = [i for i in facts["plan_items"] if i["item_type"] == "study"]
        self.assertEqual([i["unit_id"] for i in study], ["dictation_u01", "dictation_u02"])
        self.assertTrue(all(i["unit_title"] for i in study))
        tests = [i for i in facts["plan_items"] if i["item_type"] == "test"]
        self.assertEqual(sorted(len(t["test_unit_ids"]) for t in tests), [1, 2])
        self.assertEqual(len(facts["test_attempts"]), 2, "只带阶段测，不带模块测试")
        self.assertEqual([a["passed"] for a in facts["test_attempts"]], [True, False])
        self.assertTrue(all(a["test_title"] for a in facts["test_attempts"]))
        self.assertEqual(facts["module_names"]["dictation"], "听力1000词")

    def test_attempts_survive_plan_reapply(self) -> None:
        conn = _connect()
        _plan(conn, ["dictation_u01"], [["dictation_u01"]])
        tid = conn.execute("SELECT id FROM plan_items WHERE item_type='test'").fetchone()["id"]
        submit_stage_test(conn, "s1", tid, 90, threshold=80)
        _plan(conn, ["dictation_u01", "dictation_u02"], [["dictation_u01"]])
        apply_draft_to_live(conn, "s1")
        facts = build_route_facts(conn, "s1")
        test_item = next(i for i in facts["plan_items"] if i["item_type"] == "test")
        self.assertFalse(test_item["test_passed"], "重新应用清单会清零计划里的过关标记")
        self.assertEqual(len(facts["test_attempts"]), 1)
        self.assertEqual(facts["test_attempts"][0]["test_title"], test_item["test_title"] or "阶段测")


if __name__ == "__main__":
    unittest.main()
