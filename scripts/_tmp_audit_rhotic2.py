# -*- coding: utf-8 -*-
"""对比两个词表的 rhotic（儿化）风格。"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for f in ["listening_basic.html", "listening.html"]:
    ws = json.loads(re.search(
        r"const ALL_WORDS = (\[[\s\S]*?\]);",
        io.open("sources/tinglidanciceshi/" + f, encoding="utf-8").read(),
    ).group(1))

    def n(pred):
        return sum(1 for w in ws if pred(w.get("phonetic", "")))

    print("### %s（%d 词）" % (f, len(ws)))
    print("  (r) 形式（英式）        :", n(lambda p: "(r)" in p))
    print("  ər 结尾（美式儿化）     :", n(lambda p: re.search(r"ər/?\]?$", p)))
    print("  ə(r) 结尾（英式）       :", n(lambda p: re.search(r"ə\(r\)/?\]?$", p)))
    print("  ɑːr/ɔːr/ɜːr（儿化）     :", n(lambda p: re.search(r"[ɑɔɜ]ːr", p)))
    print("  ɪr/ɛr/ʊr（儿化）        :", n(lambda p: re.search(r"[ɪɛʊ]r", p)))
    print("  ær（美式）              :", n(lambda p: "ær" in p))
    print()
