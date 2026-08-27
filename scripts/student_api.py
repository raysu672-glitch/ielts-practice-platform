"""Student-scoped API helpers (session identity is enforced by the caller)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional  # noqa: F401 — Optional used below

from password_utils import hash_password

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def dumps_details(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value if value is not None else [], ensure_ascii=False)


def norm_speaking_question_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(text or "").lower())


def upsert_speaking_best_score(
    conn: Any,
    student_id: str,
    question_text: str,
    score: float,
    *,
    part: str = "p1",
) -> dict[str, Any]:
    """Keep the highest Band for a student+question. Returns the stored row dict."""
    qtext = str(question_text or "").strip()
    key = norm_speaking_question_key(qtext)
    band = float(score)
    if not student_id or not key or band <= 0:
        raise ValueError("student_id / question / score 无效")
    part = str(part or "p1").strip() or "p1"
    now = utc_now()
    existing = conn.execute(
        """
        SELECT best_score, question_text FROM speaking_best_scores
        WHERE student_id = ? AND question_key = ?
        """,
        (student_id, key),
    ).fetchone()
    if existing is None:
        conn.execute(
            """
            INSERT INTO speaking_best_scores
                (student_id, question_key, question_text, part, best_score, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (student_id, key, qtext, part, band, now),
        )
        best = band
    else:
        prev = float(existing["best_score"] if hasattr(existing, "keys") else existing[0])
        best = max(prev, band)
        stored_text = existing["question_text"] if hasattr(existing, "keys") else existing[1]
        final_text = qtext or (stored_text or "")
        conn.execute(
            """
            UPDATE speaking_best_scores
            SET best_score = ?, question_text = ?, part = ?, updated_at = ?
            WHERE student_id = ? AND question_key = ?
            """,
            (best, final_text, part, now, student_id, key),
        )
    conn.commit()
    return {
        "student_id": student_id,
        "question_key": key,
        "question_text": qtext,
        "part": part,
        "best_score": best,
    }


def _ingest_speaking_details(
    conn: Any,
    student_id: str,
    details: Any,
    fallback_score: Optional[float] = None,
) -> None:
    items = details
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except json.JSONDecodeError:
            items = []
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict):
            continue
        qtext = item.get("question") or item.get("q") or item.get("title") or ""
        overall = item.get("overall")
        if overall is None:
            overall = item.get("score")
        if overall is None:
            overall = fallback_score
        try:
            band = float(overall)
        except (TypeError, ValueError):
            continue
        if not qtext or band <= 0:
            continue
        try:
            upsert_speaking_best_score(conn, student_id, str(qtext), band, part="p1")
        except ValueError:
            continue


def backfill_speaking_best_from_test_records(conn: Any, student_id: str) -> None:
    rows = conn.execute(
        """
        SELECT score, details FROM test_records
        WHERE student_id = ? AND module_type = 'speaking'
        ORDER BY created_at ASC
        """,
        (student_id,),
    ).fetchall()
    for row in rows:
        details = row["details"] if hasattr(row, "keys") else row[1]
        score = row["score"] if hasattr(row, "keys") else row[0]
        try:
            fallback = float(score) if score is not None else None
        except (TypeError, ValueError):
            fallback = None
        _ingest_speaking_details(conn, student_id, details, fallback)


def load_speaking_best_scores(conn: Any, student_id: str) -> dict[str, float]:
    """Return {question_key: best_score}. Backfills from historical speaking test_records."""
    backfill_speaking_best_from_test_records(conn, student_id)
    rows = conn.execute(
        """
        SELECT question_key, best_score FROM speaking_best_scores
        WHERE student_id = ?
        """,
        (student_id,),
    ).fetchall()
    out: dict[str, float] = {}
    for row in rows:
        key = row["question_key"] if hasattr(row, "keys") else row[0]
        val = row["best_score"] if hasattr(row, "keys") else row[1]
        try:
            out[str(key)] = float(val)
        except (TypeError, ValueError):
            continue
    return out


