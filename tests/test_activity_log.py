"""Tests for activity_log (key-action timeline, 90-day retention)."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from activity_log import (  # noqa: E402
    ensure_activity_tables,
    list_student_activity,
    log_activity,
    log_student_client_events,
    prune_old_activity_events,
)


class ActivityLogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        ensure_activity_tables(self.conn)

    def tearDown(self) -> None:
        self.conn.close()

    def test_log_and_list_for_student(self) -> None:
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025062",
            actor_name="商娇龙",
            action="sentence.abc_submit",
            module_type="sentence",
            target_student_id="2025062",
            summary="主谓宾正确",
            detail={"box_index": 0, "correct": True},
        )
        log_activity(
            self.conn,
            actor_role="teacher",
            actor_id="admin",
            action="plan.save",
            target_student_id="2025062",
            summary="保存计划",
        )
        rows = list_student_activity(self.conn, "2025062", limit=20)
        self.assertEqual(len(rows["events"]), 2)
        self.assertEqual(rows["events"][0]["action"], "plan.save")
        self.assertEqual(rows["events"][1]["action"], "sentence.abc_submit")
        self.assertIn("created_at_cn", rows["events"][0])

    def test_client_events_filter_unknown_actions(self) -> None:
        out = log_student_client_events(
            self.conn,
            student_id="2025001",
            student_name="测",
            events=[
                {"action": "sentence.open", "summary": "开句"},
                {"action": "hack.delete_all", "summary": "应被拒绝"},
                {"action": "translate.step_submit", "detail": {"correct": False}},
            ],
        )
        self.assertEqual(out["saved"], 2)
        rows = list_student_activity(self.conn, "2025001")
        actions = {r["action"] for r in rows["events"]}
        self.assertEqual(actions, {"sentence.open", "translate.step_submit"})

    def test_prune_older_than_90_days(self) -> None:
        old = (datetime.now(timezone.utc) - timedelta(days=100)).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        )
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025001",
            action="task.open",
            target_student_id="2025001",
            created_at=old,
            prune_occasionally=False,
        )
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025001",
            action="task.exit",
            target_student_id="2025001",
            prune_occasionally=False,
        )
        deleted = prune_old_activity_events(self.conn, retention_days=90)
        self.assertEqual(deleted, 1)
        rows = list_student_activity(self.conn, "2025001")
        self.assertEqual(len(rows["events"]), 1)
        self.assertEqual(rows["events"][0]["action"], "task.exit")

    def test_filter_by_china_date_and_page(self) -> None:
        from activity_log import _china_day_utc_bounds

        start, end = _china_day_utc_bounds("2026-09-14")
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025001",
            action="sentence.open",
            target_student_id="2025001",
            created_at=start.replace(".000Z", ".100Z"),
            prune_occasionally=False,
        )
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025001",
            action="task.open",
            target_student_id="2025001",
            created_at=end,  # next day boundary exclusive
            prune_occasionally=False,
        )
        page1 = list_student_activity(
            self.conn, "2025001", on_date="2026-09-14", page=1, page_size=10
        )
        self.assertEqual(page1["total"], 1)
        self.assertEqual(page1["events"][0]["action"], "sentence.open")


if __name__ == "__main__":
    unittest.main()
