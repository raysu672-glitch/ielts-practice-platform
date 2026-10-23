# -*- coding: utf-8 -*-
"""精确抓「音标内多余空格」：空格后面不是重音记号 ˌ/ˈ 的位置。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

print("=== 单字词的音标内嵌空格（空格后不是 ˌ/ˈ）===")
n = 0
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) != 1:      # 短语的词间空格属正常
        continue
    for m in re.finditer(r"\s+", ph):
        nxt = ph[m.end():m.end() + 1]
        if nxt not in ("ˈ", "ˌ"):
            n += 1
            print("  %-24s %-32s %s" % (word, ph, w.get("meaning", "")))
            break
print("  小计 %d 条" % n)

print()
print("=== 短语（多词）中，音标分段数 ≠ 词数 的（疑似串位）===")
m2 = 0
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    nw = len(word.replace("-", " ").split())
    if nw < 2:
        continue
    body = ph.strip().strip("/[]")
    # 只在「非重音前的空格」计入分段
    seg = [x for x in re.split(r"\s+(?![ˈˌ])", body) if x.strip()]
    if len(seg) != nw:
        m2 += 1
        print("  %-26s 词%d段 音标%d段  %s" % (word, nw, len(seg), ph))
print("  小计 %d 条" % m2)
