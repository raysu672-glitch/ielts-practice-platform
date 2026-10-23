#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HTML = Path("sources/juzifanyixin/index.html")
html = HTML.read_text(encoding="utf-8")
m = re.search(r"(const translationData = )(\[[\s\S]*?\n\]);", html)
data = json.loads(m.group(2))
by = {s["id"]: s for s in data}

# #80 gossips → gossip
s = by[80]
old, new = "sharing gossips and pictures", "sharing gossip and pictures"
s["finalEnglish"] = s["finalEnglish"].replace(old, new)
for st in s["steps"]:
    st["correctAnswer"] = st["correctAnswer"].replace(old, new)
    if st.get("hint"):
        st["hint"] = st["hint"].replace(old, new)

# #112 set up → form（构成屏障）
s = by[112]
for old, new in [
    ("set up a natural barrier", "form a natural barrier"),
    ("set up a barrier", "form a barrier"),
]:
    s["finalEnglish"] = s["finalEnglish"].replace(old, new)
    for st in s["steps"]:
        st["correctAnswer"] = st["correctAnswer"].replace(old, new)
        if st.get("hint"):
            st["hint"] = st["hint"].replace(old, new)

HTML.write_text(
    html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
    encoding="utf-8",
)
print("fixed #80 #112")
print("#80:", by[80]["finalEnglish"])
print("#112:", by[112]["finalEnglish"])
