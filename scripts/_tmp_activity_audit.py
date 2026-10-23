"""对比 HEAD 与工作区里「活动日志」（activity_log / _activityLog / log_activity）的接线数量。

只统计真正跟活动日志有关的标记，避免被词表里的 "activity" 干扰。
"""

import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MARKERS = [
    "log_activity",
    "ensure_activity_tables",
    "list_student_activity",
    "log_student_client_events",
    "_activityLog",
    "_activityActionLabels",
    "_activityTimelineState",
    "student-activity",
    "activity/me",
    "reportActivity",
]

FILES = [
    "scripts/local_server.py",
    "scripts/activity_log.py",
    "sources/tinglidanciceshi/js/teacher.js",
    "sources/tinglidanciceshi/js/student.js",
    "sources/tinglidanciceshi/js/app.js",
    "sources/tinglidanciceshi/index.html",
    "sources/changnanju/index.html",
    "sources/juzifanyixin/index.html",
    "sources/kouyulianxi/app.js",
    "sources/kouyulianxi/complex-sentences.html",
    "sources/kouyulianxi/p1-data.js",
    "sources/tongyitihuan/index.html",
    "sources/tinglidanciceshi/listening_basic.html",
    "sources/tinglidanciceshi/listening.html",
]


def head(path: str) -> str:
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def work(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


print(f"{'file':56} {'marker':26} HEAD  WORK")
for path in FILES:
    h, w = head(path), work(path)
    for m in MARKERS:
        ch, cw = h.count(m), w.count(m)
        if ch or cw:
            flag = "  <-- 丢失" if cw < ch else ""
            print(f"{path:56} {m:26} {ch:4} {cw:4}{flag}")
