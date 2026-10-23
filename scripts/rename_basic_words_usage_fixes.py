#!/usr/bin/env python3
"""Rename basic_words audio after remaining usage fixes."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "sources" / "tinglidanciceshi" / "audio" / "basic_words"

# Keep in sync with fix_content_audit_batch.BASIC_WORD_FIXES
FIXES = {
    "alarming system": "alarm system",
    "golf court": "golf course",
    "plane science": "planet science",
    "personal officer": "personnel officer",
    "privacy company": "private company",
    "bottle water": "bottled water",
    "animals behavior": "animal behaviour",
    "culture awareness": "cultural awareness",
    "culture context": "cultural context",
    "families life": "family life",
    "finance market": "financial market",
    "environment damage": "environmental damage",
    "economics history": "economic history",
    "eye contacts": "eye contact",
    "children background": "children's background",
    "children mind": "children's minds",
    "girl club": "girls' club",
    "hairs": "hair",
    "weathers": "weather",
    "study skill": "study skills",
    "repaired cost": "repair cost",
    "time consuming": "time-consuming",
    "triangle sharp": "triangle shape",
    "political man": "politician",
    "high user": "heavy user",
    "free pick": "free pick-up",
    "banana ride": "banana boat",
    "advance level": "advanced level",
    "view shelter": "viewing shelter",
    "pet meat": "pet food",
    "videocameras": "video cameras",
}


def main() -> None:
    if not AUDIO.is_dir():
        print("audio dir missing")
        return
    ok = skip = miss = 0
    for old, new in FIXES.items():
        src = AUDIO / f"{old}.mp3"
        dst = AUDIO / f"{new}.mp3"
        if not src.is_file():
            miss += 1
            print(f"missing: {old}.mp3")
            continue
        if dst.is_file():
            # target exists (duplicate case) — remove old typo file
            src.unlink()
            skip += 1
            print(f"removed duplicate source (target exists): {old}.mp3")
            continue
        src.rename(dst)
        ok += 1
        print(f"OK: {old}.mp3 -> {new}.mp3")
    print(f"done renamed={ok} removed_dup_src={skip} missing={miss}")
    print(f"mp3 count={len(list(AUDIO.glob('*.mp3')))}")


if __name__ == "__main__":
    main()
