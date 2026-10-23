# -*- coding: utf-8 -*-
"""Audit spelling/translation/logic issues in content modules."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Known high-confidence English typos / wrong forms
KNOWN_EN_TYPO = {
    "a lay of": "a layer of",
    "sequent": "sequential (if synonym intended)",
    "decrement": "decrease (decrement is rare in IELTS writing)",
    "upwardly": "upward (adverb form unusual)",
    "eight fold": "eightfold",
    "be circled by forests": "be surrounded by forests",
    "be located on the shopping mall": "be located next to/near the shopping mall",
    "arrows and bows": "bows and arrows",
    "flourishment": "flourishing",
    "bottie water": "bottle water",
    "compulsory": None,  # placeholder
}

# Suspicious English patterns (OCR/keyboard)
SUSPICIOUS_EN = re.compile(
    r"(^i[a-z]{3,}|iamp|iand\b|ianes|iaptop|iaw |iegroom|ieisure|iength|infiuence|"
    r"informai|ioans|iookout|iost\b|iungs|knowiedge|piants|modei|moraiity|"
    r"ciass|ciothing|compi|compui|detaiis|famiiy|fiash|fiavor|fiute|styie|gioves|"
    r"graduai|personai|popuiar|practicai|reaiism|reguiar|reieased|abell|seif-|"
    r"shaiiow|steei|symboi|tempie|tities|transiation|iocks|bottie|butterfi|"
    r"eniarg|cabie\b|paining\b|flourishment|teh\b|hte\b|recieve|occured|seperate|"
    r"definately|accomodate|occassion|wierd|goverment|enviroment|maintainance|"
    r"neccessary|occurence|priviledge|sucessful|tommorow|untill\b|wether\b|"
    r"alot\b|aswell\b|eachother\b|everyday\b(?!\s+\w)|its'\b|your\s+self\b)",
    re.I,
)

# Obvious grammar patterns in English sentences
GRAMMAR_PATTERNS = [
    (re.compile(r"\bwhen some students studying abroad,\s*they\b", re.I),
     "when + 分词短语缺谓语，应为 when some students study abroad 或 when some students are studying abroad"),
    (re.compile(r"\bbe twice the size of it was\b", re.I),
     "应为 twice the size it was 或 twice as large as it was"),
    (re.compile(r"\bremain roughly static\b", re.I), None),  # ok
    (re.compile(r"\bdisplay a continuous growth\b", re.I), None),
    (re.compile(r"\bclimb up with fluctuations\b", re.I),
     "climb with fluctuations（up 冗余）"),
    (re.compile(r"\bbe slightly above the average\b", re.I), None),
    (re.compile(r"\bthey are enabled by .+ to talk\b", re.I),
     "they can use ... to talk / they can talk ... via ...（enabled by 搭配不自然）"),
    (re.compile(r"\bFor example, when some students\b", re.I), None),
    (re.compile(r"\ba drastic decrement\b", re.I),
     "decrement 作名词表「减少」不地道，建议 drastic drop/decrease"),
    (re.compile(r"\bdrop to its bottom\b", re.I),
     "应为 hit/reach its lowest point 或 bottom out"),
    (re.compile(r"\bbe located on the shopping mall\b", re.I),
     "on the shopping mall 介词错误，应为 next to/near/by"),
    (re.compile(r"\bbe circled by\b", re.I),
     "circled by 不自然，应为 surrounded by / encircled by"),
    (re.compile(r"\barrows and bows\b", re.I),
     "固定搭配 bows and arrows"),
    (re.compile(r"\ba lay of\b", re.I),
     "拼写错误：a layer of"),
    (re.compile(r"\beight fold\b", re.I),
     "应为 eightfold（一个词）"),
    (re.compile(r"\bbe twice the size of it was\b", re.I),
     "语法错误：of it was → it was 或 as ... as it was"),
    (re.compile(r"\bfluctuate upwardly\b", re.I),
     "upwardly 不常用，建议 fluctuate upward 或 show an upward fluctuation"),
    (re.compile(r"\bclimb steadily/solidly\b", re.I), None),  # slash ok in data
    (re.compile(r"\bcontinue to increase /soar\b", re.I),
     "斜杠前缺空格：/ soar"),
]

BLANK_RE = re.compile(r"_{3,}|____+|\[\s*\]|\(\s*\)")


def extract_js_const(name: str, text: str, bracket: str = "[") -> str:
    """Return raw JSON-ish substring for const NAME = [...] or {...}."""
    open_b, close_b = ("[", "]") if bracket == "[" else ("{", "}")
    m = re.search(rf"const\s+{name}\s*=\s*\{re.escape(open_b)}", text)
    if not m:
        m = re.search(rf"var\s+{name}\s*=\s*\{re.escape(open_b)}", text)
    if not m:
        raise ValueError(f"missing const {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == open_b:
            depth += 1
        elif c == close_b:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise ValueError(f"unclosed {name}")


def load_json_from_html(path: Path, const_name: str) -> list | dict:
    text = path.read_text(encoding="utf-8")
    raw = extract_js_const(const_name, text)
    return json.loads(raw)


def count_blanks(s: str) -> int:
    return len(re.findall(r"_{3,}|____+", s or ""))


def check_en_text(module: str, loc: str, text: str, issues: list) -> None:
    if not text or not str(text).strip():
        issues.append((module, loc, "英文内容为空", "补充英文", "空缺"))
        return
    t = str(text)
    for pat, msg in GRAMMAR_PATTERNS:
        if pat.search(t) and msg:
            issues.append((module, loc, f"英文：{t[:120]}", msg, "语法"))
    for word, fix in KNOWN_EN_TYPO.items():
        if fix and word.lower() in t.lower():
            issues.append((module, loc, f"含 '{word}'", fix, "拼写/用词"))
    if SUSPICIOUS_EN.search(t):
        issues.append((module, loc, f"可疑拼写：{t[:100]}", "人工核对 OCR/键盘误触", "拼写"))


def audit_listening_questions(module: str, path: Path, const_name: str, issues: list) -> None:
    data = load_json_from_html(path, const_name)
    items = data
    if isinstance(data, list) and data and isinstance(data[0], list):
        items = [q for g in data for q in g]
    for q in items:
        qid = q.get("id", "?")
        loc = f"{path.name}#id{qid}"
        ans = (q.get("answer") or "").strip()
        blank = q.get("blank") or ""
        opts = q.get("options") or []
        if not ans:
            issues.append((module, loc, "answer 为空", "补充答案", "空缺"))
        nb = count_blanks(blank)
        if nb == 0 and "______" not in blank:
            issues.append((module, loc, "blank 无填空位", "添加 ______", "逻辑"))
        elif nb > 1:
            issues.append((module, loc, f"blank 有 {nb} 个空，answer 仅 '{ans}'", "多空需拆分或合并", "blank不匹配"))
        if ans and blank and nb == 1:
            # answer should fit in blank context
            if ans not in (q.get("paraphrase") or "") and ans not in blank.replace("______", ans):
                pass  # paraphrase may differ slightly
        if len(opts) != 4:
            issues.append((module, loc, f"选项数={len(opts)}（期望4）", "补齐或调整选项", "逻辑"))
        if len(set(o.strip().lower() for o in opts if o)) != len([o for o in opts if o]):
            issues.append((module, loc, f"选项重复：{opts}", "去重", "选项重复"))
        ci = q.get("correct_idx")
        if ci is not None and opts:
            if ci < 0 or ci >= len(opts):
                issues.append((module, loc, f"correct_idx={ci} 越界", "修正索引", "逻辑"))
            elif ans and opts[ci].strip().lower() != ans.strip().lower():
                issues.append((module, loc, f"correct_idx 指向 '{opts[ci]}' 与 answer '{ans}' 不一致", "对齐 answer/correct_idx", "逻辑"))
        elif ans and opts and ans not in opts:
            issues.append((module, loc, f"answer '{ans}' 不在 options 中", "加入选项或改 answer", "逻辑"))
        for field in ("original", "paraphrase", "blank", "answer"):
            check_en_text(module, f"{loc}.{field}", q.get(field, ""), issues)


def audit_reading_synonym_groups(module: str, path: Path, issues: list) -> None:
    groups = load_json_from_html(path, "ALL_GROUPS")
    for gi, grp in enumerate(groups, 1):
        if not grp:
            issues.append((module, f"{path.name}#group{gi}", "词组为空", "删除或补充", "空缺"))
            continue
        head = grp[0]
        loc = f"{path.name}#group{gi}({head[:30]})"
        for wi, word in enumerate(grp):
            wloc = f"{loc}[{wi}]"
            if not str(word).strip():
                issues.append((module, wloc, "词条为空", "删除空项", "空缺"))
            check_en_text(module, wloc, str(word), issues)
        # duplicate within group (case-insensitive, strip annotations)
        def norm(w):
            w = re.sub(r"（[^）]*）", "", str(w)).strip().lower()
            return w
        seen = {}
        for wi, word in enumerate(grp):
            n = norm(word)
            if not n:
                continue
            if n in seen:
                issues.append((module, loc, f"组内重复：'{word}' 与 '{grp[seen[n]]}'", "去重", "选项重复"))
            else:
                seen[n] = wi
        # known issues in reading synonym
        if head == "coat" and "a lay of" in grp:
            issues.append((module, loc, "a lay of", "a layer of", "拼写"))
        if "arrows and bows" in str(grp):
            issues.append((module, loc, "arrows and bows", "bows and arrows", "用词"))


def audit_translation_json(module: str, path: Path, issues: list) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data:
        qid = item.get("id", "?")
        loc = f"{path.name}#id{qid}"
        zh = (item.get("fullChinese") or "").strip()
        en = (item.get("finalEnglish") or "").strip()
        if not zh:
            issues.append((module, loc, "fullChinese 为空", "补充中文", "空缺"))
        if not en:
            issues.append((module, loc, "fullChinese 为空", "补充英文", "空缺"))
        check_en_text(module, f"{loc}.finalEnglish", en, issues)
        for si, step in enumerate(item.get("steps") or [], 1):
            sloc = f"{loc}.step{si}"
            ca = (step.get("correctAnswer") or "").strip()
            if not ca:
                issues.append((module, sloc, "correctAnswer 为空", "补充", "空缺"))
            check_en_text(module, sloc, ca, issues)
            sch = (step.get("chinese") or "").strip()
            if not sch:
                issues.append((module, sloc, "chinese 为空", "补充", "空缺"))


def audit_xiezuocihuo(module: str, path: Path, issues: list) -> None:
    text = path.read_text(encoding="utf-8")
    # parse vocab entries { zh: '...', en: '...' }
    for m in re.finditer(r"\{\s*zh:\s*'([^']*)',\s*en:\s*'([^']*)'\s*\}", text):
        zh, en = m.group(1), m.group(2)
        # find line number approx
        line = text[: m.start()].count("\n") + 1
        loc = f"{path.name}:L{line}"
        if not zh.strip():
            issues.append((module, loc, "中文为空", "补充", "空缺"))
        if not en.strip():
            issues.append((module, loc, "英文为空", "补充", "空缺"))
        check_en_text(module, loc, en, issues)
        # specific high-confidence pairs
        if "drastic decrement" in en.lower():
            issues.append((module, loc, f"en='{en}'", "decrement→decrease/drop", "用词"))
        if "twice the size of it was" in en.lower():
            issues.append((module, loc, f"en='{en}'", "语法：twice the size it was in 2015", "语法"))
        if "be located on the shopping mall" in en.lower():
            issues.append((module, loc, f"en='{en}'", "介词：next to/near the shopping mall", "语法"))
        if "be circled by" in en.lower():
            issues.append((module, loc, f"en='{en}'", "surrounded by forests", "用词"))
        if "eight fold" in en.lower():
            issues.append((module, loc, f"en='{en}'", "eightfold", "拼写"))
        if "upwardly" in en.lower():
            issues.append((module, loc, f"en='{en}'", "fluctuate upward", "用词"))
        if "保持大致的不变的" in zh:
            issues.append((module, loc, f"zh='{zh}'", "保持大致不变（删「的」）", "中文"))


def audit_changnanju(module: str, path: Path, issues: list) -> None:
    sentences = load_json_from_html(path, "SENTENCES")
    for s in sentences:
        num = s.get("num", "?")
        loc = f"{path.name}#句{num}"
        orig = s.get("original") or ""
        if not orig.strip():
            issues.append((module, loc, "original 为空", "补充", "空缺"))
        check_en_text(module, f"{loc}.original", orig, issues)
        for key in ("challenge1", "challenge2"):
            ch = s.get(key)
            if not ch:
                continue
            for bi, box in enumerate(ch.get("boxes") or [], 1):
                bloc = f"{loc}.{key}.box{bi}"
                ans = (box.get("answer") or "").strip()
                if not ans:
                    issues.append((module, bloc, "answer 为空", "补充", "空缺"))
                check_en_text(module, bloc, ans, issues)


def dedupe_issues(issues: list) -> list:
    seen = set()
    out = []
    for row in issues:
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out


def main() -> None:
    issues: list[tuple] = []

    modules = [
        ("阅读同义替换-学习", ROOT / "sources/tongyitihuan/index.html", "reading"),
        ("阅读同义替换-测试", ROOT / "sources/tongyitihuanceshi/index.html", "reading"),
        ("听力同义替换-学习", ROOT / "sources/daanjutingxie/index.html", "listening_learn"),
        ("听力同义替换-测试", ROOT / "sources/daanjutingxieceshi/index.html", "listening_test"),
        ("写作句子翻译-学习", ROOT / "sources/juzifanyixin/translation_data.json", "translation"),
        ("写作句子翻译-测试", ROOT / "sources/juzifanyixin/translation_data.json", "translation"),
        ("写作词伙", ROOT / "sources/xiezuocihuo/categories.js", "phrase"),
        ("长难句", ROOT / "sources/changnanju/index.html", "sentence"),
    ]

    for name, path, kind in modules:
        if not path.exists():
            print(f"SKIP missing: {path}", file=sys.stderr)
            continue
        try:
            if kind == "reading":
                audit_reading_synonym_groups(name, path, issues)
            elif kind in ("listening_learn",):
                audit_listening_questions(name, path, "GROUPS", issues)
            elif kind == "listening_test":
                audit_listening_questions(name, path, "ALL_QUESTIONS", issues)
            elif kind == "translation":
                audit_translation_json(name, path, issues)
            elif kind == "phrase":
                audit_xiezuocihuo(name, path, issues)
            elif kind == "sentence":
                audit_changnanju(name, path, issues)
        except Exception as e:
            issues.append((name, str(path), f"解析失败: {e}", "修复数据格式", "逻辑"))

    issues = dedupe_issues(issues)
    # filter: only high confidence - remove generic suspicious unless pattern is strong
    high = []
    for row in issues:
        module, loc, err, sug, typ = row
        if typ == "拼写" and "可疑拼写" in err and "人工核对" in sug:
            continue  # skip low-confidence spellcheck
        high.append(row)

    print(f"TOTAL_ISSUES={len(high)}\n")
    for module, loc, err, sug, typ in high:
        print(f"{module} | {loc} | {err} | {sug} | {typ}")


if __name__ == "__main__":
    main()
