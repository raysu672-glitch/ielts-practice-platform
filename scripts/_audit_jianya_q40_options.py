# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
CUT = re.compile(
    r"(?:Your dedicated|Facebook|Quick Links|elementor|wp-content|tidio|admin-ajax|simplyielts|prefetch|\{)",
    re.I,
)

for kd in sorted(ROOT.glob("academic*/keys/reading/*.json")):
    key = json.loads(kd.read_text(encoding="utf-8"))
    av = str((key.get("answers") or {}).get("40") or "")
    if not av:
        continue
    low = av.lower()
    if not any(x in low for x in ["ieltszone", "elementor", "wp-content", "tidio", "simplyielts", "your dedicated"]):
        continue
    m = CUT.search(av)
    cleaned = (av[: m.start()] if m else av).strip()
    paper_path = ROOT / kd.parts[-4] / "reading" / f"{kd.stem}.json"
    paper = json.loads(paper_path.read_text(encoding="utf-8"))
    q = next((x for x in paper["questions"] if x["number"] == 40), None)
    if not q:
        continue
    opts = [(o.get("value"), (o.get("label") or "")[:50]) for o in (q.get("options") or [])]
    print(kd.parts[-4], key.get("sId"), "ans=", cleaned, "type=", q.get("type"), "opts=", opts)

print("--- CLEAN C21 ---")
for kd in sorted((ROOT / "academic21" / "keys" / "reading").glob("*.json")):
    key = json.loads(kd.read_text(encoding="utf-8"))
    if "40" not in (key.get("answers") or {}):
        continue
    paper = json.loads((ROOT / "academic21" / "reading" / f"{kd.stem}.json").read_text(encoding="utf-8"))
    q = next(x for x in paper["questions"] if x["number"] == 40)
    print(
        "C21",
        key["sId"],
        key["answers"]["40"],
        q.get("type"),
        [(o.get("value"), (o.get("label") or "")[:30]) for o in (q.get("options") or [])],
    )
