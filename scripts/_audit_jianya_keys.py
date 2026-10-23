# -*- coding: utf-8 -*-
"""Audit jianya exam-data papers vs answer keys for structural mismatches."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
OUT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_audit.md")

TFNG = {"true", "false", "not given", "yes", "no", "t", "f", "ng", "y", "n"}
CHOICE_LETTERS = re.compile(r"^[A-Ha-h](?:\s*[/|,]\s*[A-Ha-h])*$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def option_values(q: dict) -> set[str]:
    vals = set()
    for opt in q.get("options") or []:
        if isinstance(opt, dict):
            v = str(opt.get("value") or "").strip()
            lab = str(opt.get("label") or "").strip()
            if v:
                vals.add(v.upper())
            # sometimes label starts with A/B/C
            m = re.match(r"^([A-Ha-h])\b", lab)
            if m:
                vals.add(m.group(1).upper())
        else:
            s = str(opt).strip()
            if s:
                vals.add(s.upper())
    return vals


def split_alts(ans: str) -> list[str]:
    return [x.strip() for x in re.split(r"\s*[/|]\s*", ans) if x.strip()]


def audit_part(book: str, subject: str, paper_path: Path, key_path: Path | None) -> list[dict]:
    issues: list[dict] = []
    paper = load(paper_path)
    s_id = paper.get("sId")
    label = paper.get("sName") or f"{book} {subject} {paper_path.stem}"
    qs = paper.get("questions") or []
    q_nums = [q.get("number") for q in qs]
    q_by_num = {q.get("number"): q for q in qs}

    if key_path is None or not key_path.is_file():
        issues.append(
            {
                "sev": "high",
                "kind": "missing_key_file",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"无 keys/{subject}/{paper_path.name}",
            }
        )
        return issues

    key = load(key_path)
    answers = key.get("answers") or {}
    if not isinstance(answers, dict):
        issues.append(
            {
                "sev": "high",
                "kind": "bad_key_format",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": "answers 不是对象",
            }
        )
        return issues

    if key.get("sId") not in (None, s_id, str(s_id)):
        issues.append(
            {
                "sev": "high",
                "kind": "sid_mismatch",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"key.sId={key.get('sId')} != paper.sId={s_id}",
            }
        )

    # number sets
    try:
        paper_set = {int(n) for n in q_nums if n is not None}
    except Exception:
        paper_set = set()
        issues.append(
            {
                "sev": "high",
                "kind": "bad_question_numbers",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"题目题号异常: {q_nums[:20]}",
            }
        )

    key_set = set()
    for k in answers:
        try:
            key_set.add(int(k))
        except Exception:
            issues.append(
                {
                    "sev": "high",
                    "kind": "bad_key_number",
                    "book": book,
                    "subject": subject,
                    "sId": s_id,
                    "label": label,
                    "detail": f"答案键非数字题号: {k!r}",
                }
            )

    missing = sorted(paper_set - key_set)
    extra = sorted(key_set - paper_set)
    if missing:
        issues.append(
            {
                "sev": "high",
                "kind": "key_missing_numbers",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"题目有、答案缺: {missing}",
            }
        )
    if extra:
        issues.append(
            {
                "sev": "high",
                "kind": "key_extra_numbers",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"答案有、题目无: {extra}",
            }
        )

    # duplicate question numbers
    cnt = Counter(q_nums)
    dups = sorted([n for n, c in cnt.items() if c > 1])
    if dups:
        issues.append(
            {
                "sev": "high",
                "kind": "duplicate_question_numbers",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"重复题号: {dups}",
            }
        )

    # empty / suspicious answers
    empty = []
    placeholder = []
    for kn, av in answers.items():
        s = str(av or "").strip()
        if not s:
            empty.append(kn)
        elif s.lower() in {"todo", "tbd", "null", "none", "?", "-", "xxx", "n/a"}:
            placeholder.append(f"{kn}={s}")
    if empty:
        issues.append(
            {
                "sev": "high",
                "kind": "empty_answer",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"空答案题号: {empty}",
            }
        )
    if placeholder:
        issues.append(
            {
                "sev": "high",
                "kind": "placeholder_answer",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"占位答案: {placeholder}",
            }
        )

    # choice answer vs options
    for num in sorted(paper_set & key_set):
        q = q_by_num.get(num) or {}
        ans = str(answers.get(str(num)) or answers.get(num) or "").strip()
        qtype = str(q.get("type") or "")
        opts = option_values(q)
        alts = split_alts(ans)
        if qtype == "single_choice" and opts:
            ok = False
            for a in alts:
                au = a.upper()
                if au in opts:
                    ok = True
                    break
                # allow full label match loosely
                if any(au == o or au in o or o in au for o in opts):
                    ok = True
                    break
            if not ok and CHOICE_LETTERS.match(ans.replace(" ", "")):
                issues.append(
                    {
                        "sev": "high",
                        "kind": "choice_answer_not_in_options",
                        "book": book,
                        "subject": subject,
                        "sId": s_id,
                        "label": label,
                        "detail": f"Q{num} 答案={ans!r} 不在选项 {sorted(opts)}",
                    }
                )
            elif not ok and len(ans) <= 3:
                issues.append(
                    {
                        "sev": "med",
                        "kind": "choice_answer_suspicious",
                        "book": book,
                        "subject": subject,
                        "sId": s_id,
                        "label": label,
                        "detail": f"Q{num} 选择题答案={ans!r} 与选项 {sorted(opts)} 难对齐",
                    }
                )

        # TF/NG style answers on non-TF questions with letter options only
        if opts and set(x.upper() for x in opts) <= set("ABCDEFGH") and alts:
            if all(a.lower() in TFNG for a in alts):
                issues.append(
                    {
                        "sev": "high",
                        "kind": "tfng_answer_on_letter_choice",
                        "book": book,
                        "subject": subject,
                        "sId": s_id,
                        "label": label,
                        "detail": f"Q{num} 选项是字母 {sorted(opts)}，答案却是 TF/NG: {ans!r}",
                    }
                )

        # letter answers on gap_fill with no options
        if qtype == "gap_fill" and not opts and CHOICE_LETTERS.match(ans.replace(" ", "")) and len(ans) <= 5:
            # could be matching heading A-H; often valid. mark low.
            issues.append(
                {
                    "sev": "low",
                    "kind": "letter_answer_on_gap",
                    "book": book,
                    "subject": subject,
                    "sId": s_id,
                    "label": label,
                    "detail": f"Q{num} gap_fill 答案为字母 {ans!r}（可能是配对/标题题，需人工核）",
                }
            )

    # count mismatch even if sets somehow weird
    if len(qs) != len(answers) and not missing and not extra:
        issues.append(
            {
                "sev": "med",
                "kind": "count_mismatch_same_set",
                "book": book,
                "subject": subject,
                "sId": s_id,
                "label": label,
                "detail": f"题目数={len(qs)} 答案数={len(answers)}（集合相同但有重复？）",
            }
        )

    # part range sanity: reading P1 usually 1-13, P2 14-26, P3 27-40
    # listening P1 1-10 etc. If numbers jump wrongly, flag.
    if paper_set:
        mn, mx = min(paper_set), max(paper_set)
        part = paper.get("sPart")
        if subject == "reading" and part in (1, 2, 3):
            expected = {1: (1, 13), 2: (14, 26), 3: (27, 40)}.get(part)
            if expected and (mn < expected[0] - 2 or mx > expected[1] + 2 or mn > expected[0] + 5):
                issues.append(
                    {
                        "sev": "med",
                        "kind": "reading_part_range_odd",
                        "book": book,
                        "subject": subject,
                        "sId": s_id,
                        "label": label,
                        "detail": f"sPart={part} 题号范围 {mn}-{mx}，常见应为 {expected[0]}-{expected[1]}",
                    }
                )
        if subject == "listening" and part in (1, 2, 3, 4):
            expected = {1: (1, 10), 2: (11, 20), 3: (21, 30), 4: (31, 40)}.get(part)
            if expected and (mn < expected[0] - 2 or mx > expected[1] + 2):
                issues.append(
                    {
                        "sev": "med",
                        "kind": "listening_part_range_odd",
                        "book": book,
                        "subject": subject,
                        "sId": s_id,
                        "label": label,
                        "detail": f"sPart={part} 题号范围 {mn}-{mx}，常见应为 {expected[0]}-{expected[1]}",
                    }
                )

    return issues


def main():
    all_issues: list[dict] = []
    stats = defaultdict(int)
    books = sorted(ROOT.glob("academic*"), key=lambda p: int(re.search(r"\d+", p.name).group()))
    for book_dir in books:
        book = book_dir.name
        for subject in ("reading", "listening"):
            paper_dir = book_dir / subject
            key_dir = book_dir / "keys" / subject
            if not paper_dir.is_dir():
                continue
            papers = sorted(paper_dir.glob("*.json"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem)
            stats["parts"] += len(papers)
            for paper_path in papers:
                key_path = key_dir / paper_path.name
                issues = audit_part(book, subject, paper_path, key_path if key_path.exists() else None)
                all_issues.extend(issues)
                for it in issues:
                    stats[it["kind"]] += 1
                    stats[f"sev_{it['sev']}"] += 1

    # answer value frequency anomalies: same answer repeated too much in a part
    # already covered structurally; add cross-book empty scan done.

    OUT.parent.mkdir(parents=True, exist_ok=True)
    high = [i for i in all_issues if i["sev"] == "high"]
    med = [i for i in all_issues if i["sev"] == "med"]
    low = [i for i in all_issues if i["sev"] == "low"]

    lines = []
    lines.append("# 剑雅真题 / 模考 题目-答案键 筛查报告")
    lines.append("")
    lines.append(f"- 检查目录: `{ROOT}`")
    lines.append(f"- Part 总数: {stats['parts']}")
    lines.append(f"- 问题总数: {len(all_issues)}（高 {len(high)} / 中 {len(med)} / 低 {len(low)}）")
    lines.append("")
    lines.append("## 按类型统计")
    lines.append("")
    for k, v in sorted(((k, v) for k, v in stats.items() if not k.startswith("sev_") and k != "parts"), key=lambda x: -x[1]):
        lines.append(f"- `{k}`: {v}")
    lines.append("")

    def render(title: str, rows: list[dict]):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("（无）")
            lines.append("")
            return
        # group by book/subject/sId
        by = defaultdict(list)
        for r in rows:
            by[(r["book"], r["subject"], r["sId"], r["label"])].append(r)
        for (book, subject, s_id, label), items in sorted(by.items()):
            lines.append(f"### {book} / {subject} / sId={s_id}")
            lines.append(f"- 标签: {label}")
            for it in items:
                lines.append(f"- **{it['kind']}**: {it['detail']}")
            lines.append("")

    render("高优先级（会直接导致判分错 / 对不上）", high)
    render("中优先级（范围异常 / 可疑）", med)
    render("低优先级（需人工确认）", low[:80])
    if len(low) > 80:
        lines.append(f"（低优先级其余 {len(low)-80} 条已省略，完整见脚本重跑）")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"parts={stats['parts']} issues={len(all_issues)} high={len(high)} med={len(med)} low={len(low)}")
    # print top high kinds
    c = Counter(i["kind"] for i in high)
    for k, v in c.most_common(15):
        print(f"  HIGH {k}: {v}")


if __name__ == "__main__":
    main()
