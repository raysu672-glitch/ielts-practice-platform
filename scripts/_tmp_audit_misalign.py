# -*- coding: utf-8 -*-
"""抓「音标串位」：音标的分段数/长度与单词严重不符。"""
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

VOW = set("əɪʊɛɔæɒʌɑɜeiou")
IPA = "əɪʊɛɔæɒʌɜɑʒʃθðŋɡʤʧˈˌ:ː"
CLEAN = re.compile(r"[^a-zA-Z" + IPA + r"]")


def segs(s: str) -> list[str]:
    body = s.strip().strip("/[]")
    # 重音记号前的空格是排版风格，不算分段
    body = body.replace(" ˈ", "ˈ").replace(" ˌ", "ˌ")
    return [x for x in re.split(r"\s+", body.strip()) if x]


print("=== ① 音标分段数 ≠ 单词词数（疑似串位）===")
n = 0
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    nw = len(word.replace("-", " ").split())
    np_ = len(segs(ph))
    if nw != np_:
        n += 1
        print("  %-24s 词%d段 音标%d段  %s" % (word, nw, np_, ph))
print("  小计 %d 条" % n)

print()
print("=== ② 音标音素数 / 单词字母数 比例异常 ===")
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    letters = len(re.sub(r"[^a-zA-Z]", "", word))
    phones = len(CLEAN.sub("", ph.strip().strip("/[]").replace(" ", "")))
    if letters < 4 or phones < 3:
        continue
    ratio = phones / letters
    if ratio > 1.35 or ratio < 0.35:
        print("  %-24s %-30s %d字母/%d音素=%.2f" % (word, ph, letters, phones, ratio))

print()
print("=== ③ 音标里含空格但单词是单个词（反向）===")
for w in ws:
    word, ph = w["word"], w.get("phonetic", "")
    if len(word.split()) == 1 and len(segs(ph)) > 1:
        print("  %-24s %s" % (word, ph))

print()
print("=== ④ 同一音标被多个词共用（疑似复制粘贴）===")
from collections import defaultdict  # noqa: E402

m = defaultdict(list)
for w in ws:
    key = re.sub(r"\s+", "", w.get("phonetic", "").strip())
    if key:
        m[key].append(w["word"])
for k, v in m.items():
    if len(v) > 1:
        print("  %-30s <- %s" % (k, v))
