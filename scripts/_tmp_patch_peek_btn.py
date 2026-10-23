from pathlib import Path

p = Path("sources/xiezuocihuo/index.html")
t = p.read_text(encoding="utf-8")
old = '<div class="study-learn-btns"><button id="studySkipBtn">跳过此词伙</button>'
new = (
    '<div class="study-learn-btns">'
    '<button type="button" id="studyPeekBtn">显示英文</button>'
    '<button id="studySkipBtn" style="display:none">跳过此词伙</button>'
)
if old not in t:
    raise SystemExit("old snippet not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("ok")
