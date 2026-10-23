"""Teacher-scoped API helpers (session identity is enforced by the caller)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo


from password_utils import (
    STUDENT_INITIAL_PASSWORD,
    TEACHER_INITIAL_PASSWORD,
    hash_password,
)

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def parse_details(item: dict[str, Any]) -> None:
    details = item.get("details")
    if isinstance(details, str):
        try:
            item["details"] = json.loads(details)
        except json.JSONDecodeError:
            pass


def public_student_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "student_id": row.get("student_id"),
        "name": row.get("name"),
        "is_password_changed": bool(row.get("is_password_changed")),
        "target_score": row.get("target_score"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def public_teacher_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "teacher_id": row.get("teacher_id"),
        "name": row.get("name"),
        "position": row.get("position") or "",
        "subjects": row.get("subjects") or "",
        "status": row.get("status"),
        "is_password_changed": bool(row.get("is_password_changed")),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "is_admin": row.get("teacher_id") == "admin",
    }


def list_students(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM students ORDER BY created_at DESC"
        ).fetchall()
    ]
    return [public_student_row(item) for item in rows]


def next_student_id(conn: Any) -> str:
    row = conn.execute(
        "SELECT student_id FROM students ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    if not row:
        return "2025001"
    try:
        return str(int(row["student_id"]) + 1)
    except (TypeError, ValueError):
        return "2025001"


def create_student(
    conn: Any,
    *,
    name: str,
    target_score: float = 6.5,
    student_id: Optional[str] = None,
) -> tuple[Optional[dict[str, Any]], Optional[str], Optional[str]]:
    name = str(name or "").strip()
    if not name:
        return None, "请输入姓名", None
    try:
        target = float(target_score)
    except (TypeError, ValueError):
        return None, "目标分无效", None
    if target not in (6, 6.5, 7):
        return None, "目标分仅支持 6 / 6.5 / 7", None
    sid = str(student_id or "").strip() or next_student_id(conn)
    exists = conn.execute(
        "SELECT 1 FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if exists:
        return None, "学号已存在", None
    initial_password = STUDENT_INITIAL_PASSWORD
    now = utc_now()
    conn.execute(
        """
        INSERT INTO students (
            student_id, name, password,
            is_password_changed, target_score, status, created_at, updated_at
        ) VALUES (?, ?, ?, 0, ?, 'active', ?, ?)
        """,
        (sid, name, hash_password(initial_password), target, now, now),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    return public_student_row(dict(row)), None, initial_password


def update_student(
    conn: Any,
    *,
    student_id: str,
    name: str,
    target_score: float = 6.5,
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    name = str(name or "").strip()
    if not sid:
        return None, "缺少学号"
    if not name:
        return None, "请输入姓名"
    try:
        target = float(target_score)
    except (TypeError, ValueError):
        return None, "目标分无效"
    if target not in (6, 6.5, 7):
        return None, "目标分仅支持 6 / 6.5 / 7"
    row = conn.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    conn.execute(
        """
        UPDATE students
        SET name = ?, target_score = ?, updated_at = ?
        WHERE student_id = ?
        """,
        (name, target, utc_now(), sid),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    return public_student_row(dict(updated)), None


def create_students_batch(
    conn: Any,
    items: list[dict[str, Any]],
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    if not items:
        return None, "没有有效的学生数据"
    start_id = int(next_student_id(conn))
    created: list[dict[str, Any]] = []
    offset = 0
    for item in items:
        name = str((item or {}).get("name") or "").strip()
        if not name:
            continue
        target = (item or {}).get("target_score", (item or {}).get("targetScore", 6.5))
        student, err, _initial_password = create_student(
            conn,
            name=name,
            target_score=target,
            student_id=str(start_id + offset),
        )
        if err:
            return None, err
        created.append(student or {})
        offset += 1
    if not created:
        return None, "没有有效的学生数据"
    return {"count": len(created), "students": created}, None


def reset_student_password(conn: Any, student_id: str) -> tuple[Optional[str], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    initial_password = STUDENT_INITIAL_PASSWORD
    conn.execute(
        """
        UPDATE students
        SET password = ?, is_password_changed = 0, updated_at = ?
        WHERE student_id = ?
        """,
        (hash_password(initial_password), utc_now(), sid),
    )
    conn.commit()
    return initial_password, None


def toggle_student_status(
    conn: Any, student_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    item = dict(row)
    new_status = "inactive" if item.get("status") == "active" else "active"
    conn.execute(
        "UPDATE students SET status = ?, updated_at = ? WHERE student_id = ?",
        (new_status, utc_now(), sid),
    )
    conn.commit()
    item["status"] = new_status
    return public_student_row(item), None


def list_test_records(conn: Any, limit: int = 1000) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT r.*, s.name AS student_name
            FROM test_records r
            LEFT JOIN students s ON s.student_id = r.student_id
            ORDER BY r.created_at DESC
            LIMIT ?
            """,
            (max(1, min(int(limit), 5000)),),
        ).fetchall()
    ]
    for item in rows:
        parse_details(item)
        item["is_passed"] = bool(item.get("is_passed"))
        item["students"] = {"name": item.get("student_name")} if item.get("student_name") else None
    return rows


