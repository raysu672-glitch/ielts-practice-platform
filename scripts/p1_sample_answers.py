# -*- coding: utf-8 -*-
"""Generate band-6+ P1 sample answers from per-question words + frames, with logic checks."""
from __future__ import annotations

import re
from typing import Any

from p1_topic_materials import get_question_pack
from p1_word_banks_core import norm_q

HAND_SAMPLES: dict[str, str] = {}
# (norm_q, kitId) → answer — Freestyle: same question, different material = different sample
HAND_KIT_SAMPLES: dict[tuple[str, str], str] = {}


def _hand(q: str, answer: str, kit_id: str = "") -> None:
    text = " ".join(answer.split())
    key = norm_q(q)
    if kit_id:
        HAND_KIT_SAMPLES[(key, kit_id)] = text
    else:
        HAND_SAMPLES[key] = text


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
        "Do you work or are you a student?",
        "I'm a full-time student at university. I major in business and attend classes on campus every weekday. "
        "When I am free, I also finish assignments in the library. "
        "I find this student routine practical for my future career.",
    )
    _hand(
        "Why did you choose that job or that subject?",
        "I chose my subject for the reason that it matches my strengths and leads to clearer career options. "
        "Since I want useful skills, I take related courses every weekday and review notes at weekends. "
        "I find the choice practical and quite useful.",
    )
    _hand(
        "What do you find most challenging about your work or your studies?",
        "The most challenging part is balancing assignments with exams. "
        "For example, I often stay in the library until late when deadlines pile up every week. "
        "I find it stressful at times, but it also makes me more organised.",
    )
    _hand(
        "What do you like most about your job or your studies?",
        "What I like most is learning with classmates and discussing real cases in class. "
        "I am keen on group projects for the reason that we share ideas almost every week. "
        "I find this part enjoyable and really useful for my future career.",
    )
    _hand(
        "What is a typical day like for you at work or at school?",
        "A typical school day starts with morning classes, then I review notes in the library after lunch. "
        "In the evening I finish assignments and sometimes join a short club meeting. "
        "I find this routine busy but practical.",
    )
    _hand(
        "What would you like to be doing in your career or studies in a few years?",
        "In a few years I would like to finish my degree and start an internship in a business-related role. "
        "I hope to keep taking practical courses while I build work experience. "
        "I find that plan realistic and quite useful.",
    )
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
    # ---- 2026 9-12 season high-visibility topics ----
    _hand(
        "What kind of shoes do you wear most often?",
        "Comfortable sneakers. I wear them on campus every weekday because they feel loose and protect my feet. "
        "At weekends I sometimes switch to a nicer pair when I hang out. "
        "I find them practical and really comfortable.",
    )
    _hand(
        "What kind of shoes did you wear as a child?",
        "As a child I mostly wore simple school shoes that my parents bought before term started. "
        "I used them every weekday to school, and they were plain but sturdy. "
        "I find those shoes practical, though not stylish by today's standards.",
    )
    _hand(
        "What do you usually do when you feel tired?",
        "When I feel tired, I usually take a short walk or rest with soft music. "
        "After a long day of classes, ten or fifteen minutes is enough to slow down and recover. "
        "I find this more effective for relieving tiredness than scrolling on my phone.",
    )
    _hand(
        "Which websites do you visit most often?",
        "I visit Xiaohongshu and a few study websites most often. "
        "I use them to search information and watch short useful videos almost every day. "
        "I find them practical and really convenient for both study and daily tips.",
    )
    _hand(
        "What do you do when you see rubbish on the street?",
        "I pick it up if I can and put it into a nearby bin. "
        "Since sorting rubbish matters in my dorm building, I try to do the same outside. "
        "I find this habit responsible, and it also keeps the street cleaner.",
    )
    _hand(
        "What kind of home would you like to have in the future?",
        "I would like a quiet rented apartment near campus or the subway. "
        "I hope it has a bright living room and a tidy desk so I can study and rest easily. "
        "I find that kind of home practical and comfortable.",
    )
    _hand(
        "Would you like to live in your hometown in the future?",
        "Maybe for a while. I enjoy going home for local food and family time every holiday. "
        "But for work or further study I may need to stay in a bigger city. "
        "I find both options possible, so I have not decided yet.",
    )
    _hand(
        "What scientific discovery would you like to see in the future?",
        "I would like to see clean energy breakthroughs and better medical discoveries. "
        "I often watch space and science documentaries, which make me curious about real progress. "
        "I find these discoveries exciting and useful for everyday life.",
    )
    _hand(
        "How do you think space travel will change in the future?",
        "I think space travel will become more common but still expensive at first. "
        "People may take short trips or follow more public space projects through documentaries and news. "
        "I find the idea exciting, though it is not something I need right now.",
    )
    # ---- Teachers ----
    _hand(
        "What makes someone a good teacher?",
        "Patience and clear explanations. A good teacher can explain concepts step by step without rushing students. "
        "In secondary school one teacher stayed after class to help me, and that still shapes how I judge teaching. "
        "I find those qualities really important and encouraging.",
    )
    _hand(
        "What kind of teacher do you learn best from?",
        "I learn best from patient teachers who give clear explanations and encouraging feedback. "
        "When assignments felt hard, that kind of teacher made me less afraid to ask questions. "
        "I find this teaching style practical and really helpful.",
    )
    _hand(
        "Who was your favourite teacher when you were at school?",
        "My favourite was a secondary-school teacher who stayed after class to explain concepts without rushing me. "
        "She used simple examples and encouraged us every week in that class. "
        "I find her teaching style still useful when I study on my own.",
    )
    _hand(
        "In what way has your favourite teacher helped you?",
        "She helped me keep going when assignments felt hard in secondary school. "
        "Because she explained concepts patiently, I became less afraid to ask questions and more self-driven. "
        "I find that support really appreciated even now when I study on my own.",
    )
    _hand(
        "Have you ever wanted to be a teacher?",
        "Yes, briefly. After I met a patient teacher who explained concepts clearly, I thought teaching could be meaningful. "
        "But later I chose business for my strengths and career path. "
        "I still find good teaching admirable, even if it is not my plan now.",
    )
    _hand(
        "How has the way teachers teach changed since you were a child?",
        "It has changed a lot. Teachers now use more slides, videos and group work than when I was a child. "
        "By contrast, classes used to rely more on the blackboard and copying notes. "
        "I find the new style more interactive, though clear explanations still matter most.",
    )
    # ---- Secondary school (not teacher-forced) ----
    _hand(
        "What was your favourite subject at secondary school?",
        "My favourite subject was English, and sometimes maths when the class felt clear. "
        "I liked it mainly because the lessons were practical and I could use them outside class. "
        "I find that subject still useful for my studies now.",
    )
    _hand(
        "What was your secondary school like?",
        "It was a busy but friendly school with clear routines and supportive classmates. "
        "We had morning classes, short breaks, and after-school clubs a few times a week. "
        "I find those years practical and full of warm memories.",
    )


