#!/usr/bin/env python3
"""Batch-fix content audit issues: listening basic, writing phrases, dictation dedupe, P1 dirt."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "sources" / "tinglidanciceshi" / "js" / "modules.js"
LISTENING_BASIC = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"
LISTENING = ROOT / "sources" / "tinglidanciceshi" / "listening.html"
CATEGORIES = ROOT / "sources" / "xiezuocihuo" / "categories.js"
P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
AUDIO_XIHAO_25 = ROOT / "sources" / "kouyulianxi" / "audio" / "xihao" / "25.txt"

BASIC_WORD_FIXES: dict[str, str] = {
    "alarming system": "alarm system",
    "golf court": "golf course",
    "plane science": "planet science",  # may duplicate; dedupe later
    "personal officer": "personnel officer",
    "privacy company": "private company",
    "bottle water": "bottled water",  # may duplicate
    "animals behavior": "animal behaviour",
    "culture awareness": "cultural awareness",
    "culture context": "cultural context",
    "families life": "family life",
    "finance market": "financial market",
    "environment damage": "environmental damage",
    "economics history": "economic history",
    "eye contacts": "eye contact",
    "children background": "children's background",
    "children mind": "children's minds",
    "girl club": "girls' club",
    "hairs": "hair",
    "weathers": "weather",
    "study skill": "study skills",
    "repaired cost": "repair cost",
    "time consuming": "time-consuming",
    "triangle sharp": "triangle shape",
    "political man": "politician",
    "high user": "heavy user",
    "free pick": "free pick-up",
    "banana ride": "banana boat",
    "advance level": "advanced level",
    "view shelter": "viewing shelter",  # may duplicate
    "pet meat": "pet food",
    "videocameras": "video cameras",
}

BASIC_MEANING_FIXES: dict[str, str] = {
    "academic": "学术的；学院的",
    "achievement": "成就；成绩",
    "planet science": "行星科学",
    "politician": "政治家",
    "children's minds": "儿童心智",
    "triangle shape": "三角形",
    "alarm system": "警报系统",
    "golf course": "高尔夫球场",
    "private company": "私人公司",
    "animal behaviour": "动物行为",
    "personnel officer": "人事主管",
    "free pick-up": "免费接送",
    "banana boat": "香蕉船",
    "advanced level": "高级水平",
    "viewing shelter": "观景棚",
    "pet food": "宠物食品",
    "video cameras": "摄像机",
    "bottled water": "瓶装水",
}

PHRASE_FIXES: list[tuple[str, str]] = [
    ("a drastic decrement", "a drastic decrease"),
    ("climb up with fluctuations", "climb with fluctuations"),
    ("continue to increase /soar", "continue to increase / soar"),
    ("保持大致的不变的", "保持大致不变"),
    ("remain roughly static", "remain roughly stable"),
    ("fluctuate upwardly", "fluctuate upward"),
    ("eight fold", "eightfold"),
    ("rise more than eightfold", "rise more than eightfold"),  # noop if already
    ("be twice the size of it was in 2015", "be twice the size it was in 2015"),
    ("be located on the shopping mall", "be located next to the shopping mall"),
    ("be circled by forests", "be surrounded by forests"),
    ("intrusion of privacy", "invasion of privacy"),
    ("financial-disadvantaged families", "financially disadvantaged families"),
    ("break laws", "break the law"),
    ("have deterrent effect", "have a deterrent effect"),
    ("exploit the nature excessively", "exploit nature excessively"),
    ("过渡地开采大自然", "过度地开采自然"),
    ("运用最新科技技术", "运用最新科技"),
    ("a good job prospect", "good job prospects"),
    ("advocate vegetarian diet", "advocate a vegetarian diet"),
    ("create a favorable condition", "create favourable conditions"),
    ("attach importance to education background", "attach importance to educational background"),
    ("be of commercial and cultural values", "be of commercial and cultural value"),
    ("drop to its bottom at 34%", "reach its lowest point at 34%"),
    ("a very shortsighted view", "a very short-sighted view"),
    ("增长的最大", "增幅最大"),
    ("非常的昂贵", "极其昂贵"),
]


def extract_array(name: str, text: str) -> tuple[list, int, int]:
    m = re.search(rf"var {name}\s*=\s*\[", text)
    if not m:
        raise SystemExit(f"missing {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1]), start, i + 1
    raise SystemExit(f"unclosed {name}")


def dedupe_keep_order(words: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for w in words:
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
    return out


def fix_modules_basic_and_dictation() -> None:
    text = MODULES.read_text(encoding="utf-8")
    basic, bs, be = extract_array("allWordsListeningBasic", text)
    fixed_basic = []
    for w in basic:
        fixed_basic.append(BASIC_WORD_FIXES.get(w, w))
    fixed_basic = dedupe_keep_order(fixed_basic)

    dictation, ds, de = extract_array("allWords", text)
    # Prefer merging split phrases where both halves exist adjacent-ish
    # Just dedupe for now; phrase merge is riskier without positions
    fixed_dict = dedupe_keep_order(dictation)

    # apply phrase text fixes in modules.js (phraseCategories + foundation)
    for old, new in PHRASE_FIXES:
        if old != new:
            text = text.replace(old, new)

    # replace arrays (re-extract positions after phrase replaces? phrases are outside arrays usually)
    # Re-read arrays from original positions may be wrong if phrase edits shifted.
    # Safer: rewrite from current text after phrase fixes.
    text = MODULES.read_text(encoding="utf-8")
    for old, new in PHRASE_FIXES:
        if old != new:
            text = text.replace(old, new)

    basic, bs, be = extract_array("allWordsListeningBasic", text)
    fixed_basic = dedupe_keep_order([BASIC_WORD_FIXES.get(w, w) for w in basic])
    dictation, ds, de = extract_array("allWords", text)
    fixed_dict = dedupe_keep_order(dictation)

    # Replace larger end first
    if ds > bs:
        text = text[:ds] + json.dumps(fixed_dict, ensure_ascii=False) + text[de:]
        basic, bs, be = extract_array("allWordsListeningBasic", text)
        text = text[:bs] + json.dumps(fixed_basic, ensure_ascii=False) + text[be:]
    else:
        text = text[:bs] + json.dumps(fixed_basic, ensure_ascii=False) + text[be:]
        dictation, ds, de = extract_array("allWords", text)
        text = text[:ds] + json.dumps(fixed_dict, ensure_ascii=False) + text[de:]

    MODULES.write_text(text, encoding="utf-8")
    print(f"modules.js basic: {len(basic)} -> {len(fixed_basic)}; dictation: {len(dictation)} -> {len(fixed_dict)}")


def fix_listening_basic_html() -> None:
    html = LISTENING_BASIC.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", html, flags=re.S)
    if not m:
        raise SystemExit("ALL_WORDS missing in listening_basic.html")
    words = json.loads(m.group(1))
    seen: set[str] = set()
    out = []
    for item in words:
        w = BASIC_WORD_FIXES.get(item["word"], item["word"])
        item = dict(item)
        item["word"] = w
        if w in BASIC_MEANING_FIXES:
            item["meaning"] = BASIC_MEANING_FIXES[w]
        if w in seen:
            continue
        seen.add(w)
        out.append(item)
    new_json = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    html = html[: m.start(1)] + new_json + html[m.end(1) :]
    LISTENING_BASIC.write_text(html, encoding="utf-8")
    print(f"listening_basic.html: {len(words)} -> {len(out)}")


def fix_listening_html_dedupe() -> None:
    html = LISTENING.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", html, flags=re.S)
    if not m:
        raise SystemExit("ALL_WORDS missing in listening.html")
    words = json.loads(m.group(1))
    seen: set[str] = set()
    out = []
    for item in words:
        w = item["word"]
        if w in seen:
            continue
        seen.add(w)
        out.append(item)
    new_json = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    # preserve spacing style roughly - original used spaces after colons sometimes
    html = html[: m.start(1)] + new_json + html[m.end(1) :]
    LISTENING.write_text(html, encoding="utf-8")
    print(f"listening.html: {len(words)} -> {len(out)}")


def fix_categories_js() -> None:
    if not CATEGORIES.exists():
        print("categories.js missing, skip")
        return
    text = CATEGORIES.read_text(encoding="utf-8")
    n = 0
    for old, new in PHRASE_FIXES:
        if old != new and old in text:
            text = text.replace(old, new)
            n += 1
    CATEGORIES.write_text(text, encoding="utf-8")
    print(f"categories.js phrase fixes applied: {n}")


def fix_p1() -> None:
    text = P1.read_text(encoding="utf-8")
    # collapse repeated "the "
    text2 = re.sub(r"\b(?:the\s+){2,}the\b", "the", text)
    text2 = text2.replace("classroomss", "classrooms")
    text2 = text2.replace("in nowadays", "nowadays")
    text2 = text2.replace("live in in the future", "live in the future")
    text2 = text2.replace("in in the future", "in the future")

    # Fix broken contrast samples
    # Pattern: "... because of X and is regarded as. By contrast, ..."
    def rewrite_sample(m: re.Match) -> str:
        full = m.group(0)
        # extract because of ... and is regarded as
        mm = re.search(
            r"As for the first side, it is regarded as stronger because of (.+?) and is regarded as\."
            r" By contrast, regarding the other side, people find it different due to (.+?)(?: and by contrast)?\."
            r" Overall, I find (.+?) more suitable, which (.+?)\.",
            full,
        )
        if not mm:
            return full
        a, b, prefer, tail = mm.group(1), mm.group(2), mm.group(3), mm.group(4)
        # clean tails like "which practical." / "which I prefer."
        if "prefer" not in tail and "prefer" in prefer:
            ending = "which I prefer."
        elif tail.strip() in ("I prefer", "I prefer.", "practical", "practical."):
            ending = "which I prefer."
        else:
            ending = f"which {tail.strip().rstrip('.')}."
        new = (
            f'I prefer A. As for the first side, it feels stronger because of {a}. '
            f'By contrast, the other side differs due to {b}. '
            f'Overall, I find {prefer} more suitable, {ending}'
        )
        return f'"sample": "{new}"'

    text2 = re.sub(
        r'"sample":\s*"I prefer[^"]*and is regarded as\.[^"]*"',
        rewrite_sample,
        text2,
    )

    # Fix xihao#36 nonsense sample if still present
    text2 = text2.replace(
        "I am keen on this for the reason that the heavy traffic and because matters to me. Whenever I have time, I enjoy it during rush hour to stay positive. I find this activity relaxed, which helps me unwind, and it really gets to me.",
        "Not really. What I dislike most is the heavy traffic during rush hour — it wears me out. Whenever I have time, I prefer quieter spots so I can stay positive and unwind.",
    )

    P1.write_text(text2, encoding="utf-8")
    print(
        "p1 remaining:",
        "the-repeat", len(re.findall(r"the the the", text2)),
        "regarded", len(re.findall(r"and is regarded as\.", text2)),
        "nowadays", len(re.findall(r"in nowadays", text2)),
        "in in", len(re.findall(r"in in the", text2)),
        "classroomss", len(re.findall(r"classroomss", text2)),
    )

    if AUDIO_XIHAO_25.exists():
        a = AUDIO_XIHAO_25.read_text(encoding="utf-8")
        a2 = a.replace("live in in the future", "live in the future").replace(
            "in in the future", "in the future"
        )
        AUDIO_XIHAO_25.write_text(a2, encoding="utf-8")
        print("audio xihao/25.txt updated")


def main() -> None:
    fix_modules_basic_and_dictation()
    fix_listening_basic_html()
    fix_listening_html_dedupe()
    fix_categories_js()
    fix_p1()


if __name__ == "__main__":
    main()
