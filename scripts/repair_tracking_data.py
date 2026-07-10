#!/usr/bin/env python3
"""Repair legacy duplicate tracking rows without touching student accounts."""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = ROOT / "data" / "ielts_local.db"


def parse_timestamp(value: Any) -> datetime:
    text = str(value or "").strip()
    if not text:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def details_are_empty(value: Any) -> bool:
    if value in (None, "", "[]"):
        return True
    try:
        return json.loads(value) == [] if isinstance(value, str) else value == []
    except (TypeError, json.JSONDecodeError):
        return False


def cluster_rows(
    rows: Iterable[sqlite3.Row],
    key_fields: tuple[str, ...],
    max_gap_seconds: int = 2,
) -> list[list[sqlite3.Row]]:
    grouped: dict[tuple[Any, ...], list[sqlite3.Row]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[field] for field in key_fields)].append(row)

    clusters: list[list[sqlite3.Row]] = []
    for group in grouped.values():
        ordered = sorted(group, key=lambda row: (parse_timestamp(row["created_at"]), row["id"]))
        current: list[sqlite3.Row] = []
        for row in ordered:
            if current:
                gap = (parse_timestamp(row["created_at"]) - parse_timestamp(current[-1]["created_at"])).total_seconds()
                if gap > max_gap_seconds:
                    clusters.append(current)
                    current = []
            current.append(row)
        if current:
            clusters.append(current)
    return clusters


def study_activity_score(row: sqlite3.Row) -> tuple[int, int, int, int]:
    activity = sum(
        max(0, int(row[field] or 0))
        for field in ("words_tested", "initial_correct", "initial_wrong", "groups_completed")
    )
    return (
        activity,
        1 if row["started_at"] else 0,
        max(0, int(row["duration_seconds"] or 0)),
        -int(row["id"]),
    )


def duplicate_study_ids(conn: sqlite3.Connection) -> list[int]:
    rows = conn.execute(
        """
        SELECT id, student_id, module_type, session_kind, duration_seconds,
               words_tested, initial_correct, initial_wrong, groups_completed,
               started_at, ended_at, created_at
        FROM study_sessions
        WHERE session_kind IS NULL OR session_kind = 'study'
        ORDER BY student_id, module_type, created_at, id
        """
    ).fetchall()
    delete_ids: list[int] = []
    for cluster in cluster_rows(rows, ("student_id", "module_type", "session_kind")):
        if len(cluster) < 2:
            continue
        has_missing_start = any(not row["started_at"] for row in cluster)
        signatures = {
            (
                int(row["duration_seconds"] or 0),
                int(row["words_tested"] or 0),
                int(row["initial_correct"] or 0),
                int(row["initial_wrong"] or 0),
                int(row["groups_completed"] or 0),
            )
            for row in cluster
        }
        if not has_missing_start and len(signatures) != 1:
            continue
        winner = max(cluster, key=study_activity_score)
        delete_ids.extend(int(row["id"]) for row in cluster if row["id"] != winner["id"])
    return sorted(set(delete_ids))


def legacy_incomplete_test_ids(conn: sqlite3.Connection) -> list[int]:
    rows = conn.execute(
        """
        SELECT id, student_id, module_type, test_type, score, correct_count,
               total_count, duration_seconds, details, started_at, created_at
        FROM test_records
        WHERE module_type = 'reading_synonym' AND test_type = 'module_test'
        ORDER BY student_id, created_at, id
        """
    ).fetchall()
    delete_ids: list[int] = []
    key_fields = ("student_id", "module_type", "test_type", "score", "correct_count", "total_count")
    for cluster in cluster_rows(rows, key_fields):
        if len(cluster) < 2:
            continue
        durations = [max(0, int(row["duration_seconds"] or 0)) for row in cluster]
        if max(durations) - min(durations) > 2:
            continue
        if all(details_are_empty(row["details"]) for row in cluster):
            delete_ids.extend(int(row["id"]) for row in cluster)
    return sorted(set(delete_ids))


def build_repair_plan(conn: sqlite3.Connection) -> dict[str, list[int]]:
    test_session_ids = [
        int(row["id"])
        for row in conn.execute("SELECT id FROM study_sessions WHERE session_kind = 'test'").fetchall()
    ]
    return {
        "test_session_ids": sorted(test_session_ids),
        "duplicate_study_ids": duplicate_study_ids(conn),
        "legacy_incomplete_test_ids": legacy_incomplete_test_ids(conn),
    }


def delete_study_session_ids(conn: sqlite3.Connection, ids: list[int]) -> None:
    if not ids:
        return
    conn.executemany("DELETE FROM study_sessions WHERE id = ?", [(item_id,) for item_id in ids])


def delete_test_record_ids(conn: sqlite3.Connection, ids: list[int]) -> None:
    if not ids:
        return
    conn.executemany("DELETE FROM test_records WHERE id = ?", [(item_id,) for item_id in ids])


def apply_repair(conn: sqlite3.Connection, plan: dict[str, list[int]]) -> None:
    delete_study_session_ids(conn, plan["test_session_ids"])
    delete_study_session_ids(conn, plan["duplicate_study_ids"])
    delete_test_record_ids(conn, plan["legacy_incomplete_test_ids"])
    conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair legacy IELTS tracking rows")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--apply", action="store_true", help="Apply the repair; default is dry-run")
    parser.add_argument("--no-backup", action="store_true", help="Skip the sidecar database backup")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = args.db.resolve()
    if not db_path.is_file():
        raise SystemExit(f"database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        plan = build_repair_plan(conn)
        summary = {key: len(value) for key, value in plan.items()}
        print(
            json.dumps(
                {"mode": "apply" if args.apply else "dry-run", "summary": summary, "ids": plan},
                ensure_ascii=False,
            )
        )
        if not args.apply:
            return 0

        if not args.no_backup:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = db_path.with_name(f"{db_path.name}.tracking_fix_{stamp}.bak")
            shutil.copy2(db_path, backup_path)
            print(f"backup={backup_path}")
        apply_repair(conn, plan)
        print("repair=complete")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
