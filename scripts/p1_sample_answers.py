# -*- coding: utf-8 -*-
"""Generate band-6+ P1 sample answers from per-question words + frames, with logic checks."""
from __future__ import annotations

import re
from typing import Any

from p1_word_banks_core import norm_q

HAND_SAMPLES: dict[str, str] = {}


def _hand(q: str, answer: str) -> None:
    HAND_SAMPLES[norm_q(q)] = " ".join(answer.split())


def _build_hand() -> None:
    # ---- Watch ----
    _hand(
        "Have you ever got a watch as a gift?",
        "Yes, definitely. I got a smartwatch from my parents as a birthday gift last year, "
        "which helps me check the time quickly. On special occasions I still remember that day. "
        "I find it really convenient and practical.",
    )
    _hand(
        "Do you wear a watch?",
        "Yes, almost every day. Since I need to stay punctual, I check the time before heading out. "
        "It is convenient for me to wear it during class every morning. "
        "Wearing a watch can be seen as a habit that helps me stay organised.",
    )
    _hand(
        "Why do some people wear expensive watches?",
        "I think so. Since an expensive watch can be a status symbol, some people wear one "
        "to make a fashion statement. They often do this at formal events, which shows success. "
        "I find it understandable, though it is not my style.",
    )
    _hand(
        "Do you think it is important to wear a watch? Why?",
        "Yes, quite important. Since students need to stay punctual, I wear a watch to check time quickly. "
        "It helps in class and meetings every day, which keeps me on schedule. "
        "I find it practical and really convenient.",
    )
    # ---- Cars ----
    _hand(
        "Did you enjoy traveling by car when you were a kid?",
        "Yes, I loved it. When I was a child, we often went on family road trips during the holidays, "
        "which created great memories. Back then I felt relaxed and at ease in the car. "
        "I find those trips so much fun even now.",
    )
    _hand(
        "What types of cars do you like?",
        "I prefer SUVs for the reason that they have more space and comfortable seats. "
        "I am keen on them for long trips with my family to feel safer. "
        "I find this type more comfortable and practical.",
    )
    _hand(
        "Will you buy an expensive car in the future?",
        "Maybe in the future. I plan to buy a practical car first after I graduate, "
        "when I can afford it. In a few years, after I start working, I might reconsider. "
        "For now, practical matters more than price.",
    )
    _hand(
        "What do you usually do when there is a traffic jam?",
        "I usually stay calm. Since I do not want to get stressed, I listen to music or watch short videos. "
        "While waiting during rush hour, it is common for me to chat with friends. "
        "This can be seen as a way to relieve stress and pass the time.",
    )
    _hand(
        "Do you think car colours are important?",
        "It depends. Since colour can show personality, some people choose white or black cars "
        "to keep them easy to clean. When buying a car, this matters for resale value, "
        "which some buyers care about. Personally, I find it not that important to me.",
    )
    _hand(
        "Do you prefer to be a driver or a passenger?",
        "I'd rather be a passenger. As for being a passenger, it is regarded as more relaxing to rest. "
        "By contrast, regarding driving, people find it more tiring to focus the whole time. "
        "I find being a passenger more comfortable, which lets me enjoy the view.",
    )
    # ---- Work/studies key ----
    _hand(
        "What subjects are you studying?",
        "I'm majoring in business, and I also take related courses like economics. "
        "I attend classes every weekday to build a solid foundation, which will be useful for my future career. "
        "I find this field quite practical.",
    )
    _hand(
        "Why did you choose to study that subject?",
        "I chose it for the reason that I have a passion for the subject and it matches my strengths. "
        "Since I want a clear future career path, I study related courses every weekday. "
        "I find it practical and quite useful.",
    )
    _hand(
        "What work do you do?",
        "I'm a student, and I also do a part-time internship on campus. "
        "I work as a tutor from time to time, which helps me practice communication. "
        "I find this experience really useful for my future career.",
    )
    _hand(
        "Who helps you the most? And how?",
        "My parents help me the most. They give me advice and encourage me, which helps with planning. "
        "Whenever I feel stuck with study or life choices, they support me patiently. "
        "I find their help really practical, and I rely on it a lot.",
    )
    # ---- Websites ----
    _hand(
        "Are there any changes to the websites you often visit?",
        "Yes, definitely. For example, there is a new layout and more short videos, which take time to get used to. "
        "I have noticed these updates in the past year. I find the changes mostly positive and still useful.",
    )
    _hand(
        "What have you learned from websites that help with your life or studies?",
        "Quite a lot. I learn study skills and cooking tips online, which helps me search information quickly. "
        "Whenever I need help before exams, I use these sites almost every day. "
        "I find them really useful and practical, so I keep going back to them.",
    )
    _hand(
        "What is your favourite website?",
        "My favourite is Bilibili. I am keen on it for the reason that I can watch tutorials and learn new skills. "
        "I visit it almost every day in my free time to relax. I find it really fun and very useful.",
    )
    _hand(
        "Do you prefer getting information from websites or books?",
        "I prefer websites. As for websites, they are regarded as faster and up to date to search. "
        "By contrast, regarding books, people find them deeper and better for focus. "
        "I find websites more suitable for daily needs, which still leaves room for books on hard topics.",
    )
    # ---- Gifts ----
    _hand(
        "Have you ever sent handmade gifts to others?",
        "Yes, I have. I once made a handmade card and a DIY gift for a close friend, which they really liked. "
        "I do this on birthdays from time to time. I find it meaningful and worth the effort.",
    )
    _hand(
        "Have you ever received a great gift?",
        "Yes, definitely. I received a thoughtful gift from my best friend last month, which really surprised me. "
        "It was on my birthday, and I still remember how excited I felt. "
        "I find such gifts really make me happy, and they mean more than expensive things.",
    )


