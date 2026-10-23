#!/usr/bin/env python3
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
html = open("sources/juzifanyixin/index.html", encoding="utf-8").read()
m = re.search(r"const translationData = (\[[\s\S]*?\n\]);", html)
data = json.loads(m.group(1))
by = {s["id"]: s for s in data}
for i in [47, 12, 114, 10, 2]:
    s = by[i]
    print("=" * 60, f"#{i}")
    print("fullCN:", s["fullChinese"])
    print("fullEN:", s["finalEnglish"])
    for idx, st in enumerate(s["steps"], 1):
        print(f"  s{idx} [{st.get('label','')}]:")
        print(f"    CN: {st['chinese']}")
        print(f"    EN: {st['correctAnswer']}")
