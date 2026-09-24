"""Unit tests for task system MVP (boxing, tomorrow生效, progress X/Y)."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from task_api import (  # noqa: E402
    PACK_MODE_TIME_BUDGET,
    PACK_MODE_UNITS_PER_DAY,
    STAGE_TEST_ATTENTION_FAILS,
    SHANGHAI,
    GENDU_DAILY_PRACTICES,
    GENDU_MODULE,
    GENDU_PASS_SCORE,
    _interleave_by_module,
    _plan_progress_brief,
    _profile_has_real_pending,
    _profile_pending_due,
    _student_overview_row,
    _gendu_day_practice_count,
    apply_draft_to_live,
    backlog_plan_item_ids,
    build_daily_tasks,
    catalog_unit_progress_for_student,
    ensure_active_plan_daily_tasks,
    china_ymd,
    class_overview,
    clear_gendu_assignment,
    clear_plan_pause,
    complete_study,
    ensure_module_quota,
    ensure_task_tables,
    ensure_time_profile,
    get_gendu_assignment,
    get_plan,
    get_today,
    insert_stage_test,
    is_weekend,
    LISTENING_GENDU_LESSONS,
    maybe_apply_pending_for_today,
    normalize_stage_test_positions,
    preview_daily_pack_items,
    put_gendu_assignment,
    put_plan_draft,
    put_plan_pause,
    put_time_profile,
    report_gendu_practice,
    seed_mvp_units,
    stage_tests_pending,
    submit_stage_test,
    day_task_progress,
    day_unfinished_count,
    update_scope_progress,
)


def _recent_weekday() -> str:
    """返回一个确定的工作日（若今天是周末则回退到周五）。

    部分排程用例断言的是工作日预算，直接用「今天」会在周末跑到
    weekend_minutes 分支而必然失败；这里让用例与运行当天的星期解耦。
    """
    day = datetime.strptime(china_ymd(), "%Y-%m-%d")
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day.strftime("%Y-%m-%d")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL DEFAULT 'x',
            target_score REAL DEFAULT 6.5,
            status TEXT DEFAULT 'active'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE test_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT DEFAULT 'dictation',
            module_name TEXT DEFAULT '',
            test_type TEXT NOT NULL DEFAULT 'module_test',
            score REAL NOT NULL,
            correct_count INTEGER NOT NULL DEFAULT 0,
            total_count INTEGER NOT NULL DEFAULT 0,
            is_passed INTEGER NOT NULL,
            pass_threshold REAL NOT NULL,
            duration_seconds INTEGER DEFAULT 0,
            details TEXT DEFAULT '[]',
            started_at TEXT,
            ended_at TEXT,
            created_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_type TEXT NOT NULL,
            module_name TEXT,
            session_kind TEXT DEFAULT 'study',
            words_tested INTEGER DEFAULT 0,
            initial_correct INTEGER DEFAULT 0,
            initial_wrong INTEGER DEFAULT 0,
            groups_completed INTEGER DEFAULT 0,
            plan_item_id INTEGER,
            unit_id TEXT,
            score_percent REAL,
            duration_seconds INTEGER NOT NULL DEFAULT 0,
            details TEXT DEFAULT '[]',
            started_at TEXT,
            ended_at TEXT,
            created_at TEXT
        )
        """
    )
    conn.execute(
        "INSERT INTO students (student_id, name) VALUES ('2025001', '测试生')"
    )
    ensure_task_tables(conn)
    seed_mvp_units(conn)
    return conn


