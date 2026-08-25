# -*- coding: utf-8 -*-
"""Per-question complex-sentence frame hints for P1 (steps 2–4)."""
from __future__ import annotations

from typing import Any

Frame = dict[str, str]

# Category defaults (step index 1–3 = UI steps 2–4)
_CAT_DEFAULT: dict[str, dict[int, Frame]] = {
    "shishi": {
        1: {
            "name": "句型4 which / 句型5 to do",
            "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
            "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的",
        },
        2: {
            "name": "句型6 Whenever / As long as",
            "pattern": "Whenever / As long as I ______, I ______.",
            "tip": "第3步：时间/条件状语，交代什么时候会做",
        },
        3: {
            "name": "句型1B / 句型2 I find",
            "pattern": "I find it ______ to ______. / I find this ______.",
            "tip": "第4步：形式宾语或宾补，收束感受",
        },
    },
    "xihao": {
        1: {
            "name": "句型6 Whenever / 句型3 for the reason that",
            "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
            "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since",
        },
        2: {
            "name": "句型5 to do 目的状语",
            "pattern": "I am crazy about ______ to ______.",
            "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）",
        },
        3: {
            "name": "句型2 + 句型4 I find..., which",
            "pattern": "I find this activity ______, which ______.",
            "tip": "第4步：宾补写感受，再用 which 补放松/收获",
        },
    },
    "xingwei": {
        1: {
            "name": "句型3 for the reason that / since / as",
            "pattern": "For the reason that / Since ______, I ______.",
            "tip": "第2步：高级原因状语，替换普通 because",
        },
        2: {
            "name": "句型1A It is + adj. + for me to do",
            "pattern": "It is ______ for me to ______.",
            "tip": "第3步：形式主语描述时间线里的行为",
        },
        3: {
            "name": "句型7 can be seen / regarded as",
            "pattern": "______ can be seen / regarded as ______.",
            "tip": "第4步：被动语态收束影响，更客观",
        },
    },
    "guandian": {
        1: {
            "name": "句型3 since + 句型5 to do",
            "pattern": "Since ______, people / I ______ to ______.",
            "tip": "第2步：since/for the reason that 给原因，to do 表目的",
        },
        2: {
            "name": "句型4 which 补充说明",
            "pattern": "..., which ______.",
            "tip": "第3步：非限定定语从句，补作用或影响",
        },
        3: {
            "name": "句型1B I find it + adj. + to do",
            "pattern": "I / they find it ______ to ______.",
            "tip": "第4步：形式宾语收束感受或普遍看法",
        },
    },
    "duibi": {
        1: {
            "name": "句型7 regarded as + 句型5 to do",
            "pattern": "As for A, ______ is regarded as ______ to ______.",
            "tip": "第2步：选项1用被动 + 目的状语写特点与作用",
        },
        2: {
            "name": "句型1B find it + adj. + to do",
            "pattern": "By contrast, regarding B, they find it ______ to ______.",
            "tip": "第3步：选项2用形式宾语对比难点/偏好",
        },
        3: {
            "name": "句型2 I find + 句型4 which",
            "pattern": "I find ______ more ______, which ______.",
            "tip": "第4步：个人偏好 + which 补一句理由",
        },
    },
}

_PAST_CHILD = {
    1: {
        "name": "过去时 When I was...",
        "pattern": "When I was a child / little, I ______.",
        "tip": "第2步：童年题用过去时，别套 Whenever",
    },
    2: {
        "name": "Back then / At that time",
        "pattern": "Back then / At that time, I ______.",
        "tip": "第3步：承接童年时间线",
    },
}

_WHY = {
    1: {
        "name": "句型3 for the reason that / since",
        "pattern": "I chose it for the reason that / since ______.",
        "tip": "第2步：Why 题直接给原因状语",
    },
}

