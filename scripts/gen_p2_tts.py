"""Generate natural male British MP3 for kouyulianxi P2 materials & questions.

Voice: en-GB-RyanNeural (male, neural, more natural than browser TTS)
Output: sources/kouyulianxi/audio/p2/ + manifest.js
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("ERROR: edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

VOICE = "en-GB-RyanNeural"  # male British neural
RATE = "+0%"
VOLUME = "+0%"
PITCH = "+0Hz"

ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "sources" / "kouyulianxi" / "p2-data.js"
OUT_DIR = ROOT / "sources" / "kouyulianxi" / "audio" / "p2"
MANIFEST_JS = OUT_DIR / "manifest.js"


def load_p2_data() -> dict:
    # Locate the P2_DATA object with brace counting (data file may end with a
    # `window.P2_DATA = ...` block, so regex/$ anchoring is unreliable).
    import subprocess

    script = (
        "const fs=require('fs');"
        f"const t=fs.readFileSync({json.dumps(str(DATA_JS))},'utf8');"
        "const start=t.indexOf('{', t.indexOf('const P2_DATA'));"
        "let depth=0, inStr=false, esc=false, end=-1;"
        "for(let i=start;i<t.length;i++){"
        "  const c=t[i];"
        "  if(inStr){ if(esc){esc=false;} else if(c==='\\\\'){esc=true;} else if(c==='\"'){inStr=false;} continue; }"
        "  if(c==='\"'){inStr=true;}"
        "  else if(c==='{'){depth++;}"
        "  else if(c==='}'){depth--; if(depth===0){end=i; break;}}"
        "}"
        "if(end<0){console.error('parse fail'); process.exit(1);}"
        "const data=eval('('+t.slice(start,end+1)+')');"
        "process.stdout.write(JSON.stringify(data));"
    )
    out = subprocess.check_output(["node", "-e", script], cwd=str(ROOT))
    return json.loads(out.decode("utf-8"))


def collect_jobs(data: dict) -> list[tuple[str, str, Path]]:
    """Return list of (manifest_key, text, out_path)."""
    jobs: list[tuple[str, str, Path]] = []

    for mat in data.get("materials") or []:
        mid = mat["id"]
        for i, step in enumerate(mat.get("steps") or []):
            en = (step.get("en") or "").strip()
            if not en:
                continue
            key = f"material:{mid}:{i}"
            rel = OUT_DIR / "materials" / mid / f"{i}.mp3"
            jobs.append((key, en, rel))
        for var in mat.get("variants") or []:
            vid = var.get("id") or "x"
            en = (var.get("en") or "").strip()
            if not en:
                continue
            # variants replace step 1 for yumeng
            key = f"material:{mid}:1:{vid}"
            rel = OUT_DIR / "materials" / mid / f"1-{vid}.mp3"
            jobs.append((key, en, rel))

    for q in data.get("questions") or []:
        qid = q["id"]
        qtext = (q.get("q") or q.get("title") or "").strip()
        if qtext:
            key = f"question:{qid}:q"
            jobs.append((key, qtext, OUT_DIR / "questions" / f"{qid}-q.mp3"))
        opening = (q.get("openingEn") or "").strip()
        if opening:
            key = f"question:{qid}:opening"
            jobs.append((key, opening, OUT_DIR / "questions" / f"{qid}-opening.mp3"))
        opening_by = q.get("openingById") or {}
        for oid, body in opening_by.items():
            en = (body.get("en") if isinstance(body, dict) else "") or ""
            en = en.strip()
            if not en:
                continue
            key = f"question:{qid}:opening:{oid}"
            jobs.append((key, en, OUT_DIR / "questions" / f"{qid}-opening-{oid}.mp3"))

    # de-dupe by key (keep first)
    seen = set()
    unique = []
    for key, text, path in jobs:
        if key in seen:
            continue
        seen.add(key)
        unique.append((key, text, path))
    return unique


async def generate_one(
    text: str, out_path: Path, semaphore: asyncio.Semaphore
) -> bool:
    async with semaphore:
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            communicate = edge_tts.Communicate(
                text, VOICE, rate=RATE, volume=VOLUME, pitch=PITCH
            )
            await communicate.save(str(out_path))
            return out_path.is_file() and out_path.stat().st_size > 200
        except Exception as exc:
            print(f"  FAIL {out_path.name}: {exc}", flush=True)
            return False


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force-all",
        action="store_true",
        help="regenerate every clip at standard rate (+0%)",
    )
    args = parser.parse_args()

    print(f"Voice: {VOICE} rate={RATE}")
    print(f"Reading: {DATA_JS}")
    data = load_p2_data()
    jobs = collect_jobs(data)
    print(f"Jobs: {len(jobs)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.force_all:
        pending = jobs
        print("Force-all: regenerating every clip")
    else:
        pending = [(k, t, p) for k, t, p in jobs if not (p.is_file() and p.stat().st_size > 200)]
    print(f"Already present: {len(jobs) - len(pending)}, pending: {len(pending)}")

    semaphore = asyncio.Semaphore(6)
    success = 0
    if pending:
        tasks = [
            (key, asyncio.create_task(generate_one(text, path, semaphore)))
            for key, text, path in pending
        ]
        for i, (key, task) in enumerate(tasks, 1):
            ok = await task
            if ok:
                success += 1
            if i % 10 == 0 or i == len(tasks):
                print(f"  Progress: {i}/{len(tasks)} ({success} OK)", flush=True)

    # write manifest for all successful files
    manifest: dict[str, str] = {}
    for key, _text, path in jobs:
        if path.is_file() and path.stat().st_size > 200:
            rel = path.relative_to(ROOT / "sources" / "kouyulianxi").as_posix()
            manifest[key] = rel

    MANIFEST_JS.write_text(
        "// Auto-generated P2 male British neural audio map\n"
        "window.P2_AUDIO_MANIFEST = "
        + json.dumps(manifest, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"\nManifest entries: {len(manifest)}")
    print(f"Wrote: {MANIFEST_JS}")
    print(f"Generated this run: {success}/{len(pending)}")
    missing = [k for k, _, p in jobs if k not in manifest]
    if missing:
        print(f"Missing ({len(missing)}): {missing[:10]}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
