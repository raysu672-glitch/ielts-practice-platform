# -*- coding: utf-8 -*-
"""Try reuse daanjutingxie mp3 for placement listening sentences."""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sources/xinshengmodi/audio"
QUESTIONS = ROOT / "sources/xinshengmodi/questions_a.js"
DJX = ROOT / "sources/daanjutingxie/index.html"
CDN = "https://raysu672-glitch.github.io/daanjutingxie/"


def load_form():
    t = QUESTIONS.read_text(encoding="utf-8")
    m = re.search(r"window\.PLACEMENT_FORM_A\s*=\s*(\{[\s\S]*\})\s*;\s*$", t.strip())
    return json.loads(m.group(1))


def load_djx_by_original():
    t = DJX.read_text(encoding="utf-8")
    m = re.search(r"const GROUPS\s*=\s*(\[.*?\]);", t, re.S)
    if not m:
        raise SystemExit("GROUPS not found")
    groups = json.loads(m.group(1))
    by_text = {}
    for g in groups:
        for q in g:
            orig = (q.get("original") or "").strip()
            af = q.get("audio_file") or ""
            if orig and af:
                by_text[orig] = af
    return by_text


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    form = load_form()
    by_text = load_djx_by_original()
    print("djx audio map", len(by_text))
    for q in form["listening"]:
        text = q["text"].strip()
        af = by_text.get(text)
        dest = OUT / f"{q['id']}.mp3"
        if dest.is_file() and dest.stat().st_size > 1000:
            print("have", dest.name)
            continue
        if not af:
            print("NO MATCH", q["id"], text[:50])
            continue
        # local first
        local = ROOT / "sources/daanjutingxie" / urllib.parse.unquote(af)
        if local.is_file():
            dest.write_bytes(local.read_bytes())
            print("copy", dest.name, "from local")
            continue
        # af 形如「A听力答案句/2%20%20If...mp3」：文件夹需 UTF-8 百分号编码
        parts = af.split("/", 1)
        folder = urllib.parse.quote(parts[0])
        rest = parts[1] if len(parts) > 1 else ""
        url = CDN + folder + "/" + rest
        try:
            print("fetch", q["id"], url[:100], "...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < 500:
                print("too small", q["id"], len(data))
                continue
            dest.write_bytes(data)
            print("ok", dest.name, len(data))
        except Exception as e:
            print("fail", q["id"], e)


if __name__ == "__main__":
    main()
