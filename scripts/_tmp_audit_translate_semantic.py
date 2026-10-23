#!/usr/bin/env python3
"""用统一 AI 配置，按句语义复核每一步中英是否对齐、递进是否合理。"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_sim_out/translate_steps_audit_raw.json").read_text(encoding="utf-8"))
OUT = ROOT / "_sim_out/translate_steps_semantic_report.md"
OUT_JSON = ROOT / "_sim_out/translate_steps_semantic.json"


def load_ai_env() -> dict[str, str]:
    env = {}
    p = ROOT / "config" / "ai.env"
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


SYSTEM = """你是雅思写作翻译教材编辑。给定一句多步骤中译英练习，检查「每一步」：
1) 该步中文与英文 correctAnswer 语义是否对齐（允许教学性简化，但关键意思不能丢/不能明显错译）；
2) 步骤之间是否合理递进（后一步在前一步基础上扩展，不应删掉前步已有的核心信息，也不应中文已写明却英文缺失）；
3) 高亮【】新增内容是否在英文中有对应增补。

只输出 JSON 数组，不要 markdown。每条问题格式：
{"id":句id,"step":步骤号从1起,"severity":"high|medium|low","issue":"一句话说明问题","suggest":"可选：建议改成什么"}
若该句完全没问题，输出 []。
不要为代词 them/they 指代 children、be likely / more likely、even / even if 等合理对应报 low 噪点。
只报真正的中英不对齐或递进逻辑错误。"""


def chat(env: dict, user: str) -> str:
    base = env.get("AI_BASE_URL", "https://api.deepseek.com").rstrip("/")
    url = base + "/chat/completions"
    model = env.get("AI_MODEL") or "deepseek-chat"
    body = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + env["AI_API_KEY"],
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def parse_issues(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    # find array
    start = text.find("[")
    end = text.rfind("]")
    if start < 0 or end < 0:
        return []
    try:
        data = json.loads(text[start : end + 1])
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def fmt_sentence(s: dict) -> str:
    lines = [
        f"id={s['id']} category={s.get('category')}",
        f"fullChinese={s.get('fullChinese')}",
        f"finalEnglish={s.get('finalEnglish')}",
        "steps:",
    ]
    for i, st in enumerate(s.get("steps") or [], 1):
        lines.append(
            f"  {i}. [{st.get('label')}] CN={st.get('chinese')} || EN={st.get('correctAnswer')} || hint={st.get('hint')} || kw={st.get('keywords')}"
        )
    return "\n".join(lines)


def main() -> None:
    env = load_ai_env()
    if not env.get("AI_API_KEY") or "your_" in env.get("AI_API_KEY", ""):
        raise SystemExit("AI_API_KEY 未配置")

    # 每批 8 句，控制上下文
    batch_size = 8
    all_issues: list[dict] = []
    errors: list[str] = []

    for start in range(0, len(DATA), batch_size):
        batch = DATA[start : start + batch_size]
        user = "请检查下列句子（可多句），合并输出一个 JSON 数组：\n\n" + "\n\n----\n\n".join(
            fmt_sentence(s) for s in batch
        )
        print(f"batch {start // batch_size + 1}/{(len(DATA) + batch_size - 1) // batch_size} ids {[s['id'] for s in batch]} ...", flush=True)
        try:
            raw = chat(env, user)
            issues = parse_issues(raw)
            # 只保留本批 id
            ids = {s["id"] for s in batch}
            issues = [x for x in issues if isinstance(x, dict) and x.get("id") in ids]
            all_issues.extend(issues)
            print(f"  -> {len(issues)} issues", flush=True)
        except Exception as exc:  # noqa: BLE001
            msg = f"batch {[s['id'] for s in batch]} failed: {exc}"
            print("  !!", msg, flush=True)
            errors.append(msg)
        time.sleep(0.4)

    # 排序
    sev_rank = {"high": 0, "medium": 1, "low": 2}
    all_issues.sort(key=lambda x: (sev_rank.get(str(x.get("severity")), 9), x.get("id", 0), x.get("step", 0)))

    by_sev = {"high": [], "medium": [], "low": []}
    for it in all_issues:
        by_sev.setdefault(str(it.get("severity") or "low"), []).append(it)

    lines = [
        "# 句子翻译逐步语义审计（AI）",
        "",
        f"- 句数：{len(DATA)}",
        f"- 步骤：{sum(len(s['steps']) for s in DATA)}",
        f"- 问题条数：{len(all_issues)}（high={len(by_sev.get('high', []))} medium={len(by_sev.get('medium', []))} low={len(by_sev.get('low', []))}）",
        f"- API 失败批次：{len(errors)}",
        "",
    ]
    for sev in ("high", "medium", "low"):
        items = by_sev.get(sev) or []
        lines.append(f"## {sev.upper()}（{len(items)}）")
        lines.append("")
        if not items:
            lines.append("（无）")
            lines.append("")
            continue
        for it in items:
            sid, step = it.get("id"), it.get("step")
            # attach CN/EN
            sent = next((s for s in DATA if s["id"] == sid), None)
            cn = en = ""
            if sent and isinstance(step, int) and 1 <= step <= len(sent["steps"]):
                st = sent["steps"][step - 1]
                cn, en = st.get("chinese", ""), st.get("correctAnswer", "")
            lines.append(f"### #{sid} Step {step}")
            if cn:
                lines.append(f"- 中：{cn}")
            if en:
                lines.append(f"- 英：{en}")
            lines.append(f"- 问题：{it.get('issue')}")
            if it.get("suggest"):
                lines.append(f"- 建议：{it.get('suggest')}")
            lines.append("")

    if errors:
        lines.append("## API 错误")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps({"issues": all_issues, "errors": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT}")
    print(f"wrote {OUT_JSON}")
    print(
        f"summary high={len(by_sev.get('high', []))} medium={len(by_sev.get('medium', []))} low={len(by_sev.get('low', []))}"
    )


if __name__ == "__main__":
    main()
