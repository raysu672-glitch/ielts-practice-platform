# -*- coding: utf-8 -*-
"""
Rebuild sources/kouyulianxi/p2-data.js questions from 2026-05~08 heat list (56).
Keeps the existing materials block unchanged; replaces only `questions` + header comment.

Question definitions (opening/hint/sample/material) live in p2_heat_questions.QUESTIONS.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p2_heat_questions import QUESTIONS  # noqa: E402

P2_PATH = ROOT / "sources" / "kouyulianxi" / "p2-data.js"
SUMMARY = ROOT / "_p2_rebuild_summary.txt"
META = "// P2 data - 6 大素材 + 56 道答题思路（2026年5-8月现行题库，含参考答案）\n"


def extract_materials_js(text: str) -> str:
    """Return the raw `materials: [...]` source (unchanged)."""
    m = re.search(r"\bmaterials\s*:\s*\[", text)
    if not m:
        raise SystemExit("materials array not found")
    start = m.start()
    i = m.end() - 1  # at '['
    depth = 0
    for j in range(i, len(text)):
        ch = text[j]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                # include trailing comma if present
                end = j + 1
                if end < len(text) and text[end] == ",":
                    end += 1
                return text[start:end]
    raise SystemExit("unclosed materials array")


def count_materials(materials_js: str) -> tuple[int, list[str]]:
    """Top-level material ids only (skip nested variant ids)."""
    known = {"yumeng", "sun", "movie", "badminton", "bear", "basketball", "tianchi", "robot"}
    ids = [i for i in re.findall(r'\bid\s*:\s*"([^"]+)"', materials_js) if i in known]
    # preserve order, unique
    seen: list[str] = []
    for i in ids:
        if i not in seen:
            seen.append(i)
    return len(seen), seen


def word_count(s: str) -> int:
    return len((s or "").split())


def validate(questions: list[dict]) -> list[str]:
    errs: list[str] = []
    if len(questions) != 56:
        errs.append(f"expected 56 questions, got {len(questions)}")
    for q in questions:
        qid = q.get("id")
        for key in ("openingEn", "materialHint", "endingTip", "sampleEn", "cuePoints", "tag", "heatLevel"):
            if not q.get(key):
                errs.append(f"q{qid} missing {key}")
        if not (q.get("materialId") or q.get("materialIds")):
            errs.append(f"q{qid} missing materialId/materialIds")
        if word_count(q.get("sampleEn", "")) < 120:
            errs.append(f"q{qid} sampleEn words={word_count(q.get('sampleEn', ''))}")
        by_id = q.get("sampleEnById") or {}
        for mid, sample in by_id.items():
            if word_count(sample) < 120:
                errs.append(f"q{qid} sampleEnById[{mid}] words={word_count(sample)}")
    return errs


def material_key(q: dict) -> str:
    if q.get("materialIds"):
        return "+".join(q["materialIds"])
    return q.get("materialId") or "?"


def build_output(materials_js: str, questions: list[dict]) -> str:
    q_json = json.dumps(questions, ensure_ascii=False, indent=2)
    # indent questions block to match file style (2 spaces under root)
    q_indented = "\n".join(
        ("  " + line if line else line) for line in q_json.splitlines()
    )
    return (
        META
        + "const P2_DATA = {\n"
        + "  "
        + materials_js.strip()
        + "\n"
        + "  questions: "
        + q_indented.lstrip()
        + "\n};\n"
    )


def main() -> None:
    text = P2_PATH.read_text(encoding="utf-8")
    materials_js = extract_materials_js(text)
    mat_n, mat_ids = count_materials(materials_js)
    if mat_n < 6:
        raise SystemExit(f"materials too few: {mat_n}")

    questions = []
    for q in QUESTIONS:
        item = dict(q)
        if item.get("materialIds") and not item.get("materialOptions"):
            item["materialOptions"] = list(item["materialIds"])
        questions.append(item)

    errs = validate(questions)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs[:40]:
            print(" ", e)
        raise SystemExit(1)

    out = build_output(materials_js, questions)
    P2_PATH.write_text(out, encoding="utf-8")

    # sanity: materials still parse as balanced, questions loadable
    raw = out[out.find("{") : out.rfind("}") + 1]
    # questions only via regex extract
    qm = re.search(r"\bquestions\s*:\s*(\[[\s\S]*\])\s*\}\s*;?\s*$", out)
    if not qm:
        raise SystemExit("failed to locate questions in output")
    loaded = json.loads(qm.group(1))
    if len(loaded) != 56:
        raise SystemExit(f"output questions count {len(loaded)}")

    hist = Counter(material_key(q) for q in questions)
    lines = [
        "P2 rebuild summary",
        f"questions: {len(questions)}",
        f"materials kept: {mat_n} ids={mat_ids}",
        "material usage:",
    ]
    for mid, n in sorted(hist.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"  {mid}: {n}")
    short_ok = all(word_count(q["sampleEn"]) >= 120 for q in questions)
    lines.append(f"sampleEn all >=120: {short_ok}")
    lines.append(
        "examples: "
        + ", ".join(
            f"#{q['id']} {q['title']}->{q.get('materialId')}"
            for q in questions
            if q["id"] in (1, 23, 50)
        )
    )
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {P2_PATH}")
    print(f"wrote {SUMMARY}")


if __name__ == "__main__":
    main()
