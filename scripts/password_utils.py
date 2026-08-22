"""Password hashing helpers (stdlib only)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from typing import Any, Optional

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 310_000
HASH_PREFIX = "pbkdf2_sha256"

STUDENT_INITIAL_PASSWORD = "123456"
TEACHER_INITIAL_PASSWORD = "123456"


def _b64_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64_decode(text: str) -> bytes:
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def is_password_hashed(stored: str) -> bool:
    return str(stored or "").startswith(f"{HASH_PREFIX}$")


def hash_password(password: str) -> str:
    plain = str(password or "")
    if not plain:
        raise ValueError("password must not be empty")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        plain.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"{HASH_PREFIX}${PBKDF2_ITERATIONS}${_b64_encode(salt)}${_b64_encode(digest)}"


def verify_password(password: str, stored: str) -> bool:
    plain = str(password or "")
    stored = str(stored or "")
    if not plain or not stored:
        return False
    if is_password_hashed(stored):
        try:
            _prefix, iterations_text, salt_text, digest_text = stored.split("$", 3)
            iterations = int(iterations_text)
            salt = _b64_decode(salt_text)
            expected = _b64_decode(digest_text)
        except (TypeError, ValueError):
            return False
        actual = hashlib.pbkdf2_hmac(
            PBKDF2_ALGORITHM,
            plain.encode("utf-8"),
            salt,
            iterations,
        )
        return hmac.compare_digest(actual, expected)
    return hmac.compare_digest(plain, stored)


def upgrade_password_hash(
    conn: Any,
    *,
    table: str,
    id_column: str,
    row_id: str,
    plaintext: str,
    stored: str,
) -> None:
    if is_password_hashed(stored):
        return
    conn.execute(
        f"UPDATE {table} SET password = ? WHERE {id_column} = ?",
        (hash_password(plaintext), row_id),
    )
    conn.commit()


def authenticate_row_password(
    conn: Any,
    *,
    table: str,
    id_column: str,
    row_id: str,
    password: str,
) -> Optional[Any]:
    row = conn.execute(
        f"SELECT * FROM {table} WHERE {id_column} = ?",
        (row_id,),
    ).fetchone()
    if not row:
        return None
    stored = row["password"]
    if not verify_password(password, stored):
        return None
    upgrade_password_hash(
        conn,
        table=table,
        id_column=id_column,
        row_id=row_id,
        plaintext=password,
        stored=stored,
    )
    return row
