# -*- coding: utf-8 -*-
"""Deep audit: listening + reading synonym modules."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_js_const(name: str, text: str) -> str:
    m = re.search(rf"(?:const|var)\s+{name}\s*=\s*\[", text)
    if not m:
        raise ValueError(f"missing {name}")
    start = m.end() - 1
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise ValueError(f"unclosed {name}")


def parse_js_array(raw: str):
    """Parse JS array literal (allows trailing commas)."""
    cleaned = re.sub(r",(\s*[\]}])", r"\1", raw)
    return json.loads(cleaned)


def count_blanks(s: str) -> int:
    return len(re.findall(r"_{3,}", s or ""))


def audit_listening(path: Path, const: str, module: str):
    text = path.read_text(encoding="utf-8")
    raw = extract_js_const(const, text)
    data = parse_js_array(raw)
    items = data
    if isinstance(data[0], list):
        items = [q for g in data for q in g]
    issues = []
    for q in items:
        qid = q["id"]
        loc = f"{path.name}#id{qid}"
        ans = (q.get("answer") or "").strip()
        blank = q.get("blank") or ""
        opts = q.get("options") or []
        if not ans:
            issues.append((module, loc, "answer 为空", "补充答案", "空缺"))
        nb = count_blanks(blank)
        if nb == 0:
            issues.append((module, loc, "blank 无 ______", "添加填空", "逻辑"))
        if len(opts) != 4:
            issues.append((module, loc, f"选项数={len(opts)}", "应为4项", "逻辑"))
        low = [o.strip().lower() for o in opts if o]
        if len(low) != len(set(low)):
            issues.append((module, loc, f"选项重复 {opts}", "去重", "选项重复"))
        ci = q.get("correct_idx")
        if ci is not None and opts and (ci < 0 or ci >= len(opts)):
            issues.append((module, loc, f"correct_idx={ci} 越界", "修正", "逻辑"))
        if ci is not None and ans and opts and opts[ci].strip().lower() != ans.strip().lower():
            issues.append((module, loc, f"correct_idx→'{opts[ci]}' ≠ answer '{ans}'", "对齐", "逻辑"))
        # blank-answer fit: replacing blank with answer should match paraphrase roughly
        if ans and blank and "______" in blank:
            filled = blank.replace("______", ans)
            para = q.get("paraphrase") or ""
            # normalize dashes/spaces
            def norm(x):
                return re.sub(r"\s+", " ", x.replace("—", "-").replace("–", "-")).strip().lower()
            if para and norm(filled) != norm(para):
                # allow if answer is substring issue only
                if ans.lower() not in para.lower():
                    issues.append((module, loc, f"填空后 '{filled[:80]}...' 与 paraphrase 不一致", "核对 blank/answer/paraphrase", "逻辑"))
        # English typos in fields
        for field in ("original", "paraphrase"):
            t = q.get(field) or ""
            if re.search(r"\b(recieve|occured|seperate|definately|enviroment|goverment|maintainance|neccessary|wierd|teh\b|hte\b)\b", t, re.I):
                issues.append((module, f"{loc}.{field}", f"疑似拼写错：{t[:100]}", "人工核对", "拼写"))
    return issues


def audit_reading(path: Path, module: str):
    text = path.read_text(encoding="utf-8")
    groups = parse_js_array(extract_js_const("ALL_GROUPS", text))
    issues = []
    for gi, grp in enumerate(groups, 1):
        head = grp[0] if grp else "?"
        loc = f"{path.name}#G{gi}({str(head)[:25]})"
        if not grp:
            issues.append((module, loc, "空组", "删除", "空缺"))
        for wi, w in enumerate(grp):
            if not str(w).strip():
                issues.append((module, loc, f"[{wi}] 空词条", "删除", "空缺"))
        if head == "coat" and any("lay of" in str(x) for x in grp):
            issues.append((module, loc, "a lay of", "a layer of", "拼写"))
        if any("arrows and bows" in str(x) for x in grp):
            issues.append((module, loc, "arrows and bows", "bows and arrows", "用词"))
        if any(re.search(r"\b(sequent|recieve|occured|enviroment)\b", str(x), re.I) for x in grp):
            for wi, w in enumerate(grp):
                if re.search(r"\b(sequent|recieve|occured|enviroment)\b", str(w), re.I):
                    issues.append((module, f"{loc}[{wi}]", str(w), "核对拼写", "拼写"))
        # dupes
        seen = {}
        for wi, w in enumerate(grp):
            n = re.sub(r"（[^）]*）", "", str(w)).strip().lower()
            if n and n in seen:
                issues.append((module, loc, f"组内重复 '{w}'", "去重", "选项重复"))
            seen[n] = wi
    return issues


def main():
    all_issues = []
    all_issues += audit_reading(ROOT / "sources/tongyitihuan/index.html", "阅读同义替换-学习")
    all_issues += audit_reading(ROOT / "sources/tongyitihuanceshi/index.html", "阅读同义替换-测试")
    all_issues += audit_listening(ROOT / "sources/daanjutingxie/index.html", "GROUPS", "听力同义替换-学习")
    all_issues += audit_listening(ROOT / "sources/daanjutingxieceshi/index.html", "ALL_QUESTIONS", "听力同义替换-测试")
    for row in all_issues:
        print("|".join(row))
    print(f"\nCOUNT={len(all_issues)}", file=sys.stderr)


if __name__ == "__main__":
    main()
