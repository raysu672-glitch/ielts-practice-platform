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

patterns = [
    (r"University,\s+[A-Z][a-z]+'?s story proves", "同位语断句错误，缺 says/ argues 等谓语"),
    (r"\bPedeleose\b", "Pedeleose 专名疑似错误"),
    (r"\bteh\b", "teh"),
    (r"\brecieve\b", "recieve"),
    (r"\boccured\b", "occured"),
    (r"\benviroment\b", "enviroment"),
]
for s in sents:
    orig = s.get("original", "")
    for pat, msg in patterns:
        if re.search(pat, orig, re.I):
            print(f"句{s['num']}: {msg}")
            print(f"  {orig[:180]}")
            print()
