# -*- coding: utf-8 -*-
"""
Rebuild sources/kouyulianxi/p1-data.js from 2026-05~08 heat list.
- Keep only currently tested questions
- Order by heat within each of 5 categories
- Per-question word banks from p1_word_banks.resolve_words
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_frames import resolve_frames
from p1_sample_answers import generate_sample
from p1_word_banks import resolve_words
from p1_word_banks_core import kit_for, norm_q

HEAT = ROOT / "_p1_heat_parsed.json"
OLD = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
OUT = ROOT / "sources" / "kouyulianxi" / "p1-data.js"


def load_old_index() -> dict[str, dict]:
    """Map normalized q -> old question object (prefer first)."""
    if not OLD.is_file():
        return {}
    text = OLD.read_text(encoding="utf-8")
    raw = text[text.find("{") : text.rfind("}") + 1]
    data = json.loads(raw)
    idx: dict[str, dict] = {}
    for cat in data["categories"]:
        for q in cat["questions"]:
            key = norm_q(q.get("q") or q.get("title") or "")
            if key and key not in idx:
                idx[key] = {**q, "_oldCat": cat["id"]}
    return idx


def build_tip(cat_name: str, topic: dict, qtext: str, logic: str, kit: dict) -> str:
    return (
        f"【{topic['tag']}·热度#{topic['heatRank']}·近{topic['recentCount']}人】"
        f"{logic} 本题按「{cat_name}」四步答；素材：{kit['mat']}。"
    )


def short_title(q: str) -> str:
    t = q.strip().rstrip("?")
    if len(t) > 72:
        t = t[:69] + "..."
    return t


def main() -> None:
    heat = json.loads(HEAT.read_text(encoding="utf-8"))
    old_idx = load_old_index()
    source_stats: dict[str, int] = {}
    sample_fail = 0
    categories = []

    for cat in heat:
        questions = []
        qid = 1
        for topic in cat["topics"]:
            kit = kit_for(topic["topicEn"])
            for qtext in topic["questions"]:
                old = old_idx.get(norm_q(qtext))
                words, logic, source = resolve_words(cat["id"], qtext, cat["steps"], topic["topicEn"])
                frames = resolve_frames(cat["id"], qtext)
                sample = generate_sample(cat["id"], qtext, cat["steps"], words, frames)
                source_stats[source] = source_stats.get(source, 0) + 1
                item = {
                    "id": qid,
                    "title": short_title(qtext),
                    "q": qtext if qtext.endswith("?") else qtext + "?",
                    "topicEn": topic["topicEn"],
                    "topicZh": topic["topicZh"],
                    "tag": topic["tag"],
                    "recentCount": topic["recentCount"],
                    "heatRank": topic["heatRank"],
                    "tip": build_tip(cat["name"], topic, qtext, logic, kit),
                    "logic": logic,
                    "material": kit["mat"],
                    "words": words,
                    "frames": frames,
                    "sample": sample["text"],
                    "sampleOk": sample["ok"],
                    "sampleNote": sample["note"],
                    "sampleSource": sample["source"],
                    "wordSource": source,
                }
                if old and old.get("clueId"):
                    item["clueId"] = old["clueId"]
                if not sample["ok"]:
                    sample_fail += 1
                questions.append(item)
                qid += 1
        categories.append(
            {
                "id": cat["id"],
                "name": cat["name"],
                "steps": cat["steps"],
                "questions": questions,
            }
        )

    data = {
        "meta": {
            "season": "2026年5-8月",
            "heatSource": "雅思哥 2026-08-25",
            "note": "仅保留大陆考区当季在考小题；同类内按近期考过人数排序",
            "totalQuestions": sum(len(c["questions"]) for c in categories),
            "wordSourceStats": source_stats,
            "sampleLogicFail": sample_fail,
        },
        "categories": categories,
    }

    js = (
        "// P1 data - 2026年5-8月在考题（五类按热度）+ 逐题词块\n"
        "const P1_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n"
    )
    OUT.write_text(js, encoding="utf-8")
    summary = ROOT / "_p1_rebuild_summary.txt"
    lines = [
        f"wrote {OUT}",
        f"total={data['meta']['totalQuestions']} sources={source_stats}",
        f"sampleLogicFail={sample_fail}",
    ]
    for c in categories:
        lines.append(f"{c['id']}: {len(c['questions'])}")
        seen = set()
        tops = []
        for q in c["questions"]:
            if q["topicEn"] in seen:
                continue
            seen.add(q["topicEn"])
            tops.append(f"  #{q['heatRank']} {q['topicEn']} ({q['recentCount']})")
            if len(tops) >= 3:
                break
        lines.extend(tops)
    summary.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
