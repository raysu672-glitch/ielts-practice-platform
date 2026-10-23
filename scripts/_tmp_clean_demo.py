import sqlite3

c = sqlite3.connect("data/_stage_test_demo.db")
for sql in (
    "DELETE FROM students WHERE student_id='2025001'",
    "DELETE FROM plan_items WHERE student_id='2025001'",
    "DELETE FROM plan_items_draft WHERE student_id='2025001'",
    "DELETE FROM daily_tasks WHERE student_id='2025001'",
    "DELETE FROM task_unit_progress WHERE student_id='2025001'",
    "DELETE FROM student_time_profiles WHERE student_id='2025001'",
    "DELETE FROM student_module_daily_quota WHERE student_id='2025001'",
):
    c.execute(sql)
c.commit()
print("remaining students:", c.execute("SELECT COUNT(*) FROM students").fetchone()[0])
