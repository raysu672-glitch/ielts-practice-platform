# -*- coding: utf-8 -*-
"""Per-question complex-sentence frame hints for P1 (steps 2–4).

Each step carries 3 fixed patterns (primary + 2 alts). Within one topic, questions
rotate which pattern is recommended first, so Part 1's 3–4 answers don't all
reuse the same structure.
"""
from __future__ import annotations

from typing import Any

Frame = dict[str, Any]

# Three interchangeable fixed patterns per category × step (UI steps 2–4 → keys 1–3)
_CAT_VARIANTS: dict[str, dict[int, list[Frame]]] = {
    "shishi": {
        1: [
            {
                "name": "句型4 which",
                "pattern": "I ______ (举例/地点), which ______.",
                "tip": "举例后用 which 补结果或感受",
            },
            {
                "name": "句型5 to do",
                "pattern": "I ______ to ______.",
                "tip": "用 to do 交代目的（去哪/做什么）",
            },
            {
                "name": "句型3 since / for the reason that",
                "pattern": "Since / For the reason that ______, I ______.",
                "tip": "需要解释原因时用 since，少用 because",
            },
        ],
        2: [
            {
                "name": "句型6 Whenever / As long as",
                "pattern": "Whenever / As long as I ______, I ______.",
                "tip": "时间/条件状语，交代什么时候会做",
            },
            {
                "name": "频率状语 Most days / From time to time",
                "pattern": "Most days / From time to time, I ______.",
                "tip": "用频率状语换掉反复出现的 Whenever",
            },
            {
                "name": "句型1A It is + adj. + for me to do",
                "pattern": "It is ______ for me to ______.",
                "tip": "形式主语描述习惯行为，听感更稳",
            },
        ],
        3: [
            {
                "name": "句型1B I find it + adj. + to do",
                "pattern": "I find it ______ to ______.",
                "tip": "形式宾语收束感受",
            },
            {
                "name": "句型2 I find this + adj.",
                "pattern": "I find this ______ / Overall, it feels ______.",
                "tip": "宾补收束，或换成 Overall, it feels…",
            },
            {
                "name": "To be honest / This makes me feel",
                "pattern": "To be honest, I would say it is ______. / This makes me feel ______.",
                "tip": "换掉连续的 I find，避免四题结尾同款",
            },
        ],
    },
    "xihao": {
        1: [
            {
                "name": "句型3 for the reason that / since",
                "pattern": "I am keen on ______ for the reason that / since ______.",
                "tip": "喜好+原因，少用 because",
            },
            {
                "name": "句型6 Whenever",
                "pattern": "Whenever I ______, I ______.",
                "tip": "有时间线时用 Whenever 带出习惯",
            },
            {
                "name": "What I like most is…",
                "pattern": "What I like most is ______, because / since ______.",
                "tip": "主词提前，换掉反复的 I am keen on",
            },
        ],
        2: [
            {
                "name": "句型5 to do 目的状语",
                "pattern": "I ______ to ______.",
                "tip": "行为举例时用 to do 交代目的",
            },
            {
                "name": "In my free time / At weekends",
                "pattern": "In my free time / At weekends, I ______.",
                "tip": "用时间状语换掉 crazy about 套话",
            },
            {
                "name": "句型1A It is + adj. + to do",
                "pattern": "It is ______ for me to ______ when ______.",
                "tip": "形式主语写具体行为",
            },
        ],
        3: [
            {
                "name": "句型2 + which",
                "pattern": "I find this activity ______, which ______.",
                "tip": "宾补写感受，再用 which 补收获",
            },
            {
                "name": "It always cheers me up / helps me unwind",
                "pattern": "It always cheers me up / helps me unwind when ______.",
                "tip": "结果导向收束，少重复 I find",
            },
            {
                "name": "Overall, it feels…",
                "pattern": "Overall, it feels ______ and ______.",
                "tip": "短收束，适合连答最后一题",
            },
        ],
    },
    "xingwei": {
        1: [
            {
                "name": "句型3 since / for the reason that",
                "pattern": "Since / For the reason that ______, I ______.",
                "tip": "高级原因状语，替换 because",
            },
            {
                "name": "The main reason is that…",
                "pattern": "The main reason is that ______, so I ______.",
                "tip": "原因前置，换掉连续 Since",
            },
            {
                "name": "句型5 to do",
                "pattern": "I ______ to ______.",
                "tip": "直接用目的状语说明为何养成习惯",
            },
        ],
        2: [
            {
                "name": "句型1A It is + adj. + for me to do",
                "pattern": "It is ______ for me to ______.",
                "tip": "形式主语描述时间线里的行为",
            },
            {
                "name": "句型6 Whenever / While",
                "pattern": "Whenever / While I ______, I ______.",
                "tip": "时间状语写习惯触发点",
            },
            {
                "name": "On weekdays / After class",
                "pattern": "On weekdays / After class, I usually ______.",
                "tip": "用具体时间段替换抽象条件句",
            },
        ],
        3: [
            {
                "name": "句型7 can be seen / regarded as",
                "pattern": "______ can be seen / regarded as ______.",
                "tip": "被动收束影响，更客观",
            },
            {
                "name": "This habit helps me…",
                "pattern": "This habit helps me ______ and also ______.",
                "tip": "主动句写影响，换掉被动套话",
            },
            {
                "name": "As a result…",
                "pattern": "As a result, I feel / become ______.",
                "tip": "结果导向收束",
            },
        ],
    },
    "guandian": {
        1: [
            {
                "name": "句型3 since + to do",
                "pattern": "Since ______, people / I ______ to ______.",
                "tip": "since 给原因，to do 表目的",
            },
            {
                "name": "In my view…",
                "pattern": "In my view, ______ since / for the reason that ______.",
                "tip": "先亮态度再给理由",
            },
            {
                "name": "I would say…",
                "pattern": "I would say ______, mainly because / since ______.",
                "tip": "口语化观点句，换掉连续 Since",
            },
        ],
        2: [
            {
                "name": "句型4 which",
                "pattern": "..., which ______.",
                "tip": "非限定定语从句补作用或影响",
            },
            {
                "name": "This means that…",
                "pattern": "This means that ______.",
                "tip": "用 This means that 换掉 which 堆叠",
            },
            {
                "name": "For example…",
                "pattern": "For example, ______, so ______.",
                "tip": "举例推进观点，适合第二、三问",
            },
        ],
        3: [
            {
                "name": "句型1B find it + adj. + to do",
                "pattern": "I / they find it ______ to ______.",
                "tip": "形式宾语收束感受或普遍看法",
            },
            {
                "name": "That is why…",
                "pattern": "That is why I think ______.",
                "tip": "因果收束，避免每题都以 I find 结尾",
            },
            {
                "name": "Overall / Personally",
                "pattern": "Overall / Personally, I feel it is ______.",
                "tip": "简短态度收束",
            },
        ],
    },
    "duibi": {
        1: [
            {
                "name": "句型7 regarded as + to do",
                "pattern": "As for A, ______ is regarded as ______ to ______.",
                "tip": "选项1：被动 + 目的状语",
            },
            {
                "name": "On the one hand…",
                "pattern": "On the one hand, ______ is ______ because ______.",
                "tip": "一边说清选项1",
            },
            {
                "name": "When it comes to A…",
                "pattern": "When it comes to A, people often ______ to ______.",
                "tip": "话题引入式对比，换掉 As for 套话",
            },
        ],
        2: [
            {
                "name": "By contrast + find it",
                "pattern": "By contrast, regarding B, they find it ______ to ______.",
                "tip": "选项2：形式宾语对比",
            },
            {
                "name": "On the other hand…",
                "pattern": "On the other hand, ______ can be ______.",
                "tip": "另一边对照，结构清晰",
            },
            {
                "name": "However / Whereas",
                "pattern": "However / Whereas ______, ______.",
                "tip": "转折对比，避免连续 By contrast",
            },
        ],
        3: [
            {
                "name": "I prefer… which…",
                "pattern": "I prefer ______, which ______.",
                "tip": "个人偏好 + which 理由",
            },
            {
                "name": "I'd rather… than…",
                "pattern": "I'd rather ______ than ______.",
                "tip": "用 rather than 换掉 prefer+which",
            },
            {
                "name": "If I have to choose…",
                "pattern": "If I have to choose, I would go for ______ because ______.",
                "tip": "选择收束，适合对比题最后一句",
            },
        ],
    },
}


