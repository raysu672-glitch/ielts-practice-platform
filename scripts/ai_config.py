"""Shared AI provider settings for the whole platform.

Canonical secrets file: <repo>/config/ai.env
All current and future AI features must use:
  AI_API_KEY, AI_BASE_URL, AI_MODEL

Optional tuning keys (also shared):
  AI_THINKING, AI_MAX_TOKENS, AI_MAX_TOKENS_RETRY, ...
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_ENV_PATH = ROOT / "config" / "ai.env"
AI_ENV_EXAMPLE_PATH = ROOT / "config" / "ai.env.example"

DEFAULT_AI_BASE_URL = "https://api.deepseek.com"
DEFAULT_AI_MODEL = "deepseek-v4-flash"


def load_env_file(path: Path | str, *, override: bool = False) -> bool:
    """Load KEY=VALUE lines into os.environ. Stdlib-only (no python-dotenv)."""
    env_path = Path(path)
    if not env_path.is_file():
        return False
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if not key:
            continue
        if override or key not in os.environ:
            os.environ[key] = value
    return True


def load_ai_env(*, override: bool = False) -> Path | None:
    """Load the platform-wide AI env file. Returns path if loaded."""
    if load_env_file(AI_ENV_PATH, override=override):
        return AI_ENV_PATH
    return None


def ai_settings() -> dict[str, str]:
    """Resolved AI settings after env files / process env are applied."""
    api_key = (
        os.environ.get("AI_API_KEY", "").strip()
        or os.environ.get("SILICONFLOW_API_KEY", "").strip()
    )
    base_url = (
        os.environ.get("AI_BASE_URL", "").strip()
        or os.environ.get("SILICONFLOW_BASE_URL", "").strip()
        or DEFAULT_AI_BASE_URL
    )
    model = (
        os.environ.get("AI_MODEL", "").strip()
        or os.environ.get("SILICONFLOW_MODEL", "").strip()
        or DEFAULT_AI_MODEL
    )
    return {
        "api_key": api_key,
        "base_url": base_url.rstrip("/"),
        "model": model,
    }
