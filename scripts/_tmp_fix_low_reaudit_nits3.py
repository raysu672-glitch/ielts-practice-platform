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

# #3：后步保留「此外」
s = by[3]
s["steps"][1]["chinese"] = (
    "此外，【患有相同疾病的】人们能够建立【在线】社区。"
)
s["steps"][2]["chinese"] = (
    "此外，患有相同疾病的人们能够建立在线社区，"
    "【在那里分享战胜疾病的励志故事以及有助于康复的实用信息】。"
)

# #103：步骤1 补「学生」，与 students 对齐
s = by[103]
s["steps"][0]["chinese"] = "要求学生穿校服有助于减轻同伴压力。"

# #112：enjoy great popularity（去不定冠词）
s = by[112]
old = "enjoy a great popularity"
new = "enjoy great popularity"
s["finalEnglish"] = s["finalEnglish"].replace(old, new)
for st in s["steps"]:
    st["correctAnswer"] = st["correctAnswer"].replace(old, new)
    if st.get("hint"):
        st["hint"] = st["hint"].replace(old, new)

HTML.write_text(
    html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
    encoding="utf-8",
)
print("fixed #3 #103 #112")
