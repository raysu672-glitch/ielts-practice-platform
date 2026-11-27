# -*- coding: utf-8 -*-
"""
Align every P1 question from the composable life-material bank.

User model:
1) Fixed CAT_STEPS by question type
2) Pick a material → fill open / origin / frequency(+feel|impact)
3) Same question + different material = different answer
4) Same material reusable across topics
"""
from __future__ import annotations

import re
from typing import Any

from p1_frames import resolve_frames, variant_seed_for
from p1_word_banks_core import CAT_STEPS
from p1_material_bank import (
    FEEL_HAPPY,
    FEEL_PRACTICAL,
    FEEL_RELAX,
    FEEL_STRESS,
    FREQ_OFTEN,
    get_material,
    material_ids_for_question,
    materials_for_question,
)

try:
    from p1_topic_materials import get_question_pack
except ImportError:  # pragma: no cover
    def get_question_pack(qtext: str):  # type: ignore
        return None


def _mentions_work_studies(ql: str) -> bool:
    return any(
        k in ql
        for k in (
            "job",
            "studies",
            "student",
            "subject",
            "career",
            "major",
            "at work",
            "at school",
            "your work",
            "your studies",
            "work or",
        )
    )


def detect_intent(q: str) -> str:
    """What the question is actually asking — sample/open must answer this."""
    ql = (q or "").lower().strip()
    if "do you work or are you a student" in ql:
        return "work_or_student"
    if "why did you choose" in ql or (ql.startswith("why ") and ("job" in ql or "subject" in ql or "major" in ql)):
        return "why_choose"
    if ("challenging" in ql or "difficult" in ql or "hard about" in ql) and _mentions_work_studies(ql):
        return "challenging"
    if ("typical day" in ql or "daily routine" in ql) and _mentions_work_studies(ql):
        return "typical_day"
    # Career/studies future only — bare "in the future" is NOT enough
    if "would you like to be doing" in ql and _mentions_work_studies(ql):
        return "future_plan"
    if ("in a few years" in ql or "future career" in ql) and _mentions_work_studies(ql):
        return "future_plan"
    if ("like most" in ql or "enjoy most" in ql) and _mentions_work_studies(ql):
        return "like_most"
    if ql.startswith("how often"):
        return "how_often"
    if "prefer" in ql or "rather" in ql:
        return "prefer"
    if ql.startswith("why "):
        return "why"
    if any(x in ql for x in ("when you were a child", "as a child", "in your childhood", "when you were little")):
        return "childhood"
    if "do you think" in ql or "is it important" in ql or "how do you think" in ql:
        return "opinion"
    if re.search(r"what do you (usually )?do when", ql) or "what do you do if" in ql:
        return "do_when"
    if "would you like to live" in ql:
        return "live_wish"
    if "what kind of home" in ql or "what kind of house" in ql:
        return "home_wish"
    if "scientific discovery" in ql:
        return "science_wish"
    if "where would you most like to travel" in ql or "where would you like to travel" in ql:
        return "travel_wish"
    return "general"


