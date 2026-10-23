# -*- coding: utf-8 -*-
from pathlib import Path
import re
t = Path("sources/tinglidanciceshi/index.html").read_text(encoding="utf-8")
# teacher home tabs
for m in re.finditer(r'data-tab="([^"]+)"', t):
    print("data-tab", m.group(1))
for m in re.finditer(r"switchTeacherTab\('([^']+)'\)", t):
    print("switch", m.group(1))
i = t.find("teacherHome")
print("teacherHome snippet:", t[i:i+800] if i>=0 else "missing")
