# -*- coding: utf-8 -*-
"""Unit tests for wecom_checkup (fake DBs; no G: drive dependency)."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from wecom_checkup import (  # noqa: E402
    extract_utf8_fragments,
    match_learning_groups,
    open_ro,
    pick_primary_group,
)


class WecomCheckupTests(unittest.TestCase):
    def test_extract_utf8_fragments_from_blob(self) -> None:
        # Mimic protobuf: noise bytes + UTF-8 Chinese
        blob = b"\x0a\xfe\x01\x08\x00" + "10.23打卡内容：任务一".encode("utf-8") + b"\x00\x01"
        text = extract_utf8_fragments(blob)
        self.assertIn("打卡内容", text)
        self.assertIn("任务一", text)

    def test_match_and_pick_primary_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "session.db"
            conn = sqlite3.connect(str(session))
            conn.execute(
                """
                CREATE TABLE conversation_table (
                    con_numeric_id INTEGER,
                    id TEXT,
                    name TEXT,
                    create_time INTEGER,
                    last_message_time INTEGER
                )
                """
            )
            conn.executemany(
                "INSERT INTO conversation_table VALUES (?,?,?,?,?)",
                [
                    (1, "R:1", "20260912雅思预备4班", 1, 100),
                    (2, "R:2", "宋知宸打卡群", 1, 200),
                    (3, "R:3", "丁笑冉宋知宸雅思一对二6.5学习群", 1, 300),
                    (4, "R:4", "无关群", 1, 400),
                ],
            )
            conn.commit()
            conn.close()

            sconn = open_ro(session)
            cands = match_learning_groups(sconn, "宋知宸")
            sconn.close()
            names = {c["name"] for c in cands}
            self.assertIn("宋知宸打卡群", names)
            self.assertIn("丁笑冉宋知宸雅思一对二6.5学习群", names)
            self.assertNotIn("20260912雅思预备4班", names)
            self.assertNotIn("无关群", names)

            primary, conf = pick_primary_group(cands)
            self.assertEqual(conf, "multi_pick_latest")
            assert primary is not None
            # 打卡群 gets a score boost over shared 学习群 even if older
            self.assertEqual(primary["name"], "宋知宸打卡群")

    def test_pick_unique(self) -> None:
        primary, conf = pick_primary_group(
            [{"conversation_id": "R:1", "name": "张三学习群", "last_message_time": 1}]
        )
        self.assertEqual(conf, "unique")
        assert primary is not None
        self.assertEqual(primary["name"], "张三学习群")

    def test_pick_none(self) -> None:
        primary, conf = pick_primary_group([])
        self.assertIsNone(primary)
        self.assertEqual(conf, "none")


if __name__ == "__main__":
    unittest.main()
