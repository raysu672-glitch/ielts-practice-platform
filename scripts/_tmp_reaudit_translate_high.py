#!/usr/bin/env python3
"""复核已修复的 8 条 high 严重句子。"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "sources" / "juzifanyixin" / "index.html"
OUT = ROOT / "_sim_out" / "translate_high_reaudit.md"
IDS = [24, 38, 43, 70, 98, 104, 110, 111]


def load_ai_env() -> dict[str, str]:
    env = {}
    for line in (ROOT / "config" / "ai.env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


SYSTEM = """你是雅思写作翻译教材编辑。这些句子刚被人工修订，请严格复核每一步：
1) 该步中文与英文是否语义对齐；
2) 步骤递进是否合理；
3) fullChinese / finalEnglish 是否与末步一致。
只输出 JSON 数组。有问题：
{"id":句id,"step":步骤号或0表示全文,"severity":"high|medium|low","issue":"...","suggest":"..."}
若全部通过，输出 []。不要为合理的教学简化过度挑刺。"""


def fmt(s: dict) -> str:
    lines = [
        f"id={s['id']}",
        f"fullChinese={s.get('fullChinese')}",
        f"finalEnglish={s.get('finalEnglish')}",
        "steps:",
    ]
    for i, st in enumerate(s["steps"], 1):
        lines.append(f"  {i}. [{st['label']}] CN={st['chinese']} || EN={st['correctAnswer']}")
    return "\n".join(lines)


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    m = re.search(r"const translationData = (\[[\s\S]*?\n\]);", html)
    data = json.loads(m.group(1))
    subset = [s for s in data if s["id"] in IDS]
    env = load_ai_env()
    body = {
        "model": env.get("AI_MODEL") or "deepseek-chat",
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": "请复核下列已修订句子：\n\n"
                + "\n\n----\n\n".join(fmt(s) for s in subset),
            },
        ],
    }
    req = urllib.request.Request(
        env.get("AI_BASE_URL", "https://api.deepseek.com").rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + env["AI_API_KEY"],
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
    print("RAW:\n", raw)
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    start, end = text.find("["), text.rfind("]")
    issues = json.loads(text[start : end + 1]) if start >= 0 else []

    lines = ["# 高严重 8 句修订后复核", "", f"- 复核句：{IDS}", f"- 仍报问题：{len(issues)}", ""]
    if not issues:
        lines.append("全部通过：这 8 句逐步中英对齐与递进逻辑未再检出高/中严重问题。")
    else:
        for it in issues:
            lines.append(f"### #{it.get('id')} step={it.get('step')} [{it.get('severity')}]")
            lines.append(f"- {it.get('issue')}")
            if it.get("suggest"):
                lines.append(f"- 建议：{it.get('suggest')}")
            lines.append("")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT}")
    print(f"remaining issues: {len(issues)}")


if __name__ == "__main__":
    main()
