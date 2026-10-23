# -*- coding: utf-8 -*-
"""One-off: extract curated Form A items for xinshengmodi."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_listening():
    t = (ROOT / "sources/daanjutingxieceshi/index.html").read_text(encoding="utf-8")
    m = re.search(r"ALL_QUESTIONS\s*=\s*(\[.*?\]);", t, re.S)
    qs = json.loads(m.group(1))
    # Prefer shorter originals for dictation (40–120 chars)
    picked = []
    for q in qs:
        o = (q.get("original") or "").strip()
        if 35 <= len(o) <= 110:
            picked.append({"id": f"L{q['id']}", "text": o})
        if len(picked) >= 8:
            break
    return picked


def load_reading():
    t = (ROOT / "sources/tongyitihuanceshi/index.html").read_text(encoding="utf-8")
    # Try common patterns
    for pat in [
        r"allQuestions\s*=\s*(\[.*?\]);",
        r"QUESTIONS\s*=\s*(\[.*?\]);",
        r"questionBank\s*=\s*(\[.*?\]);",
        r"const\s+data\s*=\s*(\[.*?\]);",
    ]:
        m = re.search(pat, t, re.S)
        if m:
            try:
                qs = json.loads(m.group(1))
                print("reading pattern", pat, "count", len(qs), "keys", qs[0].keys() if qs else None)
                return qs[:28]
            except Exception as e:
                print("fail", pat, e)
    # fallback: scan for objects with prompt/answer style
    print("reading html len", len(t))
    # look for array of {q, a} or similar near script
    idxs = [m.start() for m in re.finditer(r"options\s*:", t)]
    print("options: count", len(idxs))
    # Try tongyitihuan learning data
    learn = ROOT / "sources/tongyitihuan"
    for p in learn.rglob("*.json"):
        print("json", p)
    for p in learn.rglob("*.js"):
        print("js", p.name, p.stat().st_size)
    return []


def load_phrase():
    t = (ROOT / "sources/xiezuocihuoceshi/index.html").read_text(encoding="utf-8")
    # foundationVocab often array of {chinese, english} or similar
    m = re.search(r"foundationVocab\s*=\s*(\[.*?\]);", t, re.S)
    if not m:
        m = re.search(r"getAllVocab[\s\S]{0,200}?return\s+(\[)", t)
    print("phrase foundation", bool(m))
    # Find objects with chinese/english
    items = re.findall(
        r'\{\s*"?chinese"?\s*:\s*"([^"]+)"\s*,\s*"?english"?\s*:\s*"([^"]+)"',
        t,
    )
    if not items:
        items = re.findall(
            r"chinese:\s*'([^']+)'\s*,\s*english:\s*'([^']+)'",
            t,
        )
    if not items:
        items = re.findall(
            r'chinese:\s*"([^"]+)"[\s\S]{0,80}?english:\s*"([^"]+)"',
            t,
        )
    print("phrase pairs", len(items))
    out = []
    for i, (cn, en) in enumerate(items[:10]):
        out.append({"id": f"P{i+1}", "prompt": cn, "answer": en})
    return out


def load_translate():
    td = json.loads((ROOT / "sources/juzifanyixin/translation_data.json").read_text(encoding="utf-8"))
    print("translate type", type(td).__name__)
    items = []
    if isinstance(td, list):
        src = td
    elif isinstance(td, dict):
        src = []
        for v in td.values():
            if isinstance(v, list):
                src.extend(v)
            elif isinstance(v, dict) and "sentences" in v:
                src.extend(v["sentences"])
    else:
        src = []
    print("translate src", len(src), "sample keys", src[0].keys() if src and isinstance(src[0], dict) else src[:1])
    for i, s in enumerate(src[:5]):
        if isinstance(s, dict):
            en = s.get("en") or s.get("english") or s.get("sentence") or s.get("src") or ""
            zh = s.get("zh") or s.get("chinese") or s.get("translation") or s.get("answer") or ""
            items.append({"id": f"T{i+1}", "en": en, "zh": zh})
    return items


def main():
    L = load_listening()
    print("L", len(L), L[0] if L else None)
    R = load_reading()
    print("R", len(R))
    P = load_phrase()
    print("P", P[:2])
    T = load_translate()
    print("T", T[:2])


if __name__ == "__main__":
    main()
