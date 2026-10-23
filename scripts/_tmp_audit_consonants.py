# -*- coding: utf-8 -*-
"""专项排查：辅音字母组合与音标不符（θ/ð、ʃ、tʃ、dʒ、ŋ 等）。"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

print("=== A. 单词含 th，但音标里没有 θ 或 ð ===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if "th" in word and "θ" not in ph and "ð" not in ph:
        print("  %-24s %-30s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== B. 单词不含 th，但音标里有 θ/ð（反向）===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if "th" not in word and ("θ" in ph or "ð" in ph):
        print("  %-24s %-30s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== C. 单词含 sh，但音标里没有 ʃ ===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if "sh" in word and "ʃ" not in ph:
        print("  %-24s %-30s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== D. 单词含 ng，但音标里没有 ŋ ===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if re.search(r"ng", word) and "ŋ" not in ph and "ndʒ" not in ph and "dʒ" not in ph:
        print("  %-24s %-30s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== E. 音标里出现孤立 ə 结尾但单词以辅音字母结尾（疑似辅音被写成 ə）===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    core = re.sub(r"[^a-z]", "", word)
    if re.search(r"[bcdfghjklmnpqrstvwxz]$", core) and re.search(r"ə/\]?$", ph):
        print("  %-24s %-30s %s" % (w["word"], ph, w.get("meaning", "")))
