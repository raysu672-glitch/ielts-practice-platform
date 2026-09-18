#!/usr/bin/env python3
"""Fix known typos in 听力基础词汇 (modules.js, listening_basic.html, audio).

注意：音频部分必须**重新生成**，不能只重命名文件。
早期版本这里只做 `src.rename(dst)`，于是 land.mp3 里念的仍然是生成时的拼错词
"iand"（听起来像 "End"），学生反馈读音不对。详见
scripts/repair_basic_words_audio.py 的模块说明。
"""
from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 词表规模守卫：用于发现 ALL_WORDS 被意外破坏
EXPECTED_WORD_COUNT = 2037
# 与 scripts/gen_tts_words.py 保持一致
VOICE = "en-GB-SoniaNeural"
RATE = "+0%"
VOLUME = "+0%"
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
    """按正确拼写重新生成音频；旧名的 mp3 直接删除。

    只重命名是不够的——文件名换了，音频内容还是拼错词的读音。
    """
    if not AUDIO_DIR.is_dir():
        return 0, ["audio dir missing"]
    try:
        import edge_tts
    except ImportError:
        return 0, ["edge-tts 未安装，音频未重新生成（pip install edge-tts）"]

    async def gen(word: str) -> None:
        await edge_tts.Communicate(word, VOICE, rate=RATE, volume=VOLUME).save(
            str(AUDIO_DIR / f"{word}.mp3")
        )

    regenerated = 0
    issues: list[str] = []
    for old, new in TYPO_MAP.items():
        old_path = AUDIO_DIR / f"{old}.mp3"
        try:
            asyncio.run(gen(new))
        except Exception as exc:  # noqa: BLE001 - 网络抖动
            issues.append(f"regenerate failed: {new}.mp3 ({exc})")
            continue
        regenerated += 1
        if old_path.is_file():
            old_path.unlink()
    return regenerated, issues


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
    if len(words) != EXPECTED_WORD_COUNT:
        raise SystemExit(
            f"word count changed: {len(words)} != {EXPECTED_WORD_COUNT}；"
            "若词表是刻意调整的，请同步更新 EXPECTED_WORD_COUNT。"
        )


def main() -> None:
    n_mod = fix_modules()
    n_html = fix_listening_basic_html()
    n_audio, audio_issues = fix_audio()
    verify()
    print(f"modules.js: {n_mod} words fixed")
    print(f"listening_basic.html: {n_html} entries fixed")
    print(f"audio: {n_audio} files regenerated")
    if audio_issues:
        print("audio notes:")
        for line in audio_issues:
            print(f"  {line}")


if __name__ == "__main__":
    main()
