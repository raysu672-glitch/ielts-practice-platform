"""新版学习路线（试验）：给学生端进度图提供原始事实。

只读、不改任何旧系统数据。三层进度（单元 → 科目阶段 → 总路线）和掌握度
都在前端 ``sources/v2-progress/progress_model.js`` 里由同一套规则推导，
服务端只负责把「计划清单 + 阶段测尝试记录」原样交出去，避免两处口径漂移。

口径约束（见 ``docs/v2-pass-system-rules.md``）：
- 总路线 = 旧系统该生的 live 计划清单（``plan_items`` 未移除条目）。
- 过关证据只来自测试；``study_completed``（学完打勾）原样带出，前端只作「已学」标记。
- ``plan_items.test_passed`` 会在助教重新应用清单时被清零，所以过关证据以
  ``test_records`` 为准；它没有 plan_item_id，只能按（科目, 阶段测标题）对上。
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from task_api import _parse_json_list, ensure_task_tables

FALLBACK_MODULE_NAMES = {
    "dictation": "听力1000词",
    "listening_basic": "听力基础词汇",
    "reading_synonym": "阅读同义替换",
    "listening_synonym": "听力同义替换",
    "sentence": "长难句分析",
    "writing_phrase": "写作词伙",
    "writing_translate": "写作句子翻译",
    "speaking_p1": "口语P1",
    "speaking_complex": "口语复合句",
    "listening_p4_speed": "听力P4跟读",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _module_names(conn: sqlite3.Connection) -> dict[str, str]:
    names = dict(FALLBACK_MODULE_NAMES)
    try:
        for row in conn.execute("SELECT module_type, module_name FROM pass_standards"):
            if row["module_type"] and row["module_name"]:
                names[str(row["module_type"])] = str(row["module_name"])
    except sqlite3.OperationalError:
        pass
    return names


def build_route_facts(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    ensure_task_tables(conn)
    sid = str(student_id or "").strip()
    student = conn.execute(
        "SELECT student_id, name, target_score FROM students WHERE student_id=?",
        (sid,),
    ).fetchone()

    plan_rows = conn.execute(
        """
        SELECT p.id, p.sort_order, p.item_type, p.unit_id, p.module_type,
               p.test_unit_ids, p.test_title, p.status, p.study_completed,
               p.test_passed, p.created_at, u.title AS unit_title, u.unit_no
        FROM plan_items p
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE p.student_id=? AND p.status!='removed'
        ORDER BY p.sort_order, p.id
        """,
        (sid,),
    ).fetchall()
    plan_items = []
    applied_at = None
    for r in plan_rows:
        created = r["created_at"]
        if created and (applied_at is None or created > applied_at):
            applied_at = created
        plan_items.append(
            {
                "id": int(r["id"]),
                "sort_order": int(r["sort_order"] or 0),
                "item_type": r["item_type"],
                "unit_id": r["unit_id"],
                "unit_title": r["unit_title"],
                "unit_no": r["unit_no"],
                "module_type": r["module_type"] or "",
                "test_unit_ids": _parse_json_list(r["test_unit_ids"]),
                "test_title": r["test_title"] or "",
                "status": r["status"],
                "study_completed": bool(r["study_completed"]),
                "test_passed": bool(r["test_passed"]),
            }
        )

    attempts = [
        {
            "id": int(r["id"]),
            "module_type": r["module_type"] or "",
            "test_title": r["module_name"] or "",
            "score": float(r["score"]),
            "threshold": float(r["pass_threshold"]),
            "passed": bool(r["is_passed"]),
            "at": r["created_at"],
        }
        for r in conn.execute(
            """
            SELECT id, module_type, module_name, score, is_passed, pass_threshold, created_at
            FROM test_records
            WHERE student_id=? AND test_type='stage_test'
            ORDER BY created_at, id
            """,
            (sid,),
        ).fetchall()
    ]

    meta = conn.execute(
        "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
        (sid,),
    ).fetchone()
    draft_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=? AND status!='removed'",
        (sid,),
    ).fetchone()["c"]

    return {
        "source": "platform_db",
        "server_time": _utc_now_iso(),
        "student": {
            "id": sid,
            "name": student["name"] if student else "",
            "target_score": float(student["target_score"]) if student and student["target_score"] is not None else None,
        },
        "module_names": _module_names(conn),
        "plan_items": plan_items,
        "test_attempts": attempts,
        "plan_meta": {
            "applied_at": applied_at,
            "draft_pending": bool(draft_n),
            "draft_saved_ymd": meta["saved_ymd"] if meta and draft_n else None,
            "draft_effective_from": meta["effective_from"] if meta and draft_n else None,
        },
    }
