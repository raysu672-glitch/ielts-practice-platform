# -*- coding: utf-8 -*-
"""Topic pools resolved from core kits (thin wrapper)."""
from __future__ import annotations

from typing import Any

from p1_core_kits import get_kit, kit_to_pool, primary_kit_id


def get_pool(topic_en: str, kit_id: str | None = None) -> dict[str, Any] | None:
    kid = (kit_id or "").strip() or primary_kit_id(topic_en)
    kit = get_kit(kid)
    if not kit:
        kit = get_kit(primary_kit_id(topic_en))
    if not kit:
        return None
    return kit_to_pool(kit, topic_en)
