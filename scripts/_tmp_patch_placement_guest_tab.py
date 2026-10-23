# -*- coding: utf-8 -*-
"""Add teacher tab for placement guest results."""
from pathlib import Path

html_path = Path("sources/tinglidanciceshi/index.html")
t = html_path.read_text(encoding="utf-8")

tab_btn = (
    '<div class="tab" onclick="switchTeacherTab(\'placementGuests\')">入学摸底</div>'
)
pane = (
    '<div id="tabPlacementGuests" style="display:none;">'
    '<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px;flex-wrap:wrap;">'
    '<div><strong>访客入学摸底</strong>'
    '<div style="color:#666;font-size:0.9rem;margin-top:4px;">无需学号的临时测试结果；正式学生仍走学生端「入学摸底」。</div></div>'
    '<button class="btn btn-secondary btn-sm" type="button" onclick="loadPlacementGuests()">刷新</button>'
    '</div>'
    '<p style="color:#666;font-size:0.9rem;margin:0 0 12px;">分享链接：'
    '<code>/xinshengmodi/?guest=1</code></p>'
    '<div id="placementGuestsList"></div></div>'
)

if "placementGuests" in t and "tabPlacementGuests" in t:
    print("already patched")
else:
    # Insert tab button after 测试记录 tab
    needle = "switchTeacherTab('records')"
    i = t.find(needle)
    if i < 0:
        raise SystemExit("records tab not found")
    # find end of that tab div
    end = t.find("</div>", i)
    if end < 0:
        raise SystemExit("tab close not found")
    insert_at = end + len("</div>")
    t = t[:insert_at] + tab_btn + t[insert_at:]

    # Insert pane after tabRecords
    marker = 'id="tabRecords"'
    j = t.find(marker)
    if j < 0:
        raise SystemExit("tabRecords not found")
    # find matching close of tabRecords: look for next id="tab after tabRecords content
    # simpler: insert before tabProgress or tabTasks
    for nxt in ('id="tabTasks"', 'id="tabProgress"', 'id="tabWriting"'):
        k = t.find(nxt)
        if k > j:
            # walk back to <div
            start_div = t.rfind("<div", 0, k)
            t = t[:start_div] + pane + t[start_div:]
            break
    else:
        raise SystemExit("insert point for pane not found")

    html_path.write_text(t, encoding="utf-8")
    print("html patched")
