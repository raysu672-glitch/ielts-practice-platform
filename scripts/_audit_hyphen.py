#!/usr/bin/env python3
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"D:/ielts-practice-platform/sources")
files = [
    ("写作词伙", ROOT / "xiezuocihuo/categories.js"),
    ("写作词伙测试", ROOT / "xiezuocihuoceshi/index.html"),
    ("听力模块", ROOT / "tinglidanciceshi/js/modules.js"),
]

# adjective + participle/adj without -ly (high-confidence subset)
bad = re.compile(
    r"\b(financial|economic|social|environment)-"
    r"(disadvantaged|motivated|oriented|related|connected|dependent|"
    r"conscious|aware|friendly|sensitive|active|engaged|involved|"
    r"acceptable|responsible|sustainable)\b",
    re.I,
)

for mod, fp in files:
    text = fp.read_text(encoding="utf-8")
    for m in bad.finditer(text):
        ln = text.count("\n", 0, m.start()) + 1
        print(f"{mod} | {fp.name}:{ln} | {m.group()} | {m.group(1).lower()}ly {m.group(2).lower()} | 副词缺-ly")

print("done")
