"""为产品测试播种一个模拟学生：李哲（大一，高考英语 100/150，雅思目标 6.5）。

人物设定与逐项评估见 canvases/student-profile-li-zhe.canvas.tsx。
本脚本把这个学生真的写进本地 SQLite：学号、目标分、各模块测试记录、
练习时长、错题本、单词掌握、口语历史分、时间偏好。

对齐口径（与前端一致）
--------------------
- 达标线按学生 target_score 取 pass_standards 的 score_6 / score_6_5 / score_7 列；
  李哲目标 6.5，因此走 score_6_5。
- 阅读 / 听力 Part 1-4 属于「计数模块」：test_records.score 存的是答对个数，
  达标判定用 correct_count >= pass_threshold。
- 其余模块 score 存百分比；口语存 Band 分。

用法
----
    python scripts/seed_mock_student.py                    # 预览，不写库
    python scripts/seed_mock_student.py --apply            # 写库（学号已存在则报错）
    python scripts/seed_mock_student.py --apply --reset    # 先清空该学号旧数据再写
    python scripts/seed_mock_student.py --db path/to.db --student-id 2026001
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from password_utils import STUDENT_INITIAL_PASSWORD, hash_password  # noqa: E402

DEFAULT_DB = ROOT / "data" / "ielts_local.db"

try:  # Windows 控制台默认 GBK，避免中文打印炸掉
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass


STUDENT_ID = "2026001"
STUDENT_NAME = "李哲"
TARGET_SCORE = 6.5
PASSWORD_CHANGED = 0  # 0 = 首次登录强制改密码，与平台新建学生一致

FIRST_STUDY_DAY = "2026-09-01"
LAST_STUDY_DAY = "2026-09-18"

# (module_type, module_name, 最好成绩, 首测成绩, 题量, 达标线)
PERCENT_TESTS = [
    ("dictation", "听力1000词", 58.0, 45.0, 20, 80.0),
    ("listening_basic", "听力基础词汇", 62.0, 50.0, 20, 80.0),
    ("listening_synonym", "听力同义替换", 32.0, 24.0, 10, 80.0),
    ("listening_p4_speed", "听力P4跟读练习", 40.0, 33.0, 1, 80.0),
    ("reading_synonym", "阅读同义替换", 35.0, 28.0, 20, 80.0),
    ("sentence", "长难句分析", 30.0, 22.0, 10, 80.0),
    ("writing_phrase", "写作词伙", 18.0, 12.0, 10, 70.0),
    ("writing_translate", "写作句子翻译", 22.0, 15.0, 10, 70.0),
]

# (module_type, module_name, 最好答对, 首测答对, 总题量, 达标线=目标答对个数)
COUNT_TESTS = [
    ("reading_p1", "阅读Part1", 5, 3, 13, 11.0),
    ("reading_p2", "阅读Part2", 3, 2, 13, 10.0),
    ("reading_p3", "阅读Part3", 2, 1, 14, 6.0),
    ("listening_p1", "听力Part1", 4, 3, 10, 9.0),
    ("listening_p2", "听力Part2", 4, 3, 10, 8.0),
    ("listening_p3", "听力Part3", 2, 1, 10, 4.0),
    ("listening_p4", "听力Part4", 2, 2, 10, 6.0),
]

SPEAKING = {
    "module_type": "speaking",
    "module_name": "口语练习",
    "best": 4.0,
    "first": 3.5,
    "threshold": 6.0,
    "questions": [
        "Do you work or are you a student?",
        "Where are you from?",
        "Do you like your hometown?",
        "What do you usually do at weekends?",
    ],
}

# (module_type, module_name, 每次分钟数, 次数)
STUDY_PLAN = [
    ("dictation", "听力1000词", 35, 7),
    ("listening_basic", "听力基础词汇", 25, 4),
    ("listening_synonym", "听力同义替换", 25, 4),
    ("reading_synonym", "阅读同义替换", 30, 6),
    ("sentence", "长难句分析", 30, 5),
    ("writing_phrase", "写作词伙", 20, 3),
    ("writing_translate", "写作句子翻译", 20, 3),
    ("speaking", "口语练习", 20, 5),
    ("reading_p1", "阅读Part1", 25, 2),
    ("listening_p1", "听力Part1", 20, 2),
]

# 错词（听力 1000 词 / 听力基础词汇）
WRONG_WORDS = [
    ("dictation", "accommodation", 3, 0),
    ("dictation", "questionnaire", 2, 0),
    ("dictation", "itinerary", 2, 0),
    ("dictation", "vegetarian", 2, 1),
    ("dictation", "deposit", 1, 0),
    ("dictation", "receipt", 2, 0),
    ("dictation", "laundry", 1, 1),
    ("dictation", "landlord", 1, 0),
    ("listening_basic", "colleague", 2, 0),
    ("listening_basic", "pharmacy", 1, 0),
    ("listening_basic", "discount", 2, 1),
    ("listening_basic", "insurance", 1, 0),
]

# 错题（非单词类模块）
WRONG_ITEMS = [
    ("reading_synonym", "substantial", "substantial → considerable", {"answer": "considerable"}),
    ("reading_synonym", "decline", "decline → decrease", {"answer": "decrease"}),
    ("reading_synonym", "crucial", "crucial → vital", {"answer": "vital"}),
    ("reading_synonym", "mitigate", "mitigate → reduce", {"answer": "reduce"}),
    ("sentence", "s-014", "让步状语从句嵌套定语从句", {"answer": "拆分主干"}),
    ("sentence", "s-027", "that 引导的同位语从句", {"answer": "识别同位语"}),
    ("listening_synonym", "ls-003", "book → reserve", {"answer": "reserve"}),
    ("listening_synonym", "ls-011", "free → complimentary", {"answer": "complimentary"}),
    ("writing_phrase", "wp-006", "缓解压力", {"answer": "relieve stress"}),
    ("writing_phrase", "wp-017", "承担后果", {"answer": "bear the consequences"}),
    ("writing_translate", "wt-004", "越来越多的人开始关注环境问题。", {"answer": "A growing number of people ..."}),
]

# 单词掌握记录 (word, correct_count, wrong_count, is_initial_correct)
WORD_MASTERY = [
    ("accommodation", 2, 3, 0),
    ("questionnaire", 1, 2, 0),
    ("receipt", 2, 2, 0),
    ("colleague", 3, 2, 0),
    ("itinerary", 1, 2, 0),
    ("environment", 5, 0, 1),
    ("government", 5, 0, 1),
    ("university", 5, 0, 1),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def as_stamp(day: str, hour: int, minute: int) -> str:
    return f"{day}T{hour:02d}:{minute:02d}:00.000Z"


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


RESET_TABLES = [
    "test_records",
    "study_sessions",
    "wrong_words",
    "wrong_items",
    "word_mastery",
    "speaking_best_scores",
    "student_time_profiles",
    "student_attention_state",
    "student_attention_events",
    "student_module_daily_quota",
    "student_plan_pause",
    "gendu_practice_events",
    "daily_tasks",
    "plan_items",
    "plan_items_draft",
    "plan_draft_meta",
    "task_unit_progress",
    "jianya_drafts",
    "jianya_submissions",
    "jianya_recipients",
    "jianya_reviews",
    "mock_speaking_exams",
]


def reset_student(conn: sqlite3.Connection, student_id: str) -> list[str]:
    touched: list[str] = []
    for table in RESET_TABLES:
        if not table_exists(conn, table):
            continue
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if "student_id" not in cols:
            continue
        cur = conn.execute(f"DELETE FROM {table} WHERE student_id = ?", (student_id,))
        if cur.rowcount:
            touched.append(f"{table}({cur.rowcount})")
    cur = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    if cur.rowcount:
        touched.append("students(1)")
    conn.commit()
    return touched


def build_test_records(student_id: str) -> list[tuple]:
    """返回待插入 test_records 的行元组（无 id）。"""
    now = utc_now()
    rows: list[tuple] = []

    def add(module_type, module_name, score, correct, total, passed, threshold,
            day, duration, details):
        rows.append(
            (
                student_id, module_type, module_name, "module_test", float(score),
                int(correct), int(total), 1 if passed else 0, float(threshold),
                int(duration), json.dumps(details, ensure_ascii=False),
                as_stamp(day, 20, 10), as_stamp(day, 20, 10 + max(1, duration // 60)),
                now,
            )
        )

    # 首测 → 复测：两次记录，最好成绩落在复测上
    schedule = [
        (PERCENT_TESTS[0], "2026-09-02", "2026-09-15"),
        (PERCENT_TESTS[1], "2026-09-03", "2026-09-16"),
        (PERCENT_TESTS[2], "2026-09-05", "2026-09-16"),
        (PERCENT_TESTS[3], "2026-09-11", None),
        (PERCENT_TESTS[4], "2026-09-04", "2026-09-15"),
        (PERCENT_TESTS[5], "2026-09-06", "2026-09-17"),
        (PERCENT_TESTS[6], "2026-09-08", "2026-09-17"),
        (PERCENT_TESTS[7], "2026-09-09", "2026-09-18"),
    ]
    for (module_type, module_name, best, first, total, threshold), d1, d2 in schedule:
        first_correct = round(first / 100 * total)
        best_correct = round(best / 100 * total)
        if d2:  # 测过两次：首测偏低，复测才是当前水平
            add(module_type, module_name, first, first_correct, total, first >= threshold,
                threshold, d1, 600, [])
            add(module_type, module_name, best, best_correct, total, best >= threshold,
                threshold, d2, 600, [])
        else:  # 只做过一次：这次测评就是当前水平
            add(module_type, module_name, best, best_correct, total, best >= threshold,
                threshold, d1, 600, [])

    count_schedule = {
        "reading_p1": ("2026-09-07", "2026-09-18"),
        "reading_p2": ("2026-09-07", None),
        "reading_p3": ("2026-09-12", None),
        "listening_p1": ("2026-09-04", "2026-09-18"),
        "listening_p2": ("2026-09-10", "2026-09-18"),
        "listening_p3": ("2026-09-13", None),
        "listening_p4": ("2026-09-14", None),
    }
    for module_type, module_name, best, first, total, threshold in COUNT_TESTS:
        d1, d2 = count_schedule[module_type]
        if d2:
            add(module_type, module_name, first, first, total, first >= threshold,
                threshold, d1, 1500, [])
            add(module_type, module_name, best, best, total, best >= threshold,
                threshold, d2, 1500, [])
        else:
            add(module_type, module_name, best, best, total, best >= threshold,
                threshold, d1, 1500, [])

    # 口语：一次 AI 评分记录，details 带题目与 Band 分
    details = [
        {"question": q, "overall": SPEAKING["first"] if i == 0 else SPEAKING["first"] + 0.5}
        for i, q in enumerate(SPEAKING["questions"])
    ]
    add(
        SPEAKING["module_type"], SPEAKING["module_name"], SPEAKING["best"],
        1, 4, SPEAKING["best"] >= SPEAKING["threshold"], SPEAKING["threshold"],
        "2026-09-18", 540, details,
    )
    return rows


def build_study_sessions(student_id: str) -> list[tuple]:
    now = utc_now()
    start = datetime.strptime(FIRST_STUDY_DAY, "%Y-%m-%d")
    last = datetime.strptime(LAST_STUDY_DAY, "%Y-%m-%d")
    days = [(start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((last - start).days + 1)]

    tasks: list[tuple[str, str, int]] = []
    for module_type, module_name, minutes, times in STUDY_PLAN:
        tasks.extend([(module_type, module_name, minutes)] * times)

    rows: list[tuple] = []
    day_index = 0
    slot_hours = [8, 13, 19, 21]
    for i, (module_type, module_name, minutes) in enumerate(tasks):
        if i and i % 2 == 0:
            day_index = min(day_index + 1, len(days) - 1)
        day = days[day_index]
        hour = slot_hours[i % len(slot_hours)]
        if module_type == "speaking":
            words_tested = 6 + (i % 4)
            details = [{"totalQuestions": 12}]
        else:
            words_tested = minutes // 2
            details = []
        rows.append(
            (
                student_id, module_type, module_name, "study",
                words_tested, max(0, words_tested - 3), min(3, words_tested),
                1, float(40 + (i * 7) % 45), minutes * 60,
                json.dumps(details, ensure_ascii=False),
                as_stamp(day, hour, 5),
                as_stamp(day, hour, 5 + minutes),
                now,
            )
        )
    rows.sort(key=lambda r: r[10])
    return rows


def insert_all(conn: sqlite3.Connection, student_id: str, name: str) -> dict[str, int]:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO students (
            student_id, name, password, is_password_changed, target_score,
            status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
        """,
        (
            student_id,
            name,
            hash_password(STUDENT_INITIAL_PASSWORD),
            PASSWORD_CHANGED,
            TARGET_SCORE,
            now,
            now,
        ),
    )

    test_rows = build_test_records(student_id)
    conn.executemany(
        """
        INSERT INTO test_records (
            student_id, module_type, module_name, test_type, score,
            correct_count, total_count, is_passed, pass_threshold,
            duration_seconds, details, started_at, ended_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        test_rows,
    )

    session_rows = build_study_sessions(student_id)
    conn.executemany(
        """
        INSERT INTO study_sessions (
            student_id, module_type, module_name, session_kind,
            words_tested, initial_correct, initial_wrong, groups_completed,
            score_percent, duration_seconds, details, started_at, ended_at, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        session_rows,
    )

    wrong_word_rows = [
        (student_id, module_type, word, wrong_count, 0, as_stamp("2026-09-17", 21, 0),
         1 if mastered else 0)
        for module_type, word, wrong_count, mastered in WRONG_WORDS
    ]
    conn.executemany(
        """
        INSERT INTO wrong_words (
            student_id, module_type, word, wrong_count, correct_streak,
            last_tested, is_mastered
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        wrong_word_rows,
    )

    wrong_item_rows = [
        (student_id, module_type, item_key, title,
         json.dumps(payload, ensure_ascii=False), 1, 0,
         as_stamp("2026-09-17", 21, 30), 0)
        for module_type, item_key, title, payload in WRONG_ITEMS
    ]
    conn.executemany(
        """
        INSERT INTO wrong_items (
            student_id, module_type, item_key, title, payload,
            wrong_count, correct_streak, last_tested, is_mastered
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        wrong_item_rows,
    )

    mastery_rows = [
        (student_id, word, "learning", correct_count, wrong_count,
         1 if initial_ok else 0, 1 if correct_count > wrong_count else 0,
         as_stamp("2026-09-17", 20, 40), now, now)
        for word, correct_count, wrong_count, initial_ok in WORD_MASTERY
    ]
    conn.executemany(
        """
        INSERT INTO word_mastery (
            student_id, word, status, correct_count, wrong_count,
            is_initial_correct, last_result, last_practiced_at, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        mastery_rows,
    )

    speaking_rows = []
    for i, question in enumerate(SPEAKING["questions"]):
        key = "".join(ch.lower() for ch in question if ch.isalnum())
        band = SPEAKING["first"] if i % 3 == 0 else SPEAKING["first"] + 0.5
        speaking_rows.append(
            (student_id, key, question, "p1", band, as_stamp("2026-09-18", 20, 30))
        )
    conn.executemany(
        """
        INSERT INTO speaking_best_scores (
            student_id, question_key, question_text, part, best_score, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        speaking_rows,
    )

    conn.execute(
        """
        INSERT INTO student_time_profiles (
            student_id, weekday_minutes, weekend_minutes, stage_test_every_n,
            pack_mode, updated_at
        ) VALUES (?, 90, 180, 3, 'units_per_day', ?)
        """,
        (student_id, now),
    )
    conn.commit()

    return {
        "students": 1,
        "test_records": len(test_rows),
        "study_sessions": len(session_rows),
        "wrong_words": len(wrong_word_rows),
        "wrong_items": len(wrong_item_rows),
        "word_mastery": len(mastery_rows),
        "speaking_best_scores": len(speaking_rows),
        "student_time_profiles": 1,
    }


def summarize(test_rows: list[tuple]) -> None:
    order = [
        t[1] for t in sorted(test_rows, key=lambda r: (r[1], -float(r[4])))
    ]
    seen: dict[str, float] = {}
    for row in test_rows:
        module_type, unit_score = row[1], row[4]
        if module_type not in seen or unit_score > seen[module_type]:
            seen[module_type] = unit_score
    print("  模块最好成绩：")
    for module_type in sorted(set(order)):
        print(f"    {module_type:<22} {seen[module_type]:g}")


def main() -> int:
    parser = argparse.ArgumentParser(description="播种模拟学生 李哲（大一，高考英语 100/150）")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="SQLite 路径")
    parser.add_argument("--student-id", default=STUDENT_ID, help="学号")
    parser.add_argument("--name", default=STUDENT_NAME, help="姓名")
    parser.add_argument("--apply", action="store_true", help="真正写库（默认只预览）")
    parser.add_argument("--reset", action="store_true", help="先清空该学号的旧数据")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"[ERROR] 数据库不存在：{args.db}")
        return 1

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    exists = conn.execute(
        "SELECT 1 FROM students WHERE student_id = ?", (args.student_id,)
    ).fetchone()
    if exists and not args.reset:
        print(f"[ERROR] 学号 {args.student_id} 已存在。加 --reset 可先清空后重建。")
        return 1

    plan = {
        "students": 1,
        "test_records": len(build_test_records(args.student_id)),
        "study_sessions": len(build_study_sessions(args.student_id)),
        "wrong_words": len(WRONG_WORDS),
        "wrong_items": len(WRONG_ITEMS),
        "word_mastery": len(WORD_MASTERY),
        "speaking_best_scores": len(SPEAKING["questions"]),
        "student_time_profiles": 1,
    }

    print(f"数据库：{args.db}")
    print(f"学生：{args.name}（{args.student_id}）· 目标 {TARGET_SCORE} · 初始密码 {STUDENT_INITIAL_PASSWORD}")
    print("将写入：")
    for key, value in plan.items():
        print(f"  {key:<24} {value}")
    summarize(build_test_records(args.student_id))

    if not args.apply:
        print("\n[dry-run] 未写库。加 --apply 执行。")
        return 0

    if args.reset:
        touched = reset_student(conn, args.student_id)
        print(f"\n[reset] 已清理：{', '.join(touched) if touched else '无旧数据'}")

    result = insert_all(conn, args.student_id, args.name)
    print("\n[applied] 写入完成：")
    for key, value in result.items():
        print(f"  {key:<24} {value}")
    print(
        "\n提示：首次登录会强制改密码（is_password_changed=0）。"
        f"学生端 /tinglidanciceshi/ → 学号 {args.student_id} / 密码 {STUDENT_INITIAL_PASSWORD}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
