# -*- coding: utf-8 -*-
"""Generate missing complex-audio mp3 with Edge neural TTS, stage all 170, ready to upload."""
from __future__ import annotations

import asyncio
import re
import shutil
from pathlib import Path

import edge_tts

SRC = Path(r"G:\口语练习\audio")
ROOT = Path(r"D:\ielts-practice-platform")
HTML = ROOT / "sources" / "kouyulianxi" / "complex-sentences.html"
OUT = ROOT / "sources" / "kouyulianxi" / "complex-audio"
VOICE = "en-GB-SoniaNeural"
RATE = "+0%"


def build_sentence(skeleton: str, ans: list[str]) -> str:
    def repl(m: re.Match[str]) -> str:
        return ans[int(m.group(1))]

    s = re.sub(r"\[(\d+)\]", repl, skeleton)
    s = re.sub(r"\s+([.,!?])", r"\1", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def extract_adv_missing() -> list[tuple[str, str]]:
    """Parse ADV from HTML; return (filename, sentence) for items 9 and 10."""
    text = HTML.read_text(encoding="utf-8")
    start = text.index("const ADV = [")
    end = text.index("/* ============ 全局状态 ============ */")
    block = text[start:end]
    missing: list[tuple[str, str]] = []
    for m in re.finditer(
        r'id:"(a\d+)"[\s\S]*?skeleton:"([^"]+)"[\s\S]*?items:\[([\s\S]*?)\n\]\n\}',
        block,
    ):
        pid, skeleton, items_raw = m.group(1), m.group(2), m.group(3)
        ans_list: list[list[str]] = []
        for im in re.finditer(r"ans:(\[[^\]]*\])", items_raw):
            # JS single-quoted-ish arrays use double quotes in this file
            raw = im.group(1)
            # eval-safe: only strings in double quotes
            parts = re.findall(r'"((?:\\.|[^"\\])*)"', raw)
            ans_list.append([p.replace(r"\"", '"') for p in parts])
        for idx in (9, 10):
            if idx > len(ans_list):
                raise SystemExit(f"{pid} missing item {idx}")
            sentence = build_sentence(skeleton, ans_list[idx - 1])
            missing.append((f"adv_{pid}_{idx}.mp3", sentence))
    return missing


async def gen_one(name: str, text: str, dest: Path) -> None:
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(dest))
    print(f"OK {name} ({dest.stat().st_size} bytes) <- {text}")


async def generate_missing(pairs: list[tuple[str, str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in pairs:
        dest = OUT / name
        await gen_one(name, text, dest)


def copy_existing() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = list(SRC.glob("*.mp3"))
    print(f"Copying {len(files)} from {SRC}")
    for f in files:
        shutil.copy2(f, OUT / f.name)


def verify() -> None:
    needed = {f"p{p}_{i}.mp3" for p in range(1, 8) for i in range(1, 11)}
    needed |= {f"adv_a{a}_{i}.mp3" for a in range(1, 11) for i in range(1, 11)}
    have = {p.name for p in OUT.glob("*.mp3")}
    miss = sorted(needed - have)
    print(f"staging={len(have)} missing={len(miss)}")
    if miss:
        print("MISSING:", miss)
        raise SystemExit(1)


def main() -> None:
    pairs = extract_adv_missing()
    print(f"to_generate={len(pairs)}")
    for n, t in pairs:
        print(f"  {n}: {t}")
    copy_existing()
    asyncio.run(generate_missing(pairs))
    verify()
    print("DONE")


if __name__ == "__main__":
    main()
