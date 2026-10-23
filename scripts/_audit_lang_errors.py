#!/usr/bin/env python3
"""High-confidence language error scan for focus content files."""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sources"

KNOWN_BAD = [
    (r"financial-disadvantaged", "financially disadvantaged", "副词缺-ly"),
    (r"financial disadvantaged\b", "financially disadvantaged", "副词缺-ly"),
    (r"economically-disadvantaged", "economically disadvantaged", "错误连字符"),
    (r"economic-disadvantaged", "economically disadvantaged", "副词缺-ly"),
    (r"economic disadvantaged\b", "economically disadvantaged", "副词缺-ly"),
    (r"socially-disadvantaged", "socially disadvantaged", "错误连字符"),
    (r"social-disadvantaged", "socially disadvantaged", "副词缺-ly"),
    (r"social disadvantaged\b", "socially disadvantaged", "副词缺-ly"),
    (r"environment-disadvantaged", "environmentally disadvantaged", "副词缺-ly"),
    (r"a drastic decrement", "a drastic decrease / a sharp decline", "用词错误"),
    (r"drastic decrement", "drastic decrease / sharp decline", "用词错误"),
    (r"\beight fold\b", "eightfold", "拼写/构词"),
    (r"intrusion of privacy", "invasion of privacy", "搭配错误"),
    (r"golf court\b", "golf course", "用词错误"),
    (r"plane science\b", "plant science", "拼写错误"),
    (r"primary cause\b", "a primary cause", "缺冠词"),
]

# Adjective prefix + participle without -ly (high-confidence subset)
ADV_PART = re.compile(
    r"\b(financial|economic|social|environment)-"
    r"(disadvantaged|motivated|oriented|related|connected|dependent|"
    r"conscious|aware|friendly|sensitive|active|engaged|involved|"
    r"acceptable|responsible|sustainable|friendly)\b",
    re.I,
)

FILES = [
    ("写作词伙", ROOT / "xiezuocihuo/categories.js"),
    ("写作词伙测试", ROOT / "xiezuocihuoceshi/index.html"),
    ("听力模块", ROOT / "tinglidanciceshi/js/modules.js"),
    ("听力2400", ROOT / "tinglidanciceshi/listening.html"),
    ("听力基础", ROOT / "tinglidanciceshi/listening_basic.html"),
]

ZH_EN_RE = re.compile(
    r"(?:zh:\s*['\"]([^'\"]+)['\"]|zh:'([^']*)')"
    r".*?"
    r"(?:en:\s*['\"]([^'\"]+)['\"]|en:'([^']*)')",
    re.DOTALL,
)
INLINE_RE = re.compile(r"\{\s*zh:'([^']*)',\s*en:'([^']*)'\s*\}")
WORD_JSON_RE = re.compile(r'"word"\s*:\s*"([^"]+)"[^}]*?"meaning"\s*:\s*"([^"]+)"')


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def extract_pairs(text: str):
    pairs = []
    for m in INLINE_RE.finditer(text):
        pairs.append((m.group(1), m.group(2), m.start()))
    for m in ZH_EN_RE.finditer(text):
        zh = m.group(1) or m.group(2)
        en = m.group(3) or m.group(4)
        if zh and en:
            pairs.append((zh, en, m.start()))
    for m in WORD_JSON_RE.finditer(text):
        pairs.append((m.group(2), m.group(1), m.start()))
    return pairs


def check_en(en: str):
    hits = []
    for pat, sug, typ in KNOWN_BAD:
        m = re.search(pat, en, re.I)
        if m:
            hits.append((m.group(), sug, typ))
    m = ADV_PART.search(en)
    if m:
        prefix, rest = m.group(1).lower(), m.group(2).lower()
        hits.append((m.group(), f"{prefix}ly {rest}", "副词缺-ly/错误连字符"))
    return hits


def main():
    all_findings = []
    for mod, fp in FILES:
        if not fp.exists():
            print(f"MISSING {fp}")
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        mod_findings = []

        for m in ADV_PART.finditer(text):
            ln = line_no(text, m.start())
            mod_findings.append((mod, f"{fp.name}:{ln}", m.group(), f"{m.group(1).lower()}ly {m.group(2).lower()}", "副词缺-ly/错误连字符"))

        for pat, sug, typ in KNOWN_BAD:
            for m in re.finditer(pat, text, re.I):
                ln = line_no(text, m.start())
                mod_findings.append((mod, f"{fp.name}:{ln}", m.group(), sug, typ))

        for zh, en, pos in extract_pairs(text):
            for bad, sug, typ in check_en(en):
                ln = line_no(text, pos)
                loc = f"{fp.name}:{ln} 「{zh[:40]}」"
                mod_findings.append((mod, loc, bad if bad in en else en, sug, typ))

        # Extra high-confidence listening mismatches
        if "listening" in fp.name:
            for m in WORD_JSON_RE.finditer(text):
                word = m.group(1)
                meaning = m.group(2)
                ln = line_no(text, m.start())
                # obvious typos in meaning vs word
                checks = [
                    (r"golf court", word, "golf course", "用词错误"),
                    (r"plane science", word, "plant science", "拼写错误"),
                ]
                for pat, w, sug, typ in checks:
                    if re.search(pat, word, re.I):
                        mod_findings.append((mod, f"{fp.name}:{ln} word={word}", word, sug, typ))

        # dedupe per module
        seen = set()
        for f in mod_findings:
            key = (f[1], f[2], f[4])
            if key not in seen:
                seen.add(key)
                all_findings.append(f)

    for f in sorted(all_findings, key=lambda x: (x[0], x[1])):
        print(" | ".join(f))
    print("---TOTAL", len(all_findings))
    for mod, _ in FILES:
        cnt = sum(1 for x in all_findings if x[0] == mod)
        print(f"  {mod}: {cnt} issues")


if __name__ == "__main__":
    main()
