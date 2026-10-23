"""判分排查（c1）：逐模块核对「判分严格度 vs 达标线 vs 线上实际通过率」。

只读，不改任何库。产出 _sim_out/grading_audit.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = ROOT / "_sim_out" / "grading_audit.md"


def phrases() -> list[tuple[str, str]]:
    html = (ROOT / "sources" / "xiezuocihuoceshi" / "index.html").read_text(
        encoding="utf-8", errors="replace"
    )
    out: list[tuple[str, str]] = []
    for m in re.finditer(r"en\s*:\s*(['\"])(.*?)\1", html, re.S):
        out.append(("", m.group(2)))
    return out


def main() -> None:
    lines: list[str] = ["# 判分排查（c1）", ""]
    allp = phrases()
    bad = [en for _, en in allp if re.search(r"[/()]", en)]
    lines.append("## 1. 写作词伙 `writing_phrase`")
    lines.append(f"- 题库共 **{len(allp)}** 条；答案里含 `/` 或 `()` 的有 **{len(bad)}** 条（{len(bad)/max(1,len(allp))*100:.0f}%）。")
    lines.append("")
    lines.append("`normalize()` 把 `/` `()` **替换成空格**，但标准答案没有同步拆分：")
    lines.append("")
    lines.append("```js")
    lines.append("function normalize(s) {")
    lines.append("  return s.toLowerCase()")
    lines.append("    .replace(/\\s+/g, ' ')")
    lines.append("    .replace(/[\\/\\(\\)]/g, ' ')   // ← a/b 变成 'a b'")
    lines.append("    ...;")
    lines.append("}")
    lines.append("function isCorrect(user, answer) {")
    lines.append("  return normalize(user) === normalize(answer);")
    lines.append("}")
    lines.append("```")
    lines.append("")
    lines.append("于是标准答案变成「a b」，学生填 `a` 或 `b` **都判错**，必须把两个说法")
    lines.append("连着打出来才算对。这类题**永远拿不到分**：")
    lines.append("")
    for en in bad[:20]:
        lines.append(f"  - `{en}` → 规范化成 `{re.sub(r'[/(),;:!?' + chr(39) + ']', ' ', en).lower()}`")
    if len(bad) > 20:
        lines.append(f"  - …另 {len(bad) - 20} 条")
    lines.append("")
    lines.append("## 2. 写作句子翻译 `writing_translate`")
    lines.append("- 判分用 `TranslateMatch.isChineseMatch()`：**逐字全等**。")
    lines.append("  `normalizeChinese()` 只去掉空白与标点，**不做任何同义/语序容错**。")
    lines.append("- 结果：换个说法（哪怕意思完全对）一律 0 分。")
    lines.append("- 线上 11 次提交 **全部 0.0 分**、达标线 70 —— 通过率为 0% 不是学生的问题。")
    lines.append("- 题目是「给中文写英文」还是「给英文写中文」决定难度上限，需要人工确认。")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
