# -*- coding: utf-8 -*-
"""Find contaminated / garbage answer keys in jianya exam-data."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
OUT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_contamination.md")

GARBAGE_PATTERNS = [
    (r"ieltszone", "ieltszone"),
    (r"elementor", "elementor"),
    (r"wp-content", "wp-content"),
    (r"facebook\s+instagram", "social_footer"),
    (r"all rights reserved", "copyright_footer"),
    (r"tidiochatcode|tidio\.co", "tidio_chat"),
    (r"prefetch", "prefetch_json"),
    (r"privacy policy", "privacy_policy"),
    (r"quick links", "quick_links"),
    (r"document\.querySelector", "js_snippet"),
    (r"admin-ajax\.php", "wp_ajax"),
    (r"your dedicated path to band", "marketing_blurb"),
]

# answers that are clearly not IELTS answers
PHONEISH = re.compile(r"^\d{8,}$")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def classify(ans: str) -> list[str]:
    tags = []
    s = ans or ""
    low = s.lower()
    if len(s) > 120:
        tags.append("overlong")
    for pat, name in GARBAGE_PATTERNS:
        if re.search(pat, low):
            tags.append(name)
    if PHONEISH.match(s.strip()):
        tags.append("phoneish_number")
    if re.search(r"[\u4e00-\u9fff]", s):
        tags.append("chinese")
    if "{" in s and "}" in s and len(s) > 80:
        tags.append("jsonish")
    if s.count("function") >= 2 or "=>" in s and "const " in s:
        tags.append("js_heavy")
    return tags


def main():
    bad_rows = []
    book_bad = Counter()
    tag_counts = Counter()
    total_answers = 0
    parts = 0

    for book_dir in sorted(ROOT.glob("academic*"), key=lambda p: int(re.search(r"\d+", p.name).group())):
        book = book_dir.name
        for subject in ("reading", "listening"):
            kd = book_dir / "keys" / subject
            if not kd.is_dir():
                continue
            for fp in sorted(kd.glob("*.json"), key=lambda p: int(p.stem) if p.stem.isdigit() else 0):
                key = load(fp)
                parts += 1
                answers = key.get("answers") or {}
                label = key.get("label") or fp.stem
                for kn, av in answers.items():
                    total_answers += 1
                    s = str(av or "")
                    tags = classify(s)
                    if not tags:
                        continue
                    # only keep meaningful contamination / hard errors
                    hard = [t for t in tags if t not in {"overlong"}]
                    if not hard and "overlong" in tags:
                        hard = ["overlong"]
                    # skip mild overlong if it's just a long phrase without garbage
                    if hard == ["overlong"] and len(s) < 200 and not re.search(r"[<>{}]", s):
                        continue
                    tag_counts.update(hard)
                    book_bad[book] += 1
                    bad_rows.append(
                        {
                            "book": book,
                            "subject": subject,
                            "sId": key.get("sId"),
                            "label": label,
                            "q": kn,
                            "tags": hard,
                            "preview": s.replace("\n", " ")[:160],
                            "len": len(s),
                        }
                    )

    # also find answers that start with letter then huge junk: "B Your dedicated..."
    letter_junk = [
        r
        for r in bad_rows
        if re.match(r"^[A-H]\s+\S{10,}", r["preview"]) and r["len"] > 80
    ]

    lines = []
    lines.append("# 剑雅标准答案污染 / 垃圾答案筛查")
    lines.append("")
    lines.append(f"- 检查 Part: {parts}")
    lines.append(f"- 答案条目总数: {total_answers}")
    lines.append(f"- 异常答案条数: {len(bad_rows)}")
    lines.append(f"- 其中「字母+网页垃圾」形态: {len(letter_junk)}")
    lines.append("")
    lines.append("## 按册统计异常答案数")
    lines.append("")
    for book, n in book_bad.most_common():
        lines.append(f"- `{book}`: {n}")
    lines.append("")
    lines.append("## 按标签统计")
    lines.append("")
    for t, n in tag_counts.most_common():
        lines.append(f"- `{t}`: {n}")
    lines.append("")
    lines.append("## 明细（按册/科目）")
    lines.append("")
    by = defaultdict(list)
    for r in bad_rows:
        by[(r["book"], r["subject"], r["sId"], r["label"])].append(r)
    for (book, subject, s_id, label), rows in sorted(by.items()):
        lines.append(f"### {book} / {subject} / sId={s_id}")
        lines.append(f"- {label}")
        for r in rows:
            lines.append(
                f"- Q{r['q']} tags={','.join(r['tags'])} len={r['len']}: `{r['preview']}`"
            )
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"parts={parts} total_answers={total_answers} bad={len(bad_rows)}")
    print("by book:", dict(book_bad))
    print("tags:", dict(tag_counts))
    # show compact list of affected sIds
    affected = sorted({(r["book"], r["subject"], r["sId"]) for r in bad_rows})
    print(f"affected parts: {len(affected)}")
    for row in affected:
        print(" ", row)


if __name__ == "__main__":
    main()
