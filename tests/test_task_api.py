"""Unit tests for task system MVP (boxing, tomorrow生效, progress X/Y)."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from task_api import (  # noqa: E402
    SHANGHAI,
    _interleave_by_module,
    apply_draft_to_live,
    build_daily_tasks,
    china_ymd,
    complete_study,
    ensure_task_tables,
    get_plan,
    get_today,
    insert_stage_test,
    normalize_stage_test_positions,
    preview_daily_pack_items,
    put_plan_draft,
    put_time_profile,
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
        n_read = conn.execute(
            "SELECT COUNT(*) AS c FROM task_units WHERE module_type='reading_synonym'"
        ).fetchone()["c"]
        n_dict = conn.execute(
            "SELECT COUNT(*) AS c FROM task_units WHERE module_type='dictation'"
        ).fetchone()["c"]
        self.assertEqual(n_read, 23)
        self.assertEqual(n_dict, 50)
        u23 = conn.execute(
            "SELECT content_ref FROM task_units WHERE unit_id='reading_synonym_u23'"
        ).fetchone()
        self.assertIn('"scope_total": 5', u23["content_ref"])

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


if __name__ == "__main__":
    unittest.main()
