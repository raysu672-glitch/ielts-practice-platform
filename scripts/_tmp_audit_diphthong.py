# -*- coding: utf-8 -*-
"""检查二合元音记法：oɪ/oi 应为 ɔɪ、oʊ 与 əʊ 混用等。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

checks = {
    "oɪ  (应为 ɔɪ)": r"oɪ",
    "oi  (应为 ɔɪ)": r"oi",
    "oʊ  (美式写法)": r"oʊ",
    "əʊ  (英式写法)": r"əʊ",
    "ou  (字母残留)": r"ou",
    "ei  (应为 eɪ)": r"ei",
    "ai  (应为 aɪ)": r"ai",
    "au  (应为 aʊ)": r"au",
    "ɔɪ  (标准)": r"ɔɪ",
}
for label, pat in checks.items():
    hits = [w["word"] for w in ws if re.search(pat, w.get("phonetic", ""))]
    print("%-18s %3d 条  %s" % (label, len(hits), ", ".join(hits[:14])))

print()
print("=== 「o」单独出现（既非 oʊ 也非 oɪ/oː）的条目 ===")
for w in ws:
    p = w.get("phonetic", "")
    t = re.sub(r"oʊ|oɪ|oː", "", p)
    if "o" in t:
        print("  %-24s %s" % (w["word"], p))
