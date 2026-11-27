# -*- coding: utf-8 -*-
"""Full P1 audit: kit topic fit + sample answers the question (not forced material)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_align_engine import align_question_all_kits, detect_intent  # noqa: E402
from p1_material_bank import (  # noqa: E402
    MATERIALS,
    QUESTION_KIT_ALLOW,
    effective_topics,
    material_ids_for_question,
    normalize_topic,
)
from p1_word_banks_core import norm_q  # noqa: E402

P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"

# Topic → expected content keywords in sample (any hit OK)
TOPIC_HINTS: dict[str, tuple[str, ...]] = {
    "shoes": ("shoe", "sneaker", "trainer", "pair", "feet", "wear"),
    "clothing": ("clothes", "t-shirt", "shirt", "coat", "sweatshirt", "wear", "dress"),
    "mirrors": ("mirror", "look at myself", "get dressed", "reflect"),
    "watch": ("watch", "time", "punctual", "wrist"),
    "headphones": ("headphone", "earbud", "music", "listen", "noise"),
    "music": ("music", "song", "listen", "playlist"),
    "singing": ("sing", "song", "ktv", "karaoke"),
    "jokes & comedies": ("joke", "comed", "laugh", "funny"),
    "social media": ("wechat", "xiaohongshu", "douyin", "social", "post", "app"),
    "websites": ("website", "site", "online", "search", "bilibili", "xiaohongshu"),
    "advertisements": ("ad", "advert", "commercial", "poster", "screen"),
    "shopping": ("shop", "mall", "buy", "store", "online"),
    "street markets": ("market", "stall", "street", "bargain", "fresh"),
    "fruit and vegetables": ("fruit", "vegetable", "apple", "healthy", "fresh"),
    "rubbish and recycling": ("rubbish", "recycl", "bin", "garbage", "sort", "litter"),
    "paper": ("paper", "note", "book", "write", "print"),
    "tidiness": ("tidy", "clean", "desk", "organise", "organize", "mess"),
    "home & accommodation": ("home", "dorm", "apartment", "flat", "room", "live", "rent"),
    "the area you live in": ("area", "neighbour", "neighbor", "residential", "nearby", "live"),
    "the city you live in": ("city", "subway", "live", "urban", "crowded"),
    "hometown": ("hometown", "home town", "local", "grow up", "where i from", "my town"),
    "public gardens and parks": ("park", "garden", "walk", "fresh air", "green"),
    "cars": ("car", "drive", "driver", "passenger", "traffic", "road"),
    "travelling": ("travel", "trip", "holiday", "tour", "journey"),
    "teachers": ("teacher", "teach", "class", "explain", "lesson"),
    "secondary school": ("secondary", "school", "subject", "classmate", "uniform", "english", "maths", "math"),
    "science": ("science", "experiment", "biology", "lab", "discover", "technology", "tech", "space"),
    "outer space and stars": ("space", "star", "universe", "planet", "astronomy", "documentary"),
    "feeling bored": ("bored", "boring", "kill time", "scroll", "hang out"),
    "tiredness": ("tired", "exhaust", "rest", "break", "sleep", "nap", "relax"),
    "politeness": ("polite", "thank", "please", "manners", "respect", "door"),
    "name": ("name", "call", "meaning", "parents"),
    "opportunities": ("opportunit", "chance", "offer", "internship"),
    "work or studies": ("student", "stud", "class", "library", "major", "job", "career", "assignment", "exam", "degree", "campus", "business"),
}


BAD_SAMPLE_PATTERNS = [
    (r"\bi wear or use this\b", "template 'wear or use this'"),
    (r"\bi deal with this\b", "template 'deal with this'"),
    (r"\bmatters to me\b.*\bmatters to me\b", "repeated matters"),
    (r"\byes, definitely\.\s+to be specific, i focus on\b", "generic yes+focus dump"),
    (r"\byes, definitely\.\s+i am keen on (this|it) for the reason that\b", "generic yes+keen dump"),
    (r"\bis the detail i usually mention\b", "generic detail-mention dump"),
    (r"\bmatters in my routine, i keep the habit consistently\b", "generic habit-consistently dump"),
    (r"\bscience class and experiments\b.*\bdaily life\b|\bdaily life\b.*\bscience class and experiments\b", "science daily-life hard fit"),
    (r"\bkeep the answer concrete\b", "meta pad"),
    (r"\bi usually keep this\b", "forced habit closer"),
]


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


def kit_topic_ok(mid: str, topic_en: str, qtext: str) -> bool:
    m = MATERIALS.get(mid)
    if not m:
        return False
    # 题级白名单可跨话题池挂真正扣题的套装
    allow = QUESTION_KIT_ALLOW.get(norm_q(qtext or ""))
    if allow and mid in allow:
        return True
    return normalize_topic(topic_en) in effective_topics(m)


def sample_topic_ok(topic_en: str, qtext: str, sample: str) -> list[str]:
    issues: list[str] = []
    sl = (sample or "").lower()
    ql = qtext.lower()
    if not sample:
        return ["empty sample"]
    for pat, note in BAD_SAMPLE_PATTERNS:
        if re.search(pat, sl):
            issues.append(note)
    hints = TOPIC_HINTS.get(normalize_topic(topic_en), ())
    if hints and not any(h in sl for h in hints):
        # also allow question-content words (with light stems)
        stop = {
            "what", "when", "where", "which", "your", "does", "have", "been", "would", "could",
            "about", "most", "often", "usually", "people", "think", "with", "from", "that", "this",
            "did", "you", "the", "and", "for", "are", "was", "how", "who", "why", "any", "had",
            "kind", "type", "area", "part", "thing", "things", "like",
        }
        short_keep = {"car", "own", "bus", "ads", "lab", "nap", "job", "app", "map", "gym"}
        q_tokens = []
        for w in re.findall(r"[a-z]{3,}", ql):
            if w in stop:
                continue
            if len(w) >= 4 or w in short_keep:
                q_tokens.append(w)

        def hit(tok: str) -> bool:
            if tok in sl:
                return True
            alts = {tok + "s", tok + "es", tok + "ed", tok + "ing"}
            if tok.endswith("e"):
                alts.add(tok[:-1])
            return any(a in sl for a in alts) or (len(tok) >= 5 and tok[:-1] in sl)

        if not any(hit(t) for t in q_tokens[:6]):
            issues.append("sample missing topic/question keywords")
    # Opening mismatch heuristics
    if ql.startswith(("what kind", "what type", "which ")) and sl.startswith(("yes,", "not really")):
        issues.append("what/which Q opens with Yes/Not really")
    if "who " in ql[:8] and sl.startswith(("yes,", "not really")):
        issues.append("who Q opens with Yes/Not really")
    if ql.startswith(("how does", "how often", "how do you")) and sl.startswith("yes,"):
        issues.append("how Q opens with Yes")
    if ql.startswith("when ") and sl.startswith(("yes,", "not really")):
        issues.append("when Q opens with Yes/Not really")
    if "affect your daily life" in ql and "science class" in sl and not any(
        x in sl for x in ("phone", "technology", "transport", "weather", "app", "everyday")
    ):
        issues.append("daily-life Q stuck on classroom science")
    return issues


def main() -> int:
    data = load_p1()
    topic_order: dict[str, list[str]] = {}
    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            topic_order.setdefault(t, [])
            if q["q"] not in topic_order[t]:
                topic_order[t].append(q["q"])

    rows: list[str] = []
    checked = 0
    cov_lt2 = 0
    same_sample = 0
    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            idx = topic_order.get(t, [q["q"]]).index(q["q"]) if q["q"] in topic_order.get(t, []) else 0
            kids = material_ids_for_question(t, q["q"])
            aligned = align_question_all_kits(cat["id"], q["q"], t, topic_q_index=idx)
            variants = aligned.get("kitVariants") or {aligned.get("kitId") or "main": aligned}
            # Freestyle coverage: prefer ≥2 kits
            if len(kids) < 2:
                cov_lt2 += 1
                rows.append(
                    f"- [{cat['id']}/{detect_intent(q['q'])}] {t} | {q['q']}\n"
                    f"  kit=coverage :: need ≥2 kits, got {len(kids)} {kids}"
                )
            # Switching kits must change the sample text
            if len(kids) >= 2:
                samples = [(kid, (variants.get(kid) or {}).get("sample") or "") for kid in kids]
                uniq = {s for _, s in samples if s}
                if len(uniq) < 2:
                    same_sample += 1
                    rows.append(
                        f"- [{cat['id']}/{detect_intent(q['q'])}] {t} | {q['q']}\n"
                        f"  kit=variants :: identical samples across kits {kids}\n"
                        f"  sample={(samples[0][1] if samples else '')[:160]}"
                    )
            for kid in kids:
                checked += 1
                issues: list[str] = []
                if not kit_topic_ok(kid, t, q["q"]):
                    issues.append(f"kit '{kid}' not fit topic '{t}'")
                v = variants.get(kid) or {}
                sample = v.get("sample") or aligned.get("sample") or ""
                issues.extend(sample_topic_ok(t, q["q"], sample))
                if issues:
                    rows.append(
                        f"- [{cat['id']}/{detect_intent(q['q'])}] {t} | {q['q']}\n"
                        f"  kit={kid} :: {'; '.join(issues)}\n"
                        f"  sample={sample[:160]}"
                    )

    print(f"checked={checked} misfits={len(rows)} cov_lt2={cov_lt2} same_sample={same_sample}")
    for line in rows[:100]:
        print(line)
    if len(rows) > 100:
        print(f"... and {len(rows) - 100} more")
    # write full report
    out = ROOT / "_p1_full_fit_audit.txt"
    out.write_text(
        f"checked={checked} misfits={len(rows)} cov_lt2={cov_lt2} same_sample={same_sample}\n\n"
        + "\n".join(rows),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
