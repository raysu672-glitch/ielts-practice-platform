# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
basic = json.loads(re.search(r"const ALL_WORDS = (\[.*?\]);", (ROOT/"sources/tinglidanciceshi/listening_basic.html").read_text(encoding="utf-8"), re.S).group(1))
listen = json.loads(re.search(r"const ALL_WORDS = (\[.*?\]);", (ROOT/"sources/tinglidanciceshi/listening.html").read_text(encoding="utf-8"), re.S).group(1))

# Scan listening.html for likely wrong meanings
listen_issues = []
for e in listen:
    w, m = e["word"], e["meaning"]
    wl = w.lower()
    if wl == "intelligence" and ("情报" in m or "人工" in m):
        listen_issues.append((w, m, "智能；智力", "中英"))
    if wl == "artificial" and "情报" in m:
        listen_issues.append((w, m, "人工的；人造的", "中英"))
    if wl == "labour" and "劳动" not in m and "工作" not in m:
        listen_issues.append((w, m, "劳动；劳工", "中英"))
    if wl == "grant" and m.strip() in ("授予", "同意"):
        listen_issues.append((w, m, "拨款；补助金", "中英"))
    if wl == "buffet" and "自助餐" not in m and "打击" not in m:
        listen_issues.append((w, m, "自助餐；冲击", "中英"))
    if wl == "presenting" and "呈现" not in m and "介绍" not in m:
        listen_issues.append((w, m, "展示；介绍", "中英"))
    if wl == "moderate" and "温和" not in m and "中等" not in m:
        listen_issues.append((w, m, "适度的；温和的", "中英"))
    if wl == "firm" and m.strip() == "公司":
        listen_issues.append((w, m, "公司；坚固的", "中英"))
    if wl == "aid" and m.strip() == "援助" and "急救" not in m:
        pass
    if wl == "lost" and "found" not in m and m.strip() == "失去的":
        pass
    if wl == "social" and m.strip() == "社会的":
        pass
    if wl == "program" and "节目" not in m and "程序" in m:
        pass
    if wl == "application" and "申请" not in m:
        listen_issues.append((w, m, "申请；应用", "中英"))

basic_issues = []
checks = {
    "advance level": ("进阶水平", "高级水平", "中英"),
    "plane science": ("航空科学", "行星科学", "中英"),
    "political man": ("政治人", "政治家", "中英"),
    "children mind": ("儿童心智", "托儿/看孩子(childminder)", "中英"),
    "environment damage": ("环境损害", "环境破坏", "中英"),
    "academic": ("学院的", "学术的；学院的", "中英"),
    "achievement": ("完成达到", "成就；成绩", "中英"),
    "greenfield": ("绿色田野", "未开发土地/绿地", "中英"),
    "piano life": ("钢琴", "钢琴生活(?) / 需核实原文", "逻辑"),
    "cheapest budget": ("最便宜的预算", "最经济/最低预算", "中英"),
    "compulsory and regular": ("必修和常规", "必修且定期", "中英"),
    "unsocial": ("不合群", "不善社交/反社会(?) ", "中英"),
    "free pick": ("免费接", "免费接送(pickup)", "中英"),
    "alarming system": ("报警系统", "alarm system(英文错)", "拼写"),
    "golf court": ("高尔夫球场", "golf course(英文错)", "拼写"),
    "privacy company": ("私人公司", "private company(英文错)", "拼写"),
    "weathers": ("天气(复)", "weather(英文错)", "语法"),
    "hairs": ("头发(复)", "hair(英文错)", "语法"),
    "study skill": ("学习技巧", "study skills(英文错)", "语法"),
    "finance market": ("金融市场", "financial market(英文错)", "语法"),
    "families life": ("家庭生活", "family life(英文错)", "语法"),
    "culture awareness": ("文化意识", "cultural awareness(英文错)", "语法"),
    "culture context": ("文化背景", "cultural context(英文错)", "语法"),
    "bottle water": ("瓶装水", "bottled water(英文错)", "语法"),
    "repaired cost": ("维修成本", "repair cost(英文错)", "语法"),
    "cooperation loan": ("合作贷款", "co-operative loan(?)", "逻辑"),
    "triangle sharp": ("锐角三角", "sharp triangle(英文错)", "语法"),
    "time consuming": ("耗费时间", "time-consuming(英文错)", "语法"),
    "animals behavior": ("动物行为", "animal behaviour(英文错)", "语法"),
    "pet meat": ("宠物食品", "pet food(英文错)", "逻辑"),
    "personal officer": ("人事管理员", "personnel officer(英文错)", "拼写"),
    "firework": ("烟花", "fireworks(英文错)", "语法"),
    "driving license": ("驾照", "driving licence(英式)", "拼写"),
    "defense": ("防御", "defence(英式)", "拼写"),
}

