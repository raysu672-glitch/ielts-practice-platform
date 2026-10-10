#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fsrs_api.py — FSRS 复习调度封装（基于 py-fsrs 6.x vendored）
供 local_server.py 调用。纯函数风格, 不持有数据库连接。
"""
import sys
import os
from datetime import datetime, timedelta, timezone

# 让 fsrs 从仓库内 vendor 目录加载（无需 pip 安装）
_VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'vendor')
if _VENDOR not in sys.path:
    sys.path.insert(0, os.path.abspath(_VENDOR))

from fsrs import Card, Scheduler, Rating, State

from . import db

# 默认「牢记」档：desired_retention=0.9，学习步 60s/600s
SCHEDULER = Scheduler()
# 方案 C2「轻负」档：保持率 0.85，间隔略长、每日复习负担更低（学习步不变）
SCHEDULER_LIGHT = Scheduler(desired_retention=0.85)

# 新词「毕业」间隔（Learning → Review）：对齐 Anki 的 graduating interval=1 天，
# 不用 FSRS 默认的 ~2 天（Good）/~8 天（Easy）。复习中的卡仍走 FSRS 长间隔。
# 到期时刻 = 下一学习日 04:00（北京），与剂量/完成率口径一致。

# 零基础专用调度器（缺陷 ③）：学习步缩到 30s/180s、目标保持率降到 0.85。
# 默认的 60s/600s 对"每天只有 10 张卡、没有任何旧卡可穿插"的初学者是灾难：
# 做完一轮后只能在 600 秒的等待里干等，一张卡一天内被反复拉起来十几次，
# 25 分钟会话大半耗在等，正反馈极稀（模拟中零基础一张卡被评 16.8 次）。
# 初学者需要的是更短更密的循环，而不是更长的间隔。
SCHEDULER_BEGINNER = Scheduler(
    desired_retention=0.85,
    learning_steps=(timedelta(seconds=30), timedelta(seconds=180)),
    relearning_steps=(timedelta(minutes=3),),
)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_card() -> dict:
    """创建一张新卡（Learning, step=0, due=now）。返回 dict 形式以便存 SQLite。"""
    return Card().to_dict()


def _next_study_day_due() -> datetime:
    """下一学习日起点（UTC），新词第一次毕业时的 due。"""
    due = datetime.fromisoformat(db.study_day_start_iso(1))
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return due


def review_card(card_dict: dict, rating: int, beginner: bool = False,
                desired_retention: float = 0.9, auto: bool = False) -> dict:
    """
    对卡片评分并返回更新后的卡片 dict。
    rating: 1=Again 2=Hard 3=Good 4=Easy（映射到四键自评）
    beginner: 零基础班使用更短学习步的调度器（见 SCHEDULER_BEGINNER）
    desired_retention: 方案 C2，普通班 0.9（牢记）/ 0.85（轻负）；beginner 忽略此参
    auto: 系统超时代评（正面 5s 没翻 / 背面 10s 没点），不是学生主动点「模糊」

    产品层间隔：
    - 学习步内按「秒懂」→ 按「记得」处理，走完当天复查再毕业。
    - Learning → Review 的第一次毕业 → due 固定到下一学习日。
    - Learning +「模糊」：最多 3 分钟后再出，半懂当天要多见面。
    - Review + 学生主动「模糊」：约 15 分钟后再出（对齐墨墨：半懂当天多见面）。
      当天第二次主动模糊 / 模糊后再点记得 → 由 local_server 压到下一学习日。
    - Review + 系统自动 Hard：最多 3 分钟后再出——没点击≠认半懂。
    """
    card = Card.from_dict(card_dict)
    if card.due.tzinfo is None:  # 兜底: 旧数据可能无 tz
        card.due = card.due.replace(tzinfo=timezone.utc)
    if beginner:
        sch = SCHEDULER_BEGINNER
    elif desired_retention is not None and float(desired_retention) < 0.875:
        sch = SCHEDULER_LIGHT
    else:
        sch = SCHEDULER
    eff = rating
    if card.state == State.Learning and rating == 4:
        eff = 3
    before = card.state
    updated, _log = sch.review_card(card, Rating(eff))
    now = now_utc()
    if before == State.Learning and updated.state == State.Review:
        updated.due = _next_study_day_due()
    elif before == State.Learning and rating == 2:
        # 学习步内模糊：别干等 10 分钟，最多 3 分钟再出
        hard_cap = now + timedelta(minutes=3)
        if updated.due is None or updated.due > hard_cap:
            updated.due = hard_cap
    elif before == State.Review and rating == 2:
        if auto:
            # 系统代评：当天短时重出，给学生真正点一次的机会
            hard_cap = now + timedelta(minutes=3)
        else:
            # 学生主动「模糊」：当天再插一次（约 15 分钟），对齐墨墨半懂多见面
            hard_cap = now + timedelta(minutes=15)
        if updated.due is None or updated.due > hard_cap:
            updated.due = hard_cap
    return updated.to_dict()


def cap_due_next_study_day(card_dict: dict) -> dict:
    """把 due 压到不晚于下一学习日（模糊后「记得」仍保证明天见）。"""
    out = dict(card_dict)
    nxt = _next_study_day_due()
    due = datetime.fromisoformat(out['due'])
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    if due > nxt:
        out['due'] = nxt.isoformat()
    return out


def card_state_str(card_dict: dict) -> str:
    s = card_dict.get('state')
    # state int: 1=Learning 2=Review 3=Relearning
    return {1: 'learning', 2: 'review', 3: 'relearning'}.get(s, '?')


def is_due(card_dict: dict) -> bool:
    due = datetime.fromisoformat(card_dict['due'])
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return due <= now_utc()


def due_in_seconds(card_dict: dict) -> int:
    """距离 due 还有多少秒（负数=已过期）。学习步内的卡不参与此项。"""
    due = datetime.fromisoformat(card_dict['due'])
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return (due - now_utc()).total_seconds()


if __name__ == '__main__':
    # 自测
    c = new_card()
    print('new:', c)
    c2 = review_card(c, 3)
    print('after Good:', c2)
    c3 = review_card(c2, 3)
    print('after Good x2:', c3)
    print('state:', card_state_str(c3), 'due_in:', due_in_seconds(c3))
    import json
    print(json.dumps(c3, ensure_ascii=False))