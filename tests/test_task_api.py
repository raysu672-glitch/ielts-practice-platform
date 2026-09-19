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
    SHANGHAI,
    GENDU_DAILY_PRACTICES,
    GENDU_MODULE,
    GENDU_PASS_SCORE,
    _interleave_by_module,
    _plan_progress_brief,
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
    get_gendu_assignment,
    get_plan,
    get_today,
    insert_stage_test,
    is_weekend,
    LISTENING_GENDU_LESSONS,
    normalize_stage_test_positions,
    preview_daily_pack_items,
    put_gendu_assignment,
    put_plan_draft,
    put_plan_pause,
    put_time_profile,
    report_gendu_practice,
    seed_mvp_units,
    submit_stage_test,
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
        self.assertIn("test_url: '../P4gendu/index.html?part=p4'", modules_js)
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
        put_time_profile(
            conn, "2025001", {"weekday_minutes": 90, "weekend_minutes": 90, "effective": "today"}
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
        # 90 * 1.15 = 103.5 → expect alternating dict/read while budget allows
        self.assertGreaterEqual(len(module_seq), 3)
        if len(module_seq) >= 4:
            self.assertNotEqual(module_seq[0], module_seq[1])
            self.assertNotEqual(module_seq[1], module_seq[2])
        # First item still from earliest module block (dictation added first)
        self.assertEqual(module_seq[0], "dictation")

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

    def test_pack_preview_uses_weekday_override(self) -> None:
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
        self.assertEqual(low["budget_minutes"], 40)
        self.assertEqual(high["budget_minutes"], 120)
        self.assertGreater(len(high["items"]), len(low["items"]))

    def test_save_duration_today_rebuilds_daily_budget(self) -> None:
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
        self.assertGreater(len(daily120), len(daily40))

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
        self.assertTrue(all(d["priority_class"] == "carry_over" for d in daily2))
        # As of day2: day1's 3 unfinished count; day2's in-progress do not add extra.
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001", before_date=day2)), 3)
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001", before_date="2026-08-27")), 3)

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

    def test_pack_mode_defaults_time_budget(self) -> None:
        conn = _connect()
        profile = get_plan(conn, "2025001")["time_profile"]
        self.assertEqual(profile.get("pack_mode"), PACK_MODE_TIME_BUDGET)

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
        yday = "2026-09-01"
        yday_n = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001' AND task_date=?",
            (yday,),
        ).fetchone()["c"]
        self.assertGreater(yday_n, 0)
        row = data["students"][0]
        self.assertEqual(row["today_total"], 3)
        # done_fail does not count as done
        self.assertEqual(row["today_done"], 1)
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

    def test_class_overview_backlog_red(self) -> None:
        conn = _connect()
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 5)
        ]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        self._backdate_plan_start(conn, "2026-08-01")
        rows = conn.execute(
            "SELECT id FROM plan_items WHERE student_id='2025001' ORDER BY sort_order"
        ).fetchall()
        yesterday = "2026-09-01"
        for i, r in enumerate(rows[:3]):
            conn.execute(
                """
                INSERT INTO daily_tasks
                (student_id, task_date, plan_item_id, priority_class, sort_in_day, state, locked, forced)
                VALUES (?, ?, ?, 'fresh', ?, 'todo', 1, 0)
                """,
                ("2025001", yesterday, r["id"], i),
            )
        conn.commit()
        noon = datetime(2026, 9, 2, 12, 0, tzinfo=SHANGHAI)
        data = class_overview(conn, task_date="2026-09-02", now=noon)
        row = data["students"][0]
        self.assertGreaterEqual(row["backlog"], 3)
        self.assertEqual(row["row_status"], "red")

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
        today = "2026-09-15"
        put_gendu_assignment(
            conn, "2025001", {"start_unit_id": start_unit, "starts_on": today}
        )
        self._backdate_plan_start(conn, "2026-09-01")
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
            backlog_plan_item_ids(conn, "2025001", before_date="2026-09-16"), []
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


if __name__ == "__main__":
    unittest.main()
