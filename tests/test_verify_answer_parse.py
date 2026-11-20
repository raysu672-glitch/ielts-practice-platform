"""作文批改：AI 答案复核 JSON 解析。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "sources" / "xiezuopigai" / "ielts-writing-backend"
sys.path.insert(0, str(BACKEND))

from verify_parse import parse_verify_answer_content  # noqa: E402


class VerifyAnswerParseTests(unittest.TestCase):
    def test_plain_json(self) -> None:
        data = parse_verify_answer_content('{"correct": true, "reason": "短语等价"}')
        self.assertEqual(data, {"correct": True, "reason": "短语等价"})

    def test_false_and_string_bool(self) -> None:
        data = parse_verify_answer_content('{"correct": false, "reason": "仍含原错"}')
        self.assertEqual(data["correct"], False)
        data2 = parse_verify_answer_content('{"correct": "yes", "reason": "ok"}')
        self.assertTrue(data2["correct"])

    def test_markdown_fence(self) -> None:
        raw = '```json\n{"correct": true, "reason": "少虚词可接受"}\n```'
        data = parse_verify_answer_content(raw)
        self.assertTrue(data["correct"])

    def test_empty(self) -> None:
        self.assertIsNone(parse_verify_answer_content(""))
        self.assertIsNone(parse_verify_answer_content("not json"))


if __name__ == "__main__":
    unittest.main()
