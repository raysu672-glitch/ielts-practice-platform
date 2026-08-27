# -*- coding: utf-8 -*-
"""Align P1 question audio to current p1-data.js and generate missing clips.

1) Remap existing mp3 files by matching question text from a previous p1-data.js
2) Generate missing clips with edge-tts (en-GB-LibbyNeural, natural rate)
3) Rewrite sources/kouyulianxi/audio/manifest.js

Usage:
  python scripts/gen_p1_tts.py
  python scripts/gen_p1_tts.py --force-missing   # only generate missing (default)
  python scripts/gen_p1_tts.py --force-all       # regenerate every clip
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("ERROR: edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
AUDIO_DIR = ROOT / "sources" / "kouyulianxi" / "audio"
MANIFEST_JS = AUDIO_DIR / "manifest.js"

VOICE = "en-GB-LibbyNeural"
RATE = "-3%"
PITCH = "+0Hz"
VOLUME = "+0%"


def norm_q(s: str) -> str:
    s = (s or "").lower().strip()
    for a, b in [("'", "'"), ("'", "'"), ("'", "'")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "", s)


def load_p1_via_node(path: Path) -> dict:
    script = (
        "const fs=require('fs');"
        f"const t=fs.readFileSync({json.dumps(str(path))},'utf8');"
        "const i=t.indexOf('{'); const j=t.lastIndexOf('}');"
        "const data=eval('('+t.slice(i,j+1)+')');"
        "process.stdout.write(JSON.stringify(data));"
    )
    out = subprocess.check_output(["node", "-e", script], cwd=str(ROOT))
    return json.loads(out.decode("utf-8"))


def load_old_p1_from_git() -> dict | None:
    """Best-effort: p1-data before the heat-list rebuild."""
    candidates = [
        "8e7b850:sources/kouyulianxi/p1-data.js",
        "HEAD~5:sources/kouyulianxi/p1-data.js",
        "HEAD~10:sources/kouyulianxi/p1-data.js",
    ]
    # Prefer the commit just before P1 rebuild if available
    try:
        log = subprocess.check_output(
            ["git", "log", "--oneline", "--", "sources/kouyulianxi/p1-data.js"],
            cwd=str(ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in log.splitlines():
            if "Rebuild P1" in line or "heat" in line.lower():
                sha = line.split()[0]
                # parent of rebuild
                parent = subprocess.check_output(
                    ["git", "rev-parse", f"{sha}^"],
                    cwd=str(ROOT),
                    text=True,
                ).strip()
                candidates.insert(0, f"{parent}:sources/kouyulianxi/p1-data.js")
                break
    except Exception:
        pass

    tmp = ROOT / "_p1_git_old.js"
    for ref in candidates:
        try:
            blob = subprocess.check_output(["git", "show", ref], cwd=str(ROOT))
            tmp.write_bytes(blob)
            data = load_p1_via_node(tmp)
            print(f"Old p1-data from git: {ref}")
            return data
        except Exception:
            continue
    return None


def iter_questions(data: dict) -> list[dict]:
    items = []
    for cat in data.get("categories") or []:
        cid = cat["id"]
        for q in cat.get("questions") or []:
            qtext = (q.get("q") or "").strip()
            if not qtext:
                continue
            items.append(
                {
                    "catId": cid,
                    "id": q["id"],
                    "q": qtext,
                    "key": f"{cid}:{q['id']}",
                    "textKey": f"q:{norm_q(qtext)}",
                    "rel": f"audio/{cid}/{q['id']}.mp3",
                    "path": AUDIO_DIR / cid / f"{q['id']}.mp3",
                }
            )
    return items


def build_text_to_path(old_data: dict | None) -> dict[str, Path]:
    """Map normalized question text -> existing mp3 path."""
    mapping: dict[str, Path] = {}
    if not old_data:
        return mapping
    for cat in old_data.get("categories") or []:
        cid = cat["id"]
        for q in cat.get("questions") or []:
            qtext = (q.get("q") or "").strip()
            if not qtext:
                continue
            path = AUDIO_DIR / cid / f"{q['id']}.mp3"
            if path.is_file() and path.stat().st_size > 500:
                mapping[norm_q(qtext)] = path
    return mapping


async def generate_one(text: str, out_path: Path, sem: asyncio.Semaphore) -> bool:
    async with sem:
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = out_path.with_suffix(".tmp.mp3")
            communicate = edge_tts.Communicate(
                text, VOICE, rate=RATE, volume=VOLUME, pitch=PITCH
            )
            await communicate.save(str(tmp))
            if tmp.is_file() and tmp.stat().st_size > 500:
                tmp.replace(out_path)
                return True
            if tmp.exists():
                tmp.unlink()
            return False
        except Exception as exc:
            print(f"  FAIL {out_path.name}: {exc}", flush=True)
            return False


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-all", action="store_true")
    parser.add_argument("--voices", action="store_true")
    args = parser.parse_args()

    if args.voices:
        vs = await edge_tts.list_voices()
        for v in vs:
            if v["Locale"] == "en-GB" and "Neural" in v["ShortName"]:
                print(f"{v['ShortName']:28} {v['Gender']}")
        return

    print(f"Voice={VOICE} rate={RATE}")
    current = load_p1_via_node(DATA_JS)
    items = iter_questions(current)
    print(f"Current questions: {len(items)}")

    old = load_old_p1_from_git()
    text_map = build_text_to_path(old)
    print(f"Reusable clips by text match: {len(text_map)}")

    def sidecar_path(mp3: Path) -> Path:
        return mp3.with_suffix(".txt")

    def write_sidecar(mp3: Path, text: str) -> None:
        sidecar_path(mp3).write_text(text.strip() + "\n", encoding="utf-8")

    def sidecar_matches(mp3: Path, text: str) -> bool:
        sp = sidecar_path(mp3)
        if not (mp3.is_file() and mp3.stat().st_size > 500 and sp.is_file()):
            return False
        return norm_q(sp.read_text(encoding="utf-8")) == norm_q(text)

    remapped = 0
    reused = 0
    need_gen: list[dict] = []

    for it in items:
        dest: Path = it["path"]
        nkey = norm_q(it["q"])
        src = text_map.get(nkey)

        if args.force_all:
            need_gen.append(it)
            continue

        if src and src.is_file() and src.stat().st_size > 500:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.resolve() != dest.resolve():
                shutil.copy2(src, dest)
                remapped += 1
            write_sidecar(dest, it["q"])
            reused += 1
            continue

        if sidecar_matches(dest, it["q"]):
            reused += 1
            continue

        # Existing file at dest is likely WRONG text after rebuild — regenerate
        need_gen.append(it)

    print(f"Remapped/copied: {remapped}")
    print(f"Already aligned: {reused}")
    print(f"Need generate: {len(need_gen)}")

    sem = asyncio.Semaphore(5)
    ok_n = 0
    if need_gen:
        tasks = [
            (it, asyncio.create_task(generate_one(it["q"], it["path"], sem)))
            for it in need_gen
        ]
        for i, (it, task) in enumerate(tasks, 1):
            ok = await task
            if ok:
                ok_n += 1
                write_sidecar(it["path"], it["q"])
            if i % 15 == 0 or i == len(tasks):
                print(f"  Progress {i}/{len(tasks)} ok={ok_n}", flush=True)

    # Write manifest (id keys + content keys)
    manifest: dict[str, str] = {}
    missing = []
    for it in items:
        if it["path"].is_file() and it["path"].stat().st_size > 500:
            manifest[it["key"]] = it["rel"]
            manifest[it["textKey"]] = it["rel"]
        else:
            missing.append(it["key"])

    MANIFEST_JS.write_text(
        "// Auto-generated P1 question audio map (id + text keys)\n"
        "const P1_AUDIO_MANIFEST = "
        + json.dumps(manifest, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Manifest keys: {len(manifest)} (id+text) -> {MANIFEST_JS}")
    print(f"Questions with audio: {sum(1 for it in items if it['key'] in manifest)}/{len(items)}")
    if missing:
        print(f"Still missing ({len(missing)}): {missing[:12]}")
        sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
