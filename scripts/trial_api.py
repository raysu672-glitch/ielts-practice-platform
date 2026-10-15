# -*- coding: utf-8 -*-
"""试用激活码：一码一次，顾问生成、客户领取。"""
from __future__ import annotations

import re
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Any

from student_api import utc_now

_CODE_ALPHABET = "".join(c for c in string.ascii_uppercase + string.digits if c not in "O0IL1")
_WX_RE = re.compile(r"\s+")


def ensure_trial_tables(conn: Any) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trial_activation_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            advisor_wx TEXT NOT NULL DEFAULT '',
            guest_wx TEXT NOT NULL DEFAULT '',
            days_valid INTEGER NOT NULL DEFAULT 5,
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
    conn.commit()


def _clean(value: Any, max_len: int) -> str:
    s = _WX_RE.sub(" ", str(value or "").strip())
    if len(s) > max_len:
        s = s[:max_len]
    return s


def _normalize_code(value: Any) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", str(value or "").strip()).upper()


def _new_code(conn: Any) -> str:
    for _ in range(20):
        code = "".join(secrets.choice(_CODE_ALPHABET) for _ in range(8))
        row = conn.execute(
            "SELECT 1 FROM trial_activation_codes WHERE code = ?", (code,)
        ).fetchone()
        if not row:
            return code
    raise RuntimeError("无法生成唯一激活码，请重试")


def create_trial_code(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """顾问生成一次性激活码（绑定顾问微信 + 客户微信）。"""
    ensure_trial_tables(conn)
    advisor_wx = _clean(payload.get("advisor_wx") or payload.get("wx"), 80)
    guest_wx = _clean(payload.get("guest_wx") or payload.get("client_wx"), 80)
    if not advisor_wx:
        raise ValueError("请填写顾问微信号")
    if not guest_wx:
        raise ValueError("请填写客户微信号")
    try:
        days = int(payload.get("days_valid") or payload.get("days") or 5)
    except (TypeError, ValueError):
        days = 5
    days = max(1, min(days, 30))

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
        "once": True,
    }


def claim_trial_code(conn: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """客户激活：一码一次，用过即失效。"""
    ensure_trial_tables(conn)
    code = _normalize_code(payload.get("code"))
    name = _clean(payload.get("guest_name") or payload.get("name"), 40)
    guest_wx = _clean(payload.get("guest_wx") or payload.get("client_wx"), 80)
    contact = _clean(payload.get("contact") or payload.get("guest_contact"), 80)
    if not code:
        raise ValueError("请填写激活码")
    if not name:
        raise ValueError("请填写姓名")
    if not guest_wx:
        raise ValueError("链接无效：缺少顾问登记的客户微信")

    try:
        target = float(payload.get("target_score") or 6.5)
    except (TypeError, ValueError):
        target = 6.5
    if target not in (5.0, 5.5, 6.0, 6.5, 7.0, 7.5):
        target = 6.5

    row = conn.execute(
        """
        SELECT id, code, advisor_wx, guest_wx, days_valid, created_at, used_at
        FROM trial_activation_codes
        WHERE code = ?
        """,
        (code,),
    ).fetchone()
    if not row:
        raise ValueError("激活码无效，请让顾问重新生成链接")
    if row["used_at"]:
        raise ValueError("该激活码已使用过，请联系顾问重新生成")
    bound = _clean(row["guest_wx"], 80)
    if bound and bound != guest_wx:
        raise ValueError("激活码与链接中的客户微信不匹配，请使用顾问发给你的原链接")

    now = utc_now()
    try:
        days = int(row["days_valid"] or 5)
    except (TypeError, ValueError):
        days = 5
    days = max(1, min(days, 30))
    expires = (
        datetime.now(timezone.utc) + timedelta(days=days)
    ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    cur = conn.execute(
        """
        UPDATE trial_activation_codes
        SET used_at = ?, guest_name = ?, guest_contact = ?,
            target_score = ?, expires_at = ?
        WHERE id = ? AND used_at IS NULL
        """,
        (now, name, contact, target, expires, row["id"]),
    )
    conn.commit()
    if cur.rowcount != 1:
        raise ValueError("该激活码已使用过，请联系顾问重新生成")

    return {
        "code": code,
        "guest_name": name,
        "guest_wx": guest_wx,
        "contact": contact,
        "target_score": target,
        "advisor_wx": row["advisor_wx"],
        "days_left": days,
        "expires_at": expires,
        "used_at": now,
        "once": True,
    }
