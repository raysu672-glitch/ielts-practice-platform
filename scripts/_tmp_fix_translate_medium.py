#!/usr/bin/env python3
"""按用户分工修复 medium：26/33/36/54 改中文；56/65/77/100 不动；其余改英文。"""
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
    # #26 Step1：补上施动者，对齐已有英文
    s = by[26]
    s["steps"][0]["chinese"] = "童年时期，我们被父母和老师教唱歌。"
    s["steps"][0]["keywords"] = [
        "As children (童年时期)",
        "are taught songs (被教唱歌)",
        "by our parents and teachers (由父母和老师)",
    ]

    # #33：中文改为「之一」，对齐 One of
    s = by[33]
    s["steps"][0]["chinese"] = "最明显的例证之一是射击比赛。"
    s["steps"][1]["chinese"] = (
        "最明显的例证之一是射击比赛，【在该项目中，专注于靶心且不受观众干扰的能力远比身体力量更为重要】。"
    )
    s["fullChinese"] = (
        "射击比赛便是最明显的例证之一：在该项目中，专注于靶心且不受观众干扰的能力远比身体力量更为重要。"
    )

    # #36 Step4：理顺中文，对齐 made by hosting...
    s = by[36]
    s["steps"][3]["chinese"] = (
        "【举办这一国际赛事所做出的】另一贡献是能为大多数民众激发对体育运动的兴趣，促使他们增加身体活动量。"
    )
    s["fullChinese"] = (
        "此外，举办这一国际赛事的另一贡献是激发大多数民众对体育运动的兴趣，促使他们增加身体活动量。"
    )

    # #54：去掉「反而」，只保留然而
    s = by[54]
    s["steps"][1]["chinese"] = (
        "【然而，】我认为这种【非传统的】工作方式会引发更多问题。"
    )
    s["fullChinese"] = "然而，我认为这种非传统的工作方式会引发更多问题。"

    # ========== 改英文 ==========
    # #9 key carrier
    s = by[9]
    new9 = (
        "Their adult world will be changing constantly in terms of technology "
        "and the Internet is the key carrier of all the knowledge and information "
        "available in the world today."
    )
    s["finalEnglish"] = new9
    s["steps"][1]["correctAnswer"] = new9
    s["steps"][1]["hint"] = (
        "in terms of technology修饰changing；the key carrier of ... 对应关键载体；"
        "available in the world today是后置定语"
    )
    s["steps"][1]["keywords"] = [
        "in terms of (在…领域)",
        "key carrier (关键载体)",
        "available (可获取的)",
        "knowledge and information (知识与信息)",
    ]

    # #11 with
    s = by[11]
    replace_en_all(s, "connecting alien life forms", "connecting with alien life forms")
    s["steps"][1]["hint"] = (
        "from the perspective of some optimists是观点状语；"
        "to connecting with alien life forms说明益处来源；great修饰benefits"
    )
    s["steps"][1]["keywords"] = [
        "from the perspective of (从…的角度来看)",
        "optimists (乐观主义者)",
        "connecting with (与…建立联系)",
        "alien life forms (外星生命体)",
        "great (巨大的)",
    ]

    # #17 cultivate next generation
    s = by[17]
    old17 = (
        "which contributes a healthier generation of population to the development of a country."
    )
    new17 = (
        "which helps cultivate a healthier next generation for the country's development."
    )
    replace_en_all(s, old17, new17)
    s["steps"][3]["hint"] = "which引导非限制性定语从句，helps cultivate对应培养出"
    s["steps"][3]["keywords"] = [
        "which helps cultivate (从而培养出)",
        "healthier next generation (更健康的下一代)",
    ]

    # #20 I must admit（末步与全文）
    s = by[20]
    s["finalEnglish"] = s["finalEnglish"].replace("I admit that", "I must admit that", 1)
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]
    # 仅末步体现「必须」；前两步保持 I admit，与其步骤中文一致

    # #21 vividly 提前到 step1/2
    s = by[21]
    s["steps"][0]["correctAnswer"] = (
        "For example, there are books and magazines, vividly picturing how people live their daily lives."
    )
    s["steps"][0]["hint"] = s["steps"][0]["correctAnswer"].rstrip(".")
    s["steps"][0]["keywords"] = [
        "For example (例如)",
        "books and magazines (书籍和杂志)",
        "vividly picturing (生动地描绘)",
        "live their daily lives (生活)",
    ]
    s["steps"][1]["correctAnswer"] = (
        "For example, there are thousands of books and magazines, such as Lonely Planet, "
        "vividly picturing how people live their daily lives."
    )
    # step3 已有 vividly，保持；高亮【生动地】在递进上略弱，但用户要求改英文

    # #22 local
    s = by[22]
    replace_en_all(s, "about their food tradition", "about local food tradition")
    s["steps"][1]["hint"] = (
        "about local food tradition and festival celebration修饰Information；"
        "at almost no cost of time and money是方式状语"
    )

    # #23 immersive + also
    s = by[23]
    s["finalEnglish"] = (
        "In a similar way, watching movies can also allow viewers to immersively experience "
        "a lifestyle totally different from their own."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = (
        "can also allow viewers to immersively experience 对应也能身临其境地体验；"
        "totally different from their own修饰lifestyle"
    )
    s["steps"][1]["keywords"] = [
        "can also (也能)",
        "immersively experience (身临其境地体验)",
        "totally different from (与…截然不同的)",
        "their own (自身的)",
    ]

    # #35 remove in cash
    s = by[35]
    replace_en_all(s, "billions of dollars in cash", "billions of dollars in economic benefits")
    s["steps"][2]["keywords"] = [
        "both of which (这两项活动均)",
        "bring in (带来)",
        "billions of dollars in economic benefits (数十亿美元的经济收益)",
        "create a large number of (创造大量)",
        "job opportunities (就业机会)",
    ]

    # #39 traditional
    s = by[39]
    s["steps"][1]["correctAnswer"] = (
        "This is because traditional performance forms need to be altered."
    )
    s["steps"][1]["hint"] = "traditional performance forms 对应传统表演方式/形式"
    s["steps"][1]["keywords"] = [
        "traditional (传统的)",
        "performance forms (表演形式)",
        "altered (改编)",
    ]
    s["finalEnglish"] = (
        "This is because traditional performance forms need to be altered "
        "to meet the needs of tourists."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]
    s["steps"][2]["chinese"] = (
        "这是因为传统表演形式必须加以改编【以满足游客需求】。"
    )

    # #44 strictly
    s = by[44]
    s["finalEnglish"] = (
        "Private companies' involvement in the research of some technologies "
        "must be strictly restricted."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["keywords"] = [
        "private companies (私营企业)",
        "research (研发)",
        "technologies (技术)",
        "strictly restricted (严格限制)",
    ]

    # #49 significantly
    s = by[49]
    s["finalEnglish"] = (
        "Firstly, working at home can significantly save employees' time."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = "Firstly放句首；significantly对应显著"
    s["steps"][1]["keywords"] = [
        "Firstly (首先)",
        "significantly (显著)",
    ]
    # step1 仍用原句，与「显著」未出现的中文一致

    # #58 remove disturbed
    s = by[58]
    replace_en_all(s, "distracted and disturbed by", "distracted by")
    s["steps"][0]["keywords"] = [
        "distracted (分散注意力)",
        "many things (许多事物)",
    ]
    s["steps"][1]["keywords"] = [
        "such as (例如)",
        "snacks (零食)",
        "gadgets (电子设备)",
        "visitors (访客)",
    ]

    # #60 effectively — 两步都有「有效」
    s = by[60]
    replace_en_all(
        s,
        "communicate with others in real life",
        "communicate effectively with others in real life",
    )
    s["steps"][0]["keywords"] = [
        "difficult (困难的)",
        "communicate effectively (有效交流)",
        "in real life (在现实生活中)",
    ]

    # #67 去掉英文多余的 some people say / now
    s = by[67]
    s["steps"][0]["correctAnswer"] = (
        "There are two reasons why people are more dependent on each other."
    )
    s["steps"][0]["hint"] = s["steps"][0]["correctAnswer"].rstrip(".")
    s["steps"][0]["keywords"] = [
        "two reasons (两个原因)",
        "dependent on each other (彼此依赖)",
    ]
    s["finalEnglish"] = (
        "On the one hand, there are two reasons why people are more dependent on each other."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]

    # #75 and + even greater
    s = by[75]
    s["finalEnglish"] = (
        "Such a negative emotion is difficult to deal with even for adults, "
        "and for young children it is an even greater challenge."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = (
        "and 表递进；an even greater challenge 对应更是巨大的挑战"
    )
    s["steps"][1]["keywords"] = [
        "and (递进)",
        "even greater challenge (更巨大的挑战)",
        "young children (年幼的孩子)",
    ]

    # #84 in advance（step3/4）
    s = by[84]
    replace_en_all(
        s,
        "if tourists make a precise plan to pay a visit",
        "if tourists make a precise plan in advance to pay a visit",
    )
    # also In addition version
    replace_en_all(
        s,
        "if tourists make a precise plan in advance to pay a visit",
        "if tourists make a precise plan in advance to pay a visit",
    )
    s["steps"][2]["keywords"] = [
        "if (如果)",
        "precise plan in advance (提前制定详细计划)",
        "during festivals (在节日期间)",
    ]

    # #86 residents and businesses
    s = by[86]
    old86 = "to meet the needs of more space for either residence or business"
    new86 = "to meet residents' and businesses' need for more space"
    # step3 still has residence or business with matching Chinese — only step4/final change the ending
    s["finalEnglish"] = (
        "As more and more people choose to live and work in big cities, "
        "the government has to keep building modern high-rise buildings "
        "to meet residents' and businesses' need for more space."
    )
    s["steps"][3]["correctAnswer"] = s["finalEnglish"]
    # step3 Chinese is 无论是居住还是商业 — keep step3 EN as is

    # #87 gradual
    s = by[87]
    s["steps"][1]["correctAnswer"] = (
        "As a result, there has been a gradual decrease in the number of traditional buildings."
    )
    s["steps"][1]["hint"] = "As a result表结论；gradual对应逐渐"
    s["steps"][1]["keywords"] = [
        "As a result (结果是/结论是)",
        "gradual decrease (逐渐减少)",
    ]
    s["finalEnglish"] = (
        "As a result, there has been a gradual decrease in the number of traditional buildings, "
        "which leads to the consequence that a city does not look unique anymore."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]

    # #97 merely + 去掉 for the children（全文无此信息）
    s = by[97]
    s["steps"][1]["chinese"] = "这些活动绝非【只是】浪费时间。"
    s["steps"][1]["correctAnswer"] = (
        "Such activities are far from being merely a waste of time."
    )
    s["steps"][1]["hint"] = "merely对应只是"
    s["steps"][1]["keywords"] = ["merely (只是)"]
    s["steps"][2]["chinese"] = (
        "这些活动绝非只是浪费时间，【因为它们并不涉及学业内容】。"
    )
    s["finalEnglish"] = (
        "Such activities are far from being merely a waste of time "
        "simply because they are not academic."
    )
    s["steps"][2]["correctAnswer"] = s["finalEnglish"]
    # 注：#97 去掉「对孩子们而言」属于改中文；用户说其余改英文。
    # 但 for the children 不在 fullChinese，改英文删除更合适；步骤中文同步去掉以免残留。

    # #105 remove as
    s = by[105]
    s["finalEnglish"] = (
        "As a result, no one would feel a sense of superiority or being prejudiced."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]

    # #109 without restriction
    s = by[109]
    s["finalEnglish"] = (
        "They are allowed to have whatever they want and to behave as they please, "
        "without any restriction."
    )
    s["steps"][1]["correctAnswer"] = s["finalEnglish"]
    s["steps"][1]["hint"] = (
        "behave as they please 对应随心所欲；without any restriction 对应不受任何约束"
    )
    s["steps"][1]["keywords"] = [
        "behave as they please (随心所欲)",
        "without any restriction (不受任何约束)",
    ]

    # 写回
    new_json = json.dumps(data, ensure_ascii=False, indent=2)
    HTML.write_text(html[: m.start(2)] + new_json + html[m.end(2) :], encoding="utf-8")

    changed_cn = [26, 33, 36, 54]
    changed_en = [
        9, 11, 17, 20, 21, 22, 23, 35, 39, 44, 49, 58, 60, 67, 75, 84, 86, 87, 97, 105, 109
    ]
    skipped = [56, 65, 77, 100]
    print("CN fixed:", changed_cn)
    print("EN fixed:", changed_en)
    print("skipped:", skipped)
    print("also synced CN on #97 (removed 对孩子们而言 to match EN/fullChinese)")


if __name__ == "__main__":
    main()
