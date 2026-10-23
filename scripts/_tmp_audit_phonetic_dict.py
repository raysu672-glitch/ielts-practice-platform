# -*- coding: utf-8 -*-
"""用 CMUdict(eng_to_ipa) 与词表音标做骨架比对，找出「音标与单词不匹配」的条目。

英式/美式差异（ɒ/ɑ、əʊ/oʊ、rhotic 的 r、长短音）先归一化掉，
再看两者的音素骨架相似度。相似度极低 => 音标很可能属于另一个词。
"""
import difflib
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import eng_to_ipa as eipa  # noqa: E402

HTML = Path("sources/tinglidanciceshi/listening_basic.html")
words = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open(HTML, encoding="utf-8").read()).group(1))

# 多字符音素先替换成单字符占位，再归一化
MULTI = [("əʊ", "1"), ("oʊ", "1"), ("əu", "1"), ("aɪ", "2"), ("aʊ", "3"),
         ("eɪ", "4"), ("ɔɪ", "5"), ("ɪə", "6"), ("eə", "7"), ("ʊə", "8"),
         ("dʒ", "J"), ("ʤ", "J"), ("tʃ", "C"), ("ʧ", "C")]

# 归一化：抹平英式/美式与记法差异
NORM = {
    "ː": "", ":": "", "ˈ": "", "ˌ": "", " ": "", "/": "", "[": "", "]": "",
    "ɒ": "ɑ", "ɔ": "ɑ", "ɒ": "ɑ", "o": "ɑ",
    "ɜ": "ə", "ʌ": "ə", "ə": "ə",
    "ɪ": "i", "i": "i", "ɛ": "e", "ε": "e", "e": "e", "æ": "a",
    "ʊ": "u", "u": "u",
    "ɡ": "g", "ʒ": "ʒ", "ʃ": "ʃ", "θ": "θ", "ð": "ð", "ŋ": "ŋ",
    "r": "", "(": "", ")": "", "'": "", "’": "", "-": "", ".": "",
    "ɑ": "ɑ", "a": "a",
}


def skeleton(s: str) -> str:
    t = s
    for a, b in MULTI:
        t = t.replace(a, b)
    out = []
    for ch in t:
        # 未在 NORM 里列出的字符（普通辅音等）保留原样，只有显式映射为 "" 的才丢弃
        v = NORM[ch] if ch in NORM else ch
        if v:
            out.append(v)
    return "".join(out)


def sim(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


rows = []
failed = []
for w in words:
    word, ph = w["word"], w.get("phonetic", "")
    ref = eipa.convert(word)
    if "*" in ref or not ref.strip():
        failed.append(word)
        continue
    s_a, s_b = skeleton(ph), skeleton(ref)
    r = sim(s_a, s_b)
    rows.append((r, word, ph, ref, s_a, s_b))

rows.sort()

print("=== 自检：拿几个显然正确的词确认流程无误 ===")
for probe in ["bike", "cable", "family", "complex", "flute"]:
    for r, word, ph, ref, sa, sb in rows:
        if word == probe:
            print("  %-12s 相似度 %.2f  词表骨架=%-16s 词典骨架=%s" % (word, r, sa, sb))
            break

print()
print("词典可比对 %d 条；CMUdict 未收录 %d 条\n" % (len(rows), len(failed)))

for thr, label in [(0.34, "极低（几乎肯定是别的词）"), (0.5, "低（高度可疑）"), (0.65, "偏低（需人工看）")]:
    n = sum(1 for r, *_ in rows if r < thr)
    print("  相似度 < %.2f  %-28s %d 条" % (thr, label, n))

print()
print("=== 相似度 < 0.5 的条目 ===")
print("%-6s %-24s %-28s %s" % ("相似度", "词", "词表音标", "CMUdict"))
print("-" * 104)
for r, word, ph, ref, sa, sb in rows:
    if r < 0.5:
        print("%-6.2f %-24s %-28s %s" % (r, word, ph, ref))

print()
print("=== CMUdict 未收录（%d 条，前 40）===" % len(failed))
print("  " + ", ".join(failed[:40]))

if failed:
    Path("_tmp_cmudict_failed.txt").write_text("\n".join(failed), encoding="utf-8")
Path("_tmp_low_sim.txt").write_text(
    "\n".join("%.3f\t%s\t%s\t%s" % (r, w, p, ref) for r, w, p, ref, _, _ in rows),
    encoding="utf-8")
print("\n明细已写入 _tmp_low_sim.txt")