for e in basic:
    wl = e["word"].lower()
    if wl in checks:
        bad, good, typ = checks[wl]
        m = e["meaning"]
        if bad in m or (wl == "academic" and m.strip() == "学院的"):
            basic_issues.append((e["word"], m, good, typ))
        elif wl in ("plane science", "political man", "children mind", "environment damage", "greenfield", "piano life", "cheapest budget", "compulsory and regular", "unsocial", "free pick"):
            basic_issues.append((e["word"], m, good, typ))

print("listening.html issues:")
for row in listen_issues:
    print("%s | %s | %s | %s" % (row[0], row[2], row[3], row[1]))

print("\nbasic issues:")
for row in basic_issues:
    print("%s | %s | %s | %s" % (row[0], row[2], row[3], row[1]))

# More basic English scan from modules.js list
mods = (ROOT/"sources/tinglidanciceshi/js/modules.js").read_text(encoding="utf-8")
words = json.loads(re.search(r"var allWordsListeningBasic = (\[.*?\]);", mods).group(1))
extra_patterns = [
    (r"^banana ride$", "banana boat", "拼写"),
    (r"^burning time$", "burning time(?)", "逻辑"),
    (r"^card index$", "card index (OK)", "逻辑"),
    (r"^children background$", "children's background", "语法"),
    (r"^compulsory and regular$", "compulsory and regular(?)", "逻辑"),
    (r"^cooperation loan$", "co-operative loan(?)", "逻辑"),
    (r"^double-grill$", "double grill(?)", "拼写"),
    (r"^economics history$", "economic history", "语法"),
    (r"^environment damage$", "environmental damage", "语法"),
    (r"^eye contacts$", "eye contact", "语法"),
    (r"^finance market$", "financial market", "语法"),
    (r"^free pick$", "free pickup", "拼写"),
    (r"^girl club$", "girls' club", "语法"),
    (r"^high user$", "heavy user", "拼写"),
    (r"^note system$", "note-taking system(?)", "逻辑"),
    (r"^objective matters$", "objective matters(?)", "逻辑"),
    (r"^piano life$", "piano life(?)", "逻辑"),
    (r"^plane science$", "planet science", "拼写"),
    (r"^privacy company$", "private company", "拼写"),
    (r"^regular exercises$", "regular exercise", "语法"),
    (r"^research finding$", "research findings", "语法"),
    (r"^statement position$", "statement of position(?)", "逻辑"),
    (r"^swimming suit$", "swimsuit / swimming suit", "用法"),
    (r"^textbooks allowance$", "textbook allowance", "语法"),
    (r"^triangle sharp$", "sharp triangle", "语法"),
    (r"^view shelter$", "viewing shelter", "拼写"),
    (r"^waterpower$", "water power / hydropower", "拼写"),
    (r"^biological fishing$", "biological fishing(?)", "逻辑"),
    (r"^china stone$", "China stone", "逻辑"),
    (r"^greenfield$", "greenfield (undeveloped land)", "用法"),
    (r"^micro-radiogram$", "micro-radiogram(?)", "逻辑"),
    (r"^pet meat$", "pet food", "逻辑"),
    (r"^political man$", "politician", "中式"),
    (r"^sandglass$", "hourglass / sandglass", "用法"),
    (r"^sandy$", "sandy (OK adj)", "逻辑"),
]
print("\nextra basic english from modules.js:")
for w in words:
    for pat, fix, typ in extra_patterns:
        if re.match(pat, w, re.I):
            print("%s | %s | %s" % (w, fix, typ))
