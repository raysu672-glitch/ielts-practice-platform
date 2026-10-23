#!/usr/bin/env python3
"""审计 juzifanyixin 每句每步：中英对应、递进逻辑、关键词落点。"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_sim_out/translate_steps_audit_raw.json").read_text(encoding="utf-8"))
OUT = ROOT / "_sim_out/translate_steps_audit_report.md"
OUT_JSON = ROOT / "_sim_out/translate_steps_audit.json"

# 中文概念 → 英文应至少出现其一（宽松启发式）
CN_EN_CUES = [
    (r"简化|更容易|更便捷|更方便", ["easier", "easy", "simplify", "simplifies", "simplified", "simplify"]),
    (r"最大", ["greatest", "biggest", "largest", "maximum", "most"]),
    (r"互联网|因特网", ["internet", "online"]),
    (r"极大地|显著|大大", ["much", "greatly", "significantly", "remarkably", "considerably", "dramatically"]),
    (r"人与人|彼此|互相", ["between people", "each other", "one another", "people"]),
    (r"例如|比如", ["for example", "for instance", "such as", "like"]),
    (r"因为|由于|as ", ["because", "as", "since", "due to"]),  # as 易误报，后面再滤
    (r"此外|另外|而且", ["in addition", "additionally", "moreover", "furthermore", "what's more", "also"]),
    (r"因此|所以", ["therefore", "thus", "so", "hence", "consequently"]),
    (r"尽管|虽然|即使", ["in spite of", "despite", "although", "though", "even if", "even though"]),
    (r"一方面", ["on the one hand"]),
    (r"另一方面", ["on the other hand"]),
    (r"政府", ["government"]),
    (r"投资", ["investment", "invest"]),
    (r"免费", ["free"]),
    (r"儿童|孩子", ["children", "child", "kids"]),
    (r"疾病", ["disease", "diseases", "illness"]),
    (r"疫苗", ["vaccine", "vaccines"]),
]


def strip_marks(cn: str) -> str:
    return re.sub(r"[【】]", "", cn or "")


def highlights(cn: str) -> list[str]:
    return re.findall(r"【(.+?)】", cn or "")


def norm_en(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def en_tokens(s: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", norm_en(s))


def almost_contained(prev: str, cur: str) -> tuple[bool, float, list[str]]:
    """prev 的实词是否大部分出现在 cur（允许增词、少量屈折差异）。"""
    pt = [t for t in en_tokens(prev) if t not in {"a", "an", "the", "to", "of", "in", "on", "at", "is", "are", "be", "that", "it"}]
    if not pt:
        return True, 1.0, []
    ct = set(en_tokens(cur))
    missing = [t for t in pt if t not in ct]
    # 允许少数缺失（屈折/改写），缺失过多则报警
    ratio = 1 - len(missing) / len(pt)
    return ratio >= 0.75, ratio, missing


def keyword_en_parts(kw: str) -> list[str]:
    """'advantage (优势)' / 'makes ... easier (简化)' → 英文侧。"""
    left = kw.split("(")[0].strip()
    left = left.replace("...", " ").replace("…", " ")
    parts = [p.strip().lower() for p in re.split(r"[/,]", left) if p.strip()]
    return parts


def check_keywords_in_answer(step: dict) -> list[str]:
    ans = norm_en(step.get("correctAnswer") or "")
    issues = []
    for kw in step.get("keywords") or []:
        parts = keyword_en_parts(kw)
        if not parts:
            continue
        # 每个 part 的词都要在答案里（makes ... easier → makes 与 easier）
        for part in parts:
            words = [w for w in re.findall(r"[a-z0-9']+", part) if w not in {"and", "or", "the", "a"}]
            if not words:
                continue
            if not all(w in ans for w in words):
                issues.append(f"关键词「{kw}」的英文「{part}」未完整出现在答案中")
                break
    return issues


def check_cn_en_cues(cn: str, en: str) -> list[str]:
    issues = []
    en_l = norm_en(en)
    cn_plain = strip_marks(cn)
    for cn_pat, en_opts in CN_EN_CUES:
        if re.search(cn_pat, cn_plain):
            if not any(opt in en_l for opt in en_opts):
                # 特殊：中文「因为」在主干步可能尚未加入
                issues.append(
                    f"中文含「{cn_pat}」相关含义，英文未见 {en_opts[:4]} 等对应"
                )
    return issues


def check_highlight_vs_growth(prev_en: str | None, cur: dict) -> list[str]:
    """【】新增中文，英文应相对上一步有新增词（非第一步）。"""
    issues = []
    hs = highlights(cur.get("chinese") or "")
    if not hs:
        return issues
    if not prev_en:
        # 第一步有【】不常见，标注意
        issues.append(f"第一步中文含高亮【】{hs}，请确认是否应为无高亮主干")
        return issues
    prev_set = set(en_tokens(prev_en))
    cur_set = set(en_tokens(cur.get("correctAnswer") or ""))
    added = sorted(cur_set - prev_set)
    if not added:
        issues.append(f"中文有新增高亮{hs}，但英文相对上一步几乎无新增词")
    return issues


def audit_sentence(s: dict) -> list[dict]:
    findings = []
    steps = s.get("steps") or []
    final = s.get("finalEnglish") or ""
    for i, step in enumerate(steps):
        cn = step.get("chinese") or ""
        en = step.get("correctAnswer") or ""
        label = step.get("label") or f"step{i+1}"
        probs = []

        if not en.strip():
            probs.append("英文答案为空")
        if not cn.strip():
            probs.append("中文为空")

        # 关键词
        probs.extend(check_keywords_in_answer(step))

        # 中英线索
        for msg in check_cn_en_cues(cn, en):
            # 过滤过宽：第一步常故意省略部分修饰
            if i == 0 and any(x in msg for x in ["最大", "互联网", "极大地", "人与人", "例如", "此外", "因此", "尽管", "一方面", "政府", "免费"]):
                # 若中文主干步已写出这些词，则仍报
                plain = strip_marks(cn)
                serious = False
                if re.search(r"最大", plain) and "最大" in msg:
                    serious = True
                if re.search(r"互联网|因特网", plain) and ("互联网" in msg or "因特网" in msg):
                    serious = True
                if re.search(r"极大地|显著地|大大", plain) and "极大地" in msg:
                    serious = True
                if re.search(r"简化|更容易|更便捷", plain) and "简化" in msg:
                    serious = True
                if not serious:
                    continue
            probs.append(msg)

        # 递进：相对上一步
        if i > 0:
            prev_en = steps[i - 1].get("correctAnswer") or ""
            ok, ratio, missing = almost_contained(prev_en, en)
            if not ok:
                probs.append(
                    f"递进断裂：上一步实词保留率 {ratio:.0%}，缺失例 {missing[:8]}"
                )
            probs.extend(check_highlight_vs_growth(prev_en, step))
            # 上一步不应比当前更长太多（当前应扩展）
            if len(en_tokens(en)) + 1 < len(en_tokens(prev_en)):
                probs.append("英文比上一步更短，递进方向异常")

        # 最后一步应接近 finalEnglish
        if i == len(steps) - 1 and final:
            ok, ratio, missing = almost_contained(en, final)
            ok2, ratio2, missing2 = almost_contained(final, en)
            if norm_en(en) != norm_en(final):
                if not (ok and ok2):
                    probs.append(
                        f"末步与 finalEnglish 不一致（互含率 {ratio:.0%}/{ratio2:.0%}），"
                        f"差集例 {sorted(set(missing + missing2))[:10]}"
                    )
                elif norm_en(en) != norm_en(final):
                    # 仅标点/微小差异
                    if abs(len(en) - len(final)) > 5:
                        probs.append("末步与 finalEnglish 文本不完全相同（请人工确认）")

        # 英文残缺句启发式：makes X. 无形容词；以介词结尾等
        if re.search(r"\bmakes\s+\w+\.$", en.strip(), re.I):
            if not re.search(r"easier|easy|possible|better|harder", en, re.I):
                probs.append("英文疑似残缺（makes Noun. 无补足语），与中文可能不对齐")

        if probs:
            findings.append(
                {
                    "id": s["id"],
                    "category": s.get("category"),
                    "step": i + 1,
                    "label": label,
                    "chinese": cn,
                    "english": en,
                    "problems": probs,
                }
            )
    return findings


def main() -> None:
    all_f = []
    for s in DATA:
        all_f.extend(audit_sentence(s))

    # 去重问题类型统计
    by_type = defaultdict(int)
    for f in all_f:
        for p in f["problems"]:
            key = p.split("：")[0].split("「")[0][:40]
            by_type[key] += 1

    lines = []
    lines.append("# 句子翻译逐步中英对齐审计")
    lines.append("")
    lines.append(f"- 句数：{len(DATA)}")
    lines.append(f"- 步骤总数：{sum(len(s['steps']) for s in DATA)}")
    lines.append(f"- 检出问题步骤：{len(all_f)}")
    lines.append("")
    lines.append("## 问题类型统计")
    lines.append("")
    for k, n in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"- {k}: {n}")
    lines.append("")
    lines.append("## 问题明细（按句子 ID）")
    lines.append("")

    by_id = defaultdict(list)
    for f in all_f:
        by_id[f["id"]].append(f)

    for sid in sorted(by_id):
        items = by_id[sid]
        cat = items[0]["category"]
        lines.append(f"### #{sid} · {cat}")
        for f in items:
            lines.append(f"- **Step {f['step']}（{f['label']}）**")
            lines.append(f"  - 中：{f['chinese']}")
            lines.append(f"  - 英：{f['english']}")
            for p in f["problems"]:
                lines.append(f"  - ⚠ {p}")
        lines.append("")

    # 另附：无问题句子 ID，便于确认覆盖
    clean = [s["id"] for s in DATA if s["id"] not in by_id]
    lines.append("## 启发式未报问题的句子")
    lines.append("")
    lines.append(f"共 {len(clean)} 句：{', '.join(str(i) for i in clean)}")
    lines.append("")
    lines.append(
        "> 说明：本报告以规则/关键词/递进结构为主，语义细微偏差仍需人工抽查；"
        "「中文含某含义但英文未见」在主干步可能是故意省略，已做部分过滤。"
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {"findings": all_f, "clean_ids": clean, "by_type": dict(by_type)},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"findings={len(all_f)} sentences_flagged={len(by_id)} clean={len(clean)}")
    print(f"wrote {OUT}")
    # print top summary
    for k, n in sorted(by_type.items(), key=lambda x: -x[1])[:15]:
        print(f"  {n:4} {k}")


if __name__ == "__main__":
    main()
