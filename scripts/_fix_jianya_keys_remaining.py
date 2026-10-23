# -*- coding: utf-8 -*-
"""Fix remaining contaminated jianya keys (C16 Test 3 + C10 reading gaps)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"D:/ielts-practice-platform/sources/jianyazhenti/exam-data")
REPORT = Path(r"D:/ielts-practice-platform/_sim_out/jianya_keys_remaining_fix.md")

# Cross-checked against multiple public Cambridge answer keys + embedded
# simplyielts table inside academic16/keys/listening/658.json Q40 blob.
# For either-order pairs, both slots accept either letter (A/C style).
C16_TEST3 = {
    1: "park",
    2: "blue",
    3: "reference",
    4: "story",
    5: "rain",
    6: "snack",
    7: "medication",
    8: "helmet",
    9: "tent",
    10: "199",
    11: "A/C",
    12: "A/C",
    13: "B/C",
    14: "B/C",
    15: "D",
    16: "F",
    17: "A",
    18: "H",
    19: "C",
    20: "G",
    21: "C/D",
    22: "C/D",
    23: "C/E",
    24: "C/E",
    25: "C",
    26: "A",
    27: "B",
    28: "A",
    29: "A",
    30: "C",
    31: "grandmother",
    32: "decade",
    33: "equipment",
    34: "economic",
    35: "basic",
    36: "round",
    37: "bone",
    38: "rough",
    39: "style",
    40: "sheep",
}

C16_FILES = {
    "655.json": range(1, 11),
    "656.json": range(11, 21),
    "657.json": range(21, 31),
    "658.json": range(31, 41),
}

# Extracted from embedded simplyielts tables in the garbage blobs + public keys.
C10_FIXES = {
    ("787.json", "2"): "viii",  # Test 2 Passage 1
    ("790.json", "1"): "ii",  # Test 3 Passage 1
    ("793.json", "2"): "10 / ten times",  # Test 4 Passage 1
}


def main() -> None:
    changes: list[str] = []

    for fname, nums in C16_FILES.items():
        path = ROOT / "academic16" / "keys" / "listening" / fname
        key = json.loads(path.read_text(encoding="utf-8"))
        before = dict(key.get("answers") or {})
        for n in nums:
            key["answers"][str(n)] = C16_TEST3[n]
        path.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for n in nums:
            old = str(before.get(str(n), ""))
            new = C16_TEST3[n]
            if old != new:
                changes.append(
                    f"academic16/listening/sId={key.get('sId')} Q{n}: "
                    f"{old[:50]!r} -> {new!r}"
                )

    for fname, qn in C10_FIXES:
        path = ROOT / "academic10" / "keys" / "reading" / fname
        key = json.loads(path.read_text(encoding="utf-8"))
        old = str(key["answers"].get(qn, ""))
        new = C10_FIXES[(fname, qn)]
        key["answers"][qn] = new
        path.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append(
            f"academic10/reading/sId={key.get('sId')} Q{qn}: {old[:50]!r} -> {new!r}"
        )

    # verify no website-garbage left
    left = []
    overlong = []
    for kd in sorted(ROOT.glob("academic*/keys/*/*.json")):
        d = json.loads(kd.read_text(encoding="utf-8"))
        for k, v in (d.get("answers") or {}).items():
            s = str(v)
            low = s.lower()
            if any(
                x in low
                for x in (
                    "ieltszone",
                    "elementor",
                    "wp-content",
                    "tidio",
                    "simplyielts",
                    "your dedicated path",
                    "admin-ajax.php",
                )
            ):
                left.append((kd.parts[-4], kd.parts[-2], d.get("sId"), k, len(s)))
            elif len(s) > 120:
                overlong.append((kd.parts[-4], kd.parts[-2], d.get("sId"), k, len(s), s[:80]))

    lines = [
        "# 剩余答案修复报告",
        "",
        f"- 改动条数: {len(changes)}",
        f"- 网页垃圾残留: {len(left)}",
        f"- 超长答案(>120)残留: {len(overlong)}",
        "",
        "## 改动明细",
        "",
    ]
    lines.extend(f"- {c}" for c in changes)
    lines += ["", "## 网页垃圾残留", ""]
    if not left:
        lines.append("（无）")
    else:
        lines.extend(f"- {r}" for r in left)
    lines += ["", "## 超长答案残留（可能仍是解析文，非本题第2步范围）", ""]
    if not overlong:
        lines.append("（无）")
    else:
        for r in overlong[:40]:
            lines.append(f"- {r[0]}/{r[1]}/sId={r[2]} Q{r[3]} len={r[4]}: {r[5]!r}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"changes={len(changes)} garbage_left={len(left)} overlong={len(overlong)}")
    print("Wrote", REPORT)
    for r in left:
        print("GARBAGE", r)
    for r in overlong[:15]:
        print("OVERLONG", r[:5])


if __name__ == "__main__":
    main()
