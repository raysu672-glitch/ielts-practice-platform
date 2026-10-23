#!/usr/bin/env python3
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
html = open("sources/juzifanyixin/index.html", encoding="utf-8").read()
m = re.search(r"const translationData = (\[[\s\S]*?\n\]);", html)
data = json.loads(m.group(1))
by = {s["id"]: s for s in data}
ids = [2, 3, 4, 8, 10, 12, 13, 47, 64, 69, 76, 77, 80, 81, 88, 103, 106, 108, 112, 113, 114]
for i in ids:
    s = by[i]
    print("=" * 60)
    print(f"#{i}")
    print("fullCN:", s["fullChinese"])
    print("fullEN:", s["finalEnglish"])
    for idx, st in enumerate(s["steps"], 1):
        print(f"  s{idx}: {st['chinese']}")
        print(f"       EN: {st['correctAnswer']}")
