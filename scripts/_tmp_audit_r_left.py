# -*- coding: utf-8 -*-
"""列出仍保留 r、但 r 后面不是元音的位置（英式下应为 0）。"""
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
print("=== r 后不是元音、且未写成 (r) 的位置（英式下应为 0）===")
n = 0
for w in ws:
    ph = w.get("phonetic", "")
    for m in re.finditer("r", ph):
        nxt = ph[m.end():m.end() + 1]
        prev = ph[m.start() - 1:m.start()]
        if prev == "(" and nxt == ")":
            continue
        if nxt in VOW:
            continue
        n += 1
        print("  %-26s %s   (r 后是 %r)" % (w["word"], ph, nxt))
        break
print("  小计 %d 条" % n)

print()
print("=== 仅剩的 ɪr/ɛr/ʊr 组合（应都是 r+元音）===")
for w in ws:
    ph = w.get("phonetic", "")
    for m in re.finditer(r"[ɪɛʊ]r", ph):
        print("  %-26s %s" % (w["word"], ph))
        break
