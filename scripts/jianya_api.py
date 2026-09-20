"""剑雅真题作业：作业包、布置、提交、草稿。"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

PACK_SUBJECTS = ("listening", "reading", "writing", "speaking")
EXAM_SUBJECTS = ("listening", "reading")
OPEN_SUBJECTS = ("listening", "reading", "writing")
SUBJECTS = PACK_SUBJECTS
ADMIN_CREATOR = "admin"
DEFAULT_SUBJECT = "listening"
WRITING_BOOK_ID = 100
PACKS_JSON = (
    Path(__file__).resolve().parents[1]
    / "sources"
    / "jianyazhenti"
    / "exam-data"
    / "assignment-packs.json"
)
WRITING_TOPICS_JSON = (
    Path(__file__).resolve().parents[1]
    / "sources"
    / "jianyazhenti"
    / "src"
    / "data"
    / "writing-topics.json"
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
            correction_json TEXT,
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
        CREATE TABLE IF NOT EXISTS jianya_recipients (
            assignment_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            assigned_at TEXT NOT NULL,
            PRIMARY KEY (assignment_id, student_id)
        );
        CREATE TABLE IF NOT EXISTS jianya_reviews (
            assignment_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            comment TEXT NOT NULL DEFAULT '',
            created_by TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            PRIMARY KEY (assignment_id, student_id)
        );
        CREATE INDEX IF NOT EXISTS idx_jianya_submissions_assignment
            ON jianya_submissions(assignment_id);
        CREATE INDEX IF NOT EXISTS idx_jianya_submissions_student
            ON jianya_submissions(student_id);
        CREATE INDEX IF NOT EXISTS idx_jianya_assignments_created
            ON jianya_assignments(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_jianya_recipients_student
            ON jianya_recipients(student_id);
        """
    )
    conn.commit()
    _ensure_column(conn, "jianya_submissions", "correction_json", "TEXT")


def _ensure_column(
    conn: sqlite3.Connection, table: str, column: str, decl: str
) -> None:
    cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
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


def normalize_pack_subject(subject: str) -> str:
    value = str(subject or "").strip()
    if value not in PACK_SUBJECTS:
        raise ValueError("科目必须是听力、阅读、写作或口语")
    return value


def pack_visible_to(pack: dict[str, Any], viewer_id: str) -> bool:
    if pack.get("builtin"):
        return True
    created = str(pack.get("createdBy") or "")
    viewer = str(viewer_id or "").strip()
    if not viewer:
        return True
    return created == viewer or created == ADMIN_CREATOR


def pack_rank(pack: dict[str, Any]) -> int:
    if str(pack.get("createdBy") or "") == ADMIN_CREATOR:
        return 0
    if pack.get("builtin"):
        return 2
    return 1