def load_progress(conn: Any, student_id: str) -> dict[str, Any]:
    records = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM test_records WHERE student_id = ? ORDER BY created_at DESC",
            (student_id,),
        ).fetchall()
    ]
    sessions = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM study_sessions WHERE student_id = ? ORDER BY created_at DESC",
            (student_id,),
        ).fetchall()
    ]
    wrong_words = [
        dict(row)
        for row in conn.execute(
            """
            SELECT * FROM wrong_words
            WHERE student_id = ? AND is_mastered = 0
            ORDER BY last_tested DESC
            """,
            (student_id,),
        ).fetchall()
    ]
    for item in records + sessions:
        details = item.get("details")
        if isinstance(details, str):
            try:
                item["details"] = json.loads(details)
            except json.JSONDecodeError:
                pass
    for item in records:
        if "is_passed" in item:
            item["is_passed"] = bool(item["is_passed"])
    for item in wrong_words:
        item["is_mastered"] = bool(item.get("is_mastered"))
    return {
        "test_records": records,
        "study_sessions": sessions,
        "wrong_words": wrong_words,
        "wrong_book_counts": load_wrong_book_counts(conn, student_id),
    }


def load_test_records(conn: Any, student_id: str) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM test_records WHERE student_id = ? ORDER BY created_at DESC",
            (student_id,),
        ).fetchall()
    ]
    for item in rows:
        if isinstance(item.get("details"), str):
            try:
                item["details"] = json.loads(item["details"])
            except json.JSONDecodeError:
                pass
        item["is_passed"] = bool(item.get("is_passed"))
    return rows


def load_standards(conn: Any) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM pass_standards WHERE is_active = 1 ORDER BY module_type"
        ).fetchall()
    ]
    for item in rows:
        item["is_active"] = bool(item.get("is_active"))
    return rows


def change_password(conn: Any, student_id: str, new_password: str) -> Optional[str]:
    password = str(new_password or "").strip()
    if len(password) < 4:
        return "密码至少4位"
    conn.execute(
        """
        UPDATE students
        SET password = ?,
            is_password_changed = 1,
            updated_at = ?
        WHERE student_id = ?
        """,
        (hash_password(password), utc_now(), student_id),
    )
    conn.commit()
    return None