def _rotate(variants: list[Frame], seed: int) -> Frame:
    """Pick primary by seed; attach the other two as alts."""
    n = len(variants)
    if n == 0:
        return {"name": "", "pattern": "", "tip": "", "alts": []}
    idx = seed % n
    primary = dict(variants[idx])
    alts = [dict(variants[j]) for j in range(n) if j != idx]
    primary["alts"] = alts
    primary["variantIndex"] = idx
    return primary


def _match_overrides(qtext: str, seed: int) -> dict[int, Frame]:
    """Question-type overrides still rotate among their own small pools."""
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
            "as a child",
        )
    ):
        o[1] = _rotate(
            [
                {"name": "过去时 When I was…", "pattern": "When I was a child / little, I ______.", "tip": "童年题用过去时"},
                {"name": "Back in those days…", "pattern": "Back in those days, I used to ______.", "tip": "used to 写旧习惯"},
                {"name": "I still remember…", "pattern": "I still remember ______ when I was little.", "tip": "记忆引出童年细节"},
            ],
            seed,
        )
        o[2] = _rotate(
            [
                {"name": "Back then / At that time", "pattern": "Back then / At that time, I ______.", "tip": "承接童年时间线"},
                {"name": "In primary school…", "pattern": "In primary school / At that age, I ______.", "tip": "落到具体阶段"},
                {"name": "Compared with now…", "pattern": "Compared with now, I ______ more often then.", "tip": "今昔对比"},
            ],
            seed,
        )

    if ql.startswith("why ") or " why " in ql:
        o[1] = _rotate(
            [
                {"name": "for the reason that / since", "pattern": "I chose it for the reason that / since ______.", "tip": "Why 题直接给原因"},
                {"name": "The main reason is that…", "pattern": "The main reason is that ______.", "tip": "原因前置"},
                {"name": "What matters most is…", "pattern": "What matters most is ______, so I ______.", "tip": "强调最关键因素"},
            ],
            seed,
        )

    if any(x in ql for x in ("will you", "in the future", "next five years", "would you like to")):
        o[1] = _rotate(
            [
                {"name": "plan to / hope to", "pattern": "I plan / hope to ______ in the future.", "tip": "将来计划"},
                {"name": "I would like to…", "pattern": "I would like to ______ in a few years.", "tip": "愿望表达"},
                {"name": "My goal is to…", "pattern": "My goal is to ______ after I graduate.", "tip": "目标导向"},
            ],
            seed,
        )
        o[2] = _rotate(
            [
                {"name": "After I graduate / In a few years", "pattern": "After I graduate / In a few years, I ______.", "tip": "时间线"},
                {"name": "Once I…", "pattern": "Once I ______, I will ______.", "tip": "条件+将来"},
                {"name": "By then…", "pattern": "By then, I hope I can ______.", "tip": "展望收束"},
            ],
            seed,
        )

    if ql.startswith("please describe") or ql.startswith("can you describe") or "describe the" in ql:
        o[1] = _rotate(
            [
                {"name": "which 描述细节", "pattern": "It is ______, which ______.", "tip": "which 补细节"},
                {"name": "The key point is…", "pattern": "The key point is that ______.", "tip": "抓重点描述"},
                {"name": "You can notice…", "pattern": "You can notice ______, and ______.", "tip": "可观察细节"},
            ],
            seed,
        )

    if any(x in ql for x in ("how often", "do you often", "how frequently")):
        o[2] = _rotate(
            [
                {"name": "Whenever / often", "pattern": "Whenever I ______ / I ______ quite often.", "tip": "频次"},
                {"name": "Most days / From time to time", "pattern": "Most days / From time to time, I ______.", "tip": "频率状语"},
                {"name": "It depends, but usually…", "pattern": "It depends, but usually I ______ about ______.", "tip": "先让步再给频率"},
            ],
            seed,
        )

    if ql.startswith("what do you usually") or ql.startswith("what do you do when"):
        o[2] = _rotate(
            [
                {"name": "It is + adj. + to do", "pattern": "It is ______ for me to ______ when ______.", "tip": "形式主语"},
                {"name": "I tend to…", "pattern": "I tend to ______ when ______.", "tip": "tend to 写习惯"},
                {"name": "My usual way is to…", "pattern": "My usual way is to ______.", "tip": "直接说做法"},
            ],
            seed,
        )

    if "typical day" in ql:
        o[1] = _rotate(
            [
                {"name": "since / for the reason that", "pattern": "I ______ for the reason that / since ______.", "tip": "为何这样安排"},
                {"name": "A typical day starts with…", "pattern": "A typical day starts with ______, then ______.", "tip": "时间线开场"},
                {"name": "I usually begin by…", "pattern": "I usually begin by ______ to ______.", "tip": "begin by + to do"},
            ],
            seed,
        )
        o[2] = _rotate(
            [
                {"name": "In the morning / After lunch", "pattern": "In the morning / After lunch / In the evening, I ______.", "tip": "按时间线"},
                {"name": "Then / After that", "pattern": "Then / After that, I ______.", "tip": "顺序连接"},
                {"name": "Before ______, I…", "pattern": "Before ______, I usually ______.", "tip": "Before 时间状语"},
            ],
            seed,
        )

    if any(x in ql for x in ("rather", "prefer", "compared with", "difference between", "compared to")) or any(
        x in ql
        for x in (
            "noisy or a quiet",
            "big city or a small",
            "apartment or",
            "house or a",
            "house or flat",
            "house or a flat",
            "driver or a passenger",
            "websites or books",
            "comfort or style",
            "shopping mall or",
            "headphones or small",
            "big headphones or",
        )
    ):
        o[3] = _rotate(
            [
                {"name": "I prefer… which…", "pattern": "I prefer ______, which ______.", "tip": "偏好+which"},
                {"name": "I'd rather… than…", "pattern": "I'd rather ______ than ______.", "tip": "rather than"},
                {"name": "If I have to choose…", "pattern": "If I have to choose, I would go for ______ because ______.", "tip": "选择收束"},
            ],
            seed,
        )

    if "do you think" in ql or "is it important" in ql:
        o[1] = _rotate(
            [
                {"name": "In my view / since", "pattern": "In my view, ______ since ______.", "tip": "态度+理由"},
                {"name": "I strongly believe…", "pattern": "I strongly believe ______ because / since ______.", "tip": "强调看法"},
                {"name": "It depends, but generally…", "pattern": "It depends, but generally I think ______.", "tip": "先让步再表态"},
            ],
            seed,
        )

    if "have you ever" in ql:
        o[1] = _rotate(
            [
                {"name": "which 经历举例", "pattern": "Yes, I ______, which ______.", "tip": "经历+which"},
                {"name": "I still remember…", "pattern": "I still remember the time when I ______.", "tip": "记忆引出经历"},
                {"name": "One example is…", "pattern": "One example is ______, and ______.", "tip": "举例式经历"},
            ],
            seed,
        )

    if ql.startswith("what ") and any(x in ql for x in ("types", "kinds", "sorts")):
        o[1] = _rotate(
            [
                {"name": "prefer / keen on", "pattern": "I prefer / am keen on ______ because ______.", "tip": "类型+原因"},
                {"name": "I usually go for…", "pattern": "I usually go for ______, since ______.", "tip": "go for 表选择"},
                {"name": "My first choice is…", "pattern": "My first choice is ______, which ______.", "tip": "first choice+which"},
            ],
            seed,
        )

    if "who helps" in ql or "in what way" in ql:
        o[1] = _rotate(
            [
                {"name": "who + which", "pattern": "______ helps me the most, which ______.", "tip": "人物+which"},
                {"name": "The person I rely on is…", "pattern": "The person I rely on is ______, because ______.", "tip": "rely on"},
                {"name": "Whenever I struggle…", "pattern": "Whenever I struggle, ______ will ______.", "tip": "情景+帮助"},
            ],
            seed,
        )

    if "traffic jam" in ql:
        o[2] = _rotate(
            [
                {"name": "While waiting / During rush hour", "pattern": "While waiting / During rush hour, I ______.", "tip": "堵车场景"},
                {"name": "To kill time…", "pattern": "To kill time, I usually ______.", "tip": "目的状语"},
                {"name": "Instead of getting angry…", "pattern": "Instead of getting angry, I ______.", "tip": "对比行为"},
            ],
            seed,
        )

    return o


def resolve_frames(cat_id: str, qtext: str, variant_seed: int = 0) -> dict[str, Frame]:
    """Return frames keyed by '1'|'2'|'3' for UI steps 2–4, each with alts."""
    seed = int(variant_seed or 0)
    base_vars = _CAT_VARIANTS.get(cat_id) or _CAT_VARIANTS["shishi"]
    merged: dict[int, Frame] = {k: _rotate(v, seed) for k, v in base_vars.items()}
    overrides = _match_overrides(qtext, seed)
    merged.update(overrides)
    return {str(k): v for k, v in merged.items() if k in (1, 2, 3)}


def variant_seed_for(topic_en: str, qtext: str, topic_q_index: int = 0) -> int:
    """Stable rotation key: prefer order within topic, fallback to hash."""
    if topic_q_index is not None and topic_q_index >= 0:
        return topic_q_index
    return sum(ord(c) for c in (topic_en or "") + (qtext or "")) % 3
