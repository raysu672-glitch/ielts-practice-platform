# -*- coding: utf-8 -*-
"""Build per-question P1 word banks + logic for all 231 heat-list questions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from p1_word_banks_core import (
    CAT_STEPS,
    CLUE_ALIAS,
    apply_fixes,
    enrich_step_words,
    kit_for,
    norm_q,
    pack,
    tweak_combined,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).resolve().parent / "p1_question_data.json"
CLUE_PATH = ROOT / "_p1_clue_index.json"

_DATA: dict[str, Any] | None = None
_CLUE: dict[str, dict] | None = None


def load_question_data() -> dict[str, dict]:
    global _DATA
    if _DATA is None:
        if not DATA_PATH.is_file():
            raise FileNotFoundError(f"Missing {DATA_PATH}; run scripts/_build_p1_question_data.py")
        raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        _DATA = raw["questions"]
    return _DATA


def load_clue_index() -> dict[str, dict]:
    global _CLUE
    if _CLUE is None:
        _CLUE = json.loads(CLUE_PATH.read_text(encoding="utf-8"))["index"]
    return _CLUE


def resolve_words(
    cat_id: str,
    qtext: str,
    steps: list[str],
    topic_en: str | None = None,
) -> tuple[dict[str, list[str]], str, str]:
    """Return (words per step, logic sentence, source tag)."""
    key = norm_q(qtext)
    data = load_question_data().get(key)
    if data and data.get("words"):
        words = {s: apply_fixes(list(data["words"].get(s, [])))[:5] for s in steps}
        logic = data.get("logic", "")
        source = data.get("source", "explicit")
        return words, logic, source

    # live fallback (should not happen after data build)
    clue = load_clue_index()
    source = "derived"
    logic = ""
    words: dict[str, list[str]] = {}

    if key in clue:
        words = {s: list(clue[key]["words"].get(s, [])) for s in steps}
        words = tweak_combined(cat_id, qtext, words, steps)
        source = "clue"
    else:
        alias = CLUE_ALIAS.get(key)
        if alias and alias in clue:
            words = {s: list(clue[alias]["words"].get(s, [])) for s in steps}
            words = tweak_combined(cat_id, qtext, words, steps)
            source = "clue-alias"

    if not words:
        kit = kit_for(topic_en or "")
        chips = kit["chips"]
        words = pack(cat_id, ["Yes", "Definitely"], chips[:4], ["from time to time", "at weekends"], ["practical", "really convenient"])
        source = "derived"

    kit = kit_for(topic_en or "")
    logic = kit.get("logic", "先直接回答，再举具体例子，补频次，最后感受收束。")

    for s in steps:
        words[s] = enrich_step_words(words.get(s, []), cat_id, topic_en or "", s, steps)

    return words, logic, source


def validate_all() -> tuple[list[str], dict[str, int]]:
    """Validate all 231 heat questions; return failures and source stats."""
    heat = json.loads((ROOT / "_p1_heat_parsed.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    stats: dict[str, int] = {}
    total = 0

    for cat in heat:
        steps = cat["steps"]
        for topic in cat["topics"]:
            for qtext in topic["questions"]:
                total += 1
                words, logic, source = resolve_words(cat["id"], qtext, steps, topic["topicEn"])
                stats[source] = stats.get(source, 0) + 1
                issues: list[str] = []
                if not logic:
                    issues.append("empty logic")
                for s in steps:
                    w = words.get(s, [])
                    if len(w) < 3:
                        issues.append(f"{s}: only {len(w)} chips")
                if issues:
                    failures.append(f"{topic['topicEn']} | {qtext} | {source} | {', '.join(issues)}")

    stats["total"] = total
    return failures, stats


if __name__ == "__main__":
    failures, stats = validate_all()
    out = ROOT / "_p1_words_validation.txt"
    lines = [f"total={stats.get('total', 0)}", f"stats={stats}", f"failures={len(failures)}", ""]
    lines.extend(failures)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:20]))
    print(f"... wrote {out}")