def load_overview(conn: Any) -> dict[str, Any]:
    students = list_students(conn)
    records = [dict(row) for row in conn.execute("SELECT * FROM test_records").fetchall()]
    sessions = [dict(row) for row in conn.execute("SELECT * FROM study_sessions").fetchall()]
    for item in records:
        parse_details(item)
        item["is_passed"] = bool(item.get("is_passed"))
    for item in sessions:
        parse_details(item)
    return {
        "students": students,
        "test_records": records,
        "study_sessions": sessions,
    }


def load_student_detail(
    conn: Any, student_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    sid = str(student_id or "").strip()
    if not sid:
        return None, "缺少学号"
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,),
    ).fetchone()
    if not row:
        return None, "学生不存在"
    records = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM test_records WHERE student_id = ? ORDER BY created_at DESC",
            (sid,),
        ).fetchall()
    ]
    sessions = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM study_sessions WHERE student_id = ? ORDER BY created_at DESC",
            (sid,),
        ).fetchall()
    ]
    wrong_words = [
        dict(r)
        for r in conn.execute(
            """
            SELECT * FROM wrong_words
            WHERE student_id = ? AND is_mastered = 0
            ORDER BY last_tested DESC
            """,
            (sid,),
        ).fetchall()
    ]
    for item in records + sessions:
        parse_details(item)
    for item in records:
        item["is_passed"] = bool(item.get("is_passed"))
    for item in wrong_words:
        item["is_mastered"] = bool(item.get("is_mastered"))

    student = public_student_row(dict(row))
    mock_exams = [
        r
        for r in records
        if str(r.get("test_type") or "") == "mock_exam"
        and str(r.get("module_type") or "") in ("mock_reading", "mock_listening")
    ]

    wrong_book_counts: dict[str, int] = {}
    try:
        from student_api import load_wrong_book_counts

        wrong_book_counts = load_wrong_book_counts(conn, sid)
    except Exception:
        wrong_book_counts = {}

    task_overview: Optional[dict[str, Any]] = None
    try:
        from task_api import student_task_snapshot

        task_overview = student_task_snapshot(
            conn, sid, str(student.get("name") or "")
        )
    except Exception:
        task_overview = None

    return {
        "student": student,
        "test_records": records,
        "study_sessions": sessions,
        "wrong_words": wrong_words,
        "wrong_book_counts": wrong_book_counts,
        "mock_exams": mock_exams,
        "task_overview": task_overview,
    }, None