_build_hand()


def _chips(words: dict[str, list[str]], step: str, n: int = 4) -> list[str]:
    skip = {
        "yes", "definitely", "absolutely", "sure", "not really", "sometimes",
        "exactly", "perhaps", "maybe",
    }
    raw = list(words.get(step, []) or [])
    primary = [c for c in raw if c.lower() not in skip]
    pool = primary if len(primary) >= 2 else raw
    out: list[str] = []
    seen: set[str] = set()
    for c in pool:
        k = c.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(c.strip())
        if len(out) >= n:
            break
    while len(out) < 2:
        out.append("this")
    return out


def _opening(words: dict[str, list[str]], steps: list[str], qtext: str = "") -> str:
    ql = (qtext or "").lower()
    # Question-aware openings beat generic clue chips
    if "where is your hometown" in ql:
        return "My hometown is in the south"
    if "famous for" in ql:
        return "It is mainly famous for local food"
    if "describe your hometown" in ql or "describe the place where you live" in ql:
        return "Sure, I can give a short description"
    if "describe the room" in ql:
        return "My room is small but cosy"
    if "apartment or a house" in ql:
        return "I live in an apartment"
    if "how long have you lived" in ql or "how long have you been living" in ql:
        return "I have lived there for several years"
    if "permanent residence" in ql:
        return "For now, yes"
    if "noisy or a quiet" in ql:
        return "It is quite quiet"
    if "big city or a small" in ql:
        return "It is a medium-sized city"
    if "what type of headphones" in ql:
        return "I usually use wireless earbuds"
    if "when did you start using social" in ql:
        return "I started in high school"
    if "are you still in touch" in ql:
        return "Not really, only sometimes"
    if "do you know any famous people" in ql:
        return "Not personally"
    if "do you know any of your neighbors" in ql:
        return "Yes, a few of them"
    if "requirements" in ql and "job" in ql:
        return "There were several requirements"
    if "why did you choose to do that type of work" in ql:
        return "I chose it since it matches my major"

    for c in words.get(steps[0], []) or []:
        cl = c.lower().strip()
        if cl in {"yes", "definitely", "absolutely", "sure"}:
            return "Yes, definitely"
        if cl.startswith("yes"):
            return c if c[0].isupper() else c[0].upper() + c[1:]
        if any(
            cl.startswith(p)
            for p in (
                "i ", "i'", "i’m", "i'm", "i’d", "i'd", "i prefer", "i'd rather",
                "not really", "not sure", "maybe", "perhaps", "it depends",
                "somewhat", "several", "quite", "a few", "my ",
            )
        ):
            return c if c[0].isupper() else c[0].upper() + c[1:]
        if "prefer" in cl or "rather" in cl:
            return c if c[0].isupper() else c[0].upper() + c[1:]
    chips = words.get(steps[0], []) or ["Yes"]
    c = chips[0]
    # Avoid clue-merge junk like "I live in a big city" on unrelated hometown sub-questions
    if "i live in a big city" in c.lower() and any(
        x in ql for x in ("hometown", "room", "apartment", "how long", "famous", "permanent")
    ):
        return "Yes, I can answer that briefly"
    return c if c[0].isupper() else c[0].upper() + c[1:]


