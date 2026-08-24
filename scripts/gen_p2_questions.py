# -*- coding: utf-8 -*-
"""One-shot generator: rebuild p2-data.js questions from P2答题思路（新）."""
from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"G:\口语练习\_review\P2答题思路（新）.txt")
OUT = ROOT / "sources" / "kouyulianxi" / "p2-data.js"
OLD = OUT


# PDF OCR/export often uses CJK Radicals Supplement glyphs that NFKC won't fix.
RADICAL_MAP = str.maketrans(
    {
        "\u2ec5": "见",  # ⻅
        "\u2ec6": "角",  # ⻆
        "\u2ecb": "车",  # ⻋
        "\u2ed3": "长",  # ⻓
        "\u2ed4": "门",  # ⻔
        "\u2edb": "风",  # ⻛
        "\u2ee2": "马",  # ⻢
        "\u2f2f": "工",  # ⼯
        "\u2f08": "人",
        "\u2f22": "大",
        "\u2f3c": "手",  # ⼿
        "\u2f63": "心",
        "\u2f8f": "言",
    }
)


def nf(s: str) -> str:
    return unicodedata.normalize("NFKC", s).translate(RADICAL_MAP)


END = {
    "yumeng": "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议",
    "sun": "用素材第三步感受收尾：她极其受欢迎，人们着迷于她可爱的酒窝和贴纸",
    "movie": "用素材第三步感受收尾：领悟到爱才是生命中最宝贵的东西",
    "badminton": "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力",
    "bear": "用素材第三步感受收尾：它真的就像一个老朋友一样",
    "basketball": "用素材第三步感受收尾：它真的就像一个老朋友一样",
    "tianchi": "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了",
    "robot": "用素材第三步感受收尾：它帮我节省大量时间，打扫不再是问题",
}

# Hand-tuned basketball hints when naive rewrite sounds wrong
BEAR_QIDS = {13, 14, 24, 30, 35, 40, 43, 47, 50, 53, 54}
BB_HINT_OVERRIDE = {
    35: "那是高考前夜,突然停电让我极度焦躁睡不着。我只能下楼投篮减压,这才感到平静入睡。",
    40: "小学时父亲送的篮球,陪我度过了高考等无数个压力山大的夜晚,就像老朋友。",
    43: "不小心弄坏了朋友送的那只心爱的篮球,心里特别愧疚。",
    47: "童年时最喜欢父亲送的篮球,一有空就抱着它投篮。",
    50: "店员极其耐心地帮我为好朋友挑选一个手感很好的篮球。",
    53: "生活中离不开那只陪伴多年的篮球,高压时投几下就能平静下来。",
    54: "回家后最爱窝在沙发上,旁边放着那只像老朋友一样的篮球。",
}


def map_mat(tag: str) -> str | None:
    t = tag.replace(" ", "")
    if "孙颖莎" in t or ("明星" in t and "雨萌" not in t):
        return "sun"
    if "雨萌" in t:
        return "yumeng"
    if "羽毛球" in t:
        return "badminton"
    if "天池" in t or "长白山" in t:
        return "tianchi"
    if "夏洛特" in t or "影音" in t or "沈腾" in t:
        return "movie"
    if "小熊" in t or "玩偶" in t:
        return "bear"
    return None


