# -*- coding: utf-8 -*-
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from placement_api import (  # noqa: E402
    ensure_placement_guest_table,
    insert_placement_guest,
    list_placement_guests,
)


class PlacementGuestTests(unittest.TestCase):
    def setUp(self):
        self.db = Path(tempfile.mkdtemp()) / "p.db"
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        ensure_placement_guest_table(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_insert_requires_name(self):
        with self.assertRaises(ValueError):
            insert_placement_guest(self.conn, {"guest_name": "  "})

    def test_insert_and_list(self):
        row = insert_placement_guest(
            self.conn,
            {
                "guest_name": "李四",
                "contact": "wx_demo",
                "target_score": 6.5,
                "score_percent": 58,
                "summary": "整体约 5.5",
                "report": {
                    "form": "A",
                    "overall": {"label": "5.5–6.0"},
                    "bands": {"listening": {"label": "5.5–6.0"}},
                    "planHint": "写作基础优先",
                },
            },
        )
        self.assertTrue(row["id"])
        rows = list_placement_guests(self.conn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["guest_name"], "李四")
        self.assertEqual(rows[0]["report"]["overall"]["label"], "5.5–6.0")


if __name__ == "__main__":
    unittest.main()
