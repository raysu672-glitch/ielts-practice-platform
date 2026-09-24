"""Debug traces stay out of the teacher activity timeline."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from activity_log import list_student_activity, log_activity  # noqa: E402
from debug_trace import (  # noqa: E402
    list_student_debug_events,
    log_student_debug_events,
    prune_debug_events,
)


class DebugTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row

    def tearDown(self) -> None:
        self.conn.close()

    def test_debug_events_are_not_in_teacher_timeline(self) -> None:
        log_activity(
            self.conn,
            actor_role="student",
            actor_id="2025065",
            action="task.open",
            target_student_id="2025065",
            summary="打开任务",
        )
        log_student_debug_events(
            self.conn,
            student_id="2025065",
            events=[
                {
                    "action": "click",
                    "page": "/juzifanyixin/index.html",
                    "target": "button 下一句",
                    "detail": {"password": "secret", "value": "hello"},
                    "t": "2026-09-24T05:00:00.000Z",
                }
            ],
        )
        timeline = list_student_activity(self.conn, "2025065")
        actions = [ev["action"] for ev in timeline["events"]]
        self.assertEqual(actions, ["task.open"])
        self.assertNotIn("click", actions)

        debug = list_student_debug_events(self.conn, "2025065")
        self.assertEqual(len(debug), 1)
        self.assertEqual(debug[0]["action"], "click")
        self.assertEqual(debug[0]["target"], "button 下一句")
        self.assertEqual(debug[0]["detail"]["password"], "")
        self.assertEqual(debug[0]["detail"]["value"], "hello")
        self.assertEqual(debug[0]["source"], "client")

    def test_drops_malformed_actions_and_prunes_old_rows(self) -> None:
        log_student_debug_events(
            self.conn,
            student_id="2025065",
            events=[{"action": "click ok"}, {"action": "page"}],
            source="server",
        )
        rows = list_student_debug_events(self.conn, "2025065")
        self.assertEqual([r["action"] for r in rows], ["page"])
        self.assertEqual(rows[0]["source"], "server")

        old = (datetime.now(timezone.utc) - timedelta(days=40)).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        )
        self.conn.execute(
            "UPDATE student_debug_events SET created_at=? WHERE action='page'",
            (old,),
        )
        self.conn.commit()
        deleted = prune_debug_events(self.conn, retention_days=30)
        self.assertEqual(deleted, 1)
        self.assertEqual(list_student_debug_events(self.conn, "2025065"), [])
