# -*- coding: utf-8 -*-
"""试用身份：系统生成激活码为唯一标识，同一码共用一条记录与进度。"""
from __future__ import annotations

import json
import math
import re
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Any

from student_api import utc_now

_CODE_ALPHABET = "".join(c for c in string.ascii_uppercase + string.digits if c not in "O0IL1")
_WX_RE = re.compile(r"\s+")
DEFAULT_TRIAL_DAYS = 15
MODULE_LISTENING_BASIC = "listening_basic"


def ensure_trial_tables(conn: Any) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trial_activation_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            advisor_wx TEXT NOT NULL DEFAULT '',
            guest_wx TEXT NOT NULL DEFAULT '',
            days_valid INTEGER NOT NULL DEFAULT 15,
            created_at TEXT NOT NULL,
            used_at TEXT,
            guest_name TEXT DEFAULT '',
            guest_contact TEXT DEFAULT '',
            target_score REAL DEFAULT 6.5,
            expires_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_trial_codes_guest_wx
        ON trial_activation_codes(guest_wx)
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trial_module_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL DEFAULT '',
            guest_wx TEXT NOT NULL DEFAULT '',
            module_type TEXT NOT NULL,
            progress_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL
        )
        """
    )
    cols = {
        str(r[1])
        for r in conn.execute("PRAGMA table_info(trial_module_progress)").fetchall()
    }
    if "code" not in cols:
        try:
            conn.execute(
                "ALTER TABLE trial_module_progress ADD COLUMN code TEXT NOT NULL DEFAULT ''"
            )
        except Exception:
            pass
    # 进度按激活码唯一（旧库可能有空 code，失败则忽略，读写仍按 code 匹配）
    try:
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_trial_progress_code_module
            ON trial_module_progress(code, module_type)
            """
        )
    except Exception:
        pass
    conn.commit()


def _clean(value: Any, max_len: int) -> str:
    s = _WX_RE.sub(" ", str(value or "").strip())
    if len(s) > max_len:
        s = s[:max_len]
    return s


def _normalize_code(value: Any) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", str(value or "").strip()).upper()


def _parse_iso(value: Any) -> datetime | None:
    s = str(value or "").strip()
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _days_left(expires_at: Any) -> int:
    exp = _parse_iso(expires_at)
    if not exp:
        return 0
    secs = (exp - datetime.now(timezone.utc)).total_seconds()
    if secs <= 0:
        return 0
    return max(1, int(math.ceil(secs / 86400.0)))


def _clamp_days(value: Any, default: int = DEFAULT_TRIAL_DAYS) -> int:
    try:
        days = int(value)
    except (TypeError, ValueError):
        days = default
    return max(1, min(days, 30))


def _new_code(conn: Any) -> str:
    for _ in range(20):
        code = "".join(secrets.choice(_CODE_ALPHABET) for _ in range(8))
        row = conn.execute(
            "SELECT 1 FROM trial_activation_codes WHERE code = ?", (code,)
        ).fetchone()
        if not row:
            return code
    raise RuntimeError("无法生成唯一激活码，请重试")


def _row_to_claim(row: Any, *, returning: bool = False) -> dict[str, Any]:
    expires_at = row["expires_at"] or ""
    days_left = _days_left(expires_at)
    if not expires_at and row["used_at"]:
        days = _clamp_days(row["days_valid"])
        activated = _parse_iso(row["used_at"]) or datetime.now(timezone.utc)
        expires = activated + timedelta(days=days)
        expires_at = expires.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        days_left = _days_left(expires_at)
    return {
        "code": row["code"],
        "guest_name": row["guest_name"] or "",
        "guest_wx": row["guest_wx"] or "",
        "contact": row["guest_contact"] or "",
        "target_score": float(row["target_score"] or 6.5),
        "advisor_wx": row["advisor_wx"] or "",
        "days_valid": _clamp_days(row["days_valid"]),
        "days_left": days_left,
        "expires_at": expires_at,
        "activated_at": row["used_at"] or "",
        "returning": returning,
        "once": False,
    }


def _get_by_code(conn: Any, code: str) -> Any:
    code = _normalize_code(code)
    if not code:
        return None
    return conn.execute(
        """
        SELECT id, code, advisor_wx, guest_wx, days_valid, created_at, used_at,
               guest_name, guest_contact, target_score, expires_at
        FROM trial_activation_codes
        WHERE code = ?
        """,
        (code,),
    ).fetchone()


