#!/usr/bin/env python3
"""修复句子翻译 high 严重 8 句，并写回 juzifanyixin/index.html。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "sources" / "juzifanyixin" / "index.html"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    m = re.search(r"(const translationData = )(\[[\s\S]*?\n\]);", html)
    if not m:
        raise SystemExit("translationData not found")
    data = json.loads(m.group(2))
    by_id = {s["id"]: s for s in data}

    # ----- #24 -----
    s = by_id[24]
    s["finalEnglish"] = (
        "Indian movies, for example, let people deeply appreciate "
        "how important singing and dancing are to Indian culture."
    )
    s["steps"][0]["correctAnswer"] = (
        "Indian movies let people know how important singing and dancing are."
    )
    s["steps"][0]["hint"] = (
        "Indian movies let people know how important singing and dancing are"
    )
    s["steps"][1]["chinese"] = (
        "印度电影，【例如】，让人们深刻体会到歌唱和舞蹈【对印度文化的】重要性。"
    )
    s["steps"][1]["hint"] = (
        "for example是插入语；deeply appreciate对应深刻体会；to Indian culture对应对印度文化"
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "for example (例如)",
        "deeply appreciate (深刻体会到)",
        "to Indian culture (对印度文化)",
    ]

    # ----- #38 -----
    s = by_id[38]
    s["finalEnglish"] = (
        "Using traditional cultures as money-making tourist attractions "
        "may destroy their authenticity."
    )
    s["steps"][0]["keywords"] = [
        "Using...as... (将…作为…)",
        "traditional cultures (传统文化)",
        "tourist attractions (旅游景点)",
        "may destroy (可能会破坏)",
        "them (指代传统文化)",
    ]
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = (
        "money-making修饰tourist attractions；their authenticity对应原真性"
    )
    s["steps"][1]["keywords"] = [
        "money-making (营利性的)",
        "authenticity (原真性)",
    ]

    # ----- #43 -----
    s = by_id[43]
    s["fullChinese"] = "据信，实现财务目标最有效的方法之一就是频繁更换雇主。"
    s["finalEnglish"] = (
        "It is believed that one of the most effective ways to achieve "
        "financial ambition is to hop from one company to another."
    )
    s["logicExplanation"] = (
        "形式主语 It is believed that + 宾语从句；主语含不定式后置修饰。"
    )
    s["steps"][0]["hint"] = (
        "One of the most effective ways is to hop from one company to another"
    )
    s["steps"][0]["correctAnswer"] = (
        "One of the most effective ways is to hop from one company to another."
    )
    s["steps"][0]["keywords"] = [
        "effective (有效的)",
        "hop from one company to another (频繁更换雇主)",
    ]
    s["steps"][1]["chinese"] = (
        "【据信，】【实现财务目标的】最有效的方法之一就是频繁更换雇主。"
    )
    s["steps"][1]["hint"] = (
        "It is believed that表据信；to achieve financial ambition修饰ways"
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "It is believed that (据信)",
        "achieve (实现)",
        "financial ambition (财务目标)",
    ]

    # ----- #70 -----
    s = by_id[70]
    s["finalEnglish"] = (
        "Housing prices are higher than ever, and if young people relied "
        "entirely on their parents, many of them would be unable to pay "
        "a deposit and mortgage."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = (
        "and连接并列句；if young people relied entirely on their parents 对应"
        "若完全依赖父母；would be unable to 对应无力"
    )
    s["steps"][1]["keywords"] = [
        "relied entirely on their parents (完全依赖父母)",
        "unable to (无力)",
        "deposit (首付款)",
        "mortgage (房贷)",
    ]

    # ----- #98 -----
    s = by_id[98]
    s["finalEnglish"] = (
        "It is important to remember that children need to develop more than "
        "just intellectual skills, and the best way to do this is through "
        "activities such as sports, games and playing with other kids."
    )
    s["steps"][1]["hint"] = (
        "more than just 对应不仅是；such as 表例如"
    )
    s["steps"][1]["correctAnswer"] = (
        "Children need to develop more than just intellectual skills, "
        "and the best way to do this is through activities such as sports, "
        "games and playing with other kids."
    )
    s["steps"][1]["keywords"] = [
        "more than just (不仅是)",
        "intellectual skills (智力技能)",
        "such as (例如)",
    ]
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # ----- #104 -----
    s = by_id[104]
    s["finalEnglish"] = (
        "When everyone in the class is dressed in the same way, they are not "
        "likely to talk about the price and style of clothes."
    )
    s["steps"][0]["hint"] = (
        "They are not likely to talk about the price and style"
    )
    s["steps"][0]["correctAnswer"] = (
        "They are not likely to talk about the price and style."
    )
    s["steps"][0]["keywords"] = [
        "not likely to (不太可能)",
        "talk about (讨论)",
        "price and style (价格和款式)",
    ]
    s["steps"][1]["correctAnswer"] = (
        "They are not likely to talk about the price and style of clothes."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # ----- #110：fullChinese 与步骤/英文不一致，以步骤语义为准改全文中文 -----
    s = by_id[110]
    s["fullChinese"] = "这意味着孩子们成长时缺乏对他人的考虑。"
    # steps/final 已对齐，无需改英文

    # ----- #111：fullChinese 误含上一句内容，改为与步骤一致 -----
    s = by_id[111]
    s["fullChinese"] = (
        "当他们开始上学时，他们尚未学会尊重他人或遵守规则。"
    )

    # 写回：保持可读缩进（与原文件相近的 2 空格）
    new_json = json.dumps(data, ensure_ascii=False, indent=2)
    # 原文件是 const translationData = [...]; 顶层数组每项缩进 2
    html2 = html[: m.start(2)] + new_json + html[m.end(2) :]
    HTML.write_text(html2, encoding="utf-8")
    print("updated", HTML)
    for sid in [24, 38, 43, 70, 98, 104, 110, 111]:
        s = by_id[sid]
        print(f"\n#{sid} fullCN={s['fullChinese']}")
        print(f"     finalEN={s['finalEnglish']}")
        for i, st in enumerate(s["steps"], 1):
            print(f"     {i}. {st['chinese']}")
            print(f"        {st['correctAnswer']}")


if __name__ == "__main__":
    main()
