# -*- coding: utf-8 -*-
"""Parse May-Aug 2026 P1 heat list into structured JSON."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

SRC = Path(r"G:\口语练习\2026年5-8月P1题目_五类分类按热度.txt")
OUT = Path("_p1_heat_parsed.json")

CAT_MAP = {
    "事实陈述类": ("shishi", ["正面回答", "来源或举例", "频次", "感受"]),
    "喜好类": ("xihao", ["正面回答", "原因或时间", "频次", "感受"]),
    "行为习惯类": ("xingwei", ["正面回答", "原因", "时间线+行为描述", "影响"]),
    "观点类": ("guandian", ["正面回答", "举例或原因", "作用或影响", "感受"]),
    "对比类": ("duibi", ["正面回答", "选项1的特点与作用", "选项2的特点与作用", "个人感受"]),
}


def nf(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


TOPIC_PAT = re.compile(
    r"(?m)^(\d+)\.\s+(.+?)\(([^)]+)\)\s*【([^】]+)】\s+近期\s+(\d+)\s*人考过\s*$"
)


def parse_topics(block: str) -> list[dict]:
    topics = []
    matches = list(TOPIC_PAT.finditer(block))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        qs_block = block[start:end]
        qs_block = re.split(r"(?m)^怎么用|^数据日期|^类别", qs_block)[0]
        qs = re.findall(r"(?m)^-\s+(.+?)\s*$", qs_block)
        cleaned = []
        for q in qs:
            q = re.sub(r"\s+", " ", q).strip().rstrip(".,;，。")
            if not q.endswith("?"):
                q += "?"
            cleaned.append(q)
        topics.append(
            {
                "rankInCat": int(m.group(1)),
                "topicEn": m.group(2).strip(),
                "topicZh": m.group(3).strip(),
                "tag": m.group(4).strip(),
                "recentCount": int(m.group(5)),
                "questions": cleaned,
            }
        )
    topics.sort(key=lambda t: (-t["recentCount"], t["rankInCat"]))
    for i, t in enumerate(topics, 1):
        t["heatRank"] = i
    return topics


def main() -> None:
    text = nf(SRC.read_text(encoding="utf-8"))
    # Split by category headers (keep delimiter)
    pieces = re.split(r"(?m)^(类别[一二三四五][:：].+)$", text)
    categories = []
    # pieces: [preamble, header1, body1, header2, body2, ...]
    for i in range(1, len(pieces), 2):
        header = pieces[i].strip()
        body = pieces[i + 1] if i + 1 < len(pieces) else ""
        cname = None
        for k in CAT_MAP:
            if k in header or k in body[:120]:
                cname = k
                break
        if not cname:
            continue
        cid, steps = CAT_MAP[cname]
        topics = parse_topics(body)
        categories.append(
            {
                "id": cid,
                "name": cname,
                "steps": steps,
                "topics": topics,
                "q_count": sum(len(t["questions"]) for t in topics),
            }
        )

    OUT.write_text(json.dumps(categories, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = [
        f"{c['id']} {c['name']} q={c['q_count']} topics={len(c['topics'])}" for c in categories
    ]
    summary.append(f"TOTAL {sum(c['q_count'] for c in categories)}")
    Path("_p1_heat_summary.txt").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
