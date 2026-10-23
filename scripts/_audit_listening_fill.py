# -*- coding: utf-8 -*-
"""Find listening answers that duplicate words already outside the blank."""
import json, re
from pathlib import Path

text = Path("sources/daanjutingxie/index.html").read_text(encoding="utf-8")
m = re.search(r"const GROUPS = \[", text)
start = m.end() - 1
depth = 0
for i in range(start, len(text)):
    if text[i] == "[":
        depth += 1
    elif text[i] == "]":
        depth -= 1
        if depth == 0:
            data = json.loads(re.sub(r",(\s*[\]}])", r"\1", text[start : i + 1]))
            break

items = [q for g in data for q in g]
for q in items:
    blank = q["blank"]
    ans = q["answer"]
    if "______" not in blank:
        continue
    before, after = blank.split("______", 1)
    filled = before + ans + after
    para = q["paraphrase"]
    # normalize
    def n(s):
        return re.sub(r"\s+", " ", s.replace("—", "-").replace("–", "-")).strip().lower()

    if n(filled) != n(para):
        # check if answer contains words from after-part incorrectly
        after_words = re.findall(r"[a-zA-Z']+", after.lower())
        ans_lower = ans.lower()
        overlap = [w for w in after_words if len(w) > 3 and w in ans_lower]
        if overlap or " / " in ans:
            print(f"id{q['id']}: ans={ans!r}")
            print(f"  blank_after={after[:60]!r}")
            print(f"  para={para[:100]}")
            print(f"  filled={filled[:100]}")
            print()