def _adj(feel: list[str]) -> str:
    for c in feel:
        cl = c.lower()
        for a in (
            "convenient", "practical", "useful", "helpful", "relaxed", "comfortable",
            "enjoyable", "important", "fun", "positive", "energetic", "organised",
            "meaningful", "safer", "surprising",
        ):
            if a in cl:
                return a
        if cl.startswith(("really ", "quite ", "very ")):
            return cl.split(" ", 1)[1].strip() or "practical"
    return "practical"


def _np(chips: list[str], n: int = 2) -> str:
    """Join chips as noun/phrase examples (never as bare verbs)."""
    parts = [c for c in chips if c and c.lower() != "this"][:n]
    if not parts:
        return "a specific example"
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} and {parts[1]}"


def _freq(chips: list[str]) -> str:
    for c in chips:
        cl = c.lower()
        if any(
            x in cl
            for x in (
                "every", "often", "weekend", "time to time", "morning", "night",
                "day", "week", "year", "holiday", "free time", "recently", "last",
                "once", "rarely", "seldom", "during", "after", "before",
            )
        ):
            return c
    return chips[0] if chips else "from time to time"


def _polish(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" .", ".").replace(" ,", ",")
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    parts = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        sent = sent.strip()
        if not sent:
            continue
        if sent[0].islower():
            sent = sent[0].upper() + sent[1:]
        # fix "I Am" style from chip casing lightly
        sent = re.sub(r"\bi\b", "I", sent)
        parts.append(sent)
    out = " ".join(parts)
    if not out.endswith((".", "!", "?")):
        out += "."
    # clean awkward doubles
    out = out.replace("to to ", "to ").replace("a a ", "a ")
    out = re.sub(r"\bthis this\b", "this", out, flags=re.I)
    return out


def _logic_ok(qtext: str, answer: str, cat_id: str) -> tuple[bool, str]:
    ql = qtext.lower()
    al = answer.lower()
    words_n = len(answer.split())
    if words_n < 36:
        return False, f"short({words_n})"
    if answer.count(".") + answer.count("!") < 2:
        return False, "need 3 sentences"
    if "______" in answer or "..." in answer:
        return False, "placeholder"
    if re.search(r"\bi (once|often|usually) (from|for|with|in|on|at|of)\b", al):
        return False, "chip used as verb"
    if " is involved" in al or "are involved" in al:
        return False, "awkward involved"
    if cat_id == "duibi" and not any(
        x in al for x in ("prefer", "rather", "by contrast", "whereas", "while ", "compared", "on the other")
    ):
        return False, "no contrast"
    if ("why" in ql or ql.startswith("why ")) and not any(
        x in al for x in ("since", "for the reason", "because", "so that", "as ")
    ):
        return False, "why no reason"
    if "have you ever" in ql and not any(
        x in al for x in ("yes", "have", "once", "last", "got", "received", "bought", "tried", "learned", "learnt")
    ):
        return False, "ever no experience"
    return True, "ok"


