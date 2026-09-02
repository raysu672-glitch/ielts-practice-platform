#!/usr/bin/env python3
"""Fix known typos in 听力基础词汇 (modules.js, listening_basic.html, audio filenames)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "sources" / "tinglidanciceshi" / "js" / "modules.js"
LISTENING_BASIC = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"
AUDIO_DIR = ROOT / "sources" / "tinglidanciceshi" / "audio" / "basic_words"

TYPO_MAP: dict[str, str] = {
    "air-condition": "air conditioning",
    "bottie water": "bottle water",
    "businessmanagement": "business management",
    "butterfiies": "butterflies",
    "cabie": "cable",
    "ciothing sections": "clothing sections",
    "compiaints": "complaints",
    "compiete": "complete",
    "compiex": "complex",
    "compuisory": "compulsory",
    "computerprogrammer": "computer programmer",
    "contact detaiis": "contact details",
    "desk iamp": "desk lamp",
    "disable people": "disabled people",
    "eniargement": "enlargement",
    "entertainmentindustry": "entertainment industry",
    "equai": "equal",
    "famiiy": "family",
    "fiashiight": "flashlight",
    "fiavor": "flavor",
    "fiute": "flute",
    "flourishment": "flourishing",
    "french styie": "french style",
    "gioves": "gloves",
    "graduai": "graduate",
    "iand": "land",
    "ianes": "lanes",
    "iaptops": "laptops",
    "iaw department": "law department",
    "iegroom": "legroom",
    "ieisure": "leisure",
    "iength": "length",
    "infiuence": "influence",
    "informai": "informal",
    "ioans": "loans",
    "iookout point": "lookout point",
    "iost": "lost",
    "iungs": "lungs",
    "journaiism": "journalism",
    "knowiedge sharing": "knowledge sharing",
    "laboratories report": "laboratory report",
    "marine piants": "marine plants",
    "modei": "model",
    "moraiity": "morality",
    "paining": "painting",
    "painting ciass": "painting class",
    "personai alarm": "personal alarm",
    "personalinformation": "personal information",
    "popuiar": "popular",
    "practicai course": "practical course",
    "presenting result": "presenting results",
    "reaiism": "realism",
    "reguiar": "regular",
    "reieased": "released",
    "ring abell": "ring a bell",
    "seif-iocking": "self-locking",
    "shaiiow": "shallow",
    "steei": "steel",
    "symboi": "symbol",
    "tempie waiis": "temple walls",
    "tities": "titles",
    "transiation": "translation",
    "window iocks": "window locks",
}


def extract_array(name: str, text: str) -> list[str]:
    m = re.search(rf"var {name}\s*=\s*\[", text)
    if not m:
        raise SystemExit(f"missing {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise SystemExit(f"unclosed {name}")


def replace_array(name: str, text: str, words: list[str]) -> str:
    m = re.search(rf"var {name}\s*=\s*\[", text)
    if not m:
        raise SystemExit(f"missing {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                new_json = json.dumps(words, ensure_ascii=False)
                return text[:start] + new_json + text[i + 1 :]
    raise SystemExit(f"unclosed {name}")


def fix_modules() -> int:
    text = MODULES.read_text(encoding="utf-8")
    words = extract_array("allWordsListeningBasic", text)
    changed = 0
    fixed: list[str] = []
    for w in words:
        if w in TYPO_MAP:
            fixed.append(TYPO_MAP[w])
            changed += 1
        else:
            fixed.append(w)
    if changed:
        MODULES.write_text(replace_array("allWordsListeningBasic", text, fixed), encoding="utf-8")
    return changed


def fix_listening_basic_html() -> int:
    html = LISTENING_BASIC.read_text(encoding="utf-8")
    changed = 0
    for old, new in TYPO_MAP.items():
        old_pat = f'"word":{json.dumps(old, ensure_ascii=False)}'
        new_pat = f'"word":{json.dumps(new, ensure_ascii=False)}'
        if old_pat in html:
            html = html.replace(old_pat, new_pat)
            changed += 1
    if changed:
        LISTENING_BASIC.write_text(html, encoding="utf-8")
    return changed


def fix_audio() -> tuple[int, list[str]]:
    if not AUDIO_DIR.is_dir():
        return 0, ["audio dir missing"]
    renamed = 0
    issues: list[str] = []
    for old, new in TYPO_MAP.items():
        src = AUDIO_DIR / f"{old}.mp3"
        dst = AUDIO_DIR / f"{new}.mp3"
        if not src.is_file():
            issues.append(f"missing audio: {old}.mp3")
            continue
        if dst.is_file() and dst != src:
            issues.append(f"target exists, skip: {new}.mp3")
            continue
        src.rename(dst)
        renamed += 1
    return renamed, issues


def verify() -> None:
    text = MODULES.read_text(encoding="utf-8")
    words = extract_array("allWordsListeningBasic", text)
    remaining = [w for w in words if w in TYPO_MAP]
    if remaining:
        raise SystemExit(f"modules.js still has typos: {remaining}")
    html = LISTENING_BASIC.read_text(encoding="utf-8")
    for old in TYPO_MAP:
        if f'"word":{json.dumps(old, ensure_ascii=False)}' in html:
            raise SystemExit(f"html still has typo: {old}")
    if len(words) != 2041:
        raise SystemExit(f"word count changed: {len(words)}")


def main() -> None:
    n_mod = fix_modules()
    n_html = fix_listening_basic_html()
    n_audio, audio_issues = fix_audio()
    verify()
    print(f"modules.js: {n_mod} words fixed")
    print(f"listening_basic.html: {n_html} entries fixed")
    print(f"audio: {n_audio} files renamed")
    if audio_issues:
        print("audio notes:")
        for line in audio_issues:
            print(f"  {line}")


if __name__ == "__main__":
    main()
