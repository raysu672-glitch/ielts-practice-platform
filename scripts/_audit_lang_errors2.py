#!/usr/bin/env python3
"""Extended high-confidence language error scan."""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sources"

FILES = [
    ("写作词伙 categories.js", ROOT / "xiezuocihuo/categories.js"),
    ("写作词伙测试", ROOT / "xiezuocihuoceshi/index.html"),
    ("听力 modules.js", ROOT / "tinglidanciceshi/js/modules.js"),
    ("听力2400 listening.html", ROOT / "tinglidanciceshi/listening.html"),
    ("听力基础 listening_basic.html", ROOT / "tinglidanciceshi/listening_basic.html"),
]

INLINE = re.compile(r"\{\s*zh:\s*['\"]([^'\"]+)['\"]\s*,\s*en:\s*['\"]([^'\"]+)['\"]\s*\}")
INLINE2 = re.compile(r"\{\s*zh:'([^']*)',\s*en:'([^']*)'\s*\}")
WORD_JSON = re.compile(
    r'\{"word":"([^"]+)","phonetic":"[^"]*","pos":"[^"]*","meaning":"([^"]+)"\}'
)


def extract_zh_en(text):
    pairs = []
    for m in INLINE.finditer(text):
        pairs.append((m.group(1), m.group(2), m.start()))
    for m in INLINE2.finditer(text):
        pairs.append((m.group(1), m.group(2), m.start()))
    return pairs


def line_no(text, pos):
    return text.count("\n", 0, pos) + 1


def audit_pairs(mod, fname, text, pairs):
    hits = []
    for zh, en, pos in pairs:
        ln = line_no(text, pos)
        loc = f"{fname}:{ln}"

        # High-confidence checks
        if re.search(r"parents\s+'expectations", en):
            hits.append((mod, loc, en, "parents' expectations", "标点/拼写", zh))
        if "性别/年龄歧视" in zh and "gender" in en.lower() and "age" not in en.lower():
            hits.append((mod, loc, en, "discriminate on the basis of gender or age", "中英不匹配", zh))
        if re.search(r"\bfinancial-disadvantaged\b", en, re.I):
            hits.append((mod, loc, en, "financially disadvantaged", "副词缺-ly", zh))
        if re.search(r"\bsocially-disadvantaged\b", en, re.I):
            hits.append((mod, loc, en, "socially disadvantaged", "错误连字符", zh))
        if re.search(r"\beight fold\b", en, re.I):
            hits.append((mod, loc, en, "eightfold", "拼写/构词", zh))
        if re.search(r"drastic decrement", en, re.I):
            hits.append((mod, loc, en, "drastic decrease", "用词错误", zh))
        if re.search(r"intrusion of privacy", en, re.I):
            hits.append((mod, loc, en, "invasion of privacy", "搭配错误", zh))
        if re.search(r"golf court\b", en, re.I):
            hits.append((mod, loc, en, "golf course", "用词错误", zh))
        if re.search(r"plane science\b", en, re.I):
            hits.append((mod, loc, en, "plant science", "拼写错误", zh))
        if re.search(r"\b(financial|economic|social|environment)-disadvantaged\b", en, re.I):
            hits.append((mod, loc, en, re.sub(r"-", "ly ", en, flags=re.I), "副词缺-ly/错误连字符", zh))

    return hits


def audit_listening_words(mod, fname, text):
    hits = []
    for m in WORD_JSON.finditer(text):
        word, meaning = m.group(1), m.group(2)
        ln = line_no(text, m.start())
        loc = f"{fname}:{ln} [{word}]"
        checks = [
            (r"golf court", "golf course", "用词错误"),
            (r"plane science", "plant science", "拼写错误"),
            (r"高尔夫球场的", word, "若 word=golf 则释义应为「高尔夫球」非球场", "中英不匹配"),
        ]
        if word.lower() == "golf" and "球场" in meaning:
            hits.append((mod, loc, f"{word} → {meaning}", "高尔夫球（运动）", "中英不匹配"))
        if word.lower() == "plant science" and "飞机" in meaning:
            hits.append((mod, loc, f"{word} → {meaning}", "植物科学", "中英不匹配"))
        if "plane science" in word.lower():
            hits.append((mod, loc, word, "plant science", "拼写错误"))
        if "golf court" in word.lower():
            hits.append((mod, loc, word, "golf course", "用词错误"))
    return hits


def main():
    all_hits = []
    for mod, fp in FILES:
        text = fp.read_text(encoding="utf-8", errors="replace")
        pairs = extract_zh_en(text)
        all_hits.extend(audit_pairs(mod, fp.name, text, pairs))
        if "listening" in fp.name:
            all_hits.extend(audit_listening_words(mod, fp.name, text))

    # dedupe
    seen = set()
    out = []
    for h in all_hits:
        key = (h[0], h[1], h[2], h[4])
        if key not in seen:
            seen.add(key)
            out.append(h)

    for mod, loc, err, sug, typ, *rest in sorted(out, key=lambda x: (x[0], x[1])):
        zh = rest[0] if rest else ""
        extra = f" （{zh}）" if zh else ""
        print(f"{mod} | {loc}{extra} | {err} | {sug} | {typ}")

    print(f"\n--- TOTAL: {len(out)}")
    for mod, _ in FILES:
        n = sum(1 for h in out if h[0] == mod)
        status = "已干净" if n == 0 else f"{n} 条"
        print(f"  {mod}: {status}")


if __name__ == "__main__":
    main()
