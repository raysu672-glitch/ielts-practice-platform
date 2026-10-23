#!/usr/bin/env python3
"""Local full student checkup: platform DB + WeCom learning group -> AI report.

Does NOT deploy WeCom data to the server. Output: console + _sim_out/full_checkup_{id}.md
"""

from __future__ import annotations

import argparse
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
from wecom_checkup import (  # noqa: E402
    build_wecom_group_summary,
    format_wecom_summary_prompt,
)

FULL_SYSTEM_PROMPT = """你是雅思练习平台的教师助教，做「平台学习数据 + 企微学习群」联合详版体检。
只依据摘要中的数据下结论，不要编造未出现的事实。
态度只能做行为推断，不做心理诊断。
方案只给老师参考，不要声称已自动改计划。
必须交叉验证平台与企微，并引用摘要中的日期/数字。
企微 multi_pick / 多群时，分群说明并指出统计边界。
尽量详细，可用条目和简单 Markdown 表；每个大段至少 4 条实质证据。

严格按下列标题输出：
## 1. 一眼结论
## 2. 平台进度与效果
（含模块投入明细、计划库存、测试/错题证据）
## 3. 执行节奏与态度（行为推断）
（含日历模式、时段、短会话/打开退出比）
## 4. 学习群表现
（含分群对比、催促/布置/承诺、回复延迟）
## 5. 平台×企微按日对账
（逐条解释「有练无报 / 有报无练 / 双有 / 双无」）
## 6. 风险与证据缺口
## 7. 接下来7天可执行方案
（按天或按优先级列出，可勾选）
"""


def build_cross_check(
    thicker: dict,
    wecom: dict,
) -> list[dict[str, str]]:
    """Day-level reconcile: platform done vs wecom check-in."""
    platform_days = set(thicker.get("platform_done_days") or [])
    # Prefer explicit calendar window days if present
    cal_days = {x.get("date") for x in (thicker.get("daily_calendar") or []) if x.get("date")}
    checkin_days = set((wecom.get("stats") or {}).get("checkin_days") or wecom.get("checkin_days") or [])
    speak_hint = set()
    # union recent calendar + checkin + platform done for coverage
    all_days = sorted(cal_days | platform_days | checkin_days, reverse=True)[:21]
    rows: list[dict[str, str]] = []
    for d in all_days:
        p = d in platform_days
        w = d in checkin_days
        if p and w:
            tag = "双有"
        elif p and not w:
            tag = "有练无报"
        elif w and not p:
            tag = "有报无练"
        else:
            tag = "双无/仅挂账"
        rows.append({"date": d, "platform_done": "Y" if p else "N", "wecom_checkin": "Y" if w else "N", "tag": tag})
        speak_hint.add(d)
    return rows


def latest_aliyun_db(root: Path) -> Path | None:
    backups = root / "backups"
    if not backups.is_dir():
        return None
    cands = sorted(
        backups.glob("aliyun_*/ielts_local.db"),
        key=lambda p: p.parent.name,
        reverse=True,
    )
    return cands[0] if cands else None


def call_ai(prompt: str, *, max_tokens: int = 5000) -> str:
    load_ai_env()
    settings = ai_settings()
    if not settings["api_key"]:
        raise SystemExit("AI_API_KEY missing（config/ai.env）")
    body = {
        "model": settings["model"],
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "thinking": {"type": "disabled"},
        "system": FULL_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
    target = settings["base_url"].rstrip("/") + "/anthropic/v1/messages"
    req = urllib.request.Request(
        target,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
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
        raise SystemExit(f"AI HTTP {exc.code}: {exc.read()[:800]!r}") from exc

    parts: list[str] = []
    content = upstream.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
    analysis = "\n".join(p for p in parts if p).strip()
    if not analysis:
        raise SystemExit(f"AI 返回无正文：{str(upstream)[:500]}")
    return analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="本地全面体检（平台+企微）")
    parser.add_argument("--student-id", required=True)
    parser.add_argument("--db", default="", help="SQLite 路径，默认最近 aliyun 备份")
    parser.add_argument(
        "--wecom-dir",
        default=r"G:\ds harness\wecom-data",
        help="企微解密库目录",
    )
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--skip-ai", action="store_true", help="只打印摘要不调 AI")
    args = parser.parse_args()

    db_path = Path(args.db) if args.db else latest_aliyun_db(ROOT)
    if db_path is None:
        db_path = ROOT / "data" / "ielts_local.db"
    if not db_path.is_file():
        raise SystemExit(f"数据库不存在：{db_path}")

    sid = str(args.student_id).strip()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    digest, err = build_student_checkup_digest(conn, sid, days=args.days)
    conn.close()
    if err:
        raise SystemExit(err)
    assert digest is not None
    name = str((digest.get("student") or {}).get("name") or "")

    wecom = build_wecom_group_summary(
        args.wecom_dir,
        student_name=name,
        days=args.days,
        merge_all_groups=True,
        max_samples=60,
    )
    thicker = digest.get("thicker") or {}
    cross = build_cross_check(thicker, wecom)
    platform_block = format_student_checkup_prompt(digest)
    wecom_block = format_wecom_summary_prompt(wecom)
    cross_lines = ["日期 | 平台有完成 | 群打卡相关 | 对账标签"]
    for row in cross:
        cross_lines.append(
            f"{row['date']} | {row['platform_done']} | {row['wecom_checkin']} | {row['tag']}"
        )
    user_prompt = (
        f"请对学号 {sid}（{name}）做详版全面学习体检。\n\n"
        f"【平台数据摘要】\n{platform_block}\n\n"
        f"【企微学习群摘要】\n{wecom_block}\n\n"
        f"【平台×企微按日对账表】\n" + "\n".join(cross_lines) + "\n"
    )

    header = (
        f"# 全面体检（详版） {sid} {name}\n\n"
        f"- DB: `{db_path}`\n"
        f"- WeCom: `{args.wecom_dir}`\n"
        f"- days: {args.days}\n"
        f"- wecom_match: {wecom.get('match_confidence')} "
        f"groups={len(wecom.get('per_group') or [])} "
        f"{(wecom.get('primary_group') or {}).get('name') or ''}\n\n"
    )

    if args.skip_ai:
        out = header + "## 摘要（未调 AI）\n\n" + user_prompt
    else:
        analysis = call_ai(user_prompt, max_tokens=5000)
        out = header + analysis

    out_dir = ROOT / "_sim_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"full_checkup_{sid}.md"
    out_path.write_text(out, encoding="utf-8")
    print(out)
    print(f"\n(已写入 {out_path})")


if __name__ == "__main__":
    main()
