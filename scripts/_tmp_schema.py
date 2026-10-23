import sqlite3

c = sqlite3.connect("data/ielts_local.db")
print("students cols:", [d[1] for d in c.execute("PRAGMA table_info(students)")])
print()
print("tables:")
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print("  ", r[0])
