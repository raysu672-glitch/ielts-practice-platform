#!/usr/bin/env python3
"""Fix remaining phrase issues + improve broken P1 contrast samples."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MORE_PHRASE_FIXES = [
    ("在1995 年达到峰值 200 亿", "在1995年达到峰值20亿"),
    ("peak at 2 billion in 1995", "peak at 2 billion in 1995"),  # keep EN; CN fixed above
    ("discriminate between right and wrong", "distinguish between right and wrong"),
    ("对保护环境重要", "对保护环境至关重要"),
    ("be crucial to protecting the environment", "be crucial for protecting the environment"),
    ("break ecological balance", "disrupt ecological balance"),
    ("cultural devolution", "cultural decline"),
    ("寻求在线退款复杂而低效", "在线申请退款繁琐且低效"),
    ("可以无限制的上网", "可无限上网"),
    ("be obedient to parents 'expectations", "be obedient to parents' expectations"),
    ("be obedient to parents 'expectations", "be obedient to parents' expectations"),
    ("保持大致的不变的", "保持大致不变"),
    ("remain roughly static", "remain roughly stable"),
    ("drop to its bottom at 34%", "reach its lowest point at 34%"),
    ("fluctuate upwardly within a decade", "fluctuate upward within a decade"),
    ("增长的最大", "增幅最大"),
    ("break laws", "break the law"),
    ("have deterrent effect", "have a deterrent effect"),
    ("intrusion of privacy", "invasion of privacy"),
    ("create a favorable condition", "create favourable conditions"),
    ("过渡地开采大自然", "过度地开采自然"),
    ("exploit the nature excessively", "exploit nature excessively"),
    ("attach importance to education background", "attach importance to educational background"),
    ("be of commercial and cultural values", "be of commercial and cultural value"),
    ("运用最新科技技术", "运用最新科技"),
    ("a drastic decrement", "a drastic decrease"),
    ("climb up with fluctuations", "climb with fluctuations"),
    ("continue to increase /soar", "continue to increase / soar"),
    ("eight fold", "eightfold"),
    ("be twice the size of it was in 2015", "be twice the size it was in 2015"),
    ("be located on the shopping mall", "be located next to the shopping mall"),
    ("be circled by forests", "be surrounded by forests"),
    ("financial-disadvantaged families", "financially disadvantaged families"),
    ("a good job prospect", "good job prospects"),
    ("advocate vegetarian diet", "advocate a vegetarian diet"),
]

# Map old broken sample text -> improved sample (full string inside quotes)
# Keys are unique fragments of the broken samples after first rewrite.
P1_SAMPLE_REPLACEMENTS = [
    (
        "I prefer A. As for the first side, it feels stronger because of have breakfast. By contrast, the other side differs due to binge-watch TV shows. Overall, I find work hard at my studies more suitable, which I prefer.",
        "I prefer having breakfast to binge-watching TV shows. A proper breakfast keeps me focused for morning classes, while long shows often waste time and make me sluggish. Overall, studying with energy matters more to me.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of my rented apartment. By contrast, the other side differs due to attend classes and parties. Overall, I find practical more suitable, which I prefer.",
        "I prefer living in a rented apartment near campus. It is more practical for attending classes, even though parties with friends are fun. Being close to school helps me manage time better.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of tasty local food. By contrast, the other side differs due to groceries and fresh ingredients. Overall, I find it really hits the spot more suitable, which I prefer.",
        "I prefer tasty local food when I eat out. It really hits the spot, although buying groceries and cooking with fresh ingredients is healthier. For a quick treat, local dishes win for me.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of shop online. By contrast, the other side differs due to the classroom. Overall, I find time-saving and effortless more suitable, which I prefer.",
        "I prefer shopping online because it is time-saving and effortless. Going out or dealing with crowded places takes longer. For daily needs, online shopping suits me better.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of have breakfast. By contrast, the other side differs due to watch short videos. Overall, I find feel relaxed and at ease more suitable, which I prefer.",
        "I prefer having breakfast in the morning rather than scrolling short videos. Eating properly helps me feel relaxed and ready for the day, while videos often leave me restless.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of attend classes. By contrast, the other side differs due to binge-watch TV shows. Overall, I find self-care more suitable, which I prefer.",
        "I prefer attending classes over binge-watching TV shows. Classes keep me on track, and I still leave some evening time for self-care. Balance matters more than endless episodes.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of play video games. By contrast, the other side differs due to me-time. Overall, I find have a good laugh more suitable, which I prefer.",
        "I prefer playing video games when I need a good laugh with friends. Quiet me-time is also valuable, but games help me unwind faster after a stressful day.",
    ),
    (
        "I prefer reading on paper. As for the first side, it feels stronger because of flip through physical books. By contrast, the other side differs due to spend a lot of time on my phone. Overall, I find reflect on things more suitable, which I prefer.",
        "I prefer reading on paper because flipping through physical books helps me reflect. Spending a lot of time on my phone is convenient, but paper reading feels deeper and calmer.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of physical books. By contrast, the other side differs due to takeout. Overall, I find work hard at my studies more suitable, which I prefer.",
        "I prefer physical books when I study hard. Takeout is convenient on busy nights, but books keep me focused better than eating while scrolling.",
    ),
    (
        "I prefer A. As for the first side, it feels stronger because of enjoy tasty local food. By contrast, the other side differs due to hiking. Overall, I find unwind more suitable, which I prefer.",
        "I prefer enjoying tasty local food to unwind, though hiking is a healthier option. After a long week, good food helps me relax more quickly.",
    ),
]


def apply_phrase_fixes(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    n = 0
    for old, new in MORE_PHRASE_FIXES:
        if old != new and old in text:
            c = text.count(old)
            text = text.replace(old, new)
            n += c
    path.write_text(text, encoding="utf-8")
    return n


def fix_p1_samples() -> int:
    path = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
    text = path.read_text(encoding="utf-8")
    n = 0
    for old, new in P1_SAMPLE_REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            n += 1
        else:
            # try slightly different whitespace
            print("WARN missing sample fragment:", old[:60], "...")
    path.write_text(text, encoding="utf-8")
    return n


def main() -> None:
    files = [
        ROOT / "sources" / "tinglidanciceshi" / "js" / "modules.js",
        ROOT / "sources" / "xiezuocihuo" / "categories.js",
        ROOT / "sources" / "xiezuocihuoceshi" / "index.html",
    ]
    for f in files:
        n = apply_phrase_fixes(f)
        print(f"{f.name}: {n} phrase replacements")
    n = fix_p1_samples()
    print(f"p1 samples replaced: {n}")
    # verify leftovers
    p1 = (ROOT / "sources" / "kouyulianxi" / "p1-data.js").read_text(encoding="utf-8")
    print("leftover feels stronger because of:", p1.count("feels stronger because of"))
    for s in ["保持大致的不变的", "break laws", "intrusion of privacy", "过渡地开采", "200 亿", "discriminate between right"]:
        total = 0
        for f in files:
            total += f.read_text(encoding="utf-8").count(s)
        print(f" leftover {s!r}: {total}")


if __name__ == "__main__":
    main()
