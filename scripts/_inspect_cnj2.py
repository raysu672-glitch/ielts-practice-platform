# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

text = Path("sources/changnanju/index.html").read_text(encoding="utf-8")

def extract_const(name):
    m = re.search(rf"const {name} = \[", text)
    if not m:
        m = re.search(rf"const {name} = \{{", text)
    start = m.end() - 1
    open_c = text[start]
    close_c = "}" if open_c == "{" else "]"
    depth = 0
    for i in range(start, len(text)):
        if text[i] == open_c:
            depth += 1
        elif text[i] == close_c:
            depth -= 1
            if depth == 0:
                return json.loads(re.sub(r",(\s*[\]}])", r"\1", text[start : i + 1]))

sents = extract_const("SENTENCES")
keys = extract_const("ANSWER_KEYS")

for num in [14, 25, 58]:
    s = next(x for x in sents if x["num"] == num)
    print("=== sentence", num)
    print("original:", s["original"])
    k = keys.get(str(num), keys.get(num))
    print("answer_keys count:", len(k) if k else 0)
    if k:
        for i, item in enumerate(k[:8]):
            print(f"  key{i}: raw={item.get('raw')}")