def build_student_checkup_digest(
    conn: Any,
    student_id: str,
    *,
    days: int = 14,
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """Compact per-student digest for AI checkup (not for direct client display)."""
    detail, err = load_student_detail(conn, student_id)
    if err:
        return None, err
    assert detail is not None
    days = max(1, min(int(days or 14), 30))
    student = detail.get("student") or {}
    records = detail.get("test_records") or []
    sessions = detail.get("study_sessions") or []
    wrong_words = detail.get("wrong_words") or []
    wrong_book_counts = detail.get("wrong_book_counts") or {}
    mock_exams = detail.get("mock_exams") or []
    task = detail.get("task_overview") or {}

    total_seconds = 0
    for s in sessions:
        try:
            total_seconds += int(s.get("duration_seconds") or 0)
        except (TypeError, ValueError):
            pass
    passed = sum(1 for r in records if r.get("is_passed"))
    module_pass: dict[str, dict[str, int]] = {}
    for r in records:
        mt = str(r.get("module_type") or "(empty)")
        bucket = module_pass.setdefault(mt, {"total": 0, "passed": 0})
        bucket["total"] += 1
        if r.get("is_passed"):
            bucket["passed"] += 1

    recent_records = []
    for r in records[:20]:
        recent_records.append(
            {
                "module_type": r.get("module_type"),
                "test_type": r.get("test_type"),
                "score": r.get("score"),
                "is_passed": bool(r.get("is_passed")),
                "created_at": r.get("created_at"),
            }
        )

    from activity_log import build_student_activity_summary_for_ai

    activity = build_student_activity_summary_for_ai(
        conn, str(student.get("student_id") or student_id), days=days
    )

    digest = {
        "days": days,
        "student": {
            "student_id": student.get("student_id"),
            "name": student.get("name"),
            "target_score": student.get("target_score"),
            "status": student.get("status"),
        },
        "study": {
            "session_count": len(sessions),
            "total_minutes": int(round(total_seconds / 60.0)) if total_seconds else 0,
            "test_count": len(records),
            "pass_count": passed,
            "mock_exam_count": len(mock_exams),
            "unmastered_wrong_words": len(wrong_words),
            "wrong_book_counts": wrong_book_counts,
        },
        "module_pass_rates": module_pass,
        "recent_tests": recent_records,
        "task_overview": {
            "plan_status": task.get("plan_status"),
            "row_status": task.get("row_status"),
            "today_done": task.get("today_done"),
            "today_total": task.get("today_total"),
            "yesterday_done": task.get("yesterday_done"),
            "yesterday_total": task.get("yesterday_total"),
            "yesterday_incomplete": task.get("yesterday_incomplete"),
            "today_minutes": task.get("today_minutes"),
            "yesterday_minutes": task.get("yesterday_minutes"),
            "total_minutes": task.get("total_minutes"),
            "budget_minutes": task.get("budget_minutes"),
            "backlog": task.get("backlog"),
            "content_refresh": task.get("content_refresh"),
            "stage_test_pending": task.get("stage_test_pending"),
            "stage_test_needs_attention": task.get("stage_test_needs_attention"),
            "plan_progress_brief": task.get("plan_progress_brief"),
            "pending_plan_change": task.get("pending_plan_change"),
            "schedule_paused": bool((task.get("plan_pause") or {}).get("active")),
        },
        "activity": activity,
        "thicker": build_thicker_platform_metrics(conn, student_id, days=max(days, 30)),
    }
    return digest, None


def build_thicker_platform_metrics(
    conn: Any,
    student_id: str,
    *,
    days: int = 30,
) -> dict[str, Any]:
    """Extra platform metrics for full checkup (30d tasks, hours, budget)."""
    sid = str(student_id or "").strip()
    days = max(7, min(int(days or 30), 60))
    out: dict[str, Any] = {
        "days": days,
        "task_days_with_items": 0,
        "task_days_all_done": 0,
        "task_completion_rate": None,
        "red_light_proxy_days": 0,
        "done_items": 0,
        "total_items": 0,
        "hour_buckets": {},
        "budget_minutes": None,
        "actual_minutes_window": 0,
        "budget_vs_actual": None,
        "stage_test_pending": None,
    }
    if not sid:
        return out

    # daily_tasks window
    try:
        rows = conn.execute(
            """
            SELECT task_date, state
            FROM daily_tasks
            WHERE student_id = ?
              AND task_date >= date('now', ?)
            """,
            (sid, f"-{days} day"),
        ).fetchall()
    except Exception:
        rows = []

    by_day: dict[str, dict[str, int]] = {}
    for r in rows:
        d = str(r["task_date"] if hasattr(r, "keys") else r[0])
        state = str(r["state"] if hasattr(r, "keys") else r[1] or "")
        bucket = by_day.setdefault(d, {"total": 0, "done": 0})
        bucket["total"] += 1
        if state in ("done_study", "done_pass"):
            bucket["done"] += 1
            out["done_items"] += 1
        out["total_items"] += 1
    out["task_days_with_items"] = len(by_day)
    out["task_days_all_done"] = sum(
        1 for v in by_day.values() if v["total"] > 0 and v["done"] >= v["total"]
    )
    # Proxy "red": day had tasks and done==0
    out["red_light_proxy_days"] = sum(
        1 for v in by_day.values() if v["total"] > 0 and v["done"] == 0
    )
    if out["total_items"]:
        out["task_completion_rate"] = round(out["done_items"] / out["total_items"], 3)
    # Day calendar (newest first, cap 30)
    calendar = [
        {
            "date": d,
            "done": v["done"],
            "total": v["total"],
            "leftover": max(0, v["total"] - v["done"]),
            "all_done": v["total"] > 0 and v["done"] >= v["total"],
        }
        for d, v in sorted(by_day.items(), reverse=True)
    ]
    out["daily_calendar"] = calendar[:30]
    out["platform_done_days"] = [x["date"] for x in calendar if x["done"] > 0]

    # study hour distribution + module breakdown + short sessions
    hour_buckets = {f"{h:02d}": 0 for h in range(24)}
    actual_secs = 0
    module_stats: dict[str, dict[str, int]] = {}
    short_lt_60 = 0
    short_lt_180 = 0
    session_n = 0
    try:
        sessions = conn.execute(
            """
            SELECT created_at, duration_seconds, module_type, session_kind
            FROM study_sessions
            WHERE student_id = ?
              AND created_at >= datetime('now', ?)
            """,
            (sid, f"-{days} day"),
        ).fetchall()
    except Exception:
        sessions = []
    for s in sessions:
        session_n += 1
        try:
            dur = int(
                (s["duration_seconds"] if hasattr(s, "keys") else s[1]) or 0
            )
        except (TypeError, ValueError):
            dur = 0
        actual_secs += dur
        if dur < 60:
            short_lt_60 += 1
        if dur < 180:
            short_lt_180 += 1
        mt = str(
            (s["module_type"] if hasattr(s, "keys") else (s[2] if len(s) > 2 else ""))
            or "(empty)"
        )
        bucket = module_stats.setdefault(mt, {"sessions": 0, "seconds": 0})
        bucket["sessions"] += 1
        bucket["seconds"] += dur
        created = str((s["created_at"] if hasattr(s, "keys") else s[0]) or "")
        hour = None
        try:
            text = created.replace("Z", "+00:00")
            dt = datetime.fromisoformat(text)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            hour = dt.astimezone(timezone.utc).astimezone(ZoneInfo("Asia/Shanghai")).hour
        except ValueError:
            m = re.search(r"T(\d{2})", created)
            if m:
                hour = int(m.group(1))
        if hour is not None:
            hour_buckets[f"{hour:02d}"] = hour_buckets.get(f"{hour:02d}", 0) + 1
    out["hour_buckets"] = {k: v for k, v in hour_buckets.items() if v}
    out["actual_minutes_window"] = int(round(actual_secs / 60.0)) if actual_secs else 0
    out["module_sessions"] = [
        {
            "module_type": k,
            "sessions": v["sessions"],
            "minutes": int(round(v["seconds"] / 60.0)),
        }
        for k, v in sorted(
            module_stats.items(), key=lambda kv: kv[1]["seconds"], reverse=True
        )
    ]
    out["quality_proxies"] = {
        "sessions": session_n,
        "short_lt_60s": short_lt_60,
        "short_lt_180s": short_lt_180,
        "short_lt_60s_ratio": round(short_lt_60 / session_n, 3) if session_n else None,
        "short_lt_180s_ratio": round(short_lt_180 / session_n, 3) if session_n else None,
    }

    # plan inventory
    try:
        plan_rows = conn.execute(
            """
            SELECT status, COUNT(*) AS c
            FROM plan_items
            WHERE student_id = ?
            GROUP BY status
            """,
            (sid,),
        ).fetchall()
        out["plan_inventory"] = {
            str(r["status"] if hasattr(r, "keys") else r[0]): int(
                r["c"] if hasattr(r, "keys") else r[1]
            )
            for r in plan_rows
        }
    except Exception:
        out["plan_inventory"] = {}

    # activity open/exit
    try:
        act = conn.execute(
            """
            SELECT action, COUNT(*) AS c
            FROM activity_events
            WHERE created_at >= datetime('now', ?)
              AND (
                target_student_id = ?
                OR (actor_role = 'student' AND actor_id = ?)
              )
              AND (action LIKE 'task.%' OR action LIKE 'module.%')
            GROUP BY action
            ORDER BY c DESC
            LIMIT 30
            """,
            (f"-{days} day", sid, sid),
        ).fetchall()
        action_counts = {
            str(r["action"] if hasattr(r, "keys") else r[0]): int(
                r["c"] if hasattr(r, "keys") else r[1]
            )
            for r in act
        }
        opens = sum(v for k, v in action_counts.items() if k.endswith(".open") or k == "task.open")
        exits = sum(v for k, v in action_counts.items() if k.endswith(".exit") or k == "task.exit")
        completes = sum(
            v
            for k, v in action_counts.items()
            if "complete" in k or k.endswith(".done")
        )
        out["activity_task_mix"] = {
            "top_actions": action_counts,
            "open_like": opens,
            "exit_like": exits,
            "complete_like": completes,
            "exit_per_open": round(exits / opens, 3) if opens else None,
        }
    except Exception:
        out["activity_task_mix"] = {}

    try:
        from task_api import _budget_minutes, china_ymd, ensure_time_profile

        profile = ensure_time_profile(conn, sid)
        budget = _budget_minutes(profile, china_ymd())
        out["budget_minutes"] = budget
        if budget:
            # Compare window actual vs budget * active task days (rough)
            denom_days = max(1, out["task_days_with_items"] or days)
            expected = int(budget) * denom_days
            out["budget_vs_actual"] = {
                "expected_minutes_proxy": expected,
                "actual_minutes": out["actual_minutes_window"],
                "ratio": round(out["actual_minutes_window"] / expected, 3)
                if expected
                else None,
            }
    except Exception:
        pass

    try:
        from task_api import student_task_snapshot

        name_row = conn.execute(
            "SELECT name FROM students WHERE student_id=?", (sid,)
        ).fetchone()
        name = ""
        if name_row:
            name = str(
                name_row["name"] if hasattr(name_row, "keys") else name_row[0] or ""
            )
        snap = student_task_snapshot(conn, sid, name)
        out["stage_test_pending"] = snap.get("stage_test_pending")
        out["plan_progress_brief"] = snap.get("plan_progress_brief")
    except Exception:
        pass

    return out


def format_student_checkup_prompt(digest: dict[str, Any]) -> str:
    """Turn build_student_checkup_digest() output into a compact AI prompt block."""
    student = digest.get("student") or {}
    study = digest.get("study") or {}
    task = digest.get("task_overview") or {}
    activity = digest.get("activity") or {}
    lines = [
        f"学号：{student.get('student_id')} 姓名：{student.get('name')}",
        f"目标分：{student.get('target_score')} 状态：{student.get('status')}",
        f"统计窗口：近 {digest.get('days')} 天",
        "—— 学习投入 ——",
        (
            f"练习场次 {study.get('session_count')} · 总时长约 "
            f"{study.get('total_minutes')} 分钟 · 测试 {study.get('test_count')} 次"
            f"（达标 {study.get('pass_count')}）· 模拟考 {study.get('mock_exam_count')} · "
            f"未掌握错词 {study.get('unmastered_wrong_words')}"
        ),
        f"错题本计数：{json.dumps(study.get('wrong_book_counts') or {}, ensure_ascii=False)}",
        "分科测试粗览：",
        json.dumps(digest.get("module_pass_rates") or {}, ensure_ascii=False),
        "近期测试（最多20条）：",
        json.dumps(digest.get("recent_tests") or [], ensure_ascii=False),
        "—— 任务看板 ——",
        (
            f"计划状态 {task.get('plan_status')} · 行状态/灯 {task.get('row_status')} · "
            f"今日 {task.get('today_done')}/{task.get('today_total')} · "
            f"昨日 {task.get('yesterday_done')}/{task.get('yesterday_total')} · "
            f"积压 {task.get('backlog')} · 内容刷新 {task.get('content_refresh')}"
        ),
        (
            f"今日学习 {task.get('today_minutes')} 分 / 预算 {task.get('budget_minutes')} 分 · "
            f"昨日 {task.get('yesterday_minutes')} 分 · 累计任务侧 "
            f"{task.get('total_minutes')} 分"
        ),
        (
            f"待过阶段测 {task.get('stage_test_pending')} · 反复不过关注 "
            f"{task.get('stage_test_needs_attention')} · 计划暂停 "
            f"{task.get('schedule_paused')} · 待生效改动 {task.get('pending_plan_change')}"
        ),
        f"进度摘要：{task.get('plan_progress_brief')}",
        "—— 加厚指标 ——",
        json.dumps(digest.get("thicker") or {}, ensure_ascii=False),
        "—— 行为事件 ——",
        f"近窗事件数：{activity.get('total_events')}",
        "动作 Top：",
        json.dumps(activity.get("top_actions") or [], ensure_ascii=False),
        "模块 Top：",
        json.dumps(activity.get("top_modules") or [], ensure_ascii=False),
        "近期样本（新→旧）：",
    ]
    lines.extend(activity.get("sample_lines") or [])
    text = "\n".join(str(x) for x in lines)
    if len(text) > 18000:
        return text[:17900] + "\n…(截断)"
    return text


def list_standards(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM pass_standards WHERE is_active = 1 ORDER BY module_type"
        ).fetchall()
    ]
    for item in rows:
        item["is_active"] = bool(item.get("is_active"))
    return rows


