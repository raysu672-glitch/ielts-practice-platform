# -*- coding: utf-8 -*-
"""Deeper content/heuristic checks for jianya keys vs papers."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
OUT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_deep.md")

DATA_ANSWER_RE = re.compile(r'data-answer=["\']([^"\']+)["\']', re.I)
# common tongzhuo / scraped answer markers
ANS_ATTR_RE = re.compile(
    r'(?:data-correct|data-right|data-ans|correctanswer|rightanswer)\s*=\s*["\']([^"\']+)["\']',
    re.I,
)
QNUM_IN_HTML_RE = re.compile(r'data-(?:q(?:uestion)?(?:-?no|num|number)|number)=["\']?(\d+)', re.I)


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def split_alts(ans: str):
    return [x.strip() for x in re.split(r"\s*[/|]\s*", ans) if x.strip()]


def extract_html_answers(html: str) -> dict[int, str]:
    """Best-effort extract per-question answers from paperHtml if present."""
    found: dict[int, str] = {}
    if not html:
        return found
    # pattern: blocks with question number nearby and data-answer
    # try paired attributes on same tag
    for m in re.finditer(
        r'<[^>]+data-(?:q(?:uestion)?(?:-?no|num|number)|number)=["\']?(\d+)["\']?[^>]*>',
        html,
        re.I,
    ):
        tag = m.group(0)
        num = int(m.group(1))
        am = DATA_ANSWER_RE.search(tag) or ANS_ATTR_RE.search(tag)
        if am:
            found[num] = am.group(1).strip()
    # also standalone data-answer after q markers in nearby window
    return found


def looks_chinese(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def main():
    issues = []
    stats = Counter()
    html_compare_total = 0
    html_mismatch = 0

    books = sorted(ROOT.glob("academic*"), key=lambda p: int(re.search(r"\d+", p.name).group()))
    for book_dir in books:
        book = book_dir.name
        for subject in ("reading", "listening"):
            paper_dir = book_dir / subject
            key_dir = book_dir / "keys" / subject
            if not paper_dir.is_dir():
                continue
            for paper_path in sorted(paper_dir.glob("*.json"), key=lambda p: int(p.stem) if p.stem.isdigit() else 0):
                key_path = key_dir / paper_path.name
                if not key_path.exists():
                    continue
                paper = load(paper_path)
                key = load(key_path)
                answers = key.get("answers") or {}
                label = paper.get("sName") or paper_path.stem
                s_id = paper.get("sId")
                stats["parts"] += 1

                # chinese / garbage answers
                for kn, av in answers.items():
                    s = str(av or "").strip()
                    if looks_chinese(s):
                        issues.append(
                            (
                                "high",
                                "chinese_answer",
                                book,
                                subject,
                                s_id,
                                label,
                                f"Q{kn}={s!r}",
                            )
                        )
                    if len(s) > 80:
                        issues.append(
                            (
                                "med",
                                "overlong_answer",
                                book,
                                subject,
                                s_id,
                                label,
                                f"Q{kn} len={len(s)}: {s[:60]}...",
                            )
                        )
                    if re.fullmatch(r"\d{5,}", s):
                        issues.append(
                            (
                                "high",
                                "numeric_id_as_answer",
                                book,
                                subject,
                                s_id,
                                label,
                                f"Q{kn}={s!r} 像内部ID而非答案",
                            )
                        )

                # identical answers for many consecutive questions (suspicious swap/copy)
                vals = []
                for n in sorted((int(k) for k in answers if str(k).isdigit())):
                    vals.append((n, str(answers[str(n)]).strip().lower()))
                run = 1
                for i in range(1, len(vals)):
                    if vals[i][1] and vals[i][1] == vals[i - 1][1]:
                        run += 1
                        if run >= 4:
                            issues.append(
                                (
                                    "med",
                                    "same_answer_streak",
                                    book,
                                    subject,
                                    s_id,
                                    label,
                                    f"连续>={run}题同答案 {vals[i][1]!r} around Q{vals[i][0]}",
                                )
                            )
                            break
                    else:
                        run = 1

                # compare with html-embedded answers if any
                html = paper.get("paperHtml") or ""
                embedded = extract_html_answers(html)
                if embedded:
                    stats["parts_with_html_answers"] += 1
                    for num, ea in embedded.items():
                        ka = str(answers.get(str(num)) or "").strip()
                        if not ka:
                            continue
                        html_compare_total += 1
                        ea_n = ea.strip().lower()
                        ka_alts = {a.lower() for a in split_alts(ka)}
                        if ea_n not in ka_alts and not any(ea_n in a or a in ea_n for a in ka_alts):
                            html_mismatch += 1
                            issues.append(
                                (
                                    "high",
                                    "html_key_mismatch",
                                    book,
                                    subject,
                                    s_id,
                                    label,
                                    f"Q{num} key={ka!r} html={ea!r}",
                                )
                            )

                # choice: answer letter vs option values more carefully
                for q in paper.get("questions") or []:
                    num = q.get("number")
                    opts = q.get("options") or []
                    if not opts:
                        continue
                    ka = str(answers.get(str(num)) or "").strip()
                    if not ka:
                        continue
                    values = []
                    for opt in opts:
                        if isinstance(opt, dict):
                            values.append(str(opt.get("value") or "").strip())
                        else:
                            values.append(str(opt).strip())
                    values_u = [v.upper() for v in values if v]
                    alts = [a.upper() for a in split_alts(ka)]
                    # If options are A/B/C... and answer is a long word, mismatch
                    if values_u and all(re.fullmatch(r"[A-H]", v) for v in values_u):
                        if all(not re.fullmatch(r"[A-H]", a) for a in alts):
                            # allow TRUE/FALSE/NG mapped somehow? no
                            if all(a.lower() not in {"true", "false", "not given", "yes", "no"} for a in split_alts(ka)):
                                issues.append(
                                    (
                                        "high",
                                        "word_answer_for_letter_options",
                                        book,
                                        subject,
                                        s_id,
                                        label,
                                        f"Q{num} options={values_u} answer={ka!r}",
                                    )
                                )
                    # If options are words and answer is single letter not matching
                    if values_u and all(len(v) > 1 for v in values_u):
                        if all(re.fullmatch(r"[A-H]", a) for a in alts):
                            # map letter index
                            ok = False
                            for a in alts:
                                idx = ord(a) - ord("A")
                                if 0 <= idx < len(values_u):
                                    ok = True
                            if not ok:
                                issues.append(
                                    (
                                        "high",
                                        "letter_answer_out_of_option_range",
                                        book,
                                        subject,
                                        s_id,
                                        label,
                                        f"Q{num} options={values_u[:6]} answer={ka!r}",
                                    )
                                )

                # listening answers that look like reading TFNG only when part is form filling?
                # skip

    # dedupe same_answer_streak noise: keep unique
    seen = set()
    uniq = []
    for row in issues:
        key = row
        if key in seen:
            continue
        seen.add(key)
        uniq.append(row)
    issues = uniq

    high = [i for i in issues if i[0] == "high"]
    med = [i for i in issues if i[0] == "med"]

    lines = [
        "# 剑雅答案深度筛查",
        "",
        f"- parts: {stats['parts']}",
        f"- parts_with_html_answers: {stats['parts_with_html_answers']}",
        f"- html_compare pairs: {html_compare_total}, mismatches: {html_mismatch}",
        f"- high: {len(high)}, med: {len(med)}",
        "",
        "## 高优先级",
        "",
    ]
    by_kind = Counter(i[1] for i in high)
    for k, v in by_kind.most_common():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    for sev, kind, book, subject, s_id, label, detail in high[:200]:
        lines.append(f"- **{book}/{subject}/sId={s_id}** `{kind}` {detail}  _{label}_")
    if len(high) > 200:
        lines.append(f"- ... 另有 {len(high)-200} 条")
    lines.append("")
    lines.append("## 中优先级")
    lines.append("")
    by_kind_m = Counter(i[1] for i in med)
    for k, v in by_kind_m.most_common():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    for sev, kind, book, subject, s_id, label, detail in med[:100]:
        lines.append(f"- **{book}/{subject}/sId={s_id}** `{kind}` {detail}")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"parts={stats['parts']} high={len(high)} med={len(med)} html_mismatch={html_mismatch}")
    for k, v in by_kind.most_common(20):
        print("HIGH", k, v)


if __name__ == "__main__":
    main()
