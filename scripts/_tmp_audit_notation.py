# -*- coding: utf-8 -*-
"""统计音标里的记法使用情况 + 找可疑的「两个主重音」。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))


def cnt(pred):
    return sum(1 for w in ws if pred(w.get("phonetic", "")))


print("总条数                =", len(ws))
print("含 ASCII 单引号 '     =", cnt(lambda p: "'" in p))
print("含 IPA 主重音  ́      =", cnt(lambda p: "\u02c8" in p))
print("含 ASCII 逗号 ,       =", cnt(lambda p: "," in p))
print("含 IPA 次重音 ˌ        =", cnt(lambda p: "\u02cc" in p))
print("含 ASCII 冒号 :       =", cnt(lambda p: ":" in p))
print("含 IPA 长音 ː         =", cnt(lambda p: "\u02d0" in p))

print()
print("=== 可疑：同一音标里出现 >=2 个主重音记号 ===")
for w in ws:
    p = w.get("phonetic", "")
    if len(re.findall(r"[\u02c8']", p)) >= 2:
        print("  %-24s %s" % (w["word"], p))

print()
print("=== 可疑：音标以 ASCII 单引号或逗号开头（包裹/记法脏）===")
for w in ws:
    p = w.get("phonetic", "").strip()
    if re.match(r"^[/\[]\s*['“,]", p):
        print("  %-24s %s" % (w["word"], p))
