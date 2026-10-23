"""One-off: run student checkup digest + AI, print analysis only."""
from __future__ import annotations

import json
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ai_config import ai_settings, load_ai_env  # noqa: E402
from teacher_api import (  # noqa: E402
    build_student_checkup_digest,
    format_student_checkup_prompt,
)

SID = (sys.argv[1] if len(sys.argv) > 1 else "2025001").strip()
DB = Path(sys.argv[2]) if len(sys.argv) > 2 else (ROOT / "data" / "ielts_local.db")
if not DB.is_absolute():
    DB = ROOT / DB


def main() -> None:
    load_ai_env()
    settings = ai_settings()
    if not settings["api_key"]:
        raise SystemExit("AI_API_KEY missing")
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    digest, err = build_student_checkup_digest(conn, SID, days=14)
    conn.close()
    if err:
        raise SystemExit(err)
    assert digest is not None
    prompt = format_student_checkup_prompt(digest)
    question = (
        "请给该生做全面学习体检：当前学习状态、进度、学习态度（仅基于行为推断），"
        "薄弱点，以及接下来 7 天可执行方案。证据不足请标明。"
    )
    upstream_body = {
        "model": settings["model"],
        "max_tokens": 2500,
        "temperature": 0.2,
        # deepseek-flash 默认 thinking 会吃光 max_tokens，正文为空
        "thinking": {"type": "disabled"},
        "system": (
            "你是雅思练习平台的教师助教。根据提供的学生数据摘要写学习体检报告。"
            "只依据摘要中的数据下结论，不要编造未出现的事实。"
            "态度只能做行为推断，不做心理诊断。"
            "方案只给老师参考，不要声称已自动改计划。"
            "用简洁中文：先结论（状态/进度/态度），再薄弱点，再接下来7天建议。"
        ),
        "messages": [
            {
                "role": "user",
                "content": f"教师问题：{question}\n\n学生数据摘要：\n{prompt}",
            }
        ],
    }
    target = settings["base_url"].rstrip("/") + "/anthropic/v1/messages"
    req = urllib.request.Request(
        target,
        data=json.dumps(upstream_body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": settings["api_key"],
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            upstream = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"AI HTTP {exc.code}: {exc.read()[:500]!r}") from exc

    parts = []
    content = upstream.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
    analysis = "\n".join(p for p in parts if p).strip()
    stu = digest.get("student") or {}
    study = digest.get("study") or {}
    header = (
        f"=== 体检对象 ===\n"
        f"{stu.get('student_id')} {stu.get('name')} 目标{stu.get('target_score')}\n"
        f"近窗投入：场次{study.get('session_count')} 约{study.get('total_minutes')}分钟 "
        f"测试{study.get('test_count')} 达标{study.get('pass_count')} "
        f"错词{study.get('unmastered_wrong_words')}\n"
        f"=== AI 报告 ===\n"
    )
    out = header + (analysis or "(空报告)")
    out_path = ROOT / "_sim_out" / f"checkup_{SID}.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print(out)
    print(f"\n(已写入 {out_path})")


if __name__ == "__main__":
    main()
