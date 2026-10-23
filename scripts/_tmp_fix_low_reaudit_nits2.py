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

# #76：步骤1 去掉「颇具」，留给步骤2 与 rather 同步
by[76]["steps"][0]["chinese"] = "学习外语有难度。"

# #81：fullChinese 与末步「因为」对齐（去掉「这不仅」）
by[81]["fullChinese"] = (
    "精心规划假期旅行至关重要，因为这能帮助人们节省开支，还能让假期过得更加愉快。"
)

HTML.write_text(
    html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
    encoding="utf-8",
)
print("fixed #76 #81")