def create_trial_code(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """顾问生成系统激活码（唯一标识，15 天内可多端用同一码进同一记录）。"""
    ensure_trial_tables(conn)
    advisor_wx = _clean(payload.get("advisor_wx") or payload.get("wx"), 80)
    # 客户微信仅备注，不再作为身份
    guest_wx = _clean(payload.get("guest_wx") or payload.get("client_wx") or payload.get("note"), 80)
    if not advisor_wx:
        raise ValueError("请填写顾问微信号")
    days = _clamp_days(payload.get("days_valid") or payload.get("days") or DEFAULT_TRIAL_DAYS)

    code = _new_code(conn)
    now = utc_now()
    conn.execute(
        """
        INSERT INTO trial_activation_codes (
            code, advisor_wx, guest_wx, days_valid, created_at
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (code, advisor_wx, guest_wx, days, now),
    )
    conn.commit()
    return {
        "code": code,
        "advisor_wx": advisor_wx,
        "guest_wx": guest_wx,
        "days_valid": days,
        "created_at": now,
        "activated": False,
        "expires_at": "",
        "days_left": days,
        "reused": False,
        "once": False,
    }


def claim_trial_code(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """学生用激活码进入：同一码共用一条记录；首次填姓名，之后只输码即可。"""
    ensure_trial_tables(conn)
    code = _normalize_code(payload.get("code"))
    name = _clean(payload.get("guest_name") or payload.get("name"), 40)
    guest_wx = _clean(payload.get("guest_wx") or payload.get("client_wx"), 80)
    contact = _clean(payload.get("contact") or payload.get("guest_contact"), 80)
    if not code:
        raise ValueError("请填写激活码")

    try:
        target = float(payload.get("target_score") or 6.5)
    except (TypeError, ValueError):
        target = 6.5
    if target not in (5.0, 5.5, 6.0, 6.5, 7.0, 7.5):
        target = 6.5

    row = _get_by_code(conn, code)
    if not row:
        raise ValueError("激活码无效，请向顾问索取系统生成的激活码")

    # 已激活：同一码再次进入 → 同一条记录
    if row["used_at"]:
        claim = _row_to_claim(row, returning=True)
        if claim["days_left"] <= 0:
            raise ValueError("试用已到期，请微信联系顾问重新开通")
        expires_at = claim["expires_at"]
        keep_name = name or (row["guest_name"] or "")
        keep_contact = contact or (row["guest_contact"] or "")
        keep_wx = guest_wx or (row["guest_wx"] or "")
        keep_target = (
            target
            if payload.get("target_score") is not None
            else float(row["target_score"] or 6.5)
        )
        if keep_target not in (5.0, 5.5, 6.0, 6.5, 7.0, 7.5):
            keep_target = 6.5
        conn.execute(
            """
            UPDATE trial_activation_codes
            SET guest_name = ?, guest_contact = ?, guest_wx = ?, target_score = ?,
                expires_at = COALESCE(NULLIF(expires_at, ''), ?)
            WHERE id = ?
            """,
            (keep_name, keep_contact, keep_wx, keep_target, expires_at, row["id"]),
        )
        conn.commit()
        refreshed = _get_by_code(conn, code)
        return _row_to_claim(refreshed, returning=True)

    # 首次激活
    if not name:
        raise ValueError("首次使用请填写姓名")
    days = _clamp_days(row["days_valid"] or DEFAULT_TRIAL_DAYS)
    now = utc_now()
    expires = (
        datetime.now(timezone.utc) + timedelta(days=days)
    ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    conn.execute(
        """
        UPDATE trial_activation_codes
        SET used_at = ?, guest_name = ?, guest_contact = ?, guest_wx = ?,
            target_score = ?, expires_at = ?
        WHERE id = ? AND used_at IS NULL
        """,
        (now, name, contact, guest_wx, target, expires, row["id"]),
    )
    conn.commit()
    refreshed = _get_by_code(conn, code)
    if not refreshed or not refreshed["used_at"]:
        raise ValueError("激活失败，请重试")
    return _row_to_claim(refreshed, returning=False)


def login_trial(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """已激活客户用激活码再次进入。"""
    ensure_trial_tables(conn)
    code = _normalize_code(payload.get("code"))
    if not code:
        raise ValueError("请填写激活码")
    row = _get_by_code(conn, code)
    if not row:
        raise ValueError("激活码无效")
    if not row["used_at"]:
        raise ValueError("请先完成首次登录（填写姓名）")
    claim = _row_to_claim(row, returning=True)
    if claim["days_left"] <= 0:
        raise ValueError("试用已到期，请微信联系顾问重新开通")
    return claim


def _require_active_trial(conn: Any, code: str) -> Any:
    code = _normalize_code(code)
    if not code:
        raise ValueError("缺少激活码")
    row = _get_by_code(conn, code)
    if not row or not row["used_at"]:
        raise ValueError("试用未激活")
    claim = _row_to_claim(row, returning=True)
    if claim["days_left"] <= 0:
        raise ValueError("试用已到期")
    return row


def save_trial_progress(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    ensure_trial_tables(conn)
    code = _normalize_code(payload.get("code"))
    module_type = _clean(payload.get("module_type") or MODULE_LISTENING_BASIC, 40) or MODULE_LISTENING_BASIC
    row = _require_active_trial(conn, code)

    progress = payload.get("progress")
    if progress is None:
        raise ValueError("缺少进度数据")
    if isinstance(progress, str):
        try:
            progress = json.loads(progress)
        except json.JSONDecodeError as exc:
            raise ValueError("进度数据格式错误") from exc
    if not isinstance(progress, dict):
        raise ValueError("进度数据须为对象")

    now = utc_now()
    blob = json.dumps(progress, ensure_ascii=False)
    guest_wx = _clean(row["guest_wx"], 80)
    existing = conn.execute(
        """
        SELECT id FROM trial_module_progress
        WHERE code = ? AND module_type = ?
        """,
        (code, module_type),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE trial_module_progress
            SET progress_json = ?, updated_at = ?, guest_wx = ?
            WHERE id = ?
            """,
            (blob, now, guest_wx, existing["id"]),
        )
    else:
        conn.execute(
            """
            INSERT INTO trial_module_progress (code, guest_wx, module_type, progress_json, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (code, guest_wx, module_type, blob, now),
        )
    conn.commit()
    return {
        "code": code,
        "module_type": module_type,
        "updated_at": now,
        "ok": True,
    }


def get_trial_progress(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    ensure_trial_tables(conn)
    code = _normalize_code(payload.get("code"))
    module_type = _clean(payload.get("module_type") or MODULE_LISTENING_BASIC, 40) or MODULE_LISTENING_BASIC
    _require_active_trial(conn, code)

    row = conn.execute(
        """
        SELECT progress_json, updated_at
        FROM trial_module_progress
        WHERE code = ? AND module_type = ?
        """,
        (code, module_type),
    ).fetchone()
    if not row:
        return {
            "code": code,
            "module_type": module_type,
            "progress": None,
            "updated_at": "",
        }
    try:
        progress = json.loads(row["progress_json"] or "{}")
    except json.JSONDecodeError:
        progress = {}
    return {
        "code": code,
        "module_type": module_type,
        "progress": progress,
        "updated_at": row["updated_at"] or "",
    }


def _progress_summary(progress: Any) -> dict[str, Any]:
    if not isinstance(progress, dict):
        return {"groups_done": 0, "seconds": 0}
    status = progress.get("groupStatus") or []
    done = sum(1 for s in status if s == "completed")
    seconds = int(progress.get("totalSecondsLearned") or 0)
    return {"groups_done": done, "groups_total": len(status) or None, "seconds": seconds}


def list_trial_guests(conn: Any, limit: int = 200) -> list[dict[str, Any]]:
    ensure_trial_tables(conn)
    try:
        limit = max(1, min(int(limit), 500))
    except (TypeError, ValueError):
        limit = 200
    rows = conn.execute(
        """
        SELECT c.id, c.code, c.advisor_wx, c.guest_wx, c.days_valid, c.created_at,
               c.used_at, c.guest_name, c.guest_contact, c.target_score, c.expires_at,
               p.progress_json, p.updated_at AS progress_updated_at
        FROM trial_activation_codes c
        LEFT JOIN trial_module_progress p
          ON p.code = c.code AND p.module_type = ?
        WHERE c.used_at IS NOT NULL
        ORDER BY c.used_at DESC
        LIMIT ?
        """,
        (MODULE_LISTENING_BASIC, limit),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        try:
            progress = json.loads(row["progress_json"] or "{}") if row["progress_json"] else None
        except json.JSONDecodeError:
            progress = None
        claim = _row_to_claim(row, returning=True)
        summary = _progress_summary(progress)
        out.append(
            {
                "code": claim["code"],
                "guest_name": claim["guest_name"],
                "guest_wx": claim["guest_wx"],
                "contact": claim["contact"],
                "advisor_wx": claim["advisor_wx"],
                "target_score": claim["target_score"],
                "activated_at": claim["activated_at"],
                "expires_at": claim["expires_at"],
                "days_left": claim["days_left"],
                "days_valid": claim["days_valid"],
                "listening_basic": summary,
                "progress_updated_at": row["progress_updated_at"] or "",
            }
        )
    return out