class TaskApiTests(unittest.TestCase):
    def test_seed_counts(self) -> None:
        conn = _connect()
        expected = {
            "reading_synonym": 23,
            "dictation": 50,
            "listening_basic": 41,
            "listening_synonym": 24,
            "sentence": 12,
            "writing_phrase": 28,
            "writing_translate": 23,
            "listening_p4_speed": 24,
            "speaking_complex": 17,
            "speaking_p1": 24,
            "speaking_p2_material": 8,
            "speaking_p2_apply": 12,
        }
        for mt, n in expected.items():
            got = conn.execute(
                "SELECT COUNT(*) AS c FROM task_units WHERE module_type=?", (mt,)
            ).fetchone()["c"]
            self.assertEqual(got, n, mt)
        self.assertEqual(len(LISTENING_GENDU_LESSONS), 24)
        codes = [code for _, code, _ in LISTENING_GENDU_LESSONS]
        self.assertEqual(len(set(codes)), 24)
        lessons_js = (Path(__file__).resolve().parents[1] / "sources" / "P4gendu" / "lessons-data.js").read_text(encoding="utf-8")
        for code in codes:
            self.assertIn(f'"code": "{code}"', lessons_js)
        modules_js = (Path(__file__).resolve().parents[1] / "sources" / "tinglidanciceshi" / "js" / "modules.js").read_text(encoding="utf-8")
        self.assertIn("id: 'listening_p4_speed'", modules_js)
        # 测试页必须是会回传分数的 P4genduceshi：
        # P4gendu 只练不判分、不做任何 postMessage 上报，用它当阶段测会导致学生做完也交不上
        self.assertIn("test_url: '../P4genduceshi/index.html'", modules_js)
        self.assertIn("targets: { 6: 70, 6.5: 80, 7: 90 }", modules_js)
        self.assertNotRegex(
            modules_js,
            r"id: 'listening_p4_speed'[\s\S]{0,280}study_only:\s*true",
        )
        self.assertEqual(
            conn.execute(
                "SELECT study_url FROM task_units WHERE unit_id='listening_p4_u01'"
            ).fetchone()["study_url"],
            "../P4genduceshi/index.html?lessonId=C4T1S4&part=p4",
        )
        self.assertEqual(
            conn.execute(
                "SELECT COUNT(*) AS c FROM task_units WHERE module_type='writing_correction'"
            ).fetchone()["c"],
            0,
        )
        u23 = conn.execute(
            "SELECT content_ref FROM task_units WHERE unit_id='reading_synonym_u23'"
        ).fetchone()
        self.assertIn('"scope_total": 5', u23["content_ref"])
        self.assertEqual(
            conn.execute(
                "SELECT parent_module FROM task_units WHERE unit_id='speaking_p1_u01'"
            ).fetchone()["parent_module"],
            "speaking",
        )
    def test_plan_progress_xy(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {"item_type": "study", "unit_id": "reading_synonym_u03"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        prog = get_plan(conn, "2025001")["progress"]["reading_synonym"]
        self.assertEqual(prog["study_y"], 3)
        self.assertEqual(prog["study_x"], 0)
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='reading_synonym_u01'"
        ).fetchone()
        update_scope_progress(conn, "2025001", item["id"], scope_done=10)
        complete_study(conn, "2025001", item["id"], "1")
        prog = get_plan(conn, "2025001")["progress"]["reading_synonym"]
        self.assertEqual(prog["study_x"], 1)
        self.assertEqual(prog["study_y"], 3)

    def test_catalog_unit_progress_uses_task_units_total(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='reading_synonym_u01'"
        ).fetchone()
        update_scope_progress(conn, "2025001", item["id"], scope_done=10)
        complete_study(conn, "2025001", item["id"], "1")
        cat = catalog_unit_progress_for_student(conn, "2025001")["reading_synonym"]
        catalog_total = conn.execute(
            "SELECT COUNT(*) AS c FROM task_units WHERE is_active=1 AND module_type='reading_synonym'"
        ).fetchone()["c"]
        self.assertEqual(cat["done"], 1)
        self.assertEqual(cat["total"], catalog_total)
        self.assertGreater(cat["total"], 2)

    def test_complete_study_requires_reading_scope(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='reading_synonym_u01'"
        ).fetchone()
        with self.assertRaises(ValueError):
            complete_study(conn, "2025001", item["id"], "1")
        update_scope_progress(conn, "2025001", item["id"], scope_done=10)
        complete_study(conn, "2025001", item["id"], "1")

    def test_complete_study_requires_translate_and_sentence_scope(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "writing_translate_u01"},
                {"item_type": "study", "unit_id": "sentence_u01"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        for unit_id in ("writing_translate_u01", "sentence_u01"):
            item = conn.execute(
                "SELECT id FROM plan_items WHERE unit_id=?", (unit_id,)
            ).fetchone()
            with self.assertRaises(ValueError):
                complete_study(conn, "2025001", item["id"], "1")
            unit = conn.execute(
                "SELECT content_ref FROM task_units WHERE unit_id=?", (unit_id,)
            ).fetchone()
            ref = unit["content_ref"]
            if isinstance(ref, str):
                import json as _json

                ref = _json.loads(ref)
            total = int((ref or {}).get("scope_total") or 0)
            self.assertGreater(total, 0)
            update_scope_progress(conn, "2025001", item["id"], scope_done=total)
            complete_study(conn, "2025001", item["id"], "1")

    def test_complete_study_requires_scope_for_all_scoped_modules(self) -> None:
        """所有带 scope_total 的科目（跟读除外）未做满不能打勾。"""
        conn = _connect()
        samples = (
            "dictation_u01",
            "listening_basic_u01",
            "listening_synonym_u01",
            "writing_phrase_u01",
            "speaking_p1_u01",
        )
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": uid} for uid in samples],
        )
        apply_draft_to_live(conn, "2025001")
        for unit_id in samples:
            item = conn.execute(
                "SELECT id FROM plan_items WHERE unit_id=?", (unit_id,)
            ).fetchone()
            self.assertIsNotNone(item, unit_id)
            with self.assertRaises(ValueError, msg=unit_id):
                complete_study(conn, "2025001", item["id"], "1")
            unit = conn.execute(
                "SELECT content_ref FROM task_units WHERE unit_id=?", (unit_id,)
            ).fetchone()
            ref = unit["content_ref"]
            if isinstance(ref, str):
                import json as _json

                ref = _json.loads(ref)
            total = int((ref or {}).get("scope_total") or 0)
            self.assertGreater(total, 0, unit_id)
            complete_study(conn, "2025001", item["id"], "1", scope_done=total)
    def test_duplicate_unit_rejected(self) -> None:
        conn = _connect()
        with self.assertRaises(ValueError):
            put_plan_draft(
                conn,
                "2025001",
                [
                    {"item_type": "study", "unit_id": "reading_synonym_u01"},
                    {"item_type": "study", "unit_id": "reading_synonym_u01"},
                ],
            )

    def test_boxing_respects_budget(self) -> None:
        conn = _connect()
        items = [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 9)]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        put_time_profile(
            conn, "2025001", {"weekday_minutes": 40, "weekend_minutes": 40, "effective": "today"}
        )
        self._backdate_plan_start(conn, "2026-08-01")
        # Force a weekday date
        weekday = "2026-08-26"  # Wednesday
        daily = build_daily_tasks(conn, "2025001", weekday)
        # 40 * 1.15 = 46; each reading unit 15 → at most 3
        self.assertGreaterEqual(len(daily), 1)
        self.assertLessEqual(len(daily), 4)
        total_est = sum(d["est_minutes"] for d in daily)
        self.assertLessEqual(total_est, 46 + 15)  # first oversize still allowed

    def test_profile_pending_tomorrow(self) -> None:
        conn = _connect()
        put_time_profile(conn, "2025001", {"weekday_minutes": 20})
        row = conn.execute(
            "SELECT * FROM student_time_profiles WHERE student_id='2025001'"
        ).fetchone()
        self.assertEqual(row["weekday_minutes"], 40)
        self.assertEqual(row["pending_weekday_minutes"], 20)

    def test_draft_does_not_change_locked_today(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        day = "2026-08-26"
        first = build_daily_tasks(conn, "2025001", day)
        self.assertTrue(first)
        ids_before = [x["plan_item_id"] for x in first]
        # Change draft (add more) — today already locked, rebuild returns same
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {"item_type": "study", "unit_id": "dictation_u01"},
            ],
        )
        second = build_daily_tasks(conn, "2025001", day)
        self.assertEqual([x["plan_item_id"] for x in second], ids_before)

    def test_stage_test_done_fail_not_complete(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()
        # Put only the test into today by completing study first then packing
        study = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='study'"
        ).fetchone()
        update_scope_progress(conn, "2025001", study["id"], scope_done=10)
        complete_study(conn, "2025001", study["id"], "1")
        day = china_ymd()
        # Force insert daily for test
        conn.execute(
            """
            INSERT OR IGNORE INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 1)
            """,
            (day, test_item["id"]),
        )
        result = submit_stage_test(
            conn, "2025001", test_item["id"], score=50, threshold=80
        )
        self.assertFalse(result["passed"])
        daily = conn.execute(
            "SELECT state FROM daily_tasks WHERE plan_item_id=?", (test_item["id"],)
        ).fetchone()
        self.assertEqual(daily["state"], "done_fail")
        # stage_test in test_records
        rec = conn.execute(
            "SELECT test_type FROM test_records WHERE student_id='2025001'"
        ).fetchone()
        self.assertEqual(rec["test_type"], "stage_test")

    def test_stage_test_pass_backfills_history_rows(self) -> None:
        """阶段测通过后，历史未完成日任务行必须一起回写为 done_pass。

        否则「昨天没做、今天补过」的行会永远停在 todo，教师看板的
        「昨日完成度」在补做当天误报未完成（与 complete_study 口径不一致）。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()
        study = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='study'"
        ).fetchone()
        update_scope_progress(conn, "2025001", study["id"], scope_done=10)
        complete_study(conn, "2025001", study["id"], "1")

        today = china_ymd()
        yday = (
            datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        for i, d in enumerate((yday, today)):
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked)
                VALUES ('2025001', ?, ?, 'carry_over', ?, 'todo', 1)
                """,
                (d, test_item["id"], i),
            )
        conn.commit()

        result = submit_stage_test(
            conn, "2025001", test_item["id"], score=90, threshold=80
        )
        self.assertTrue(result["passed"])
        states = [
            r["state"]
            for r in conn.execute(
                "SELECT state FROM daily_tasks WHERE plan_item_id=? ORDER BY task_date",
                (test_item["id"],),
            ).fetchall()
        ]
        self.assertEqual(states, ["done_pass", "done_pass"])

    def test_complete_study_keeps_older_skip_days_untouched(self) -> None:
        """断更日不能被回写洗白：只回写「今天 + 昨天」。

        线上 2025046 于 09-06 看板显示 3/3、真实 0/3，就是无 task_date 限制的
        回写把学生没打开 App 的日子一并改成了已完成，教师看板因此系统性虚高。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        study = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='study'"
        ).fetchone()
        update_scope_progress(conn, "2025001", study["id"], scope_done=10)

        today = china_ymd()
        base = datetime.strptime(today, "%Y-%m-%d")
        skip = (base - timedelta(days=3)).strftime("%Y-%m-%d")
        yday = (base - timedelta(days=1)).strftime("%Y-%m-%d")
        for i, d in enumerate((skip, yday, today)):
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked)
                VALUES ('2025001', ?, ?, 'carry_over', ?, 'todo', 1)
                """,
                (d, study["id"], i),
            )
        conn.commit()

        complete_study(conn, "2025001", study["id"], "1")

        got = {
            r["task_date"]: r["state"]
            for r in conn.execute(
                "SELECT task_date, state FROM daily_tasks WHERE plan_item_id=?",
                (study["id"],),
            ).fetchall()
        }
        self.assertEqual(got[skip], "todo")
        self.assertEqual(got[yday], "done_study")
        self.assertEqual(got[today], "done_study")

    def test_stage_test_pass_keeps_older_skip_days_untouched(self) -> None:
        """阶段测通过同样只回写「今天 + 昨天」，不得洗白更早的断更日。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()
        study = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='study'"
        ).fetchone()
        update_scope_progress(conn, "2025001", study["id"], scope_done=10)
        complete_study(conn, "2025001", study["id"], "1")

        today = china_ymd()
        base = datetime.strptime(today, "%Y-%m-%d")
        skip = (base - timedelta(days=5)).strftime("%Y-%m-%d")
        yday = (base - timedelta(days=1)).strftime("%Y-%m-%d")
        for i, d in enumerate((skip, yday, today)):
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked)
                VALUES ('2025001', ?, ?, 'carry_over', ?, 'todo', 1)
                """,
                (d, test_item["id"], i),
            )
        conn.commit()

        result = submit_stage_test(
            conn, "2025001", test_item["id"], score=90, threshold=80
        )
        self.assertTrue(result["passed"])
        got = {
            r["task_date"]: r["state"]
            for r in conn.execute(
                "SELECT task_date, state FROM daily_tasks WHERE plan_item_id=?",
                (test_item["id"],),
            ).fetchall()
        }
        self.assertEqual(got[skip], "todo")
        self.assertEqual(got[yday], "done_pass")
        self.assertEqual(got[today], "done_pass")

    def test_passed_stage_test_is_not_downgraded_by_later_failure(self) -> None:
        """已通过的阶段测，换天重考考砸不得把 test_passed 打回 0。

        这个场景是可达的：换天后 test_attempt_count_today 归零，
        `attempts >= 2` 那道门槛拦不住再次提交。一旦降级，条目会从「已完成」
        变回未完成、任务复活并重新计入积压，教师看板完成度还会倒退。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()

        first = submit_stage_test(
            conn, "2025001", test_item["id"], score=95, threshold=80
        )
        self.assertTrue(first["passed"])
        self.assertFalse(first["already_passed"])

        # 模拟「换了一天」：把今日次数清零，绕开重测上限
        conn.execute(
            "UPDATE plan_items SET test_attempt_ymd='2000-01-01' WHERE id=?",
            (test_item["id"],),
        )
        conn.commit()

        second = submit_stage_test(
            conn, "2025001", test_item["id"], score=10, threshold=80
        )
        self.assertTrue(second["passed"], "生效结果应保持通过")
        self.assertTrue(second["already_passed"])

        row = conn.execute(
            "SELECT test_passed FROM plan_items WHERE id=?", (test_item["id"],)
        ).fetchone()
        self.assertEqual(int(row["test_passed"]), 1, "计划状态不得被降级")

        # 但 test_records 要如实记下这一次是失败的
        last = conn.execute(
            "SELECT is_passed FROM test_records ORDER BY id DESC LIMIT 1"
        ).fetchone()
        self.assertEqual(int(last["is_passed"]), 0)

    def test_stage_test_records_carry_test_page_details(self) -> None:
        """阶段测的题数 / 用时来自测试页真实判分，必须如实落进 test_records。

        之前 correct_count / total_count 被写死 0，阶段测记录看不出做了多少题、
        用了多久；同时前端不再重复写一条 module_test，否则一次测试算两次、
        看板「总测试次数」会虚高。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()

        submit_stage_test(
            conn,
            "2025001",
            test_item["id"],
            score=41,
            threshold=80,
            correct_count=20,
            total_count=49,
            duration_seconds=375,
        )
        row = conn.execute(
            """
            SELECT test_type, score, correct_count, total_count, duration_seconds,
                   is_passed, pass_threshold
            FROM test_records ORDER BY id DESC LIMIT 1
            """
        ).fetchone()
        self.assertEqual(row["test_type"], "stage_test")
        self.assertAlmostEqual(float(row["score"]), 41.0)
        self.assertEqual(int(row["correct_count"]), 20)
        self.assertEqual(int(row["total_count"]), 49)
        self.assertEqual(int(row["duration_seconds"]), 375)
        self.assertEqual(int(row["is_passed"]), 0)
        self.assertAlmostEqual(float(row["pass_threshold"]), 80.0)

    def test_stage_test_clamps_negative_detail_counts(self) -> None:
        """负数明细（前端被篡改）不得写进库，一律回落到 0。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                    "est_minutes": 20,
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_item = conn.execute(
            "SELECT id FROM plan_items WHERE item_type='test'"
        ).fetchone()

        submit_stage_test(
            conn,
            "2025001",
            test_item["id"],
            score=90,
            threshold=80,
            correct_count=-5,
            total_count=-1,
            duration_seconds=-100,
        )
        row = conn.execute(
            """
            SELECT correct_count, total_count, duration_seconds
            FROM test_records ORDER BY id DESC LIMIT 1
            """
        ).fetchone()
        self.assertEqual(int(row["correct_count"]), 0)
        self.assertEqual(int(row["total_count"]), 0)
        self.assertEqual(int(row["duration_seconds"]), 0)

    def test_backlog_excludes_paused_module(self) -> None:
        """配额被设为 0 的模块（助教暂停）不计积压；配额恢复后重新计入。

        否则这些条目既不会被派发、又永远清不掉，看板和教师端会一直标红
        （线上 2025066 有 29 条这种「假积压」）。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "speaking_p1_u01"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        spk = conn.execute(
            "SELECT id, module_type FROM plan_items "
            "WHERE item_type='study' AND unit_id='speaking_p1_u01'"
        ).fetchone()
        rs = conn.execute(
            "SELECT id FROM plan_items "
            "WHERE item_type='study' AND unit_id='reading_synonym_u01'"
        ).fetchone()
        spk_pid, spk_mt = int(spk["id"]), str(spk["module_type"])
        rs_pid = int(rs["id"])
        self.assertNotEqual(spk_mt, "reading_synonym")

        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    },
                    {"module_type": spk_mt, "weekday_units": 1, "weekend_units": 1},
                ],
                "effective": "today",
            },
        )
        today = china_ymd()
        yday = (
            datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        self._backdate_plan_start(conn, yday)
        for i, pid in enumerate((rs_pid, spk_pid)):
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class,
                 sort_in_day, state, locked)
                VALUES ('2025001', ?, ?, 'fresh', ?, 'todo', 1)
                """,
                (yday, pid, i),
            )
        conn.commit()
        self.assertEqual(
            set(backlog_plan_item_ids(conn, "2025001", before_date=today)),
            {rs_pid, spk_pid},
        )

        # 助教把该模块配额改成 0 = 暂停
        conn.execute(
            "UPDATE student_module_daily_quota SET weekday_units=0, weekend_units=0 "
            "WHERE student_id='2025001' AND module_type=?",
            (spk_mt,),
        )
        conn.commit()
        paused = set(backlog_plan_item_ids(conn, "2025001", before_date=today))
        self.assertNotIn(spk_pid, paused)
        self.assertIn(rs_pid, paused)

        # 配额恢复 → 重新计入
        conn.execute(
            "UPDATE student_module_daily_quota SET weekday_units=1, weekend_units=1 "
            "WHERE student_id='2025001' AND module_type=?",
            (spk_mt,),
        )
        conn.commit()
        self.assertIn(
            spk_pid, set(backlog_plan_item_ids(conn, "2025001", before_date=today))
        )

    def test_china_ymd_uses_shanghai(self) -> None:
        # Sanity: function returns YYYY-MM-DD
        ymd = china_ymd()
        self.assertRegex(ymd, r"^\d{4}-\d{2}-\d{2}$")
        now_sh = datetime.now(SHANGHAI).strftime("%Y-%m-%d")
        self.assertEqual(ymd, now_sh)

    def test_first_plan_applies_immediately(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        live = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live, 1)

    def test_first_plan_explicit_tomorrow_stays_draft(self) -> None:
        """Teacher chose 明天生效 on an empty live plan — no tasks until that day."""
        conn = _connect()
        tomorrow = (datetime.now(SHANGHAI) + timedelta(days=1)).strftime("%Y-%m-%d")
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
            effective_from=tomorrow,
        )
        live = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live, 0)
        plan = get_plan(conn, "2025001")
        self.assertTrue(plan["pending_plan_change"])
        self.assertEqual(plan["draft_effective_from"], tomorrow)
        daily = build_daily_tasks(conn, "2025001", china_ymd())
        self.assertEqual(daily, [])
        live_after = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live_after, 0)

    def test_draft_applies_next_day_only(self) -> None:
        conn = _connect()
        # Seed live first
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        # Second edit → draft pending until tomorrow
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
        )
        day1 = china_ymd()
        build_daily_tasks(conn, "2025001", day1)
        live = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live, 1)  # still first plan
        tomorrow = (datetime.now(SHANGHAI) + timedelta(days=1)).strftime("%Y-%m-%d")
        # Clear today's locked so next-day boxing can apply draft
        conn.execute("DELETE FROM daily_tasks WHERE student_id='2025001'")
        conn.commit()
        build_daily_tasks(conn, "2025001", tomorrow)
        live2 = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live2, 2)

    def test_today_actual_minutes_from_study_sessions(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "dictation_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        day = "2026-08-26"
        plan_item = conn.execute(
            "SELECT id FROM plan_items WHERE student_id='2025001' LIMIT 1"
        ).fetchone()
        conn.execute(
            """
            INSERT INTO study_sessions (
                student_id, module_type, session_kind, duration_seconds,
                plan_item_id, unit_id, ended_at, created_at
            ) VALUES ('2025001', 'dictation', 'study', 900, ?, 'dictation_u01', ?, ?)
            """,
            (plan_item["id"], f"{day}T10:00:00+08:00", f"{day}T10:00:00+08:00"),
        )
        conn.execute(
            """
            INSERT INTO study_sessions (
                student_id, module_type, session_kind, duration_seconds,
                ended_at, created_at
            ) VALUES ('2025001', 'dictation', 'study', 300, ?, ?)
            """,
            (f"{day}T11:00:00+08:00", f"{day}T11:00:00+08:00"),
        )
        conn.commit()

        from task_api import sum_today_study_by_plan_item, sum_today_study_seconds

        total = sum_today_study_seconds(conn, "2025001", day)
        self.assertEqual(total, 1200)
        by_item = sum_today_study_by_plan_item(conn, "2025001", day)
        self.assertEqual(by_item[int(plan_item["id"])], 900)

    def test_multi_module_balanced_boxing(self) -> None:
        conn = _connect()
        # Teacher adds all dictation first, then reading — old behavior would pack dict-only
        items = (
            [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 4)]
            + [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 3)]
        )
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        # 两科各 2 单元/天：配额相等时应当交替出题，而不是排完 dictation 再排 reading
        put_time_profile(
            conn,
            "2025001",
            {
                "effective": "today",
                "module_quotas": [
                    {"module_type": "dictation", "weekday_units": 2, "weekend_units": 2},
                    {"module_type": "reading_synonym", "weekday_units": 2, "weekend_units": 2},
                ],
            },
        )
        self._backdate_plan_start(conn, "2026-08-01")
        day = "2026-08-26"
        daily = build_daily_tasks(conn, "2025001", day)
        module_seq = []
        for d in daily:
            row = conn.execute(
                "SELECT module_type FROM plan_items WHERE id=?",
                (d["plan_item_id"],),
            ).fetchone()
            module_seq.append(row["module_type"])
        self.assertEqual(len(module_seq), 4)
        # 首条仍来自最早加入的模块块（dictation 先加），其后两科交替
        self.assertEqual(module_seq[0], "dictation")
        self.assertNotEqual(module_seq[0], module_seq[1])
        self.assertNotEqual(module_seq[1], module_seq[2])

    def test_interleave_single_module_unchanged(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 4)],
        )
        apply_draft_to_live(conn, "2025001")
        rows = conn.execute(
            "SELECT * FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        items = [dict(r) for r in rows]
        ordered = _interleave_by_module(items)
        self.assertEqual([x["unit_id"] for x in ordered], [x["unit_id"] for x in items])

    def test_insert_stage_test_after_units_not_at_end(self) -> None:
        conn = _connect()
        items = (
            [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 4)]
            + [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 4)]
        )
        put_plan_draft(conn, "2025001", items)
        insert_stage_test(
            conn,
            "2025001",
            unit_ids=["reading_synonym_u01", "reading_synonym_u02", "reading_synonym_u03"],
        )
        draft = conn.execute(
            "SELECT item_type, unit_id, test_unit_ids, sort_order FROM plan_items_draft WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        types = [r["item_type"] for r in draft]
        test_idx = types.index("test")
        read_idxs = [i for i, r in enumerate(draft) if r["unit_id"] and r["unit_id"].startswith("reading")]
        self.assertGreater(test_idx, max(read_idxs))

    def test_normalize_stage_test_moves_test_after_study(self) -> None:
        items = [
            {"item_type": "study", "unit_id": "reading_synonym_u01", "test_unit_ids": []},
            {"item_type": "test", "unit_id": None, "test_unit_ids": ["reading_synonym_u02", "reading_synonym_u03"]},
            {"item_type": "study", "unit_id": "reading_synonym_u02", "test_unit_ids": []},
            {"item_type": "study", "unit_id": "reading_synonym_u03", "test_unit_ids": []},
        ]
        fixed = normalize_stage_test_positions(items)
        test_idx = next(i for i, x in enumerate(fixed) if x["item_type"] == "test")
        self.assertEqual(test_idx, 3)

    def test_normalize_stage_test_multi_segment_and_dedupe(self) -> None:
        items = (
            [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 4)]
            + [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 4)]
            + [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(4, 7)]
            + [
                {
                    "item_type": "test",
                    "test_unit_ids": ["reading_synonym_u04", "reading_synonym_u05", "reading_synonym_u06"],
                    "test_title": "4-6测",
                },
                {
                    "item_type": "test",
                    "test_unit_ids": ["reading_synonym_u04", "reading_synonym_u05", "reading_synonym_u06"],
                    "test_title": "4-6测重复",
                },
                {
                    "item_type": "test",
                    "test_unit_ids": ["reading_synonym_u01", "reading_synonym_u02", "reading_synonym_u03"],
                    "test_title": "1-3测",
                },
            ]
        )
        fixed = normalize_stage_test_positions(items)
        tests = [x for x in fixed if x["item_type"] == "test"]
        self.assertEqual(len(tests), 2)
        idx13 = fixed.index(tests[0]) if tests[0]["test_title"] == "1-3测" else fixed.index(tests[1])
        idx46 = fixed.index(tests[0]) if tests[0]["test_title"] == "4-6测" else fixed.index(tests[1])
        u3 = next(i for i, x in enumerate(fixed) if x.get("unit_id") == "reading_synonym_u03")
        u6 = next(i for i, x in enumerate(fixed) if x.get("unit_id") == "reading_synonym_u06")
        self.assertEqual(idx13, u3 + 1)
        self.assertEqual(idx46, u6 + 1)
        self.assertLess(idx13, idx46)

    def test_preview_daily_pack_items_unsaved_draft(self) -> None:
        conn = _connect()
        put_time_profile(
            conn, "2025001", {"weekday_minutes": 90, "weekend_minutes": 90, "effective": "today"}
        )
        items = (
            [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 4)]
            + [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 3)]
        )
        preview = preview_daily_pack_items(conn, "2025001", items)
        self.assertGreaterEqual(len(preview["items"]), 2)
        self.assertTrue(preview["rotated"])

    def test_custom_draft_effective_from(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        future = (datetime.now(SHANGHAI) + timedelta(days=7)).strftime("%Y-%m-%d")
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
            effective_from=future,
        )
        build_daily_tasks(conn, "2025001", china_ymd())
        live = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live, 1)
        plan_pending = get_plan(conn, "2025001")
        self.assertEqual(plan_pending["draft_effective_from"], future)
        conn.execute("DELETE FROM daily_tasks WHERE student_id='2025001'")
        conn.commit()
        build_daily_tasks(conn, "2025001", future)
        live2 = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live2, 2)

    def test_get_plan_promotes_due_draft(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        day = china_ymd()
        build_daily_tasks(conn, "2025001", day)
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
            effective_from=(datetime.now(SHANGHAI) + timedelta(days=7)).strftime("%Y-%m-%d"),
        )
        live_before = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live_before, 1)
        conn.execute(
            "UPDATE plan_draft_meta SET effective_from=? WHERE student_id='2025001'",
            (day,),
        )
        conn.commit()
        plan = get_plan(conn, "2025001")
        self.assertEqual(len(plan["live"]), 2)
        self.assertFalse(plan["draft"])
        self.assertFalse(plan["pending_plan_change"])

    def test_today_effective_applies_on_save(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        day = china_ymd()
        build_daily_tasks(conn, "2025001", day)
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
            effective_from=day,
        )
        live = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items WHERE student_id='2025001' AND status!='removed'"
        ).fetchone()["c"]
        self.assertEqual(live, 2)
        draft_n = conn.execute(
            "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id='2025001'"
        ).fetchone()["c"]
        self.assertEqual(draft_n, 0)
        plan = get_plan(conn, "2025001")
        self.assertFalse(plan["pending_plan_change"])

    def test_custom_profile_effective_from(self) -> None:
        conn = _connect()
        future = (datetime.now(SHANGHAI) + timedelta(days=3)).strftime("%Y-%m-%d")
        put_time_profile(
            conn,
            "2025001",
            {"weekday_minutes": 25, "effective_from": future},
        )
        row = conn.execute(
            "SELECT weekday_minutes, pending_weekday_minutes, pending_effective_from "
            "FROM student_time_profiles WHERE student_id='2025001'"
        ).fetchone()
        self.assertEqual(row["weekday_minutes"], 40)
        self.assertEqual(row["pending_weekday_minutes"], 25)
        self.assertEqual(row["pending_effective_from"], future)
        build_daily_tasks(conn, "2025001", china_ymd())
        row2 = conn.execute(
            "SELECT weekday_minutes, pending_weekday_minutes FROM student_time_profiles WHERE student_id='2025001'"
        ).fetchone()
        self.assertEqual(row2["weekday_minutes"], 40)
        build_daily_tasks(conn, "2025001", future)
        row3 = conn.execute(
            "SELECT weekday_minutes, pending_weekday_minutes FROM student_time_profiles WHERE student_id='2025001'"
        ).fetchone()
        self.assertEqual(row3["weekday_minutes"], 25)
        self.assertIsNone(row3["pending_weekday_minutes"])

    def test_pack_preview_ignores_minute_overrides(self) -> None:
        """按分钟装箱已下线：weekday/weekend_minutes 不再影响试算结果。"""
        conn = _connect()
        items = [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 9)]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        # 固定在某个工作日试算，确保命中的是 weekday_minutes 分支
        weekday = _recent_weekday()
        low = preview_daily_pack_items(
            conn, "2025001", items, task_date=weekday, weekday_minutes=40, weekend_minutes=90
        )
        high = preview_daily_pack_items(
            conn, "2025001", items, task_date=weekday, weekday_minutes=120, weekend_minutes=90
        )
        self.assertEqual(low["pack_mode"], PACK_MODE_UNITS_PER_DAY)
        self.assertNotIn("budget_minutes", low)
        self.assertEqual(
            [x["title"] for x in low["items"]],
            [x["title"] for x in high["items"]],
            "改预算不应再改变当日条目：装箱只认单元配额",
        )

    def test_save_duration_today_updates_budget_display_only(self) -> None:
        """改时长只影响「预算 xx′」展示，不再重排今日任务。"""
        conn = _connect()
        items = [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 9)]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        day = china_ymd()
        # 今天生效的预算取 weekday_minutes 还是 weekend_minutes，取决于运行当天是星期几
        expected_budget = 240 if is_weekend(day) else 120
        put_time_profile(
            conn, "2025001", {"weekday_minutes": 40, "weekend_minutes": 90, "effective": "today"}
        )
        daily40 = build_daily_tasks(conn, "2025001", day)
        self.assertGreaterEqual(len(daily40), 1)
        put_time_profile(
            conn,
            "2025001",
            {"weekday_minutes": 120, "weekend_minutes": 240, "effective_from": day},
        )
        n_locked = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=? AND task_date=?",
            ("2025001", day),
        ).fetchone()["c"]
        self.assertEqual(n_locked, 0)
        daily120 = build_daily_tasks(conn, "2025001", day)
        today = get_today(conn, "2025001")
        self.assertEqual(today["budget_minutes"], expected_budget)
        self.assertEqual(
            len(daily120), len(daily40), "时长不再驱动装箱，条目数应保持不变"
        )

    def _apply_reading_plan(self, conn: sqlite3.Connection, count: int) -> None:
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, count + 1)
        ]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")

    def _backdate_plan_start(self, conn: sqlite3.Connection, ymd: str) -> None:
        """把「计划生效日」提前，用于模拟早就有计划的老学生。

        早于计划生效日的 daily_tasks 视为幽灵行（不值班、不算积压），
        所以构造历史任务的测试必须先把计划生效日挪到那些日期之前。
        """
        conn.execute(
            "UPDATE plan_items SET created_at=? WHERE student_id='2025001'",
            (ymd + "T00:00:00.000Z",),
        )
        conn.commit()

    def _enable_units_mode(
        self,
        conn: sqlite3.Connection,
        *,
        weekday_units: int = 1,
        weekend_units: int = 1,
        module_type: str = "reading_synonym",
        effective: str = "today",
    ) -> None:
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": module_type,
                        "weekday_units": weekday_units,
                        "weekend_units": weekend_units,
                    }
                ],
                "effective": effective,
            },
        )

    def _set_pending_quota(
        self,
        conn: sqlite3.Connection,
        module_type: str,
        *,
        weekday_units: int,
        weekend_units: int,
        effective: str,
    ) -> None:
        """直接写 pending 配额列（绕过「生效日不得早于今天」的入参校验）。"""
        ensure_module_quota(conn, "2025001", module_type)
        conn.execute(
            """
            UPDATE student_module_daily_quota SET
                pending_weekday_units=?, pending_weekend_units=?
            WHERE student_id='2025001' AND module_type=?
            """,
            (weekday_units, weekend_units, module_type),
        )
        conn.execute(
            "UPDATE student_time_profiles SET pending_effective_from=? WHERE student_id='2025001'",
            (effective,),
        )
        conn.commit()

    def test_units_mode_two_per_day(self) -> None:
        conn = _connect()
        self._apply_reading_plan(conn, 5)
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)
        self._backdate_plan_start(conn, "2026-08-01")
        day1 = "2026-08-26"
        daily1 = build_daily_tasks(conn, "2025001", day1)
        self.assertEqual(len(daily1), 2)
        day2 = "2026-08-27"
        daily2 = build_daily_tasks(conn, "2025001", day2)
        self.assertEqual(len(daily2), 2)

    def test_zero_quota_means_module_skipped(self) -> None:
        """配额 0 = 当天不排这科；不能被当成「未设置」兜底成 1。"""
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._enable_units_mode(conn, weekday_units=0, weekend_units=0)
        self._backdate_plan_start(conn, "2026-08-01")
        self.assertEqual(build_daily_tasks(conn, "2025001", "2026-08-26"), [])

    def test_weekend_only_quota_is_supported(self) -> None:
        """完全可以只排周末：周中 0 / 周末 1（界面 min=0，后端 max(0,...)）。"""
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._enable_units_mode(conn, weekday_units=0, weekend_units=1)
        self._backdate_plan_start(conn, "2026-08-01")
        # 2026-08-26 是周三，2026-08-29 是周六
        self.assertEqual(build_daily_tasks(conn, "2025001", "2026-08-26"), [])
        self.assertEqual(len(build_daily_tasks(conn, "2025001", "2026-08-29")), 1)

    def test_quota_change_from_zero_is_detected(self) -> None:
        """0 是合法配额：把某科从「仅周末」改回「周中也排」必须被识别为变更。

        回归：以前用 `value or DEFAULT` 判等，0 被当成未设置→1，
        于是 0→1 的改动被判为「无变化」，pending 永不应用，该科周中回不来。
        """
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._backdate_plan_start(conn, "2026-08-01")
        self._enable_units_mode(conn, weekday_units=0, weekend_units=1)

        # 老师改回「周中也排 1 条」，写 pending 待明天生效
        # （直接写列，避免依赖「生效日不得早于今天」的校验）
        self._set_pending_quota(
            conn, "reading_synonym", weekday_units=1, weekend_units=1, effective="2026-08-27"
        )
        prof = ensure_time_profile(conn, "2025001")
        self.assertTrue(_profile_has_real_pending(prof))
        self.assertTrue(_profile_pending_due(prof, "2026-08-27"))

        maybe_apply_pending_for_today(conn, "2025001", "2026-08-27")
        row = conn.execute(
            """
            SELECT weekday_units FROM student_module_daily_quota
            WHERE student_id='2025001' AND module_type='reading_synonym'
            """
        ).fetchone()
        self.assertEqual(row["weekday_units"], 1)
        # 周四（2026-08-27）应当能派出来了
        self.assertEqual(len(build_daily_tasks(conn, "2025001", "2026-08-27")), 1)

    def test_quota_change_to_zero_is_detected(self) -> None:
        """反向：把某科改成「仅周末」也必须被识别为变更，并重建当天任务。"""
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._backdate_plan_start(conn, "2026-08-01")
        self._enable_units_mode(conn, weekday_units=1, weekend_units=1)
        self._set_pending_quota(
            conn, "reading_synonym", weekday_units=0, weekend_units=1, effective="2026-08-27"
        )
        prof = ensure_time_profile(conn, "2025001")
        self.assertTrue(_profile_has_real_pending(prof))
        maybe_apply_pending_for_today(conn, "2025001", "2026-08-27")
        row = conn.execute(
            """
            SELECT weekday_units FROM student_module_daily_quota
            WHERE student_id='2025001' AND module_type='reading_synonym'
            """
        ).fetchone()
        self.assertEqual(row["weekday_units"], 0)
        self.assertEqual(build_daily_tasks(conn, "2025001", "2026-08-27"), [])

    def test_units_mode_multi_subject_same_day(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {"item_type": "study", "unit_id": "dictation_u01"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 2,
                        "weekend_units": 1,
                    },
                    {
                        "module_type": "dictation",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    },
                ],
                "effective": "today",
            },
        )
        day = "2026-08-26"
        self._backdate_plan_start(conn, "2026-08-01")
        daily = build_daily_tasks(conn, "2025001", day)
        self.assertEqual(len(daily), 3)
        modules = [d["module_type"] for d in daily]
        self.assertEqual(modules.count("reading_synonym"), 2)
        self.assertEqual(modules.count("dictation"), 1)

    def test_units_mode_backlog_capped_by_quota(self) -> None:
        """Unfinished weekend/heavy day must not dump all onto a smaller weekday."""
        conn = _connect()
        self._apply_reading_plan(conn, 5)
        self._backdate_plan_start(conn, "2026-08-01")
        self._enable_units_mode(conn, weekday_units=3, weekend_units=3)
        day1 = "2026-08-25"
        build_daily_tasks(conn, "2025001", day1)
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)
        day2 = "2026-08-26"
        daily2 = build_daily_tasks(conn, "2025001", day2)
        self.assertEqual(len(daily2), 2)
        # 保底名额：积压不得占满，必须给新单元留一条，否则新内容永远进不来
        self.assertEqual(
            sorted(d["priority_class"] for d in daily2), ["carry_over", "fresh"]
        )
        # As of day2: day1's 3 unfinished count; day2's in-progress do not add extra.
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001", before_date=day2)), 3)
        # 8/27 口径：day1 的 3 条 + day2 新派出的 2 条（其中 1 条是新推进的单元）
        self.assertEqual(
            len(backlog_plan_item_ids(conn, "2025001", before_date="2026-08-27")), 4
        )

    def test_fresh_unit_reserved_when_backlog_fills_quota(self) -> None:
        """积压占满配额时必须给新单元留一条，否则新内容永远进不来（Bug 5）。

        线上 2025085 连续 10 天派同一批、完成率 0%，就是因为积压长期占满全部名额。
        """
        conn = _connect()
        self._apply_reading_plan(conn, 6)
        self._backdate_plan_start(conn, "2026-08-01")
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)

        day1 = "2026-08-25"
        first = build_daily_tasks(conn, "2025001", day1)
        self.assertEqual(len(first), 2)
        self.assertTrue(all(d["priority_class"] == "fresh" for d in first))

        # 第 2 天积压 2 条 = 配额 2：必须让出 1 条给新单元
        day2 = "2026-08-26"
        second = build_daily_tasks(conn, "2025001", day2)
        self.assertEqual(len(second), 2)
        self.assertEqual(
            sorted(d["priority_class"] for d in second), ["carry_over", "fresh"]
        )
        # 让出来的那条必须是「从没派过」的新单元
        fresh_ids = {
            int(d["plan_item_id"]) for d in second if d["priority_class"] == "fresh"
        }
        day1_ids = {int(d["plan_item_id"]) for d in first}
        self.assertFalse(fresh_ids & day1_ids)

    def test_single_quota_alternates_backlog_and_fresh(self) -> None:
        """quota=1 时积压与新单元按日期轮流，两支都要能往前走。"""
        conn = _connect()
        self._apply_reading_plan(conn, 6)
        self._backdate_plan_start(conn, "2026-08-01")
        self._enable_units_mode(conn, weekday_units=1, weekend_units=1)

        day1 = "2026-08-25"  # 奇数日：无积压，只能派新单元
        first = build_daily_tasks(conn, "2025001", day1)
        self.assertEqual(len(first), 1)
        self.assertEqual(first[0]["priority_class"], "fresh")

        day2 = "2026-08-26"  # 偶数日：优先新单元
        second = build_daily_tasks(conn, "2025001", day2)
        self.assertEqual(len(second), 1)
        self.assertEqual(second[0]["priority_class"], "fresh")

        day3 = "2026-08-27"  # 奇数日：优先消化积压
        third = build_daily_tasks(conn, "2025001", day3)
        self.assertEqual(len(third), 1)
        self.assertEqual(third[0]["priority_class"], "carry_over")

    def test_backlog_excludes_today_unfinished(self) -> None:
        """Today's unlocked work is not backlog until the day has passed."""
        conn = _connect()
        self._apply_reading_plan(conn, 3)
        self._backdate_plan_start(conn, "2026-09-01")
        self._enable_units_mode(conn, weekday_units=3, weekend_units=3)
        today = "2026-09-10"
        daily = build_daily_tasks(conn, "2025001", today)
        self.assertEqual(len(daily), 3)
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001", before_date=today)), 0)
        tomorrow = "2026-09-11"
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001", before_date=tomorrow)), 3)

    def test_day_unfinished_count_clears_when_that_day_done(self) -> None:
        """看板积压：**昨天**那批做完 = 0；今天没做不算积压（2026-09-20 第二次修订）。"""
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._backdate_plan_start(conn, "2026-09-01")
        self._enable_units_mode(conn, weekday_units=4, weekend_units=4)
        yesterday = "2026-09-09"
        today = "2026-09-10"
        build_daily_tasks(conn, "2025001", yesterday)
        y_pids = [
            int(r["plan_item_id"])
            for r in conn.execute(
                "SELECT plan_item_id FROM daily_tasks WHERE student_id='2025001' AND task_date=?",
                (yesterday,),
            )
        ]
        self.assertGreaterEqual(len(y_pids), 2)

        # 更早的 09-03 也派过、且没做。旧口径（历史累计）会把它算进积压。
        for i, pid in enumerate(y_pids):
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES ('2025001', '2026-09-03', ?, 'fresh', ?, 'todo', 1, 0)
                """,
                (pid, i),
            )
        conn.commit()

        # 看板只回看昨天：昨天这批一条没做 → 积压 = 昨天条数
        self.assertEqual(day_unfinished_count(conn, "2025001", yesterday), len(y_pids))

        # 昨天全部做完 → 积压必须是 0（不管 09-03 那批多旧）
        # scope_done 给一个足够大的值：本用例只关心积压口径，不关心 scope 校验。
        for pid in y_pids:
            complete_study(conn, "2025001", pid, "1", scope_done=1000)
        self.assertEqual(day_unfinished_count(conn, "2025001", yesterday), 0)

        # 今天照常派任务、一条没做：那是「今天还没做完」，正常现象，不算积压。
        build_daily_tasks(conn, "2025001", today)
        self.assertEqual(day_unfinished_count(conn, "2025001", yesterday), 0)

    def test_day_unfinished_count_ignores_tests_and_residue(self) -> None:
        """阶段测不算任务量：既不进分母也不进分子；已完成条目的残留 todo 行也不算。

        口径见 ``day_task_progress``（2026-09-20 第四次修订）。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-09-01")
        # 用真实「今天」：complete_study 的回写窗口是「今天 + 昨天」，假日期会让
        # daily 行停在 todo，测不到本用例真正关心的「阶段测是否计入任务量」。
        today = china_ymd()
        rows = conn.execute(
            "SELECT id, item_type FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        for i, r in enumerate(rows):
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES ('2025001', ?, ?, 'fresh', ?, 'todo', 1, 0)
                """,
                (today, r["id"], i),
            )
        conn.commit()
        # 3 条 todo（2 学习 + 1 阶段测）→ 阶段测不进分母，只算 2 条学习
        self.assertEqual(day_task_progress(conn, "2025001", today), (0, 2))
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 2)

        # 两个学习条目做掉、阶段测没考 → 学习那部分清零（阶段测不影响）
        studies = [r for r in rows if r["item_type"] == "study"]
        for r in studies:
            complete_study(conn, "2025001", int(r["id"]), "1", scope_done=1000)
        self.assertEqual(day_task_progress(conn, "2025001", today), (2, 2))
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)

        # 阶段测考挂了也不会让积压冒出来：考挂只留那条测挂着，科目任务不动。
        test_row = [r for r in rows if r["item_type"] == "test"][0]
        submit_stage_test(
            conn, "2025001", int(test_row["id"]), 30, threshold=80
        )
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)
        submit_stage_test(
            conn, "2025001", int(test_row["id"]), 90, threshold=80
        )
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)
        self.assertEqual(day_task_progress(conn, "2025001", today), (2, 2))

        # 已完成条目若还残留 todo 行，也不该算积压。
        # 用 u02：验证「学习单元一旦学完就不会被阶段测打回未完成」。
        conn.execute(
            "UPDATE daily_tasks SET state='todo' WHERE student_id='2025001' AND task_date=? "
            "AND plan_item_id=?",
            (today, int(studies[1]["id"])),
        )
        conn.commit()
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)

    def test_failed_stage_test_not_counted_as_backlog(self) -> None:
        """阶段测考了没过（done_fail 且 test_passed 仍为 0）→ 仍是「没考过」，
        但**不计入任务量，也不计入积压**（2026-09-20 第四次修订）。

        它留在队列里的事实由「待通过阶段测」列呈现，不占用任务的完成率。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-09-01")
        # 真实「今天」：理由同上（complete_study 的回写窗口）
        today = china_ymd()
        rows = conn.execute(
            "SELECT id, item_type FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        for i, r in enumerate(rows):
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES ('2025001', ?, ?, 'fresh', ?, 'todo', 1, 0)
                """,
                (today, r["id"], i),
            )
        conn.commit()
        for r in rows:
            if r["item_type"] == "study":
                complete_study(conn, "2025001", int(r["id"]), "1", scope_done=1000)
        test_row = [r for r in rows if r["item_type"] == "test"][0]

        # 考了一次没过 → 分母只有那 1 条学习，已完成 → 积压 0
        submit_stage_test(conn, "2025001", int(test_row["id"]), 40, threshold=80)
        self.assertEqual(day_task_progress(conn, "2025001", today), (1, 1))
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)
        # 但「待通过阶段测」那一列照旧看得见它
        self.assertEqual(len(stage_tests_pending(conn, "2025001")), 1)

        # 再考一次过了 → 依然 0
        submit_stage_test(conn, "2025001", int(test_row["id"]), 85, threshold=80)
        self.assertEqual(day_unfinished_count(conn, "2025001", today), 0)

    def test_test_only_day_stays_green(self) -> None:
        """昨天只派了一个阶段测、没考 → 昨日任务 0/0 → 绿灯，积压 0。

        「阶段测不算任务量」（2026-09-20 第四次修订）：测不进分母，所以没有
        「一条没做」这个事实可比，不判红。测的欠账在「待通过阶段测」列看。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        test_row = conn.execute(
            "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
        ).fetchone()
        yesterday = "2026-09-01"
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 1, 0)
            """,
            (yesterday, int(test_row["id"])),
        )
        conn.commit()
        row = class_overview(conn, task_date="2026-09-02")["students"][0]
        self.assertEqual(row["yesterday_total"], 0)
        self.assertEqual(row["yesterday_done"], 0)
        self.assertEqual(row["backlog"], 0)
        self.assertEqual(row["row_status"], "green")
        # 测没考过这件事仍然可见
        self.assertEqual(row["stage_test_pending"], 1)

    def test_day_progress_counts_plan_completed_even_if_daily_todo(self) -> None:
        """跟读类条目：达标后 `plan.study_completed=1`，但那天 daily 行仍残留 todo。

        这一天其实做完了，不能被算成「没做」，否则学生练到 76 分达标、看板却给红灯。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001'"
            ).fetchone()["id"]
        )
        yesterday = "2026-09-01"
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 1, 0)
            """,
            (yesterday, pid),
        )
        conn.commit()
        # daily 行是 todo → 看起来没做
        self.assertEqual(day_unfinished_count(conn, "2025001", yesterday), 1)

        # 条目达标（跟读对账就是这么写的），daily 行不动
        conn.execute("UPDATE plan_items SET study_completed=1 WHERE id=?", (pid,))
        conn.commit()
        self.assertEqual(day_task_progress(conn, "2025001", yesterday), (1, 1))
        self.assertEqual(day_unfinished_count(conn, "2025001", yesterday), 0)

        row = class_overview(conn, task_date="2026-09-02")["students"][0]
        self.assertEqual(row["yesterday_done"], 1)
        self.assertEqual(row["yesterday_total"], 1)
        self.assertEqual(row["row_status"], "green")

    def test_stage_tests_pending_reports_attempts_and_best(self) -> None:
        """阶段测单独记录：明细带累计已考次数与最高分。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阅读同替 U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )
        pending = stage_tests_pending(conn, "2025001")
        self.assertEqual(len(pending), 1)
        self.assertTrue(pending[0]["never_attempted"])
        self.assertEqual(pending[0]["attempts"], 0)

        submit_stage_test(conn, "2025001", test_pid, 40, threshold=80)
        pending = stage_tests_pending(conn, "2025001")
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["attempts"], 1)
        self.assertEqual(pending[0]["best_score"], 40.0)
        self.assertFalse(pending[0]["never_attempted"])

        # 通过后即从「待通过」里消失
        submit_stage_test(conn, "2025001", test_pid, 90, threshold=80)
        self.assertEqual(stage_tests_pending(conn, "2025001"), [])

    def test_stage_test_retries_are_unlimited(self) -> None:
        """阶段测不限重测次数：同一天连续考很多次都不能被拦。

        回归自线上反馈「阶段测试过不去，任务也完成了，学不了了啊」——
        原来的「每天 2 次」上限让考不过的学生既过不了、又不让再考，
        当天任务永远完不成，直接被锁死。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阅读同替 U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )
        # 远超原先的 2 次上限，全部应当被接受（不能抛 ValueError）
        for i in range(7):
            submit_stage_test(conn, "2025001", test_pid, 30, threshold=80)
        pending = stage_tests_pending(conn, "2025001")
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["attempts"], 7)
        self.assertEqual(pending[0]["best_score"], 30.0)
        # 次数很多 → 打上「建议助教介入」标记，但不影响继续提交
        self.assertTrue(pending[0]["needs_attention"])
        submit_stage_test(conn, "2025001", test_pid, 95, threshold=80)
        self.assertEqual(stage_tests_pending(conn, "2025001"), [])

    def test_stage_test_missing_yesterday_keeps_row_green(self) -> None:
        """阶段测不算任务量：昨天 3 条学习做完、1 条阶段测没考 → 3/3 → 绿灯。

        「任务阶段测试不算任务量」（2026-09-20 第四次修订）。测没考这件事只在
        「待通过阶段测」列可见，不把学生的昨日完成率拖成 3/4。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {"item_type": "study", "unit_id": "reading_synonym_u03"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        yesterday = "2026-09-01"
        today = "2026-09-02"
        rows = conn.execute(
            "SELECT id, item_type FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        for i, r in enumerate(rows):
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES ('2025001', ?, ?, 'fresh', ?, ?, 1, 0)
                """,
                (yesterday, r["id"], i, "done_study" if r["item_type"] == "study" else "todo"),
            )
        conn.commit()
        row = class_overview(conn, task_date=today)["students"][0]
        self.assertEqual(row["yesterday_total"], 3)
        self.assertEqual(row["yesterday_done"], 3)
        self.assertEqual(row["backlog"], 0)
        self.assertEqual(row["row_status"], "green")
        self.assertEqual(row["stage_test_pending"], 1)

    def test_stage_needs_attention_is_flagged_not_red(self) -> None:
        """昨天任务全做完 → 绿灯；今天反复考不过只在「待通过阶段测」列标记，不判红。

        老师的痛点是「看不见卡死」，所以加独立标记而不是把灯改成红。
        不限重测次数之后，标记的含义从「今天考不动了」改成「累计考了很多次还没过」。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        # 用真实日期：stage_tests_pending 内部按 china_ymd() 判断「今天考了几次」，
        # 用假日期会导致看板（按 task_date）和明细（按真实今天）对不上。
        today = china_ymd()
        yesterday = (
            datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        study_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='study' "
                "ORDER BY sort_order LIMIT 1"
            ).fetchone()["id"]
        )
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'done_study', 1, 0)
            """,
            (yesterday, study_pid),
        )
        conn.commit()
        # 昨天那条学习任务做完了 → 1/1 → 绿，且没有反复考不过标记
        row = class_overview(conn, task_date=today)["students"][0]
        self.assertEqual(row["row_status"], "green")
        self.assertEqual(row["stage_test_needs_attention"], 0)

        # 累计考满 STAGE_TEST_ATTENTION_FAILS 次仍未过 → 标记 1，但灯不变红
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )
        for _ in range(STAGE_TEST_ATTENTION_FAILS):
            submit_stage_test(conn, "2025001", test_pid, 30, threshold=80)
        row = class_overview(conn, task_date=today)["students"][0]
        self.assertEqual(row["stage_test_needs_attention"], 1)
        self.assertEqual(row["stage_test_pending"], 1)
        self.assertEqual(row["row_status"], "green")

        # 明细接口也要带上这个标记，供前端展开时显示
        pend = stage_tests_pending(conn, "2025001")
        self.assertEqual(len(pend), 1)
        self.assertTrue(pend[0]["needs_attention"])
        self.assertNotIn("attempts_left_today", pend[0])

    def test_units_mode_weekend_backlog_weekday_cap(self) -> None:
        """Weekend 6 unfinished → Monday shows weekday 3, rest stay in backlog."""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            (
                [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 5)]
                + [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 5)]
                + [
                    {"item_type": "study", "unit_id": f"listening_synonym_u{i:02d}"}
                    for i in range(1, 5)
                ]
            ),
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {"module_type": "reading_synonym", "weekday_units": 1, "weekend_units": 2},
                    {"module_type": "dictation", "weekday_units": 1, "weekend_units": 2},
                    {"module_type": "listening_synonym", "weekday_units": 1, "weekend_units": 2},
                ],
                "effective": "today",
            },
        )
        weekend = build_daily_tasks(conn, "2025001", "2026-08-29")
        self.assertEqual(len(weekend), 6)
        monday = build_daily_tasks(conn, "2025001", "2026-08-31")
        self.assertEqual(len(monday), 3)
        self.assertTrue(all(d["priority_class"] == "carry_over" for d in monday))
        self.assertEqual(
            len(backlog_plan_item_ids(conn, "2025001", before_date="2026-08-31")), 6
        )

    def test_units_mode_weekend_quota(self) -> None:
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._enable_units_mode(conn, weekday_units=2, weekend_units=1)
        self._backdate_plan_start(conn, "2026-08-01")
        weekend = build_daily_tasks(conn, "2025001", "2026-08-29")
        self.assertEqual(len(weekend), 1)
        conn.execute("DELETE FROM daily_tasks WHERE student_id='2025001'")
        conn.commit()
        weekday = build_daily_tasks(conn, "2025001", "2026-08-26")
        self.assertEqual(len(weekday), 2)

    def test_units_mode_pending_quota_future(self) -> None:
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        future = (datetime.now(SHANGHAI) + timedelta(days=2)).strftime("%Y-%m-%d")
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    }
                ],
                "effective": "today",
            },
        )
        put_time_profile(
            conn,
            "2025001",
            {
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 3,
                        "weekend_units": 3,
                    }
                ],
                "effective_from": future,
            },
        )
        today = china_ymd()
        daily_today = build_daily_tasks(conn, "2025001", today)
        self.assertEqual(len(daily_today), 1)
        conn.execute("DELETE FROM daily_tasks WHERE student_id='2025001'")
        conn.commit()
        daily_future = build_daily_tasks(conn, "2025001", future)
        self.assertEqual(len(daily_future), 3)

    def test_pack_mode_defaults_units_per_day(self) -> None:
        conn = _connect()
        profile = get_plan(conn, "2025001")["time_profile"]
        self.assertEqual(profile.get("pack_mode"), PACK_MODE_UNITS_PER_DAY)

    def test_legacy_time_budget_profile_still_packs_units(self) -> None:
        """老档案里残留的 pack_mode='time_budget' 不能把分钟制放回来。"""
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        conn.execute(
            "UPDATE student_time_profiles SET pack_mode=? WHERE student_id='2025001'",
            (PACK_MODE_TIME_BUDGET,),
        )
        conn.commit()
        daily = build_daily_tasks(conn, "2025001", china_ymd())
        self.assertGreaterEqual(len(daily), 1)
        preview = preview_daily_pack_items(
            conn, "2025001", [], pack_mode=PACK_MODE_TIME_BUDGET, weekday_minutes=5
        )
        self.assertEqual(preview["pack_mode"], PACK_MODE_UNITS_PER_DAY)
        self.assertNotIn("budget_minutes", preview)

    def test_put_time_profile_rejects_time_budget(self) -> None:
        conn = _connect()
        with self.assertRaises(ValueError):
            put_time_profile(conn, "2025001", {"pack_mode": PACK_MODE_TIME_BUDGET})

    def test_units_preview_includes_schedule(self) -> None:
        conn = _connect()
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, 6)
        ]
        preview = preview_daily_pack_items(
            conn,
            "2025001",
            items,
            pack_mode=PACK_MODE_UNITS_PER_DAY,
            module_quotas=[
                {
                    "module_type": "reading_synonym",
                    "weekday_units": 2,
                    "weekend_units": 2,
                }
            ],
        )
        self.assertEqual(preview["pack_mode"], PACK_MODE_UNITS_PER_DAY)
        self.assertEqual(preview["units_total"], 2)
        self.assertGreaterEqual(len(preview.get("schedule") or []), 2)

    def test_units_schedule_advances_each_day(self) -> None:
        conn = _connect()
        items = (
            [{"item_type": "study", "unit_id": f"dictation_u{i:02d}"} for i in range(1, 4)]
            + [
                {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
                for i in range(1, 4)
            ]
        )
        # Pin to a Monday so weekend quotas don't compress the 3-day layout.
        with mock.patch("task_api.china_ymd", return_value="2026-09-07"):
            preview = preview_daily_pack_items(
                conn,
                "2025001",
                items,
                pack_mode=PACK_MODE_UNITS_PER_DAY,
                module_quotas=[
                    {"module_type": "dictation", "weekday_units": 1, "weekend_units": 2},
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 2,
                    },
                ],
            )
        schedule = preview.get("schedule") or []
        self.assertGreaterEqual(len(schedule), 3)
        day0 = {x["title"] for x in schedule[0]["items"]}
        day1 = {x["title"] for x in schedule[1]["items"]}
        day2 = {x["title"] for x in schedule[2]["items"]}
        self.assertEqual(len(day0), 2)
        self.assertEqual(len(day1), 2)
        self.assertFalse(day0 & day1)
        self.assertFalse(day0 & day2)
        self.assertFalse(day1 & day2)

    def test_class_overview_empty_plan_is_none(self) -> None:
        conn = _connect()
        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)
        data = class_overview(conn, task_date="2026-09-02", now=noon)
        self.assertEqual(data["stats"]["total"], 1)
        row = data["students"][0]
        self.assertEqual(row["student_id"], "2025001")
        self.assertEqual(row["plan_status"], "none")
        self.assertEqual(row["row_status"], "none")
        self.assertEqual(row["today_total"], 0)

    def test_failed_stage_test_only_keeps_test_pending(self) -> None:
        """阶段测考挂 → 只留这条测「待通过」，不重排科目任务（2026-09-20 决议）。

        回归自「阶段测过不去、任务又都做完了，学不了了啊」。先试过「考挂 → 把覆盖单元
        打回未完成强制重学」，但模拟里学生被钉在同一批单元上（每单元重学 3 轮到顶），
        一天还被十几条考挂的测占满时间。改为：科目任务不重排，学生想再学，从
        「学习进度」里点对应模块的学习按钮就能进去。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01", "reading_synonym_u02"],
                    "test_title": "U1-U2 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-09-01")
        studies = conn.execute(
            "SELECT id, unit_id FROM plan_items WHERE student_id='2025001' "
            "AND item_type='study' ORDER BY sort_order"
        ).fetchall()
        for r in studies:
            complete_study(conn, "2025001", int(r["id"]), "1", scope_done=1000)
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )

        def _study_state() -> list[tuple[int, int]]:
            return [
                (int(r["study_completed"]), int(r["need_refresh"]))
                for r in conn.execute(
                    "SELECT study_completed, need_refresh FROM plan_items "
                    "WHERE student_id='2025001' AND item_type='study' ORDER BY sort_order"
                ).fetchall()
            ]

        self.assertEqual(_study_state(), [(1, 0), (1, 0)])

        res = submit_stage_test(conn, "2025001", test_pid, 30, threshold=80)
        self.assertFalse(res["passed"])
        # 不重排：覆盖单元保持「已学完、不需要重学」
        self.assertEqual(res["restudy_units"], [])
        self.assertEqual(_study_state(), [(1, 0), (1, 0)])

        # 连考多次也不会把单元打回未完成（重测不限次数）
        for score in (20, 10, 40, 0, 55):
            submit_stage_test(conn, "2025001", test_pid, score, threshold=80)
        self.assertEqual(_study_state(), [(1, 0), (1, 0)])

        # 测自己挂在清单里：仍是 pending、仍未通过，随时可再考
        row = conn.execute(
            "SELECT status, test_passed, test_attempt_count_today FROM plan_items WHERE id=?",
            (test_pid,),
        ).fetchone()
        self.assertEqual(str(row["status"]), "pending")
        self.assertEqual(int(row["test_passed"]), 0)
        self.assertGreaterEqual(int(row["test_attempt_count_today"]), 6)

        # 考过之后收工
        self.assertTrue(submit_stage_test(conn, "2025001", test_pid, 95, threshold=80)["passed"])

    def test_failed_stage_test_does_not_add_rows_to_today(self) -> None:
        """考挂不会往当天任务里补学习条目；当天那批保持不变。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-09-01")
        today = china_ymd()
        study_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='study'"
            ).fetchone()["id"]
        )
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )
        # 当天先锁定一批：只有那条测（单元当时还没学完）
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 1, 0)
            """,
            (today, test_pid),
        )
        conn.commit()

        def _today_rows() -> list[tuple[int, str]]:
            return [
                (int(r["plan_item_id"]), str(r["state"]))
                for r in conn.execute(
                    "SELECT plan_item_id, state FROM daily_tasks "
                    "WHERE student_id='2025001' AND task_date=? ORDER BY sort_in_day",
                    (today,),
                ).fetchall()
            ]

        before = _today_rows()
        complete_study(conn, "2025001", study_pid, "1", scope_done=1000)
        submit_stage_test(conn, "2025001", test_pid, 30, threshold=80)

        # 没有新增学习条目，只有那条测自己被记成 done_fail
        self.assertEqual([pid for pid, _ in _today_rows()], [pid for pid, _ in before])
        self.assertIn((test_pid, "done_fail"), _today_rows())

    def test_failed_test_leaves_titles_and_progress_clean(self) -> None:
        """考挂后学生端标题不出现「需重学」，教师端计划进度也不显示「·重N」。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "U1 阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-09-01")
        study_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='study'"
            ).fetchone()["id"]
        )
        test_pid = int(
            conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' AND item_type='test'"
            ).fetchone()["id"]
        )
        complete_study(conn, "2025001", study_pid, "1", scope_done=1000)
        submit_stage_test(conn, "2025001", test_pid, 30, threshold=80)

        row = class_overview(conn, task_date=china_ymd())["students"][0]
        texts = [b["text"] for b in row["plan_progress_brief"]]
        self.assertFalse(any("·重" in t for t in texts), texts)

        today = get_today(conn, "2025001")
        titles = [str(x.get("title") or "") for x in today["items"]]
        self.assertFalse(any("需重学" in t for t in titles), titles)
        self.assertFalse(any("内容已更新" in t for t in titles), titles)


    def test_class_overview_today_counts_and_done_fail(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
                {
                    "item_type": "test",
                    "module_type": "reading_synonym",
                    "test_unit_ids": ["reading_synonym_u01"],
                    "test_title": "阶段测",
                },
            ],
        )
        apply_draft_to_live(conn, "2025001")
        # 让计划在 task_date 前一天(09-01)就已生效，这样「补昨日」才合理——
        # 新规则：class_overview 不会补早于计划生效日的日期。
        conn.execute(
            "UPDATE plan_items SET created_at='2026-09-01T00:00:00Z' WHERE student_id='2025001'"
        )
        conn.commit()
        items = conn.execute(
            "SELECT id, item_type FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        day = "2026-09-02"
        for i, it in enumerate(items):
            state = "todo"
            if it["item_type"] == "study" and i == 0:
                state = "done_study"
            elif it["item_type"] == "test":
                state = "done_fail"
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES (?, ?, ?, 'fresh', ?, ?, 1, 0)
                """,
                ("2025001", day, it["id"], i, state),
            )
        conn.commit()
        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)
        today_before = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001' AND task_date=?",
            (day,),
        ).fetchone()["c"]
        data = class_overview(conn, task_date=day, now=noon)
        today_after = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001' AND task_date=?",
            (day,),
        ).fetchone()["c"]
        # Existing today pack is kept; overview may also materialize yesterday.
        self.assertEqual(today_before, today_after)
        # 「补昨日」的正例见 test_class_overview_materializes_missing_days。
        # 这里昨天的 3 个条目都已在今天的 pack 里 release 过，units 模式的
        # released 集合按学生全局计算（不区分日期），所以昨天补不出任务。
        row = data["students"][0]
        # 阶段测不算任务量：3 条 daily 里只有 2 条学习进分母
        self.assertEqual(row["today_total"], 2)
        # done_fail does not count as done
        self.assertEqual(row["today_done"], 1)
        # 测没过这件事仍在「待通过阶段测」列可见
        self.assertEqual(row["test_fail"], 1)
        self.assertTrue(any(b["label"] == "阅" for b in row["plan_progress_brief"]))

    def test_class_overview_materializes_missing_days(self) -> None:
        """Active plan students get today+yesterday packs even if they never opened 今日任务."""
        conn = _connect()
        self._apply_reading_plan(conn, 5)
        # 让计划在 task_date 前一天(09-01)就已生效，这样「补昨日」才合理——
        # 新规则：class_overview 不会补早于计划生效日的日期。
        conn.execute(
            "UPDATE plan_items SET created_at='2026-09-01T00:00:00Z' WHERE student_id='2025001'"
        )
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)
        # Wipe any packs created by profile apply so we simulate a lazy student.
        conn.execute("DELETE FROM daily_tasks WHERE student_id='2025001'")
        conn.commit()
        day = "2026-09-02"
        self.assertEqual(
            conn.execute(
                "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001'"
            ).fetchone()["c"],
            0,
        )
        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)
        data = class_overview(conn, task_date=day, now=noon)
        row = data["students"][0]
        self.assertGreater(row["today_total"], 0)
        self.assertGreater(row["yesterday_total"], 0)

    def test_ensure_active_plan_no_backfill_before_plan_start(self) -> None:
        """回归：计划今天刚生效时，回填只应覆盖「计划生效日」及之后，
        不得把昨日/更早塞进「计划尚未生效」的日期，否则会制造虚假 backlog。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 4)],
        )
        apply_draft_to_live(conn, "2025001")
        today = china_ymd()  # 计划此时生效（created_at ≈ now）
        ensure_active_plan_daily_tasks(conn, "2025001", as_of=today, lookback_days=7)
        rows = conn.execute(
            "SELECT DISTINCT task_date FROM daily_tasks WHERE student_id='2025001'"
        ).fetchall()
        dates = [str(r[0]) for r in rows]
        # 早于计划生效日的日期必须一条都没有
        self.assertTrue(dates, "活跃计划今天应至少有一条任务")
        self.assertGreaterEqual(
            min(dates), today, f"不得回填早于计划生效日{today}的日期，实际={dates}"
        )
        # 且不产生虚假 backlog：早于今天的「未完成」不该计入（今天不算积压）
        self.assertEqual(
            len(backlog_plan_item_ids(conn, "2025001", before_date=today)), 0
        )

    def test_backlog_ignores_legacy_ghost_rows_before_plan_start(self) -> None:
        """回归（线上左茜文 2025144）：旧版回填留下的幽灵行不能再算积压。

        线上实例：计划 9/17 11:45 创建，11:46 有幽灵行落到 9/16，
        导致「昨日任务 3/3 · 100%」却仍显示「积压 3」并标红。
        这里手工插入同样的历史脏数据，验证 backlog / 昨日看板都忽略它。
        """
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
                for i in range(1, 4)
            ],
        )
        apply_draft_to_live(conn, "2025001")
        # 计划生效日固定为 2026-09-17（上海日）
        conn.execute(
            "UPDATE plan_items SET created_at='2026-09-17T03:45:56.301Z' "
            "WHERE student_id='2025001'"
        )
        conn.commit()
        today = "2026-09-18"
        plan_item_ids = [
            int(r["id"])
            for r in conn.execute(
                "SELECT id FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
            ).fetchall()
        ]
        # 模拟旧版回填：把队首单元塞进计划生效日之前（9/16）
        for sort_i, pid in enumerate(plan_item_ids):
            conn.execute(
                """
                INSERT INTO daily_tasks
                    (student_id, task_date, plan_item_id, priority_class,
                     sort_in_day, state, locked)
                VALUES ('2025001', '2026-09-16', ?, 'fresh', ?, 'todo', 1)
                """,
                (pid, sort_i),
            )
        conn.commit()
        # 幽灵行不得计入积压
        self.assertEqual(
            backlog_plan_item_ids(conn, "2025001", before_date=today),
            [],
            "计划生效日之前的幽灵行不应计入积压",
        )
        # 幽灵日也不能冒充「昨日任务」
        row = _student_overview_row(
            conn, "2025001", "测试学生", today, hour=10
        )
        self.assertEqual(row["yesterday_total"], 0)
        self.assertNotEqual(row["row_status"], "red")

    def test_plan_progress_brief_lists_all_modules(self) -> None:
        brief = _plan_progress_brief(
            {
                "reading_synonym": {"study_x": 1, "study_y": 23},
                "writing_translate": {"study_x": 0, "study_y": 22},
                "writing_phrase": {"study_x": 0, "study_y": 14},
                "sentence": {"study_x": 0, "study_y": 11},
            }
        )
        self.assertEqual(len(brief), 4)
        self.assertFalse(any(b.get("module_type") == "_more" for b in brief))
        texts = [b["text"] for b in brief]
        self.assertIn("阅1/23", texts)
        self.assertIn("翻译0/22", texts)
        self.assertIn("词伙0/14", texts)
        self.assertIn("长难0/11", texts)

    def test_overview_backlog_and_status_follow_yesterday(self) -> None:
        """看板积压与红黄灯都回看**昨天**（2026-09-20 第二次修订）。

        昨天任务全没做 → 红；只做了一部分 → 黄；全做完 → 绿（哪怕今天一条没做）。
        今天还没做完是正常现象，不进积压、不判红黄。
        """
        conn = _connect()
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 6)
        ]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        rows = conn.execute(
            "SELECT id FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        yesterday = "2026-09-01"
        today = "2026-09-02"

        def _set_yesterday(states: list[str]) -> None:
            conn.execute(
                "DELETE FROM daily_tasks WHERE student_id='2025001' AND task_date=?",
                (yesterday,),
            )
            for i, (r, st) in enumerate(zip(rows[:5], states)):
                conn.execute(
                    """
                    INSERT INTO daily_tasks
                    (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                    VALUES ('2025001', ?, ?, 'fresh', ?, ?, 1, 0)
                    """,
                    (yesterday, r["id"], i, st),
                )
            conn.commit()

        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)

        # 昨天 5 条一条没做 → 积压 5，红灯
        _set_yesterday(["todo"] * 5)
        row = class_overview(conn, task_date=today, now=noon)["students"][0]
        self.assertEqual(row["backlog"], 5)
        self.assertEqual(row["yesterday_done"], 0)
        self.assertEqual(row["row_status"], "red")

        # 昨天做了 2 条、没做完 → 积压 3，黄灯
        _set_yesterday(["done_study", "done_study"] + ["todo"] * 3)
        row = class_overview(conn, task_date=today, now=noon)["students"][0]
        self.assertEqual(row["backlog"], 3)
        self.assertEqual(row["yesterday_done"], 2)
        self.assertEqual(row["row_status"], "yellow")

        # 昨天全做完 → 积压 0，绿灯；今天照常派了任务没做也不影响
        _set_yesterday(["done_study"] * 5)
        row = class_overview(conn, task_date=today, now=noon)["students"][0]
        self.assertEqual(row["backlog"], 0)
        self.assertEqual(row["yesterday_done"], 5)
        self.assertEqual(row["row_status"], "green")

    def test_class_overview_yesterday_incomplete(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": "reading_synonym_u01"},
                {"item_type": "study", "unit_id": "reading_synonym_u02"},
            ],
        )
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        rows = conn.execute(
            "SELECT id FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        yesterday = "2026-09-01"
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES (?, ?, ?, 'fresh', 0, 'done_study', 1, 0)
            """,
            ("2025001", yesterday, rows[0]["id"]),
        )
        conn.execute(
            """
            INSERT INTO daily_tasks
            (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES (?, ?, ?, 'fresh', 1, 'todo', 1, 0)
            """,
            ("2025001", yesterday, rows[1]["id"]),
        )
        conn.commit()
        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)
        data = class_overview(conn, task_date="2026-09-02", now=noon)
        row = data["students"][0]
        self.assertEqual(row["yesterday_done"], 1)
        self.assertEqual(row["yesterday_total"], 2)
        self.assertTrue(row["yesterday_incomplete"])
        self.assertEqual(data["stats"]["yesterday_incomplete"], 1)

    def test_get_today_includes_upcoming_schedule(self) -> None:
        conn = _connect()
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    }
                ],
                "effective_from": china_ymd(),
            },
        )
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
                for i in range(1, 5)
            ],
            effective_from=china_ymd(),
        )
        apply_draft_to_live(conn, "2025001")
        today = get_today(conn, "2025001")
        self.assertIn("upcoming_schedule", today)
        self.assertIn("remaining_plan", today)
        self.assertGreaterEqual(len(today["remaining_plan"]), 3)
        # upcoming starts tomorrow; should advance beyond today's release
        sched = today["upcoming_schedule"] or []
        self.assertTrue(len(sched) >= 1)
        titles0 = {x["title"] for x in (sched[0].get("items") or [])}
        self.assertTrue(titles0)
        # read-only: no future daily_tasks rows materialized
        future_n = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=? AND task_date>?",
            ("2025001", china_ymd()),
        ).fetchone()["c"]
        self.assertEqual(future_n, 0)

    def test_teacher_schedule_matches_student_today_and_upcoming(self) -> None:
        """Teacher units schedule day0/day1 must match student today / upcoming day0."""
        conn = _connect()
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    }
                ],
                "effective_from": china_ymd(),
            },
        )
        draft_items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, 6)
        ]
        put_plan_draft(conn, "2025001", draft_items, effective_from=china_ymd())
        apply_draft_to_live(conn, "2025001")
        student_today = get_today(conn, "2025001")
        teacher = preview_daily_pack_items(
            conn,
            "2025001",
            draft_items,
            pack_mode=PACK_MODE_UNITS_PER_DAY,
            module_quotas=[
                {
                    "module_type": "reading_synonym",
                    "weekday_units": 1,
                    "weekend_units": 1,
                }
            ],
        )
        self.assertTrue(teacher.get("aligned"))
        sched = teacher.get("schedule") or []
        self.assertGreaterEqual(len(sched), 2)
        today_titles = {x.get("title") for x in (student_today.get("items") or [])}
        teacher_day0 = {x.get("title") for x in (sched[0].get("items") or [])}
        self.assertEqual(today_titles, teacher_day0)
        self.assertEqual(sched[0].get("source"), "actual")
        upcoming0 = {
            x.get("title")
            for x in ((student_today.get("upcoming_schedule") or [{}])[0].get("items") or [])
        }
        teacher_day1 = {x.get("title") for x in (sched[1].get("items") or [])}
        self.assertEqual(upcoming0, teacher_day1)
        self.assertFalse(today_titles & upcoming0)

    def test_upcoming_weekend_uses_pending_quota(self) -> None:
        """After pending生效日, weekend days use pending_weekend_units (not live)."""
        conn = _connect()
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    }
                ],
                "effective_from": china_ymd(),
            },
        )
        tomorrow = (
            datetime.strptime(china_ymd(), "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 2,
                    }
                ],
                "effective_from": tomorrow,
            },
        )
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
                for i in range(1, 10)
            ],
            effective_from=china_ymd(),
        )
        apply_draft_to_live(conn, "2025001")
        today = get_today(conn, "2025001")
        self.assertEqual(len(today.get("items") or []), 1)
        weekend_days = [
            d
            for d in (today.get("upcoming_schedule") or [])
            if d.get("task_date")
            and datetime.strptime(d["task_date"], "%Y-%m-%d").weekday() >= 5
        ]
        self.assertTrue(weekend_days)
        self.assertEqual(len(weekend_days[0].get("items") or []), 2)

    def test_plan_pause_requires_reason_and_blocks_daily(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 4)],
        )
        apply_draft_to_live(conn, "2025001")
        put_time_profile(
            conn,
            "2025001",
            {
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": [
                    {
                        "module_type": "reading_synonym",
                        "weekday_units": 1,
                        "weekend_units": 1,
                    }
                ],
                "effective": "today",
            },
        )
        today = china_ymd()
        tomorrow = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        day_after = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=3)
        ).strftime("%Y-%m-%d")
        with self.assertRaises(ValueError):
            put_plan_pause(
                conn,
                "2025001",
                {"pause_from": today, "resume_on": day_after, "reason": "  "},
            )
        plan = put_plan_pause(
            conn,
            "2025001",
            {
                "pause_from": today,
                "resume_on": day_after,
                "reason": "考试周请假",
            },
        )
        self.assertEqual(plan["plan_status"], "all_paused")
        self.assertTrue(plan["plan_pause"]["active"])
        self.assertEqual(plan["plan_pause"]["reason"], "考试周请假")
        daily = build_daily_tasks(conn, "2025001", today)
        self.assertEqual(daily, [])
        noon = datetime.strptime(today, "%Y-%m-%d").replace(
            hour=12, tzinfo=SHANGHAI
        )
        overview = class_overview(conn, task_date=today, now=noon)
        row = overview["students"][0]
        self.assertEqual(row["row_status"], "none")
        self.assertEqual(overview["stats"]["plan_paused"], 1)
        # Early resume
        clear_plan_pause(conn, "2025001")
        daily2 = build_daily_tasks(conn, "2025001", tomorrow)
        self.assertGreaterEqual(len(daily2), 1)

    def test_plan_pause_auto_expires_on_resume_day(self) -> None:
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "reading_synonym_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        today = china_ymd()
        resume = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        put_plan_pause(
            conn,
            "2025001",
            {"pause_from": today, "resume_on": resume, "reason": "临时有事"},
        )
        # Simulate resume day via expire helper
        from task_api import expire_plan_pause_if_due, get_plan_pause

        cleared = expire_plan_pause_if_due(conn, "2025001", on_date=resume)
        self.assertTrue(cleared)
        self.assertIsNone(get_plan_pause(conn, "2025001", on_date=resume))

    def test_gendu_assignment_daily_three_and_advance(self) -> None:
        conn = _connect()
        put_time_profile(
            conn,
            "2025001",
            {"pack_mode": PACK_MODE_UNITS_PER_DAY, "effective_from": china_ymd()},
        )
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? AND is_active=1
            ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        next_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? AND is_active=1 AND unit_no>1
            ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        today = china_ymd()
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": today}
        )
        asg = get_gendu_assignment(conn, "2025001", on_date=today)
        self.assertTrue(asg["active"])
        self.assertEqual(asg["current_unit_id"], start_unit)
        ends = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=29)
        ).strftime("%Y-%m-%d")
        self.assertEqual(asg["ends_on"], ends)

        daily = build_daily_tasks(conn, "2025001", today)
        gendu = [x for x in daily if x["module_type"] == GENDU_MODULE]
        self.assertEqual(len(gendu), 1)
        self.assertEqual(gendu[0]["unit_id"], start_unit)
        pid = gendu[0]["plan_item_id"]

        with self.assertRaises(ValueError):
            complete_study(conn, "2025001", pid, "1")

        r1 = report_gendu_practice(conn, "2025001", plan_item_id=pid, score=50)
        self.assertEqual(r1["practice_count"], 1)
        self.assertFalse(r1["day_complete"])
        self.assertFalse(r1["passed_lesson"])

        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=60)
        r3 = report_gendu_practice(conn, "2025001", plan_item_id=pid, score=75)
        self.assertEqual(r3["practice_count"], GENDU_DAILY_PRACTICES)
        self.assertTrue(r3["day_complete"])
        self.assertTrue(r3["passed_lesson"])
        self.assertGreaterEqual(r3["best_score"], GENDU_PASS_SCORE)

        daily2 = build_daily_tasks(conn, "2025001", today)
        g2 = [x for x in daily2 if x["module_type"] == GENDU_MODULE][0]
        self.assertEqual(g2["state"], "done_study")
        self.assertEqual(g2["unit_id"], start_unit)

        tomorrow = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        daily3 = build_daily_tasks(conn, "2025001", tomorrow)
        g3 = [x for x in daily3 if x["module_type"] == GENDU_MODULE]
        self.assertEqual(len(g3), 1)
        self.assertEqual(g3[0]["unit_id"], next_unit)
        asg2 = get_gendu_assignment(conn, "2025001", on_date=tomorrow)
        self.assertEqual(asg2["current_unit_id"], next_unit)
        self.assertFalse(asg2["passed_current"])

    def test_genu_practice_day_done_not_backlog(self) -> None:
        """跟读当天做满 3 次（未过 70 分关）不应计积压。"""
        conn = _connect()
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        today = china_ymd()
        tomorrow = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": today}
        )
        daily = build_daily_tasks(conn, "2025001", today)
        gendu = [x for x in daily if x["module_type"] == GENDU_MODULE][0]
        pid = gendu["plan_item_id"]
        # 做满 3 次，但分数都低于 70，未过关 → study_completed 仍为 0
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=50, task_date=today)
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=60, task_date=today)
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=62, task_date=today)
        row = conn.execute(
            "SELECT state, gendu_practice_count FROM daily_tasks "
            "WHERE student_id=? AND task_date=? AND plan_item_id=?",
            ("2025001", today, pid),
        ).fetchone()
        self.assertEqual(row["state"], "done_study")
        item = conn.execute(
            "SELECT study_completed FROM plan_items WHERE id=?", (pid,)
        ).fetchone()
        self.assertEqual(item["study_completed"], 0)
        # 官方积压口径：当日做满 → 不算积压
        self.assertEqual(
            backlog_plan_item_ids(conn, "2025001", before_date=tomorrow), []
        )

    def test_genu_practice_day_done_not_backlog_keeps_true_backlog(self) -> None:
        """跟读当日做满不计积压，但其它真正未完成的单元仍要计积压。"""
        conn = _connect()
        today = china_ymd()
        tomorrow = (datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": today}
        )
        daily = build_daily_tasks(conn, "2025001", today)
        gendu = [x for x in daily if x["module_type"] == GENDU_MODULE][0]
        pid = gendu["plan_item_id"]
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=50, task_date=today)
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=60, task_date=today)
        report_gendu_practice(conn, "2025001", plan_item_id=pid, score=62, task_date=today)
        # 手工插入一个普通未完成单元 + 昨日 daily_tasks 行，模拟真正的积压
        cur = conn.execute(
            """
            INSERT INTO plan_items (student_id, sort_order, item_type, unit_id, module_type, status)
            VALUES ('2025001', 99, 'study', 'reading_synonym_u01', 'reading_synonym', 'pending')
            """
        )
        normal_pid = cur.lastrowid
        conn.execute(
            """
            INSERT INTO daily_tasks (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
            VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 1, 0)
            """,
            (today, normal_pid),
        )
        conn.commit()
        back = backlog_plan_item_ids(conn, "2025001", before_date=tomorrow)
        # 跟读 pid 已被排除，普通未完成单元仍计 1
        self.assertNotIn(pid, back)
        self.assertIn(normal_pid, back)
        self.assertEqual(len(back), 1)
        self.assertTrue(all(x != pid for x in back))

    def test_gendu_day_counts_across_passage_swap(self) -> None:
        """回归（线上廉昕 2025114）：当天 3 次要按天累加，不能因换篇断成 1/3+1/3。

        线上：她 20:56 在第 1 篇练 1 次（73.9% 达标）→ 被立刻换到第 2 篇 →
        21:03/21:03 又练 2 次。她当天确实做满 3 次，但按课文单独算就是
        1/3 与 1/3，页面显示「未完成」。
        """
        conn = _connect()
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        next_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? AND unit_no>1 ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        today = china_ymd()
        yesterday = (
            datetime.strptime(today, "%Y-%m-%d").date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": yesterday}
        )
        self._backdate_plan_start(conn, yesterday)
        daily = build_daily_tasks(conn, "2025001", today)
        gendu = [x for x in daily if x["module_type"] == GENDU_MODULE][0]
        pid = gendu["plan_item_id"]

        # 第 1 次：达标
        r1 = report_gendu_practice(
            conn, "2025001", plan_item_id=pid, score=GENDU_PASS_SCORE + 3.9,
            task_date=today,
        )
        self.assertTrue(r1["passed_lesson"])
        self.assertEqual(r1["practice_count"], 1)

        # 模拟旧版 bug：当天被换到下一篇，之后 2 次记在新课名下
        conn.execute(
            "UPDATE student_gendu_assignment SET current_unit_id=?, passed_current=0 "
            "WHERE student_id='2025001'",
            (next_unit,),
        )
        for score in (39.7, 50.0):
            conn.execute(
                """
                INSERT INTO gendu_practice_events
                    (student_id, unit_id, plan_item_id, task_date, score)
                VALUES ('2025001', ?, ?, ?, ?)
                """,
                (next_unit, pid, today, score),
            )
        conn.commit()

        self.assertEqual(
            _gendu_day_practice_count(conn, "2025001", today), 3,
            "当天练习次数应跨课文累加",
        )
        # 当天 3 次 → 该行必须显示完成，且进度 3/3
        refreshed = build_daily_tasks(conn, "2025001", today)
        g2 = [x for x in refreshed if x["module_type"] == GENDU_MODULE]
        self.assertTrue(g2)
        self.assertEqual(g2[0]["state"], "done_study")
        self.assertEqual(g2[0]["scope_done"], GENDU_DAILY_PRACTICES)

        # 不能留假积压
        tomorrow = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        self.assertEqual(
            backlog_plan_item_ids(conn, "2025001", before_date=tomorrow), []
        )

    def test_gendu_no_advance_when_backfilling_yesterday(self) -> None:
        """回归（线上廉昕 2025114）：回填「昨日」不得触发跟读换课。

        线上实例：学生 9/17 晚把当前课跟读到 73.9%（过关），当晚系统在
        回填 9/16 的每日任务时误判「9/16 当日几乎没练」，于是**提前换课**：
        - 9/16 被塞进还没布置过的新课（幽灵任务 → 假积压）
        - 9/17 已完成的旧课记录被新单位覆盖，学生看到「未完成」
        正确行为是「次日起换课」：过关当天不换，且回填历史不得改写旧记录。
        """
        conn = _connect()
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        next_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? AND unit_no>1 ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        today = china_ymd()
        yesterday = (
            datetime.strptime(today, "%Y-%m-%d").date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        two_days_ago = (
            datetime.strptime(today, "%Y-%m-%d").date() - timedelta(days=2)
        ).strftime("%Y-%m-%d")
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": two_days_ago}
        )
        # 计划早就生效（线上廉昕 plan_items 创建于 9/06），这样「回填昨日」才不
        # 会被「不早于计划生效日」的守卫跳过，才能复现误换课。
        self._backdate_plan_start(conn, two_days_ago)
        # 线上廉昕是 units_per_day 排程，换课判定走 _build_daily_tasks_units。
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)
        build_daily_tasks(conn, "2025001", yesterday)
        today_pack = build_daily_tasks(conn, "2025001", today)
        gendu = [x for x in today_pack if x["module_type"] == GENDU_MODULE][0]
        pid = gendu["plan_item_id"]
        self.assertEqual(gendu["unit_id"], start_unit)

        # 当晚过关（>=70）。report_gendu_practice 内部会 get_today →
        # 回填 today + yesterday，旧逻辑会在回填 yesterday 时误换课。
        r = report_gendu_practice(
            conn, "2025001", plan_item_id=pid, score=GENDU_PASS_SCORE + 3.9,
            task_date=today,
        )
        self.assertTrue(r["passed_lesson"])

        # 1) 过关当天不得换课
        asg = get_gendu_assignment(conn, "2025001", on_date=today)
        self.assertEqual(
            asg["current_unit_id"], start_unit,
            "过关当天不应换课（次日起才换）",
        )
        # 2) 昨日不得出现「还没布置过的新课」
        y_rows = conn.execute(
            """
            SELECT p.unit_id FROM daily_tasks d JOIN plan_items p ON p.id=d.plan_item_id
            WHERE d.student_id='2025001' AND d.task_date=? AND p.module_type=?
            """,
            (yesterday, GENDU_MODULE),
        ).fetchall()
        y_units = [str(x["unit_id"]) for x in y_rows]
        self.assertNotIn(
            next_unit, y_units, "昨日不得被塞进当天尚未布置的新课（幽灵任务）"
        )
        # 3) 今天的跟读记录仍是旧课，且当晚练习没丢
        t_row = conn.execute(
            """
            SELECT p.unit_id, d.gendu_practice_count FROM daily_tasks d
            JOIN plan_items p ON p.id=d.plan_item_id
            WHERE d.student_id='2025001' AND d.task_date=? AND p.module_type=?
            """,
            (today, GENDU_MODULE),
        ).fetchone()
        self.assertEqual(str(t_row["unit_id"]), start_unit)
        self.assertEqual(int(t_row["gendu_practice_count"]), 1)

        # 4) 次日仍然正常换课
        tomorrow = (
            datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        tmr = build_daily_tasks(conn, "2025001", tomorrow)
        g_tmr = [x for x in tmr if x["module_type"] == GENDU_MODULE][0]
        self.assertEqual(g_tmr["unit_id"], next_unit)

    def test_backfill_skips_items_created_after_that_day(self) -> None:
        """回归（线上 2025145/2025084 等）：计划后来新增的单元不得回填到昨天。

        学生昨天根本没这批作业，补进去会变成「昨日任务未完成 / 积压」并标红。
        """
        conn = _connect()
        today = china_ymd()
        yesterday = (
            datetime.strptime(today, "%Y-%m-%d").date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        # 昨天已生效的旧单元
        conn.execute(
            """
            INSERT INTO plan_items
                (student_id, sort_order, item_type, unit_id, module_type,
                 status, created_at, updated_at)
            VALUES ('2025001', 0, 'study', 'reading_synonym_u01', 'reading_synonym',
                    'pending', ?, ?)
            """,
            (f"{yesterday}T02:00:00.000Z", f"{yesterday}T02:00:00.000Z"),
        )
        # 今天新增的单元（created_at 就是今天）
        conn.execute(
            """
            INSERT INTO plan_items
                (student_id, sort_order, item_type, unit_id, module_type,
                 status, created_at, updated_at)
            VALUES ('2025001', 1, 'study', 'reading_synonym_u02', 'reading_synonym',
                    'pending', strftime('%Y-%m-%dT%H:%M:%fZ','now'),
                    strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            """
        )
        conn.commit()

        # 每日 2 个单元：今天才能「补做 u01 + 排进 u02」同时成立
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)

        build_daily_tasks(conn, "2025001", yesterday)
        y_units = [
            str(r["unit_id"])
            for r in conn.execute(
                """
                SELECT p.unit_id FROM daily_tasks d
                JOIN plan_items p ON p.id = d.plan_item_id
                WHERE d.student_id='2025001' AND d.task_date=?
                """,
                (yesterday,),
            ).fetchall()
        ]
        self.assertIn("reading_synonym_u01", y_units)
        self.assertNotIn(
            "reading_synonym_u02", y_units,
            "当天新增的单元不得被回填到昨天（幽灵任务 → 假积压）",
        )
        # 今天照常排进来
        build_daily_tasks(conn, "2025001", today)
        t_units = [
            str(r["unit_id"])
            for r in conn.execute(
                """
                SELECT p.unit_id FROM daily_tasks d
                JOIN plan_items p ON p.id = d.plan_item_id
                WHERE d.student_id='2025001' AND d.task_date=?
                """,
                (today,),
            ).fetchall()
        ]
        self.assertIn("reading_synonym_u02", t_units)

    def test_gendu_assignment_expires_stops_pack(self) -> None:
        conn = _connect()
        put_time_profile(
            conn,
            "2025001",
            {"pack_mode": PACK_MODE_UNITS_PER_DAY, "effective_from": china_ymd()},
        )
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        start = "2026-01-01"
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": start}
        )
        after = "2026-02-01"  # day 32, outside 30-day window
        daily = build_daily_tasks(conn, "2025001", after)
        self.assertFalse(any(x["module_type"] == GENDU_MODULE for x in daily))
        asg = get_gendu_assignment(conn, "2025001", on_date=after)
        self.assertTrue(asg["expired"])

    def test_gendu_clear_assignment(self) -> None:
        conn = _connect()
        start_unit = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 1
            """,
            (GENDU_MODULE,),
        ).fetchone()["unit_id"]
        put_gendu_assignment(conn, "2025001", {"start_unit_id": start_unit})
        clear_gendu_assignment(conn, "2025001")
        self.assertIsNone(get_gendu_assignment(conn, "2025001"))

    def test_gendu_sync_from_plan_draft(self) -> None:
        """单元库保存清单后自动生成跟读作业；清单只保留当前起始课。"""
        conn = _connect()
        units = conn.execute(
            """
            SELECT unit_id FROM task_units
            WHERE module_type=? ORDER BY unit_no LIMIT 3
            """,
            (GENDU_MODULE,),
        ).fetchall()
        self.assertGreaterEqual(len(units), 2)
        u0, u1 = units[0]["unit_id"], units[1]["unit_id"]
        put_plan_draft(
            conn,
            "2025001",
            [
                {"item_type": "study", "unit_id": u0},
                {"item_type": "study", "unit_id": u1},
            ],
            effective_from=china_ymd(),
        )
        asg = get_gendu_assignment(conn, "2025001")
        self.assertIsNotNone(asg)
        self.assertEqual(asg["start_unit_id"], u0)
        self.assertEqual(asg["current_unit_id"], u0)
        pending = conn.execute(
            """
            SELECT unit_id FROM plan_items
            WHERE student_id=? AND module_type=? AND status='pending'
            ORDER BY sort_order
            """,
            ("2025001", GENDU_MODULE),
        ).fetchall()
        self.assertEqual([r["unit_id"] for r in pending], [u0])

    def test_complete_study_backfills_yesterday_daily_task(self) -> None:
        """复现：跨零点做完长难句，昨日 daily_tasks 仍停在 todo。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "sentence_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='sentence_u01'"
        ).fetchone()
        pid = int(item["id"])
        unit = conn.execute(
            "SELECT content_ref FROM task_units WHERE unit_id='sentence_u01'"
        ).fetchone()
        ref = unit["content_ref"]
        if isinstance(ref, str):
            import json as _json

            ref = _json.loads(ref)
        total = int((ref or {}).get("scope_total") or 0)
        self.assertGreater(total, 0)

        today = china_ymd()
        yesterday = (
            datetime.strptime(today, "%Y-%m-%d").date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        # 模拟：任务原挂在昨天，过零点后学生补做完
        for day in (yesterday, today):
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked)
                VALUES ('2025001', ?, ?, 'fresh', 0, 'todo', 0)
                """,
                (day, pid),
            )
        conn.commit()

        update_scope_progress(conn, "2025001", pid, scope_done=total)
        complete_study(conn, "2025001", pid, "1")

        rows = conn.execute(
            """
            SELECT task_date, state FROM daily_tasks
            WHERE student_id='2025001' AND plan_item_id=?
            ORDER BY task_date
            """,
            (pid,),
        ).fetchall()
        by_day = {r["task_date"]: r["state"] for r in rows}
        self.assertEqual(by_day.get(yesterday), "done_study")
        self.assertEqual(by_day.get(today), "done_study")
        plan = conn.execute(
            "SELECT study_completed FROM plan_items WHERE id=?", (pid,)
        ).fetchone()
        self.assertEqual(int(plan["study_completed"]), 1)

    def test_complete_study_accepts_inline_scope_done_race(self) -> None:
        """复现：进度 postMessage 尚未落库就打勾 → 旧逻辑报「当前 0/N」。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "sentence_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='sentence_u01'"
        ).fetchone()
        pid = int(item["id"])
        unit = conn.execute(
            "SELECT content_ref FROM task_units WHERE unit_id='sentence_u01'"
        ).fetchone()
        ref = unit["content_ref"]
        if isinstance(ref, str):
            import json as _json

            ref = _json.loads(ref)
        total = int((ref or {}).get("scope_total") or 0)
        self.assertGreater(total, 0)

        # 旧竞态：库里还是 0，直接 complete → 应失败
        with self.assertRaises(ValueError) as ctx:
            complete_study(conn, "2025001", pid, "1")
        self.assertIn(f"当前 0/{total}", str(ctx.exception))

        # 新路径：同一请求带上最终 scope_done，原子落库并打勾
        complete_study(conn, "2025001", pid, "1", scope_done=total)
        prog = conn.execute(
            """
            SELECT scope_done FROM task_unit_progress
            WHERE student_id='2025001' AND plan_item_id=?
            """,
            (pid,),
        ).fetchone()
        self.assertEqual(int(prog["scope_done"]), total)
        plan = conn.execute(
            "SELECT study_completed FROM plan_items WHERE id=?", (pid,)
        ).fetchone()
        self.assertEqual(int(plan["study_completed"]), 1)

    def test_complete_study_race_insufficient_scope_still_rejected(self) -> None:
        """带 scope_done 也不能少做：未满仍拒绝。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "writing_translate_u01"}],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='writing_translate_u01'"
        ).fetchone()
        pid = int(item["id"])
        unit = conn.execute(
            "SELECT content_ref FROM task_units WHERE unit_id='writing_translate_u01'"
        ).fetchone()
        ref = unit["content_ref"]
        if isinstance(ref, str):
            import json as _json

            ref = _json.loads(ref)
        total = int((ref or {}).get("scope_total") or 0)
        self.assertGreater(total, 1)
        with self.assertRaises(ValueError) as ctx:
            complete_study(conn, "2025001", pid, "1", scope_done=total - 1)
        self.assertIn(f"当前 {total - 1}/{total}", str(ctx.exception))

    def test_scope_progress_never_decreases_and_keeps_sentence_keys(self) -> None:
        """重进页面从 1 重报时，不能把已经做过的句数盖掉；句号要累加。"""
        conn = _connect()
        put_plan_draft(
            conn,
            "2025001",
            [{"item_type": "study", "unit_id": "sentence_u02"}],
        )
        apply_draft_to_live(conn, "2025001")
        item = conn.execute(
            "SELECT id FROM plan_items WHERE unit_id='sentence_u02'"
        ).fetchone()
        pid = int(item["id"])
        first = update_scope_progress(conn, "2025001", pid, scope_done=3)
        self.assertEqual(first["scope_done"], 3)
        again = update_scope_progress(conn, "2025001", pid, scope_done=1)
        self.assertEqual(again["scope_done"], 3)
        # 旧数据只有数字：补报第 9 句时，先按单元顺序认前 3 句，再累加第 9 句
        added = update_scope_progress(conn, "2025001", pid, scope_key="9", scope_done=1)
        self.assertEqual(added["scope_keys"], ["6", "7", "8", "9"])
        self.assertEqual(added["scope_done"], 4)
        done = update_scope_progress(conn, "2025001", pid, scope_key="10", scope_done=2)
        self.assertEqual(done["scope_done"], 5)
        self.assertEqual(done["scope_keys"], ["6", "7", "8", "9", "10"])
        complete_study(conn, "2025001", pid, "1", scope_done=2)
        plan = conn.execute(
            "SELECT study_completed FROM plan_items WHERE id=?", (pid,)
        ).fetchone()
        self.assertEqual(int(plan["study_completed"]), 1)


if __name__ == "__main__":
    unittest.main()
