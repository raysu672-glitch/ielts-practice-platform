# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_js_array(text, name):
    m = re.search(rf"{name}\s*=\s*\[", text)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    for j in range(i, len(text)):
        c = text[j]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                raw = text[i : j + 1]
                # convert JS object literals loosely
                fixed = raw
                fixed = re.sub(r"(\{|\,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', fixed)
                fixed = fixed.replace("'", '"')
                # trailing commas
                fixed = re.sub(r",\s*}", "}", fixed)
                fixed = re.sub(r",\s*]", "]", fixed)
                try:
                    return json.loads(fixed)
                except Exception as e:
                    print("parse fail", name, e)
                    print(fixed[:400])
                    return None
    return None


def reading_items():
    t = (ROOT / "sources/tongyitihuanceshi/index.html").read_text(encoding="utf-8")
    (ROOT / "_tmp_syn_head.txt").write_text(t[:3000], encoding="utf-8")
    # find fetch or embedded
    for name in ["allGroups", "groups", "questions", "ITEMS", "DATA", "bank"]:
        arr = extract_js_array(t, name)
        if arr:
            print("found", name, len(arr))
            return arr
    # look in tongyitihuan
    for p in (ROOT / "sources/tongyitihuan").rglob("*"):
        if p.suffix in {".js", ".json", ".html"} and p.stat().st_size < 5_000_000:
            print("file", p.relative_to(ROOT), p.stat().st_size)
    return []


def phrase_items():
    t = (ROOT / "sources/xiezuocihuoceshi/index.html").read_text(encoding="utf-8")
    arr = extract_js_array(t, "foundationVocab")
    print("foundation", len(arr) if arr else None)
    if arr:
        print(arr[0])
    return (arr or [])[:10]


def main():
    reading_items()
    phrase_items()
    td = json.loads((ROOT / "sources/juzifanyixin/translation_data.json").read_text(encoding="utf-8"))
    print("T0", td[0]["fullChinese"][:40], "|", td[0]["finalEnglish"][:60])


if __name__ == "__main__":
    main()
