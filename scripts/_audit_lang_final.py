#!/usr/bin/env python3
import re, json, ast
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources")
OUT = Path(r"D:/ielts-practice-platform/scripts/_audit_lang_out.txt")

lines = []

def add(mod, loc, err, sug, typ):
    lines.append(f"{mod} | {loc} | {err} | {sug} | {typ}")

# --- zh/en pairs ---
for mod, rel in [
    ("写作词伙", "xiezuocihuo/categories.js"),
    ("写作词伙测试", "xiezuocihuoceshi/index.html"),
    ("听力模块", "tinglidanciceshi/js/modules.js"),
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    pat = re.compile(r"zh:\s*['\"]([^'\"]+)['\"].*?en:\s*['\"]([^'\"]+)['\"]", re.DOTALL)
    for m in pat.finditer(text):
        zh, en = m.group(1), m.group(2)
        ln = text.count("\n", 0, m.start()) + 1
        loc = f"{Path(rel).name}:{ln}「{zh}」"

        if re.search(r"parents\s+'expectations", en):
            add(mod, loc, en, "parents' expectations", "标点/所有格")
        if "性别/年龄歧视" in zh and "age" not in en.lower():
            add(mod, loc, en, "discriminate on the basis of gender or age", "中英不匹配")
        for bad, sug, typ in [
            (r"financial-disadvantaged", "financially disadvantaged", "副词缺-ly"),
            (r"socially-disadvantaged", "socially disadvantaged", "错误连字符"),
            (r"\beight fold\b", "eightfold", "拼写/构词"),
            (r"drastic decrement", "drastic decrease", "用词错误"),
            (r"intrusion of privacy", "invasion of privacy", "搭配错误"),
            (r"golf court\b", "golf course", "用词错误"),
            (r"plane science\b", "plant science", "拼写错误"),
        ]:
            if re.search(bad, en, re.I):
                add(mod, loc, en, sug, typ)

# foundationPhrases only in modules - primary cause is phrase fragment, skip

# --- listening word lists ---
KNOWN_WORD_ISSUES = {
    "golf court": ("golf course", "用词错误"),
    "plane science": ("plant science", "拼写错误"),
}

for mod, rel in [
    ("听力2400", "tinglidanciceshi/listening.html"),
    ("听力基础", "tinglidanciceshi/listening_basic.html"),
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", text, re.DOTALL)
    words = json.loads(m.group(1))
    for w in words:
        word, meaning = w["word"], w["meaning"]
        wl = word.lower()
        if wl in KNOWN_WORD_ISSUES:
            sug, typ = KNOWN_WORD_ISSUES[wl]
            add(mod, f"{Path(rel).name} [{word}]", word, sug, typ)
        if wl == "golf" and "球场" in meaning:
            add(mod, f"{Path(rel).name} [{word}]", f"{word}→{meaning}", "高尔夫球", "中英不匹配")
        if "plant science" in wl and "飞机" in meaning:
            add(mod, f"{Path(rel).name} [{word}]", f"{word}→{meaning}", "植物科学", "中英不匹配")

# allWordsListeningBasic string list
mod_text = (ROOT / "tinglidanciceshi/js/modules.js").read_text(encoding="utf-8")
m = re.search(r"var allWordsListeningBasic = (\[.*?\]);", mod_text, re.DOTALL)
basic = ast.literal_eval(m.group(1))
for w in basic:
    wl = w.lower()
    if wl in KNOWN_WORD_ISSUES:
        sug, typ = KNOWN_WORD_ISSUES[wl]
        add("听力模块", f"modules.js allWordsListeningBasic", w, sug, typ)

# dedupe
seen = set()
out = []
for ln in lines:
    if ln not in seen:
        seen.add(ln)
        out.append(ln)

OUT.write_text("\n".join(out) + f"\n\n--- TOTAL {len(out)} ---\n", encoding="utf-8")
for mod in ["写作词伙", "写作词伙测试", "听力模块", "听力2400", "听力基础"]:
    n = sum(1 for x in out if x.startswith(mod + " |"))
    OUT.write_text(OUT.read_text(encoding="utf-8") + f"{mod}: {'已干净' if n==0 else str(n)+'条'}\n", encoding="utf-8")
