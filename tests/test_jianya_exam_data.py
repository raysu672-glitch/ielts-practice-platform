"""剑雅真题题库目录与路径安全。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from local_server import LocalHandler, build_jianya_catalog  # noqa: E402


class JianyaCatalogTests(unittest.TestCase):
    def test_catalog_lists_academic_books_newest_first(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "academic20").mkdir()
            (root / "academic21").mkdir()
            (root / "academic21" / "manifest.json").write_text(
                json.dumps({"label": "ACADEMIC 21", "scrapedAt": "2026-08-28"}),
                encoding="utf-8",
            )
            (root / "notes").mkdir()
            data = build_jianya_catalog(root)
            ids = [row["bookId"] for row in data["books"]]
            self.assertEqual(ids, [21, 20])
            self.assertEqual(data["books"][0]["label"], "ACADEMIC 21")

    def test_exam_data_rejects_path_escape(self) -> None:
        handler = LocalHandler.__new__(LocalHandler)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "safe.json").write_text("{}", encoding="utf-8")
            escaped = handler._safe_under(root, "../safe.json")
            self.assertIsNone(escaped)
            inside = handler._safe_under(root, "safe.json")
            self.assertEqual(inside, (root / "safe.json").resolve())


if __name__ == "__main__":
    unittest.main()