def update_standard(
    conn: Any,
    module_type: str,
    payload: dict[str, Any],
) -> Optional[str]:
    module_type = str(module_type or "").strip()
    if not module_type:
        return "缺少模块类型"
    row = conn.execute(
        "SELECT * FROM pass_standards WHERE module_type = ?",
        (module_type,),
    ).fetchone()
    if not row:
        return "模块标准不存在"
    fields: dict[str, Any] = {}
    for key in ("score_6", "score_6_5", "score_7"):
        if key in payload and payload[key] is not None:
            try:
                fields[key] = float(payload[key])
            except (TypeError, ValueError):
                return f"{key} 无效"
    if not fields:
        return "没有可更新的字段"
    fields["updated_at"] = utc_now()
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(
        f"UPDATE pass_standards SET {sets} WHERE module_type = ?",
        list(fields.values()) + [module_type],
    )
    conn.commit()
    return None


def list_teachers(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM teachers ORDER BY created_at DESC"
        ).fetchall()
    ]
    return [public_teacher_row(item) for item in rows]


def create_teacher(
    conn: Any,
    *,
    teacher_id: str,
    name: str,
    position: str = "",
    subjects: str = "",
) -> tuple[Optional[dict[str, Any]], Optional[str], Optional[str]]:
    tid = str(teacher_id or "").strip().lower()
    name = str(name or "").strip()
    if not name:
        return None, "请输入姓名", None
    if not tid:
        return None, "请输入登录账号", None
    if tid == "admin":
        return None, "不能使用保留账号 admin", None
    if not all(ch.isalnum() or ch == "_" for ch in tid) or tid != tid.lower():
        return None, "账号仅支持小写字母、数字、下划线", None
    exists = conn.execute(
        "SELECT 1 FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if exists:
        return None, "账号已存在", None
    now = utc_now()
    initial_password = TEACHER_INITIAL_PASSWORD
    conn.execute(
        """
        INSERT INTO teachers (
            teacher_id, name, password,
            is_password_changed, position, subjects, status, created_at, updated_at
        ) VALUES (?, ?, ?, 0, ?, ?, 'active', ?, ?)
        """,
        (
            tid,
            name,
            hash_password(initial_password),
            position or "",
            subjects or "",
            now,
            now,
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    return public_teacher_row(dict(row)), None, initial_password


def update_teacher(
    conn: Any,
    *,
    teacher_id: str,
    name: str,
    position: str = "",
    subjects: str = "",
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    tid = str(teacher_id or "").strip().lower()
    name = str(name or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能修改管理员账号"
    if not name:
        return None, "请输入姓名"
    row = conn.execute(
        "SELECT teacher_id FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    conn.execute(
        """
        UPDATE teachers
        SET name = ?, position = ?, subjects = ?, updated_at = ?
        WHERE teacher_id = ?
        """,
        (name, position or "", subjects or "", utc_now(), tid),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    return public_teacher_row(dict(updated)), None


def reset_teacher_password(conn: Any, teacher_id: str) -> tuple[Optional[str], Optional[str]]:
    tid = str(teacher_id or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能重置管理员密码"
    row = conn.execute(
        "SELECT teacher_id FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    initial_password = TEACHER_INITIAL_PASSWORD
    conn.execute(
        """
        UPDATE teachers
        SET password = ?, is_password_changed = 0, updated_at = ?
        WHERE teacher_id = ?
        """,
        (hash_password(initial_password), utc_now(), tid),
    )
    conn.commit()
    return initial_password, None


def toggle_teacher_status(
    conn: Any, teacher_id: str
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    tid = str(teacher_id or "").strip()
    if not tid:
        return None, "缺少教师账号"
    if tid == "admin":
        return None, "不能禁用管理员"
    row = conn.execute(
        "SELECT * FROM teachers WHERE teacher_id = ?",
        (tid,),
    ).fetchone()
    if not row:
        return None, "教师不存在"
    item = dict(row)
    new_status = "inactive" if item.get("status") == "active" else "active"
    conn.execute(
        "UPDATE teachers SET status = ?, updated_at = ? WHERE teacher_id = ?",
        (new_status, utc_now(), tid),
    )
    conn.commit()
    item["status"] = new_status
    return public_teacher_row(item), None
