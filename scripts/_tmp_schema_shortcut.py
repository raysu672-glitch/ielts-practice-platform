#!/usr/bin/env python3
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
c = sqlite3.connect(r"file:backups/aliyun_20261019_155050/ielts_local.db?mode=ro", uri=True)
tables = [
    r[0]
    for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1"
    )
]
print("ALL:", tables)
for t in tables:
    if any(
        k in t
        for k in (
            "daily",
            "task",
            "gendu",
            "speak",
            "session",
            "progress",
            "activity",
            "study",
        )
    ):
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})")]
        n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t} ({n}): {cols}")
