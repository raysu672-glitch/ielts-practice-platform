# -*- coding: utf-8 -*-
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from trial_api import (  # noqa: E402
    claim_trial_code,
    create_trial_code,
    ensure_trial_tables,
)


class TrialApiTests(unittest.TestCase):
    def setUp(self):
        self.db = Path(tempfile.mkdtemp()) / "t.db"
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        ensure_trial_tables(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_create_requires_wx(self):
        with self.assertRaises(ValueError):
            create_trial_code(self.conn, {"advisor_wx": "a"})
        with self.assertRaises(ValueError):
            create_trial_code(self.conn, {"guest_wx": "b"})

    def test_one_time_claim(self):
        created = create_trial_code(
            self.conn,
            {"advisor_wx": "advisor1", "guest_wx": "client1", "days": 5},
        )
        code = created["code"]
        self.assertEqual(len(code), 8)
        self.assertTrue(created["once"])

        claim = claim_trial_code(
            self.conn,
            {
                "code": code.lower(),
                "guest_name": "王五",
                "guest_wx": "client1",
                "target_score": 5.0,
            },
        )
        self.assertEqual(claim["guest_name"], "王五")
        self.assertEqual(claim["days_left"], 5)

        with self.assertRaises(ValueError) as ctx:
            claim_trial_code(
                self.conn,
                {
                    "code": code,
                    "guest_name": "另一个人",
                    "guest_wx": "client1",
                },
            )
        self.assertIn("已使用", str(ctx.exception))

    def test_guest_wx_mismatch(self):
        created = create_trial_code(
            self.conn,
            {"advisor_wx": "advisor1", "guest_wx": "client1"},
        )
        with self.assertRaises(ValueError) as ctx:
            claim_trial_code(
                self.conn,
                {
                    "code": created["code"],
                    "guest_name": "王五",
                    "guest_wx": "wrong_wx",
                },
            )
        self.assertIn("不匹配", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
