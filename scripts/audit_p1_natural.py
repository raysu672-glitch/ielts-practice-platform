# -*- coding: utf-8 -*-
"""Naturalness + light Q-fit audit for P1 samples (all kit variants)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"

BAD = [
    (r"\bfor questions about\b", "meta for-questions-about"),
    (r"\bkeeping this .{0,50} in mind helps me answer\b", "meta keeping-in-mind"),
    (r"\bwhich became a clear memory about\b", "memory-about filler"),
    (r"\bthis comes up\b", "this-comes-up filler"),
    (r"\bwhen \w+ comes up\b", "when-comes-up filler"),
    (r"\bit still connects to\b", "connects-to filler"),
    (r"\bthis also relates to\b", "relates-to filler"),
    (r"\bis the detail i usually mention\b", "detail-mention dump"),
    (r"\bis what i would mention\b", "would-mention meta"),
    (r"\bfits the point about\b", "fits-point meta"),
    (r"\ba specific example\b", "specific-example"),
    (r"\bi usually keep this\b", "keep-this"),
    (r"\bmatters in my routine, i keep the habit\b", "habit-dump"),
    (r"\bstill feels makes\b", "broken-feel-pad"),
    (r"\bstill feels help", "broken-feel-pad"),
    (r"\bthis question about\b", "meta-question-about"),
    (r"\bone related detail in my week\b", "related-detail dump"),
    (r"\bwhich feels .+ \(.+\)", "paren-freq dump"),
]

YES_BAD_PREFIX = (
    "what kind", "what type", "which ", "who ", "how does", "how often", "how do you", "how did", "what "
)


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


def check_sample(qtext: str, sample: str) -> list[str]:
    issues: list[str] = []
    s = sample or ""
    sl = s.lower()
    ql = qtext.lower()
    if not s:
        return ["empty"]
    if len(s.split()) < 30:
        issues.append(f"short({len(s.split())})")
    for pat, name in BAD:
        if re.search(pat, sl):
            issues.append(name)
    if any(ql.startswith(p) for p in YES_BAD_PREFIX) and sl.startswith("yes,"):
        issues.append("bad-Yes-open")
    if ql.startswith("who ") and sl.startswith(("not really", "yes,", "i live in a")):
        issues.append("bad-Who-open")
    # light keyword: at least one content token from Q
    stop = {
        "what", "when", "where", "which", "your", "does", "have", "been", "would", "could",
        "about", "most", "often", "usually", "people", "think", "with", "from", "that", "this",
        "were", "like", "feel", "felt", "they", "them", "their", "there", "some", "many",
        "did", "you", "the", "and", "for", "are", "was", "how", "who", "why", "any", "had",
        "kind", "type", "area", "part", "thing", "things",
    }
    short_keep = {"car", "own", "bus", "ads", "lab", "nap", "job", "app", "map", "gym"}
    toks = []
    for w in re.findall(r"[a-z]{3,}", ql):
        if w in stop:
            continue
        if len(w) >= 4 or w in short_keep:
            toks.append(w)

    synonyms = {
        "headphones": ("earbud", "earbuds", "headset"),
        "headphone": ("earbud", "earbuds", "headset"),
        "studies": ("study", "studying", "class", "campus", "course"),
        "study": ("studies", "studying", "class", "course"),
        "job": ("work", "career", "internship"),
    }

    def hit(tok: str) -> bool:
        if tok in sl:
            return True
        alts = {tok + "s", tok + "es", tok + "ed", tok + "ing"}
        if tok.endswith("e"):
            alts.add(tok[:-1])
        if any(a in sl for a in alts):
            return True
        if len(tok) >= 5 and tok[:-1] in sl:
            return True
        if any(s in sl for s in synonyms.get(tok, ())):
            return True
        return False

    if toks and not any(hit(t) for t in toks[:6]):
        issues.append("weak-Q-keyword")
    return issues


def main() -> int:
    data = load_p1()
    rows: list[str] = []
    checked = 0
    same = 0
    for cat in data["categories"]:
        for q in cat["questions"]:
            kids = q.get("kitIds") or []
            variants = q.get("kitVariants") or {}
            samples = []
            for kid in kids or [q.get("kitId") or "main"]:
                checked += 1
                v = variants.get(kid) or {}
                sample = v.get("sample") or q.get("sample") or ""
                samples.append(sample)
                notes = check_sample(q["q"], sample)
                if notes:
                    rows.append(
                        f"- [{cat['id']}] {q.get('topicEn')} | {q['q']}\n"
                        f"  kit={kid} src={v.get('sampleSource') or q.get('sampleSource')} :: {'; '.join(notes)}\n"
                        f"  sample={sample[:160]}"
                    )
            if len(kids) >= 2:
                uniq = {s for s in samples if s}
                if len(uniq) < 2:
                    same += 1
                    rows.append(
                        f"- [{cat['id']}] {q.get('topicEn')} | {q['q']}\n"
                        f"  kit=variants :: identical samples across {kids}"
                    )

    print(f"checked={checked} issues={len(rows)} identical_multi={same}")
    for line in rows[:80]:
        print(line)
    if len(rows) > 80:
        print(f"... and {len(rows) - 80} more")
    out = ROOT / "_p1_natural_audit.txt"
    out.write_text(
        f"checked={checked} issues={len(rows)} identical_multi={same}\n\n" + "\n".join(rows),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
