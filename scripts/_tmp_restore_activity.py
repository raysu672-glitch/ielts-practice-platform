"""把工作区里「意外丢失的活动日志接线」从 HEAD 恢复回来。

背景：`scripts/local_server.py`、`sources/tinglidanciceshi/js/{teacher,student}.js`
在工作区里丢掉了「学生操作时间线」这一整套接线（HEAD 有、线上正在用，
线上 activity_events 每天 500~950 条，最新一条就是今天）。直接部署会让老师端的
操作时间线整块消失，所以先把这几块按 HEAD 原文补回，再继续本轮的改动。

做法：用 difflib 对齐 HEAD 与工作区，只把**整块删除且含活动日志标记**的片段补回，
其余差异（本轮的改动）原样保留。
"""

import difflib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MARKERS = (
    "log_activity",
    "ensure_activity_tables",
    "list_student_activity",
    "log_student_client_events",
    "student-activity",
    "activity/me",
    "reportActivity",
    "_activityActionLabels",
    "_activityTimelineState",
    "onStudentActivityDateChange",
    "loadStudentActivityTimeline",
    "studentActivityTimeline",
    "studentActivityDate",
    "TASK_MODULE_LABELS",
    "_activity_plan_context",
    "client_ip",
    "handle_activity_me_post",
    "handle_teacher_student_activity",
    "from activity_log import",
)

TARGETS = [
    "scripts/local_server.py",
    "sources/tinglidanciceshi/js/teacher.js",
    "sources/tinglidanciceshi/js/student.js",
]


def head_text(path: str) -> str:
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"读不到 HEAD:{path}")
    return r.stdout


def is_activity_block(lines: list[str]) -> bool:
    blob = "\n".join(lines)
    return any(m in blob for m in MARKERS)


for path in TARGETS:
    with open(path, encoding="utf-8") as fh:
        work = fh.read()
    head = head_text(path)
    if not head:
        print(f"跳过 {path}（HEAD 无此文件）")
        continue

    h = head.splitlines(keepends=True)
    w = work.splitlines(keepends=True)
    sm = difflib.SequenceMatcher(None, h, w, autojunk=False)

    out: list[str] = []
    restored = 0
    restored_lines = 0
    pos = 0  # 已被消费的 work 行数
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        # 先把 work 里 j1 之前尚未消费的行原样拷过来
        if j1 > pos:
            out.extend(w[pos:j1])
            pos = j1
        if tag in ("delete", "replace"):
            block = h[i1:i2]
            if tag == "delete" and is_activity_block(block):
                out.extend(block)
                restored += 1
                restored_lines += len(block)
                continue
        if tag in ("equal", "delete", "replace"):
            out.extend(w[j1:j2])
            pos = j2
        elif tag == "insert":
            out.extend(w[j1:j2])
            pos = j2
    out.extend(w[pos:])

    new = "".join(out)
    if new != work:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print(f"OK  {path}: 恢复 {restored} 段 / {restored_lines} 行")
    else:
        print(f"--  {path}: 无需恢复")
