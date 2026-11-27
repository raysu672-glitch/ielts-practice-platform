# -*- coding: utf-8 -*-
"""Export latest P1 Freestyle samples/kits to a downloadable Excel file."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from p1_freestyle_packs import build  # noqa: E402
from p1_material_bank import (  # noqa: E402
    MATERIALS,
    QUESTION_KIT_ALLOW,
    effective_topics,
    material_ids_for_question,
)
from p1_word_banks_core import norm_q  # noqa: E402


def load_p1_data() -> dict:
    build()
    text = (ROOT / "sources/kouyulianxi/p1-data.js").read_text(encoding="utf-8")
    brace = text.find("{", text.find("const P1_DATA"))
    depth = 0
    for i, ch in enumerate(text[brace:], brace):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[brace : i + 1])
    raise RuntimeError("P1_DATA not found")


def main() -> Path:
    data = load_p1_data()
    out_dir = ROOT / "exports"
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = out_dir / f"p1_freestyle_latest_{stamp}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "示范与素材"
    headers = [
        "话题",
        "题型",
        "题面",
        "素材ID",
        "素材名",
        "答题思路",
        "素材提示",
        "示范英文",
        "示范中文",
        "是否白名单",
    ]
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(1, c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="2F5496")
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    allow_set = set(QUESTION_KIT_ALLOW.keys())
    n = 0
    q_count = 0
    for cat in data["categories"]:
        cat_id = cat.get("id") or ""
        steps = " / ".join(cat.get("steps") or [])
        for q in cat["questions"]:
            q_count += 1
            topic = q.get("topicEn") or ""
            qtext = q.get("q") or ""
            kits = material_ids_for_question(topic, qtext, 3)
            variants = q.get("kitVariants") or {}
            for kid in kits:
                v = variants.get(kid) or {}
                mid = MATERIALS.get(kid) or {}
                ws.append(
                    [
                        topic,
                        f"{cat_id} ({steps})",
                        qtext,
                        kid,
                        mid.get("nameZh") or kid,
                        v.get("logic") or "",
                        v.get("kitHint") or "",
                        v.get("sample") or "",
                        v.get("sampleZh") or "",
                        "Y" if norm_q(qtext) in allow_set else "N",
                    ]
                )
                n += 1

    widths = [18, 28, 42, 22, 16, 36, 36, 55, 55, 10]
    for col, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(col)].width = w
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=10):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.auto_filter.ref = f"A1:J{ws.max_row}"
    ws.freeze_panes = "A2"

    ws2 = wb.create_sheet("题级白名单")
    ws2.append(["题面", "素材1", "素材2", "素材3", "素材4"])
    for c in range(1, 6):
        cell = ws2.cell(1, c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="548235")
    norm_to_q = {}
    for cat in data["categories"]:
        for q in cat["questions"]:
            norm_to_q[norm_q(q["q"])] = q["q"]
    for nq, kits in sorted(
        QUESTION_KIT_ALLOW.items(), key=lambda x: norm_to_q.get(x[0], x[0])
    ):
        row = [norm_to_q.get(nq, nq)] + list(kits)
        while len(row) < 5:
            row.append("")
        ws2.append(row[:5])
    for col, w in enumerate([50, 24, 24, 24, 24], 1):
        ws2.column_dimensions[get_column_letter(col)].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:E{ws2.max_row}"

    ws3 = wb.create_sheet("共享素材库")
    ws3.append(["素材ID", "中文名", "类型", "可挂话题", "摘要"])
    for c in range(1, 6):
        cell = ws3.cell(1, c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="833C0C")
    for mid, m in sorted(MATERIALS.items()):
        ws3.append(
            [
                mid,
                m.get("nameZh") or "",
                m.get("kind") or "",
                " / ".join(effective_topics(m)),
                m.get("summary") or "",
            ]
        )
    for col, w in enumerate([24, 16, 14, 48, 50], 1):
        ws3.column_dimensions[get_column_letter(col)].width = w
    ws3.freeze_panes = "A2"

    ws4 = wb.create_sheet("说明")
    ws4["A1"] = "P1 Freestyle 最新导出（改后版本）"
    ws4["A2"] = f"导出时间: {stamp}"
    ws4["A3"] = f"示范行数: {n}"
    ws4["A4"] = f"题数: {q_count}"
    ws4["A5"] = f"白名单题数: {len(QUESTION_KIT_ALLOW)}"
    ws4["A6"] = (
        "内容来源: sources/kouyulianxi/p1-data.js + scripts/p1_packs + QUESTION_KIT_ALLOW"
    )
    ws4["A7"] = "工作表: 示范与素材 / 题级白名单 / 共享素材库"
    ws4.column_dimensions["A"].width = 90

    wb.save(out)

    # stable latest copy for easy download
    latest = out_dir / "p1_freestyle_latest.xlsx"
    latest.write_bytes(out.read_bytes())
    print(out.resolve())
    print(latest.resolve())
    print(f"rows={n} questions={q_count} allow={len(QUESTION_KIT_ALLOW)}")
    return latest


if __name__ == "__main__":
    main()
