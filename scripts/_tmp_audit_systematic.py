# -*- coding: utf-8 -*-
"""深挖系统性音标错误：θ→ə、d→ɒ、ŋ→n/ɡ 等。"""
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

print("=== ① θ 被写成 ə 的完整清单（单词含 th，音标无 θ/ð）===")
n = 0
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if "th" in word and "θ" not in ph and "ð" not in ph:
        n += 1
        print("  %-22s %-28s %s" % (w["word"], ph, w.get("meaning", "")))
print("  小计 %d 条" % n)

print()
print("=== ② 音标含 nɒ / ɒʒ / ɒz（疑似 d 被写成 ɒ）===")
for w in ws:
    ph = w.get("phonetic", "")
    if re.search(r"nɒ[ʒz]|ɒə", ph):
        print("  %-22s %-28s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== ③ 单词以 -ing 结尾，音标词尾却是 n（疑似 ŋ→n）===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if re.search(r"ing$", word) and re.search(r"[ɪiə]n/?\]?$", ph) and "ŋ" not in ph:
        print("  %-22s %-28s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== ④ 单词含 ng 但音标里是 ɡ 而非 ŋ（疑似 ŋ→ɡ）===")
for w in ws:
    word, ph = w["word"].lower(), w.get("phonetic", "")
    if re.search(r"ng", word) and "ŋ" not in ph and re.search(r"ɡ", ph):
        print("  %-22s %-28s %s" % (w["word"], ph, w.get("meaning", "")))

print()
print("=== ⑤ 音标里 ɒ 出现次数 >= 2 的词（便于人工核对）===")
for w in ws:
    ph = w.get("phonetic", "")
    if ph.count("ɒ") >= 2:
        print("  %-22s %-28s %s" % (w["word"], ph, w.get("meaning", "")))
