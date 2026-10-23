# -*- coding: utf-8 -*-
"""找重音记号前完全没有元音的条目（重音被挪到词首辅音之后，如 mˈjuzɪk）。"""
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

print("=== 主重音 ˈ 之前有辅音、却没有任何元音（疑似重音错位）===")
n = 0
for w in ws:
    ph = w.get("phonetic", "")
    for m in re.finditer("ˈ", ph):
        head = [c for c in ph[:m.start()] if c.isalpha()]
        if head and not any(c in VOW for c in head):
            n += 1
            print("  %-24s %s" % (w["word"], ph))
            break
print("  小计 %d 条" % n)

print()
print("=== 次重音 ˌ 之前有辅音、却没有任何元音（同理）===")
n2 = 0
for w in ws:
    ph = w.get("phonetic", "")
    for m in re.finditer("ˌ", ph):
        head = [c for c in ph[:m.start()] if c.isalpha()]
        if head and not any(c in VOW for c in head):
            n2 += 1
            print("  %-24s %s" % (w["word"], ph))
            break
print("  小计 %d 条" % n2)
