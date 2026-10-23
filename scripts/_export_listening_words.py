#!/usr/bin/env python3
"""把网站现有听力词表导出成一个 Excel（可重复运行）。

数据来源是页面实际加载的常量，因此导出结果 = 线上所见：
  sources/tinglidanciceshi/listening.html        const ALL_WORDS  -> 听力1000词   (module_type=dictation)
  sources/tinglidanciceshi/listening_basic.html  const ALL_WORDS  -> 听力基础词汇 (module_type=listening_basic)

用法
----
  python scripts/_export_listening_words.py
  python scripts/_export_listening_words.py --out D:/tmp/听力单词表.xlsx

说明：本脚本只读源码 + 写 xlsx，不改动仓库任何文件。
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "tinglidanciceshi"
DEFAULT_OUT = Path.home() / "Downloads" / "听力单词表.xlsx"

# (工作表名, 源文件, 音频目录名, 任务系统 unit_id 前缀)
SPECS = [
    ("听力1000词(dictation)", "listening.html", "words", "dictation_u"),
    ("听力基础词汇(listening_basic)", "listening_basic.html", "basic_words", "listening_basic_u"),
]


def extract_all_words(html_path: Path) -> list[dict]:
    """从 HTML 里取出 const ALL_WORDS = [...]（按括号配平截取，再交给 json 解析）。"""
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"const\s+ALL_WORDS\s*=\s*", text)
    if not m:
        raise SystemExit(f"{html_path.name}: 找不到 ALL_WORDS 定义")
    start = text.index("[", m.end())
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                data = json.loads(text[start : i + 1])
                if not isinstance(data, list):
                    raise SystemExit(f"{html_path.name}: ALL_WORDS 不是数组")
                return data
    raise SystemExit(f"{html_path.name}: ALL_WORDS 数组没有闭合")


def words_per_group(html_path: Path) -> int:
    m = re.search(r"const\s+WORDS_PER_GROUP\s*=\s*(\d+)", html_path.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 0


def mode_hint(html_path: Path) -> str:
    """抓页面里 __taskMode.module 之类的口径提示（拿不到就留空）。"""
    m = re.search(r"const\s+ALL_WORDS", html_path.read_text(encoding="utf-8"))
    return "listening" if m else ""


def build_sheet(ws, words: list[dict], per_group: int, has_pos: bool, unit_prefix: str) -> int:
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    header = ["序号", "分组", "任务单元", "组内序号", "单词", "音标"]
    if has_pos:
        header.append("词性")
    header += ["释义"]

    fill = PatternFill("solid", fgColor="DDEBF7")
    bold = Font(bold=True)
    ws.append(header)
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = fill
        cell.font = bold
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for idx, w in enumerate(words, 1):
        word = (w.get("word") or "").strip()
        group = (idx - 1) // per_group + 1 if per_group else 0
        row = [
            idx,
            group,
            f"{unit_prefix}{group:02d}" if per_group else "",
            (idx - 1) % per_group + 1 if per_group else "",
            word,
            (w.get("phonetic") or "").strip(),
        ]
        if has_pos:
            row.append((w.get("pos") or "").strip())
        row.append((w.get("meaning") or "").strip())
        ws.append(row)

    widths = [6, 6, 20, 8, 26, 22]
    if has_pos:
        widths.append(6)
    widths += [44]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(header))}{len(words) + 1}"
    return len(header)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出 xlsx 路径")
    args = ap.parse_args()

    from openpyxl import Workbook

    wb = Workbook()
    wb.remove(wb.active)
    report = []

    for sheet_name, file_name, audio_dir, unit_prefix in SPECS:
        path = SRC / file_name
        words = extract_all_words(path)
        per_group = words_per_group(path)
        has_pos = any((w.get("pos") or "").strip() for w in words)
        ws = wb.create_sheet(sheet_name[:31])
        cols = build_sheet(ws, words, per_group, has_pos, unit_prefix)

        audio_path = SRC / "audio" / audio_dir
        have = {f.name for f in audio_path.glob("*.mp3")} if audio_path.is_dir() else set()
        want = {f"{(w.get('word') or '').strip()}.mp3" for w in words}
        report.append(
            {
                "sheet": sheet_name,
                "source": file_name,
                "words": len(words),
                "per_group": per_group,
                "cols": cols,
                "audio_missing": sorted(want - have),
                "audio_orphan": sorted(have - want) if have else [],
                "dup": len(words) - len({(w.get("word") or "").strip().lower() for w in words}),
                "no_meaning": sum(1 for w in words if not (w.get("meaning") or "").strip()),
                "no_phonetic": sum(1 for w in words if not (w.get("phonetic") or "").strip()),
            }
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)

    print(f"已生成 {out}  ({out.stat().st_size / 1024:.1f} KB)")
    for r in report:
        print(f"  [{r['sheet']}] 源 {r['source']}：{r['words']} 词 / 每组 {r['per_group']} / {r['cols']} 列")
        print(
            f"      重复词 {r['dup']} · 无释义 {r['no_meaning']} · 无音标 {r['no_phonetic']} · "
            f"缺音频 {len(r['audio_missing'])} · 多余音频 {len(r['audio_orphan'])}"
        )
        if r["audio_missing"]:
            print(f"      缺音频示例：{r['audio_missing'][:6]}")
        if r["audio_orphan"]:
            print(f"      多余音频示例：{r['audio_orphan'][:6]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
