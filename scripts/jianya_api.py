"""剑雅真题作业：作业包、布置、提交、草稿。"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

SUBJECTS = ("listening", "reading")
PACKS_JSON = (
    Path(__file__).resolve().parents[1]
    / "sources"
    / "jianyazhenti"
    / "exam-data"
    / "assignment-packs.json"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id(prefix: str) -> str:
    return prefix + uuid.uuid4().hex[:8]


def ensure_jianya_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS jianya_packs (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            parts_json TEXT NOT NULL,
            created_by TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jianya_assignments (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            parts_json TEXT NOT NULL,
            pack_id TEXT,
            created_by TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jianya_submissions (
            assignment_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            s_id INTEGER NOT NULL,
            answers_json TEXT NOT NULL,
            correct INTEGER NOT NULL,
            total INTEGER NOT NULL,
            wrong INTEGER NOT NULL,
            blank INTEGER NOT NULL,
            pct INTEGER NOT NULL,
            submitted_at TEXT NOT NULL,
            PRIMARY KEY (assignment_id, student_id, book_id, subject, s_id)
        );
        CREATE TABLE IF NOT EXISTS jianya_drafts (
            assignment_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            s_id INTEGER NOT NULL,
            answers_json TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (assignment_id, student_id, book_id, subject, s_id)
        );
        CREATE INDEX IF NOT EXISTS idx_jianya_submissions_assignment
            ON jianya_submissions(assignment_id);
        CREATE INDEX IF NOT EXISTS idx_jianya_submissions_student
            ON jianya_submissions(student_id);
        CREATE INDEX IF NOT EXISTS idx_jianya_assignments_created
            ON jianya_assignments(created_at DESC);
        """
    )
    conn.commit()


def _parse_json_list(raw: str) -> list[Any]:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _parse_json_obj(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _validate_parts(parts: Any, subject: str) -> list[dict[str, Any]]:
    if subject not in SUBJECTS:
        raise ValueError("科目必须是 listening 或 reading")
    if not isinstance(parts, list) or not parts:
        raise ValueError("请至少选择一个 Part")
    cleaned: list[dict[str, Any]] = []
    for item in parts:
        if not isinstance(item, dict):
            raise ValueError("Part 格式无效")
        part_subject = str(item.get("subject") or subject)
        if part_subject != subject:
            raise ValueError("一份作业只能包含同一科目")
        try:
            book_id = int(item.get("bookId") or item.get("book_id") or 0)
            s_id = int(item.get("sId") or item.get("s_id") or 0)
            test_no = int(item.get("testNo") or item.get("test_no") or 0)
            s_part = int(item.get("sPart") or item.get("s_part") or 0)
            question_count = int(item.get("questionCount") or item.get("question_count") or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError("Part 字段无效") from exc
        if book_id <= 0 or s_id <= 0:
            raise ValueError("Part 缺少册号或题目编号")
        cleaned.append(
            {
                "bookId": book_id,
                "subject": subject,
                "sId": s_id,
                "testNo": test_no,
                "sPart": s_part,
                "label": str(item.get("label") or "").strip(),
                "questionCount": question_count,
            }
        )
    return cleaned


def _pack_row(row: sqlite3.Row, *, builtin: bool = False) -> dict[str, Any]:
    out = {
        "id": row["id"],
        "title": row["title"],
        "subject": row["subject"],
        "description": row["description"] or "",
        "parts": _parse_json_list(row["parts_json"]),
        "builtin": builtin,
        "createdAt": row["created_at"],
    }
    if not builtin:
        out["createdBy"] = row["created_by"]
    return out


def _assignment_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "subject": row["subject"],
        "parts": _parse_json_list(row["parts_json"]),
        "packId": row["pack_id"] or None,
        "createdBy": row["created_by"],
        "createdAt": row["created_at"],
    }


def _submission_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "assignmentId": row["assignment_id"],
        "studentId": row["student_id"],
        "bookId": row["book_id"],
        "subject": row["subject"],
        "sId": row["s_id"],
        "status": "submitted",
        "answers": _parse_json_obj(row["answers_json"]),
        "correct": row["correct"],
        "total": row["total"],
        "wrong": row["wrong"],
        "blank": row["blank"],
        "pct": row["pct"],
        "submittedAt": row["submitted_at"],
    }


