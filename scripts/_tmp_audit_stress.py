# -*- coding: utf-8 -*-
"""检查主重音位置是否与词典一致（英式/美式重音偶有差异，只报明显错位）。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import eng_to_ipa as eipa  # noqa: E402

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

VOW = set("əɪʊɛɔæɒʌɑɜeiou")


def stress_pos(ph: str):
    t = ph.replace("dʒ", "J").replace("tʃ", "C").replace("ʤ", "J").replace("ʧ", "C")
    for mark in ("ˈ", "'"):
        i = t.find(mark)
        if i >= 0:
            return sum(1 for c in t[:i] if c in VOW)
    return None


def n_syll(ph: str) -> int:
    t = ph.replace("dʒ", "J").replace("tʃ", "C")
    return sum(1 for c in t if c in VOW)


rows = []
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) != 1 or "-" in word:
        continue
    ref = eipa.convert(word)
    if "*" in ref or not ref.strip():
        continue
    a, b = stress_pos(ph), stress_pos(ref)
    if a is None or b is None:
        continue
    if a != b:
        rows.append((abs(a - b), word, ph, ref, a, b, n_syll(ph)))

rows.sort(reverse=True)
print("=== 主重音位置与 CMUdict 不一致（%d 条）===" % len(rows))
print("说明：a=词表主重音前元音数，b=词典，diff 为偏差\n")
print("%-5s %-24s %-28s %-22s a  b  音节" % ("diff", "词", "词表", "CMUdict"))
print("-" * 100)
for d, word, ph, ref, a, b, sy in rows:
    print("%-5d %-24s %-28s %-22s %-2d %-2d %d" % (d, word, ph, ref, a, b, sy))