def _gen_shishi(q: str, words: dict, steps: list[str]) -> str:
    open_ = _opening(words, steps, q)
    ex = _chips(words, steps[1])
    fr = _chips(words, steps[2])
    feel = _chips(words, steps[3])
    adj = _adj(feel)
    ex_np = _np(ex)
    fr_p = _freq(fr)
    feel_tail = feel[0] if feel else adj
    ql = q.lower()

    if "have you ever" in ql:
        return (
            f"{open_}. For example, I once dealt with {ex_np}, which left a clear impression on me. "
            f"That happened {fr_p}, so I still remember the details. "
            f"Overall, I find it {adj}, and {feel_tail} is what I would emphasise."
        )
    if any(ql.startswith(x) for x in ("what ", "which ", "who ")):
        return (
            f"{open_}. To be specific, I would mention {ex_np}, which matters in my daily routine. "
            f"I usually talk about this {fr_p}, and I can give a short example if needed. "
            f"I find it {adj}, so {feel_tail} is a fair summary."
        )
    if "describe" in ql or ql.startswith("where "):
        return (
            f"{open_}. The key details are {ex_np}, which are easy to notice in real life. "
            f"I experience this {fr_p}, so I can describe it without making things up. "
            f"I find this place {adj}, and {feel_tail} is how I feel about it."
        )
    if ql.startswith("how "):
        return (
            f"{open_}. The main point is {ex_np}, which shapes my answer clearly. "
            f"This has been true {fr_p}, so I do not need a complicated story. "
            f"I find it {adj}, and {feel_tail} is the feeling I want to share."
        )
    if " or " in ql and ("noisy" in ql or "quiet" in ql or "apartment" in ql or "house" in ql or "big" in ql):
        return (
            f"{open_}. In my case, {ex_np} is the better description, which fits where I live. "
            f"I notice this {fr_p}, especially when I compare different areas. "
            f"I find it {adj}, and {feel_tail} is my honest reaction."
        )
    return (
        f"{open_}. For example, I can talk about {ex_np}, which is quite typical for me. "
        f"I notice this {fr_p}, so it is easy to keep the answer concrete. "
        f"I find it {adj}, and {feel_tail} is what I would say at the end."
    )


def _gen_xihao(q: str, words: dict, steps: list[str]) -> str:
    open_ = _opening(words, steps, q)
    reason = _chips(words, steps[1])
    fr = _chips(words, steps[2])
    feel = _chips(words, steps[3])
    adj = _adj(feel)
    r_np = _np(reason)
    fr_p = _freq(fr)
    feel_tail = feel[0] if feel else "it helps me unwind"
    ql = q.lower()

    if any(x in ql for x in ("when you were a kid", "when you were little", "childhood", "when you were a child")):
        return (
            f"{open_}. When I was a child, I enjoyed {r_np}, which created warm memories. "
            f"Back then I did this {fr_p}, and I still remember how simple it felt. "
            f"I find those days {adj}, which is why {feel_tail}."
        )
    if any(x in ql for x in ("will you", "in the future", "would you like", "do you want")):
        return (
            f"{open_}. I hope to focus on {r_np} for the reason that it fits my long-term plan. "
            f"I may do this {fr_p}, after I have more time and money. "
            f"I find the idea {adj}, and {feel_tail} is how I feel about it now."
        )
    return (
        f"{open_}. I am keen on this for the reason that {r_np} matters to me. "
        f"Whenever I have time, I enjoy it {fr_p} to stay positive. "
        f"I find this activity {adj}, which helps me unwind, and {feel_tail}."
    )


