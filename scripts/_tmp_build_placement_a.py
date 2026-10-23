# -*- coding: utf-8 -*-
"""Build sources/xinshengmodi/questions_a.js (Form A)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sources/xinshengmodi/questions_a.js"


def extract_js_array(text, name):
    m = re.search(rf"{name}\s*=\s*\[", text)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    in_str = None
    esc = False
    for j in range(i, len(text)):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
            continue
        if c in ("'", '"'):
            in_str = c
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                raw = text[i : j + 1]
                # JS → JSON-ish
                fixed = re.sub(
                    r"(?<=\{|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:",
                    r' "\1":',
                    raw,
                )
                fixed = re.sub(r"'", '"', fixed)
                fixed = re.sub(r",\s*}", "}", fixed)
                fixed = re.sub(r",\s*]", "]", fixed)
                # strip Chinese comments in strings already handled
                try:
                    return json.loads(fixed)
                except Exception:
                    # fallback: eval-like via node? use regex pairs
                    return None
    return None


def listening():
    t = (ROOT / "sources/daanjutingxieceshi/index.html").read_text(encoding="utf-8")
    m = re.search(r"ALL_QUESTIONS\s*=\s*(\[.*?\]);", t, re.S)
    qs = json.loads(m.group(1))
    out = []
    for q in qs:
        o = (q.get("original") or "").strip()
        if 40 <= len(o) <= 100:
            out.append({"id": f"L{q['id']}", "text": o})
        if len(out) >= 8:
            break
    return out


def strip_anno(s):
    s = re.sub(r"（[^）]*）", "", s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"｜[^｜]*", "", s)
    return s.strip()


def reading():
    t = (ROOT / "sources/tongyitihuanceshi/index.html").read_text(encoding="utf-8")
    m = re.search(r"const\s+ALL_GROUPS\s*=\s*\[", t)
    if not m:
        raise SystemExit("ALL_GROUPS not found")
    # End of groups: ALL_GROUPS.forEach
    end = t.find("ALL_GROUPS.forEach", m.start())
    chunk = t[m.end() : end if end > 0 else m.end() + 80000]
    groups = []
    for line in chunk.splitlines():
        line = line.strip()
        if not line.startswith("["):
            continue
        words = re.findall(r'"([^"]*)"', line)
        if len(words) >= 2:
            groups.append(words)
    clean = []
    for g in groups:
        words = [strip_anno(w) for w in g if strip_anno(w)]
        # skip Chinese-only stems / meta labels
        words = [w for w in words if re.search(r"[A-Za-z]", w)]
        seen = set()
        uniq = []
        for w in words:
            k = w.lower()
            if k not in seen and 2 <= len(w) <= 48:
                seen.add(k)
                uniq.append(w)
        if len(uniq) >= 3:
            clean.append(uniq)
    if len(clean) < 28:
        raise SystemExit(f"not enough synonym groups: {len(clean)}")
    # Build 28 MC: stem = first word, correct = second, distractors from other groups
    out = []
    gi = 0
    while len(out) < 28 and clean:
        g = clean[gi % len(clean)]
        stem = g[0]
        correct = g[1]
        distractors = []
        for offset in range(1, 12):
            og = clean[(gi + offset * 7) % len(clean)]
            cand = og[0]
            if cand.lower() != stem.lower() and cand.lower() != correct.lower():
                if cand not in distractors:
                    distractors.append(cand)
            if len(distractors) >= 3:
                break
        if len(distractors) < 3:
            gi += 1
            continue
        options = [correct] + distractors[:3]
        # stable rotate by id
        rot = len(out) % 4
        options = options[rot:] + options[:rot]
        correct_idx = options.index(correct)
        out.append(
            {
                "id": f"R{len(out)+1}",
                "stem": stem,
                "options": options,
                "correct_idx": correct_idx,
            }
        )
        gi += 1
    return out


def phrase():
    t = (ROOT / "sources/xiezuocihuoceshi/index.html").read_text(encoding="utf-8")
    # match { zh: "...", en: "..." }
    pairs = re.findall(r'\{\s*zh:\s*"([^"]+)"\s*,\s*en:\s*"([^"]+)"\s*\}', t)
    if len(pairs) < 10:
        pairs = re.findall(r"\{\s*zh:\s*'([^']+)'\s*,\s*en:\s*'([^']+)'\s*\}", t)
    out = []
    for i, (zh, en) in enumerate(pairs[:10]):
        out.append({"id": f"P{i+1}", "zh": zh, "en": en})
    return out


def translate():
    td = json.loads(
        (ROOT / "sources/juzifanyixin/translation_data.json").read_text(encoding="utf-8")
    )
    out = []
    for s in td:
        en = (s.get("finalEnglish") or "").strip()
        zh = (s.get("fullChinese") or "").strip()
        if en and zh and 40 <= len(en) <= 140:
            out.append(
                {
                    "id": f"T{s.get('id', len(out)+1)}",
                    "en": en,
                    "zh": zh,
                    "category": s.get("category") or "",
                }
            )
        if len(out) >= 5:
            break
    return out


def speaking():
    return [
        {
            "id": "S1",
            "q": "Do you work or are you a student?",
            "hint": "Answer in 3–5 sentences. Mention what you do and how you feel about it.",
        },
        {
            "id": "S2",
            "q": "What do you usually do in your free time?",
            "hint": "Answer in 3–5 sentences. Give one or two concrete examples.",
        },
    ]


def main():
    data = {
        "form": "A",
        "listening": listening(),
        "reading": reading(),
        "phrase": phrase(),
        "translate": translate(),
        "speaking": speaking(),
    }
    assert len(data["listening"]) == 8, len(data["listening"])
    assert len(data["reading"]) == 28, len(data["reading"])
    assert len(data["phrase"]) == 10, len(data["phrase"])
    assert len(data["translate"]) == 5, len(data["translate"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = "window.PLACEMENT_FORM_A = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT.write_text(body, encoding="utf-8")
    print("wrote", OUT)
    print(
        "counts",
        {k: len(v) if isinstance(v, list) else v for k, v in data.items()},
    )


if __name__ == "__main__":
    main()
