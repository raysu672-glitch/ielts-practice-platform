# -*- coding: utf-8 -*-
"""Regenerate IPA for multi-word / hyphenated entries in listening_basic.html.

Uses eng-to-ipa so displayed phonetics match the English text (fixes rename leftovers
like banana boat still showing 'ride', and OCR-garbled phrase IPA).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import eng_to_ipa as ipa
except ImportError:
    print("ERROR: pip install eng-to-ipa", file=sys.stderr)
    sys.exit(1)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"

# Manual overrides when eng-to-ipa has no reliable entry
MANUAL = {
    "micro-radiogram": "/ˈmaɪkrəʊ ˈreɪdiəɡræm/",
}


def is_phrase(word: str) -> bool:
    return (" " in word) or ("-" in word)


def to_ipa(word: str) -> str | None:
    if word in MANUAL:
        return MANUAL[word]
    candidates = [word]
    if "-" in word:
        candidates.append(word.replace("-", " "))
    if "'" in word:
        candidates.append(word.replace("'", ""))
    for cand in candidates:
        raw = (ipa.convert(cand) or "").strip()
        if not raw or raw.endswith("*") or "*" in raw:
            continue
        return "/" + raw + "/"
    return None


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", text, re.S)
    if not m:
        raise SystemExit("ALL_WORDS not found")
    words = json.loads(m.group(1))

    updated = 0
    failed: list[str] = []
    unchanged = 0
    for row in words:
        w = str(row.get("word") or "")
        if not is_phrase(w):
            continue
        new_ph = to_ipa(w)
        if not new_ph:
            failed.append(w)
            continue
        old = row.get("phonetic") or ""
        if old == new_ph:
            unchanged += 1
            continue
        row["phonetic"] = new_ph
        updated += 1

    dump = json.dumps(words, ensure_ascii=False, separators=(",", ":"))
    new_text = text[: m.start(1)] + dump + text[m.end(1) :]
    HTML.write_text(new_text, encoding="utf-8")

    print(f"updated={updated} unchanged={unchanged} failed={len(failed)}")
    if failed:
        print("failed:")
        for w in failed:
            print(" ", w)

    by = {r["word"]: r["phonetic"] for r in words}
    for w in [
        "banana boat",
        "alarm system",
        "pet food",
        "animal behaviour",
        "bottled water",
        "free pick-up",
        "children's minds",
        "advanced level",
        "academic record",
        "time-consuming",
        "micro-radiogram",
    ]:
        print(f"  {w}: {by.get(w)}")


if __name__ == "__main__":
    main()