_build_hand()

# Extra season hand samples (override templates / earlier stubs)
from p1_hand_samples_912 import HAND_912  # noqa: E402
from p1_hand_samples_fix import HAND_FIX  # noqa: E402
from p1_hand_samples_kit import HAND_KIT  # noqa: E402

HAND_SAMPLES.update(HAND_912)
HAND_SAMPLES.update(HAND_FIX)
HAND_KIT_SAMPLES.update(HAND_KIT)


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
    if ql.startswith("who "):
        for c in words.get(steps[0], []) or []:
            cl = (c or "").lower()
            if cl.startswith((
                "yes", "definitely", "absolutely", "sure", "not really", "sometimes",
                "exactly", "perhaps", "maybe", "i live in",
            )):
                continue
            if c and len(c.split()) <= 10:
                return c if c[0].isupper() else c[0].upper() + c[1:]
        if "live with" in ql:
            return "I live with my roommate"
        if "kept your room" in ql or ("tidy" in ql and "who" in ql):
            return "My mum"
        if "chose your name" in ql or "chose your clothes" in ql:
            return "My parents"
        if "go shopping with" in ql:
            return "My parents"
        if "taught you" in ql:
            return "My parents"
        if "funniest" in ql:
            return "My roommate"
        if "teacher" in ql:
            return "A patient secondary-school teacher"
        return "Someone close to me"
    if ql.startswith(("what kind", "what type", "which ")):
        for c in words.get(steps[0], []) or []:
            cl = (c or "").lower()
            if cl.startswith((
                "yes", "definitely", "absolutely", "sure", "i remember", "i love",
                "not really", "sometimes", "i do", "i like it",
            )):
                continue
            if "love it" in cl or cl in {"i do", "sure"}:
                continue
            if c and len(c.split()) <= 12:
                return c if c[0].isupper() else c[0].upper() + c[1:]
        if "music" in ql:
            return "I like light pop and soft playlists"
        if "comedy" in ql or "comed" in ql:
            return "I enjoy light comedies"
        if "advert" in ql:
            return "I enjoy short funny adverts"
        if "room" in ql:
            return "I like the living room best"
        if "home" in ql:
            return "I would like a bright apartment"
        if "opportunity" in ql:
            return "I would like a useful internship"
        if "places" in ql or "place" in ql:
            return "I like quiet parks and small markets"
        if "car" in ql:
            return "I would like a practical small car"
        if "shoe" in ql:
            return "Comfortable sneakers"
        return "A few clear everyday examples"
    if ql.startswith("how does "):
        if "science" in ql:
            return "It affects me through everyday technology"
        if "tired" in ql:
            return "It mainly hurts my focus"
        return "It affects me in small practical ways"
    if ql.startswith("how do you feel"):
        return "I feel fine about it overall"
    if ql.startswith("how do you think"):
        return "I think it will keep changing"
    if ql.startswith("how often "):
        for c in words.get(steps[0], []) or []:
            cl = (c or "").lower()
            if any(x in cl for x in ("every", "often", "once", "twice", "rarely", "seldom", "week", "day")):
                return c if c[0].isupper() else c[0].upper() + c[1:]
        return "Quite often"
    if ql.startswith("when did ") or ql.startswith("when do "):
        for c in words.get(steps[0], []) or []:
            cl = (c or "").lower()
            if cl.startswith(("yes", "definitely", "absolutely", "sure")):
                continue
            if c:
                return c if c[0].isupper() else c[0].upper() + c[1:]
        if "start" in ql and "science" in ql:
            return "In primary school"
        return "A few years ago"
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
    if "do you work or are you a student" in ql:
        return "I'm a full-time student"
    if "what do you find most challenging" in ql:
        return "Balancing deadlines is the hardest part"
    if "what do you like most about your job or your studies" in ql:
        return "I like learning with classmates most"
    if "typical day" in ql and ("work" in ql or "school" in ql):
        return "A typical day is packed with classes"
    if "in your career or studies in a few years" in ql or "would you like to be doing" in ql:
        return "I would like to grow into a practical role"
    if "why did you choose that job or that subject" in ql:
        return "I chose it since it matches my strengths"

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
    parts = [c for c in chips if c and c.lower() not in {"this", "a specific example"}][:n]
    if not parts:
        return "a simple daily detail"
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
    if any(
        x in al
        for x in (
            "i can talk about",
            "i would mention",
            "shapes my answer",
            "what i would say at the end",
            "is a fair summary",
            "is a fair conclusion",
            "keep the answer concrete",
            "without making things up",
            "fits the point about",
            "still sits in that memory",
            "one related detail in my week",
            "i keep the answer on the question",
            "is only a small supporting detail",
            "is unrelated to the forgetting",
        )
    ):
        return False, "meta template"
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
            f"{open_}. For example, I once tried {ex_np}, which left a clear impression on me. "
            f"That happened {fr_p}, so I still remember the details. "
            f"Overall, I find it {adj} and {feel_tail}."
        )
    if ql.startswith(("what kind", "what type", "which kind", "which ")):
        return (
            f"{open_}. The main example is {ex_np}, which fits what I actually use. "
            f"This comes up {fr_p}, so I can describe it with real details. "
            f"I find it {adj}, and {feel_tail}."
        )
    if ql.startswith("who "):
        return (
            f"{open_}. Looking back, that person was part of my daily life with {ex_np}. "
            f"This was true {fr_p}, and the memory is still clear. "
            f"I find it {adj}, and {feel_tail}."
        )
    if any(ql.startswith(x) for x in ("what ",)):
        return (
            f"{open_}. To be specific, the key point is {ex_np}, which comes up in my daily routine. "
            f"I notice this {fr_p}, and it has become quite familiar. "
            f"I find it {adj}, so {feel_tail} describes my feeling well."
        )
    if "describe" in ql or ql.startswith("where "):
        return (
            f"{open_}. The key details are {ex_np}, which you can notice in real life. "
            f"I experience this {fr_p}, so the picture is clear in my mind. "
            f"I find this place {adj}, and {feel_tail}."
        )
    if "affect" in ql and ("daily life" in ql or "work" in ql or "stud" in ql):
        return (
            f"{open_}. For example, {ex_np} shows up in ordinary routines, not only in big events. "
            f"I notice this {fr_p}, especially when my schedule is busy. "
            f"I find the effect {adj}, and {feel_tail}."
        )
    if ql.startswith("how "):
        return (
            f"{open_}. The main point is {ex_np}, which shapes what I do day to day. "
            f"This has been true {fr_p}, so I can explain it with simple details. "
            f"I find it {adj}, and {feel_tail}."
        )
    if " or " in ql and ("noisy" in ql or "quiet" in ql or "apartment" in ql or "house" in ql or "big" in ql):
        return (
            f"{open_}. In my case, {ex_np} is the better description, which fits where I live. "
            f"I notice this {fr_p}, especially when I compare different areas. "
            f"I find it {adj}, and {feel_tail}."
        )
    if "do you work or are you a student" in ql:
        return (
            f"{open_}. I major in business and attend classes on campus, which fills most weekdays. "
            f"I also finish assignments in the library {fr_p}. "
            f"I find this student life {adj} and {feel_tail}."
        )
    return (
        f"{open_}. For example, {ex_np} comes up often in my week, so I can give a real answer. "
        f"I notice this {fr_p}, and the habit feels natural now. "
        f"I find it {adj}, and {feel_tail}."
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
            f"I find the idea {adj}, and {feel_tail}."
        )
    if ql.startswith(("do you like", "do you enjoy", "are you keen", "did you like")):
        return (
            f"{open_}. I enjoy {r_np}, which fits my routine and keeps me in a better mood. "
            f"I usually do this {fr_p} when I am free. "
            f"I find this activity {adj}, which helps me unwind."
        )
    if ql.startswith(("what do you like", "what kind", "which ", "what ")):
        return (
            f"{open_}. I like it mainly because of {r_np}, which fits my routine. "
            f"I enjoy this {fr_p}, especially when I want a short break. "
            f"I find it {adj}, and {feel_tail}."
        )
    return (
        f"{open_}. I enjoy {r_np}, which fits my routine and keeps me in a better mood. "
        f"I usually do this {fr_p} when I am free. "
        f"I find this activity {adj}, which helps me unwind."
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
    if ql.startswith("how often") or ql.startswith("when do"):
        return (
            f"{open_}. I usually involve {r_np} in an ordinary week. "
            f"It is common for me to do this {t_p}, especially when my schedule allows. "
            f"This habit {_impact_clause(i1)}, and it also {_impact_clause(i2)}."
        )
    return (
        f"{open_}. I keep {r_np} as part of a normal week rather than a special event. "
        f"It is common for me to do this {t_p}, so the habit feels automatic. "
        f"This {_impact_clause(i1)}, and it also {_impact_clause(i2)}."
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
            f"I find it {adj} to keep this in mind."
        )
    return (
        f"{open_}. Since {r_np} is common, people take it seriously in daily life. "
        f"This shows up in {e_np}, which affects routines more than we think. "
        f"I find it {adj}, and {feel_tail}."
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


def _chip_hit(chip: str, answer_l: str) -> bool:
    cl = (chip or "").lower().strip()
    if not cl:
        return False
    if cl in answer_l:
        return True
    # allow partial content words (len>3)
    parts = [p for p in re.findall(r"[a-zA-Z']+", cl) if len(p) > 3]
    if not parts:
        return False
    return sum(1 for p in parts if p in answer_l) >= max(1, len(parts) // 2)


def _align_ok(steps: list[str], words: dict[str, list[str]], answer: str) -> tuple[bool, str]:
    al = answer.lower()
    missing: list[str] = []
    for s in steps:
        chips = [c for c in (words.get(s) or []) if c]
        if not chips:
            continue
        if not any(_chip_hit(c, al) for c in chips[:4]):
            missing.append(s)
    if missing:
        return False, "chips unused:" + ",".join(missing)
    return True, "ok"


def _cap(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return s
    return s[0].upper() + s[1:]


def _low(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return s
    if s[0].isupper() and (len(s) == 1 or s[1].islower() or s[1] == " "):
        return s[0].lower() + s[1:]
    return s


def _kit_detail(kind: str, origin: str) -> str:
    """Prefer short kind label; fall back to a trimmed origin clause."""
    k = (kind or "").strip()
    # Avoid bare verb phrases like "use the subway" as noun detail
    k = re.sub(
        r"(?i)^(use|take|go for|go to|look at|watch|keep|put|check)\s+",
        "",
        k,
    ).strip()
    if k and len(k.split()) <= 8:
        return k
    if origin:
        part = re.split(r"[,.]", origin)[0].strip()
        if 3 <= len(part.split()) <= 22:
            return _low(part)
    return k or origin or "a simple daily detail"


def _safe_open(open_: str, ql: str) -> str:
    o = (open_ or "").strip()
    if not o:
        return "Sure"
    ol = o.lower()
    bad_yes = ol.startswith("yes") or ol.startswith("not really") or ol.startswith("definitely")
    needs_fact = ql.startswith((
        "what kind", "what type", "which ", "who ", "how does", "how often",
        "how do you", "how did", "how is", "how has", "how have", "what ", "where ",
        "when ", "when did",
    ))
    if bad_yes and needs_fact:
        if ql.startswith("who "):
            return "Someone close to me"
        if ql.startswith(("what kind", "what type", "which ")):
            return "A few clear examples"
        if ql.startswith("where "):
            if "friend" in ql:
                return "I would take them to a nearby park"
            if "travel" in ql:
                return "I would like to visit a quieter coastal town"
            return "A few local places"
        if ql.startswith("when "):
            return "A few years ago"
        if ql.startswith("how "):
            return "In a few practical ways"
        return "I can give a short answer"
    return o


def _feel_pad(feel: str, impact: str) -> str:
    f = (feel or "practical").strip()
    imp = (impact or f).strip()
    imp = re.sub(r"(?i)\bwhen something comes up\b", "on busy days", imp)
    fl = f.lower()
    if fl.startswith(("make", "help", "let", "give", "keep")) or " me " in f:
        return f"That still {f} in ordinary weeks, and {imp}."
    if fl.startswith(("appreciated", "respected")):
        return f"I still feel {f} about it in ordinary weeks, and {imp}."
    return f"That habit still feels {f} in ordinary weeks, and {imp}."


def _who_person(ql: str, open_: str, detail: str, origin: str) -> str:
    """Force a person-first opening for Who questions."""
    blob = f"{detail} {origin}".lower()
    o = (open_ or "").strip()
    ol = o.lower()
    bad_open = ol.startswith((
        "not really", "yes", "sure", "sometimes", "i live in", "a patient teacher",
        "someone close", "i can give", "a few", "to be specific",
    )) or "is what i" in ol
    if "live with" in ql:
        if any(x in blob for x in ("dorm", "roommate", "campus")):
            return "I live with my roommate in campus dorms"
        if any(x in blob for x in ("parent", "mum", "mom", "family")):
            return "I live with my parents in our family home"
        return "I live with my roommate during term time"
    if "kept your room" in ql or ("tidy" in ql and "child" in ql):
        return "My mum mostly kept my room tidy when I was a child"
    if "chose your name" in ql:
        return "My parents chose my name"
    if "chose your clothes" in ql:
        return "My parents chose my clothes when I was a child"
    if "go shopping with" in ql:
        return "I usually went shopping with my parents"
    if "taught you to be polite" in ql or "taught you" in ql:
        return "My parents taught me to be polite"
    if "funniest" in ql:
        return "My roommate is the funniest person I know"
    if "teacher" in ql:
        return "My favourite teacher was a patient secondary-school teacher"
    if not bad_open and o and len(o.split()) <= 14:
        return _cap(o)
    return "Someone close to me"


_Q_SHORT_KEEP = {"car", "own", "bus", "ads", "lab", "nap", "job", "app", "map", "gym"}


def _q_tokens(qtext: str) -> list[str]:
    stop = {
        "what", "when", "where", "which", "your", "does", "have", "been", "would", "could",
        "about", "most", "often", "usually", "people", "think", "with", "from", "that", "this",
        "were", "like", "feel", "felt", "they", "them", "their", "there", "some", "many", "do",
        "did", "you", "the", "and", "for", "are", "was", "how", "who", "why", "any", "had",
        "kind", "type", "area", "part", "thing", "things", "person", "make", "made", "find",
        "give", "take", "come", "came", "know", "known", "tell", "told", "want", "well",
        "also", "just", "only", "very", "much", "more", "than", "into", "over", "after",
        "before", "other", "same", "such", "being", "having", "doing", "going", "would",
        "could", "should", "about", "next", "years", "year", "few",
    }
    toks: list[str] = []
    for w in re.findall(r"[a-z]{3,}", (qtext or "").lower()):
        if w in stop:
            continue
        if len(w) >= 4 or w in _Q_SHORT_KEEP:
            toks.append(w)
    return toks


def _token_hit(tok: str, sl: str) -> bool:
    if tok in sl:
        return True
    # light stem: choose/chose, wear/wearing, study/studies
    alts = {tok + "s", tok + "es", tok + "ed", tok + "ing", tok + "ies"}
    if tok.endswith("e"):
        alts.add(tok[:-1])  # choose -> chose roughly via "chos"
    if tok.endswith("y"):
        alts.add(tok[:-1] + "ies")
    if any(a in sl for a in alts):
        return True
    if len(tok) >= 5 and tok[:-1] in sl:
        return True
    return False


def _touch_q(text: str, qtext: str) -> str:
    """If answer misses question content words, add one short natural line (not meta)."""
    t = " ".join((text or "").split())
    toks = _q_tokens(qtext)
    sl = t.lower()
    if not toks or any(_token_hit(x, sl) for x in toks[:6]):
        return t
    w = toks[0]
    ql = (qtext or "").lower()
    if ql.startswith("who "):
        if "live with" in ql:
            line = "So that is who I live with in ordinary weeks."
        elif "teacher" in ql:
            line = "So that teacher is still the one I remember most clearly."
        else:
            line = f"So for {w}, that person is still the first name I give."
    elif ql.startswith(("what kind", "what type", "which ")):
        line = f"So for {w}, this is what I go for in real life."
    elif ql.startswith("why ") or "do you think" in ql:
        line = f"That is also why {w} matters in my own case."
    elif ql.startswith("when "):
        line = f"That timing still feels clear whenever I think about {w}."
    elif ql.startswith("how "):
        line = f"That is how I usually handle {w} in real life."
    else:
        line = f"For {w}, this is the part that feels most real to me."
    return f"{t} {line}".strip()


def _ensure_len(text: str, pad: str, qtext: str = "") -> str:
    t = _touch_q(text, qtext)
    if len(t.split()) >= 36:
        return t
    return (t + " " + pad).strip()


def _gen_from_kit(
    cat_id: str,
    qtext: str,
    words: dict[str, list[str]],
    steps: list[str],
    meta: dict[str, Any],
) -> str:
    """Natural Band-6 answer: answer the question, then tint with kit detail (partial chips/frames OK)."""
    open_ = _safe_open(_opening(words, steps, qtext), qtext.lower())
    origin = (meta.get("origin") or "").strip()
    route = meta.get("route") or {}
    freq = (route.get("freq") or _freq(_chips(words, steps[2] if len(steps) > 2 else steps[-1]))).strip()
    feel = (route.get("feel") or _adj(_chips(words, steps[-1]))).strip()
    impact = (route.get("impact") or feel).strip()
    kind = (meta.get("kind") or "").strip()
    detail = _kit_detail(kind, origin)
    ql = qtext.lower()
    pad = _feel_pad(feel, impact)

    if ql.startswith("who "):
        person = _who_person(ql, open_, detail, origin)
        body = (
            f"{person}. "
            f"In everyday life, {detail} was part of the same picture for me. "
            f"I remember this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if any(x in ql for x in ("when you were a child", "as a child", "when you were younger", "when you were a kid")):
        if "holiday" in ql or "where did you go" in ql:
            body = (
                f"{_cap(open_)}. As a child I usually went to nearby towns or parks with my family. "
                f"Sometimes {detail} was just how we got there, not the holiday itself. "
                f"I remember trips like that {freq}. I find those days {feel}."
            )
            return _ensure_len(body, pad, qtext)
        body = (
            f"{_cap(open_)}. As a child, that topic already felt familiar through simple daily life. "
            f"A small detail I still remember is {detail}. "
            f"I remember moments like that {freq}. I find those days {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith(("what kind", "what type", "which ")):
        body = (
            f"{_cap(open_)}. That is the kind of thing I mean; {detail} is only a small detail around it. "
            f"This happens {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("how often") or ql.startswith("when do"):
        body = (
            f"{_cap(open_)}. For example, I often rely on {detail}. "
            f"It is common for me to do this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("how do you") or ql.startswith("how does") or ql.startswith("how did") or ql.startswith("how is"):
        body = (
            f"{_cap(open_)}. A practical example is {detail}, which shows up in daily life. "
            f"I notice this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if "why did you choose" in ql:
        body = (
            f"{_cap(open_)}. I chose it because it matches my strengths and leads to clearer options later. "
            f"Day to day, {detail} only supports that choice in a small way. "
            f"I notice this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("why ") or "do you think" in ql or "how important" in ql or "is it necessary" in ql:
        body = (
            f"{_cap(open_)}. I think so for a practical reason, not only because of {detail}. "
            f"People often notice the difference {freq}. "
            f"I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ("prefer" in ql or " rather " in ql) and ("driver" in ql or "passenger" in ql):
        body = (
            f"{_cap(open_)}. As for being a passenger, I can rest and look outside more easily. "
            f"By contrast, driving needs full focus the whole time. "
            f"{detail} is only how I usually travel on weekdays. Overall I find being a passenger more suitable."
        )
        return _ensure_len(body, pad, qtext)
    if cat_id == "duibi" or "prefer" in ql or " rather " in ql:
        alt = _kit_detail("", meta.get("originAlt") or "") or "the other option"
        body = (
            f"{_cap(open_)}. As for one side, my first choice feels clearer in daily life. "
            f"By contrast, {alt} works differently day to day. "
            f"{detail} only colours the example a little. Overall I find {feel} more suitable."
        )
        return _ensure_len(body, pad, qtext)
    if "have you ever" in ql or ql.startswith("when did"):
        body = (
            f"{_cap(open_)}. For example, I once got used to {detail}, which left a clear impression. "
            f"That happened {freq}, so I still remember the details. "
            f"I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("what do you do") or ql.startswith("what do people") or "usually do" in ql:
        body = (
            f"{_cap(open_)}. I usually focus on {detail}, which keeps things simple. "
            f"I do this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith(("do you like", "do you enjoy", "did you like")):
        body = (
            f"{_cap(open_)}. I enjoy {detail}, which fits my routine quite well. "
            f"I usually do this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("are you a tidy") or "tidy person" in ql or "keep things tidy" in ql:
        body = (
            f"{_cap(open_)}. I try to keep my desk and room tidy before study, which helps my day run smoother. "
            f"I usually do this {freq}. {detail} is only the setting, not the whole answer. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if "forget" in ql and "name" in ql:
        body = (
            f"{_cap(open_)}. If I meet many people at once, I may forget a name after one chat. "
            f"I usually repeat the name or check it later {freq}. "
            f"I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if "career or studies" in ql or ("few years" in ql and ("career" in ql or "stud" in ql)):
        body = (
            f"{_cap(open_)}. In a few years I want to finish my degree and start a practical internship or job. "
            f"I keep taking useful courses {freq}. "
            f"I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("how does ") and "science" in ql and "daily" in ql:
        body = (
            f"It affects me every day through my phone and transport. "
            f"I use maps, weather apps and online classes, and {detail} is part of that picture. "
            f"I notice this {freq}. I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    if ql.startswith("are you") or ql.startswith("do you "):
        body = (
            f"{_cap(open_)}. In daily life I notice {detail} {freq}. "
            f"I find it {feel}."
        )
        return _ensure_len(body, pad, qtext)
    # Default fact-style
    body = (
        f"{_cap(open_)}. For example, {detail} is part of my daily life. "
        f"I notice this {freq}. I find it {feel}."
    )
    return _ensure_len(body, pad, qtext)


def _tint_hand_with_kit(text: str, meta: dict[str, Any], qtext: str = "") -> str:
    """Keep hand Q-fit; add a short Band-6 closer that differs by kit (no meta dumps)."""
    route = meta.get("route") or {}
    freq = (route.get("freq") or "").strip()
    kit_id = (meta.get("kitId") or meta.get("id") or "").strip()
    idx = sum(ord(c) for c in (kit_id or "x")) % 4
    base = [
        "In my week this feels quite clear.",
        "This is how it usually looks in my routine.",
        "That is the simple way I would say it.",
        "It is a small part of daily life for me.",
    ][idx]
    if freq and freq.lower() not in text.lower() and len(freq.split()) <= 8:
        return f"{text} I notice it {freq}. {base}".strip()
    return f"{text} {base}".strip()


def generate_sample(
    cat_id: str,
    qtext: str,
    steps: list[str],
    words: dict[str, list[str]],
    frames: dict[str, Any] | None = None,
    kit_id: str = "",
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    key = norm_q(qtext)
    kit_id = (kit_id or (meta or {}).get("kitId") or "").strip()
    meta = meta or {}

    # 1) Kit-specific hand sample
    if kit_id and (key, kit_id) in HAND_KIT_SAMPLES:
        text = _polish(HAND_KIT_SAMPLES[(key, kit_id)])
        ok, note = _logic_ok(qtext, text, cat_id)
        return {"text": text, "ok": ok, "note": note, "source": "hand-kit"}

    # 2) Shared Q hand first (Q-fit), soft-tint with kit so variants still differ
    if key in HAND_SAMPLES:
        text = _polish(HAND_SAMPLES[key])
        if kit_id and (meta.get("origin") or meta.get("route") or meta.get("kind")):
            text = _polish(_tint_hand_with_kit(text, meta, qtext))
            ok, note = _logic_ok(qtext, text, cat_id)
            return {"text": text, "ok": ok, "note": note, "source": "hand+kit"}
        ok, note = _logic_ok(qtext, text, cat_id)
        return {"text": text, "ok": ok, "note": note, "source": "hand"}

    # 3) Per-kit natural story when no hand exists
    if kit_id and (meta.get("origin") or meta.get("route") or meta.get("kind")):
        text = _polish(_gen_from_kit(cat_id, qtext, words, steps, meta))
        ok, note = _logic_ok(qtext, text, cat_id)
        return {"text": text, "ok": ok, "note": note, "source": "kit-story"}

    pack = get_question_pack(qtext)
    if pack and pack.get("sample"):
        text = _polish(pack["sample"])
        ok, note = _logic_ok(qtext, text, cat_id)
        aok, anote = _align_ok(steps, words or pack.get("words") or {}, text)
        if ok and not aok:
            ok, note = False, anote
        return {"text": text, "ok": ok, "note": note, "source": "topic-pack"}

    gen = _GEN.get(cat_id, _gen_shishi)
    text = _polish(gen(qtext, words, steps))
    ok, note = _logic_ok(qtext, text, cat_id)
    aok, anote = _align_ok(steps, words, text)
    if ok and not aok:
        ok, note = False, anote
    return {"text": text, "ok": ok, "note": note, "source": "template"}
