# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

text = Path("sources/changnanju/index.html").read_text(encoding="utf-8")
m = re.search(r"const SENTENCES = \[", text)
start = m.end() - 1
depth = 0
for i in range(start, len(text)):
    if text[i] == "[":
        depth += 1
    elif text[i] == "]":
        depth -= 1
        if depth == 0:
            sents = json.loads(re.sub(r",(\s*[\]}])", r"\1", text[start : i + 1]))
            break

for num in [14, 25, 58]:
    s = next(x for x in sents if x["num"] == num)
    print("=== sentence", num)
    print("original:", s["original"][:200])
    for bi, box in enumerate(s["challenge1"]["boxes"], 1):
        ans = box.get("answer")
        print(f"  box{bi}: title={box.get('title')} answer={ans!r}")
