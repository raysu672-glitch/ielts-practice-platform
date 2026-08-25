# -*- coding: utf-8 -*-
"""Shared constants and helpers for P1 word banks (no generated data)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CAT_STEPS: dict[str, list[str]] = {
    "shishi": ["正面回答", "来源或举例", "频次", "感受"],
    "xihao": ["正面回答", "原因或时间", "频次", "感受"],
    "xingwei": ["正面回答", "原因", "时间线+行为描述", "影响"],
    "guandian": ["正面回答", "举例或原因", "作用或影响", "感受"],
    "duibi": ["正面回答", "选项1的特点与作用", "选项2的特点与作用", "个人感受"],
}

GENERIC_CHIPS = frozenset(
    {
        "for example",
        "in my daily life",
        "main reason",
        "a specific memory",
        "in daily life",
    }
)

TOPIC_KITS: dict[str, dict[str, Any]] = {
    "watch": {
        "mat": "物品·手表（实用计时）",
        "logic": "手表=实用计时工具，不谈奢侈；礼物/佩戴/重要性都落在 convenient + check the time。",
        "chips": ["watch", "check the time", "convenient", "birthday gift", "smartwatch"],
    },
    "cars": {
        "logic": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
        "chips": ["family road trips", "comfortable seats", "passenger", "rush hour", "driver"],
    },
    "work or studies": {
        "logic": "学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
        "chips": ["my major", "attend classes", "library", "assignments", "future career"],
    },
    "websites": {
        "logic": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
        "chips": ["search information", "watch short videos", "study resources", "Xiaohongshu", "useful"],
    },
    "teachers": {
        "logic": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
        "chips": ["favourite teacher", "explain concepts", "encourage me", "primary school", "patient"],
    },
    "public gardens and parks": {
        "logic": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
        "chips": ["park", "go for a walk", "fresh air", "hang out", "childhood"],
    },
    "the area you live in": {
        "logic": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
        "chips": ["a residential area", "neighbors", "quiet", "convenience stores", "10-minute walk"],
    },
    "shopping": {
        "logic": "购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。",
        "chips": ["shop online", "shopping malls", "pay by phone", "return items", "convenient"],
    },
    "mirrors": {
        "logic": "镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。",
        "chips": ["look at myself in the mirror", "get dressed", "before heading out", "check my look"],
    },
    "music": {
        "logic": "音乐=listen to music 解压；课/心情题都回到 relieve stress。",
        "chips": ["listen to music", "headphones", "relieve stress", "happy songs", "while studying"],
    },
    "home & accommodation": {
        "logic": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
        "chips": ["dorms", "my rented apartment", "roommate", "living room", "subway"],
    },
    "clothing": {
        "logic": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
        "chips": ["t-shirt", "coat", "sweatshirt", "comfortable", "casual"],
    },
    "tidiness": {
        "logic": "整洁=study space tidy → focus better，童年对比一句即可。",
        "chips": ["keep tidy", "study desk", "put things away", "focus better", "childhood"],
    },
    "hometown": {
        "logic": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
        "chips": ["hometown", "small city", "famous for", "local food", "young people"],
    },
    "headphones": {
        "logic": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
        "chips": ["headphones", "listen to music", "block noise", "on the subway", "wireless"],
    },
    "social media": {
        "logic": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
        "chips": ["WeChat", "Xiaohongshu", "post photos", "watch short videos", "keep in touch"],
    },
    "singing": {
        "logic": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
        "chips": ["sing a song", "KTV", "music class", "with friends", "it always cheers me up"],
    },
    "outer space and stars": {
        "logic": "太空题用 science fiction movies / documentaries，别装专业天文。",
        "chips": ["science fiction movies", "documentaries", "curious", "stars", "universe"],
    },
    "the city you live in": {
        "logic": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
        "chips": ["this city", "subway", "friendly people", "weather", "big changes"],
    },
    "science": {
        "logic": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
        "chips": ["science class", "experiments", "science museum", "biology", "curious"],
    },
    "jokes & comedies": {
        "logic": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
        "chips": ["tell jokes", "watch comedies", "have a good laugh", "live show", "funny"],
    },
    "building": {
        "logic": "建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
        "chips": ["tall buildings", "near my home", "take photos", "city centre", "landmarks"],
    },
    "gifts": {
        "logic": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
        "chips": ["handmade gift", "birthday", "thoughtful", "receiver's preference", "happy"],
    },
    "pets and animals": {
        "logic": "宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。",
        "chips": ["a puppy", "zoo", "take care of", "unwind", "animals"],
    },
    "typing": {
        "logic": "打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
        "chips": ["laptop keyboard", "type every day", "practice", "faster", "assignments"],
    },
    "memory": {
        "logic": "记忆=phone notes / to-do list，忘事承认 once forgot + lesson。",
        "chips": ["phone notes", "to-do list", "reminders", "forgot something", "important"],
    },
    "sports team": {
        "logic": "运动队=basketball/volleyball + teamwork，观看与参与同一套。",
        "chips": ["sports team", "basketball", "volleyball", "teamwork", "at weekends"],
    },
    "life stages": {
        "logic": "人生阶段用 childhood → university → next five years，计划落回 study。",
        "chips": ["childhood", "university", "next five years", "hang out", "career plan"],
    },
    "walking": {
        "logic": "走路=go for a walk in the park，解压+景色一笔带过。",
        "chips": ["go for a walk", "park", "after dinner", "fresh air", "relax"],
    },
    "scenery": {
        "logic": "景色=travel + take photos，山/海对比用 mountains vs sea。",
        "chips": ["beautiful scenery", "while travelling", "take photos", "mountains", "sea"],
    },
    "views": {
        "logic": "与 scenery 共用 take photos of views，城乡对比即可。",
        "chips": ["views", "take pictures", "rural areas", "urban areas", "unforgettable"],
    },
    "crowded place": {
        "logic": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
        "chips": ["city centre", "rush hour", "shopping malls", "crowded", "noisy"],
    },
    "spare time": {
        "logic": "空闲时间直接套 daily leisure：watch short videos / hang out / sports。",
        "chips": ["spare time", "watch short videos", "hang out", "do some sports", "relax"],
    },
    "food": {
        "logic": "食物=favourite dish + street food/takeout，童年口味变化一句。",
        "chips": ["favourite food", "street food", "takeout", "delicious", "childhood"],
    },
    "morning time": {
        "logic": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
        "chips": ["get up", "have breakfast", "get dressed", "head out", "alarm"],
    },
    "childhood activities": {
        "logic": "童年活动=play outside / with friends，现在对比更 indoor。",
        "chips": ["childhood", "play outside", "with friends", "alone", "now prefer"],
    },
    "reading": {
        "logic": "阅读=read books / flip through pages，纸质 vs 屏幕对比。",
        "chips": ["read", "physical books", "on a screen", "carefully", "in my free time"],
    },
    "hobby": {
        "logic": "爱好直接指向 listen to music / sports / reading 中已背的一项。",
        "chips": ["hobby", "since childhood", "listen to music", "do some sports", "family"],
    },
}


def norm_q(s: str) -> str:
    s = (s or "").lower().strip()
    for a, b in [("'", "'"), ("'", "'"), ("'", "'")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "", s)


CLUE_ALIAS: dict[str, str] = {
    norm_q("Have you ever sent handmade gifts to others?"): "haveyoueversenthandmadegiftsreceivedagreatgiftwhatgiftrecently",
    norm_q("Have you ever received a great gift?"): "haveyoueversenthandmadegiftsreceivedagreatgiftwhatgiftrecently",
    norm_q("What gift have you received recently?"): "haveyoueversenthandmadegiftsreceivedagreatgiftwhatgiftrecently",
    norm_q("Is the city where you live crowded?"): "iscitycrowdedcrowdedplacenearyoulasttimeincrowdedplace",
    norm_q("Is there a crowded place near where you live?"): "iscitycrowdedcrowdedplacenearyoulasttimeincrowdedplace",
    norm_q("When was the last time you were in a crowded place?"): "iscitycrowdedcrowdedplacenearyoulasttimeincrowdedplace",
    norm_q("What subjects are you studying?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("Why did you choose to study that subject?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("What work do you do?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("Why did you choose to do that type of work (or that job)?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("What requirements did you need to meet to get your current job?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("Who helps you the most? And how?"): "subjectsworkrequirementsplanswhohelpsyou",
    norm_q("What technology do you use when you study?"): "whattechnologydoyouusewhenyoustudyatwork",
    norm_q("What technology do you use at work?"): "whattechnologydoyouusewhenyoustudyatwork",
    norm_q("Can you describe the place where you live?"): "homehometownareacity",
    norm_q("Please describe the room you live in?"): "homehometownareacity",
    norm_q("How long have you lived there?"): "homehometownareacity",
    norm_q("Do you live in an apartment or a house?"): "homehometownareacity",
    norm_q("Who do you live with?"): "homehometownareacity",
    norm_q("What kinds of accommodation do you live in?"): "homehometownareacity",
    norm_q("Where is your hometown?"): "homehometownareacity",
    norm_q("Is that a big city or a small place?"): "homehometownareacity",
    norm_q("Please describe your hometown a little?"): "homehometownareacity",
    norm_q("How long have you been living there?"): "homehometownareacity",
    norm_q("What's your hometown famous for?"): "homehometownareacity",
    norm_q("What city do you live in?"): "homehometownareacity",
    norm_q("How long have you lived in this city?"): "homehometownareacity",
    norm_q("Is this city your permanent residence?"): "homehometownareacity",
    norm_q("What's the weather like where you live?"): "homehometownareacity",
    norm_q("Do you know any famous people in your area?"): "homehometownareacity",
    norm_q("What are some changes in the area recently?"): "homehometownareacity",
    norm_q("Do you know any of your neighbors?"): "homehometownareacity",
    norm_q("Are the people in your neighborhood nice and friendly?"): "homehometownareacity",
    norm_q("Do you live in a noisy or a quiet area?"): "homehometownareacity",
    norm_q("Are there big changes in this city?"): "homehometownareacity",
    norm_q("Are there people of different ages living in this city?"): "homehometownareacity",
    norm_q("Are the people friendly in the city?"): "homehometownareacity",
    norm_q("When did you learn how to type on a keyboard?"): "whendidyoulearnhowtotypehowdoyouimproveyourtyping",
    norm_q("How do you improve your typing?"): "whendidyoulearnhowtotypehowdoyouimproveyourtyping",
    norm_q("What did you do in the morning when you were little? Why?"): "whatdidyoudointhemorningwhenyouwerelittle",
    norm_q("Have you ever visited a zoo?"): "haveyoueverhadapetbefore",
    norm_q("Do you like the area that you live in?"): "doyouliketheareathatyoulivein",
    norm_q("Where do you like to go in that area?"): "wheredoyouliketogointhatarea",
    norm_q("Do you like this city? Why?"): "doyoulikethiscitywhy",
    norm_q("Would you recommend your city to others?"): "wouldyourecommendyourcitytoothers",
    norm_q("Do you often see your neighbors?"): "doyouoftenseeyourneighbors",
    norm_q("Is the city friendly to children and old people?"): "isthecityfriendlytochildrenandoldpeople",
}


def pack(cat_id: str, a: list[str], b: list[str], c: list[str], d: list[str]) -> dict[str, list[str]]:
    steps = CAT_STEPS[cat_id]
    return {steps[0]: a, steps[1]: b, steps[2]: c, steps[3]: d}


def _load_fixes_from_parse() -> dict[str, str]:
    parse_path = Path(r"G:\口语练习\_parse_p1_full.py")
    if not parse_path.is_file():
        return {}
    text = parse_path.read_text(encoding="utf-8")
    m = re.search(r"FIXES\s*=\s*\{", text)
    if not m:
        return {}
    start = m.end() - 1
    depth = 0
    end = start
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    blob = text[start:end]
    fixes: dict[str, str] = {}
    for line in blob.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line in ("{", "}"):
            continue
        if ":" not in line:
            continue
        key_part, val_part = line.split(":", 1)
        key_part = key_part.strip().rstrip(",")
        val_part = val_part.strip().rstrip(",")
        if not (key_part.startswith("'") or key_part.startswith('"')):
            continue
        key = key_part[1:-1]
        if val_part.startswith("'") and val_part.endswith("'"):
            val = val_part[1:-1]
        elif val_part.startswith('"') and val_part.endswith('"'):
            val = val_part[1:-1]
        else:
            continue
        fixes[key] = val
    return fixes


FIXES: dict[str, str] = _load_fixes_from_parse()


def fix_phrase(phrase: str) -> str:
    p = phrase.strip().strip(".,;:")
    if p in FIXES:
        return FIXES[p]
  # partial replacements for long combined chips
    out = p
    for old, new in sorted(FIXES.items(), key=lambda x: -len(x[0])):
        if old in out and len(old) > 8:
            out = out.replace(old, new)
    return out


def apply_fixes(chips: list[str]) -> list[str]:
    out: list[str] = []
    for chip in chips:
        parts = [fix_phrase(x.strip()) for x in re.split(r"[,;/]", chip) if x.strip()]
        if len(parts) > 1 and "," in chip:
            out.extend(parts)
        else:
            out.append(fix_phrase(chip))
    dedup: list[str] = []
    seen: set[str] = set()
    for c in out:
        k = c.lower()
        if k and k not in seen and k not in GENERIC_CHIPS:
            seen.add(k)
            dedup.append(c)
    return dedup


def kit_for(topic_en: str) -> dict[str, Any]:
    key = topic_en.lower().strip()
    kit: dict[str, Any] | None = None
    if key in TOPIC_KITS:
        kit = TOPIC_KITS[key]
    else:
        for k, v in TOPIC_KITS.items():
            if k in key or key in k:
                kit = v
                break
    if kit is None:
        kit = {"logic": "用具体场景撑满四步，避免编造复杂故事。", "chips": ["park", "library", "city centre", "in my free time", "practical"]}
    if "mat" not in kit:
        kit = {**kit, "mat": str(kit.get("logic", "")).split("；")[0]}
    return kit


# Neutral padding only when a step has fewer than 3 chips (never inject topic-kit fillers).
_PAD_BY_CAT: dict[str, list[list[str]]] = {
    "shishi": [
        ["Yes", "Definitely", "Not really", "Sometimes"],
        ["such as", "in particular", "for instance"],
        ["every day", "from time to time", "at weekends"],
        ["practical", "really convenient", "quite useful", "helpful"],
    ],
    "xihao": [
        ["Yes", "Definitely", "I love it", "Not really"],
        ["because", "when I", "for the reason that"],
        ["quite often", "at weekends", "from time to time"],
        ["feel relaxed", "really enjoyable", "it always cheers me up"],
    ],
    "xingwei": [
        ["Yes", "Usually", "Definitely", "Not really"],
        ["since", "for the reason that", "because"],
        ["every morning", "before class", "after dinner"],
        ["helps me stay focused", "saves time", "keeps me organised"],
    ],
    "guandian": [
        ["Yes", "I think so", "It depends", "Somewhat"],
        ["since", "for example", "in my view"],
        ["in daily life", "for most people", "quite often"],
        ["quite important", "makes sense", "understandable"],
    ],
    "duibi": [
        ["I prefer A", "I'd rather", "It depends"],
        ["is regarded as", "more convenient", "less stressful"],
        ["by contrast", "on the other hand", "find it harder"],
        ["I prefer", "which is why", "more comfortable"],
    ],
}


def enrich_step_words(
    chips: list[str],
    cat_id: str,
    topic_en: str,
    step_name: str,
    steps: list[str],
) -> list[str]:
    cleaned = apply_fixes(chips)
    if len(cleaned) >= 3:
        return cleaned[:5]

    step_idx = steps.index(step_name)
    pads = _PAD_BY_CAT.get(cat_id, _PAD_BY_CAT["shishi"])
    extras = pads[step_idx] if step_idx < len(pads) else pads[-1]
    merged = apply_fixes(cleaned + [x for x in extras if x not in cleaned])
    return merged[:5]


def tweak_combined(cat_id: str, qtext: str, words: dict[str, list[str]], steps: list[str]) -> dict[str, list[str]]:
    ql = qtext.lower()
    out = {s: list(words.get(s, [])) for s in steps}
    if "who helps" in ql:
        out[steps[0]] = ["My parents", "My close friends", "Definitely"]
        out[steps[1]] = ["give me advice", "encourage me", "help with planning"]
    elif "requirement" in ql or "current job" in ql:
        out[steps[0]] = ["Several requirements", "Yes", "Quite a few"]
        out[steps[1]] = ["a degree", "relevant experience", "good communication skills"]
    elif "why did you choose" in ql and "subject" in ql:
        out[steps[0]] = ["Because I'm interested in it", "Definitely", "Passion"]
        out[steps[1]] = ["passion for the subject", "future career", "my strengths"]
    elif "subjects are you studying" in ql:
        out[steps[0]] = ["I'm majoring in...", "Yes", "Several subjects"]
        out[steps[1]] = ["business", "economics", "related courses"]
    elif "what work do you" in ql:
        out[steps[0]] = ["I'm a student", "I work part-time", "Internship"]
        out[steps[1]] = ["internship", "tutor", "on campus"]
    elif "sent handmade" in ql:
        out[steps[1]] = ["a handmade card", "knitted scarf", "DIY gift"]
    elif "received a great" in ql or "received recently" in ql:
        out[steps[1]] = ["a thoughtful gift", "from my best friend", "last month"]
    elif "crowded" in ql and "city where you live" in ql:
        out[steps[1]] = ["downtown", "rush hour", "shopping malls"]
    elif "crowded place near" in ql:
        out[steps[1]] = ["the city centre", "near the subway station", "weekend markets"]
    elif "last time" in ql and "crowded" in ql:
        out[steps[1]] = ["the shopping mall", "during a holiday", "last weekend"]
    elif "famous people" in ql and "area" in ql:
        out[steps[1]] = ["a local influencer", "heard on TV", "community leader"]
    elif "changes in the area" in ql:
        out[steps[1]] = ["new shopping malls", "more cafes", "subway extension"]
    elif "neighbors" in ql and "know" in ql:
        out[steps[1]] = ["say hello", "same building", "elderly couple"]
    elif "neighborhood nice" in ql or "neighbourhood nice" in ql:
        out[steps[1]] = ["help each other", "friendly greetings", "quiet community"]
    elif "noisy or a quiet" in ql:
        out[steps[1]] = ["residential area", "near main road", "peaceful at night"]
    elif "transport facilities" in ql:
        out[steps[1]] = ["near the subway", "bus stops nearby", "easy commute"]
    elif "history of your hometown" in ql and "school" in ql:
        out[steps[1]] = ["history class", "local history", "in textbooks"]
    elif "young people" in ql and "hometown" in ql:
        out[steps[1]] = ["university students", "young workers", "start-ups"]
    elif "history of your hometown" in ql:
        out[steps[1]] = ["local museum", "family stories", "history books"]
    elif "culture of your hometown" in ql:
        out[steps[1]] = ["local festivals", "traditional food", "folk customs"]
    elif "big changes in this city" in ql:
        out[steps[1]] = ["new skyscrapers", "expanded subway", "more parks"]
    elif "different ages" in ql:
        out[steps[1]] = ["young professionals", "families with kids", "elderly residents"]
    elif "people friendly in the city" in ql:
        out[steps[1]] = ["helpful strangers", "polite in shops", "give directions"]
    elif "describe the room" in ql:
        out[steps[1]] = ["my bedroom", "small but cosy", "desk and wardrobe"]
    elif "describe the place where you live" in ql:
        out[steps[1]] = ["a residential area", "convenience stores nearby", "quiet street"]
    elif "apartment or a house" in ql:
        out[steps[1]] = ["an apartment", "with my family", "in a high-rise"]
    elif "who do you live with" in ql:
        out[steps[1]] = ["my parents", "roommates", "my family"]
    elif "kinds of accommodation" in ql:
        out[steps[1]] = ["student dorms", "rented apartment", "shared flat"]
    elif "where is your hometown" in ql:
        out[steps[1]] = ["in the south", "a coastal city", "central China"]
    elif "big city or a small" in ql:
        out[steps[1]] = ["a medium-sized city", "not too big", "manageable size"]
    elif "describe your hometown" in ql:
        out[steps[1]] = ["local food", "friendly people", "nice scenery"]
    elif "hometown famous for" in ql:
        out[steps[1]] = ["local cuisine", "historical sites", "natural scenery"]
    elif "what city do you live" in ql:
        out[steps[1]] = ["a major city", "university town", "where I study"]
    elif "permanent residence" in ql:
        out[steps[1]] = ["for now yes", "while studying", "not sure long-term"]
    elif "weather like where you live" in ql:
        out[steps[1]] = ["hot summers", "mild winters", "four seasons"]
    return out
