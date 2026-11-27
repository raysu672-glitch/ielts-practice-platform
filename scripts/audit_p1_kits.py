# -*- coding: utf-8 -*-
"""Audit P1 material-bank binding and multi-material variants."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p1_material_bank import MATERIALS, material_ids_for_question  # noqa: E402

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
    errs: list[str] = []
    if len(MATERIALS) < 12:
        errs.append(f"expected >=12 materials, got {len(MATERIALS)}")

    data = load_p1()
    fail = data.get("meta", {}).get("sampleLogicFail")
    if fail:
        errs.append(f"sampleLogicFail={fail}")

    by_topic: dict[str, list[dict]] = defaultdict(list)
    for cat in data["categories"]:
        for q in cat["questions"]:
            by_topic[q.get("topicEn") or ""].append(q)

    mat_hits: Counter[str] = Counter()
    for topic, qs in by_topic.items():
        seen: list[str] = []
        for q in qs:
            if q["q"] not in seen:
                seen.append(q["q"])
        uniq = [next(q for q in qs if q["q"] == qq) for qq in seen]
        sample_q = uniq[0]["q"] if uniq else ""
        ids = material_ids_for_question(topic, sample_q)
        if len(ids) < 2:
            errs.append(f"{topic}: need >=2 materials, got {ids}")
        for mid in ids:
            mat_hits[mid] += 1
            if mid not in MATERIALS:
                errs.append(f"{topic}: unknown material {mid}")
        if len(uniq) >= 2:
            # Only flag when both supporting chips and full sample are frozen identical
            e0 = tuple((uniq[0].get("kitSlice") or [])[:3])
            e1 = tuple((uniq[1].get("kitSlice") or [])[:3])
            s0 = uniq[0].get("sample") or ""
            s1 = uniq[1].get("sample") or ""
            if e0 and e1 and e0 == e1 and s0 == s1:
                errs.append(f"{topic}: Q1/Q2 sample+slice identical")
        for q in uniq:
            if not q.get("kitIds") or len(q.get("kitIds") or []) < 2:
                errs.append(f"{topic} / {q['q'][:40]}: kitIds < 2")
            if not q.get("kitVariants"):
                errs.append(f"{topic} / {q['q'][:40]}: missing kitVariants")
            variants = q.get("kitVariants") or {}
            samples = {vid: (variants[vid] or {}).get("sample") for vid in (q.get("kitIds") or [])}
            vals = [s for s in samples.values() if s]
            if len(set(vals)) < 2 and len(vals) >= 2:
                # Also accept distinct supporting chips when openings must stay question-fixed
                slices = {
                    vid: tuple(((variants[vid] or {}).get("kitSlice") or [])[:3])
                    for vid in (q.get("kitIds") or [])
                }
                if len(set(slices.values())) < 2:
                    errs.append(f"{topic} / {q['q'][:40]}: material variants not distinct")

    print(f"materials={len(MATERIALS)} topics={len(by_topic)} hits={dict(mat_hits)}")
    if errs:
        for e in errs[:40]:
            print("ERR", e)
        print(f"{len(errs)} error(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
