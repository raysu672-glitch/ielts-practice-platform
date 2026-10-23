# -*- coding: utf-8 -*-
"""统计英式(非儿化) vs 美式(儿化) 的 r 使用，找出混用情况。"""
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
    return [w["word"] for w in ws if pred(w.get("phonetic", ""))]


pats = {
    "以 ə(r) 结尾（英式）": r"ə\(r\)/?\]?$",
    "以 ər 结尾（美式儿化）": r"ər/?\]?$",
    "(r) 形式": r"\(r\)",
    "词尾裸 r（如 ɑːr/ ɔːr/ ɜːr/）": r"[ɑɔɜ]ːr[/\s]",
    "or/er/ar 元音后 r（如 ɔːr）": r"[ɑɔɜ]ːr",
    "ær（美式）": r"ær",
    "ɪr/ɛr/ʊr（美式）": r"[ɪɛʊ]r",
}
for label, pat in pats.items():
    hits = cnt(lambda p, pat=pat: re.search(pat, p))
    print("%-32s %3d 条  %s" % (label, len(hits), ", ".join(hits[:10])))

print()
print("=== 同一词根 r 处理不一致的示例（含 r 结尾词）===")
for w in ws:
    p = w.get("phonetic", "")
    if re.search(r"[ɑɔɜ]ːr", p) or re.search(r"ər/?\]?$", p):
        print("  %-24s %s" % (w["word"], p))
