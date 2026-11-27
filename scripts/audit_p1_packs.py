# -*- coding: utf-8 -*-
"""Verify every P1 (question, kit) has a Freestyle pack and samples stay on-question."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_freestyle_packs import PACKS, get_pack  # noqa: E402
from p1_material_bank import material_ids_for_question  # noqa: E402

P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"


def load_p1() -> dict:
    text = P1.read_text(encoding="utf-8")
    brace = text.find("{", text.find("const P1_DATA"))
    depth = 0
    for i, ch in enumerate(text[brace:], brace):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[brace : i + 1])
    raise SystemExit("P1_DATA not found")


def main() -> int:
    data = load_p1()
    missing = []
    weak = []
    same = []
    checked = 0
    for cat in data["categories"]:
        steps = cat.get("steps") or []
        for q in cat["questions"]:
            qt = q["q"]
            topic = q.get("topicEn") or ""
            kids = material_ids_for_question(topic, qt) or q.get("kitIds") or []
            samples = []
            for kid in kids:
                checked += 1
                pack = get_pack(qt, kid)
                if not pack:
                    missing.append((topic, qt, kid))
                    continue
                sample = pack.get("sample") or ""
                samples.append(sample)
                if len(sample.split()) < 28:
                    weak.append((qt, kid, "short", sample[:120]))
                # light Q keyword
                stop = {
                    "what", "when", "where", "which", "your", "does", "have", "been",
                    "would", "could", "about", "most", "often", "usually", "people",
                    "think", "with", "from", "that", "this", "kind", "type", "like",
                }
                toks = [w for w in re.findall(r"[a-z]{4,}", qt.lower()) if w not in stop][:6]
                sl = sample.lower()
                if toks and not any(t in sl or t.rstrip("s") in sl for t in toks):
                    weak.append((qt, kid, "weak-Q", sample[:120]))
                # words keys should match steps loosely
                words = pack.get("words") or {}
                if steps and not any(s in words for s in steps):
                    weak.append((qt, kid, "words-steps", list(words.keys())))
            uniq = {s for s in samples if s}
            if len(kids) >= 2 and len(uniq) < 2 and samples:
                same.append((qt, kids))
    print(f"packs={len(PACKS)} checked_slots={checked} missing={len(missing)} weak={len(weak)} same={len(same)}")
    for row in missing[:40]:
        print(f"- MISSING {row[0]} | {row[1]} | {row[2]}")
    if len(missing) > 40:
        print(f"... +{len(missing) - 40} more missing")
    for row in weak[:20]:
        print(f"- WEAK {row}")
    for row in same[:10]:
        print(f"- SAME {row[0]} kits={row[1]}")
    return 1 if missing or same else 0


if __name__ == "__main__":
    raise SystemExit(main())
