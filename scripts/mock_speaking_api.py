"""口语模考（Mock Speaking）数据表与文件存储"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

DEFAULT_RETENTION_DAYS = 90


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def ensure_mock_speaking_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS mock_speaking_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            status TEXT NOT NULL DEFAULT 'started' CHECK (status IN ('started','submitted','abandoned')),
            p1_json TEXT NOT NULL DEFAULT '[]',
            p2_json TEXT NOT NULL DEFAULT '{}',
            p3_json TEXT NOT NULL DEFAULT '[]',
            audio_path TEXT,
            duration_seconds INTEGER DEFAULT 0,
            overall_band REAL,
            fc REAL,
            lr REAL,
            gra REAL,
            pron REAL,
            report_json TEXT NOT NULL DEFAULT '{}',
            started_at TEXT NOT NULL,
            ended_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_mock_speaking_student ON mock_speaking_exams(student_id);
        CREATE INDEX IF NOT EXISTS idx_mock_speaking_status ON mock_speaking_exams(status);
        CREATE INDEX IF NOT EXISTS idx_mock_speaking_created_at ON mock_speaking_exams(created_at DESC);
        """
    )


def create_mock_exam(
    conn: sqlite3.Connection,
    student_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    now = utc_now()
    cur = conn.execute(
        """
        INSERT INTO mock_speaking_exams (
            student_id, status, p1_json, p2_json, p3_json,
            started_at, created_at, updated_at
        ) VALUES (?, 'started', ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            json.dumps(payload.get("p1") or [], ensure_ascii=False),
            json.dumps(payload.get("p2") or {}, ensure_ascii=False),
            json.dumps(payload.get("p3") or [], ensure_ascii=False),
            payload.get("started_at") or now,
            now,
            now,
        ),
    )
    conn.commit()
    return {"exam_id": cur.lastrowid, "status": "started"}


def get_mock_exam(conn: sqlite3.Connection, exam_id: int, student_id: str) -> Optional[dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM mock_speaking_exams WHERE id = ? AND student_id = ?",
        (exam_id, student_id),
    ).fetchone()
    if not row:
        return None
    item = dict(row)
    for key in ("p1_json", "p2_json", "p3_json", "report_json"):
        try:
            item[key.replace("_json", "")] = json.loads(item.get(key) or ("[]" if key != "p2_json" and key != "report_json" else "{}"))
        except json.JSONDecodeError:
            item[key.replace("_json", "")] = [] if key != "p2_json" and key != "report_json" else {}
    return item


def save_mock_audio(
    conn: sqlite3.Connection,
    exam_id: int,
    student_id: str,
    audio_bytes: bytes,
    audio_dir: Path,
) -> str:
    exam = get_mock_exam(conn, exam_id, student_id)
    if not exam:
        raise ValueError("模考记录不存在")
    audio_dir.mkdir(parents=True, exist_ok=True)
    filename = f"mock_{exam_id}_{int(time.time())}.webm"
    path = audio_dir / filename
    path.write_bytes(audio_bytes)
    rel = str(path.relative_to(audio_dir.parent))
    now = utc_now()
    conn.execute(
        "UPDATE mock_speaking_exams SET audio_path = ?, updated_at = ? WHERE id = ?",
        (rel, now, exam_id),
    )
    conn.commit()
    return rel


def submit_mock_exam(
    conn: sqlite3.Connection,
    exam_id: int,
    student_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    exam = get_mock_exam(conn, exam_id, student_id)
    if not exam:
        raise ValueError("模考记录不存在")
    now = utc_now()
    segments = payload.get("segments") or []
    duration = int(payload.get("duration_seconds") or 0)
    # MVP：先不算综合 Band，留空由后续 AI 评分填充
    conn.execute(
        """
        UPDATE mock_speaking_exams
        SET status = 'submitted',
            duration_seconds = ?,
            report_json = ?,
            ended_at = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            duration,
            json.dumps({"segments": segments}, ensure_ascii=False),
            payload.get("ended_at") or now,
            now,
            exam_id,
        ),
    )
    conn.commit()
    return {"exam_id": exam_id, "status": "submitted"}


def list_student_mock_exams(conn: sqlite3.Connection, student_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT id, status, duration_seconds, overall_band, fc, lr, gra, pron,
               started_at, ended_at, created_at
        FROM mock_speaking_exams
        WHERE student_id = ?
        ORDER BY created_at DESC
        """,
        (student_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def list_teacher_mock_exams(conn: sqlite3.Connection, student_id: str) -> list[dict[str, Any]]:
    return list_student_mock_exams(conn, student_id)


def cleanup_old_audio(db_path: Path, audio_dir: Path, days: int = DEFAULT_RETENTION_DAYS) -> int:
    """删除超期音频文件，返回删除数量"""
    cutoff = time.time() - days * 86400
    removed = 0
    if not audio_dir.exists():
        return 0
    for path in audio_dir.glob("mock_*.webm"):
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
                removed += 1
        except OSError:
            pass
    return removed
