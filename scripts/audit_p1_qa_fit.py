# -*- coding: utf-8 -*-
"""Audit P1 samples for question–answer misfit (reason/story mismatch etc.)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_align_engine import (  # noqa: E402
    _looks_like_story,
    align_question_all_kits,
    detect_intent,
)

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


def _reason_clause(sample: str) -> str:
    # Stop before ", I keep this habit" so feel-reasons are not treated as stories
    m = re.search(
        r"for the reason that\s+(.+?)(?:,\s*i keep this habit|\.\s|\.$)",
        sample,
        re.I | re.S,
    )
    return (m.group(1).strip() if m else "")


def issues_for(qtext: str, sample: str, intent: str) -> list[str]:
    s = (sample or "").strip()
    sl = s.lower()
    out: list[str] = []
    if not s:
        return ["empty sample"]

    reason = _reason_clause(s)
    # Feel/impact phrases are valid xingwei reasons; only flag true narratives
    if (
        reason
        and _looks_like_story(reason)
        and not reason.lower().startswith(("it ", "this ", "i can ", "i ", "they ", "people "))
        and any(
            m in reason.lower()
            for m in ("when i ", "after i ", "my parents", "bought me", "classmate", "booked", "yellow bike")
        )
    ):
        out.append("story used as 'for the reason that'")

    m = re.search(r"what makes it hard is\s+(.+?)(?:,|\.|$)", s, re.I)
    if m and _looks_like_story(m.group(1)):
        out.append("story used as 'what makes it hard'")

    m = re.search(r"i plan to use\s+(.+?)\s+and keep building", s, re.I)
    if m and _looks_like_story(m.group(1)):
        out.append("story used as future plan object")

    m = re.search(r"for example,\s*i focus on\s+(.+?)(?:\.|$)", s, re.I)
    if m and _looks_like_story(m.group(1)):
        out.append("story used as study focus")

    if intent == "why_choose":
        need = ("match", "strength", "career", "job", "course", "business", "future", "fit", "lead")
        if not any(k in sl for k in need):
            out.append("why_choose missing career/fit language")
        bad = ("booked library", "habit stuck", "classmate booked", "yellow bike as", "comfortable pair before")
        if any(b in sl for b in bad):
            out.append("why_choose polluted by unrelated material story")

    if intent == "challenging":
        if not any(k in sl for k in ("deadline", "exam", "assignment", "balance", "stress", "hard")):
            out.append("challenging answer missing study-hardship language")

    if intent == "future_plan":
        if not any(k in sl for k in ("degree", "internship", "career", "course", "graduate", "business", "job")):
            out.append("future_plan missing career language")
        # Must not be used for non-career future Qs
        if not any(k in qtext.lower() for k in ("career", "studies", "job", "work")):
            out.append("future_plan intent on non-career question")

    if intent == "do_when":
        first = s.split(".")[0].strip().lower()
        if first in ("campus dorms", "comfortable sneakers", "a sweatshirt", "a coat", "recycling bins"):
            out.append("do_when opens with object/place instead of action")
        if "rubbish" in qtext.lower() and not any(k in sl for k in ("pick", "bin", "recycl", "sort", "rubbish")):
            out.append("rubbish Q missing bin/pick language")

    if "finish my degree" in sl and not any(k in qtext.lower() for k in ("career", "studies", "job", "work", "degree")):
        out.append("'Finish my degree' on non-career question")

    if "keep the answer concrete" in sl or "这个细节也能让回答更具体" in s:
        out.append("meta pad leaked into sample")

    ql = qtext.lower()
    fs = s.split(".")[0].strip().lower()
    if ql.startswith(("what kind", "what type", "which ")) and fs.startswith(("i love", "yes,", "not really")):
        out.append("kind/which bad opening")
    if "forget" in ql and "name" in ql and re.search(r"for example,\s*my given name shows up", sl):
        out.append("forget-names talks about own name")
    if "as a child, the subway was already familiar" in sl:
        out.append("subway hard-fit on childhood Q")
    if "which fits what i actually use or do" in sl and not any(
        x in ql for x in ("what kind", "what type", "which ", "wear", "use")
    ):
        out.append("generic use-or-do template on wrong Q")

    # Identity Q: must answer work vs student; material may tint lightly only
    if "do you work or are you a student" in ql:
        if not any(
            k in fs
            for k in (
                "i am a student",
                "i'm a student",
                "i am a full-time student",
                "i'm a full-time student",
                "i study",
                "i work",
                "i'm working",
                "i am working",
            )
        ):
            out.append("work/student Q missing identity opening")
        tidy_hits = sum(sl.count(w) for w in ("tidy", "desk", "organised", "organized", "neat"))
        if tidy_hits >= 3:
            out.append("work/student Q hijacked by tidy-desk story")

    # Work or studies topic answers must not be hijacked by tidy-desk stories
    if any(
        k in ql
        for k in (
            "work or are you a student",
            "choose that job or that subject",
            "challenging about your work or your studies",
            "like most about your job or your studies",
            "typical day like for you at work or at school",
            "career or studies in a few years",
        )
    ):
        tidy_hits = sum(sl.count(w) for w in ("tidy my desk", "tidy desk", "cleared desk", "clear desk", "neat study habits at my desk"))
        if tidy_hits >= 1 and sum(sl.count(w) for w in ("tidy", "desk")) >= 2:
            # allow one light "desk" mention only if not framed as tidying story
            if "tidy" in sl or "cleared desk" in sl or "neat study habits at my desk" in sl:
                out.append("work/studies Q polluted by tidy-desk story")

    return out


def main() -> int:
    data = load_p1()
    topic_order: dict[str, list[str]] = {}
    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            topic_order.setdefault(t, [])
            if q["q"] not in topic_order[t]:
                topic_order[t].append(q["q"])

    rows: list[tuple[str, str, str, str, list[str]]] = []
    checked = 0
    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            idx = topic_order.get(t, [q["q"]]).index(q["q"]) if q["q"] in topic_order.get(t, []) else 0
            intent = detect_intent(q["q"])
            aligned = align_question_all_kits(cat["id"], q["q"], t, topic_q_index=idx)
            variants = aligned.get("kitVariants") or {aligned.get("kitId") or "main": aligned}
            for kid, v in variants.items():
                sample = v.get("sample") or ""
                checked += 1
                probs = issues_for(q["q"], sample, intent)
                if probs:
                    rows.append((cat["id"], q["q"], kid, sample[:180], probs))

    print(f"checked={checked} misfits={len(rows)}")
    for cat_id, qtext, kid, sample, probs in rows[:60]:
        print(f"- [{cat_id}/{detect_intent(qtext)}] {qtext}")
        print(f"  kit={kid} :: {'; '.join(probs)}")
        print(f"  sample={sample}")
    if len(rows) > 60:
        print(f"... and {len(rows) - 60} more")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
