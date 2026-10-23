# -*- coding: utf-8 -*-
"""Strip website junk from recoverable jianya answer keys and write back."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
REPORT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_strip_fix.md")

CUT_RE = re.compile(
    r"(?:Your dedicated path|Facebook\s+Instagram|Quick Links|All Rights Reserved|"
    r"Privacy Policy|elementor|wp-content|tidio|admin-ajax|prefetch|"
    r"simplyielts|Cambridge IELTS \d+ (?:Academic )?(?:Reading|Listening) Test|"
    r"\{[\"']prefetch|writable:false|learndash-wrapper|contentUrl)",
    re.I,
)

GARBAGE_MARKERS = (
    "ieltszone",
    "elementor",
    "wp-content",
    "tidio",
    "admin-ajax.php",
    "simplyielts",
    "your dedicated path",
)

TFNG_MAP = {
    "true": "TRUE",
    "false": "FALSE",
    "not given": "NOT GIVEN",
    "yes": "YES",
    "no": "NO",
    "t": "TRUE",
    "f": "FALSE",
    "ng": "NOT GIVEN",
    "y": "YES",
    "n": "NO",
}


def is_garbage(s: str) -> bool:
    low = s.lower()
    return any(x in low for x in GARBAGE_MARKERS)


def strip_junk(s: str) -> str:
    m = CUT_RE.search(s)
    head = s[: m.start()] if m else s
    head = head.strip().strip("\"'`")
    return re.sub(r"\s+", " ", head).strip()


def looks_plausible(ans: str) -> bool:
    if not ans or len(ans) > 80:
        return False
    if any(x in ans.lower() for x in ("http", "{", "}", "function", "wp-", "png")):
        return False
    if re.fullmatch(r"[A-H]", ans, re.I):
        return True
    if ans.lower() in TFNG_MAP:
        return True
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\s\-\.'/&()]*", ans):
        return True
    if "/" in ans:
        parts = [p.strip() for p in ans.split("/") if p.strip()]
        return bool(parts) and all(looks_plausible(p) for p in parts)
    return False


def normalize_cleaned(ans: str, options: list) -> str:
    """Prefer option casing for TF/NG/YES/NO and single letters."""
    alts = [p.strip() for p in re.split(r"\s*/\s*", ans) if p.strip()]
    opt_values = []
    for o in options or []:
        if isinstance(o, dict):
            v = str(o.get("value") or "").strip()
        else:
            v = str(o).strip()
        if v:
            opt_values.append(v)
    opt_by_upper = {v.upper(): v for v in opt_values}

    out = []
    for a in alts:
        up = a.upper()
        if up in opt_by_upper:
            out.append(opt_by_upper[up])
            continue
        mapped = TFNG_MAP.get(a.lower())
        if mapped:
            out.append(opt_by_upper.get(mapped.upper(), mapped))
            continue
        if re.fullmatch(r"[A-H]", a, re.I):
            out.append(a.upper())
            continue
        out.append(a)
    return " / ".join(out) if len(out) > 1 and "/" in ans else (out[0] if len(out) == 1 else ans)


def main() -> None:
    fixed = []
    skipped = []
    files_touched = 0
    stats = Counter()

    for kd in sorted(ROOT.glob("academic*/keys/*/*.json")):
        book = kd.parts[-4]
        sub = kd.parts[-2]
        key = json.loads(kd.read_text(encoding="utf-8"))
        answers = key.get("answers")
        if not isinstance(answers, dict):
            continue
        paper_path = ROOT / book / sub / f"{kd.stem}.json"
        paper = json.loads(paper_path.read_text(encoding="utf-8")) if paper_path.exists() else {}
        qmeta = {q["number"]: q for q in paper.get("questions") or []}

        changed = False
        for kn, av in list(answers.items()):
            raw = str(av or "")
            if not is_garbage(raw):
                continue
            stats["contaminated"] += 1
            cleaned = strip_junk(raw)
            if not looks_plausible(cleaned):
                stats["skipped"] += 1
                skipped.append(
                    {
                        "book": book,
                        "subject": sub,
                        "sId": key.get("sId"),
                        "label": key.get("label"),
                        "q": kn,
                        "cleaned": cleaned[:120],
                        "raw_len": len(raw),
                    }
                )
                continue
            num = int(kn) if str(kn).isdigit() else None
            q = qmeta.get(num) or {}
            final = normalize_cleaned(cleaned, q.get("options") or [])
            answers[kn] = final
            changed = True
            stats["fixed"] += 1
            fixed.append(
                {
                    "book": book,
                    "subject": sub,
                    "sId": key.get("sId"),
                    "label": key.get("label"),
                    "q": kn,
                    "before_len": len(raw),
                    "after": final,
                }
            )

        if changed:
            key["answers"] = answers
            kd.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            files_touched += 1

    lines = [
        "# 剑雅答案污染自动清洗报告",
        "",
        f"- 污染条数扫描到: {stats['contaminated']}",
        f"- 已清洗写回: {stats['fixed']}",
        f"- 跳过（仍需重抓）: {stats['skipped']}",
        f"- 改动文件数: {files_touched}",
        "",
        "## 已清洗",
        "",
    ]
    for r in fixed:
        lines.append(
            f"- {r['book']}/{r['subject']}/sId={r['sId']} Q{r['q']}: "
            f"`{r['after']}` (原长 {r['before_len']}) _{r['label']}_"
        )
    lines += ["", "## 跳过（需第 2 步重抓/手补）", ""]
    for r in skipped:
        lines.append(
            f"- {r['book']}/{r['subject']}/sId={r['sId']} Q{r['q']} "
            f"raw_len={r['raw_len']} cleaned=`{r['cleaned']!r}` _{r['label']}_"
        )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"fixed={stats['fixed']} skipped={stats['skipped']} files={files_touched}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
