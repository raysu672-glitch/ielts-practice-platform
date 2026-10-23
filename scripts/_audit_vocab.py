#!/usr/bin/env python3
"""Audit vocabulary in modules.js and embedded HTML word lists."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES_JS = ROOT / "sources/tinglidanciceshi/js/modules.js"
LISTENING_HTML = ROOT / "sources/tinglidanciceshi/listening.html"
LISTENING_BASIC_HTML = ROOT / "sources/tinglidanciceshi/listening_basic.html"

# Known high-confidence fixes for listening basic (Chinglish / spelling / grammar)
BASIC_KNOWN_ISSUES = {
    "alarming system": ("alarm system", "语法"),
    "animals behavior": ("animal behaviour / animal behavior", "语法"),
    "golf court": ("golf course", "拼写"),
    "advance level": ("advanced level", "拼写"),
    "bottle water": ("bottled water", "语法"),
    "children mind": ("childminder / childcare", "中式/语法"),
    "china stone": ("China stone (porcelain clay)", "逻辑/拼写"),
    "culture awareness": ("cultural awareness", "语法"),
    "culture context": ("cultural context", "语法"),
    "defense": ("defence / defense", "拼写(美式可接受)"),
    "driving license": ("driving licence / driving license", "拼写(美式可接受)"),
    "families life": ("family life", "语法"),
    "finance market": ("financial market", "语法"),
    "firework": ("fireworks", "语法"),
    "flavor": ("flavour / flavor", "拼写(美式可接受)"),
    "free pick": ("free pickup", "拼写"),
    "hairs": ("hair", "语法"),
    "jewelry": ("jewellery / jewelry", "拼写(美式可接受)"),
    "kilometers": ("kilometres / kilometers", "拼写(英式)"),
    "license": ("licence / license", "拼写(美式可接受)"),
    "plane science": ("planet science", "拼写"),
    "political man": ("politician", "中式"),
    "privacy company": ("private company", "拼写/逻辑"),
    "repaired cost": ("repair cost", "语法"),
    "rumor": ("rumour / rumor", "拼写(美式可接受)"),
    "study skill": ("study skills", "语法"),
    "swimming suit": ("swimming suit / swimsuit", "用法"),
    "time consuming": ("time-consuming", "语法"),
    "traveling": ("travelling / traveling", "拼写(美式可接受)"),
    "weathers": ("weather", "语法"),
    "cooperation loan": ("co-operative loan / cooperation loan(?)", "逻辑"),
    "pet meat": ("pet food(?)", "逻辑"),
    "statement position": ("statement of position(?)", "逻辑"),
    "triangle sharp": ("sharp triangle(?)", "语法"),
    "objective matters": ("objective matters(?)", "逻辑"),
    "note system": ("note-taking system(?)", "逻辑"),
    "personal officer": ("personnel officer", "拼写"),
    "centimeter": ("centimetre / centimeter", "拼写(美式可接受)"),
    "programmes": None,  # British OK
    "programs": None,
    "behavior": None,
    "behaviors": ("behaviour / behavior", "拼写(美式可接受)"),
    "organize": ("organise / organize", "拼写(美式可接受)"),
    "color": None,
}

# Phrase category known issues (manual curation from reading modules.js)
PHRASE_KNOWN_ISSUES = [
    ("a drastic decrement", "a drastic decrease / drop", "语法", "小作文词伙二"),
    ("be twice the size of it was in 2015", "be twice the size it was in 2015 / twice as large as in 2015", "语法", "小作文词伙三"),
    ("be located on the shopping mall", "be located next to the shopping mall", "语法", "小作文词伙三"),
    ("rise more than eight fold", "rise more than eightfold", "拼写", "小作文词伙三"),
    ("fluctuate upwardly", "fluctuate upward", "语法", "小作文词伙二"),
    ("remain roughly static", "remain roughly stable / static", "语法", "小作文词伙二"),
    ("discriminate between right and wrong", "distinguish between right and wrong", "用法", "暴力犯罪类"),
    ("financial-disadvantaged families", "financially disadvantaged families", "语法", "家庭旅游类"),
    ("attach importance to education background", "attach importance to educational background", "语法", "品格教育类"),
    ("be obedient to parents 'expectations", "be obedient to parents' expectations", "拼写", "品格教育类"),
    ("cultural devolution", "cultural degradation / decline", "用法", "人文历史类"),
    ("discriminate on the basis of gender", "discrimination on the basis of gender / gender discrimination", "语法", "商业职场类"),
    ("exploit the nature excessively", "exploit nature excessively", "语法", "能源环保类"),
    ("break ecological balance", "disrupt ecological balance", "用法", "能源环保类"),
    ("create a favorable condition", "create favourable conditions", "语法", "能源环保类"),
    ("be crucial to protecting the environment", "be crucial for protecting the environment", "语法", "能源环保类"),
    ("过渡地开采大自然", "过度地开采自然", "中英", "能源环保类"),
    ("寻求在线退款复杂而低效", "seeking a refund online is cumbersome and inefficient", "语法", "网络科技类"),
    ("可以无限制的上网", "be given unlimited internet access", "语法", "网络科技类"),
    ("增长的最大", "增幅最大 / the largest increase", "中英", "小作文词伙二"),
    ("保持大致的不变的", "保持大致不变", "中英", "小作文词伙二"),
    ("对保护环境重要", "对保护环境至关重要", "中英", "能源环保类"),
    ("又流行起来", "再度流行 / come back into fashion", "中英", "网络科技类"),
    ("非常的昂贵", "极其昂贵", "中英", "媒体广告类"),
    ("有更高的社会接受度", "be more socially acceptable", "中英", "政府社会类"),
]

# Suspicious patterns in English phrases
EN_PATTERNS = [
    (re.compile(r"\bdecrement\b", re.I), "decrement", "decrease/drop", "语法"),
    (re.compile(r"\bupwardly\b", re.I), "upwardly", "upward", "语法"),
    (re.compile(r"size of it was", re.I), "size of it was", "size it was / as large as", "语法"),
    (re.compile(r"located on the shopping mall", re.I), "located on the shopping mall", "located next to/near the shopping mall", "语法"),
    (re.compile(r"eight fold", re.I), "eight fold", "eightfold", "拼写"),
    (re.compile(r"financial-disadvantaged", re.I), "financial-disadvantaged", "financially disadvantaged", "语法"),
    (re.compile(r"parents '\\s*'expectations", re.I), "parents 'expectations", "parents' expectations", "拼写"),
    (re.compile(r"cultural devolution", re.I), "cultural devolution", "cultural degradation/decline", "用法"),
    (re.compile(r"discriminate on the basis", re.I), "discriminate on the basis", "discrimination on the basis", "语法"),
    (re.compile(r"exploit the nature", re.I), "exploit the nature", "exploit nature", "语法"),
    (re.compile(r"break ecological balance", re.I), "break ecological balance", "disrupt ecological balance", "用法"),
    (re.compile(r"a favorable condition\b", re.I), "a favorable condition", "favourable conditions", "语法"),
    (re.compile(r"discriminate between right and wrong", re.I), "discriminate between right and wrong", "distinguish between right and wrong", "用法"),
]

# Chinglish / wrong collocation patterns in basic words
BASIC_PATTERNS = [
    (re.compile(r"^alarming system$", re.I), "alarming system", "alarm system", "语法"),
    (re.compile(r"^animals behavior$", re.I), "animals behavior", "animal behaviour/behavior", "语法"),
    (re.compile(r"^golf court$", re.I), "golf court", "golf course", "拼写"),
    (re.compile(r"^advance level$", re.I), "advance level", "advanced level", "拼写"),
    (re.compile(r"^bottle water$", re.I), "bottle water", "bottled water", "语法"),
    (re.compile(r"^children mind$", re.I), "children mind", "childminder/childcare", "中式/语法"),
    (re.compile(r"^culture awareness$", re.I), "culture awareness", "cultural awareness", "语法"),
    (re.compile(r"^culture context$", re.I), "culture context", "cultural context", "语法"),
    (re.compile(r"^families life$", re.I), "families life", "family life", "语法"),
    (re.compile(r"^finance market$", re.I), "finance market", "financial market", "语法"),
    (re.compile(r"^free pick$", re.I), "free pick", "free pickup", "拼写"),
    (re.compile(r"^hairs$", re.I), "hairs", "hair", "语法"),
    (re.compile(r"^plane science$", re.I), "plane science", "planet science", "拼写"),
    (re.compile(r"^political man$", re.I), "political man", "politician", "中式"),
    (re.compile(r"^privacy company$", re.I), "privacy company", "private company", "拼写/逻辑"),
    (re.compile(r"^repaired cost$", re.I), "repaired cost", "repair cost", "语法"),
    (re.compile(r"^study skill$", re.I), "study skill", "study skills", "语法"),
    (re.compile(r"^weathers$", re.I), "weathers", "weather", "语法"),
    (re.compile(r"^personal officer$", re.I), "personal officer", "personnel officer", "拼写"),
    (re.compile(r"^pet meat$", re.I), "pet meat", "pet food", "逻辑"),
    (re.compile(r"^cooperation loan$", re.I), "cooperation loan", "co-operative loan(?)", "逻辑"),
    (re.compile(r"^triangle sharp$", re.I), "triangle sharp", "sharp triangle", "语法"),
    (re.compile(r"^firework$", re.I), "firework", "fireworks", "语法"),
    (re.compile(r"^time consuming$", re.I), "time consuming", "time-consuming", "语法"),
    (re.compile(r"^attack humans$", re.I), "attack humans", "attack humans (OK) or attacks on humans", "用法"),
]

# Meaning sanity checks for listening_basic.html
MEANING_CHECKS = [
    (re.compile(r"^academic$", re.I), "学院的", "学术的；学院的", "中英"),
    (re.compile(r"^achievement$", re.I), "完成达到", "成就；完成", "中英"),
    (re.compile(r"^acknowledgement$", re.I), None, None, None),  # check dynamically
    (re.compile(r"^alarming system$", re.I), None, "报警系统", "中英"),
    (re.compile(r"^animals behavior$", re.I), None, "动物行为", "中英"),
    (re.compile(r"^golf court$", re.I), None, "高尔夫球场", "中英"),
    (re.compile(r"^advance level$", re.I), None, "高级水平", "中英"),
    (re.compile(r"^children mind$", re.I), None, "托儿/看孩子", "中英"),
    (re.compile(r"^political man$", re.I), None, "政治家", "中英"),
    (re.compile(r"^privacy company$", re.I), None, "私人公司", "中英"),
    (re.compile(r"^plane science$", re.I), None, "行星科学", "中英"),
    (re.compile(r"^personal officer$", re.I), None, "人事专员", "中英"),
    (re.compile(r"^pet meat$", re.I), None, "宠物食品", "中英"),
    (re.compile(r"^weathers$", re.I), None, "天气", "中英"),
    (re.compile(r"^hairs$", re.I), None, "头发", "中英"),
    (re.compile(r"^finance market$", re.I), None, "金融市场", "中英"),
    (re.compile(r"^families life$", re.I), None, "家庭生活", "中英"),
    (re.compile(r"^culture awareness$", re.I), None, "文化意识", "中英"),
    (re.compile(r"^bottle water$", re.I), None, "瓶装水", "中英"),
    (re.compile(r"^free pick$", re.I), None, "免费接送", "中英"),
    (re.compile(r"^repaired cost$", re.I), None, "维修费用", "中英"),
    (re.compile(r"^study skill$", re.I), None, "学习技巧", "中英"),
    (re.compile(r"^cooperation loan$", re.I), None, "合作贷款(?)", "逻辑"),
]

# listening.html meaning checks - sample high-confidence wrong translations
LISTENING_MEANING_CHECKS = [
    (re.compile(r"^Rafael$", re.I), None, "拉斐尔(人名)", "逻辑"),
    (re.compile(r"^Patterson$", re.I), None, "帕特森(人名)", "逻辑"),
    (re.compile(r"^living room$", re.I), None, "客厅", "中英"),
    (re.compile(r"^artificial$", re.I), None, "人工的；人造的", "中英"),
    (re.compile(r"^intelligence$", re.I), None, "智能；智力", "中英"),
    (re.compile(r"^mouse$", re.I), None, "鼠标；老鼠", "中英"),
    (re.compile(r"^present$", re.I), None, "礼物；呈现", "中英"),
    (re.compile(r"^note$", re.I), None, "纸币；笔记", "中英"),
    (re.compile(r"^flat$", re.I), None, "公寓；平的", "中英"),
    (re.compile(r"^coach$", re.I), None, "教练；长途汽车", "中英"),
    (re.compile(r"^firm$", re.I), None, "公司；坚固的", "中英"),
]

PROPER_NOUNS = {
    "Rafael", "Patterson", "Mexico", "China", "Europe", "Africa", "Italian",
    "Chinese", "Sunday", "Wednesday", "September", "Argentina", "France",
    "Germany", "India", "Japan", "Scotland", "Russia", "Spanish",
}


def extract_js_array(name: str, text: str) -> list:
    m = re.search(rf"var\s+{re.escape(name)}\s*=\s*\[", text)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    in_str = False
    esc = False
    quote = ""
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            continue
        if ch in "\"'":
            in_str = True
            quote = ch
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                arr_text = text[start : i + 1]
                return json.loads(arr_text.replace("'", '"'))
    return []


def extract_phrase_categories(text: str) -> list:
    m = re.search(r"var\s+phraseCategories\s*=\s*\[", text)
    if not m:
        return []
    start = m.start()
    # find matching ]; before foundationPhrases
    end_m = re.search(r"\n\];\n\n// 基础词伙", text)
    if not end_m:
        return []
    block = text[m.end() - 1 : end_m.start() + 2]
    # Convert JS object to JSON-ish
    block = re.sub(r"(\w+)\s*:", r'"\1":', block)
    block = block.replace("'", '"')
    block = re.sub(r",\s*]", "]", block)
    try:
        return json.loads(block)
    except json.JSONDecodeError:
        return parse_phrases_manual(text)


def parse_phrases_manual(text: str) -> list:
    cats = []
    for cat_m in re.finditer(
        r"id:\s*'([^']+)'.*?vocab:\s*\[(.*?)\]\s*,?\s*\}", text, re.S
    ):
        cat_id = cat_m.group(1)
        vocab = []
        for vm in re.finditer(
            r"\{\s*zh:\s*'((?:\\'|[^'])*)'\s*,\s*en:\s*'((?:\\'|[^'])*)'\s*\}",
            cat_m.group(2),
        ):
            vocab.append({"zh": vm.group(1), "en": vm.group(2)})
        cats.append({"id": cat_id, "vocab": vocab})
    return cats


def extract_all_words_from_html(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"const\s+ALL_WORDS\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        return []
    return json.loads(m.group(1))


def find_duplicates(words: list) -> list:
    c = Counter(w.lower() for w in words)
    return [(w, cnt) for w, cnt in c.items() if cnt > 1]


def find_abnormal_all_words(words: list) -> list:
    issues = []
    for w in words:
        wl = w.lower()
        if w in PROPER_NOUNS or wl in {p.lower() for p in PROPER_NOUNS}:
            issues.append((w, "专有名词/听力场景词(?)", "逻辑", "sources/tinglidanciceshi/js/modules.js"))
        if re.search(r"\d", w):
            issues.append((w, "含数字的词条", "逻辑", "sources/tinglidanciceshi/js/modules.js"))
        if len(w.split()) > 3:
            issues.append((w, "短语过长(>3词)", "逻辑", "sources/tinglidanciceshi/js/modules.js"))
        if w[0].isupper() and w not in PROPER_NOUNS and not w.isupper():
            if wl not in {"sunday", "wednesday", "september"}:
                issues.append((w, "非常规大写", "逻辑", "sources/tinglidanciceshi/js/modules.js"))
    return issues


def audit_basic_words(words: list, source: str) -> list:
    issues = []
    seen = set()
    for w in words:
        wl = w.lower().strip()
        if wl in seen:
            issues.append((w, f"重复: {wl}", "逻辑", source))
        seen.add(wl)
        for pat, wrong, fix, typ in BASIC_PATTERNS:
            if pat.search(w):
                issues.append((w, fix, typ, source))
    return issues


def audit_phrases(categories: list, source: str) -> list:
    issues = []
    seen_en = defaultdict(list)
    for cat in categories:
        cat_id = cat.get("id", "")
        for item in cat.get("vocab", []):
            zh = item.get("zh", "")
            en = item.get("en", "")
            seen_en[en.lower()].append((cat_id, zh))
            for known in PHRASE_KNOWN_ISSUES:
                if en.lower() == known[0].lower() or known[0].lower() in en.lower():
                    issues.append((f"{zh} / {en}", known[1], known[2], f"{source} [{cat_id}]"))
            if zh == known[0] if False else False:
                pass
            for pat, wrong, fix, typ in EN_PATTERNS:
                if pat.search(en):
                    issues.append((f"{zh} / {en}", fix, typ, f"{source} [{cat_id}]"))
            # Chinese issues
            if "的不变的" in zh or "增长的最大" in zh:
                issues.append((f"{zh} / {en}", "中文表述不通", "中英", f"{source} [{cat_id}]"))
            if "过渡地" in zh:
                issues.append((f"{zh} / {en}", zh.replace("过渡地", "过度地"), "中英", f"{source} [{cat_id}]"))
            if "非常的昂贵" in zh:
                issues.append((f"{zh} / {en}", "极其昂贵", "中英", f"{source} [{cat_id}]"))
            if "对保护环境重要" in zh:
                issues.append((f"{zh} / {en}", "对保护环境至关重要", "中英", f"{source} [{cat_id}]"))
            if "又流行起来" in zh and "come back" in en:
                issues.append((f"{zh} / {en}", "再度流行", "中英", f"{source} [{cat_id}]"))
            if "可以无限制" in zh:
                issues.append((f"{zh} / {en}", "可无限上网", "中英", f"{source} [{cat_id}]"))
            if "寻求在线退款" in zh:
                issues.append((f"{zh} / {en}", "在线申请退款繁琐低效", "中英", f"{source} [{cat_id}]"))
    for en, locs in seen_en.items():
        if len(locs) > 1:
            issues.append((en, f"英文重复出现在: {locs}", "逻辑", source))
    return issues


def audit_html_meanings(entries: list, html_path: str, checks: list, extra: list = None) -> list:
    issues = []
    for e in entries:
        word = e.get("word", "")
        meaning = e.get("meaning", "")
        wl = word.lower()
        for pat, bad, good, typ in checks:
            if pat.search(word):
                if bad and bad in meaning:
                    issues.append((f"{word}: {meaning}", good, typ, html_path))
                elif bad is None and good:
                    # flag if meaning seems wrong for known bad English
                    issues.append((f"{word}: {meaning}", good, typ, html_path))
        if extra:
            for word_pat, bad_m, good_m, typ in extra:
                if word_pat.search(word):
                    if bad_m and bad_m in meaning:
                        issues.append((f"{word}: {meaning}", good_m, typ, html_path))
                    elif bad_m is None and good_m and meaning != good_m:
                        # only flag obvious mismatches
                        pass
    return issues


def scan_listening_basic_meanings(entries: list) -> list:
    issues = []
    meaning_map = {
        "academic": ("学院的", "学术的；学院的"),
        "achievement": ("完成达到", "成就；成绩"),
        "alarming system": (None, "报警系统"),
        "animals behavior": (None, "动物行为"),
        "golf court": (None, "高尔夫球场"),
        "advance level": (None, "高级水平"),
        "children mind": (None, "托儿/看孩子"),
        "political man": (None, "政治家"),
        "privacy company": (None, "私人公司"),
        "plane science": (None, "行星科学"),
        "personal officer": (None, "人事专员"),
        "pet meat": (None, "宠物食品"),
        "weathers": (None, "天气"),
        "hairs": (None, "头发/毛发"),
        "finance market": (None, "金融市场"),
        "families life": (None, "家庭生活"),
        "culture awareness": (None, "文化意识"),
        "culture context": (None, "文化背景"),
        "bottle water": (None, "瓶装水"),
        "free pick": (None, "免费接送"),
        "repaired cost": (None, "维修费用"),
        "study skill": (None, "学习技巧"),
        "cooperation loan": (None, "合作贷款"),
        "triangle sharp": (None, "锐角三角形/尖角"),
        "firework": (None, "烟花(复)"),
        "attack humans": (None, "攻击人类"),
        "biological fishing": (None, "生物捕捞/生态渔业"),
        "economics history": (None, "经济史"),
        "environment damage": (None, "环境破坏"),
        "compulsory and regular": (None, "必修且常规"),
        "eye contacts": (None, "眼神交流"),
        "china stone": (None, "瓷石/China stone"),
        "banana ride": (None, "香蕉船(水上项目)"),
        "piano life": (None, "钢琴生活(?)/ piano life"),
        "greenfield": (None, "绿地/未开发土地"),
        "micro-radiogram": (None, "显微放射图(?)",),
        "waterpower": (None, "水力/水能"),
        "statement position": (None, "立场声明"),
        "objective matters": (None, "客观事项"),
        "note system": (None, "笔记系统"),
        "cheapest budget": (None, "最低预算/最经济"),
        "compulsory and regular": (None, "必修且定期"),
    }
    obvious_wrong = {
        "academic": ["学院的"],
        "achievement": ["完成达到", "完成 达到"],
        "acknowledgement": ["承认", "致谢"],  # if only 承认 without 致谢 context
        "administration officer": ["管理官员"],
        "against": ["反对"],  # might be fine
        "aging": ["老化"],  # OK
        "alter": ["改变"],  # OK
    }
    for e in entries:
        w = e.get("word", "")
        m = e.get("meaning", "")
        wl = w.lower()
        if wl in meaning_map:
            bad, good = meaning_map[wl]
            if bad and bad in m:
                issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
            elif bad is None:
                # Check if meaning is clearly wrong for the English error
                wrong_hints = {
                    "golf court": ["球场", "球场", "高尔夫球"],
                    "alarming system": ["报警", "警报"],
                    "animals behavior": ["行为", "动物"],
                    "plane science": ["飞机", "平面"],
                    "political man": ["政治", "男人", "政客"],
                    "privacy company": ["隐私"],
                    "pet meat": ["肉", "宠物肉"],
                    "weathers": ["天气"],
                    "personal officer": ["私人", "个人"],
                    "children mind": ["孩子", "心智"],
                    "finance market": ["金融", "市场"],
                    "families life": ["家庭"],
                    "culture awareness": ["文化"],
                    "bottle water": ["水", "瓶"],
                    "free pick": ["选择", "接"],
                    "repaired cost": ["修理", "成本", "费用"],
                    "study skill": ["学习", "技能"],
                    "cooperation loan": ["合作", "贷款"],
                    "triangle sharp": ["三角"],
                    "biological fishing": ["生物", "钓鱼", "捕鱼"],
                    "economics history": ["经济", "历史"],
                    "environment damage": ["环境", "破坏"],
                    "eye contacts": ["眼睛", "接触", "隐形眼镜"],
                    "banana ride": ["香蕉", "骑"],
                    "piano life": ["钢琴"],
                    "waterpower": ["水", "电", "力"],
                    "micro-radiogram": ["微", "辐射"],
                }
                if wl in wrong_hints:
                    # if meaning contains plane-related for plane science wrongly
                    if wl == "plane science" and ("飞机" in m or "平面" in m and "行星" not in m):
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "golf court" and "球场" in m and "高尔夫" not in m:
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "privacy company" and "隐私" in m:
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "political man" and ("男人" in m or "政治人" in m):
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "pet meat" and "肉" in m:
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "personal officer" and ("个人" in m or "私人" in m):
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
                    elif wl == "children mind" and "心智" in m:
                        issues.append((f"{w}: {m}", good, "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "academic" and m.strip() == "学院的":
            issues.append((f"{w}: {m}", "学术的；学院的", "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "achievement" and "完成" in m and "成就" not in m and "成绩" not in m:
            issues.append((f"{w}: {m}", "成就；成绩", "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "eye contacts" and ("隐形眼镜" in m or "接触" in m and "眼神" not in m):
            issues.append((f"{w}: {m}", "眼神交流", "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "biological fishing" and "钓鱼" in m:
            issues.append((f"{w}: {m}", "生物捕捞/生态渔业", "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "economics history" and "经济学历史" in m.replace(" ", ""):
            issues.append((f"{w}: {m}", "经济史", "中英", "sources/tinglidanciceshi/listening_basic.html"))
        if wl == "environment damage" and "损害" in m and "破坏" not in m:
            issues.append((f"{w}: {m}", "环境破坏", "中英", "sources/tinglidanciceshi/listening_basic.html"))
    return issues


def scan_listening_meanings(entries: list) -> list:
    issues = []
    for e in entries:
        w = e.get("word", "")
        m = e.get("meaning", "")
        wl = w.lower()
        # Multi-word entries split incorrectly in allWords
        if wl == "artificial" and "智能" in m and "人工" not in m:
            issues.append((f"{w}: {m}", "人工的；人造的", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "intelligence" and "人工" in m:
            issues.append((f"{w}: {m}", "智能；智力", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "living room" and m.strip() in ("生活 room", "生活房间", "起居室") and "客厅" not in m:
            if m == "生活 room" or "生活" in m and "room" in w:
                issues.append((f"{w}: {m}", "客厅", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "rafael" and "拉斐" not in m.lower() and "人名" not in m:
            issues.append((f"{w}: {m}", "拉斐尔(人名)", "逻辑", "sources/tinglidanciceshi/listening.html"))
        if wl == "patterson" and "帕特" not in m.lower() and "人名" not in m:
            issues.append((f"{w}: {m}", "帕特森(人名)", "逻辑", "sources/tinglidanciceshi/listening.html"))
        if wl == "present" and m.strip() == "现在":
            issues.append((f"{w}: {m}", "礼物；呈现", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "note" and m.strip() == "笔记" and "纸币" not in m:
            pass  # might be OK in isolation
        if wl == "coach" and m.strip() == "教练" :
            pass
        if wl == "mouse" and "老鼠" not in m and "鼠标" not in m:
            if "鼠" not in m:
                issues.append((f"{w}: {m}", "鼠标；老鼠", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "flat" and m.strip() == "平的":
            issues.append((f"{w}: {m}", "公寓；平的", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "firm" and m.strip() in ("公司",):
            pass
        if wl == "hacking" and "黑客" not in m and "砍" not in m:
            issues.append((f"{w}: {m}", "黑客行为/非法入侵", "中英", "sources/tinglidanciceshi/listening.html"))
        if wl == "lost" and m.strip() == "失去" and "found" in [x.get("word","") for x in entries]:
            pass
        if wl == "aid" and m.strip() == "援助":
            pass
        if wl == "refreshment" and w != wl:
            pass
        # Check words that were split from phrases
        if wl in ("living", "room") and w == "living":
            if m.strip() in ("生活", "起居"):
                issues.append((f"{w}: {m}", "living 应与 room 组成 living room(客厅)", "逻辑", "sources/tinglidanciceshi/listening.html"))
        if wl == "room" and m.strip() in ("房间",) :
            pass
    return issues


def compare_word_lists(modules_words, html_entries, label):
    issues = []
    html_words = [e["word"] for e in html_entries]
    mod_set = {w.lower() for w in modules_words}
    html_set = {w.lower() for w in html_words}
    only_mod = mod_set - html_set
    only_html = html_set - mod_set
    if only_mod or only_html:
        issues.append((f"{label} 词表不一致", f"modules多{len(only_mod)} html多{len(only_html)}", "逻辑", "modules.js vs html"))
    return issues


def main():
    text = MODULES_JS.read_text(encoding="utf-8")
    all_words = extract_js_array("allWords", text)
    basic_words = extract_js_array("allWordsListeningBasic", text)
    phrases = parse_phrases_manual(text)

    all_issues = defaultdict(list)

    # 1. allWords duplicates & abnormal
    dups = find_duplicates(all_words)
    for w, cnt in dups:
        all_issues["听力1000词 (allWords)"].append(
            (w, f"重复出现{cnt}次", "逻辑", "sources/tinglidanciceshi/js/modules.js")
        )
    for item in find_abnormal_all_words(all_words):
        all_issues["听力1000词 (allWords)"].append(item)

    # 2. basic words
    for item in audit_basic_words(basic_words, "sources/tinglidanciceshi/js/modules.js"):
        all_issues["听力基础词汇 (allWordsListeningBasic)"].append(item)
    basic_dups = find_duplicates(basic_words)
    for w, cnt in basic_dups:
        all_issues["听力基础词汇 (allWordsListeningBasic)"].append(
            (w, f"重复出现{cnt}次", "逻辑", "sources/tinglidanciceshi/js/modules.js")
        )

    # 3. phrase categories
    for item in audit_phrases(phrases, "sources/tinglidanciceshi/js/modules.js"):
        all_issues["写作词伙 (phraseCategories)"].append(item)

    # foundation phrases
    foundation_m = re.search(
        r"var foundationPhrases = \[(.*?)\];", text, re.S
    )
    if foundation_m:
        for vm in re.finditer(
            r'\{\s*zh:\s*"([^"]+)"\s*,\s*en:\s*"([^"]+)"\s*\}', foundation_m.group(1)
        ):
            zh, en = vm.group(1), vm.group(2)
            if "shortsighted" in en and "short-sighted" not in en:
                all_issues["基础词伙 (foundationPhrases)"].append(
                    (f"{zh} / {en}", "a very short-sighted view", "拼写", "sources/tinglidanciceshi/js/modules.js")
                )

    # 4. HTML meanings
    listening_entries = extract_all_words_from_html(LISTENING_HTML)
    basic_entries = extract_all_words_from_html(LISTENING_BASIC_HTML)

    for item in scan_listening_meanings(listening_entries):
        all_issues["listening.html 中文释义"].append(item)
    for item in scan_listening_basic_meanings(basic_entries):
        all_issues["listening_basic.html 中文释义"].append(item)

    # Dedupe issues per section
    for section in all_issues:
        seen = set()
        deduped = []
        for row in all_issues[section]:
            key = (row[0], row[1], row[2], row[3])
            if key not in seen:
                seen.add(key)
                deduped.append(row)
        all_issues[section] = deduped

    # Print report
    print("=" * 80)
    print("VOCAB AUDIT REPORT")
    print("=" * 80)
    total = 0
    for section, items in all_issues.items():
        if not items:
            continue
        print(f"\n## {section}\n")
        for wrong, fix, typ, path in items:
            print(f"{wrong} | {fix} | {typ} | {path}")
            total += 1
    print(f"\n--- TOTAL: {total} issues ---")
    print(f"\nStats: allWords={len(all_words)}, basic={len(basic_words)}, phrases_cats={len(phrases)}")
    print(f"listening.html entries={len(listening_entries)}, listening_basic.html entries={len(basic_entries)}")


if __name__ == "__main__":
    main()
