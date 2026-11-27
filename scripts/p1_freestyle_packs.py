# -*- coding: utf-8 -*-
"""
Per-(question, kit) Freestyle packs — same workflow as p1-freestyle-preview.html.

Each pack must include:
  logic   答题思路（只服务本题+本素材，一句说清怎么答）
  kitHint 素材切换说明（为何这套料能扣题）
  words   四步词卡（部分选用即可）
  sample  Band 6 口语示范（换素材必须换答法，禁止同文）
  sampleZh 中文对照

Hard rules:
  - 素材必须能直接服务题干；对不上就不要挂这套料
  - 示范先扣题，再带生活细节；不要词块硬拼
"""
from __future__ import annotations

from typing import Any

from p1_word_banks_core import norm_q

# (norm_q, kit_id) → pack
PACKS: dict[tuple[str, str], dict[str, Any]] = {}


def _p(q: str, kit: str, **fields: Any) -> None:
    need = ("logic", "kitHint", "words", "sample", "sampleZh")
    for k in need:
        if k not in fields or fields[k] in (None, "", {}):
            raise ValueError(f"pack missing {k} for ({q!r}, {kit})")
    PACKS[(norm_q(q), kit)] = fields


def get_pack(qtext: str, kit_id: str) -> dict[str, Any] | None:
    return PACKS.get((norm_q(qtext), (kit_id or "").strip()))


def build() -> None:
    PACKS.clear()
    from p1_packs import register_all

    register_all(_p)


build()
