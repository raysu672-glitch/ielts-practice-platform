# -*- coding: utf-8 -*-
"""List expected complex-audio filenames and sentences from complex-sentences.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "sources" / "kouyulianxi" / "complex-sentences.html"


def extract_array(text: str, var: str):
    m = re.search(rf"const\s+{var}\s*=\s*\[", text)
    if not m:
        raise SystemExit(f"missing {var}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                # Convert JS object-ish to JSON carefully is hard; use regex per pattern instead
                return text[start : i + 1]
    raise SystemExit(f"unclosed {var}")


def parse_patterns(block: str, adv_prefix: bool):
    """Parse id + items[].ans using regex (JS object literals)."""
    out = []
    # split by top-level objects starting with id:
    for m in re.finditer(
        r'id:"(?P<id>[^"]+)"[\s\S]*?skeleton:"(?P<sk>[^"]*)"[\s\S]*?items:\[(?P<items>[\s\S]*?)\n\]\n\}',
        block,
    ):
        pid = m.group("id")
        skeleton = m.group("sk")
        items_raw = m.group("items")
        ans_list = []
        for im in re.finditer(r"ans:(\[[^\]]*\])", items_raw):
            ans = json.loads(im.group(1).replace("'", '"'))
            ans_list.append(ans)
        out.append({"id": pid, "skeleton": skeleton, "items": ans_list, "adv": adv_prefix})
    return out


def build_sentence(skeleton: str, ans: list[str]) -> str:
    s = skeleton
    for i, a in enumerate(ans):
        s = s.replace(f"[{i}]", a)
    return s.strip()


def main():
    text = HTML.read_text(encoding="utf-8")
    # cut PATTERNS and ADV blocks by markers
    p_start = text.index("const PATTERNS = [")
    a_start = text.index("const ADV = [")
    g_start = text.index("/* ============ 全局状态 ============ */")
    patterns_block = text[p_start:a_start]
    adv_block = text[a_start:g_start]

    patterns = parse_patterns(patterns_block, False)
    adv = parse_patterns(adv_block, True)

    needed = []
    for group in patterns + adv:
        pre = "adv_" if group["adv"] else ""
        for idx, ans in enumerate(group["items"], start=1):
            fname = f"{pre}{group['id']}_{idx}.mp3"
            sentence = build_sentence(group["skeleton"], ans)
            needed.append({"file": fname, "id": group["id"], "idx": idx, "text": sentence})

    out = ROOT / "_complex_audio_needed.json"
    out.write_text(json.dumps(needed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"needed={len(needed)} written={out}")
    for n in needed[:3]:
        print(n["file"], "=>", n["text"][:80])
    print("...")
    for n in needed[-2:]:
        print(n["file"], "=>", n["text"][:80])


if __name__ == "__main__":
    main()
