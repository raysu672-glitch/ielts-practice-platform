# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
OUT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_recover.md")


def is_garbage(s: str) -> bool:
    low = s.lower()
    return any(x in low for x in ("ieltszone", "elementor", "wp-content", "tidio", "admin-ajax.php"))


def main():
    recover = []
    unrecovered = []
    q40_listen_types = Counter()
    q40_read_types = Counter()

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
            num = int(kn)
            q = qmeta.get(num) or {}
            qt = q.get("type")
            has_opts = bool(q.get("options"))
            m = re.match(r"^([A-H])(?:\b|\s)", s.strip())
            if m and has_opts:
                recover.append((book, sub, key.get("sId"), kn, m.group(1), qt, key.get("label")))
            else:
                head = re.split(r"Your dedicated|Facebook|Quick Links|\{|Privacy Policy", s, maxsplit=1)[0][:80]
                unrecovered.append((book, sub, key.get("sId"), kn, qt, has_opts, head, key.get("label")))
            if kn == "40" and sub == "listening":
                q40_listen_types[qt or "?"] += 1
            if kn == "40" and sub == "reading":
                q40_read_types[qt or "?"] += 1

    lines = [
        "# 污染答案可恢复性",
        "",
        f"- 可从首字母恢复（有选项）: {len(recover)}",
        f"- 无法自动恢复: {len(unrecovered)}",
        f"- Listening Q40 types: {dict(q40_listen_types)}",
        f"- Reading Q40 types: {dict(q40_read_types)}",
        "",
        "## 可恢复（取首字母）",
        "",
    ]
    for row in recover:
        lines.append(f"- {row[0]}/{row[1]}/sId={row[2]} Q{row[3]} -> `{row[4]}` ({row[5]}) _{row[6]}_")
    lines += ["", "## 无法自动恢复", ""]
    for row in unrecovered:
        lines.append(
            f"- {row[0]}/{row[1]}/sId={row[2]} Q{row[3]} type={row[4]} opts={row[5]} head=`{row[6]!r}` _{row[7]}_"
        )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print("recover", len(recover), "unrecovered", len(unrecovered))
    print("listen Q40", dict(q40_listen_types))
    print("read Q40", dict(q40_read_types))
    # print unrecovered summary by book
    c = Counter((r[0], r[1]) for r in unrecovered)
    print("unrecovered by book/subject", dict(c))


if __name__ == "__main__":
    main()