_FUTURE = {
    1: {
        "name": "句型5 plan to / hope to",
        "pattern": "I plan / hope to ______ in the future.",
        "tip": "第2步：将来计划用 plan to / hope to",
    },
    2: {
        "name": "After I graduate / In a few years",
        "pattern": "After I graduate / In a few years, I ______.",
        "tip": "第3步：时间线落到毕业后或几年后",
    },
}

_DESCRIBE = {
    1: {
        "name": "句型4 which 描述细节",
        "pattern": "It is ______, which ______.",
        "tip": "第2步：Describe 题用 which 补一句细节",
    },
}

_COMPARE_PREF = {
    3: {
        "name": "句型2 I prefer + 句型4 which",
        "pattern": "I prefer ______, which ______.",
        "tip": "第4步：对比收束用 prefer + which 给理由",
    },
}

_HOW_OFTEN = {
    2: {
        "name": "句型6 Whenever / 频率副词",
        "pattern": "Whenever I ______ / I ______ quite often.",
        "tip": "第3步：频次题用 Whenever 或 often / from time to time",
    },
}

_WHAT_DO = {
    2: {
        "name": "句型1A It is + adj. + to do",
        "pattern": "It is ______ for me to ______ when ______.",
        "tip": "第3步：What do you do 题用形式主语描述具体行为",
    },
}


def _match(qtext: str) -> dict[int, Frame]:
    ql = qtext.lower().strip()
    o: dict[int, Frame] = {}

    if any(
        x in ql
        for x in (
            "when you were a kid",
            "when you were little",
            "when you were young",
            "in your childhood",
            "when you were a child",
        )
    ):
        o.update(_PAST_CHILD)

    if ql.startswith("why ") or " why " in ql:
        o.update(_WHY)

    if any(x in ql for x in ("will you", "in the future", "next five years", "would you like to")):
        o.update(_FUTURE)

    if ql.startswith("please describe") or ql.startswith("can you describe") or "describe the" in ql:
        o.update(_DESCRIBE)

    if any(x in ql for x in ("how often", "do you often", "how frequently")):
        o.update(_HOW_OFTEN)

    if ql.startswith("what do you usually") or ql.startswith("what do you do when"):
        o.update(_WHAT_DO)

    if any(x in ql for x in ("rather", "prefer", " or ", "compared with", "difference between")):
        o.update(_COMPARE_PREF)

    if "do you think" in ql or "is it important" in ql:
        o[1] = {
            "name": "句型3 In my view / since",
            "pattern": "In my view, ______ since ______.",
            "tip": "第2步：观点题先亮态度，since 给理由",
        }

    if "have you ever" in ql:
        o[1] = {
            "name": "句型4 which 经历举例",
            "pattern": "Yes, I ______, which ______.",
            "tip": "第2步：Have you ever 用经历 + which 补感受",
        }

    if ql.startswith("what ") and any(x in ql for x in ("types", "kinds", "sorts")):
        o[1] = {
            "name": "句型2 I prefer / am keen on",
            "pattern": "I prefer / am keen on ______ because ______.",
            "tip": "第2步：类型题用 prefer / keen on + 简短原因",
        }

    if "who helps" in ql or "in what way" in ql:
        o[1] = {
            "name": "句型4 who + which",
            "pattern": "______ helps me the most, which ______.",
            "tip": "第2步：人物题用 who + which 补具体帮助",
        }

    if "traffic jam" in ql:
        o[2] = {
            "name": "句型6 While waiting / During rush hour",
            "pattern": "While waiting / During rush hour, I ______.",
            "tip": "第3步：堵车场景用 While waiting 描述当下行为",
        }

    return o


def resolve_frames(cat_id: str, qtext: str) -> dict[str, Frame]:
    """Return frames keyed by step index string '1'|'2'|'3' for UI steps 2–4."""
    base = dict(_CAT_DEFAULT.get(cat_id, _CAT_DEFAULT["shishi"]))
    overrides = _match(qtext)
    merged = {**base, **overrides}
    return {str(k): v for k, v in merged.items() if k in (1, 2, 3)}
