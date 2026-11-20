"""AI 答案复核 JSON 解析（无第三方依赖，可供 CI 单测）。"""

from __future__ import annotations

import json
import re
from typing import Optional


def parse_verify_answer_content(content: str) -> Optional[dict]:
    """解析 AI 复核 JSON，返回 {correct: bool, reason: str} 或 None。"""
    raw = (content or "").strip()
    if not raw:
        return None
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[^{}]*\}", raw, flags=re.S)
        if not m:
            return None
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(data, dict):
        return None
    correct = data.get("correct")
    if isinstance(correct, str):
        correct = correct.strip().lower() in ("1", "true", "yes", "y", "correct", "ok")
    elif not isinstance(correct, bool):
        correct = bool(correct)
    reason = str(data.get("reason") or "").strip()
    if len(reason) > 80:
        reason = reason[:80]
    return {"correct": bool(correct), "reason": reason}
