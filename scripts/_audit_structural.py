# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def parse(name, path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(rf"const\s+{name}\s*=\s*\[", text)
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return json.loads(re.sub(r",(\s*[\]}])", r"\1", text[start : i + 1]))

for mod, path, const in [
    ("learn", ROOT / "sources/daanjutingxie/index.html", "GROUPS"),
    ("test", ROOT / "sources/daanjutingxieceshi/index.html", "ALL_QUESTIONS"),
]:
    data = parse(const, path)
    items = [q for g in data for q in g] if isinstance(data[0], list) else data
    print(mod, "total", len(items))
    print("  empty_ans", [q["id"] for q in items if not (q.get("answer") or "").strip()])
    print("  bad_opts", [(q["id"], len(q.get("options") or [])) for q in items if len(q.get("options") or []) != 4])
    print("  dup", [q["id"] for q in items if len(set(o.strip().lower() for o in q.get("options") or [] if o)) < len([o for o in q.get("options") or [] if o])])
    bad_idx = []
    for q in items:
        ci = q.get("correct_idx")
        opts = q.get("options") or []
        ans = (q.get("answer") or "").strip()
        if ci is not None and opts:
            if ci < 0 or ci >= len(opts):
                bad_idx.append((q["id"], "oob"))
            elif ans and opts[ci].strip().lower() != ans.lower():
                bad_idx.append((q["id"], opts[ci], ans))
    print("  bad_idx", bad_idx)

sents = parse("SENTENCES", ROOT / "sources/changnanju/index.html")
empty = []
for s in sents:
    for key in ("challenge1", "challenge2"):
        ch = s.get(key)
        if not ch:
            continue
        for bi, box in enumerate(ch.get("boxes") or [], 1):
            if not (box.get("answer") or "").strip():
                empty.append((s["num"], key, bi))
print("changnanju sentences", len(sents), "empty boxes", empty)

text = (ROOT / "sources/xiezuocihuo/categories.js").read_text(encoding="utf-8")
vocab_count = len(re.findall(r"zh:\s*'", text))
print("xiezuocihuo vocab entries", vocab_count)

# translation empty
data = json.loads((ROOT / "sources/juzifanyixin/translation_data.json").read_text(encoding="utf-8"))
print("translation items", len(data))
print("  empty zh", [x["id"] for x in data if not (x.get("fullChinese") or "").strip()])
print("  empty en", [x["id"] for x in data if not (x.get("finalEnglish") or "").strip()])
