# -*- coding: utf-8 -*-
"""入学摸底 · 访客提交（无需正式学号）。"""
from __future__ import annotations

import json
import re
from typing import Any

from student_api import dumps_details, utc_now

_NAME_RE = re.compile(r"\s+")


def ensure_placement_guest_table(conn: Any) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS placement_guest_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            contact TEXT DEFAULT '',
            target_score REAL DEFAULT 6.5,
            form_id TEXT DEFAULT 'A',
            overall_label TEXT DEFAULT '',
            score_percent REAL DEFAULT 0,
            duration_seconds INTEGER DEFAULT 0,
            summary TEXT DEFAULT '',
            report_json TEXT DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_placement_guest_created
        ON placement_guest_results(created_at DESC)
        """
    )
    conn.commit()


def _clean_text(value: Any, max_len: int) -> str:
    s = _NAME_RE.sub(" ", str(value or "").strip())
    if len(s) > max_len:
        s = s[:max_len]
    return s


def insert_placement_guest(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    ensure_placement_guest_table(conn)
    name = _clean_text(payload.get("guest_name") or payload.get("name"), 40)
    if not name:
        raise ValueError("请填写姓名")
    contact = _clean_text(payload.get("contact"), 80)
    try:
        target = float(payload.get("target_score") or 6.5)
    except (TypeError, ValueError):
        target = 6.5
    if target not in (5.0, 5.5, 6.0, 6.5, 7.0, 7.5):
        target = 6.5
    report = payload.get("report") if isinstance(payload.get("report"), dict) else {}
    bands = report.get("bands") if isinstance(report.get("bands"), dict) else {}
    overall = report.get("overall") if isinstance(report.get("overall"), dict) else {}
    overall_label = str(overall.get("label") or payload.get("overall_label") or "")
    try:
        score_percent = float(payload.get("score_percent") or report.get("scorePercent") or 0)
    except (TypeError, ValueError):
        score_percent = 0.0
    try:
        duration = max(0, int(round(float(payload.get("duration_seconds") or 0))))
    except (TypeError, ValueError):
        duration = 0
    summary = _clean_text(payload.get("summary") or report.get("summary"), 500)
    form_id = _clean_text(payload.get("form") or report.get("form") or "A", 8) or "A"
    now = utc_now()
    cur = conn.execute(
        """
        INSERT INTO placement_guest_results (
            guest_name, contact, target_score, form_id, overall_label,
            score_percent, duration_seconds, summary, report_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            contact,
            target,
            form_id,
            overall_label,
            score_percent,
            duration,
            summary,
            dumps_details(report if report else {
                "bands": bands,
                "overall": overall,
                "tiers": report.get("tiers"),
            }),
            now,
        ),
    )
    conn.commit()
    return {
        "id": cur.lastrowid,
        "guest_name": name,
        "contact": contact,
        "target_score": target,
        "form_id": form_id,
        "overall_label": overall_label,
        "score_percent": score_percent,
        "duration_seconds": duration,
        "summary": summary,
        "created_at": now,
    }


def list_placement_guests(conn: Any, limit: int = 200) -> list[dict[str, Any]]:
    ensure_placement_guest_table(conn)
    limit = max(1, min(int(limit or 200), 1000))
    rows = conn.execute(
        """
        SELECT id, guest_name, contact, target_score, form_id, overall_label,
               score_percent, duration_seconds, summary, report_json, created_at
        FROM placement_guest_results
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        raw = item.pop("report_json", None)
        try:
            item["report"] = json.loads(raw) if isinstance(raw, str) else (raw or {})
        except json.JSONDecodeError:
            item["report"] = {}
        out.append(item)
    return out