def _gen_xingwei(q: str, words: dict, steps: list[str]) -> str:
    open_ = _opening(words, steps, q)
    reason = _chips(words, steps[1])
    timeline = _chips(words, steps[2])
    impact = _chips(words, steps[3])
    r_np = _np(reason)
    t_p = _freq(timeline)
    i1 = impact[0]
    i2 = impact[1] if len(impact) > 1 else "keeps my routine steady"
    # impact chips are often full phrases ("helps me…") not bare verbs
    def _impact_clause(chip: str) -> str:
        cl = chip.lower().strip()
        if cl.startswith(("help", "save", "keep", "make", "relieve", "recharge", "pass")):
            return chip
        if cl.startswith(("a way", "something")):
            return chip
        return f"helps me {chip}"

    ql = q.lower()

    if "traffic jam" in ql:
        return (
            f"{open_}. Since I do not want to get stressed, I rely on {r_np}. "
            f"While waiting during rush hour, it is common for me to stay patient and use the time wisely. "
            f"This can be seen as a habit that {_impact_clause(i1)}, and it also {_impact_clause(i2)}."
        )
    if ql.startswith("what do you"):
        return (
            f"{open_}. For the reason that I need a clear routine, I focus on {r_np}. "
            f"It is normal for me to do this {t_p}, especially when my schedule is busy. "
            f"This habit can be seen as something that {_impact_clause(i1)}, and it also {_impact_clause(i2)}."
        )
    return (
        f"{open_}. Since {r_np} matters in my routine, I keep the habit consistently. "
        f"It is common for me to do this {t_p}, so it has become automatic. "
        f"This can be regarded as a habit that {_impact_clause(i1)}, and it also {_impact_clause(i2)}."
    )


def _gen_guandian(q: str, words: dict, steps: list[str]) -> str:
    open_ = _opening(words, steps, q)
    reason = _chips(words, steps[1])
    effect = _chips(words, steps[2])
    feel = _chips(words, steps[3])
    r_np = _np(reason)
    e_np = _np(effect)
    adj = _adj(feel)
    feel_tail = feel[0] if feel else adj
    ql = q.lower()

    if any(x in ql for x in ("do you think", "is it important", "should ", "does ")):
        return (
            f"{open_}. In my view, this matters since {r_np} plays a real role. "
            f"People often notice it through {e_np}, which makes a clear difference in daily life. "
            f"I find it {adj} to keep this in mind, and {feel_tail} is my overall attitude."
        )
    return (
        f"{open_}. Since {r_np} is common, people tend to talk about it seriously. "
        f"This shows up in {e_np}, which affects daily life more than we think. "
        f"I find it {adj}, and {feel_tail} is a fair conclusion."
    )


def _gen_duibi(q: str, words: dict, steps: list[str]) -> str:
    open_ = _opening(words, steps, q)
    opt1 = _chips(words, steps[1])
    opt2 = _chips(words, steps[2])
    feel = _chips(words, steps[3])
    o1 = _np(opt1)
    o2 = _np(opt2)
    f1 = feel[0] if feel else "the first option"
    f2 = feel[1] if len(feel) > 1 else "fits my daily needs"
    return (
        f"{open_}. As for the first side, it is regarded as stronger because of {o1}. "
        f"By contrast, regarding the other side, people find it different due to {o2}. "
        f"Overall, I find {f1} more suitable, which {f2}."
    )


_GEN = {
    "shishi": _gen_shishi,
    "xihao": _gen_xihao,
    "xingwei": _gen_xingwei,
    "guandian": _gen_guandian,
    "duibi": _gen_duibi,
}


def generate_sample(
    cat_id: str,
    qtext: str,
    steps: list[str],
    words: dict[str, list[str]],
    frames: dict[str, Any] | None = None,
) -> dict[str, Any]:
    key = norm_q(qtext)
    if key in HAND_SAMPLES:
        text = _polish(HAND_SAMPLES[key])
        ok, note = _logic_ok(qtext, text, cat_id)
        return {"text": text, "ok": ok, "note": note, "source": "hand"}

    gen = _GEN.get(cat_id, _gen_shishi)
    text = _polish(gen(qtext, words, steps))
    ok, note = _logic_ok(qtext, text, cat_id)
    return {"text": text, "ok": ok, "note": note, "source": "template"}
