# -*- coding: utf-8 -*-
"""单字词、多音节、却无重音记号的条目（真问题）。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

VOW = set("aæeioəɪʊɛɒʌɑɔɜu")

print("=== 单字词且元音数>=3 但完全没有重音记号 ===")
n = 0
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) != 1 or "-" in word:
        continue
    syl = sum(1 for c in re.sub(r"dʒ|tʃ|ʤ|ʧ", "J", ph) if c in VOW)
    if syl >= 3 and "ˈ" not in ph and "ˌ" not in ph:
        n += 1
        print("  %-24s %-30s 元音数=%d" % (word, ph, syl))
print("  小计 %d 条" % n)

print()
print("=== 单字词且元音数>=2 但完全没有重音记号（含二音节）===")
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) != 1 or "-" in word:
        continue
    syl = sum(1 for c in re.sub(r"dʒ|tʃ|ʤ|ʧ", "J", ph) if c in VOW)
    if syl == 2 and "ˈ" not in ph and "ˌ" not in ph:
        print("  %-24s %-30s" % (word, ph))