def load_builtin_packs(path: Optional[Path] = None) -> list[dict[str, Any]]:
    file_path = path or PACKS_JSON
    if not file_path.is_file():
        return []
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    packs = payload.get("packs") if isinstance(payload, dict) else None
    if not isinstance(packs, list):
        return []
    out: list[dict[str, Any]] = []
    for item in packs:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        subject = str(item.get("subject") or "")
        if subject not in SUBJECTS:
            continue
        try:
            parts = _validate_parts(item.get("parts") or [], subject)
        except ValueError:
            continue
        out.append(
            {
                "id": str(item["id"]),
                "title": str(item.get("title") or "未命名作业包"),
                "subject": subject,
                "description": str(item.get("description") or ""),
                "parts": parts,
                "builtin": True,
                "createdAt": str(item.get("createdAt") or ""),
            }
        )
    return out


def list_custom_packs(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM jianya_packs ORDER BY created_at DESC"
    ).fetchall()
    return [_pack_row(row) for row in rows]


def list_all_packs(conn: sqlite3.Connection, packs_path: Optional[Path] = None) -> list[dict[str, Any]]:
    custom = list_custom_packs(conn)
    custom_ids = {p["id"] for p in custom}
    builtin = [p for p in load_builtin_packs(packs_path) if p["id"] not in custom_ids]
    return builtin + custom


def get_pack(conn: sqlite3.Connection, pack_id: str, packs_path: Optional[Path] = None) -> Optional[dict[str, Any]]:
    row = conn.execute("SELECT * FROM jianya_packs WHERE id = ?", (pack_id,)).fetchone()
    if row:
        return _pack_row(row)
    for pack in load_builtin_packs(packs_path):
        if pack["id"] == pack_id:
            return pack
    return None


def create_pack(
    conn: sqlite3.Connection,
    *,
    title: str,
    subject: str,
    parts: Any,
    description: str = "",
    created_by: str = "",
) -> dict[str, Any]:
    cleaned = _validate_parts(parts, subject)
    pack_id = new_id("p")
    created_at = utc_now()
    title_text = (title or "").strip() or "未命名作业包"
    desc = (description or "").strip()
    conn.execute(
        """
        INSERT INTO jianya_packs (id, title, subject, description, parts_json, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (pack_id, title_text, subject, desc, json.dumps(cleaned, ensure_ascii=False), created_by, created_at),
    )
    conn.commit()
    return {
        "id": pack_id,
        "title": title_text,
        "subject": subject,
        "description": desc,
        "parts": cleaned,
        "builtin": False,
        "createdBy": created_by,
        "createdAt": created_at,
    }


def delete_pack(conn: sqlite3.Connection, pack_id: str) -> None:
    cur = conn.execute("DELETE FROM jianya_packs WHERE id = ?", (pack_id,))
    conn.commit()
    if cur.rowcount <= 0:
        raise ValueError("内置作业包不可删除")


def list_assignments(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM jianya_assignments ORDER BY created_at DESC"
    ).fetchall()
    return [_assignment_row(row) for row in rows]


def get_assignment(conn: sqlite3.Connection, assignment_id: str) -> Optional[dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM jianya_assignments WHERE id = ?", (assignment_id,)
    ).fetchone()
    return _assignment_row(row) if row else None


def create_assignment(
    conn: sqlite3.Connection,
    *,
    title: str,
    subject: str,
    parts: Any,
    pack_id: Optional[str] = None,
    created_by: str = "",
) -> dict[str, Any]:
    cleaned = _validate_parts(parts, subject)
    assignment_id = new_id("a")
    created_at = utc_now()
    title_text = (title or "").strip() or "未命名作业"
    conn.execute(
        """
        INSERT INTO jianya_assignments (id, title, subject, parts_json, pack_id, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            assignment_id,
            title_text,
            subject,
            json.dumps(cleaned, ensure_ascii=False),
            pack_id or None,
            created_by,
            created_at,
        ),
    )
    conn.commit()
    return {
        "id": assignment_id,
        "title": title_text,
        "subject": subject,
        "parts": cleaned,
        "packId": pack_id or None,
        "createdBy": created_by,
        "createdAt": created_at,
    }


