# -*- coding: utf-8 -*-
"""生成入学摸底听力句 MP3。

优先 edge-tts；失败则从答案句 CDN 拉取同文录音。
输出：sources/xinshengmodi/audio/L*.mp3（*.mp3 已 ignore）

用法：
  python scripts/gen_placement_listening_audio.py
  python scripts/gen_placement_listening_audio.py --force
  python scripts/gen_placement_listening_audio.py --cdn-only
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "sources" / "xinshengmodi" / "questions_a.js"
DJX_HTML = ROOT / "sources" / "daanjutingxie" / "index.html"
OUT_DIR = ROOT / "sources" / "xinshengmodi" / "audio"
CDN = "https://raysu672-glitch.github.io/daanjutingxie/"

VOICE = "en-GB-SoniaNeural"
RATE = "-5%"
VOLUME = "+0%"


def load_listening() -> list[dict]:
    text = QUESTIONS.read_text(encoding="utf-8")
    m = re.search(r"window\.PLACEMENT_FORM_A\s*=\s*(\{[\s\S]*\})\s*;\s*$", text.strip())
    if not m:
        m = re.search(r"=\s*(\{[\s\S]*\})\s*;?\s*$", text.strip())
    if not m:
        raise SystemExit("cannot parse questions_a.js")
    data = json.loads(m.group(1))
    items = data.get("listening") or []
    if not items:
        raise SystemExit("no listening items")
    return items


def djx_audio_by_text() -> dict[str, str]:
    t = DJX_HTML.read_text(encoding="utf-8")
    m = re.search(r"const GROUPS\s*=\s*(\[.*?\]);", t, re.S)
    if not m:
        return {}
    groups = json.loads(m.group(1))
    out: dict[str, str] = {}
    for g in groups:
        for q in g:
            orig = (q.get("original") or "").strip()
            af = q.get("audio_file") or ""
            if orig and af:
                out[orig] = af
    return out


def fetch_cdn(text: str, dest: Path, by_text: dict[str, str]) -> bool:
    af = by_text.get(text.strip())
    if not af:
        print(f"  CDN miss text: {text[:48]}")
        return False
    local = ROOT / "sources/daanjutingxie" / urllib.parse.unquote(af)
    if local.is_file() and local.stat().st_size > 500:
        dest.write_bytes(local.read_bytes())
        print(f"  copy {dest.name}")
        return True
    parts = af.split("/", 1)
    folder = urllib.parse.quote(parts[0])
    rest = parts[1] if len(parts) > 1 else ""
    url = CDN + folder + "/" + rest
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if len(data) < 500:
            print(f"  CDN too small {dest.name}")
            return False
        dest.write_bytes(data)
        print(f"  CDN ok {dest.name} ({len(data)})")
        return True
    except Exception as e:
        print(f"  CDN fail {dest.name}: {e}")
        return False


async def gen_edge(text: str, path: Path, sem: asyncio.Semaphore) -> bool:
    try:
        import edge_tts
    except ImportError:
        return False
    async with sem:
        try:
            communicate = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME)
            await communicate.save(str(path))
            if path.is_file() and path.stat().st_size > 500:
                return True
            if path.is_file():
                path.unlink(missing_ok=True)
            return False
        except Exception as e:
            print(f"  edge FAIL [{path.name}]: {e}", flush=True)
            if path.is_file() and path.stat().st_size <= 500:
                try:
                    path.unlink()
                except OSError:
                    pass
            return False


async def main(force: bool, cdn_only: bool) -> None:
    items = load_listening()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[str, str, Path]] = []
    for q in items:
        qid = str(q["id"])
        path = OUT_DIR / f"{qid}.mp3"
        if path.is_file() and path.stat().st_size > 500 and not force:
            print(f"skip {path.name}")
            continue
        if path.is_file():
            try:
                path.unlink()
            except OSError:
                pass
        jobs.append((qid, q["text"], path))

    print(f"need {len(jobs)} / {len(items)}")
    if not jobs:
        print("all exist")
        return

    pending = list(jobs)
    if not cdn_only:
        sem = asyncio.Semaphore(4)
        results = await asyncio.gather(*[gen_edge(t, p, sem) for _, t, p in pending])
        pending = [jobs[i] for i, ok in enumerate(results) if not ok]
        print(f"edge ok {len(jobs) - len(pending)}/{len(jobs)}")

    if pending:
        by_text = djx_audio_by_text()
        print(f"CDN fallback {len(pending)}")
        for _, text, path in pending:
            fetch_cdn(text, path, by_text)

    ok = sum(1 for _, _, p in jobs if p.is_file() and p.stat().st_size > 500)
    print(f"done {ok}/{len(jobs)} -> {OUT_DIR}")
    if ok < len(jobs):
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--cdn-only", action="store_true")
    args = ap.parse_args()
    asyncio.run(main(args.force, args.cdn_only))
