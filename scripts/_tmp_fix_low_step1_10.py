#!/usr/bin/env python3
"""#10 step1 中文无「各类」，英文回退为 the equipment。"""
import json
import re
from pathlib import Path

HTML = Path("sources/juzifanyixin/index.html")
html = HTML.read_text(encoding="utf-8")
m = re.search(r"(const translationData = )(\[[\s\S]*?\n\]);", html)
data = json.loads(m.group(2))
s = next(x for x in data if x["id"] == 10)
s["steps"][0]["correctAnswer"] = (
    "Therefore, it is important that children learn to use the equipment."
)
# keywords for step1 if any mention various — leave later steps alone
HTML.write_text(
    html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
    encoding="utf-8",
)
print("ok #10 s1:", s["steps"][0]["correctAnswer"])
