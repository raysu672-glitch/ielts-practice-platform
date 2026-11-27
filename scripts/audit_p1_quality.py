# -*- coding: utf-8 -*-
"""Audit P1 steps / materials / frames / samples for all questions."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_align_engine import _chip_in  # noqa: E402
from p1_word_banks_core import CAT_STEPS  # noqa: E402

P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
OUT = ROOT / "_p1_quality_audit.txt"


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


def awkward_english(sample: str) -> list[str]:
    s = sample or ""
    sl = s.lower()
    issues = []
    patterns = [
        (r"\bi often use (feel |watch |listen |recycle |sort |keep |attend )", "verb chip jammed after 'use'"),
        (r"\bi often use [a-z]+ and [a-z]+,", "keyword dump after 'use'"),
        (r"\bincluding helps me ", "including + verb patch"),
        (r"\bthis feels routine busy\b", "broken rewrite: feels routine busy"),
        (r"\bso that is tough\b", "awkward 'so that is'"),
        (r"\band this is useful for my future career\b", "weak tacked-on career clause"),
        (r"\byes, quite often\.\s+i mainly", "yes/frequency opening on what/which"),
        (r"\bi usually focus on search information\b", "keyword opening"),
        (r"\bmainly because of kill ", "bare verb after because of"),
        (r"\bit is common for me that when i\b", "awkward variant rewrite"),
    ]
    for pat, note in patterns:
        if re.search(pat, sl):
            issues.append(note)
    # double spaces / repeated words
    if re.search(r"\b(\w+) \1\b", sl):
        issues.append("repeated word")
    if len(s.split()) < 28:
        issues.append("short sample")
    if s.count(".") < 2:
        issues.append("fewer than 3 sentences")
    return issues


def frame_issues(q: str, frames: dict) -> list[str]:
    ql = q.lower()
    issues = []
    f3 = ((frames or {}).get("3") or {}).get("pattern", "").lower()
    f2 = ((frames or {}).get("1") or {}).get("pattern", "").lower()
    if "prefer" in f3 and "prefer" not in ql and "rather" not in ql and " or " in ql:
        # may still be intentional for comfort or style etc.
        if not any(x in ql for x in ("comfort or", "style", "websites or", "books", "noisy or", "quiet", "driver or", "passenger", "mall or")):
            issues.append("prefer frame on non-contrast or-question")
    if "whenever" in f2 and any(x in ql for x in ("when you were a child", "as a child", "childhood")):
        issues.append("whenever frame on childhood question")
    alts = ((frames or {}).get("1") or {}).get("alts") or []
    if len(alts) < 2:
        issues.append("step2 missing 2 alt patterns")
    return issues


def step_fit(cat_id: str, q: str) -> list[str]:
    ql = q.lower()
    issues = []
    if cat_id == "shishi" and any(x in ql for x in ("do you like", "favourite", "favorite", "enjoy")):
        issues.append("like/favourite maybe better as xihao")
    if cat_id == "xihao" and ql.startswith("how often"):
        issues.append("how often maybe better as xingwei")
    if cat_id == "shishi" and "why do you think" in ql:
        issues.append("why do you think maybe better as guandian")
    return issues


def main() -> None:
    data = load_p1()
    lines: list[str] = []
    chip_fail = []
    awkward = []
    frame_bad = []
    step_bad = []
    empty_words = []
    no_material = []
    topic_mats: dict[str, set[str]] = defaultdict(set)
    variant_pat = Counter()
    total = 0

    for cat in data["categories"]:
        steps = cat["steps"]
        expected = CAT_STEPS.get(cat["id"], steps)
        for q in cat["questions"]:
            total += 1
            topic = q.get("topicEn") or "?"
            topic_mats[topic].add(q.get("material") or "")
            if not (q.get("material") or "").strip():
                no_material.append(q["q"])
            words = q.get("words") or {}
            for s in expected:
                if s not in words or not words[s]:
                    empty_words.append((topic, q["q"], s))
            sample = q.get("sample") or ""
            tl = sample.lower()
            for s in steps:
                chips = words.get(s) or []
                if chips and not any(_chip_in(c, tl) for c in chips[:4]):
                    chip_fail.append((topic, q["q"], s, chips[:2]))
            for note in awkward_english(sample):
                awkward.append((topic, q["q"], note, sample[:120]))
            for note in frame_issues(q["q"], q.get("frames") or {}):
                frame_bad.append((topic, q["q"], note))
            for note in step_fit(cat["id"], q["q"]):
                step_bad.append((topic, cat["id"], q["q"], note))
            fr1 = ((q.get("frames") or {}).get("1") or {}).get("pattern", "")
            variant_pat[fr1] += 1

    multi = {t: ms for t, ms in topic_mats.items() if len(ms) > 1}

    lines.append(f"total={total} topics={len(topic_mats)}")
    lines.append(f"chip_fail={len(chip_fail)}")
    lines.append(f"awkward={len(awkward)}")
    lines.append(f"frame_issues={len(frame_bad)}")
    lines.append(f"step_fit_flags={len(step_bad)}")
    lines.append(f"empty_word_steps={len(empty_words)}")
    lines.append(f"no_material={len(no_material)}")
    lines.append(f"topics_multi_material={len(multi)}")
    lines.append("")

    def dump(title: str, rows: list, limit: int = 40) -> None:
        lines.append(f"## {title} ({len(rows)})")
        for row in rows[:limit]:
            lines.append(" | ".join(str(x) for x in row))
        if len(rows) > limit:
            lines.append(f"... +{len(rows) - limit} more")
        lines.append("")

    dump("chip_fail", chip_fail)
    dump("awkward", awkward, 60)
    dump("frame_issues", frame_bad)
    dump("step_fit", step_bad)
    dump("empty_words", empty_words)
    dump("multi_material", [(t, sorted(ms)) for t, ms in multi.items()])

    # per-topic summary: first q sample + frame names
    lines.append("## per_topic_snapshot")
    for topic in sorted(topic_mats):
        qs = []
        for cat in data["categories"]:
            for q in cat["questions"]:
                if q.get("topicEn") == topic:
                    qs.append((cat["id"], q))
        # unique by q
        seen = set()
        uniq = []
        for cat_id, q in qs:
            if q["q"] in seen:
                continue
            seen.add(q["q"])
            uniq.append((cat_id, q))
        lines.append(f"### {topic} ({len(uniq)}) mat={uniq[0][1].get('material','') if uniq else ''}")
        for cat_id, q in uniq:
            fr = q.get("frames") or {}
            names = [((fr.get(str(i)) or {}).get("name") or "?") for i in (1, 2, 3)]
            lines.append(f"- [{cat_id}] {q['q']}")
            lines.append(f"  frames: {' / '.join(names)}")
            lines.append(f"  sample: {q.get('sample','')[:160]}")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:80]))
    print(f"... wrote {OUT}")


if __name__ == "__main__":
    main()
