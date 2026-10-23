# -*- coding: utf-8 -*-
"""Try stripping website junk from contaminated answers and summarize recovery."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
OUT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_strip.md")

CUT_RE = re.compile(
    r"(?:Your dedicated path|Facebook\s+Instagram|Quick Links|All Rights Reserved|"
    r"Privacy Policy|elementor|wp-content|tidio|admin-ajax|prefetch|"
    r"simplyielts|Cambridge IELTS \d+ (?:Academic )?(?:Reading|Listening) Test|"
    r"\{[\"']prefetch|writable:false|learndash-wrapper|contentUrl)",
    re.I,
)


def is_garbage(s: str) -> bool:
    low = s.lower()
    return any(
        x in low
        for x in (
            "ieltszone",
            "elementor",
            "wp-content",
            "tidio",
            "admin-ajax.php",
            "simplyielts",
            "your dedicated path",
        )
    )


def strip_junk(s: str) -> str:
    m = CUT_RE.search(s)
    head = s[: m.start()] if m else s
    head = head.strip().strip("\"'`")
    # collapse weird spaces
    head = re.sub(r"\s+", " ", head).strip()
    # if still starts with JSON debris, fail
    return head


def looks_plausible(ans: str, qtype: str | None, has_opts: bool) -> bool:
    if not ans or len(ans) > 80:
        return False
    if any(x in ans.lower() for x in ("http", "{", "}", "function", "wp-", "png")):
        return False
    if re.fullmatch(r"[A-H]", ans, re.I):
        return True
    if ans.lower() in {"true", "false", "not given", "yes", "no", "t", "f", "ng", "y", "n"}:
        return True
    # gap fill: words / numbers / slash alts
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\s\-\.'/&()]*", ans):
        return True
    if "/" in ans and all(looks_plausible(p.strip(), qtype, has_opts) for p in ans.split("/") if p.strip()):
        return True
    return False


def main():
    rows = []
    stats = Counter()
    for kd in sorted(ROOT.glob("academic*/keys/*/*.json")):
        book = kd.parts[-4]
        sub = kd.parts[-2]
        key = json.loads(kd.read_text(encoding="utf-8"))
        paper_path = ROOT / book / sub / f"{kd.stem}.json"
        paper = json.loads(paper_path.read_text(encoding="utf-8")) if paper_path.exists() else {}
        qmeta = {q["number"]: q for q in paper.get("questions") or []}
        for kn, av in (key.get("answers") or {}).items():
            s = str(av or "")
            if not is_garbage(s):
                continue
            stats["contaminated"] += 1
            num = int(kn)
            q = qmeta.get(num) or {}
            cleaned = strip_junk(s)
            ok = looks_plausible(cleaned, q.get("type"), bool(q.get("options")))
            if ok:
                stats["recoverable_by_strip"] += 1
            else:
                stats["still_bad"] += 1
            rows.append(
                {
                    "book": book,
                    "subject": sub,
                    "sId": key.get("sId"),
                    "label": key.get("label"),
                    "q": kn,
                    "type": q.get("type"),
                    "ok": ok,
                    "cleaned": cleaned,
                    "raw_len": len(s),
                }
            )

    lines = [
        "# 截断网页垃圾后的答案恢复评估",
        "",
        f"- 污染答案: {stats['contaminated']}",
        f"- 截断后看似可用: {stats['recoverable_by_strip']}",
        f"- 截断后仍不可用: {stats['still_bad']}",
        "",
        "## 可恢复明细",
        "",
    ]
    for r in rows:
        if r["ok"]:
            lines.append(
                f"- {r['book']}/{r['subject']}/sId={r['sId']} Q{r['q']} -> `{r['cleaned']}` ({r['type']}) _{r['label']}_"
            )
    lines += ["", "## 仍不可用", ""]
    for r in rows:
        if not r["ok"]:
            lines.append(
                f"- {r['book']}/{r['subject']}/sId={r['sId']} Q{r['q']} cleaned=`{r['cleaned'][:100]!r}` raw_len={r['raw_len']} _{r['label']}_"
            )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(dict(stats))
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
