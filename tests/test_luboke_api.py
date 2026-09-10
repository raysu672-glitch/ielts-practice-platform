import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from luboke_api import get_course, load_courses, public_catalog, public_course, save_catalog  # noqa: E402


class LubokeApiTests(unittest.TestCase):
    def test_load_flat_catalog_into_reading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "courses.json"
            path.write_text(
                json.dumps(
                    {
                        "courses": [
                            {
                                "id": "cnj-1-1",
                                "title": "1-1 如何阅读长难句",
                                "duration": "20分钟",
                                "summary": "拆长难句",
                                "oss_key": "courses/测试1-1如何阅读长难句.mp4",
                            },
                            {
                                "id": "bad",
                                "title": "坏路径",
                                "oss_key": "../secret.mp4",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            courses = load_courses(path)
            self.assertEqual(len(courses), 1)
            self.assertEqual(courses[0]["subject_id"], "reading")
            public = public_course(courses[0])
            self.assertEqual(public["summary"], "拆长难句")
            self.assertNotIn("oss_key", public)
            self.assertEqual(get_course(courses, "cnj-1-1")["oss_key"], "courses/测试1-1如何阅读长难句.mp4")

    def test_teacher_can_add_custom_subject(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "saved.json"
            saved = save_catalog(
                {
                    "subjects": [
                        {
                            "name": "长难句",
                            "courses": [
                                {
                                    "title": "1-1 如何阅读长难句",
                                    "duration": "20分钟",
                                    "summary": "拆句子",
                                    "oss_key": "courses/a.mp4",
                                }
                            ],
                        },
                        {"name": "听力", "courses": []},
                    ]
                },
                path,
            )
            names = [s["name"] for s in saved["subjects"]]
            self.assertEqual(names, ["长难句", "听力"])
            self.assertTrue(saved["subjects"][0]["id"])
            public = public_catalog(saved)
            self.assertNotIn("oss_key", json.dumps(public))
            self.assertEqual(len(public["subjects"]), 2)

    def test_save_rejects_empty_subjects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "saved.json"
            with self.assertRaises(ValueError):
                save_catalog({"subjects": []}, path)

    def test_repo_catalog_loads(self) -> None:
        courses = load_courses()
        self.assertGreaterEqual(len(courses), 1)
        self.assertTrue(all(item["id"] and item["oss_key"] for item in courses))
        names = [s["name"] for s in public_catalog()["subjects"]]
        self.assertIn("阅读", names)


if __name__ == "__main__":
    unittest.main()
