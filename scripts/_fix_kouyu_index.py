# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "sources" / "kouyulianxi" / "index.html"

raw = subprocess.check_output(
    ["git", "show", "a947acf:sources/kouyulianxi/index.html"],
    cwd=str(ROOT),
)
text = raw.decode("utf-8")

needle = (
    '<div class="nav-right" id="p1NavRight">\n'
    '            <button class="nav-btn" id="modeToggle"'
)
insert = (
    '<div class="nav-right" id="p1NavRight">\n'
    '            <button type="button" class="nav-btn mobile-only" id="mobileQuestionListBtn" '
    'aria-label="打开题目列表">题目</button>\n'
    '            <button class="nav-btn" id="modeToggle"'
)
text = text.replace(needle, insert)
text = text.replace("style.css?v=20260825p2b", "style.css?v=20260827complex")
text = text.replace("p1-data.js?v=20260825p1d", "p1-data.js?v=20260827d")
text = text.replace("p2-data.js?v=20260825p2b", "p2-data.js?v=20260827d")
text = text.replace("audio/manifest.js?v=20260824b", "audio/manifest.js?v=20260825p1audio")
text = text.replace("app.js?v=20260825p1d", "app.js?v=20260827complex")
text = text.replace("p2-app.js?v=20260825p2b", "p2-app.js?v=20260827complex")

TARGET.write_bytes(text.encode("utf-8"))
assert "口语复合句闯关" in text
assert "选择左侧题目开始练习" in text
print("fixed", TARGET.stat().st_size)