def sort_packs_for_teacher(packs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = list(packs)
    items.sort(key=lambda row: str(row.get("createdAt") or ""), reverse=True)
    items.sort(key=pack_rank)
    return items


def load_writing_topics(path: Optional[Path] = None) -> list[dict[str, Any]]:
    file_path = path or WRITING_TOPICS_JSON
    if not file_path.is_file():
        return []
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    items = payload.get("topics") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            topic_id = int(item.get("id") or 0)
            lesson = int(item.get("lesson") or 0)
        except (TypeError, ValueError):
            continue
        prompt = str(item.get("prompt") or "").strip()
        if topic_id <= 0 or not prompt:
            continue
        task = str(item.get("task") or "task2").strip() or "task2"
        out.append(
            {
                "id": topic_id,
                "lesson": lesson or 1,
                "lessonTitle": str(item.get("lessonTitle") or f"第{lesson}课"),
                "pattern": str(item.get("pattern") or "").strip(),
                "task": task,
                "questionType": str(item.get("questionType") or "").strip(),
                "title": str(item.get("title") or "").strip() or f"写作题目 {topic_id}",
                "examMeta": str(item.get("examMeta") or "").strip(),
                "prompt": prompt,
                "tips": str(item.get("tips") or "").strip(),
            }
        )
    return out


def writing_topic_part(topic: dict[str, Any]) -> dict[str, Any]:
    task = str(topic.get("task") or "task2")
    return {
        "bookId": WRITING_BOOK_ID,
        "subject": "writing",
        "sId": int(topic["id"]),
        "testNo": int(topic.get("lesson") or 1),
        "sPart": 1 if task == "task1" else 2,
        "label": str(topic.get("title") or "").strip(),
        "questionCount": 1,
        "prompt": str(topic.get("prompt") or "").strip(),
        "task": task,
        "lesson": int(topic.get("lesson") or 1),
        "pattern": str(topic.get("pattern") or "").strip(),
        "examMeta": str(topic.get("examMeta") or "").strip(),
        "tips": str(topic.get("tips") or "").strip(),
    }


def builtin_writing_packs(path: Optional[Path] = None) -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    for topic in load_writing_topics(path):
        part = writing_topic_part(topic)
        lesson_title = str(topic.get("lessonTitle") or f"第{part['lesson']}课")
        task_label = "Task 1" if part["task"] == "task1" else "Task 2"
        bits = [part["prompt"]]
        if part.get("examMeta"):
            bits.append(str(part["examMeta"]))
        packs.append(
            {
                "id": f"wpack-t{part['sId']}",
                "title": part["label"] or f"{lesson_title} {task_label}",
                "subject": "writing",
                "description": "\n".join(bits),
                "parts": [part],
                "builtin": True,
                "createdAt": "",
            }
        )
    return packs


def _writing_topic_by_id(topic_id: int) -> Optional[dict[str, Any]]:
    for topic in load_writing_topics():
        if int(topic["id"]) == int(topic_id):
            return topic
    return None


def _validate_writing_parts(parts: Any) -> list[dict[str, Any]]:
    if not isinstance(parts, list) or not parts:
        raise ValueError("请至少选择一个题目")
    cleaned: list[dict[str, Any]] = []
    seen: set[int] = set()
    for item in parts:
        if not isinstance(item, dict):
            raise ValueError("题目格式无效")
        try:
            topic_id = int(item.get("sId") or item.get("s_id") or item.get("id") or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError("题目编号无效") from exc
        topic = _writing_topic_by_id(topic_id)
        if not topic:
            raise ValueError(f"找不到写作题目 {topic_id}")
        if topic_id in seen:
            continue
        seen.add(topic_id)
        part = writing_topic_part(topic)
        label = str(item.get("label") or "").strip()
        if label:
            part["label"] = label
        cleaned.append(part)
    if not cleaned:
        raise ValueError("请至少选择一个题目")
    return cleaned


def _validate_parts(parts: Any, subject: str) -> list[dict[str, Any]]:
    subject = normalize_pack_subject(subject)
    if subject == "writing":
        return _validate_writing_parts(parts)
    if subject not in EXAM_SUBJECTS:
        raise ValueError("口语作业包即将开放")
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


def _enrich_writing_parts(parts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        item = dict(part)
        if str(item.get("subject") or "") == "writing" and not str(item.get("tips") or "").strip():
            try:
                topic_id = int(item.get("sId") or 0)
            except (TypeError, ValueError):
                topic_id = 0
            topic = _writing_topic_by_id(topic_id) if topic_id else None
            tips = str((topic or {}).get("tips") or "").strip()
            if tips:
                item["tips"] = tips
        out.append(item)
    return out


def _pack_row(row: sqlite3.Row, *, builtin: bool = False) -> dict[str, Any]:
    out = {
        "id": row["id"],
        "title": row["title"],
        "subject": row["subject"],
        "description": row["description"] or "",
        "parts": _enrich_writing_parts(_parse_json_list(row["parts_json"])),
        "builtin": builtin,
        "createdAt": row["created_at"],
    }
    if not builtin:
        created_by = str(row["created_by"] or "")
        out["createdBy"] = created_by
        out["fromAdmin"] = created_by == ADMIN_CREATOR
    else:
        out["fromAdmin"] = False
    return out


def _assignment_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "subject": row["subject"],
        "parts": _enrich_writing_parts(_parse_json_list(row["parts_json"])),
        "packId": row["pack_id"] or None,
        "createdBy": row["created_by"],
        "createdAt": row["created_at"],
    }


def teacher_owns_assignment(assignment: Optional[dict[str, Any]], teacher_id: str) -> bool:
    if not assignment:
        return False
    return str(assignment.get("createdBy") or "") == str(teacher_id or "").strip()


def _part_keys(assignment: dict[str, Any]) -> list[tuple[int, str, int]]:
    keys: list[tuple[int, str, int]] = []
    for part in assignment.get("parts") or []:
        if not isinstance(part, dict):
            continue
        keys.append(
            (
                int(part.get("bookId") or 0),
                str(part.get("subject") or ""),
                int(part.get("sId") or 0),
            )
        )
    return keys


def _normalize_student_ids(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        raise ValueError("学生名单格式无效")
    seen: list[str] = []
    used: set[str] = set()
    for item in raw:
        sid = str(item or "").strip()
        if not sid or sid in used:
            continue
        used.add(sid)
        seen.append(sid)
    return seen


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    return {str(row[0]) for row in rows}


def _assert_students_exist(conn: sqlite3.Connection, student_ids: list[str]) -> None:
    if not student_ids or "students" not in _table_names(conn):
        return
    placeholders = ",".join("?" * len(student_ids))
    rows = conn.execute(
        f"SELECT student_id FROM students WHERE student_id IN ({placeholders})",
        student_ids,
    ).fetchall()
    found = {str(row["student_id"]) for row in rows}
    missing = [sid for sid in student_ids if sid not in found]
    if missing:
        raise ValueError("找不到学生：" + "、".join(missing))


def _student_name_map(conn: sqlite3.Connection, student_ids: list[str]) -> dict[str, str]:
    if not student_ids or "students" not in _table_names(conn):
        return {}
    placeholders = ",".join("?" * len(student_ids))
    rows = conn.execute(
        f"SELECT student_id, name FROM students WHERE student_id IN ({placeholders})",
        student_ids,
    ).fetchall()
    return {str(row["student_id"]): str(row["name"] or "") for row in rows}


def list_recipient_ids(conn: sqlite3.Connection, assignment_id: str) -> list[str]:
    rows = conn.execute(
        """
        SELECT student_id FROM jianya_recipients
        WHERE assignment_id = ?
        ORDER BY assigned_at, student_id
        """,
        (assignment_id,),
    ).fetchall()
    return [str(row["student_id"]) for row in rows]


def is_recipient(conn: sqlite3.Connection, assignment_id: str, student_id: str) -> bool:
    if not assignment_id or not student_id:
        return False
    row = conn.execute(
        """
        SELECT 1 FROM jianya_recipients
        WHERE assignment_id = ? AND student_id = ?
        """,
        (assignment_id, student_id),
    ).fetchone()
    return bool(row)


def _insert_recipients(
    conn: sqlite3.Connection,
    assignment_id: str,
    student_ids: list[str],
    *,
    assigned_at: Optional[str] = None,
) -> int:
    if not student_ids:
        return 0
    now = assigned_at or utc_now()
    added = 0
    for sid in student_ids:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO jianya_recipients (assignment_id, student_id, assigned_at)
            VALUES (?, ?, ?)
            """,
            (assignment_id, sid, now),
        )
        added += cur.rowcount
    return added


def _submitted_part_map(
    conn: sqlite3.Connection, assignment_ids: list[str]
) -> dict[tuple[str, str], set[tuple[int, str, int]]]:
    out: dict[tuple[str, str], set[tuple[int, str, int]]] = {}
    if not assignment_ids:
        return out
    placeholders = ",".join("?" * len(assignment_ids))
    rows = conn.execute(
        f"""
        SELECT assignment_id, student_id, book_id, subject, s_id
        FROM jianya_submissions
        WHERE assignment_id IN ({placeholders})
        """,
        assignment_ids,
    ).fetchall()
    for row in rows:
        key = (str(row["assignment_id"]), str(row["student_id"]))
        out.setdefault(key, set()).add(
            (int(row["book_id"]), str(row["subject"]), int(row["s_id"]))
        )
    return out


def _enrich_assignments(
    conn: sqlite3.Connection,
    items: list[dict[str, Any]],
    *,
    for_student_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    if not items:
        return items
    ids = [str(item["id"]) for item in items]
    placeholders = ",".join("?" * len(ids))
    rec_rows = conn.execute(
        f"""
        SELECT assignment_id, student_id FROM jianya_recipients
        WHERE assignment_id IN ({placeholders})
        ORDER BY assigned_at, student_id
        """,
        ids,
    ).fetchall()
    rec_map: dict[str, list[str]] = {aid: [] for aid in ids}
    for row in rec_rows:
        rec_map[str(row["assignment_id"])].append(str(row["student_id"]))
    sub_map = _submitted_part_map(conn, ids)
    review_map: dict[str, dict[str, str]] = {}
    if for_student_id:
        rev_rows = conn.execute(
            f"""
            SELECT assignment_id, comment, updated_at FROM jianya_reviews
            WHERE student_id = ? AND assignment_id IN ({placeholders})
            """,
            [for_student_id, *ids],
        ).fetchall()
        review_map = {
            str(row["assignment_id"]): {
                "comment": str(row["comment"] or ""),
                "reviewedAt": str(row["updated_at"] or ""),
            }
            for row in rev_rows
        }
    out: list[dict[str, Any]] = []
    for item in items:
        assignment = dict(item)
        part_set = set(_part_keys(assignment))
        recipients = rec_map.get(str(assignment["id"]), [])
        submitted_count = 0
        for sid in recipients:
            done = sub_map.get((str(assignment["id"]), sid), set())
            if part_set and part_set <= done:
                submitted_count += 1
        assignment["assignedCount"] = len(recipients)
        assignment["submittedCount"] = submitted_count
        if for_student_id:
            done = sub_map.get((str(assignment["id"]), for_student_id), set())
            submitted_parts = len(part_set & done) if part_set else 0
            total_parts = len(part_set)
            assignment["mySubmittedParts"] = submitted_parts
            assignment["myTotalParts"] = total_parts
            if total_parts and submitted_parts >= total_parts:
                assignment["myStatus"] = "submitted"
            elif submitted_parts:
                assignment["myStatus"] = "partial"
            else:
                assignment["myStatus"] = "missing"
            review = review_map.get(str(assignment["id"])) or {}
            assignment["comment"] = review.get("comment") or ""
            assignment["reviewedAt"] = review.get("reviewedAt") or ""
        else:
            assignment["studentIds"] = recipients
        out.append(assignment)
    return out


def _submission_row(row: sqlite3.Row) -> dict[str, Any]:
    out: dict[str, Any] = {
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
    correction = _parse_json_obj(row["correction_json"]) if "correction_json" in row.keys() else {}
    if correction:
        out["correction"] = correction
    return out


def load_builtin_packs(path: Optional[Path] = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    file_path = path or PACKS_JSON
    if file_path.is_file():
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = None
        packs = payload.get("packs") if isinstance(payload, dict) else None
        if isinstance(packs, list):
            for item in packs:
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                subject = str(item.get("subject") or "")
                if subject not in OPEN_SUBJECTS:
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
    out.extend(builtin_writing_packs())
    return out


def list_custom_packs(
    conn: sqlite3.Connection, viewer_id: str = ""
) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM jianya_packs ORDER BY created_at DESC"
    ).fetchall()
    items = [_pack_row(row) for row in rows]
    if viewer_id:
        items = [row for row in items if pack_visible_to(row, viewer_id)]
    return items


def list_all_packs(
    conn: sqlite3.Connection,
    packs_path: Optional[Path] = None,
    viewer_id: str = "",
) -> list[dict[str, Any]]:
    custom = list_custom_packs(conn, viewer_id=viewer_id)
    custom_ids = {p["id"] for p in custom}
    builtin = [p for p in load_builtin_packs(packs_path) if p["id"] not in custom_ids]
    items = custom + builtin
    if viewer_id:
        return sort_packs_for_teacher(items)
    return items


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
    subject = normalize_pack_subject(subject)
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
        "fromAdmin": created_by == ADMIN_CREATOR,
        "createdAt": created_at,
    }


def delete_pack(
    conn: sqlite3.Connection, pack_id: str, *, actor_id: str = ""
) -> None:
    pack = get_pack(conn, pack_id)
    if not pack or pack.get("builtin"):
        raise ValueError("内置作业包不可删除")
    if actor_id and str(pack.get("createdBy") or "") != actor_id:
        raise ValueError("只能删除自己建立的作业包")
    cur = conn.execute("DELETE FROM jianya_packs WHERE id = ?", (pack_id,))
    conn.commit()
    if cur.rowcount <= 0:
        raise ValueError("内置作业包不可删除")


def list_assignments(
    conn: sqlite3.Connection, created_by: str = ""
) -> list[dict[str, Any]]:
    viewer = str(created_by or "").strip()
    if viewer:
        rows = conn.execute(
            """
            SELECT * FROM jianya_assignments
            WHERE created_by = ?
            ORDER BY created_at DESC
            """,
            (viewer,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM jianya_assignments ORDER BY created_at DESC"
        ).fetchall()
    return _enrich_assignments(conn, [_assignment_row(row) for row in rows])


def list_student_assignments(
    conn: sqlite3.Connection, student_id: str
) -> list[dict[str, Any]]:
    sid = str(student_id or "").strip()
    if not sid:
        return []
    rows = conn.execute(
        """
        SELECT a.* FROM jianya_assignments a
        INNER JOIN jianya_recipients r ON r.assignment_id = a.id
        WHERE r.student_id = ?
        ORDER BY a.created_at DESC
        """,
        (sid,),
    ).fetchall()
    return _enrich_assignments(
        conn, [_assignment_row(row) for row in rows], for_student_id=sid
    )


def get_assignment(
    conn: sqlite3.Connection,
    assignment_id: str,
    *,
    student_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM jianya_assignments WHERE id = ?", (assignment_id,)
    ).fetchone()
    if not row:
        return None
    items = _enrich_assignments(
        conn,
        [_assignment_row(row)],
        for_student_id=str(student_id).strip() if student_id else None,
    )
    return items[0]


def create_assignment(
    conn: sqlite3.Connection,
    *,
    title: str,
    subject: str,
    parts: Any,
    pack_id: Optional[str] = None,
    created_by: str = "",
    student_ids: Any = None,
) -> dict[str, Any]:
    cleaned = _validate_parts(parts, subject)
    ids = _normalize_student_ids(student_ids)
    if not ids:
        raise ValueError("请至少选择一名学生")
    _assert_students_exist(conn, ids)
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
    _insert_recipients(conn, assignment_id, ids, assigned_at=created_at)
    conn.commit()
    created = get_assignment(conn, assignment_id)
    return created or {
        "id": assignment_id,
        "title": title_text,
        "subject": subject,
        "parts": cleaned,
        "packId": pack_id or None,
        "createdBy": created_by,
        "createdAt": created_at,
        "studentIds": ids,
        "assignedCount": len(ids),
        "submittedCount": 0,
    }


def publish_from_packs(
    conn: sqlite3.Connection,
    pack_ids: list[str],
    *,
    title_prefix: str = "",
    created_by: str = "",
    packs_path: Optional[Path] = None,
    student_ids: Any = None,
) -> list[dict[str, Any]]:
    if not pack_ids:
        raise ValueError("请至少选择一个作业包")
    ids = _normalize_student_ids(student_ids)
    if not ids:
        raise ValueError("请至少选择一名学生")
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
                student_ids=ids,
            )
        )
    return created


def add_recipients(
    conn: sqlite3.Connection, assignment_id: str, student_ids: Any
) -> dict[str, Any]:
    assignment = get_assignment(conn, assignment_id)
    if not assignment:
        raise ValueError("作业不存在或已删除")
    ids = _normalize_student_ids(student_ids)
    if not ids:
        raise ValueError("请至少选择一名学生")
    _assert_students_exist(conn, ids)
    _insert_recipients(conn, assignment_id, ids)
    conn.commit()
    return get_roster(conn, assignment_id)


def get_roster(conn: sqlite3.Connection, assignment_id: str) -> dict[str, Any]:
    assignment = get_assignment(conn, assignment_id)
    if not assignment:
        raise ValueError("作业不存在或已删除")
    recipients = list_recipient_ids(conn, assignment_id)
    names = _student_name_map(conn, recipients)
    part_set = set(_part_keys(assignment))
    sub_map = _submitted_part_map(conn, [assignment_id])
    time_rows = conn.execute(
        """
        SELECT student_id, MAX(submitted_at) AS submitted_at
        FROM jianya_submissions
        WHERE assignment_id = ?
        GROUP BY student_id
        """,
        (assignment_id,),
    ).fetchall()
    submitted_at_map = {
        str(row["student_id"]): str(row["submitted_at"] or "") for row in time_rows
    }
    review_rows = conn.execute(
        """
        SELECT student_id, comment, updated_at FROM jianya_reviews
        WHERE assignment_id = ?
        """,
        (assignment_id,),
    ).fetchall()
    review_map = {
        str(row["student_id"]): {
            "comment": str(row["comment"] or ""),
            "reviewedAt": str(row["updated_at"] or ""),
        }
        for row in review_rows
    }
    students: list[dict[str, Any]] = []
    submitted_count = 0
    for sid in recipients:
        done = sub_map.get((assignment_id, sid), set())
        submitted_parts = len(part_set & done) if part_set else 0
        total_parts = len(part_set)
        if total_parts and submitted_parts >= total_parts:
            status = "submitted"
            submitted_count += 1
        elif submitted_parts:
            status = "partial"
        else:
            status = "missing"
        review = review_map.get(sid) or {}
        students.append(
            {
                "studentId": sid,
                "name": names.get(sid) or sid,
                "status": status,
                "submittedParts": submitted_parts,
                "totalParts": total_parts,
                "submittedAt": submitted_at_map.get(sid) or "",
                "comment": review.get("comment") or "",
                "reviewedAt": review.get("reviewedAt") or "",
            }
        )
    order = {"missing": 0, "partial": 1, "submitted": 2}
    students.sort(key=lambda row: (order.get(str(row["status"]), 9), str(row["studentId"])))
    return {
        "assignmentId": assignment_id,
        "assignedCount": len(recipients),
        "submittedCount": submitted_count,
        "students": students,
    }


def save_review(
    conn: sqlite3.Connection,
    *,
    assignment_id: str,
    student_id: str,
    comment: str,
    created_by: str = "",
) -> dict[str, Any]:
    assignment = get_assignment(conn, assignment_id)
    if not assignment:
        raise ValueError("作业不存在或已删除")
    sid = str(student_id or "").strip()
    if not sid:
        raise ValueError("缺少学号")
    if not is_recipient(conn, assignment_id, sid):
        raise ValueError("该学生不在这份作业名单中")
    text = str(comment or "").strip()
    now = utc_now()
    conn.execute(
        """
        INSERT INTO jianya_reviews (assignment_id, student_id, comment, created_by, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(assignment_id, student_id)
        DO UPDATE SET comment = excluded.comment, created_by = excluded.created_by, updated_at = excluded.updated_at
        """,
        (assignment_id, sid, text, created_by, now),
    )
    conn.commit()
    return {
        "assignmentId": assignment_id,
        "studentId": sid,
        "comment": text,
        "createdBy": created_by,
        "updatedAt": now,
    }


def delete_assignment(
    conn: sqlite3.Connection, assignment_id: str, *, actor_id: str = ""
) -> None:
    if actor_id:
        assignment = get_assignment(conn, assignment_id)
        if not assignment:
            raise ValueError("作业不存在或已删除")
        if not teacher_owns_assignment(assignment, actor_id):
            raise ValueError("只能删除自己布置的作业")
    conn.execute("DELETE FROM jianya_drafts WHERE assignment_id = ?", (assignment_id,))
    conn.execute("DELETE FROM jianya_submissions WHERE assignment_id = ?", (assignment_id,))
    conn.execute("DELETE FROM jianya_recipients WHERE assignment_id = ?", (assignment_id,))
    conn.execute("DELETE FROM jianya_reviews WHERE assignment_id = ?", (assignment_id,))
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
    correction: Any = None,
) -> dict[str, Any]:
    assignment = get_assignment(conn, assignment_id)
    if not assignment:
        raise ValueError("作业不存在或已删除")
    if subject not in OPEN_SUBJECTS:
        raise ValueError("科目无效")
    if not student_id:
        raise ValueError("缺少学号")
    if not is_recipient(conn, assignment_id, student_id):
        raise ValueError("这份作业未布置给你")
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
    correction_obj = correction if isinstance(correction, dict) else None
    submitted_at = utc_now()
    conn.execute(
        """
        INSERT INTO jianya_submissions (
            assignment_id, student_id, book_id, subject, s_id,
            answers_json, correction_json, correct, total, wrong, blank, pct, submitted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            assignment_id,
            student_id,
            int(book_id),
            subject,
            int(s_id),
            json.dumps(answers_obj, ensure_ascii=False),
            json.dumps(correction_obj, ensure_ascii=False) if correction_obj else None,
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
    out: dict[str, Any] = {
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
    if correction_obj:
        out["correction"] = correction_obj
    return out


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
    if not is_recipient(conn, assignment_id, student_id):
        raise ValueError("这份作业未布置给你")
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
