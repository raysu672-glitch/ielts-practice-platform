# -*- coding: utf-8 -*-
"""Offline EN→ZH for P1 sample answers: frame templates + chip glossary (+ optional API fill)."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

CACHE_PATH = Path(__file__).resolve().parent / "p1_sample_zh_cache.json"

# Long phrases first (matched before short tokens)
_PHRASES: list[tuple[str, str]] = [
    ("i'm a student", "我是学生"),
    ("i'm studying", "我在上学"),
    ("not working yet", "目前还没工作"),
    ("i chose business", "我选了商科"),
    ("it matches my strengths", "它适合我的优势"),
    ("for my future career", "为了我的未来职业"),
    ("for my future job", "为了我未来的工作"),
    ("useful for my future job", "对我未来工作有用"),
    ("useful for my future career", "对我未来职业有用"),
    ("balancing assignments", "兼顾各种作业"),
    ("exams and deadlines", "考试和截止日期"),
    ("time management", "时间管理"),
    ("morning classes first", "先上上午的课"),
    ("busy on campus", "在校园里很忙"),
    ("classes then the library", "先上课再去图书馆"),
    ("library after lunch", "午饭后去图书馆"),
    ("finish my degree", "先把学位读完"),
    ("start an internship", "开始实习"),
    ("a business-related role", "一份和商科相关的工作"),
    ("learning with classmates", "和同学一起学习"),
    ("one thing i like to do in my free time is related to my studies", "闲暇时我喜欢做和学习相关的事"),
    ("group projects", "小组项目"),
    ("business classes", "商科课程"),
    ("wechat and xiaohongshu", "微信和小红书"),
    ("mostly wechat", "主要是微信"),
    ("short-video apps", "短视频软件"),
    ("music playlists", "音乐歌单"),
    ("happy songs", "欢快的歌"),
    ("mostly music", "主要是音乐"),
    ("a simple t-shirt", "一件简单的T恤"),
    ("a sweatshirt", "一件卫衣"),
    ("a coat", "一件外套"),
    ("comfortable sneakers", "舒适的运动鞋"),
    ("a stylish pair", "一双更有型的鞋"),
    ("weekend shoes", "周末穿的鞋"),
    ("look at myself in the mirror", "照镜子看看自己"),
    ("a hallway mirror", "走廊的镜子"),
    ("a dressing mirror", "穿衣镜"),
    ("a full-length mirror", "全身镜"),
    ("the mirror in my room", "我房间里的镜子"),
    ("go to classes", "去上课"),
    ("business major", "商科专业"),
    ("my business major", "我的商科专业"),
    ("related courses", "相关课程"),
    ("library study", "图书馆学习"),
    ("handwritten notes", "手写笔记"),
    ("real books", "纸质书"),
    ("wireless earbuds", "无线耳机"),
    ("a simple watch", "一块普通手表"),
    ("recycling bins", "分类垃圾桶"),
    ("sorted rubbish", "分好的垃圾"),
    ("campus dorms", "学校宿舍"),
    ("a rented apartment", "租的公寓"),
    ("a residential area", "住宅区"),
    ("a nearby park", "附近的公园"),
    ("evening walks", "傍晚散步"),
    ("go for a walk", "去散步"),
    ("go jogging", "去慢跑"),
    ("do some sports", "做点运动"),
    ("sing a song", "唱首歌"),
    ("watch comedies", "看喜剧"),
    ("hang out with friends", "和朋友出去玩"),
    ("shopping malls", "购物中心"),
    ("a street market", "街市"),
    ("the school canteen", "学生食堂"),
    ("street food", "街头小吃"),
    ("fresh fruit", "新鲜水果"),
    ("use the subway", "坐地铁"),
    ("take a bus", "坐公交"),
    ("a small yellow bike", "一辆黄色小自行车"),
    ("my yellow bike", "我的黄色小自行车"),
    ("space documentaries", "航天纪录片"),
    ("science videos", "科普视频"),
    ("douyin short videos", "抖音短视频"),
    ("browse videos", "刷视频"),
    ("funny clips", "搞笑短视频"),
    ("subway screen ads", "地铁屏幕广告"),
    ("a patient teacher", "一位耐心的老师"),
    ("saying thank you", "说谢谢"),
    ("holding the door", "帮人扶门"),
    ("local street food", "本地小吃"),
    ("my given name", "我的名字"),
    ("its meaning", "它的含义"),
    ("my parents' choice", "父母取的"),
    ("helps me chill out", "让我放松下来"),
    ("helps me sit down and relax", "让我能坐下来放松"),
    ("helps me take a break and relax", "让我休息放松一下"),
    ("helps me relax my mind", "让我放松心情"),
    ("helps me slow down", "让我慢下来"),
    ("helps me relieve stress", "帮我解压"),
    ("helps me de-stress", "帮我减压"),
    ("helps to light up my mood", "能点亮我的心情"),
    ("makes me happy", "让我开心"),
    ("gives me a good feeling", "给我不错的感觉"),
    ("helps me enjoy a good laugh", "让我开怀大笑"),
    ("is a great stress buster", "是很好的解压方式"),
    ("helps reduce stress", "有助于减轻压力"),
    ("loose and comfortable", "宽松又舒服"),
    ("feel loose and comfortable", "感到松弛舒适"),
    ("really convenient", "非常方便"),
    ("quite useful", "挺有用的"),
    ("busy but practical", "忙碌但实用"),
    ("stressful at times", "有时会有压力"),
    ("makes me more organised", "让我更有条理"),
    ("good for the mind and the body", "对身心都有好处"),
    ("it bothers me sometimes", "有时会让我心烦"),
    ("bothers me sometimes", "有时会让我心烦"),
    ("delicious", "好吃"),
    ("necessary", "有必要"),
    ("practical", "实用"),
    ("every weekday", "每个工作日"),
    ("every day", "每天"),
    ("at weekends", "在周末"),
    ("in my spare time", "在闲暇时间"),
    ("in my free time", "在空闲时间"),
    ("from time to time", "时不时"),
    ("as often as i can", "一有机会就"),
    ("regularly", "经常"),
    ("near exam week", "临近考试周"),
    ("after lunch", "午饭后"),
    ("in the evening", "在晚上"),
    ("in a few years", "几年后"),
    ("after i graduate", "毕业之后"),
    ("every weekday after lunch", "每个工作日午饭后"),
    ("every weekday after class", "每个工作日下课后"),
    ("every weekday after classes", "每个工作日下课后"),
    ("every weekday on campus", "每个工作日在校园"),
    ("every weekday to school", "每个工作日去学校"),
    ("every weekday in rush hour", "每个工作日高峰期"),
    ("every weekday before class", "每个工作日上课前"),
    ("every weekday after i get up", "每个工作日起床后"),
    ("every weekday before i go out", "每个工作日出门前"),
    ("every weekday with classes and library time", "每个工作日上课和泡图书馆"),
    ("every weekday in cool weather", "天凉时的每个工作日"),
    ("every day after class", "每天下课后"),
    ("every day on the subway", "每天在地铁上"),
    ("every evening at home", "每天晚上在家"),
    ("every evening before i study", "每天晚上学习前"),
    ("every weekend morning", "每个周末早上"),
    ("every morning before class", "每天早上上课前"),
    ("most weekends in the evening", "多数周末晚上"),
    ("most weekends with friends", "多数周末和朋友一起"),
    ("most evenings after study", "多数学习后的傍晚"),
    ("most weekends when i hang out", "多数周末出去玩时"),
    ("most weekdays after class", "多数工作日下课后"),
    ("twice a week after class", "每周两次课后"),
    ("at weekends in the park", "周末在公园"),
    ("at weekends when i stay home", "周末待在家时"),
    ("at weekends when i go jogging", "周末慢跑时"),
    ("when i feel bored", "当我感到无聊时"),
    ("when i feel bored at weekends", "周末无聊时"),
    ("when i feel sleepy in the afternoon", "下午犯困时"),
    ("when i have time to kill", "当我有时间打发时"),
    ("when i change jackets", "换外套时"),
    ("when i go for a walk after class", "课后散步时"),
    ("when i go shopping in the city centre", "去市中心购物时"),
    ("before i go out", "出门前"),
    ("before i go out at weekends", "周末出门前"),
    ("before i go to sleep", "睡前"),
    ("after i get up", "起床后"),
    ("yes, i do", "是的，我会"),
    ("yes, i did", "是的，以前有"),
    ("yes, i used to", "是的，以前经常"),
    ("yes, i have", "是的，有过"),
    ("yes, i remember", "是的，我记得"),
    ("yes", "是的"),
    ("i prefer sitting by the window", "我更喜欢靠窗坐"),
    ("i prefer a sweatshirt", "我更喜欢卫衣"),
    ("i prefer fresh fruit", "我更喜欢新鲜水果"),
    ("they have changed a lot", "它们变化很大"),
    ("for a few clear reasons", "有几条清楚的理由"),
    ("my favourite is linked to handwritten notes", "我最喜欢的和手写笔记有关"),
    ("i went to nearby cities", "我去过附近的城市"),
    ("in a simple way", "简单来说"),
    ("it is a small city nearby", "是附近的一座小城"),
    ("a small city nearby", "附近的一座小城"),
    ("most of the time", "大多数时候"),
    ("quite often", "经常"),
    ("almost every day", "几乎每天"),
    ("most days", "多数时候"),
    ("most weekdays", "多数工作日"),
    ("with friends", "和朋友一起"),
    ("by subway", "坐地铁"),
    ("i live in dorms", "我住宿舍"),
    ("i rent an apartment", "我租公寓"),
    ("i prefer being a passenger", "我更喜欢当乘客"),
    ("i prefer the subway", "我更喜欢坐地铁"),
    ("i prefer comfort", "我更看重舒适"),
    ("i prefer a tidy desk", "我更喜欢整洁的书桌"),
    ("deadlines pile up with exams", "截止日期和考试堆在一起"),
    ("assignments keep coming", "作业一个接一个"),
    ("go to classes on campus", "在学校上课"),
    ("go to classes then library", "先上课再去图书馆"),
    ("attend classes on campus", "在校园上课"),
    ("quiet library time after lunch", "午饭后安静地泡图书馆"),
    ("build work experience", "积累工作经验"),
    ("use related courses", "用上相关课程"),
    ("we share ideas", "我们一起分享想法"),
    ("real cases on campus", "校园里的真实案例"),
    ("share opinions", "分享观点"),
    ("on campus", "在校园"),
    ("quite a long time", "挺长时间了"),
    ("for several years", "有好几年了"),
    ("since childhood", "从童年起"),
    ("in childhood", "在童年"),
    ("before i went to primary school", "上小学之前"),
    ("after i went to middle school", "上中学之后"),
    ("when i started university", "刚上大学时"),
    ("i would like coastal places", "我想去海边"),
    ("somewhere with nature", "有自然风景的地方"),
    ("a quiet city abroad", "国外一座安静的城市"),
    ("and this student routine fits me for now", "而且目前这套学生作息比较适合我"),
    ("and that pattern keeps my school day predictable", "这样一天的校园节奏也比较稳定"),
    ("and that is why i stay motivated", "这也是我保持动力的原因"),
    ("and i am preparing for it step by step", "我也在一步步准备"),
    ("and i have not regretted the decision", "而且我并不后悔这个决定"),
    ("still, i try to stay organised under pressure", "尽管如此，压力下我仍尽量保持条理"),
    ("so it has become part of my routine", "所以这已经成了我的日常习惯"),
    ("so i keep doing it without thinking too much", "所以我几乎不用多想就会继续做"),
    ("so i take it seriously in daily life", "所以在日常生活里我会认真对待"),
    ("so that is why i lean that way", "所以我才会更偏向这一边"),
    ("so that is what i usually go with", "所以我平时一般就选这个"),
    ("i come back to this idea", "我会反复想到这个想法"),
    ("whenever i take related courses", "只要我去上相关课程"),
    ("i feel the choice still fits", "就觉得这个选择仍然适合我"),
    ("especially when exams come together", "尤其是多门考试赶到一起时"),
    ("which makes a real difference", "这确实带来了明显不同"),
    ("this matters in daily life", "这在日常生活里很重要"),
    ("i keep this habit", "我保持这个习惯"),
    ("helps me get dressed quickly before i head out", "让我出门前能很快穿好衣服"),
    ("makes me look neat without spending extra hours", "不用多花时间也能看起来整洁"),
    ("helps me head out looking neat", "帮我出门时保持整洁"),
    ("avoids awkward looks in public", "避免在公共场合显得尴尬"),
    ("keeps me warm before i head out", "出门前能保暖"),
    ("is easy to put on before i head out", "出门前很好穿"),
    ("protects my feet when i go for a walk", "散步时能护住脚"),
    ("helps me do some sports without sore feet", "运动时脚不会酸痛"),
    ("lets me show preferences without hurting my feet all week", "能展现喜好又不用整周磨脚"),
    ("still works for a short walk", "短途走路也没问题"),
    ("helps me get dressed and head out with confidence", "帮我穿戴整齐、自信出门"),
    ("keeps me full without spending extra hours cooking", "吃得饱又不用花时间做饭"),
    ("lets me enjoy street food with friends", "能和朋友一起吃小吃"),
    ("gives me a quick energy boost", "能快速补充能量"),
    ("is better than takeaways for my health", "比外卖更健康"),
    ("gives me some me time after classes", "下课后能有点独处时间"),
    ("helps me finish homework independently", "帮我独立完成作业"),
    ("helps me strive in my studies with a clear desk", "书桌干净时学习更顺"),
    ("reduces small conflicts in the dorm", "减少宿舍里的小摩擦"),
]


def _load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in (data or {}).items() if v}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


_CACHE = _load_cache()


def _compile_glossary() -> list[tuple[re.Pattern[str], str]]:
    merged: dict[str, str] = {en.lower(): zh for en, zh in _PHRASES}
    for en, zh in _CACHE.items():
        merged.setdefault(en.lower(), zh)
    items = sorted(merged.items(), key=lambda x: -len(x[0]))
    return [(re.compile(re.escape(en), re.I), zh) for en, zh in items]


_GLOSS_RE = _compile_glossary()


def refresh_glossary() -> None:
    global _GLOSS_RE
    _GLOSS_RE = _compile_glossary()


_LEFTOVER_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)\bi plan to use\b"), "我计划用上"),
    (re.compile(r"(?i)\band keep building skills from my courses\b"), "，并继续从课程里积累技能"),
    (re.compile(r"(?i)\bit feels\b"), "感觉"),
    (re.compile(r"(?i)\band it\b"), "，而且它"),
    (re.compile(r"(?i)\bthough it\b"), "，虽然它"),
    (re.compile(r"(?i)\bwhich feels\b"), "，感觉"),
    (re.compile(r"(?i)\bi can look outside and feel less bored\b"), "我能往窗外看，也不容易无聊"),
    (re.compile(r"(?i)\ban aisle seat feels less interesting to me\b"), "靠过道座位对我来说没那么有意思"),
    (re.compile(r"(?i)\bi prefer sitting by the window\b"), "我更喜欢靠窗坐"),
    (re.compile(r"(?i)\bmy favourite is linked to\b"), "我最喜欢的和"),
    (re.compile(r"(?i)\bfor a few clear reasons\b"), "有几条清楚的理由"),
    (re.compile(r"(?i)\bthey have changed a lot\b"), "它们变化很大"),
    (re.compile(r"(?i)\byes, i remember\b"), "是的，我记得"),
    (re.compile(r"(?i)\bi prefer\b"), "我更喜欢"),
    (re.compile(r"(?i)\brealistic\b"), "现实可行"),
    (re.compile(r"(?i)\brespectful\b"), "有礼貌"),
    (re.compile(r"(?i)\bhandwritten notes\b"), "手写笔记"),
    (re.compile(r"(?i)\bspace documentaries\b"), "航天纪录片"),
    (re.compile(r"(?i)\bgo to classes\b"), "去上课"),
    (re.compile(r"(?i)\bthe subway\b"), "地铁"),
    (re.compile(r"(?i)\bwechat\b"), "微信"),
    (re.compile(r"(?i)\bdouyin short videos\b"), "抖音短视频"),
    (re.compile(r"(?i)\bwatch comedies\b"), "看喜剧"),
    (re.compile(r"(?i)\ba family car\b"), "家里的车"),
    (re.compile(r"(?i)\ba small yellow bike\b"), "一辆黄色小自行车"),
    (re.compile(r"(?i)\brecycling bins\b"), "分类垃圾桶"),
    (re.compile(r"(?i)\ba sweatshirt\b"), "一件卫衣"),
    (re.compile(r"(?i)\bfresh fruit\b"), "新鲜水果"),
    (re.compile(r"(?i)\bso it has become part of my routine\b"), "所以这已经成了我的日常习惯"),
    (re.compile(r"(?i)\bso that is what i usually go with\b"), "所以我平时一般就选这个"),
    (re.compile(r"(?i)\bit is a small city nearby\b"), "是附近的一座小城"),
    (re.compile(r"(?i)\bit(?=[\u4e00-\u9fff])"), "它"),
    (re.compile(r"(?i)\bit\s+(?=[\u4e00-\u9fff])"), "它"),
]


def gloss_en(text: str) -> str:
    """Replace known English chips/phrases with Chinese; leave leftovers readable."""
    s = (text or "").strip()
    if not s:
        return ""
    key = s.lower()
    if key in _CACHE:
        return _CACHE[key]
    for pat, zh in _GLOSS_RE:
        if pat.fullmatch(s) or pat.fullmatch(key):
            return zh
    out = s
    for pat, zh in _GLOSS_RE:
        out = pat.sub(zh, out)
    for pat, zh in _LEFTOVER_FIXES:
        out = pat.sub(zh, out)
    # Strip leftover articles only when followed by CJK
    out = re.sub(r"\b(a|an|the|my|our)\s+(?=[\u4e00-\u9fff])", "", out, flags=re.I)
    out = re.sub(r"\s{2,}", " ", out).strip()
    letters = sum(1 for c in out if "a" <= c.lower() <= "z")
    if letters > max(8, len(out) // 2):
        hit = _CACHE.get(key)
        if hit:
            return hit
        return out  # mixed leftover is still better than dropping translation
    return out


def _zh_sent(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    # Collapse spaces next to CJK; keep Latin word spaces
    t = re.sub(r"\s*([\u4e00-\u9fff，。！？、：；（）])\s*", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    if t[-1] not in "。！？":
        t += "。"
    return t


def _feel_zh(feel: str) -> str:
    f = (feel or "practical").strip()
    fl = f.lower()
    if fl.startswith("feel "):
        f = f[5:].strip()
        fl = f.lower()
    g = gloss_en(f)
    if fl.startswith(("help", "make", "give", "is ", "are ", "lets ", "keep")):
        return g if g.startswith(("让", "帮", "给", "是", "有")) else f"它{g}"
    if fl.startswith("it "):
        return gloss_en(f)
    return g


def _find_feel_zh(feel: str) -> str:
    return f"我觉得{_feel_zh(feel)}"


def _feel_clause_zh(feel: str) -> str:
    f = (feel or "practical").strip()
    fl = f.lower()
    if fl.startswith("feel "):
        f = f[5:].strip()
        fl = f.lower()
    g = gloss_en(f)
    if fl.startswith(("help", "make", "give", "is ", "are ", "lets ", "keep", "it ")):
        return g if fl.startswith("it ") or g.startswith(("让", "帮", "给", "是", "有", "它")) else f"它{g}"
    return f"感觉{g}"


def mymemory_translate(en: str, *, sleep_s: float = 0.35) -> str:
    """Translate one string via MyMemory; updates on-disk cache."""
    s = re.sub(r"\s+", " ", (en or "").strip())
    if not s:
        return ""
    key = s.lower()
    if key in _CACHE:
        return _CACHE[key]
    # Exact glossary hit
    g = gloss_en(s)
    if g != s and sum(1 for c in g if "a" <= c.lower() <= "z") <= 4:
        _CACHE[key] = g
        return g
    url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode(
        {"q": s[:450], "langpair": "en|zh-CN"}
    )
    try:
        with urllib.request.urlopen(url, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        zh = (data.get("responseData") or {}).get("translatedText") or ""
        zh = zh.strip()
        if data.get("responseStatus") == 200 and zh and zh.lower() != s.lower():
            _CACHE[key] = zh
            _save_cache(_CACHE)
            refresh_glossary()
            if sleep_s:
                time.sleep(sleep_s)
            return zh
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        pass
    return gloss_en(s)


def fill_chip_cache(texts: list[str], *, limit: int = 0) -> int:
    """Translate unknown chips into cache. Returns number newly fetched."""
    added = 0
    for raw in texts:
        s = re.sub(r"\s+", " ", (raw or "").strip())
        if not s:
            continue
        key = s.lower()
        if key in _CACHE:
            continue
        # Skip if fully covered by static glossary
        g = gloss_en(s)
        letters = sum(1 for c in g if "a" <= c.lower() <= "z")
        if letters <= 4:
            _CACHE[key] = g
            added += 1
            continue
        before = len(_CACHE)
        mymemory_translate(s)
        if len(_CACHE) > before:
            added += 1
        if limit and added >= limit:
            break
    _save_cache(_CACHE)
    refresh_glossary()
    return added


def translate_sample(en: str, *, intent: str = "", cat_id: str = "", meta: dict[str, Any] | None = None) -> str:
    """Produce a Chinese reading of the English sample via sentence frames + gloss."""
    meta = meta or {}
    en = re.sub(r"\s+", " ", (en or "").strip())
    if not en:
        return ""
    key = en.lower()
    if key in _CACHE and len(en) > 40:
        return _CACHE[key]

    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", en) if p.strip()]
    zh_parts: list[str] = []
    for p in parts:
        core = p[:-1] if p[-1] in ".!?" else p
        zh_parts.append(_zh_sent(_frame_or_gloss(core, intent=intent, cat_id=cat_id, meta=meta)))
    zh = "".join(zh_parts)
    # Prefer cached whole-sample translation if frames left too much English
    letters = sum(1 for c in zh if "a" <= c.lower() <= "z")
    if letters > max(20, len(zh) // 3) and key in _CACHE:
        return _CACHE[key]
    return zh


def _frame_or_gloss(core: str, *, intent: str, cat_id: str, meta: dict[str, Any]) -> str:
    c = core.strip()
    cl = c.lower()

    if cl.startswith("yes") or cl in (
        "i'm a student",
        "i'm studying",
        "not working yet",
        "quite often",
        "most of the time",
    ):
        return gloss_en(c)

    m = re.match(r"(?i)^for example,\s*i focus on\s+(.+)$", c)
    if m:
        return f"比如，我主要专注于{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^for example,\s*(.+)$", c)
    if m:
        return f"比如，{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^whenever i am free\s+(.+),\s*i finish assignments in the library$", c)
    if m:
        return f"只要我有空（{gloss_en(m.group(1))}），我就去图书馆完成作业"

    m = re.match(r"(?i)^i chose it for the reason that\s+(.+)$", c)
    if m:
        return f"我选择它是因为{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^whenever i follow this path\s+(.+),\s*i feel the choice still fits$", c)
    if m:
        return f"只要我按这条路走（{gloss_en(m.group(1))}），就觉得这个选择仍然适合我"

    m = re.match(r"(?i)^what makes it hard is\s+(.+?)(?:,\s*especially when exams come together)?$", c)
    if m:
        tail = "，尤其是多门考试赶到一起时" if "especially when exams" in cl else ""
        return f"让我觉得难的是{gloss_en(m.group(1))}{tail}"

    m = re.match(r"(?i)^this shows up\s+(.+)$", c)
    if m:
        return f"这种情况会出现在{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^i (.+), then use quiet time for study$", c)
    if m:
        return f"我会{gloss_en(m.group(1))}，然后再用安静时间学习"

    m = re.match(r"(?i)^later\s+(.+)\s+i finish assignments$", c)
    if m:
        return f"之后（{gloss_en(m.group(1))}）我会完成作业"

    m = re.match(
        r"(?i)^i plan to use\s+(.+?)\s+and keep building skills from my courses$",
        c,
    )
    if m:
        return f"我计划用上{gloss_en(m.group(1))}，并继续从课程里积累技能"

    m = re.match(r"(?i)^i plan to\s+(.+)$", c)
    if m:
        return f"我计划{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^i am working toward that\s+(.+)$", c)
    if m:
        return f"我正在朝这个方向努力（{gloss_en(m.group(1))}）"

    m = re.match(r"(?i)^i find that plan\s+(.+)$", c)
    if m:
        return f"我觉得这个计划{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^i find this routine\s+(.+)$", c)
    if m:
        return f"我觉得这套作息{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^i am keen on this for the reason that\s+(.+)$", c)
    if m:
        return f"我喜欢这一点，是因为{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^we do this\s+(.+)$", c)
    if m:
        return f"我们会在{gloss_en(m.group(1))}这样做"

    m = re.match(r"(?i)^i like it mainly because\s+(?:of\s+)?(.+)$", c)
    if m:
        return f"我喜欢它主要是因为{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^i usually keep this\s+(.+)$", c)
    if m:
        return f"我通常会保持这个习惯：{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^for the reason that\s+(.+),\s*i keep this habit$", c)
    if m:
        return f"因为{gloss_en(m.group(1))}，所以我保持这个习惯"

    m = re.match(r"(?i)^it is practical for me to keep this\s+(.+)$", c)
    if m:
        return f"对我来说，在{gloss_en(m.group(1))}保持这个习惯很实际"

    m = re.match(r"(?i)^as a result,\s*this\s+(.+)$", c)
    if m:
        return f"这样一来，这{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^since\s+(.+),\s*this matters in daily life$", c)
    if m:
        return f"因为{gloss_en(m.group(1))}，所以这在日常生活里很重要"

    m = re.match(r"(?i)^it\s+(.+),\s*which makes a real difference$", c)
    if m:
        return f"它{gloss_en(m.group(1))}，这确实带来了明显不同"

    m = re.match(
        r"(?i)^as for the first option,\s*(.+?),\s*and it\s+(.+)$",
        c,
    )
    if m:
        return f"至于第一个选项，{gloss_en(m.group(1))}，而且它{gloss_en(m.group(2))}"

    m = re.match(r"(?i)^as for the first option,\s*(.+)$", c)
    if m:
        return f"至于第一个选项，{gloss_en(m.group(1))}"

    m = re.match(
        r"(?i)^by contrast,\s*(?:the other side\s*[—\-:]?\s*)?(.+?),\s*though it\s+(.+)$",
        c,
    )
    if m:
        return f"相比之下，{gloss_en(m.group(1))}，虽然它{gloss_en(m.group(2))}"

    m = re.match(r"(?i)^by contrast,\s*(?:the other side\s*[—\-:]?\s*)?(.+)$", c)
    if m:
        return f"相比之下，{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^personally,\s*i prefer the first,\s*(?:and\s+)?(.+)$", c)
    if m:
        return f"就我个人而言，我更喜欢第一个，而且{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^my favourite is linked to\s+(.+)$", c)
    if m:
        return f"我最喜欢的和{gloss_en(m.group(1))}有关"

    m = re.match(r"(?i)^when i was younger,\s*(.+)$", c)
    if m:
        return f"我更小的时候，{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^so i prefer sitting by the window,\s*which feels\s+(.+)$", c)
    if m:
        return f"所以我更喜欢靠窗坐，感觉{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^as for a window seat,\s*(.+)$", c)
    if m:
        return f"至于靠窗座位，{gloss_en(m.group(1))}"

    m = re.match(r"(?i)^by contrast, an aisle seat feels less interesting to me$", c)
    if m:
        return "相比之下，靠过道座位对我来说没那么有意思"

    m = re.match(r"(?i)^i find (?:that )?(?:it )?(.+)$", c)
    if m:
        inner = m.group(1).strip()
        return f"我觉得{_feel_zh(inner) if not inner.lower().startswith(('that ', 'this ')) else gloss_en(inner)}"

    m = re.match(r"(?i)^it feels\s+(.+)$", c)
    if m:
        return f"感觉{gloss_en(m.group(1))}"

    m = re.match(
        r"(?i)^(?:and )?(.+)$",
        c,
    )
    # Material origin narratives — cache first; optional API only if explicitly enabled
    if len(c.split()) >= 8:
        cached = _CACHE.get(cl)
        if cached:
            return cached
        g = gloss_en(c)
        if sum(1 for ch in g if "a" <= ch.lower() <= "z") <= 8:
            return g
        import os

        if os.environ.get("P1_SAMPLE_ZH_API", "").strip() in ("1", "true", "yes"):
            return mymemory_translate(c, sleep_s=0.25)
        return g

    return gloss_en(c)
