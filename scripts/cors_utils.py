"""Explicit CORS allowlist for the local IELTS API server."""

from __future__ import annotations

import os
import urllib.parse
from typing import Optional

PRODUCTION_CORS_ORIGINS = frozenset(
    {
        "https://training.oyenglish.com.cn",
        "http://training.oyenglish.com.cn",
    }
)

LOCAL_CORS_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


def _extra_cors_origins() -> frozenset[str]:
    raw = (os.environ.get("IELTS_CORS_ORIGINS") or "").strip()
    if not raw:
        return frozenset()
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def is_allowed_cors_origin(origin: str) -> bool:
    if not origin:
        return False
    if origin in PRODUCTION_CORS_ORIGINS or origin in _extra_cors_origins():
        return True
    try:
        parsed = urllib.parse.urlparse(origin)
    except ValueError:
        return False
    if parsed.scheme != "http":
        return False
    host = (parsed.hostname or "").lower()
    return host in LOCAL_CORS_HOSTS


def cors_headers_for_origin(origin: Optional[str]) -> dict[str, str]:
    if not origin or not is_allowed_cors_origin(origin):
        return {}
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Vary": "Origin",
    }
