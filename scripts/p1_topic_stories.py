# -*- coding: utf-8 -*-
"""Optional structured overlays per topic."""
from __future__ import annotations
from typing import Any
TOPIC_STORIES: dict[str, dict[str, Any]] = {}
def get_story(topic_en: str):
    return TOPIC_STORIES.get((topic_en or "").strip().lower())