def publish_from_packs(
    conn: sqlite3.Connection,
    pack_ids: list[str],
    *,
    title_prefix: str = "",
    created_by: str = "",
    packs_path: Optional[Path] = None,
) -> list[dict[str, Any]]:
    if not pack_ids:
        raise ValueError("请至少选择一个作业包")
    created: list[dict[str, Any]] = []
    prefix = (title_prefix or "").strip()
    for pack_id in pack_ids:
        pack = get_pack(conn, str(pack_id), packs_path)
        if not pack:
            raise ValueError(f"找不到作业包 {pack_id}")
        title = f"{prefix} · {pack['title']}" if prefix else pack["title"]
        created.append(
            create_assignment(
                conn,
                title=title,
                subject=pack["subject"],
                parts=pack["parts"],
                pack_id=pack["id"],
                created_by=created_by,
            )
        )
    return created


def delete_assignment(conn: sqlite3.Connection, assignment_id: str) -> None:
    conn.execute("DELETE FROM jianya_drafts WHERE assignment_id = ?", (assignment_id,))
    conn.execute("DELETE FROM jianya_submissions WHERE assignment_id = ?", (assignment_id,))
    cur = conn.execute("DELETE FROM jianya_assignments WHERE id = ?", (assignment_id,))
    conn.commit()
    if cur.rowcount <= 0:
        raise ValueError("作业不存在或已删除")