def insert_study_session(conn: Any, student_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    now = utc_now()
    record = {
        "student_id": student_id,
        "module_type": str(payload.get("module_type") or payload.get("moduleType") or "dictation"),
        "module_name": payload.get("module_name") or payload.get("moduleName"),
        "session_kind": payload.get("session_kind") or payload.get("sessionKind") or "study",
        "words_tested": int(payload.get("words_tested") or payload.get("wordsTested") or 0),
        "initial_correct": int(payload.get("initial_correct") or payload.get("initialCorrect") or 0),
        "initial_wrong": int(payload.get("initial_wrong") or payload.get("initialWrong") or 0),
        "groups_completed": int(payload.get("groups_completed") or payload.get("groupsCompleted") or 0),
        "score_percent": payload.get("score_percent", payload.get("scorePercent")),
        "duration_seconds": max(0, int(round(float(payload.get("duration_seconds") or payload.get("durationSeconds") or 0)))),
        "details": dumps_details(payload.get("details")),
        "started_at": payload.get("started_at") or payload.get("startedAt"),
        "ended_at": payload.get("ended_at") or payload.get("endedAt") or now,
        "created_at": now,
    }
    if record["session_kind"] not in ("study", "test"):
        record["session_kind"] = "study"
    cur = conn.execute(
        """
        INSERT INTO study_sessions (
            student_id, module_type, module_name, session_kind,
            words_tested, initial_correct, initial_wrong, groups_completed,
            score_percent, duration_seconds, details, started_at, ended_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["student_id"],
            record["module_type"],
            record["module_name"],
            record["session_kind"],
            record["words_tested"],
            record["initial_correct"],
            record["initial_wrong"],
            record["groups_completed"],
            record["score_percent"],
            record["duration_seconds"],
            record["details"],
            record["started_at"],
            record["ended_at"],
            record["created_at"],
        ),
    )
    conn.commit()
    record["id"] = cur.lastrowid
    record["details"] = payload.get("details") or []
    return record


def insert_test_record(conn: Any, student_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    now = utc_now()
    total_count = int(payload.get("total_count") or payload.get("totalCount") or 0)
    correct_count = int(payload.get("correct_count") or payload.get("correctCount") or 0)
    score = payload.get("score")
    if score is None:
        score = payload.get("score_percent", payload.get("scorePercent"))
    if score is None:
        score = round(correct_count / total_count * 100, 2) if total_count > 0 else 0
    score = float(score)
    threshold = float(payload.get("pass_threshold") or payload.get("passThreshold") or 80)
    is_passed = payload.get("is_passed", payload.get("isPassed"))
    if is_passed is None:
        is_passed = score >= threshold
    record = {
        "student_id": student_id,
        "module_type": str(payload.get("module_type") or payload.get("moduleType") or "dictation"),
        "module_name": payload.get("module_name") or payload.get("moduleName") or "听力1000词",
        "test_type": payload.get("test_type") or payload.get("testType") or "module_test",
        "score": score,
        "correct_count": correct_count,
        "total_count": total_count,
        "is_passed": 1 if as_bool(is_passed) else 0,
        "pass_threshold": threshold,
        "duration_seconds": max(0, int(round(float(payload.get("duration_seconds") or payload.get("durationSeconds") or 0)))),
        "details": dumps_details(payload.get("details")),
        "started_at": payload.get("started_at") or payload.get("startedAt"),
        "ended_at": payload.get("ended_at") or payload.get("endedAt") or now,
        "created_at": now,
    }
    cur = conn.execute(
        """
        INSERT INTO test_records (
            student_id, module_type, module_name, test_type, score,
            correct_count, total_count, is_passed, pass_threshold,
            duration_seconds, details, started_at, ended_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["student_id"],
            record["module_type"],
            record["module_name"],
            record["test_type"],
            record["score"],
            record["correct_count"],
            record["total_count"],
            record["is_passed"],
            record["pass_threshold"],
            record["duration_seconds"],
            record["details"],
            record["started_at"],
            record["ended_at"],
            record["created_at"],
        ),
    )
    conn.commit()
    record["id"] = cur.lastrowid
    record["is_passed"] = bool(record["is_passed"])
    record["details"] = payload.get("details") or []
    if record["module_type"] == "speaking":
        _ingest_speaking_details(conn, student_id, record["details"], record["score"])
    return record


def load_wrong_words(
    conn: Any,
    student_id: str,
    *,
    module_type: Optional[str] = None,
    unmastered_only: bool = False,
) -> list[dict[str, Any]]:
    sql = "SELECT * FROM wrong_words WHERE student_id = ?"
    params: list[Any] = [student_id]
    if module_type:
        sql += " AND module_type = ?"
        params.append(module_type)
    if unmastered_only:
        sql += " AND is_mastered = 0"
    sql += " ORDER BY last_tested DESC"
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    for item in rows:
        item["is_mastered"] = bool(item.get("is_mastered"))
    return rows


WRONG_STREAK_TO_MASTER = 3
DICTATION_WRONG_MODULES = {"dictation", "listening_basic"}


def _dumps_payload(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value if value is not None else {}, ensure_ascii=False)


def _parse_payload(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if not value:
        return {}
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return {}


def apply_wrong_word_results(
    conn: Any,
    student_id: str,
    module_type: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    now = utc_now()
    new_wrong_count = 0
    for item in results or []:
        word = str(item.get("word") or "").strip()
        if not word:
            continue
        skipped = as_bool(item.get("skipped"))
        is_correct = as_bool(item.get("is_correct", item.get("isCorrect")))
        row = conn.execute(
            """
            SELECT * FROM wrong_words
            WHERE student_id = ? AND module_type = ? AND word = ?
            """,
            (student_id, module_type, word),
        ).fetchone()
        if not is_correct and not skipped:
            if row:
                conn.execute(
                    """
                    UPDATE wrong_words
                    SET wrong_count = ?, correct_streak = 0, last_tested = ?, is_mastered = 0
                    WHERE id = ?
                    """,
                    (int(row["wrong_count"] or 0) + 1, now, row["id"]),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO wrong_words (
                        student_id, module_type, word, wrong_count, correct_streak, last_tested, is_mastered
                    ) VALUES (?, ?, ?, 1, 0, ?, 0)
                    """,
                    (student_id, module_type, word, now),
                )
                new_wrong_count += 1
        elif is_correct and row and not bool(row["is_mastered"]):
            new_streak = int(row["correct_streak"] or 0) + 1
            conn.execute(
                """
                UPDATE wrong_words
                SET correct_streak = ?, is_mastered = ?, last_tested = ?
                WHERE id = ?
                """,
                (
                    new_streak,
                    1 if new_streak >= WRONG_STREAK_TO_MASTER else 0,
                    now,
                    row["id"],
                ),
            )
    conn.commit()
    return {"new_wrong_count": new_wrong_count}


def _word_row_to_item(row: dict[str, Any]) -> dict[str, Any]:
    word = str(row.get("word") or "")
    return {
        "id": row.get("id"),
        "student_id": row.get("student_id"),
        "module_type": row.get("module_type"),
        "item_key": word,
        "title": word,
        "payload": {"word": word},
        "wrong_count": int(row.get("wrong_count") or 0),
        "correct_streak": int(row.get("correct_streak") or 0),
        "last_tested": row.get("last_tested"),
        "is_mastered": bool(row.get("is_mastered")),
    }


def _item_row_to_dict(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["is_mastered"] = bool(item.get("is_mastered"))
    item["payload"] = _parse_payload(item.get("payload"))
    item["wrong_count"] = int(item.get("wrong_count") or 0)
    item["correct_streak"] = int(item.get("correct_streak") or 0)
    return item


def load_wrong_items(
    conn: Any,
    student_id: str,
    *,
    module_type: Optional[str] = None,
    unmastered_only: bool = False,
) -> list[dict[str, Any]]:
    sql = "SELECT * FROM wrong_items WHERE student_id = ?"
    params: list[Any] = [student_id]
    if module_type:
        sql += " AND module_type = ?"
        params.append(module_type)
    if unmastered_only:
        sql += " AND is_mastered = 0"
    sql += " ORDER BY last_tested DESC"
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    return [_item_row_to_dict(item) for item in rows]


def load_wrong_book_items(
    conn: Any,
    student_id: str,
    module_type: str,
    *,
    unmastered_only: bool = True,
) -> list[dict[str, Any]]:
    if module_type in DICTATION_WRONG_MODULES:
        rows = load_wrong_words(
            conn,
            student_id,
            module_type=module_type,
            unmastered_only=unmastered_only,
        )
        return [_word_row_to_item(row) for row in rows]
    return load_wrong_items(
        conn,
        student_id,
        module_type=module_type,
        unmastered_only=unmastered_only,
    )


def load_wrong_book_counts(conn: Any, student_id: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in conn.execute(
        """
        SELECT module_type, COUNT(*) AS c FROM wrong_words
        WHERE student_id = ? AND is_mastered = 0
        GROUP BY module_type
        """,
        (student_id,),
    ).fetchall():
        counts[str(row["module_type"])] = int(row["c"] or 0)
    try:
        item_rows = conn.execute(
            """
            SELECT module_type, COUNT(*) AS c FROM wrong_items
            WHERE student_id = ? AND is_mastered = 0
            GROUP BY module_type
            """,
            (student_id,),
        ).fetchall()
    except Exception:
        item_rows = []
    for row in item_rows:
        key = str(row["module_type"])
        counts[key] = counts.get(key, 0) + int(row["c"] or 0)
    return counts


def apply_wrong_item_results(
    conn: Any,
    student_id: str,
    module_type: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    if module_type in DICTATION_WRONG_MODULES:
        mapped = []
        for item in results or []:
            word = str(item.get("word") or item.get("item_key") or item.get("title") or "").strip()
            if not word:
                continue
            mapped.append(
                {
                    "word": word,
                    "is_correct": item.get("is_correct", item.get("isCorrect")),
                    "skipped": item.get("skipped"),
                }
            )
        return apply_wrong_word_results(conn, student_id, module_type, mapped)

    now = utc_now()
    new_wrong_count = 0
    for item in results or []:
        item_key = str(item.get("item_key") or item.get("itemKey") or "").strip()
        if not item_key:
            continue
        skipped = as_bool(item.get("skipped"))
        is_correct = as_bool(item.get("is_correct", item.get("isCorrect")))
        title = str(item.get("title") or item_key)
        payload = _dumps_payload(item.get("payload") if item.get("payload") is not None else {})
        row = conn.execute(
            """
            SELECT * FROM wrong_items
            WHERE student_id = ? AND module_type = ? AND item_key = ?
            """,
            (student_id, module_type, item_key),
        ).fetchone()
        if not is_correct and not skipped:
            if row:
                conn.execute(
                    """
                    UPDATE wrong_items
                    SET title = ?, payload = ?, wrong_count = ?, correct_streak = 0,
                        last_tested = ?, is_mastered = 0
                    WHERE id = ?
                    """,
                    (
                        title or row["title"],
                        payload or row["payload"],
                        int(row["wrong_count"] or 0) + 1,
                        now,
                        row["id"],
                    ),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO wrong_items (
                        student_id, module_type, item_key, title, payload,
                        wrong_count, correct_streak, last_tested, is_mastered
                    ) VALUES (?, ?, ?, ?, ?, 1, 0, ?, 0)
                    """,
                    (student_id, module_type, item_key, title, payload, now),
                )
                new_wrong_count += 1
        elif is_correct and row and not bool(row["is_mastered"]):
            new_streak = int(row["correct_streak"] or 0) + 1
            conn.execute(
                """
                UPDATE wrong_items
                SET correct_streak = ?, is_mastered = ?, last_tested = ?
                WHERE id = ?
                """,
                (
                    new_streak,
                    1 if new_streak >= WRONG_STREAK_TO_MASTER else 0,
                    now,
                    row["id"],
                ),
            )
    conn.commit()
    return {"new_wrong_count": new_wrong_count}


def load_word_mastery(conn: Any, student_id: str) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in conn.execute(
            "SELECT * FROM word_mastery WHERE student_id = ?",
            (student_id,),
        ).fetchall()
    ]
    for item in rows:
        item["is_initial_correct"] = bool(item.get("is_initial_correct"))
        if item.get("last_result") is not None:
            item["last_result"] = bool(item["last_result"])
    return rows


def upsert_word_mastery(conn: Any, student_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    word = str(payload.get("word") or "").strip()
    if not word:
        raise ValueError("缺少单词")
    is_correct = as_bool(payload.get("is_correct", payload.get("isCorrect")))
    is_initial = as_bool(payload.get("is_initial", payload.get("isInitial")))
    now = utc_now()
    row = conn.execute(
        "SELECT * FROM word_mastery WHERE student_id = ? AND word = ?",
        (student_id, word),
    ).fetchone()
    if row:
        correct_count = int(row["correct_count"] or 0) + (1 if is_correct else 0)
        wrong_count = int(row["wrong_count"] or 0) + (0 if is_correct else 1)
        is_initial_correct = bool(row["is_initial_correct"]) or (is_initial and is_correct)
        conn.execute(
            """
            UPDATE word_mastery
            SET correct_count = ?,
                wrong_count = ?,
                is_initial_correct = ?,
                last_result = ?,
                last_practiced_at = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                correct_count,
                wrong_count,
                1 if is_initial_correct else 0,
                1 if is_correct else 0,
                now,
                now,
                row["id"],
            ),
        )
        conn.commit()
        return {
            "id": row["id"],
            "student_id": student_id,
            "word": word,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "is_initial_correct": is_initial_correct,
            "last_result": is_correct,
            "last_practiced_at": now,
        }
    cur = conn.execute(
        """
        INSERT INTO word_mastery (
            student_id, word, status, correct_count, wrong_count,
            is_initial_correct, last_result, last_practiced_at, created_at, updated_at
        ) VALUES (?, ?, 'learning', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            word,
            1 if is_correct else 0,
            0 if is_correct else 1,
            1 if (is_initial and is_correct) else 0,
            1 if is_correct else 0,
            now,
            now,
            now,
        ),
    )
    conn.commit()
    return {
        "id": cur.lastrowid,
        "student_id": student_id,
        "word": word,
        "correct_count": 1 if is_correct else 0,
        "wrong_count": 0 if is_correct else 1,
        "is_initial_correct": bool(is_initial and is_correct),
        "last_result": is_correct,
        "last_practiced_at": now,
    }
