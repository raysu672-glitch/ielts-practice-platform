# -*- coding: utf-8 -*-
"""辅音骨架比对 + 字面字母残留检查 —— 抓「辅音被替换/丢失」类错误。"""
import difflib
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import eng_to_ipa as eipa  # noqa: E402

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

VOWEL = set("aeiouæɑɒɔəɜʌɪʊɛɐɘɵːˈˌ()/[]'’,;.- ")
MULTI = [("dʒ", "J"), ("ʤ", "J"), ("tʃ", "C"), ("ʧ", "C"), ("ɡ", "g")]


def cons_only(s: str, drop_r: bool = True) -> str:
    t = s
    for a, b in MULTI:
        t = t.replace(a, b)
    out = [c for c in t if c not in VOWEL]
    if drop_r:
        out = [c for c in out if c != "r"]
    return "".join(out)


print("=== ① 音标里残留「字面字母组合」（IPA 中不应出现）===")
LETTERS = ["th", "sh", "ch", "ph", "ck", "ng", "qu", "wh", "ee", "oo", "ea", "ou", "ai"]
for w in ws:
    ph = w.get("phonetic", "")
    core = re.sub(r"[ˈˌ:/\[\]()'’,.-]", "", ph)
    hits = [g for g in LETTERS if g in core]
    if hits:
        print("  %-22s %-30s %s" % (w["word"], ph, " ".join(hits)))

print()
print("=== ② 辅音骨架与 CMUdict 不一致（忽略 r）===")
rows = []
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    ref = eipa.convert(word)
    if "*" in ref or not ref.strip():
        continue
    ca, cb = cons_only(ph), cons_only(ref)
    if not ca or not cb:
        continue
    r = difflib.SequenceMatcher(None, ca, cb).ratio()
    if r < 0.8:
        rows.append((r, word, ph, ref, ca, cb))

rows.sort()
print("  共 %d 条（按相似度升序，前 60）\n" % len(rows))
print("%-6s %-24s %-28s %-22s %s" % ("相似度", "词", "词表音标", "CMUdict", "辅音差异"))
print("-" * 118)
for r, word, ph, ref, ca, cb in rows[:60]:
    print("%-6.2f %-24s %-28s %-22s %s -> %s" % (r, word, ph, ref, ca, cb))

Path("_tmp_cons_rows.txt").write_text(
    "\n".join("%.3f\t%s\t%s\t%s\t%s\t%s" % t for t in rows), encoding="utf-8")

print()
print("=== ③ 专项：疑似 d → ɒ（ɒʒ / ɒr / ɒə 等组合）===")
for w in ws:
    ph = w.get("phonetic", "")
    if re.search(r"ɒʒ|ɒr|ɒə|ɒz", ph):
        print("  %-22s %-30s %s" % (w["word"], ph, w.get("meaning", "")))
