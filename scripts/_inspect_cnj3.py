# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

text = Path("sources/changnanju/index.html").read_text(encoding="utf-8")

def extract_const(name):
    m = re.search(rf"const {name} = ", text)
    start = text.index("[", m.start()) if name == "SENTENCES" else text.index("{", m.start())
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

keys = extract_const("ANSWER_KEYS")
for num in [14, 25, 58]:
    k = keys[str(num)]
    print("===", num)
    for i, item in enumerate(k):
        print(f"  {i}: en={item.get('en')} cn={item.get('cn')} raw={item.get('raw')!r}")

# scan all sentences for broken original English
sents = extract_const("SENTENCES")
issues = []
for s in sents:
    orig = s.get("original", "")
    # comma splice / missing verb patterns
    if re.search(r"University,\s+[A-Z][a-z]+'?s story proves", orig):
        issues.append((s["num"], "疑似缺谓语/断句", orig))
    if re.search(r"\bPedeleose\b", orig):
        issues.append((s["num"], "Pedeleose 专名疑似 OCR 错", orig))
print("\nchangnanju orig issues:", issues)
