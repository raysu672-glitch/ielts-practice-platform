#!/usr/bin/env python3
"""按轻微复核结果修补残余不对齐。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HTML = Path("sources/juzifanyixin/index.html")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    m = re.search(r"(const translationData = )(\[[\s\S]*?\n\]);", html)
    data = json.loads(m.group(2))
    by = {s["id"]: s for s in data}

    # #47：原子弹等 留到步骤4，与 such as an atomic bomb 同步
    s = by[47]
    s["steps"][2]["chinese"] = (
        "这是因为担心【用于制造大规模杀伤性武器的放射性材料纯化】技术可能会落入不法之徒手中。"
    )

    # #12：分享 → 借给，对齐 lend
    s = by[12]
    s["fullChinese"] = (
        "我们的太空邻居很可能会将其更为先进的技术借给我们，帮助我们解决地球上的诸多问题。"
    )
    s["steps"][0]["chinese"] = "我们的邻居很可能会把技术借给我们。"
    s["steps"][1]["chinese"] = (
        "【我们的太空邻居】很可能会将其【更为先进的】技术借给我们，"
        "【帮助我们解决地球上的诸多问题】。"
    )

    # #114：fullChinese / 步骤与 There are also places 对齐
    s = by[114]
    s["fullChinese"] = "还有些地方，徒步旅行者极易感染疟疾或禽流感等疾病。"
    s["steps"][0]["chinese"] = "还有些地方，徒步旅行者极易感染疾病。"
    s["steps"][1]["chinese"] = (
        "还有些地方，徒步旅行者极易感染疾病，【例如疟疾或禽流感】。"
    )

    # #10：末步「并且伴随」→「因为需要」，对齐 as they will need
    s = by[10]
    s["fullChinese"] = (
        "因此，儿童应尽早学会热情且自信地使用各类设备，"
        "因为他们在整个学习和职业生涯中都会需要这些技能。"
    )
    s["steps"][2]["chinese"] = (
        "因此，儿童应尽早学会热情且自信地使用各类设备，"
        "【因为他们在整个学习和职业生涯中都会需要这些技能】。"
    )

    # #2：步骤2/3 补「一些」，与 some students / fullChinese 对齐
    s = by[2]
    s["steps"][1]["chinese"] = (
        "【例如】，【一些留学的】学生不会受到【思乡之情带来的】困扰。"
    )
    s["steps"][2]["chinese"] = (
        "例如，一些留学的学生不会受到思乡之情带来的困扰，"
        "【因为他们可以通过如FaceTime等即时通讯工具与家人保持日常联系】。"
    )

    HTML.write_text(
        html[: m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + html[m.end(2) :],
        encoding="utf-8",
    )
    print("fixed #47 #12 #114 #10 #2")


if __name__ == "__main__":
    main()
