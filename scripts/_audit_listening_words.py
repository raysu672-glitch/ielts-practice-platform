#!/usr/bin/env python3
import re, json
from pathlib import Path

for name in ["listening_basic.html", "listening.html"]:
    fp = Path(r"D:/ielts-practice-platform/sources/tinglidanciceshi") / name
    text = fp.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", text, re.DOTALL)
    if not m:
        print(name, "no match")
        continue
    words = json.loads(m.group(1))
    print(f"\n=== {name} ({len(words)} words) ===")
    keywords = ["golf", "court", "course", "plant", "plane", "science", "privacy", "decrement"]
    for w in words:
        wl = w["word"].lower()
        if any(k in wl for k in keywords):
            print(w)

# Check allWordsListeningBasic for golf etc
mod = Path(r"D:/ielts-practice-platform/sources/tinglidanciceshi/js/modules.js").read_text(encoding="utf-8")
m = re.search(r'var allWordsListeningBasic = (\[.*?\]);', mod, re.DOTALL)
if m:
    basic = json.loads(m.group(1).replace("'", '"'))
    hits = [x for x in basic if any(k in x.lower() for k in ["golf", "plant science", "plane", "court"])]
    print("\n=== allWordsListeningBasic hits ===")
    for h in hits:
        print(h)
