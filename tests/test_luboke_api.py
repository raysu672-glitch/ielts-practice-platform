import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from luboke_api import (  # noqa: E402
    get_course,
    load_catalog,
    load_courses,
    public_catalog,
    public_course,
    save_catalog,
    teacher_catalog,
)


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

    def test_teacher_catalog_round_trip_keeps_oss_key(self) -> None:
        """管理页必须用 teacher_catalog 回填。

        学生端 public_catalog 不含 oss_key；若管理页用它回填，保存时 oss_key 为空，
        后端会把课程全部丢弃（曾导致线上课表被清空）。
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            save_catalog(
                {
                    "subjects": [
                        {
                            "name": "语法",
                            "courses": [
                                {"title": "一般现在时", "oss_key": "courses/初级中级语法/一般现在时.mp4"},
                                {"title": "被动语态", "oss_key": "courses/初级中级语法/被动语态.mp4"},
                            ],
                        }
                    ]
                },
                path,
            )

            full = teacher_catalog(load_catalog(path))
            courses = full["subjects"][0]["courses"]
            self.assertEqual(len(courses), 2)
            self.assertTrue(all(c["oss_key"] for c in courses))

            # 管理页原样提交 teacher_catalog 的数据，课程不能被丢掉
            resaved = save_catalog(full, path)
            self.assertEqual(len(resaved["subjects"][0]["courses"]), 2)

            # 反面用例：用 public_catalog 回填会丢 oss_key，保存即清空课程
            leaked = public_catalog(load_catalog(path))
            self.assertNotIn("oss_key", leaked["subjects"][0]["courses"][0])
            wiped = save_catalog(leaked, path)
            self.assertEqual(len(wiped["subjects"][0]["courses"]), 0)

    def test_repo_catalog_loads(self) -> None:
        courses = load_courses()
        self.assertGreaterEqual(len(courses), 1)
        self.assertTrue(all(item["id"] and item["oss_key"] for item in courses))
        names = [s["name"] for s in public_catalog()["subjects"]]
        self.assertIn("阅读", names)


if __name__ == "__main__":
    unittest.main()
