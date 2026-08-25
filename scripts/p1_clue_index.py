# -*- coding: utf-8 -*-
"""Extract P1 clue word banks to JSON (no file overwrite)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_p1_clue_index.json"

# Load parse module without executing its write side effects
SRC = Path(r"G:\口语练习\_parse_p1_full.py")
code = SRC.read_text(encoding="utf-8")
# Strip the final write block
code = re.sub(
    r"# 生成 JS[\s\S]*$",
    "OUT_JSON = categories\n",
    code,
)
code = code.replace(
    "Path(r'G:\\口语练习\\_p1_extract_stats.txt').write_text",
    "# skip stats",
)
code = re.sub(
    r"Path\(r'G:\\口语练习\\_p1_extract_stats\.txt'\)\.write_text\([^)]+\)",
    "pass",
    code,
)
code = re.sub(
    r"Path\(r'D:\\ielts-practice-platform\\sources\\kouyulianxi\\p1-data\.js'\)\.write_text\([^)]+\)",
    "pass",
    code,
)
code = re.sub(
    r"Path\(r'G:\\口语练习\\_p1_extract_done\.txt'\)\.write_text\([^)]+\)",
    "pass",
    code,
)

ns: dict = {}
exec(compile(code, str(SRC), "exec"), ns)
categories = ns["categories"]


def norm_q(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("'", "'").replace("'", "'")
    return re.sub(r"[^a-z0-9]+", "", s)


index: dict[str, dict] = {}
by_cat: dict[str, dict[str, dict]] = {}
for cat in categories:
    by_cat.setdefault(cat["id"], {})
    for q in cat["questions"]:
        key = norm_q(q.get("q") or q.get("title") or "")
        if not key:
            continue
        entry = {
            "words": q["words"],
            "title": q.get("title"),
            "q": q.get("q"),
            "cat": cat["id"],
        }
        index[key] = entry
        by_cat[cat["id"]][key] = entry

OUT.write_text(
    json.dumps(
        {"index": index, "byCat": by_cat, "stats": {c["id"]: len(c["questions"]) for c in categories}},
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
print(f"clue questions={len(index)} -> {OUT}")
