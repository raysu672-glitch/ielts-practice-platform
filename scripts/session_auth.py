"""HMAC-signed HttpOnly session cookies for the local IELTS server."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from http import cookies
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SECRET_PATH = ROOT / "data" / "session_secret.txt"
SESSION_COOKIE_NAME = "ielts_session"
SESSION_DAYS = 7
SESSION_MAX_AGE = SESSION_DAYS * 24 * 60 * 60


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> bytes:
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def load_session_secret(secret_path: Path = DEFAULT_SECRET_PATH) -> bytes:
    env = (os.environ.get("IELTS_SESSION_SECRET") or "").strip()
    if env:
        return env.encode("utf-8")
    secret_path.parent.mkdir(parents=True, exist_ok=True)
    if secret_path.exists():
        data = secret_path.read_text(encoding="utf-8").strip()
        if data:
            return data.encode("utf-8")
    token = secrets.token_urlsafe(32)
    secret_path.write_text(token + "\n", encoding="utf-8")
    try:
        os.chmod(secret_path, 0o600)
    except OSError:
        pass
    return token.encode("utf-8")


def issue_session_token(
    *,
    role: str,
    subject_id: str,
    secret: bytes,
    max_age: int = SESSION_MAX_AGE,
) -> str:
    payload = {
        "role": role,
        "id": subject_id,
        "exp": int(time.time()) + int(max_age),
    }
    body = _b64url_encode(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    sig = _b64url_encode(hmac.new(secret, body.encode("ascii"), hashlib.sha256).digest())
    return f"{body}.{sig}"


def parse_session_token(token: str, secret: bytes) -> Optional[dict[str, Any]]:
    if not token or "." not in token:
        return None
    body, sig = token.rsplit(".", 1)
    expected = _b64url_encode(hmac.new(secret, body.encode("ascii"), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        payload = json.loads(_b64url_decode(body).decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    role = str(payload.get("role") or "")
    subject_id = str(payload.get("id") or "")
    exp = int(payload.get("exp") or 0)
    if role not in ("student", "teacher") or not subject_id:
        return None
    if exp < int(time.time()):
        return None
    return {"role": role, "id": subject_id, "exp": exp}


def read_cookie_header(cookie_header: str, name: str = SESSION_COOKIE_NAME) -> Optional[str]:
    if not cookie_header:
        return None
    jar = cookies.SimpleCookie()
    try:
        jar.load(cookie_header)
    except cookies.CookieError:
        return None
    morsel = jar.get(name)
    return morsel.value if morsel else None


def build_session_cookie(
    token: str,
    *,
    max_age: int = SESSION_MAX_AGE,
    clear: bool = False,
    secure: bool = False,
) -> str:
    jar = cookies.SimpleCookie()
    jar[SESSION_COOKIE_NAME] = "" if clear else token
    morsel = jar[SESSION_COOKIE_NAME]
    morsel["path"] = "/"
    morsel["httponly"] = True
    morsel["samesite"] = "Lax"
    if secure and not clear:
        morsel["secure"] = True
    if clear:
        morsel["max-age"] = "0"
        morsel["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    else:
        morsel["max-age"] = str(int(max_age))
    return morsel.OutputString()


def public_student(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "student_id": row.get("student_id"),
        "name": row.get("name"),
        "is_password_changed": bool(row.get("is_password_changed")),
        "target_score": row.get("target_score"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def public_teacher(row: dict[str, Any]) -> dict[str, Any]:
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
