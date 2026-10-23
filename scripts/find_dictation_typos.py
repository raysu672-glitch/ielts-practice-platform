# -*- coding: utf-8 -*-
"""Find likely spelling typos in listening word banks (modules.js)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "sources" / "tinglidanciceshi" / "js" / "modules.js"

# Common OCR/keyboard typos seen in this corpus (word -> correction)
KNOWN_FIXES = {
    "bottie water": "bottle water",
    "butterfiies": "butterflies",
    "cabie": "cable",
    "ciothing sections": "clothing sections",
    "compiaints": "complaints",
    "compiete": "complete",
    "compiex": "complex",
    "compuisory": "compulsory",
    "computerprogrammer": "computer programmer",
    "contact detaiis": "contact details",
    "desk iamp": "desk lamp",
    "eniargement": "enlargement",
    "entertainmentindustry": "entertainment industry",
    "famiiy": "family",
    "fiashiight": "flashlight",
    "fiavor": "flavor",
    "fiute": "flute",
    "french styie": "french style",
    "gioves": "gloves",
    "graduai": "graduate",
    "iand": "land",
    "ianes": "lanes",
    "iaptops": "laptops",
    "iaw department": "law department",
    "iegroom": "legroom",
    "ieisure": "leisure",
    "iength": "length",
    "infiuence": "influence",
    "informai": "informal",
    "ioans": "loans",
    "iookout point": "lookout point",
    "iost": "lost",
    "iungs": "lungs",
    "knowiedge sharing": "knowledge sharing",
    "marine piants": "marine plants",
    "modei": "model",
    "moraiity": "morality",
    "paining": "painting",
    "painting ciass": "painting class",
    "personai alarm": "personal alarm",
    "personalinformation": "personal information",
    "popuiar": "popular",
    "practicai course": "practical course",
    "reaiism": "realism",
    "reguiar": "regular",
    "reieased": "released",
    "ring abell": "ring a bell",
    "seif-iocking": "self-locking",
    "shaiiow": "shallow",
    "steei": "steel",
    "symboi": "symbol",
    "tempie waiis": "temple walls",
    "tities": "titles",
    "transiation": "translation",
    "window iocks": "window locks",
    "businessmanagement": "business management",
    "flourishment": "flourishment/flourishing?",  # flag only
}

# Suspicious char patterns (i/l/1 confusion, missing letters)
SUSPICIOUS_RE = re.compile(
    r"(^i[a-z]{3,}|iamp|iand\b|ianes|iaptop|iaw |iegroom|ieisure|iength|infiuence|"
    r"informai|ioans|iookout|iost\b|iungs|knowiedge|piants|modei|moraiity|"
    r"ciass|ciothing|compi|compui|detaiis|famiiy|fiash|fiavor|fiute|styie|gioves|"
    r"graduai|personai|popuiar|practicai|reaiism|reguiar|reieased|abell|seif-|"
    r"shaiiow|steei|symboi|tempie|tities|transiation|iocks|bottie|butterfi|"
    r"eniarg|cabie\b|programmer\b|personalinformation|entertainmentindustry|"
    r"businessmanagement|paining\b|flourishment|fiute|desk iamp)",
    re.I,
)


def extract_array(name: str, text: str) -> list[str]:
    m = re.search(rf"var {name}\s*=\s*\[", text)
    if not m:
        raise SystemExit(f"missing {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise SystemExit(f"unclosed {name}")


def try_spellcheck(tokens: list[str]) -> list[tuple[str, str]]:
    try:
        from spellchecker import SpellChecker
    except ImportError:
        return []
    spell = SpellChecker(language="en")
    out = []
    for w in tokens:
        if " " in w or not w.isascii():
            continue
        if not re.match(r"^[a-zA-Z\-']+$", w):
            continue
        low = w.lower()
        if low in spell:
            continue
        # ignore proper nouns / month names heuristically
        if low in {
            "rafel", "patterson", "mexico", "china", "europe", "africa",
            "argentina", "france", "germany", "india", "russia", "scotland",
            "spanish", "japanese", "french", "italian", "wednesday", "sunday",
        }:
            continue
        sug = spell.correction(low)
        if sug and sug != low:
            out.append((w, sug))
    return out


def main() -> None:
    text = MODULES.read_text(encoding="utf-8")
    dictation = extract_array("allWords", text)
    basic = extract_array("allWordsListeningBasic", text)

    print(f"dictation count: {len(dictation)}")
    print(f"listening_basic count: {len(basic)}")
    print()

    def report(label: str, words: list[str]) -> None:
        print(f"=== {label} ===")
        known = [(w, KNOWN_FIXES[w]) for w in words if w in KNOWN_FIXES]
        suspicious = [w for w in words if SUSPICIOUS_RE.search(w)]
        # merge known into suspicious display
        seen = set()
        rows = []
        for w, fix in known:
            rows.append((w, fix, "known"))
            seen.add(w)
        for w in suspicious:
            if w not in seen:
                fix = KNOWN_FIXES.get(w, "?")
                rows.append((w, fix, "pattern"))
                seen.add(w)
        rows.sort(key=lambda x: x[0].lower())
        print(f"likely typos: {len(rows)}")
        for w, fix, kind in rows:
            print(f"  [{kind}] {w!r} -> {fix!r}")
        print()

    report("听力1000词 (dictation)", dictation)
    report("听力基础词汇 (listening_basic)", basic)

    # spellcheck single-token words in basic only (large)
    sc = try_spellcheck([w for w in basic if " " not in w])
    if sc:
        print("=== spellcheck extras (listening_basic single words) ===")
        for w, sug in sorted(set(sc))[:40]:
            if w.lower() not in KNOWN_FIXES and not SUSPICIOUS_RE.search(w):
                print(f"  {w!r} -> {sug!r}")
        print(f"(showing up to 40 of {len(sc)})")


if __name__ == "__main__":
    main()
