# -*- coding: utf-8 -*-
"""听力基础词汇音标全量结构体检。

不依赖外部词典，只检查「结构上不可能正确」的问题：
  1. 非预期字符（IPA 之外的可疑字符）
  2. 包裹符号不配对 / 缺斜杠
  3. 重音记号缺失或位置可疑
  4. 空白异常（首尾空格、连续空格、斜杠内侧空格）
  5. 括号不配对
  6. 音节无元音 / 元音过多
  7. 词与音标长度比例异常（可发现「音标属于别的词」）
"""
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML = Path("sources/tinglidanciceshi/listening_basic.html")
words = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open(HTML, encoding="utf-8").read()).group(1))

# 允许出现的字符：ASCII 可见 + 常用 IPA
ASCII_OK = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/[]()'’,;.- ")
IPA_OK = set("əɪʊɛɔæɒʌʒʃθðŋˈˌɑɜːɡʤʧ")

VOY = set("əɪʊɛɔæɒʌɑɜeiouː")   # 元音类符号


def issues(w):
    word, ph = w["word"], w.get("phonetic", "")
    bad = []

    if not ph.strip():
        return ["音标为空"]

    # 1. 非预期字符
    for ch in ph:
        if ch not in ASCII_OK and ch not in IPA_OK:
            bad.append("异常字符 U+%04X(%s) %s" % (ord(ch), ch, unicodedata.name(ch, "?")))

    # 2. 包裹符号
    body = ph.strip()
    if body[0] in "/[" and body[-1] in "/]":
        pass
    elif "/" in body or "[" in body:
        bad.append("包裹符号不配对")

    # 3. 重音记号
    has_stress = "ˈ" in ph or "ˌ" in ph
    syllables = len(re.findall(r"[%s]" % re.escape("".join(VOY)), ph))
    if syllables >= 3 and not has_stress:
        bad.append("多音节(%d)但无重音记号" % syllables)
    if re.search(r"[bcdfghjklmnpqrstvwxz]ˈ[bcdfghjklmnpqrstvwxz]", ph):
        bad.append("重音记号夹在两辅音之间")

    # 4. 空白
    if ph != ph.strip():
        bad.append("首尾有空格")
    if "  " in ph:
        bad.append("连续空格")
    if re.search(r"/\s", ph) or re.search(r"\s/", ph):
        bad.append("斜杠内侧有空格")

    # 5. 括号
    if ph.count("(") != ph.count(")"):
        bad.append("括号不配对")
    if ph.count("/") not in (0, 2) and "[" not in ph:
        bad.append("斜杠数异常(%d)" % ph.count("/"))

    # 6. 元音
    if syllables == 0 and len(re.sub(r"[^a-zA-Z]", "", ph)) > 2:
        bad.append("无元音")
    if syllables > max(8, len(word.replace(" ", "").replace("'", ""))):
        bad.append("元音数(%d)远超词长" % syllables)

    # 7. 长度比例
    letters = len(re.sub(r"[^a-zA-Z]", "", word))
    phones = len(re.sub(r"[^a-zA-Zəɪʊɛɔæɒʌʒʃθðŋɡʤʧ]", "", ph))
    if letters >= 4 and phones >= 4:
        ratio = letters / phones
        if ratio > 3.0 or ratio < 0.4:
            bad.append("词/音标长度比例异常 %.2f (%d字母:%d音素)" % (ratio, letters, phones))

    return bad


print("=== 全量结构体检：%d 条 ===\n" % len(words))
flagged = []
for w in words:
    b = issues(w)
    if b:
        flagged.append((w["word"], w.get("phonetic", ""), b))

print("命中 %d 条（%.1f%%）\n" % (len(flagged), len(flagged) / len(words) * 100))

# 按问题类型汇总
kinds = Counter()
for _, _, b in flagged:
    for x in b:
        kinds[re.sub(r"\(.*?\)|U\+[0-9A-F]+ \([^)]*\)|\d+", "", x).strip()] += 1
print("=== 问题类型分布 ===")
for k, n in kinds.most_common():
    print("  %-32s %d" % (k, n))

print()
print("=== 明细（全部）===")
for word, ph, b in flagged:
    print("  %-26s %-30s %s" % (word, ph, " / ".join(b)))
