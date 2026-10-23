# -*- coding: utf-8 -*-
"""预览：把 listening_basic 的音标按英式非儿化规范化（对齐 listening.html）。仅预览。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ws = json.loads(re.search(
    r"const ALL_WORDS = (\[[\s\S]*?\]);",
    io.open("sources/tinglidanciceshi/listening_basic.html", encoding="utf-8").read(),
).group(1))

VOW = set("aæeioəɪʊɛɒʌɑɔɜu")


def rhotic(ph: str) -> str:
    n = len(ph)
    out = []
    i = 0
    while i < n:
        # 已是英式 (r)，整段跳过，避免被二次处理
        if ph[i] == "(" and i + 2 < n and ph[i + 1] == "r" and ph[i + 2] == ")":
            out.append("(r)")
            i += 3
            continue
        ch = ph[i]
        if ch != "r":
            out.append(ch)
            i += 1
            continue
        nxt = ph[i + 1] if i + 1 < n else ""
        prev = ph[i - 1] if i > 0 else ""
        if nxt in VOW:
            out.append("r")          # r 在元音前才发音（英式）
        elif prev == "ə":
            if nxt in ("/", "]", "", " "):
                out.append("(r)")    # 词尾 -er/-or/-ar
            # 否则丢弃（如 advisors 的中缀 r）
        elif prev in "ɪɛʊ":
            out.append("ə")          # beer/bear 类：ɪr/ɛr/ʊr -> ɪə/eə/ʊə
        # 其余（ɑːr/ɔːr/ɜːr + 辅音）直接删 r
        i += 1
    return "".join(out)


changed = []
for w in ws:
    old = w.get("phonetic", "")
    new = rhotic(old)
    if new != old:
        changed.append((w["word"], old, new))

print("需规范 %d 条\n" % len(changed))
for word, old, new in changed:
    print("  %-26s %-30s -> %s" % (word, old, new))
