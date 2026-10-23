#!/usr/bin/env python3
"""LOW 修复：2/3/12/13/81/103 改中文；其余改英文（#76 步骤笔误顺手改中文）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "sources" / "juzifanyixin" / "index.html"


def replace_en_all(s: dict, old: str, new: str) -> None:
    s["finalEnglish"] = s["finalEnglish"].replace(old, new)
    for st in s["steps"]:
        st["correctAnswer"] = st["correctAnswer"].replace(old, new)
        if st.get("hint"):
            st["hint"] = st["hint"].replace(old, new)


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    m = re.search(r"(const translationData = )(\[[\s\S]*?\n\]);", html)
    data = json.loads(m.group(2))
    by = {s["id"]: s for s in data}

    # ========== 改中文 ==========
    # #2 FaceTime
    s = by[2]
    s["steps"][2]["chinese"] = (
        "例如，留学的学生不会受到思乡之情带来的困扰，"
        "【因为他们可以通过如FaceTime等即时通讯工具与家人保持日常联系】。"
    )
    s["steps"][2]["keywords"] = [
        "as (因为)",
        "instant communication tools (即时通讯工具)",
        "such as FaceTime (如FaceTime等)",
        "on a daily basis (日常地)",
    ]

    # #3 此外
    s = by[3]
    s["steps"][0]["chinese"] = "此外，人们能够建立社区。"

    # #12 对齐 neighbours / lend us
    s = by[12]
    s["steps"][0]["chinese"] = "我们的邻居很可能会把技术分享给我们。"

    # #13 补回环境污染
    s = by[13]
    s["steps"][1]["chinese"] = (
        "例如，环境污染能被消除，【威胁生命的】疾病也能被治愈，"
        "【如果我们能通过外星友人的技术支持实现自身进步】。"
    )

    # #81 假期
    s = by[81]
    s["steps"][0]["chinese"] = "规划假期旅行至关重要。"

    # #103 同伴压力
    s = by[103]
    s["steps"][0]["chinese"] = "要求穿校服有助于减轻同伴压力。"

    # ========== 改英文 ==========
    # #4 effectively
    s = by[4]
    replace_en_all(s, "positively contribute", "effectively contribute")
    s["steps"][1]["hint"] = (
        "effectively修饰contribute；of traditional skills and ways of life修饰the keeping alive"
    )
    s["steps"][1]["keywords"] = [
        "effectively (有效地)",
        "traditional skills (传统技能)",
        "ways of life (生活方式)",
    ]

    # #8 cannot be ignored（对齐不容忽视）
    s = by[8]
    replace_en_all(s, "cannot be denied", "cannot be ignored")
    s["steps"][0]["keywords"] = [
        "In spite of this (尽管如此)",
        "benefits (益处)",
        "cannot be ignored (不容忽视)",
    ]
    s["steps"][1]["keywords"] = [
        "computer skills (计算机技能)",
        "for young children (对幼儿)",
        "obvious (明显的)",
        "ignored (忽视)",
    ]

    # #10 various kinds of equipment
    s = by[10]
    replace_en_all(s, "use the equipment", "use various kinds of equipment")
    s["steps"][1]["keywords"] = [
        "at an early age (尽早)",
        "enthusiastically (热情地)",
        "with confidence (自信地)",
        "various kinds of equipment (各类设备)",
    ]

    # #47 weapons of mass destruction
    s = by[47]
    replace_en_all(
        s,
        "powerful weapons of massive destruction",
        "weapons of mass destruction",
    )
    s["steps"][2]["keywords"] = [
        "purifying radioactive materials (放射性材料纯化)",
        "weapons of mass destruction (大规模杀伤性武器)",
    ]

    # #64 bedtime stories
    s = by[64]
    replace_en_all(s, "bed stories", "bedtime stories")
    s["steps"][1]["keywords"] = [
        "elder brother (哥哥)",
        "bedtime stories (睡前故事)",
        "younger ones (弟弟妹妹)",
    ]

    # #69 often（从出现「往往」的步骤起）
    s = by[69]
    s["steps"][1]["correctAnswer"] = (
        "Young adults often have to rely on their parents for financial help "
        "when renting a flat or buying a house."
    )
    s["steps"][1]["keywords"] = [
        "often (往往)",
        "renting a flat (租房)",
        "buying a house (购房)",
    ]
    s["finalEnglish"] = (
        "Young adults, for example, often have to rely on their parents for "
        "financial help when renting a flat or buying a house."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # #76 also + 修正步骤笔误「颇为难度」
    s = by[76]
    s["steps"][1]["chinese"] = "【此外】，学习外语【也】【颇具】难度。"
    s["finalEnglish"] = (
        "In addition, learning a foreign language is also rather challenging."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "In addition (此外)",
        "also (也)",
        "rather (颇为)",
    ]

    # #77 social isolation（仅 low 举例这一处；impossible 按此前 medium 不改）
    s = by[77]
    replace_en_all(s, "such as isolation and depression", "such as social isolation and depression")
    s["steps"][4]["keywords"] = [
        "such as (例如)",
        "social isolation (社交孤立)",
        "depression (抑郁)",
    ]

    # #80 keen on
    s = by[80]
    replace_en_all(
        s,
        "as they are more addicted to online sharing of gossips and pictures",
        "as they are more keen on sharing gossips and pictures online",
    )
    s["steps"][3]["keywords"] = [
        "as (因为)",
        "keen on (热衷于)",
        "online sharing (在线分享)",
    ]

    # #88 continuously decreasing
    s = by[88]
    s["steps"][1]["correctAnswer"] = (
        "The first reason for students' poor behavior is that the birth rate "
        "is continuously decreasing."
    )
    s["steps"][1]["keywords"] = [
        "poor behavior (行为不良)",
        "continuously decreasing (持续下降)",
    ]
    s["finalEnglish"] = (
        "The first reason for students' poor behavior is that the birth rate "
        "is continuously decreasing so that families are becoming smaller with fewer children."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # #106 can also
    s = by[106]
    s["finalEnglish"] = (
        "In addition, the rule of wearing school uniforms can also keep the campus safe."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "In addition (此外)",
        "can also (还能)",
    ]

    # #108 excessively
    s = by[108]
    s["finalEnglish"] = "These children are often excessively spoilt."
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "often (往往)",
        "excessively (过度)",
    ]

    # #112 natural barrier
    s = by[112]
    s["steps"][1]["correctAnswer"] = (
        "The danger and wilderness of some places set up a natural barrier for ordinary people."
    )
    s["steps"][1]["keywords"] = [
        "of some places (某些地区的)",
        "for ordinary people (对普通人而言)",
        "natural barrier (天然屏障)",
    ]
    s["finalEnglish"] = (
        "The danger and wilderness of some places set up a natural barrier for ordinary people, "
        "which is the reason why TV programs like Man vs Wild enjoy a great popularity."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # #113 tourist destinations
    s = by[113]
    s["finalEnglish"] = (
        "There are some tourist destinations where tourists may be kidnapped or robbed."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "tourist destinations (旅游目的地)",
        "where (在那些地方)",
        "kidnapped (绑架)",
        "robbed (抢劫)",
    ]

    # #114 highly（step1）
    s = by[114]
    s["steps"][0]["correctAnswer"] = (
        "There are also places where trekkers are highly vulnerable to diseases."
    )
    s["steps"][0]["hint"] = (
        "There are also places where trekkers are highly vulnerable to diseases"
    )
    s["steps"][0]["keywords"] = [
        "also (也/还)",
        "trekkers (徒步旅行者)",
        "highly vulnerable to (极易感染)",
    ]

    HTML.write_text(
        html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
        encoding="utf-8",
    )
    print("CN:", [2, 3, 12, 13, 81, 103], "+ #76 typo")
    print(
        "EN:",
        [4, 8, 10, 47, 64, 69, 76, 77, 80, 88, 106, 108, 112, 113, 114],
    )


if __name__ == "__main__":
    main()