def fix_en(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip().rstrip(".")
    if s and not s.endswith("."):
        s += "."
    reps = [
        (" Id ", " I'd "),
        (" Im ", " I'm "),
        (" dont ", " don't "),
        (" Dont ", " Don't "),
        ("familys", "family's"),
        ("homies", "homie's"),
        ("Ive ", "I've "),
        ("didnt", "didn't"),
        ("cant ", "can't "),
        ("wont ", "won't "),
    ]
    for a, b in reps:
        s = s.replace(a, b)
    return s


def bear_to_basketball_hint(hint: str) -> str:
    """Best-effort rewrite of bear hint into basketball wording."""
    s = hint
    reps = [
        ("小学时得到的Jellycat棕色泰迪熊", "小学时父亲送的篮球"),
        ("小学时得到的Jellycat泰迪熊", "小学时父亲送的篮球"),
        ("Jellycat棕色泰迪熊", "父亲送的篮球"),
        ("Jellycat泰迪熊", "父亲送的篮球"),
        ("Jellycat小熊玩偶", "手感很好的篮球"),
        ("Jellycat的棕色小熊", "手感更好的专业篮球"),
        ("Jellycat棕色小熊", "手感更好的专业篮球"),
        ("Jellycat小熊", "篮球"),
        ("Jellycat", ""),
        ("棕色毛绒小熊", "篮球"),
        ("棕色泰迪熊", "篮球"),
        ("泰迪熊", "篮球"),
        ("小熊玩偶", "篮球"),
        ("毛绒玩具", "篮球"),
        ("毛绒小熊", "篮球"),
        ("柔软可爱的东西", "手感好的运动用品"),
        ("柔软的", ""),
        ("玩具店", "体育用品店"),
        ("各种毛绒玩具", "各类球类与运动用品"),
        ("抱着朋友送我的那只", "拿着朋友送我的那个"),
        ("抱着", "拿着"),
        ("一只", "一个"),
        ("那只", "那个"),
        ("小熊", "篮球"),
        ("玩偶", "篮球"),
    ]
    for a, b in reps:
        s = s.replace(a, b)
    s = re.sub(r"\s+", "", s)
    s = s.replace("的篮球棕色篮球", "的篮球").replace("棕色篮球", "篮球")
    return s


def load_old_specials(path: Path) -> dict[int, dict]:
    """Pull openingById / curated basketball hints from previous p2-data.js."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"\n    \{\n      id: ", text)
    out: dict[int, dict] = {}
    for p in parts[1:]:
        m = re.match(r"(\d+),", p)
        if not m:
            continue
        qid = int(m.group(1))
        item: dict = {}
        om = re.search(r"openingById: \{([\s\S]*?)\n      \},", p)
        if om:
            # Parse bear/basketball en/zh blocks
            opening: dict = {}
            for mid in ("bear", "basketball"):
                bm = re.search(
                    rf"{mid}: \{{\s*en: \"((?:\\.|[^\"\\])*)\",\s*zh: \"((?:\\.|[^\"\\])*)\"\s*\}}",
                    om.group(1),
                )
                if bm:
                    opening[mid] = {"en": bm.group(1), "zh": bm.group(2)}
            if opening:
                item["openingById"] = opening
        hm = re.search(r"materialHintById: \{([\s\S]*?)\n      \},", p)
        if hm and "basketball" in hm.group(1):
            hints = {}
            for mid in ("bear", "basketball"):
                mm = re.search(rf'{mid}: "((?:\\.|[^"\\])*)"', hm.group(1))
                if mm:
                    hints[mid] = mm.group(1)
            if hints:
                item["materialHintById"] = hints
        if item:
            out[qid] = item
    return out


def parse_questions(text: str, old_specials: dict[int, dict] | None = None) -> list[dict]:
    old_specials = old_specials or {}
    text = nf(text)
    text = re.sub(r"===== PAGE.*?=====\n?", "\n", text)
    pattern = re.compile(r"(?m)^(\d{1,2})\.\s+(.+?)\s*\(([^)]+)\)\s*$")
    matches = list(pattern.finditer(text))
    byid: dict[int, dict] = {}
    for i, m in enumerate(matches):
        qid = int(m.group(1))
        if qid < 1 or qid > 54:
            continue
        # Full heading may be: 中文 (English) (注：...)
        heading = m.group(0)
        heading = re.sub(r"\s*\(注[:：][^)]*\)\s*$", "", heading)
        hm = re.match(r"^(\d{1,2})\.\s+(.+?)\s*\(([^)]+)\)\s*$", heading)
        if not hm:
            title = re.sub(r"\s*\(注[:：].*$", "", m.group(2)).strip()
            title = re.sub(r"\s*\([A-Za-z][^)]*\)\s*$", "", title).strip()
            qen = re.sub(r"\s*\(注[:：].*$", "", m.group(3)).strip()
        else:
            title = hm.group(2).strip()
            qen = hm.group(3).strip()
        title = re.sub(r"\s*\([A-Za-z][^)]*\)\s*$", "", title).strip()
        if qen.startswith("注") or "老题列表" in qen:
            # Fallback: recover English from original group if note ate the cue
            qen = "Natural place" if qid == 51 else re.sub(r"\s*\(注[:：].*$", "", m.group(3)).strip()
        qen = re.sub(r"\s+", " ", qen).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        om = re.search(
            r"自然过渡[：:]\s*(.+?)\s*\((.+?)\)\s*[。.]?\s*(?:\n|$)",
            block,
            re.S,
        )
        if om:
            opening_en = fix_en(om.group(1))
            opening_zh = re.sub(r"\s+", "", om.group(2)).strip()
        else:
            opening_en, opening_zh = "", ""

        mm = re.search(
            r"套用素材[：:]\s*(.+?)(?=\n\d+\.|\n[一二三]、|\Z)",
            block,
            re.S,
        )
        raw = mm.group(1).strip() if mm else ""
        tags = re.findall(r"【([^】]+)】", raw)
        hint = raw
        for t in tags:
            hint = hint.replace(f"【{t}】", "")
        hint = re.sub(r"^\s*[+＋]\s*", "", hint)
        hint = re.sub(r"\s+", "", hint).strip()

        ids: list[str] = []
        for t in tags:
            mid = map_mat(t)
            if mid and mid not in ids:
                ids.append(mid)
        mid = ids[0] if ids else "yumeng"

        item: dict = {
            "id": qid,
            "title": title,
            "q": qen,
            "openingEn": opening_en,
            "openingZh": opening_zh,
            "materialId": mid,
            "materialHint": hint,
            "endingTip": END.get(mid, "用素材第三步感受收尾"),
        }
        if len(ids) > 1:
            item["materialIds"] = ids
            item["materialHintById"] = {x: hint for x in ids}
        if mid == "bear" and qid in BEAR_QIDS:
            item["materialOptions"] = ["bear", "basketball"]
            special = old_specials.get(qid, {})
            if "materialHintById" in special:
                item["materialHintById"] = special["materialHintById"]
                item["materialHint"] = special["materialHintById"].get("bear", hint)
            else:
                bb = BB_HINT_OVERRIDE.get(qid) or bear_to_basketball_hint(hint)
                item["materialHintById"] = {
                    "bear": hint,
                    "basketball": bb,
                }
            if "openingById" in special:
                item["openingById"] = special["openingById"]
        byid[qid] = item

    missing = [i for i in range(1, 55) if i not in byid]
    if missing:
        raise SystemExit(f"missing question ids: {missing}")
    return [byid[i] for i in range(1, 55)]


def js_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def emit_q(q: dict) -> str:
    lines = ["    {"]
    lines.append(f"      id: {q['id']},")
    lines.append(f"      title: {js_str(q['title'])},")
    lines.append(f"      q: {js_str(q['q'])},")
    lines.append(f"      openingEn: {js_str(q['openingEn'])},")
    lines.append(f"      openingZh: {js_str(q['openingZh'])},")
    lines.append(f"      materialId: {js_str(q['materialId'])},")
    if "materialOptions" in q:
        lines.append(f"      materialOptions: {json.dumps(q['materialOptions'])},")
    if "materialIds" in q:
        lines.append(f"      materialIds: {json.dumps(q['materialIds'])},")
    lines.append(f"      materialHint: {js_str(q['materialHint'])},")
    if "materialHintById" in q:
        lines.append("      materialHintById: {")
        parts = [
            f"        {js_str(k)}: {js_str(v)}"
            for k, v in q["materialHintById"].items()
        ]
        lines.append(",\n".join(parts))
        lines.append("      },")
    if "openingById" in q:
        lines.append("      openingById: {")
        ob_parts = []
        for mid, ov in q["openingById"].items():
            ob_parts.append(
                "        "
                + mid
                + ": {\n"
                + f"          en: {js_str(ov['en'])},\n"
                + f"          zh: {js_str(ov['zh'])}\n"
                + "        }"
            )
        lines.append(",\n".join(ob_parts))
        lines.append("      },")
    lines.append(f"      endingTip: {js_str(q['endingTip'])}")
    lines.append("    }")
    return "\n".join(lines)


def main() -> None:
    # Prefer committed version for curated openingById / basketball hints
    old_src = ROOT / "_p2_old_utf8.js"
    if not old_src.exists():
        try:
            raw = subprocess.check_output(
                ["git", "show", "HEAD:sources/kouyulianxi/p2-data.js"],
                cwd=str(ROOT),
            )
            old_src.write_bytes(raw)
        except Exception:
            old_src = OLD
    specials = load_old_specials(old_src)
    questions = parse_questions(SRC.read_text(encoding="utf-8"), specials)
    old = OLD.read_text(encoding="utf-8")
    # If current file already regenerated, materials still live at top
    idx = old.find("materials:")
    qidx = old.find("questions:")
    if idx < 0 or qidx < 0:
        raise SystemExit("cannot locate materials/questions in existing p2-data.js")
    materials_src = old[idx:qidx].rstrip().rstrip(",")
    if not materials_src.endswith(","):
        materials_src += ","

    q_js = ",\n".join(emit_q(q) for q in questions)
    out = (
        "// P2 data - 6 大素材 + 54 道答题思路（按《P2答题思路（新）》补全）\n"
        "const P2_DATA = {\n"
        f"  {materials_src}\n"
        "  questions: [\n"
        f"{q_js}\n"
        "  ]\n"
        "};\n"
    )
    OUT.write_text(out, encoding="utf-8")
    r = subprocess.run(
        ["node", "--check", str(OUT)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(f"wrote {OUT} questions={len(questions)} bytes={OUT.stat().st_size}")
    if r.returncode != 0:
        raise SystemExit(r.stderr or "node --check failed")
    print("node --check OK")
    report = ROOT / "_p2_gen_summary.txt"
    report.write_text(
        "\n".join(
            [
                f"questions={len(questions)}",
                f"specials_loaded={sorted(specials)}",
                f"q13_openingById={bool(questions[12].get('openingById'))}",
                f"q16_mats={questions[15].get('materialIds')}",
                f"q34={questions[33]['title']}|{questions[33]['materialId']}",
                f"q40_bb={questions[39].get('materialHintById',{}).get('basketball','')[:40]}",
                f"q51={questions[50]['title']}|{questions[50]['materialId']}",
                f"q54={questions[53]['title']}|{questions[53]['materialId']}",
            ]
        ),
        encoding="utf-8",
    )
    print(f"summary -> {report}")


if __name__ == "__main__":
    main()
