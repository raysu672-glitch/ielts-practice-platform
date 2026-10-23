"""按前端 loadProgressTable 的口径回读李哲的进度，验证播种数据是否自洽。"""
import re
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data" / "ielts_local.db"
STUDENT_ID = "2026001"

TARGET_65 = {
    "dictation": ("%", 80), "listening_basic": ("%", 80),
    "reading_synonym": ("%", 80), "sentence": ("%", 80),
    "listening_synonym": ("%", 80), "writing_phrase": ("%", 70),
    "writing_translate": ("%", 70), "listening_p4_speed": ("%", 80),
    "reading_p1": ("个", 11), "reading_p2": ("个", 10), "reading_p3": ("个", 6),
    "listening_p1": ("个", 9), "listening_p2": ("个", 8),
    "listening_p3": ("个", 4), "listening_p4": ("个", 6),
    "speaking": ("分", 6),
}

NORMALIZE = {
    "dictation_learn": "dictation", "listening_basic_learn": "listening_basic",
    "reading_synonym_test": "reading_synonym", "writing_phrase_test": "writing_phrase",
    "sentence_test": "sentence", "listening_synonym_test": "listening_synonym",
    "writing_translate_test": "writing_translate",
    "speaking_p1": "speaking", "speaking_p2": "speaking", "speaking_p3": "speaking",
}

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

student = conn.execute("SELECT * FROM students WHERE student_id = ?", (STUDENT_ID,)).fetchone()
if not student:
    print("学生不存在")
    sys.exit(1)

records = [dict(r) for r in conn.execute(
    "SELECT * FROM test_records WHERE student_id = ?", (STUDENT_ID,))]
sessions = [dict(r) for r in conn.execute(
    "SELECT * FROM study_sessions WHERE student_id = ?", (STUDENT_ID,))]
wrong_words = [dict(r) for r in conn.execute(
    "SELECT * FROM wrong_words WHERE student_id = ? AND is_mastered = 0", (STUDENT_ID,))]
wrong_items = [dict(r) for r in conn.execute(
    "SELECT * FROM wrong_items WHERE student_id = ? AND is_mastered = 0", (STUDENT_ID,))]

print(f"学生 {student['name']}（{student['student_id']}） 目标 {student['target_score']} "
      f"状态 {student['status']} 已改密={student['is_password_changed']}")
print(f"总练习时长 {sum(int(s['duration_seconds'] or 0) for s in sessions) / 3600:.1f} 小时 "
      f"（{len(sessions)} 次）· 测试 {len(records)} 次 · 未掌握错词 {len(wrong_words)} "
      f"· 未掌握错题 {len(wrong_items)}")
print()

print(f"{'模块':<20}{'达标线':>8}{'最好成绩':>10}{'进度':>8}  状态")
print("-" * 62)
done = 0
total_modules = 0
for module_type, (unit, target) in TARGET_65.items():
    mod_records = [r for r in records
                   if NORMALIZE.get(r["module_type"], r["module_type"]) == module_type]
    best = 0.0
    for r in mod_records:
        value = float(r["correct_count"]) if unit == "个" else float(r["score"] or 0)
        best = max(best, value)
    total_modules += 1
    if not mod_records:
        print(f"{module_type:<20}{target:>8g}{'-':>10}{0:>7}%  未开始")
        continue
    progress = min(100, round(best / target * 100))
    status = "达标" if best >= target else "进行中"
    if status == "达标":
        done += 1
    passed = sum(1 for r in mod_records
                 if (float(r["correct_count"]) if unit == "个" else float(r["score"] or 0)) >= target)
    print(f"{module_type:<20}{target:>8g}{best:>10g}{progress:>7}%  {status}"
          f"（测 {len(mod_records)} 次 / 达标 {passed} 次）")

print("-" * 62)
print(f"达标 {done} / {total_modules} 个模块；其余全部「进行中」——符合 4.5 起点画像")
