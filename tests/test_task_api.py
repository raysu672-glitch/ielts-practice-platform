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
    apply_draft_to_live,
    backlog_plan_item_ids,
    build_daily_tasks,
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
            "writing_phrase": 14,
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
        low = preview_daily_pack_items(
            conn, "2025001", items, weekday_minutes=40, weekend_minutes=90
        )
        high = preview_daily_pack_items(
            conn, "2025001", items, weekday_minutes=120, weekend_minutes=90
        )
        self.assertEqual(low["budget_minutes"], 40)
        self.assertEqual(high["budget_minutes"], 120)
        self.assertGreater(len(high["items"]), len(low["items"]))

    def test_save_duration_today_rebuilds_daily_budget(self) -> None:
        conn = _connect()
        items = [{"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 9)]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
        put_time_profile(
            conn, "2025001", {"weekday_minutes": 40, "weekend_minutes": 90, "effective": "today"}
        )
        day = china_ymd()
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
        self.assertEqual(today["budget_minutes"], 120)
        self.assertGreater(len(daily120), len(daily40))

    def _apply_reading_plan(self, conn: sqlite3.Connection, count: int) -> None:
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"}
            for i in range(1, count + 1)
        ]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")

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
        daily = build_daily_tasks(conn, "2025001", day)
        self.assertEqual(len(daily), 3)
        modules = [d["module_type"] for d in daily]
        self.assertEqual(modules.count("reading_synonym"), 2)
        self.assertEqual(modules.count("dictation"), 1)

    def test_units_mode_backlog_capped_by_quota(self) -> None:
        """Unfinished weekend/heavy day must not dump all onto a smaller weekday."""
        conn = _connect()
        self._apply_reading_plan(conn, 5)
        self._enable_units_mode(conn, weekday_units=3, weekend_units=3)
        day1 = "2026-08-25"
        build_daily_tasks(conn, "2025001", day1)
        self._enable_units_mode(conn, weekday_units=2, weekend_units=2)
        day2 = "2026-08-26"
        daily2 = build_daily_tasks(conn, "2025001", day2)
        self.assertEqual(len(daily2), 2)
        self.assertTrue(all(d["priority_class"] == "carry_over" for d in daily2))
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001")), 3)

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
        self.assertEqual(len(backlog_plan_item_ids(conn, "2025001")), 6)

    def test_units_mode_weekend_quota(self) -> None:
        conn = _connect()
        self._apply_reading_plan(conn, 4)
        self._enable_units_mode(conn, weekday_units=2, weekend_units=1)
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
        before_daily = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001'"
        ).fetchone()["c"]
        data = class_overview(conn, task_date=day, now=noon)
        after_daily = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id='2025001'"
        ).fetchone()["c"]
        self.assertEqual(before_daily, after_daily)
        row = data["students"][0]
        self.assertEqual(row["today_total"], 3)
        # done_fail does not count as done
        self.assertEqual(row["today_done"], 1)
        self.assertEqual(row["test_fail"], 1)
        self.assertTrue(any(b["label"] == "阅" for b in row["plan_progress_brief"]))

    def test_class_overview_backlog_red(self) -> None:
        conn = _connect()
        items = [
            {"item_type": "study", "unit_id": f"reading_synonym_u{i:02d}"} for i in range(1, 5)
        ]
        put_plan_draft(conn, "2025001", items)
        apply_draft_to_live(conn, "2025001")
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


if __name__ == "__main__":
    unittest.main()
