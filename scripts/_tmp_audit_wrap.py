# -*- coding: utf-8 -*-
"""定位包裹符号/斜杠异常的条目。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

print("=== 包裹符号异常 / 斜杠数异常 / 括号不配对 ===")
for w in ws:
    ph = w.get("phonetic", "").strip()
    if not ph:
        print("  %-24s 【空】" % w["word"])
        continue
    bad = []
    if ph[0] not in "/[" or ph[-1] not in "/]":
        bad.append("首尾不是斜杠/方括号")
    if ph.count("/") not in (0, 2) and "[" not in ph:
        bad.append("斜杠数=%d" % ph.count("/"))
    if ph.count("(") != ph.count(")"):
        bad.append("括号不配对")
    if bad:
        print("  %-24s %-32s %s" % (w["word"], ph, " / ".join(bad)))

print()
print("=== 音标为空 / 缺失的条目 ===")
for w in ws:
    if not w.get("phonetic", "").strip():
        print("  ", w["word"])
