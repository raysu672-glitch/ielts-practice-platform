# -*- coding: utf-8 -*-
"""元音骨架比对：检查元音选用是否与词典严重不符（辅音已单独查过）。"""
import difflib
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

MULTI = [("dʒ", "J"), ("ʤ", "J"), ("tʃ", "C"), ("ʧ", "C"), ("ɡ", "g")]
# 元音归一化：抹平英式/美式
VMAP = {
    "əʊ": "O", "oʊ": "O", "əu": "O", "ou": "O", "o": "O",
    "aɪ": "Y", "ai": "Y", "ʌɪ": "Y",
    "aʊ": "W", "au": "W",
    "eɪ": "E", "ei": "E",
    "ɔɪ": "Q", "oi": "Q",
    "ɪə": "R", "iə": "R", "eə": "R", "ɛə": "R", "ʊə": "R",
    "ɑː": "A", "ɑ:": "A", "ɒː": "A", "ɒ": "A", "ɔː": "A", "ɔ:": "A", "ɑ": "A",
    "ɜː": "U", "ɜ:": "U", "ɜ": "U", "ʌ": "U", "ə": "U",
    "iː": "I", "i:": "I", "ɪ": "I", "i": "I",
    "uː": "V", "u:": "V", "ʊ": "V", "u": "V",
    "e": "X", "ɛ": "X", "æ": "X", "a": "X",
}
VOWELS = "əɪʊɛɔæɒʌɑɜeiou"
STRIP = set("ˈˌ/[]()'’,;.- ː:")


def vseq(s: str) -> str:
    t = s
    for a, b in MULTI:
        t = t.replace(a, b)
    t = t.strip().strip("/[]")
    out = []
    i = 0
    while i < len(t):
        ch = t[i]
        if ch in STRIP:
            i += 1
            continue
        two = t[i:i + 2]
        if two in VMAP:
            out.append(VMAP[two])
            i += 2
            continue
        if ch in VMAP:
            out.append(VMAP[ch])
        i += 1
    return "".join(out)


rows = []
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) != 1 or "-" in word:
        continue
    ref = eipa.convert(word)
    if "*" in ref or not ref.strip():
        continue
    a, b = vseq(ph), vseq(ref)
    if not a or not b:
        continue
    r = difflib.SequenceMatcher(None, a, b).ratio()
    rows.append((r, word, ph, ref, a, b))

rows.sort()
print("可比对 %d 条；元音骨架相似度 < 0.6 的：\n" % len(rows))
print("%-6s %-24s %-30s %-22s %-10s %s" % ("相似度", "词", "词表", "CMUdict", "词表元音", "词典元音"))
print("-" * 108)
n = 0
for r, word, ph, ref, a, b in rows:
    if r < 0.6:
        n += 1
        print("%-6.2f %-24s %-30s %-22s %-10s %s" % (r, word, ph, ref, a, b))
print("\n小计 %d 条" % n)
