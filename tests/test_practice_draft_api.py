"""作文批改：未完成进度草稿 API（需 writing backend 依赖时才跑 HTTP 测）。"""

from __future__ import annotations

import importlib.util
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "sources" / "xiezuopigai" / "ielts-writing-backend"
_HAS_WRITING_DEPS = all(
    importlib.util.find_spec(name) is not None for name in ("httpx", "fastapi", "dotenv")
)


class PracticeDraftSchemaTests(unittest.TestCase):
    """不依赖 fastapi/httpx：校验草稿表可建、可读写。"""

    def test_draft_table_crud(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "draft.db"
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS practice_drafts (
                    student_id TEXT PRIMARY KEY,
                    student_name TEXT DEFAULT '',
                    payload TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            c.execute(
                """
                INSERT INTO practice_drafts (student_id, student_name, payload)
                VALUES (?, ?, ?)
                """,
                ("2025001", "测试生", '{"answers":{"0-0":"has"}}'),
            )
            conn.commit()
            row = c.execute(
                "SELECT payload FROM practice_drafts WHERE student_id = ?",
                ("2025001",),
            ).fetchone()
            self.assertIsNotNone(row)
            self.assertIn("has", row[0])
            c.execute("DELETE FROM practice_drafts WHERE student_id = ?", ("2025001",))
            conn.commit()
            self.assertIsNone(
                c.execute(
                    "SELECT 1 FROM practice_drafts WHERE student_id = ?",
                    ("2025001",),
                ).fetchone()
            )
            conn.close()


@unittest.skipUnless(_HAS_WRITING_DEPS, "writing backend deps (httpx/fastapi/dotenv) not installed")
class PracticeDraftApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmpdir = tempfile.TemporaryDirectory()
        os.environ["PORT"] = "18080"
        cls._db = Path(cls._tmpdir.name) / "draft_test.db"
        sys.path.insert(0, str(BACKEND))
        import main as backend_main  # noqa: E402

        backend_main.DB_PATH = str(cls._db)
        backend_main.init_db()
        cls.main = backend_main
        from fastapi.testclient import TestClient  # noqa: E402

        cls.client = TestClient(backend_main.app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmpdir.cleanup()

    def test_save_get_delete_draft(self) -> None:
        payload = {
            "studentId": "2025001",
            "studentName": "测试生",
            "payload": {
                "studentId": "2025001",
                "aiSupplementDone": True,
                "sentences": [{"text": "Hello.", "checkpoints": []}],
                "done": ["0-0"],
                "verdicts": {"0-0": "correct"},
                "answers": {"0-0": "has"},
            },
        }
        save = self.client.post("/api/save-draft", json=payload)
        self.assertEqual(save.status_code, 200)
        self.assertTrue(save.json().get("success"))

        got = self.client.get("/api/student/draft", params={"studentId": "2025001"})
        self.assertEqual(got.status_code, 200)
        body = got.json()
        self.assertTrue(body.get("success"))
        self.assertIsNotNone(body.get("data"))
        self.assertEqual(body["data"]["payload"]["answers"]["0-0"], "has")

        deleted = self.client.delete("/api/student/draft", params={"studentId": "2025001"})
        self.assertEqual(deleted.status_code, 200)
        self.assertTrue(deleted.json().get("success"))

        empty = self.client.get("/api/student/draft", params={"studentId": "2025001"})
        self.assertIsNone(empty.json().get("data"))

    def test_missing_student_id(self) -> None:
        bad = self.client.post("/api/save-draft", json={"studentId": "", "payload": {"a": 1}})
        self.assertEqual(bad.status_code, 400)


if __name__ == "__main__":
    unittest.main()
