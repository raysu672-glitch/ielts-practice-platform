import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

text = (ROOT / "sources/tinglidanciceshi/listening_basic.html").read_text(encoding="utf-8")
entries = json.loads(re.search(r"const ALL_WORDS = (\[.*?\]);", text, re.S).group(1))
checks = [
    "alarming system", "animals behavior", "golf court", "advance level",
    "children mind", "political man", "privacy company", "plane science",
    "personal officer", "pet meat", "weathers", "hairs", "finance market",
    "families life", "culture awareness", "bottle water", "free pick",
    "repaired cost", "study skill", "cooperation loan", "triangle sharp",
    "firework", "eye contacts", "biological fishing", "economics history",
    "environment damage", "banana ride", "piano life", "waterpower",
    "micro-radiogram", "statement position", "objective matters",
    "note system", "cheapest budget", "compulsory and regular", "academic",
    "achievement", "acknowledgement", "china stone", "greenfield",
    "attack humans", "time consuming", "driving license", "defense",
    "bottle tops", "double-grill", "self-centered", "finance office",
    "research finding", "regular exercises", "textbooks allowance",
    "view shelter", "viewing shelter", "culture context", "fireplaces",
    "reinvest", "prevalent", "vetting", "unsocial", "undersea world",
]
print("=== listening_basic flagged words ===")
for c in checks:
    for e in entries:
        if e["word"].lower() == c.lower():
            print("%s | %s" % (e["word"], e.get("meaning", "")))
            break

text2 = (ROOT / "sources/tinglidanciceshi/listening.html").read_text(encoding="utf-8")
entries2 = json.loads(re.search(r"const ALL_WORDS = (\[.*?\]);", text2, re.S).group(1))
print("\n=== listening.html sample ===")
for w in [
    "Rafael", "Patterson", "living room", "living", "room", "artificial",
    "intelligence", "hacking", "lost", "found", "aid", "present", "flat",
    "mouse", "coach", "note", "half", "social", "plans", "changing",
    "areas", "medical", "behaviour", "labour", "nutrition", "network",
    "colony", "evolution", "victory", "view", "habit", "custom", "trend",
    "refreshment", "computer", "program", "application",
]:
    for e in entries2:
        if e["word"].lower() == w.lower():
            print("%s | %s" % (e["word"], e["meaning"]))
            break

text3 = (ROOT / "sources/tinglidanciceshi/js/modules.js").read_text(encoding="utf-8")
words = json.loads(re.search(r"var allWords = (\[.*?\]);", text3).group(1))
c = Counter(x.lower() for x in words)
print("\n=== allWords duplicates ===")
for w, n in sorted(c.items()):
    if n > 1:
        print("%s: %d" % (w, n))
print("total=%d unique=%d" % (len(words), len(c)))

basic = json.loads(re.search(r"var allWordsListeningBasic = (\[.*?\]);", text3).group(1))
cb = Counter(x.lower() for x in basic)
print("\n=== basic duplicates ===")
for w, n in sorted(cb.items()):
    if n > 1:
        print("%s: %d" % (w, n))
print("total=%d unique=%d" % (len(basic), len(cb)))