def _cap(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "Yes"
    return s if s[0].isupper() else s[0].upper() + s[1:]


def _sent(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return ""
    if text[-1] not in ".!?":
        text += "."
    return text


def _looks_like_story(chip: str) -> bool:
    """Material origin narratives must not become 'why I chose / what is hard' etc."""
    c = (chip or "").strip()
    if not c:
        return False
    words = c.split()
    if len(words) >= 8:
        return True
    cl = c.lower()
    story_marks = (
        "when i ",
        "after i ",
        "before i ",
        "my parents",
        "my mum",
        "my dad",
        "classmate",
        "bought me",
        "moved into",
        "booked",
        "stuck",
        "gave me",
    )
    return any(m in cl for m in story_marks)


# Intents where the supporting step must answer the question, not retell a life-story origin
_Q_FIT_INTENTS = frozenset(
    {
        "work_or_student",
        "why_choose",
        "challenging",
        "typical_day",
        "future_plan",
        "like_most",
    }
)


def _feel_clause(feel: str) -> str:
    """PDF feels are often full verb phrases ('helps me chill out')."""
    f = (feel or "practical").strip()
    fl = f.lower()
    if fl.startswith("feel "):
        f = f[5:].strip()
        fl = f.lower()
    if fl.startswith(("help", "make", "give", "is ", "are ", "lets ", "keep", "it ")):
        return f if fl.startswith("it ") else f"it {f}"
    return f"it feels {f}"


def _find_feel(feel: str) -> str:
    f = (feel or "practical").strip()
    fl = f.lower()
    if fl.startswith("feel "):
        f = f[5:].strip()
        fl = f.lower()
    if fl.startswith(("help", "make", "give", "is ", "are ", "lets ", "keep")):
        return f"I find that it {f}"
    if fl.startswith("it "):
        return f"I find that {f}"
    return f"I find it {f}"


def _example_clause(chip: str) -> str:
    c = (chip or "this").strip()
    # Full-sentence origin chips already capitalised
    if len(c.split()) >= 8 and c[:1].isupper():
        return c
    return f"For example, {c[0].lower() + c[1:] if c[:1].isupper() and not c.lower().startswith(('a ', 'an ', 'the ', 'my ')) else c}"


def _chip_in(chip: str, text_l: str) -> bool:
    cl = (chip or "").lower().strip()
    if not cl:
        return True
    if cl in text_l:
        return True
    parts = [p for p in re.findall(r"[a-zA-Z']+", cl) if len(p) > 3]
    if not parts:
        return len(cl) >= 3 and cl[:3] in text_l
    return sum(1 for p in parts if p.lower() in text_l) >= max(1, (len(parts) + 1) // 2)


def _pick(options: list[str], seed: int) -> str:
    if not options:
        return ""
    return options[int(seed) % len(options)]


def _open_for_q(q: str, mat: dict[str, Any], cat_id: str, pack: dict[str, Any] | None = None) -> list[str]:
    steps = CAT_STEPS.get(cat_id) or CAT_STEPS["shishi"]
    if pack and pack.get("words") and pack["words"].get(steps[0]):
        return list(pack["words"][steps[0]])[:3]

    ql = q.lower().strip()
    intent = detect_intent(q)
    opens = mat.get("open") or {}
    yes = list(opens.get("yes") or ["Yes, I do", "Yes", "Most of the time"])
    kind = list(opens.get("kind") or yes)
    prefer = list(opens.get("prefer") or prefer_fallback(kind))

    # Intent first — never answer "challenging" with a library nickname
    if intent == "work_or_student":
        return ["I'm a student", "I'm studying", "Not working yet"]
    if intent == "why_choose":
        return ["I chose business", "It matches my strengths", "For my future career"]
    if intent == "challenging":
        return ["Balancing assignments", "Exams and deadlines", "Time management"]
    if intent == "typical_day":
        return ["Morning classes first", "Busy on campus", "Classes then the library"]
    if intent == "future_plan":
        return ["Finish my degree", "Start an internship", "A business-related role"]
    if intent == "like_most":
        return [
            "Learning with classmates",
            "One thing I like to do in my free time is related to my studies",
            "Group projects",
        ]
    if intent == "live_wish":
        return ["Yes, I would", "Maybe for a while", "I am still deciding"]
    if intent == "home_wish":
        housing = [k for k in kind if any(x in (k or "").lower() for x in ("dorm", "apartment", "flat", "residential", "home"))]
        return (housing or kind or ["A quiet apartment", "A bright flat near campus", "Somewhere tidy and practical"])[:3]
    if intent == "science_wish":
        return ["Clean energy breakthroughs", "Space exploration progress", "Medical discoveries"]
    if intent == "travel_wish":
        return ["I would like coastal places", "Somewhere with nature", "A quiet city abroad"]
    if intent == "do_when":
        # Answer with an action; never a place/object nickname alone
        if "rubbish" in ql or "recycl" in ql or "garbage" in ql:
            return ["I pick it up if I can", "I put it into a recycling bin", "I sort it when possible"]
        if "tired" in ql:
            return ["I take a short walk", "I listen to music", "I take a quick break"]
        if "bored" in ql:
            return ["I go for a walk", "I watch something light", "I scroll short videos briefly"]
        act = kind[0] if kind else "a short break"
        return [f"I usually turn to {act}", f"I try {act}", "I take a short break"]
    if "social media" in ql or ("which" in ql and "app" in ql):
        return ["WeChat and Xiaohongshu", "Mostly WeChat", "Short-video apps"]
    if "listen to" in ql and "headphone" in ql:
        return ["Music playlists", "Happy songs", "Mostly music"]
    if intent == "how_often":
        return ["Quite often", "As often as I can", "From time to time"]
    if ql.startswith("how long"):
        return ["For several years", "Since childhood", "Quite a long time"]
    if "where did you go on holiday" in ql:
        return ["I went to nearby cities", "We visited coastal towns", "Mostly short city trips"]
    if "where is your hometown" in ql:
        return ["It is a small city nearby", "In my home province", "Not far from here"]
    if "sitting by the window" in ql:
        return ["I prefer sitting by the window", "A window seat", "Yes, by the window"]
    if ql.startswith("where "):
        return ["Near my home", "In my city", "On campus"]
    if ql.startswith("who ") and "funniest" in ql:
        return ["My roommate", "One of my classmates", "My younger cousin"]
    if ql.startswith("who "):
        return ["My parents", "My close friends", "My teachers"]
    if intent == "why":
        return ["For a few clear reasons", "Mainly because it fits me", "Because it works for me"]
    if intent == "prefer" or (cat_id == "duibi" and " or " in ql):
        return prefer[:3] or yes[:3]
    if "have you ever" in ql:
        return ["Yes, I have", "Yes, once", "Definitely"]
    if intent == "childhood":
        return ["Yes, I remember", "It was quite simple then", "Yes, back then"]
    if ql.startswith("when do you") or ql.startswith("when are you"):
        return ["In the evening", "After a long day", "When I am free"]
    if ql.startswith("when "):
        return ["A few years ago", "In primary school", "Last year"]
    if ql.startswith("what kind") or ql.startswith("what type") or ql.startswith("which kind"):
        return kind[:3]
    if "favourite" in ql or "favorite" in ql:
        return [f"My favourite is linked to {kind[0]}", f"I like {kind[0]} most", "I have a clear favourite"]
    if "changed" in ql or "change" in ql:
        return ["They have changed a lot", "There is a clear difference now", "Yes, quite a bit"]
    if "what do you usually do at home" in ql or "what do you do at home" in ql:
        return ["I tidy up a bit", "I rest and study", "I stay in and recharge"]
    if "post online" in ql:
        return ["Short updates on WeChat", "Funny clips", "Study notes sometimes"]
    if "people often do on social media" in ql or "people usually do on social media" in ql:
        return ["They browse short videos", "They chat and share posts", "They follow creators"]
    if "buy on the street market" in ql:
        return ["Fresh fruit", "Local snacks", "Small daily items"]
    if "usually do at the weekend" in ql or "do at the weekend" in ql:
        return ["They hang out and eat out", "They walk in parks", "They visit family"]
    if ql.startswith("what ") or ql.startswith("which "):
        return kind[:3] if kind else ["A few clear points", "Several things matter", "I can give a clear example"]
    if ql.startswith(("how did", "how do", "how have")) and intent != "opinion":
        return ["In a simple way", "Step by step", f"I usually start with {kind[0]}"]
    if ql.startswith(("do you", "does ", "are you", "is ", "did you", "have you", "would you")):
        return yes[:3]
    return yes[:3]


def prefer_fallback(kind: list[str]) -> list[str]:
    if not kind:
        return ["I'd rather choose the first", "I prefer the first option", "It depends"]
    return [f"I prefer {kind[0]}", f"I'd rather choose {kind[0]}", "It depends, but mostly the first"]


def _route_pair(mat: dict[str, Any], topic_q_index: int, seed: int) -> tuple[dict[str, str], dict[str, str]]:
    routes = list(mat.get("routes") or [{"freq": "every day", "feel": "practical", "impact": "makes life easier"}])
    i = (topic_q_index + seed) % len(routes)
    j = (i + 1) % len(routes)
    return routes[i], routes[j]


def _origin_pair(mat: dict[str, Any], topic_q_index: int, seed: int) -> tuple[str, str]:
    origins = list(mat.get("origins") or ["It started in my daily life"])
    i = (topic_q_index + seed) % len(origins)
    j = (i + 1) % len(origins)
    return origins[i], origins[j]


def _step_logic_line(cat_id: str) -> str:
    steps = CAT_STEPS.get(cat_id) or CAT_STEPS["shishi"]
    return " → ".join(steps)


def _action_label(mat: dict[str, Any], kind_list: list[str]) -> str:
    """Short noun/phrase for 时间线+行为描述 (avoid full 'I usually choose…' lines)."""
    for k in kind_list:
        kl = (k or "").lower().strip()
        if not kl:
            continue
        if kl.startswith(("i ", "i'd", "i’m", "i'm", "mostly", "something", "yes", "not ")):
            continue
        return k
    return (mat.get("id") or "this habit").replace("_", " ")


def build_words(
    cat_id: str,
    qtext: str,
    topic_en: str,
    topic_q_index: int = 0,
    kit_id: str | None = None,
) -> tuple[dict[str, list[str]], str, str, dict[str, Any]]:
    """Q-fit words first (online style); material only soft-tints freq/feel for kit switch."""
    from p1_word_banks import resolve_words

    steps = CAT_STEPS[cat_id]
    ids = material_ids_for_question(topic_en, qtext)
    mid = (kit_id or "").strip() or (ids[0] if ids else "")
    mats = materials_for_question(topic_en, qtext) or [{}]
    mat = get_material(mid) or mats[0]
    mid = mat.get("id") or mid
    seed = variant_seed_for(topic_en, qtext, topic_q_index)
    intent = detect_intent(qtext)

    words, logic, source = resolve_words(cat_id, qtext, steps, topic_en)
    words = {k: list(v or []) for k, v in (words or {}).items()}

    if mat and mat.get("routes"):
        r0, r1 = _route_pair(mat, topic_q_index, seed)
        o0, o1 = _origin_pair(mat, topic_q_index, seed)
        kind = list((mat.get("open") or {}).get("kind") or [])
        action = _action_label(mat, kind)
    else:
        r0 = {"freq": "every day", "feel": "practical", "impact": "helps me stay organised"}
        r1 = {"freq": "at weekends", "feel": "quite useful", "impact": "keeps my routine steady"}
        o0, o1, action = "", "", ""

    # Freestyle tint: kind into example/reason; freq/feel/impact into later steps
    ex_step = steps[1] if len(steps) > 1 else None
    freq_step = {"shishi": steps[2], "xihao": steps[2], "xingwei": steps[2]}.get(cat_id)
    feel_step = {"shishi": steps[3], "xihao": steps[3], "guandian": steps[3], "duibi": steps[3]}.get(cat_id)
    impact_step = {"xingwei": steps[3], "guandian": steps[2]}.get(cat_id)

    def _merge_tail(step: str | None, extras: list[str], *, allow_story: bool = False) -> None:
        if not step:
            return
        base = list(words.get(step) or [])
        merged: list[str] = []
        for c in list(extras) + base:
            if not c or c in merged:
                continue
            if not allow_story and _looks_like_story(c):
                continue
            merged.append(c)
            if len(merged) >= 4:
                break
        if merged:
            words[step] = merged

    _merge_tail(ex_step, list(kind[:2]) + ([action] if action else []))
    _merge_tail(freq_step, [r0.get("freq") or "", r1.get("freq") or ""])
    _merge_tail(feel_step, [r0.get("feel") or "", r1.get("feel") or ""])
    _merge_tail(impact_step, [r0.get("impact") or "", r1.get("impact") or ""])

    material = f"{(mat.get('nameZh') or mid)}：{(mat.get('summary') or '')}"
    if not logic:
        logic = f"先扣题回答，再按「{_step_logic_line(cat_id)}」展开；换素材会换举例/频次/感受。"
    else:
        logic = f"{logic} 素材【{mat.get('nameZh') or mid}】润色举例与频次/感受，不改题型四步。"

    meta = {
        "kitId": mid,
        "primaryKitId": ids[0] if ids else mid,
        "kitNameZh": mat.get("nameZh") or mid,
        "kitSummary": mat.get("summary") or "",
        "kitSlice": list(words.get(steps[1]) or [])[:1]
        + list(words.get(steps[2]) or [])[:1]
        + list(words.get(steps[3]) or [])[:1],
        "kitRest": [x for x in (o0, r0.get("freq"), r0.get("feel")) if x][:3],
        "angle": mat.get("kind") or "",
        "origin": o0,
        "originAlt": o1,
        "route": r0,
        "routeAlt": r1,
        "kind": action,
        "reason": (words.get(steps[1]) or [""])[0],
        "reasonAlt": (words.get(steps[1]) or ["", ""])[1] if len(words.get(steps[1]) or []) > 1 else "",
        "intent": intent,
        "wordSource": source,
        "packSample": "",
    }
    return words, logic, material, meta


def build_sample(
    cat_id: str,
    qtext: str,
    topic_en: str,
    words: dict[str, list[str]],
    variant_seed: int = 0,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prefer online-style generate_sample / hand / pack; never material-story templates."""
    from p1_sample_answers import generate_sample
    from p1_sample_zh import translate_sample

    meta = meta or {}
    steps = CAT_STEPS[cat_id]
    frames = resolve_frames(cat_id, qtext, variant_seed=variant_seed)
    result = generate_sample(
        cat_id,
        qtext,
        steps,
        words,
        frames,
        kit_id=str(meta.get("kitId") or ""),
        meta=meta,
    )
    text = result.get("text") or ""
    intent = meta.get("intent") or detect_intent(qtext)
    sample_zh = translate_sample(text, intent=intent, cat_id=cat_id, meta=meta)
    return {
        "text": text,
        "zh": sample_zh,
        "ok": bool(result.get("ok")),
        "note": result.get("note") or "ok",
        "source": result.get("source") or "template",
    }


def align_question(
    cat_id: str,
    qtext: str,
    topic_en: str,
    topic_q_index: int = 0,
    kit_id: str | None = None,
) -> dict[str, Any]:
    from p1_freestyle_packs import get_pack  # local import avoids cycles

    seed = variant_seed_for(topic_en, qtext, topic_q_index)
    ids = material_ids_for_question(topic_en, qtext)
    active = (kit_id or "").strip() or (ids[0] if ids else "")
    words, logic, material, meta = build_words(
        cat_id, qtext, topic_en, topic_q_index=topic_q_index, kit_id=active
    )
    active = meta.get("kitId") or active
    frames = resolve_frames(cat_id, qtext, variant_seed=seed)
    sample = build_sample(cat_id, qtext, topic_en, words, variant_seed=seed, meta=meta)
    slice_bits = meta.get("kitSlice") or []
    rest_bits = meta.get("kitRest") or []
    kit_hint = (
        f"当前素材【{meta.get('kitNameZh') or active}】·"
        f"{_step_logic_line(cat_id)}。"
        f"本题用：{' / '.join(slice_bits[:3]) or '开场表态'}"
        + (f"。同素材还可说：{' / '.join(rest_bits[:3])}" if rest_bits else "")
    )

    # Preview-style curated pack wins: clear logic + distinct sample per kit
    pack = get_pack(qtext, active)
    if pack:
        if pack.get("words"):
            words = pack["words"]
        if pack.get("logic"):
            logic = pack["logic"]
        if pack.get("kitHint"):
            kit_hint = pack["kitHint"]
        if pack.get("sample"):
            sample = {
                "text": " ".join(str(pack["sample"]).split()),
                "zh": pack.get("sampleZh") or sample.get("zh") or "",
                "ok": True,
                "note": "ok",
                "source": "freestyle-pack",
            }
        material = f"{meta.get('kitNameZh') or active}：{meta.get('kitSummary') or pack.get('kitHint') or ''}"

    return {
        "words": words,
        "logic": logic,
        "material": material,
        "frames": frames,
        "frameVariant": seed % 3,
        "sample": sample["text"],
        "sampleZh": sample.get("zh") or "",
        "sampleOk": sample["ok"],
        "sampleNote": sample["note"],
        "sampleSource": sample["source"],
        "wordSource": "freestyle-pack" if pack else "material-bank",
        "kitId": active,
        "kitIds": ids,
        "kitNameZh": meta.get("kitNameZh") or active,
        "kitSummary": meta.get("kitSummary") or "",
        "kitHint": kit_hint,
        "kitSlice": slice_bits,
        "kitRest": rest_bits,
        "kitAngle": meta.get("angle") or "",
    }


def align_question_all_kits(
    cat_id: str,
    qtext: str,
    topic_en: str,
    topic_q_index: int = 0,
) -> dict[str, Any]:
    ids = material_ids_for_question(topic_en, qtext)
    primary = align_question(cat_id, qtext, topic_en, topic_q_index, kit_id=ids[0] if ids else None)
    variants: dict[str, Any] = {}
    for kid in ids:
        aligned = align_question(cat_id, qtext, topic_en, topic_q_index, kit_id=kid)
        variants[kid] = {
            "words": aligned["words"],
            "sample": aligned["sample"],
            "sampleZh": aligned.get("sampleZh") or "",
            "sampleOk": aligned["sampleOk"],
            "logic": aligned["logic"],
            "material": aligned["material"],
            "kitHint": aligned["kitHint"],
            "kitNameZh": aligned["kitNameZh"],
            "kitSummary": aligned["kitSummary"],
            "kitSlice": aligned["kitSlice"],
            "kitRest": aligned["kitRest"],
            "frames": aligned["frames"],
            "frameVariant": aligned["frameVariant"],
        }
    primary["kitVariants"] = variants
    return primary
