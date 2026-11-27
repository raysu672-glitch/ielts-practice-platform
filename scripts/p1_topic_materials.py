# -*- coding: utf-8 -*-
"""
Per-question packs for high-stakes Work or studies items.
Vocabulary aligned with classroom PDF《P1素材》(go to classes / library / future job).
"""
from __future__ import annotations

from typing import Any

from p1_word_banks_core import norm_q

_WS_MAT = "学生线：business major · go to classes · library · future job（PDF 衣食住行+学习行为）"
_WS_LOGIC = "先扣题，再套 PDF 素材：I'm a student → business major / go to classes / library → every weekday → useful for my future job。"

TOPIC_QUESTION_PACKS: dict[str, dict[str, Any]] = {}


def _pack(q: str, cat: str, words: dict[str, list[str]], sample: str, logic: str = _WS_LOGIC, material: str = _WS_MAT) -> None:
    TOPIC_QUESTION_PACKS[norm_q(q)] = {
        "cat": cat,
        "words": words,
        "sample": " ".join(sample.split()),
        "logic": logic,
        "material": material,
        "source": "topic-pack",
    }


def _build_work_studies() -> None:
    _pack(
        "Do you work or are you a student?",
        "shishi",
        {
            "正面回答": ["I'm a student", "I'm studying", "Not working yet"],
            "来源或举例": ["business major", "go to classes", "on campus", "library"],
            "频次": ["every weekday", "in my spare time", "at weekends"],
            "感受": ["practical", "useful for my future job", "quite useful"],
        },
        "I'm a full-time student at university. I major in business and attend classes on campus every weekday. "
        "When I am free, I also finish assignments in the library. "
        "I find this student routine practical for my future career.",
    )
    _pack(
        "Why did you choose that job or that subject?",
        "shishi",
        {
            "正面回答": ["I chose business", "It matches my strengths", "For my future job"],
            "来源或举例": ["matches my strengths", "future job", "related courses"],
            "频次": ["every weekday", "in my spare time", "every day"],
            "感受": ["practical", "useful for my future job", "quite useful"],
        },
        "I chose my subject for the reason that it matches my strengths and leads to clearer career options. "
        "Since I want useful skills, I take related courses every weekday and review notes at weekends. "
        "I find the choice practical and quite useful.",
    )
    _pack(
        "What do you find most challenging about your work or your studies?",
        "shishi",
        {
            "正面回答": ["Balancing assignments", "Exams", "Deadlines"],
            "来源或举例": ["assignments", "exams", "library", "deadlines"],
            "频次": ["every weekday", "near exam week", "at weekends"],
            "感受": ["stressful at times", "makes me more organised", "still practical"],
        },
        "Balancing assignments is the hardest part. Deadlines pile up with exams in the library, which is tough. "
        "This happens every weekday near exam week. "
        "I find it stressful at times, but it also makes me more organised.",
    )
    _pack(
        "What do you like most about your job or your studies?",
        "xihao",
        {
            "正面回答": ["Learning with classmates", "Group projects", "Business classes"],
            "原因或时间": ["share opinions", "real cases", "on campus"],
            "频次": ["every week", "every weekday", "in my spare time"],
            "感受": ["makes me happy", "useful for my future job", "helps to light up my mood"],
        },
        "Learning with classmates is what I like most. "
        "I am keen on group projects for the reason that we share opinions about real cases on campus. "
        "We do this every week after business classes. "
        "I find this activity enjoyable, which is useful for my future job.",
    )
    _pack(
        "What is a typical day like for you at work or at school?",
        "xihao",
        {
            "正面回答": ["Morning classes first", "Busy on campus", "Library after lunch"],
            "原因或时间": ["go to classes", "library", "assignments"],
            "频次": ["every weekday", "after lunch", "in the evening"],
            "感受": ["busy but practical", "useful for my future job", "quite useful"],
        },
        "Morning classes come first on a typical school day. "
        "I go to classes on campus, then use the library after lunch for the reason that I need quiet time. "
        "In the evening every weekday I finish assignments. "
        "I find this routine busy but practical, which is useful for my future job.",
    )
    _pack(
        "What would you like to be doing in your career or studies in a few years?",
        "xihao",
        {
            "正面回答": ["Finish my degree", "Start an internship", "A business-related role"],
            "原因或时间": ["business major", "work experience", "related courses"],
            "频次": ["in a few years", "after I graduate", "every weekday until then"],
            "感受": ["realistic", "useful for my future job", "practical"],
        },
        "I would like to finish my degree and start an internship. "
        "I plan to use my business major and related courses to build work experience. "
        "After I graduate in a few years, I hope to enter a business-related role. "
        "I find that plan realistic and useful for my future job.",
    )


_build_work_studies()


def get_question_pack(qtext: str) -> dict[str, Any] | None:
    return TOPIC_QUESTION_PACKS.get(norm_q(qtext))
