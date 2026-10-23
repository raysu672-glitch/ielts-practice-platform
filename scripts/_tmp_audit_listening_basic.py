"""核查 listening_basic 题库与音频（dictation_threshold = check_first）。只读。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

mods = (ROOT / "sources" / "tinglidanciceshi" / "js" / "modules.js").read_text(
    encoding="utf-8", errors="replace"
)


def grab(name: str) -> list[str]:
    m = re.search(rf"var {name} = \[(.*?)\];", mods, re.S)
    if not m:
        return []
    return re.findall(r'"([^"]*)"', m.group(1))


for name in ("allWords", "allWordsListeningBasic"):
    words = grab(name)
    multi = [w for w in words if " " in w]
    print(f"{name}: 共 {len(words)} 条，含空格的词组 {len(multi)} 条 "
          f"({len(multi)/max(1,len(words))*100:.0f}%)")
    longest = sorted(words, key=len, reverse=True)[:8]
    print("  最长:", ", ".join(longest))
    print("  样例:", ", ".join(words[300:308]))
    print()

# 音频目录
for sub in ("words", "basic_words"):
    d = ROOT / "sources" / "tinglidanciceshi" / "audio" / sub
    n = len(list(d.glob("*"))) if d.exists() else -1
    print(f"audio/{sub}: {'缺失目录' if n < 0 else str(n) + ' 个文件'}")