def list_submissions(
    conn: sqlite3.Connection,
    assignment_id: str,
    student_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    if student_id:
        rows = conn.execute(
            """
            SELECT * FROM jianya_submissions
            WHERE assignment_id = ? AND student_id = ?
            ORDER BY submitted_at DESC
            """,
            (assignment_id, student_id),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT * FROM jianya_submissions
            WHERE assignment_id = ?
            ORDER BY submitted_at DESC
            """,
            (assignment_id,),
        ).fetchall()
    return [_submission_row(row) for row in rows]


def get_submission(
    conn: sqlite3.Connection,
    assignment_id: str,
    student_id: str,
    book_id: int,
    subject: str,
    s_id: int,
) -> Optional[dict[str, Any]]:
    row = conn.execute(
        """
        SELECT * FROM jianya_submissions
        WHERE assignment_id = ? AND student_id = ? AND book_id = ? AND subject = ? AND s_id = ?
        """,
        (assignment_id, student_id, book_id, subject, s_id),
    ).fetchone()
    return _submission_row(row) if row else None


def save_submission(
    conn: sqlite3.Connection,
    *,
    assignment_id: str,
    student_id: str,
    book_id: int,
    subject: str,
    s_id: int,
    answers: Any,
    correct: int,
    total: int,
    wrong: int,
    blank: int,
    pct: int,
) -> dict[str, Any]:
    assignment = get_assignment(conn, assignment_id)
    if not assignment:
        raise ValueError("作业不存在或已删除")
    if subject not in SUBJECTS:
        raise ValueError("科目无效")
    if not student_id:
        raise ValueError("缺少学号")
    existing = get_submission(conn, assignment_id, student_id, book_id, subject, s_id)
    if existing:
        return existing
    part_ok = any(
        int(p.get("bookId") or 0) == int(book_id)
        and p.get("subject") == subject
        and int(p.get("sId") or 0) == int(s_id)
        for p in assignment["parts"]
    )
    if not part_ok:
        raise ValueError("该 Part 不属于这份作业")
    answers_obj = answers if isinstance(answers, dict) else {}
    submitted_at = utc_now()
    conn.execute(
        """
        INSERT INTO jianya_submissions (
            assignment_id, student_id, book_id, subject, s_id,
            answers_json, correct, total, wrong, blank, pct, submitted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            assignment_id,
            student_id,
            int(book_id),
            subject,
            int(s_id),
            json.dumps(answers_obj, ensure_ascii=False),
            int(correct),
            int(total),
            int(wrong),
            int(blank),
            int(pct),
            submitted_at,
        ),
    )
    conn.execute(
        """
        INSERT INTO jianya_drafts (
            assignment_id, student_id, book_id, subject, s_id, answers_json, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(assignment_id, student_id, book_id, subject, s_id)
        DO UPDATE SET answers_json = excluded.answers_json, updated_at = excluded.updated_at
        """,
        (
            assignment_id,
            student_id,
            int(book_id),
            subject,
            int(s_id),
            json.dumps(answers_obj, ensure_ascii=False),
            submitted_at,
        ),
    )
    conn.commit()
    return {
        "assignmentId": assignment_id,
        "studentId": student_id,
        "bookId": int(book_id),
        "subject": subject,
        "sId": int(s_id),
        "status": "submitted",
        "answers": answers_obj,
        "correct": int(correct),
        "total": int(total),
        "wrong": int(wrong),
        "blank": int(blank),
        "pct": int(pct),
        "submittedAt": submitted_at,
    }


def list_student_submissions(conn: sqlite3.Connection, student_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT s.*, a.title AS assignment_title, a.parts_json
        FROM jianya_submissions s
        JOIN jianya_assignments a ON a.id = s.assignment_id
        WHERE s.student_id = ?
        ORDER BY s.submitted_at DESC
        """,
        (student_id,),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        item = _submission_row(row)
        parts = _parse_json_list(row["parts_json"])
        match = next(
            (
                p
                for p in parts
                if isinstance(p, dict)
                and int(p.get("bookId") or 0) == int(item["bookId"])
                and p.get("subject") == item["subject"]
                and int(p.get("sId") or 0) == int(item["sId"])
            ),
            None,
        )
        item["assignmentTitle"] = row["assignment_title"]
        item["sPart"] = int((match or {}).get("sPart") or 0)
        item["label"] = str((match or {}).get("label") or "")
        out.append(item)
    return out


def get_draft(
    conn: sqlite3.Connection,
    assignment_id: str,
    student_id: str,
    book_id: int,
    subject: str,
    s_id: int,
) -> dict[str, str]:
    row = conn.execute(
        """
        SELECT answers_json FROM jianya_drafts
        WHERE assignment_id = ? AND student_id = ? AND book_id = ? AND subject = ? AND s_id = ?
        """,
        (assignment_id, student_id, book_id, subject, s_id),
    ).fetchone()
    if not row:
        return {}
    return _parse_json_obj(row["answers_json"])


def save_draft(
    conn: sqlite3.Connection,
    *,
    assignment_id: str,
    student_id: str,
    book_id: int,
    subject: str,
    s_id: int,
    answers: Any,
) -> dict[str, str]:
    if not get_assignment(conn, assignment_id):
        raise ValueError("作业不存在或已删除")
    if get_submission(conn, assignment_id, student_id, book_id, subject, s_id):
        return get_draft(conn, assignment_id, student_id, book_id, subject, s_id)
    answers_obj = answers if isinstance(answers, dict) else {}
    conn.execute(
        """
        INSERT INTO jianya_drafts (
            assignment_id, student_id, book_id, subject, s_id, answers_json, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(assignment_id, student_id, book_id, subject, s_id)
        DO UPDATE SET answers_json = excluded.answers_json, updated_at = excluded.updated_at
        """,
        (
            assignment_id,
            student_id,
            int(book_id),
            subject,
            int(s_id),
            json.dumps(answers_obj, ensure_ascii=False),
            utc_now(),
        ),
    )
    conn.commit()
    return answers_obj
