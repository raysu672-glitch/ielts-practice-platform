"""Teacher-scoped API helpers (session identity is enforced by the caller)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional


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
        r for r in records if str(r.get("test_type") or "") == "mock_exam"
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
