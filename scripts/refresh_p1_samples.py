# -*- coding: utf-8 -*-
"""Align all P1 questions in place; keep heatRank/recentCount/order; attach core-kit variants."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p1_align_engine import align_question_all_kits  # noqa: E402
from p1_material_bank import MATERIALS, export_bank_for_js  # noqa: E402

P1 = ROOT / "sources" / "kouyulianxi" / "p1-data.js"
KITS_JS = ROOT / "sources" / "kouyulianxi" / "p1-kits-data.js"


def main() -> None:
    text = P1.read_text(encoding="utf-8")
    brace = text.find("{", text.find("const P1_DATA ="))
    depth = 0
    end = brace
    for i, ch in enumerate(text[brace:], brace):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    data = json.loads(text[brace:end])
    fail = 0
    note_counts: dict[str, int] = {}
    topic_order: dict[str, list[str]] = {}
    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            topic_order.setdefault(t, [])
            if q["q"] not in topic_order[t]:
                topic_order[t].append(q["q"])

    for cat in data["categories"]:
        for q in cat["questions"]:
            t = q.get("topicEn") or ""
            idx = topic_order.get(t, [q["q"]]).index(q["q"]) if q["q"] in topic_order.get(t, []) else 0
            aligned = align_question_all_kits(cat["id"], q["q"], t, topic_q_index=idx)
            for k in (
                "words",
                "logic",
                "material",
                "frames",
                "sample",
                "sampleZh",
                "sampleOk",
                "sampleNote",
                "sampleSource",
                "wordSource",
                "kitId",
                "kitIds",
                "kitNameZh",
                "kitSummary",
                "kitHint",
                "kitSlice",
                "kitRest",
                "kitAngle",
                "kitVariants",
            ):
                q[k] = aligned[k]
            q["frameVariant"] = aligned.get("frameVariant", idx % 3)
            tip = q.get("tip") or ""
            prefix = tip.split("】", 1)[0] + "】" if "】" in tip else ""
            # Keep tip = heat prefix + clean kit logic only (preview style; no messy dump)
            q["tip"] = f"{prefix}{aligned['logic']}"
            if not aligned["sampleOk"]:
                fail += 1
                note_counts[aligned["sampleNote"]] = note_counts.get(aligned["sampleNote"], 0) + 1

    data["meta"]["sampleLogicFail"] = fail
    data["meta"]["note"] = (
        "当季删旧补新；素材库对齐课堂《P1素材》PDF（衣食住行/行为爱好/时间线/感受/同义替换/万能句）；"
        "按五大题型原步骤填槽；先扣题再套料；同题可切换、同素材可串多题"
    )
    data["meta"]["coreKits"] = len(MATERIALS)
    data["meta"]["materialBank"] = len(MATERIALS)
    out = (
        "// P1 data - 2026年9-12月在考题 + 可组合生活素材库（固定四步）\n"
        "const P1_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n\nif (typeof window !== 'undefined') {\n  window.P1_DATA = P1_DATA;\n}\n"
    )
    P1.write_text(out, encoding="utf-8")

    bank = export_bank_for_js()
    # Keep P1_KITS_DATA shape so practice UI switcher keeps working (id/nameZh/summary).
    kits_payload = {
        "kits": [
            {
                "id": m["id"],
                "nameZh": m["nameZh"],
                "summary": m.get("summary") or "",
                "kind": m.get("kind") or "",
            }
            for m in bank["materials"]
        ],
        "materials": bank["materials"],
    }
    KITS_JS.write_text(
        "// P1 life-material bank (composable; switcher reads .kits)\n"
        "const P1_KITS_DATA = "
        + json.dumps(kits_payload, ensure_ascii=False, indent=2)
        + ";\n\nif (typeof window !== 'undefined') {\n  window.P1_KITS_DATA = P1_KITS_DATA;\n}\n",
        encoding="utf-8",
    )

    print(f"aligned all; sampleLogicFail={fail}")
    for k, v in sorted(note_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {v}x {k}")
    print(f"wrote {KITS_JS.name}")


if __name__ == "__main__":
    main()
