#!/usr/bin/env python3
"""Add ______ placeholders to listening synonym questions missing blanks."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLANK_FIXES = {
    10: (
        "Since they felt their work was useful, almost all of them said that volunteering "
        "made them feel more motivated at their jobs — ______"
    ),
    17: "This type of exercise is open to everyone — ______.",
    23: (
        "And people often don't understand at first that ______ — it takes real drive "
        "and hard work to train every week."
    ),
    26: (
        "What worries us, however, is the overall increase in the amount of traffic "
        "of every type — ______"
    ),
    32: (
        "The more attention you pay to something while it's happening, the more "
        "successfully you can store it in your memory — ______"
    ),
    34: (
        "How often you try to recall a memory affects how strong that memory becomes — ______"
    ),
    35: (
        "For instance, to remember where you ______ your car, you might use the colour "
        "of a sign near to the parking spot."
    ),
    37: (
        "This might happen because the ______ of self is absent — they lack a clear "
        "sense of who they are."
    ),
    50: "A number of the artists each ______ one piece of work as a donation.",
    74: (
        "We might need to put some rules in place, such as ______ — staying on the "
        "marked routes."
    ),
    80: "They would ______ a new building for her — a whole new house.",
    86: "A place where ______ — you can take a quick dip in the sea.",
    92: (
        "The amount required is climbing fast, driven by growth in population and "
        "industry around the world — ______"
    ),
    93: (
        "The trouble with ocean waves is they're unpredictable — the wind makes them "
        "______ in any direction."
    ),
    100: (
        "Astronomers had created a calendar that split the year into 24 festivals, "
        "each one ______ a different weather event."
    ),
    101: (
        "However, by the 1400s, scientists ______ the value of instruments — they saw "
        "that tools were needed."
    ),
    103: (
        "Franklin was the one who ______ the movement of storms — he found that they "
        "usually go from west to east."
    ),
    105: "______ I trained in the Finance department.",
    113: (
        "Do you take any medicine on a regular basis? ______ vitamins, no — that's "
        "everything."
    ),
}


def extract_json_array(text: str, var_name: str):
    match = re.search(r"const\s+" + re.escape(var_name) + r"\s*=\s*", text)
    if not match:
        raise ValueError(f"Could not find {var_name}")
    start = match.end()
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : index + 1]), start, index + 1
    raise ValueError(f"Unterminated JSON array for {var_name}")


def update_questions(questions, *, is_groups: bool = False) -> int:
    updated = 0
    items = (
        (question for group in questions for question in group)
        if is_groups
        else questions
    )
    for question in items:
        question_id = question["id"]
        if question_id in BLANK_FIXES:
            question["blank"] = BLANK_FIXES[question_id]
            updated += 1
    return updated


def patch_file(path: Path, var_name: str, *, is_groups: bool = False) -> int:
    text = path.read_text(encoding="utf-8")
    data, start, end = extract_json_array(text, var_name)
    updated = update_questions(data, is_groups=is_groups)
    new_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text[:start] + new_json + text[end:], encoding="utf-8")
    return updated


def verify(path: Path, var_name: str, *, is_groups: bool = False) -> list[int]:
    data, _, _ = extract_json_array(path.read_text(encoding="utf-8"), var_name)
    questions = [question for group in data for question in group] if is_groups else data
    return [question["id"] for question in questions if "______" not in question.get("blank", "")]


def main() -> None:
    study = ROOT / "sources" / "daanjutingxie" / "index.html"
    test = ROOT / "sources" / "daanjutingxieceshi" / "index.html"
    print("study updated", patch_file(study, "GROUPS", is_groups=True))
    print("test updated", patch_file(test, "ALL_QUESTIONS"))
    print("study remaining", verify(study, "GROUPS", is_groups=True))
    print("test remaining", verify(test, "ALL_QUESTIONS"))


if __name__ == "__main__":
    main()
