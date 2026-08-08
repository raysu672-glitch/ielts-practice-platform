"""Generate natural male British MP3 for kouyulianxi P2 materials & questions.

Voice: en-GB-RyanNeural (male, neural, more natural than browser TTS)
Output: sources/kouyulianxi/audio/p2/ + manifest.js
"""
from __future__ import annotations

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
RATE = "-5%"
VOLUME = "+0%"
PITCH = "+0Hz"

ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "sources" / "kouyulianxi" / "p2-data.js"
OUT_DIR = ROOT / "sources" / "kouyulianxi" / "audio" / "p2"
MANIFEST_JS = OUT_DIR / "manifest.js"


def load_p2_data() -> dict:
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"const P2_DATA\s*=\s*(\{[\s\S]*\});\s*$", text.strip())
    if not m:
        raise ValueError("P2_DATA object not found in p2-data.js")
    # JS object is close enough to JSON after light cleanup
    raw = m.group(1)
    # Keep as JSON via node for fidelity with trailing commas / unquoted keys
    import subprocess

    script = (
        "const fs=require('fs');"
        f"const t=fs.readFileSync({json.dumps(str(DATA_JS))},'utf8');"
        "const m=t.match(/const P2_DATA\\s*=\\s*([\\s\\S]*?);\\s*$/);"
        "if(!m){console.error('parse fail'); process.exit(1);}"
        "const data=eval('('+m[1]+')');"
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
    print(f"Voice: {VOICE} rate={RATE}")
    print(f"Reading: {DATA_JS}")
    data = load_p2_data()
    jobs = collect_jobs(data)
    print(f"Jobs: {len(jobs)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
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
