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
    get_trial_progress,
    list_trial_guests,
    login_trial,
    save_trial_progress,
)


class TrialApiTests(unittest.TestCase):
    def setUp(self):
        self.db = Path(tempfile.mkdtemp()) / "t.db"
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        ensure_trial_tables(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_create_requires_advisor(self):
        with self.assertRaises(ValueError):
            create_trial_code(self.conn, {"guest_wx": "b"})

    def test_system_code_is_identity(self):
        created = create_trial_code(
            self.conn,
            {"advisor_wx": "advisor1"},
        )
        code = created["code"]
        self.assertEqual(len(code), 8)
        self.assertEqual(created["days_valid"], 15)

        with self.assertRaises(ValueError) as ctx:
            claim_trial_code(self.conn, {"code": code})
        self.assertIn("姓名", str(ctx.exception))

        claim = claim_trial_code(
            self.conn,
            {"code": code, "guest_name": "王五", "target_score": 5.0},
        )
        self.assertEqual(claim["guest_name"], "王五")
        self.assertEqual(claim["days_left"], 15)
        self.assertFalse(claim["returning"])

        # 同一激活码再次进入 → 同一记录
        again = claim_trial_code(self.conn, {"code": code})
        self.assertTrue(again["returning"])
        self.assertEqual(again["guest_name"], "王五")
        self.assertEqual(again["code"], code)

        login = login_trial(self.conn, {"code": code})
        self.assertEqual(login["code"], code)

    def test_each_create_new_code(self):
        a = create_trial_code(self.conn, {"advisor_wx": "advisor1"})
        b = create_trial_code(self.conn, {"advisor_wx": "advisor1"})
        self.assertNotEqual(a["code"], b["code"])

    def test_invalid_code(self):
        with self.assertRaises(ValueError) as ctx:
            claim_trial_code(
                self.conn,
                {"code": "NOTEXIST", "guest_name": "王五"},
            )
        self.assertIn("无效", str(ctx.exception))

    def test_progress_tied_to_code(self):
        created = create_trial_code(self.conn, {"advisor_wx": "advisor1"})
        code = created["code"]
        claim_trial_code(
            self.conn,
            {"code": code, "guest_name": "王五"},
        )
        progress = {
            "groupStatus": ["completed", "pending", "pending"],
            "totalSecondsLearned": 120,
        }
        saved = save_trial_progress(
            self.conn,
            {
                "code": code,
                "module_type": "listening_basic",
                "progress": progress,
            },
        )
        self.assertTrue(saved["ok"])
        loaded = get_trial_progress(
            self.conn,
            {"code": code, "module_type": "listening_basic"},
        )
        self.assertEqual(loaded["progress"]["totalSecondsLearned"], 120)
        guests = list_trial_guests(self.conn)
        self.assertEqual(guests[0]["code"], code)
        self.assertEqual(guests[0]["listening_basic"]["groups_done"], 1)


if __name__ == "__main__":
    unittest.main()
