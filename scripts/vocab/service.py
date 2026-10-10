#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_server.py — 背单词本地服务（纯 Python stdlib, 无第三方依赖）
技术栈复用 ielts-practice-platform: ThreadingHTTPServer + SQLite + 静态前端

API:
  GET  /api/next            下一张卡（优先: 到期复习 > 新词; 无到期无新词 → wait/done）
  POST /api/review          评分 {word_id, rating(1..4)} 并返回下一张卡
  POST /api/extra_dose      赶进度「再学一组」：今天的新词上限再加一个档位（只加今天，不改档位）
  GET  /api/stats           学习统计
静态: GET /danci/ → danci/index.html（其余 repo 内文件白名单放行）

设计:
  - 新卡懒建: 首次评分才写 cards 表, 无行=未学
  - 新词顺序 = words.id = 词频降序
  - 每日新词上限: meta['new_per_day'], 普通班默认 40（方案 C1）；零基础从 10 爬坡；可用 POST /api/config 改档（每 10 一档）
  - 目标保持率: meta['desired_retention'] 0.9/0.85（方案 C2）
  - 学习步(60s/600s)的卡到期前不挡新词; 全部处理完才 wait
"""
import json
import os
import random
import re
import threading
import traceback
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import db
from . import fsrs_api

PORT = int(os.environ.get('VOCAB_PORT', '8788'))
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BEIJING = timedelta(hours=8)

# 入参上界（缺陷 B1）：超过 SQLite INTEGER 的 id 会让 sqlite3 抛 OverflowError，
# 请求体过大则白占内存。两者都在入口钳掉，避免异常冒到 socketserver 掐断连接。
SQLITE_MAX_INT = 2 ** 63 - 1
MAX_BODY_BYTES = 1 << 20  # 1 MiB

_LOCK = threading.RLock()

_CONN = None  # active connection for current request (set by bridge)
_CONN_CACHE = {}  # student_id -> sqlite connection


def get_student_conn(student_id: str):
    """Per-student SQLite file under data/vocab_students/."""
    sid = re.sub(r'[^A-Za-z0-9_\-]', '_', str(student_id or 'anon')) or 'anon'
    with _LOCK:
        conn = _CONN_CACHE.get(sid)
        if conn is not None:
            return conn
        path = os.path.join(ROOT, 'data', 'vocab_students', sid + '.db')
        conn = db.ensure_ready(path)
        _CONN_CACHE[sid] = conn
        return conn


def set_active_conn(conn) -> None:
    global _CONN
    _CONN = conn


def is_int_like(v) -> bool:
    """能不能当整数用（bool 明确排除：True 当 1 会让档位静默变成 10）。"""
    if v is None or isinstance(v, bool) or isinstance(v, (list, dict, tuple)):
        return False
    try:
        int(v)
        return True
    except (TypeError, ValueError):
        try:
            f = float(v)
        except (TypeError, ValueError):
            return False
        return f == f and f not in (float('inf'), float('-inf'))


def as_int(v, default=None, lo=None, hi=None):
    """宽松解析整数：非法值回落 default，并按 lo/hi 钳位。绝不抛异常。

    原先多处直接用 int(入参)，一个 `/api/config {"new_per_day":"abc"}` 就能让
    ValueError 冒到 socketserver，连接被直接掐断（RemoteDisconnected），
    前端只看到"网络错误"。入口一律走这里。
    """
    if not is_int_like(v):
        return default
    n = int(float(v)) if not isinstance(v, int) else v
    if lo is not None and n < lo:
        n = lo
    if hi is not None and n > hi:
        n = hi
    return n


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def beijing_day_start_iso() -> str:
    """当前学习日起点（UTC ISO）。日界见 db.DAY_CUTOFF_HOUR（凌晨 4 点）。"""
    return db.study_day_start_iso(0)


def beijing_day_start_iso_next() -> str:
    """下一个学习日起点（UTC ISO）。"""
    return db.study_day_start_iso(1)


def get_meta(conn, key, default):
    r = conn.execute('SELECT value FROM meta WHERE key=?', (key,)).fetchone()
    return r['value'] if r else default


# ---- 剂量 / 零基础（模块 4 + 8 结构层）----
GEAR_MIN, GEAR_MAX, GEAR_STEP = 10, 80, 10
# 方案 C1：默认从 60 下调到 40（质量档）。60+ 仍可选，界面标「赶进度」。
# 已手选/已写入 meta 的档位不改；只影响缺省与新编组。
DEFAULT_NORMAL = 40          # 普通班默认新词/天（推荐质量档）
GEAR_CATCHUP = 60            # ≥ 此值标为赶进度档
BEGINNER_START = 10          # 零基础起点（对齐每 10 一档）
BEGINNER_CAP = 40            # 爬到 40 后再达标一周 → 毕业到普通班 DEFAULT_NORMAL
RAMP_DAYS = 7
RAMP_SUCCESS = 0.85          # 保留：普通班口径
# 零基础爬坡门槛（缺陷①）：绝对成功率会惩罚初学者。
# 初学者学的正是"不会的词"，成功率天然只有 20~50%；要求 85% 等于永远不给升档 ——
# 实测 30 天档位一次没动。这里退回到"记忆确实在成型"的宽松线，
# 真正的过载保护交给完成率门控与疲劳感知，而不是靠正确率卡人。
RAMP_SUCCESS_BEGINNER = 0.55
GATE_NORMAL = 0.80
GATE_BEGINNER = 0.85
# 方案 C2：目标保持率。0.9=更勤见面（牢记）；0.85=间隔略长、复习负担更低（轻负）。
RETENTION_QUALITY = 0.9
RETENTION_LIGHT = 0.85
# 疲劳感知（缺陷④）：单日自动降级（翻面>10s）占比超阈值 → 判定过载。
# 完成率门控看不出这种过载：学生硬撑着把卡清完了、完成率满分，
# 实测却有一半的卡是盯着发呆 10 秒以上被系统自动降级的。
# 阈值必须按 track 区分（缺陷⑦）：初学者盯着生词发懵是常态（实测占 25~31%），
# 套用普通班的线会天天被判疲劳，反而把爬坡窗口永久卡死 —— 成功率达标的初学者
# 也永远升不了档。这两个数字都缺乏真实数据，属保守默认值，需用真机数据校准。
FATIGUE_SLOW_RATIO = 0.18          # 普通班：健康会话里超时未评应属少数
FATIGUE_SLOW_RATIO_BEGINNER = 0.45  # 零基础：想不起来才需要时间，不算过载
FATIGUE_MIN_REVIEWS = 40            # 样本太少不判定
FATIGUE_CUT_RATIO = 0.30            # 判定疲劳后，"次日"临时按比例减少新词（下限 10）
# 方案 C3：用本周延时探针保留率校正限流（样本够才介入）
PROBE_CALIB_MIN = 8                # 本周至少抽查这么多次才校准
PROBE_RETENTION_OK = 0.85          # ≥ 此值：记得牢，不因超时率砍剂量
PROBE_RETENTION_BAD = 0.70         # < 此值：即使未疲劳也限流

# 空转感知（缺陷 B5）：完成率门控只看"队列清没清空"。实测"每天全按忘了"的学生
# 每张卡都评了、完成率 100%，于是 12 天剂量纹丝不动、照发 60 新词/天，
# 最后 720 个词全部进收容所。这里补一条结果导向的通道：主动成功率过低 → 次日限流。
# 两档：低于 STRUGGLE_SOFT 减 30%，低于 STRUGGLE_HARD 减 60%。
STRUGGLE_SOFT = 0.35
STRUGGLE_HARD = 0.15
STRUGGLE_MIN_ACTIVE = 30            # 主动样本少于这个数不下结论
STRUGGLE_BACKLOG_DAYS = 3           # 到期欠账连续 3 天增长 → 判定跟不上

# 新词保底（缺陷 B3/B6）：只在到期队列里打转的学生永远学不到新词 ——
# 实测 all_slow 12 天只学了 30 词、tiny/overload 的累计卡在 164/790 再也不动。
# 每完成 NEW_RESERVE_AFTER 张复习就插一张新词，保证每天都在往前走。
NEW_RESERVE_AFTER = 12

# 同卡单日评分上限（缺陷 B3）：学生卡壳时，同一张卡会在预算内被反复投出
# （实测 40 分钟内同一张卡被投 8 次、12 天只学 30 词）。超过上限就当日不再投它，
# 会话提前收尾而不是原地空转。正常新词当天最多 3~4 次，5 已是宽裕的余量。
MAX_REVIEWS_PER_WORD_PER_DAY = 5

SHELTER_THRESHOLD = 6   # 钉子户阈值：跨天累计 lapses >= 6 进收容所（模块 7）
TEACHER_NOTE_MAX = 80   # 教师批注长度上限（T09）：学生卡片背面的一条提示，不是作文本
# 赶进度（学生主动「再学一组」）：学完当天额度后，还允许再要一个档位的词。
# 为什么"允许"却不"无限允许"：任务本来就是按天的（每天 N 个新词），一天之内
# 连塞几百个新词会直接把记忆效果毁掉 —— 那和本系统的疲劳限流/完成率门控自相矛盾。
# 所以给一个出口，但只给一组。限额"只是今天"的上限，不动 new_per_day 本身。
EXTRA_SETS_MAX = 1
# 评分可信度（方案 A）：
# A2 前 N 次见面不允许「秒懂」（防翻面后短期记忆灌 Easy）
EASY_MIN_REPS = 3
# A4 延时探针：每周从「已学且至少隔 3 天」的复习卡里抽查，只记保留率；
# 答对不改 due，答错才走正常 FSRS。
PROBE_PER_WEEK = 15
PROBE_MIN_REPS = 3
PROBE_MIN_AGE_DAYS = 3
PROBE_PER_DAY_CAP = 5           # 单日最多抽几张，避免完成页被探针占满
# 收容所复健（缺陷 B2）：收容所必须有出口，否则词永久失联。
REHAB_PER_DAY = 12              # 每日复健抽检上限
REHAB_SUCCESS_RELEASE = 2        # 复健答对 → lapse 回退量

# 卡死检测（缺陷 B6）：连续多天"有额度却几乎学不上新词"（复习把会话吃光）
SQUEEZE_MIN_DAYS = 3
SQUEEZE_RATIO = 0.5     # 实际学到的新词不足档位的一半，就算这天被"挤压"了
SQUEEZE_MIN_REVIEWS = 5  # 但前提是"昨天真的来学了"（不足 5 次评分不算，见 B9）
RECOVER_MIN_DAYS = 3    # 连续几天把额度用满 → 往回加一档
RECOVER_RATIO = 0.9


def _due_queue(conn, deadline: str) -> int:
    """deadline 前到期的「可清理」卡数 —— 必须与 next_card 的投卡口径一致。

    排除两类：
      1) 钉子户（lapses >= SHELTER_THRESHOLD）：它们只进收容所、不进每日队列。
         若把永远清不掉的卡算进门控分母，完成率会长期偏低，严重时让
         gate_block_new 永久为 1（新词永久停投），界面上「还有 N 张」也永远清不掉。
      2) 今天已经评够 MAX_REVIEWS_PER_WORD_PER_DAY 次的卡（缺陷 B3）：
         当日不再投它，否则卡壳学生会把整个会话耗在同一张卡上。
    """
    return conn.execute(
        'SELECT COUNT(*) c FROM cards c WHERE c.due <= ? AND c.lapses < ? '
        'AND (SELECT COUNT(*) FROM reviews r WHERE r.word_id = c.word_id AND r.ts >= ?) < ?',
        (deadline, SHELTER_THRESHOLD, beijing_day_start_iso(),
         MAX_REVIEWS_PER_WORD_PER_DAY)).fetchone()['c']


def _capped_word_ids_sql() -> str:
    """当日评分次数未超上限的过滤子句（参数：学习日起点、上限）。"""
    return ('(SELECT COUNT(*) FROM reviews r WHERE r.word_id = c.word_id AND r.ts >= ?) < ?')


def _shelter_count(conn) -> int:
    """已在收容所的卡数（不进学生队列，教师端可见）。"""
    return conn.execute(
        'SELECT COUNT(*) c FROM cards WHERE lapses >= ?', (SHELTER_THRESHOLD,)).fetchone()['c']


def _rehab_done(conn) -> int:
    """今日已做的收容所复健次数。"""
    if get_meta(conn, 'rehab_date', '') != _today_str():
        return 0
    return as_int(get_meta(conn, 'rehab_done', '0'), 0)


def _rehab_left(conn) -> int:
    return max(0, REHAB_PER_DAY - _rehab_done(conn))


def _probe_week_key() -> str:
    """探针按自然周计数（ISO 周，与学习日无关，便于周报）。"""
    return datetime.now(timezone.utc).strftime('%G-W%V')


def _probe_week_stats(conn) -> dict:
    """本周探针：次数 / 答对次数。"""
    key = _probe_week_key()
    if get_meta(conn, 'probe_week', '') != key:
        return {'n': 0, 'ok': 0, 'left': PROBE_PER_WEEK, 'rate': None}
    n = as_int(get_meta(conn, 'probe_n', '0'), 0)
    ok_n = as_int(get_meta(conn, 'probe_ok', '0'), 0)
    rate = round(ok_n / n * 100, 1) if n else None
    return {'n': n, 'ok': ok_n, 'left': max(0, PROBE_PER_WEEK - n), 'rate': rate}


def _probe_today_done(conn) -> int:
    if get_meta(conn, 'probe_day', '') != _today_str():
        return 0
    return as_int(get_meta(conn, 'probe_today', '0'), 0)


def _probe_left_today(conn) -> int:
    st = _probe_week_stats(conn)
    return max(0, min(st['left'], PROBE_PER_DAY_CAP - _probe_today_done(conn)))


def _bump_probe(conn, correct: bool) -> None:
    key = _probe_week_key()
    if get_meta(conn, 'probe_week', '') != key:
        _meta_set(conn, 'probe_week', key)
        _meta_set(conn, 'probe_n', 0)
        _meta_set(conn, 'probe_ok', 0)
    _meta_set(conn, 'probe_n', as_int(get_meta(conn, 'probe_n', '0'), 0) + 1)
    if correct:
        _meta_set(conn, 'probe_ok', as_int(get_meta(conn, 'probe_ok', '0'), 0) + 1)
    if get_meta(conn, 'probe_day', '') != _today_str():
        _meta_set(conn, 'probe_day', _today_str())
        _meta_set(conn, 'probe_today', 0)
    _meta_set(conn, 'probe_today', _probe_today_done(conn) + 1)


def _pick_probe_card(conn):
    """抽一张成熟复习卡做延时探针。

    只抽「尚未到期」的复习卡（避免和正常到期队列重复），排除今天已评满、
    近 7 天已探针过、收容所。年龄用 last_review（无则 created_at）≥ 3 天。
    """
    if _probe_left_today(conn) <= 0:
        return None
    now = now_iso()
    since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    r = conn.execute(
        'SELECT c.word_id, c.card, c.reps, c.lapses, w.word, w.variants, w.gloss, '
        'w.teacher_note, w.p, w.is_head, w.syll, w.book FROM cards c '
        'JOIN words w ON w.id = c.word_id '
        'WHERE c.reps >= ? AND c.lapses < ? AND c.due > ? AND ' + _capped_word_ids_sql() + ' '
        'AND COALESCE(json_extract(c.card, \'$.state\'), 2) = 2 '
        'AND ( '
        '  (json_extract(c.card, \'$.last_review\') IS NOT NULL '
        '   AND julianday(?) - julianday(json_extract(c.card, \'$.last_review\')) >= ?) '
        '  OR (json_extract(c.card, \'$.last_review\') IS NULL '
        '   AND julianday(?) - julianday(c.created_at) >= ?) '
        ') '
        'AND c.word_id NOT IN ('
        '  SELECT word_id FROM reviews WHERE kind = \'probe\' AND ts >= ?'
        ') '
        'ORDER BY RANDOM() LIMIT 1',
        (PROBE_MIN_REPS, SHELTER_THRESHOLD, now,
         beijing_day_start_iso(), MAX_REVIEWS_PER_WORD_PER_DAY,
         now, PROBE_MIN_AGE_DAYS, now, PROBE_MIN_AGE_DAYS, since)
    ).fetchone()
    return r


def _extra_sets(conn) -> int:
    """今天学生主动多要的组数。跨日自动归零（不写库，靠日期比对失效）。"""
    if get_meta(conn, 'extra_day', '') != _today_str():
        return 0
    return max(0, as_int(get_meta(conn, 'extra_sets', '0'), 0))


def _extra_left(conn) -> int:
    return max(0, EXTRA_SETS_MAX - _extra_sets(conn))


def new_pool_left(conn, track: str = 'normal') -> int:
    """还能投出去的新词数。不能只看 learned < total —— 快筛自报"认识"的词
    不建卡、也不该被算成可学，否则学生点了「再学一组」只会拿到一张空完成页。"""
    now = now_iso()
    book_sql = ' AND (w.book = 1 OR w.book IS NULL) ' if track == 'beginner' else ''
    return conn.execute(
        'SELECT COUNT(*) c FROM words w LEFT JOIN cards c ON c.word_id = w.id '
        'WHERE c.word_id IS NULL AND w.is_head = 1 ' + book_sql +
        'AND (w.screened != 1 OR w.screen_due <= ?)', (now,)).fetchone()['c']


def grant_extra_dose(conn) -> dict:
    """学生主动赶进度：今天的新词上限再加一个档位（「再学一组」）。

    只加"今天"的上限，绝不动 new_per_day —— 否则学生点一次就等于永久改档，
    爬坡与自动降档会全部错乱（和 B6 的"不持久下调档位"是同一条原则）。

    门控/限流时拒绝：那两种状态恰恰说明今天不该加量，放行等于自己打自己。
    """
    apply_dose_rollover(conn)
    if get_meta(conn, 'gate_block_new', '0') == '1':
        return {'error': '今天先把到期清完再赶进度', 'reason': 'gated'}
    if _throttle_cap(conn) >= 0:
        return {'error': '今天被限流了（先缓一缓），明天再赶', 'reason': 'throttled'}
    if _extra_left(conn) <= 0:
        return {'error': '今天已经多学过一组了，明天继续', 'reason': 'exhausted'}
    c = counts(conn)
    # 前提是"当天额度已经学完"：这是"学完了还想多学"的出口，
    # 不是"不想学完今天、直接加量"的捷径（否则额度会越滚越大）。
    if c['new_today'] < c['new_limit']:
        return {'error': '先把今天的量学完，再来加一组', 'reason': 'not_done'}
    if new_pool_left(conn, get_meta(conn, 'track', 'normal')) <= 0:
        return {'error': '没有更多新词可学了', 'reason': 'empty'}
    _meta_set(conn, 'extra_day', _today_str())
    _meta_set(conn, 'extra_sets', _extra_sets(conn) + 1)
    conn.commit()
    c = counts(conn)
    return {'ok': True, 'extra_sets': c['extra_sets'], 'extra_left': c['extra_left'],
            'added': _gear(conn), 'new_limit': c['new_limit'], 'counts': c}


def _bump_rehab(conn) -> None:
    _meta_set(conn, 'rehab_date', _today_str())
    _meta_set(conn, 'rehab_done', _rehab_done(conn) + 1)


def _today_str() -> str:
    return db.study_day_str(0)


def clamp_gear(n) -> int:
    """档位取整到 10 的倍数。非法输入回落到下限，绝不抛异常。"""
    v = as_int(n, GEAR_MIN)
    v = max(GEAR_MIN, min(GEAR_MAX, v))
    return (v // GEAR_STEP) * GEAR_STEP


def _gear(conn) -> int:
    """当前档位（对 meta 里的脏值也安全）。"""
    return clamp_gear(as_int(get_meta(conn, 'new_per_day', str(DEFAULT_NORMAL)), DEFAULT_NORMAL))


def apply_track_from_intro(conn, intro: str) -> None:
    """首进「背过多少」落编组。已有 track 不覆盖（防重复提交改档）。"""
    if get_meta(conn, 'track', ''):
        return
    if intro == 'none':
        _meta_set(conn, 'track', 'beginner')
        _meta_set(conn, 'new_per_day', BEGINNER_START)
        _meta_set(conn, 'ramp_anchor', _today_str())
        _meta_set(conn, 'gear_manual', '0')
        _meta_set(conn, 'gear_intent', 0)
        _meta_set(conn, 'recover_days', 0)
        _meta_set(conn, 'phonics_day', '1')
    else:
        _meta_set(conn, 'track', 'normal')
        _meta_set(conn, 'new_per_day', DEFAULT_NORMAL)
        _meta_set(conn, 'gear_manual', '0')
        _meta_set(conn, 'gear_intent', 0)
        _meta_set(conn, 'recover_days', 0)


def _success_rate(conn, since_iso: str):
    """since 起的「主动评分成功率」 = Good+Easy / 主动评分次数。

    必须剔除 slow=1（背面 10s 无操作由系统自动记的 Hard）——那不是学生评的，
    是系统替他判的。若把它算进成功率，反应慢的学生永远够不到爬坡门槛，
    零基础会永久卡在 10 词/天，与「每天多一点点」的目标正好相反。
    全部都是自动降级（无主动样本）时返回 None，由调用方决定如何解释。
    """
    total = conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND (slow IS NULL OR slow = 0)',
        (since_iso,)).fetchone()['c']
    if not total:
        return None
    good = conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND rating >= 3 AND (slow IS NULL OR slow = 0)',
        (since_iso,)).fetchone()['c']
    return good / total


def _success_between(conn, iso0: str, iso1: str):
    """[iso0, iso1) 窗口内的主动成功率与样本量 → (rate|None, active_n)。"""
    r = conn.execute(
        'SELECT COUNT(*) c, '
        'SUM(CASE WHEN rating >= 3 THEN 1 ELSE 0 END) g '
        'FROM reviews WHERE ts >= ? AND ts < ? AND (slow IS NULL OR slow = 0)',
        (iso0, iso1)).fetchone()
    n = r['c'] or 0
    if not n:
        return None, 0
    return (r['g'] or 0) / n, n


def _week_success(conn) -> float:
    """近 7 个学习日的主动评分成功率。无主动样本返回 0（未达标，不爬坡）。"""
    return _success_rate(conn, db.study_day_start_iso(-7)) or 0.0


def _count_active_hard_today(conn, word_id: int) -> int:
    """今日该词「学生主动点模糊」次数（不含系统 timeout/slow/探针）。"""
    today = beijing_day_start_iso()
    return conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE word_id=? AND ts>=? AND rating=2 '
        'AND (slow IS NULL OR slow!=1) '
        "AND (kind IS NULL OR kind NOT IN ('timeout','probe'))",
        (word_id, today)).fetchone()['c']


def _desired_retention(conn) -> float:
    """方案 C2：当前目标保持率。零基础固定 0.85；普通班读 meta（0.9 / 0.85）。"""
    if get_meta(conn, 'track', 'normal') == 'beginner':
        return RETENTION_LIGHT
    raw = get_meta(conn, 'desired_retention', str(RETENTION_QUALITY))
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return RETENTION_QUALITY
    return RETENTION_LIGHT if v < 0.875 else RETENTION_QUALITY


def _set_desired_retention(conn, value) -> float:
    """写入保持率；只接受 0.9 / 0.85（或邻近值）。返回落库后的值。"""
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError('desired_retention must be 0.9 or 0.85')
    if abs(v - RETENTION_LIGHT) <= 0.01:
        v = RETENTION_LIGHT
    elif abs(v - RETENTION_QUALITY) <= 0.01:
        v = RETENTION_QUALITY
    else:
        raise ValueError('desired_retention must be 0.9 or 0.85')
    _meta_set(conn, 'desired_retention', v)
    return v


def _review_burden_est(conn, new_cap: int) -> int:
    """稳态每日复习负担粗估（张）。FSRS 社区经验：R≈0.9 约 5–7×新词，R≈0.85 约 4–5×。"""
    ret = _desired_retention(conn)
    mult = 6.0 if ret >= 0.9 else 4.5
    return max(0, int(round(max(0, new_cap) * mult)))


def _throttle_cap(conn) -> int:
    """今日临时限流上限；-1 表示今天未限流（也只有"今天"有效，隔日自动失效）。"""
    if get_meta(conn, 'throttle_date', '') != _today_str():
        return -1
    return as_int(get_meta(conn, 'throttle_cap', '-1'), -1)


def _set_throttle(conn, keep_ratio: float, reason: str) -> int:
    """给"今天"设临时新词上限 = 档位 × keep_ratio，落在 10 步档位上。

    多个来源（疲劳 / 空转）可能同时命中，取更严的那个；只影响今天能学多少，
    不动 new_per_day 本身（缺陷⑧：持久下调档位会变成悄悄滑落的单向棘轮）。
    """
    cur = _throttle_cap(conn)
    new = max(GEAR_MIN, clamp_gear(int(_gear(conn) * keep_ratio)))
    if cur >= 0:
        new = min(new, cur)
    _meta_set(conn, 'throttle_date', _today_str())
    _meta_set(conn, 'throttle_cap', new)
    _meta_set(conn, 'throttle_reason', reason)
    return new


def _apply_fatigue(conn, track: str) -> bool:
    """过载感知（缺陷④⑧）：上一学习日"自动降级（翻面>10s）"占比过高 → 判定透支，
    给「今天」设一个临时新词上限。返回 True 表示判定疲劳。

    只做次日临时限流，**不改学生档位**（new_per_day）：
      档位承载的是学生的意图，而普通班没有任何自动回升机制 ——
      疲劳若持久下调档位，就成了单向棘轮，几个月后会悄悄滑到 10 词/天而无人察觉（⑧）。
      临时限流第二天自动失效、自愈，也就不需要再补一套"回升"逻辑。
    阈值按 track 区分（⑦），理由见 FATIGUE_SLOW_RATIO_BEGINNER 处。
    方案 C3：本周探针保留率已经够高时，超时多更可能是走神/测环境，不砍剂量。
    """
    st = _probe_week_stats(conn)
    if st['n'] >= PROBE_CALIB_MIN and (st['rate'] or 0) >= PROBE_RETENTION_OK * 100:
        return False
    y0 = db.study_day_start_iso(-1)
    y1 = db.study_day_start_iso(0)
    r = conn.execute(
        'SELECT COUNT(*) c, SUM(CASE WHEN slow=1 THEN 1 ELSE 0 END) s '
        'FROM reviews WHERE ts >= ? AND ts < ?', (y0, y1)).fetchone()
    total = r['c'] or 0
    slow = r['s'] or 0
    if total < FATIGUE_MIN_REVIEWS:
        return False
    thresh = (FATIGUE_SLOW_RATIO_BEGINNER if track == 'beginner' else FATIGUE_SLOW_RATIO)
    if (slow / total) < thresh:
        return False
    _set_throttle(conn, 1 - FATIGUE_CUT_RATIO, 'fatigue')
    return True


def _apply_probe_throttle(conn) -> bool:
    """方案 C3：用本周延时探针保留率校正限流。

    - 样本够且保留率低 → 即使未判疲劳也限流（假「记得」灌脏评分的信号）
    - 样本够且保留率高、且今日限流原因仅是 fatigue → 撤销该限流
    返回 True 表示改动了 throttle 状态。
    """
    st = _probe_week_stats(conn)
    if st['n'] < PROBE_CALIB_MIN:
        return False
    rate = (st['rate'] if st['rate'] is not None else 0) / 100.0
    if rate < PROBE_RETENTION_BAD:
        _set_throttle(conn, 1 - FATIGUE_CUT_RATIO, 'probe_low')
        return True
    if rate >= PROBE_RETENTION_OK and get_meta(conn, 'throttle_reason', '') == 'fatigue':
        if get_meta(conn, 'throttle_date', '') == _today_str():
            _meta_set(conn, 'throttle_date', '')
            _meta_set(conn, 'throttle_cap', -1)
            _meta_set(conn, 'throttle_reason', '')
            return True
    return False


def _apply_struggle(conn, track: str) -> bool:
    """空转感知（缺陷 B5）：上一学习日学生其实没在正常学 → 今日限流。

    补的是完成率门控的盲区：门控判的是"队列清空率"，而一个每天全按「忘了」的学生
    每张卡都评了、完成率 100%，于是被判成"超额完成"，剂量 12 天纹丝不动，
    最后所有词被反复 lapse 送进收容所。这里按"结果"而不是"动作"来判断。

    三种触发（取最严的那次限流落在同一个 throttle 上）：
      low_success  主动成功率过低
      no_active    一次主动评分都没有（全走自动降级）—— 比成功率低更严重
      backlog      到期欠账连续多天增长 —— 学生在往前走，但走得比到期速度慢
    """
    y0 = db.study_day_start_iso(-1)
    y1 = db.study_day_start_iso(0)
    total = conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND ts < ?', (y0, y1)).fetchone()['c'] or 0
    rate, n = _success_between(conn, y0, y1)

    if n == 0 and total >= STRUGGLE_MIN_ACTIVE:
        # 一次主动评分都没有：学生在页面上，但完全没参与（全部超时自动降级）
        _set_throttle(conn, 0.4, 'no_active')
        return True
    if rate is not None and n >= STRUGGLE_MIN_ACTIVE and rate < STRUGGLE_SOFT:
        _set_throttle(conn, 0.4 if rate < STRUGGLE_HARD else 0.7, 'low_success')
        return True
    if as_int(get_meta(conn, 'backlog_grew_days', '0'), 0) >= STRUGGLE_BACKLOG_DAYS:
        # 欠账在涨说明"每天清完"只是错觉：当天新增的到期把它盖住了（同缺陷②的机制）
        _set_throttle(conn, 0.4, 'backlog')
        return True
    return False


def _eval_squeeze(conn, prev_gated: bool = False) -> int:
    """卡死检测（缺陷 B6）：连续多天"有额度却学不上新词"（复习把整个会话吃光）。

    实测 tiny（每天 3 分钟）与 overload（档位 80 只有 15 分钟）都会掉进这个坑：
    累计学过的词数再也不动，而界面上一切正常。到 SQUEEZE_MIN_DAYS 天就自动降一档
    （手选档位不擅自改，只留 gear_advice 让学生自己决定）。
    返回连续挤压天数。

    降档同时记下 gear_intent（学生原本要的档位），连续学满几天再自动加回去 ——
    没有这条，一次出差的低谷会把档位永久压低（60→50→40→…→10），几个月后
    悄悄滑到每天 10 词而界面上看不出任何异常，正是我们反对的"单向棘轮"。

    prev_gated：昨天是否处于"完成率门控停投"状态。这个参数是缺陷 B9 的修复：
    "没有新词可学"和"学不上新词"是两回事，混在一起会让**刚装好还没开始学的新生**
    在第三天被静默降档（实测正式库 0 张卡却有 squeeze_days=1）。
    """
    y0 = db.study_day_start_iso(-1)
    y1 = db.study_day_start_iso(0)
    y_new = conn.execute('SELECT COUNT(*) c FROM cards WHERE created_at >= ? AND created_at < ?',
                         (y0, y1)).fetchone()['c']
    # 三个"这天的数据不算数"的前置条件（缺陷 B9），把三类误判挡在门外：
    #   ① 昨天被门控停投 —— new_limit 本来就是 0，学生没被给机会，不是"学不上"
    #   ② 昨天评分 < SQUEEZE_MIN_REVIEWS —— 快筛日 / 压根没打开 App，
    #      这类日子 y_new 天然是 0，若不排除，新生开三次 App 就被降一档
    #   ③ 昨天之前一张卡都没有 —— 还没有任何学习历史，capacity 无从谈起
    y_reviews = conn.execute('SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND ts < ?',
                             (y0, y1)).fetchone()['c']
    y_had_cards = conn.execute('SELECT COUNT(*) c FROM cards WHERE created_at < ?',
                              (y0,)).fetchone()['c']
    cap = _gear(conn)
    squeeze_days = as_int(get_meta(conn, 'squeeze_days', '0'), 0)
    # 注意用比例而不是"== 0"：新词保底插队落地后，被挤压的学生每天也能挤出两三个词，
    # 卡在 0 的门槛会永远不触发（实测 tiny 从"0 词"变成"3~4 词/天"，档位照旧 60）。
    squeezed = (cap > 0 and y_new < cap * SQUEEZE_RATIO
                and not prev_gated
                and y_reviews >= SQUEEZE_MIN_REVIEWS
                and y_had_cards > 0)
    squeeze_days = squeeze_days + 1 if squeezed else 0
    _meta_set(conn, 'squeeze_days', squeeze_days)

    # 回升：只有被自动降过档（有 gear_intent）的学生才回升，且不会超过他原本要的档位
    intent = as_int(get_meta(conn, 'gear_intent', '0'), 0)
    recover_days = as_int(get_meta(conn, 'recover_days', '0'), 0)
    if intent > cap and y_new >= cap * RECOVER_RATIO:
        recover_days += 1
    else:
        recover_days = 0
    _meta_set(conn, 'recover_days', recover_days)
    if intent > cap and recover_days >= RECOVER_MIN_DAYS:
        back = min(intent, cap + GEAR_STEP)
        _meta_set(conn, 'new_per_day', back)
        _meta_set(conn, 'recover_days', 0)
        if back >= intent:
            _meta_set(conn, 'gear_intent', 0)
        _meta_set(conn, 'gear_advice', '连续 %d 天都学满了，已把档位加回 %d 词/天'
                  % (recover_days, back))
        return 0

    if squeeze_days >= SQUEEZE_MIN_DAYS:
        if get_meta(conn, 'gear_manual', '0') == '1':
            # 手选档位：不擅自改，只出建议（UI 会顶一条提示）
            _meta_set(conn, 'gear_advice',
                      '连续 %d 天没学满一半额度，多半是复习占满了时间；建议降档或缩短单次时长'
                      % squeeze_days)
        else:
            if intent <= cap:
                _meta_set(conn, 'gear_intent', cap)
            _meta_set(conn, 'new_per_day', max(GEAR_MIN, cap - GEAR_STEP))
            _meta_set(conn, 'gear_advice',
                      '连续 %d 天没学满一半额度，已自动下调一档到 %d 词/天（学满几天会自动加回来）'
                      % (squeeze_days, max(GEAR_MIN, cap - GEAR_STEP)))
        _meta_set(conn, 'squeeze_days', 0)
        squeeze_days = 0
    return squeeze_days


def maybe_rampup(conn) -> None:
    """零基础自动爬坡：每 7 天、近 7 日成功率≥RAMP_SUCCESS_BEGINNER、
    且上一窗口没被门控停投过，则 +10；到 40 后再达标 → 毕业普通班 60。
    学生手改过档位则不再自动改。"""
    if get_meta(conn, 'track', 'normal') != 'beginner':
        return
    if get_meta(conn, 'gear_manual', '0') == '1':
        return
    today = _today_str()
    anchor = get_meta(conn, 'ramp_anchor', '')
    if not anchor:
        _meta_set(conn, 'ramp_anchor', today)
        return
    try:
        d0 = datetime.strptime(anchor, '%Y-%m-%d').date()
        d1 = datetime.strptime(today, '%Y-%m-%d').date()
        days = (d1 - d0).days
    except ValueError:
        _meta_set(conn, 'ramp_anchor', today)
        return
    if days < RAMP_DAYS:
        return
    # 掉队保护：上一窗口被门控停投过，说明到期都没清干净，不该加量
    if get_meta(conn, 'gate_block_new', '0') == '1':
        _meta_set(conn, 'ramp_anchor', today)
        return
    if _week_success(conn) < RAMP_SUCCESS_BEGINNER:
        _meta_set(conn, 'ramp_anchor', today)  # 未达标：窗口后移，再等 7 天
        return
    cur = _gear(conn)
    if cur >= BEGINNER_CAP:
        _meta_set(conn, 'track', 'normal')
        _meta_set(conn, 'new_per_day', DEFAULT_NORMAL)
        _meta_set(conn, 'gear_manual', '0')
        _meta_set(conn, 'ramp_anchor', today)
        return
    _meta_set(conn, 'new_per_day', min(BEGINNER_CAP, cur + GEAR_STEP))
    _meta_set(conn, 'ramp_anchor', today)


def apply_dose_rollover(conn) -> None:
    """跨日：结算昨日完成率门控、过载降档、尝试爬坡、快照今日到期基数。
    每天 counts 时幂等执行。"""
    today = _today_str()
    if get_meta(conn, 'dose_day', '') == today:
        return
    due_start = as_int(get_meta(conn, 'due_at_start', '0'), 0)
    due_done = as_int(get_meta(conn, 'due_done', '0'), 0)
    # 必须在覆写 gate_block_new 之前读：此刻它记录的是"刚刚结束的那一天"的门控状态。
    # 卡死检测要用它区分"没被给机会"和"学不上"（缺陷 B9）。
    prev_gated = get_meta(conn, 'gate_block_new', '0') == '1'
    track = get_meta(conn, 'track', 'normal')
    thresh = GATE_BEGINNER if track == 'beginner' else GATE_NORMAL
    # 完成率封顶 1.0（缺陷②）：当天晚些才到期的旧卡也会计进 due_done，
    # 而分母只快照了"当天开始时就到期"的卡；不封顶时比例会超过 100%，
    # 看起来像"超额完成"，反而掩盖了真实欠账。
    ratio = min(1.0, due_done / due_start) if due_start > 0 else 1.0
    block = '1' if due_start > 0 and ratio < thresh else '0'
    _meta_set(conn, 'gate_block_new', block)
    now = now_iso()
    due_now = _due_queue(conn, now)
    # 欠账增长感知（缺陷 B5 延伸）：完成率会被"当天新增的到期"盖住 ——
    # 当天晚些才到期的卡也算进 due_done，于是清不完也显示"完成"（同缺陷②的机制）。
    # 直接比较两天的到期基数，看学生到底有没有在往前走。
    grew = due_start > 0 and due_now > due_start
    gd = as_int(get_meta(conn, 'backlog_grew_days', '0'), 0)
    _meta_set(conn, 'backlog_grew_days', (gd + 1) if grew else 0)
    # 疲劳只设"今日临时上限"，不再介入爬坡（⑦）：两者一旦耦合，
    # 初学者天天被判疲劳 → 爬坡窗口天天重置 → 永远升不了档。
    _apply_fatigue(conn, track)
    # 空转感知（缺陷 B5）：与疲劳共用同一组 throttle meta，取更严者
    _apply_struggle(conn, track)
    # 方案 C3：探针保留率校正（可撤销误判疲劳，或在假秒懂时主动限流）
    _apply_probe_throttle(conn)
    # 卡死检测（缺陷 B6）：连续"有额度却学不上新词"→ 自动降档 / 出手选建议
    _eval_squeeze(conn, prev_gated=prev_gated)
    maybe_rampup(conn)
    _meta_set(conn, 'due_at_start', due_now)
    _meta_set(conn, 'due_done', 0)
    _meta_set(conn, 'dose_day', today)
    conn.commit()


def probe_ids_today(conn, now: str):
    """快筛「认识」冒头（方案 C4）：到期休眠词尽量当日抽查（全量，单日封顶）。

    旧逻辑只抽 5%，误报认识后几十天几乎失踪。现在首次休眠已缩短到 7–14 天，
    到期后应尽量全量复核；池很大时仍按日封顶，避免一天被复核淹没。
    """
    rows = conn.execute(
        'SELECT w.id FROM words w LEFT JOIN cards c ON c.word_id = w.id '
        'WHERE c.word_id IS NULL AND w.is_head = 1 AND w.screened = 1 AND w.screen_due <= ?',
        (now,)).fetchall()
    ids = [r['id'] for r in rows]
    if not ids:
        return []
    n = min(len(ids), SCREEN_RESURFACE_DAY_CAP)
    if n >= len(ids):
        return ids
    rng = random.Random(_today_str() + ':probe')
    return rng.sample(ids, n)


def counts(conn) -> dict:
    now = now_iso()
    today = beijing_day_start_iso()
    tomorrow = beijing_day_start_iso_next()
    apply_dose_rollover(conn)
    cap = _gear(conn)
    gated = get_meta(conn, 'gate_block_new', '0') == '1'
    # 疲劳/空转临时限流（④⑧ B5）：只影响"今天能学多少"，不动学生档位本身。
    thr = _throttle_cap(conn)
    eff_cap = cap if thr < 0 else min(cap, thr)
    # 赶进度（学生主动「再学一组」）：额度叠加在"今天"之上，不动档位本身。
    # 限流/门控时不给加成 —— 那些状态正是"今天别加量"的信号。
    extra = _extra_sets(conn)
    new_limit = 0 if gated else eff_cap + extra * cap
    track = get_meta(conn, 'track', 'normal')
    # 里程碑"恰好跨过"用的昨日基数：跨日时把当前已学词数滚存为 popup_prev_words。
    # 语义 = 今日起始已学基数，done 结算天然触发（counts 每次取卡都被调）。
    snap_key = 'popup_snapshot_date'
    today_str = _today_str()   # 学习日界（B4），与 new_today 口径一致
    if get_meta(conn, snap_key, '') != today_str:
        learned_now = conn.execute('SELECT COUNT(*) c FROM cards').fetchone()['c']
        _meta_set(conn, 'popup_prev_words', learned_now)
        _meta_set(conn, snap_key, today_str)
        conn.commit()
    c = {
        'total': conn.execute('SELECT COUNT(*) c FROM words').fetchone()['c'],
        'learned': conn.execute('SELECT COUNT(*) c FROM cards').fetchone()['c'],
        'due_now': _due_queue(conn, now),
        'new_today': conn.execute(
            'SELECT COUNT(*) c FROM cards WHERE created_at >= ?', (today,)).fetchone()['c'],
        'reviews_today': conn.execute(
            'SELECT COUNT(*) c FROM reviews WHERE ts >= ?', (today,)).fetchone()['c'],
        'new_limit': new_limit,
    }
    # 明日到期预告：明日 0 点（北京时间）之前到期的可清理卡数（含今日剩余）
    c['tomorrow_due'] = _due_queue(conn, tomorrow)
    # 收容所存量：不进学生队列，但要让完成页说清楚"还有顽固词在老师那边"
    c['shelter_now'] = _shelter_count(conn)
    # 今日成功率：只算主动评分（剔除系统自动降级），另单独报出自动降级次数
    total = c['reviews_today']
    auto_slow = conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND slow = 1', (today,)).fetchone()['c']
    c['today_auto_slow'] = auto_slow
    rate = _success_rate(conn, today)
    c['today_success'] = round(rate * 100, 1) if rate is not None else None
    c['today_active'] = total - auto_slow
    c['remaining_today'] = c['due_now'] + max(0, new_limit - c['new_today'])
    # 上次见你（模块6）：meta.last_active_date 存学习日标签，距今天数写进响应，再更新为今天。
    today_str = _today_str()
    last = get_meta(conn, 'last_active_date', '')
    gap = 0
    if last and last != today_str:
        try:
            d0 = datetime.strptime(last, '%Y-%m-%d').date()
            d1 = datetime.strptime(today_str, '%Y-%m-%d').date()
            gap = (d1 - d0).days
        except ValueError:
            gap = 0
    c['last_seen_days'] = gap if gap >= 1 else 0
    if last != today_str:
        _meta_set(conn, 'last_active_date', today_str)
        conn.commit()
    # 教师在线徽标（模块6）：meta.teacher_online_until 存 epoch 秒，未过期则在线
    online_until = as_int(get_meta(conn, 'teacher_online_until', '0'), 0)
    c['teacher_online'] = int(datetime.now(timezone.utc).timestamp()) < online_until
    c['track'] = track
    c['gated'] = gated
    c['new_cap'] = cap
    # 临时限流：界面用它解释"今天为什么少学了"（不改学生档位本身）
    c['fatigue_cap'] = eff_cap if thr >= 0 else None
    c['throttle_reason'] = get_meta(conn, 'throttle_reason', '') if thr >= 0 else ''
    # 方案 C1/C2：档位标签、目标保持率、稳态复习负担粗估（完成页提示用）
    c['desired_retention'] = _desired_retention(conn)
    if cap >= GEAR_CATCHUP:
        c['gear_tier'] = 'catchup'
    elif cap >= DEFAULT_NORMAL:
        c['gear_tier'] = 'recommended'
    else:
        c['gear_tier'] = 'quality'
    c['review_burden_est'] = _review_burden_est(conn, eff_cap if not gated else 0)
    c['gear_manual'] = get_meta(conn, 'gear_manual', '0') == '1'  # L8：是否已手选档位（可恢复自动）
    # 卡死提示（缺陷 B6）：连续"有额度却学不上新词"时给学生的解释/建议，读过即可清
    c['gear_advice'] = get_meta(conn, 'gear_advice', '')
    # 复健抽检剩余额度（缺陷 B2 的出口）
    c['rehab_left'] = _rehab_left(conn)
    # 休眠复核池（缺陷 B7）：到了复核期、随时能冒头的"认识但没建卡"的词
    c['probe_due'] = conn.execute(
        'SELECT COUNT(*) c FROM words w LEFT JOIN cards c ON c.word_id = w.id '
        'WHERE c.word_id IS NULL AND w.is_head = 1 AND w.screened = 1 AND w.screen_due <= ?',
        (now,)).fetchone()['c']
    c['syll_mode'] = syll_mode_for(conn)
    if track == 'beginner':
        c['total'] = conn.execute(
            'SELECT COUNT(*) c FROM words WHERE is_head=1 AND (book=1 OR book IS NULL)').fetchone()['c']
        pt = phonics_today(conn)
        c['phonics_pending'] = not pt['all_done']
        c['phonics_day'] = pt['day']
    else:
        c['phonics_pending'] = False
        c['phonics_day'] = None
    # 赶进度额度（「再学一组」）：extra_sets=今天已多要的组数，extra_can=现在还能不能再要。
    # 已经有额度没学完时不显示按钮 —— 那是"还没学"，不是"该加量"。
    c['extra_sets'] = extra
    c['extra_max'] = EXTRA_SETS_MAX
    c['extra_left'] = max(0, EXTRA_SETS_MAX - extra)
    c['extra_can'] = bool(
        not gated and thr < 0 and c['extra_left'] > 0
        and c['new_today'] >= new_limit
        and new_pool_left(conn, track) > 0)
    # 延时探针周报（方案 A4）：完成页可展示「本周抽查保留率」
    pst = _probe_week_stats(conn)
    c['probe_n'] = pst['n']
    c['probe_ok'] = pst['ok']
    c['probe_rate'] = pst['rate']
    c['probe_left'] = _probe_left_today(conn)
    return c


def next_card(conn, force=False) -> dict:
    """
    取下一张卡。返回 {mode, card?, wait_seconds?, counts}
    mode: review(到期卡) | new(新词) | wait(等学习步) | done(全部完成)
    force=True 时忽略等待时间, 直接给最早到期的卡。
    """
    now = now_iso()
    c = counts(conn)

    # 1) 到期复习卡: 最过期者优先（排除钉子户 lapses>=6，它们去收容所，不每日反复刺痛）
    #    B3：同时排除今天已经评够次数的卡，否则卡壳学生会把整个会话耗在同一张卡上。
    reserve_new = _new_reserve_due(conn, c)
    if c['due_now'] > 0 and not reserve_new:
        r = conn.execute(
            'SELECT c.word_id, c.card, c.reps, c.lapses, w.word, w.variants, w.gloss, w.teacher_note, w.p, w.is_head, w.syll, w.book '
            'FROM cards c JOIN words w ON w.id = c.word_id '
            'WHERE c.due <= ? AND c.lapses < ? AND ' + _capped_word_ids_sql() +
            ' ORDER BY c.due ASC LIMIT 1',
            (now, SHELTER_THRESHOLD, beijing_day_start_iso(),
             MAX_REVIEWS_PER_WORD_PER_DAY)).fetchone()
        if r is not None:
            return _payload(conn, 'review', r, c)

    # 2) 新词(每日限额内), 按词频降序取最小 id 未学词；只取族长(is_head=1)，族员随族长卡背面展示
    #    快筛：认识休眠不建卡；冒头仅从到期休眠池抽 5% 优先复核
    #    零基础：新词限制在第一册（book=1）
    if c['new_today'] < c['new_limit']:
        probes = probe_ids_today(conn, now)
        book_sql = ''
        if c.get('track') == 'beginner':
            book_sql = ' AND (w.book = 1 OR w.book IS NULL) '
        # 统一优先级链：冒头(0) > 拼读互锁(1) > 词频(2)。
        # 用一条 SQL 的 CASE 表达，避免"有冒头词的日子"绕过其余两级，
        # 让「不规则词不进互锁」的约束时有时无（L5）。
        prio = json.loads(get_meta(conn, 'phonics_priority', '[]')) if c.get('track') == 'beginner' else []
        marks = (','.join('?' * len(probes))) or '-1'
        # 互锁条件：命中任一已学规则，且非不规则词（irr 不参与规则互锁）
        ph_or = ' OR '.join(['w.phonics LIKE ?'] * len(prio)) or '0'
        ph_pats = ['%"' + rid + '"%' for rid in prio]
        r = conn.execute(
            'SELECT w.id word_id, w.word, w.variants, w.gloss, w.teacher_note, w.p, w.is_head, w.syll, w.book FROM words w '
            'LEFT JOIN cards c ON c.word_id = w.id '
            'WHERE c.word_id IS NULL AND w.is_head = 1 ' + book_sql +
            'AND (w.screened != 1 OR w.id IN (' + marks + ')) '
            'ORDER BY CASE '
            '  WHEN w.id IN (' + marks + ') THEN 0 '
            '  WHEN (' + ph_or + ') AND (w.irr IS NULL OR w.irr = "" OR w.irr = "0") THEN 1 '
            '  ELSE 2 END, w.id ASC LIMIT 1',
            probes + probes + ph_pats).fetchone()
        if r is not None:
            return _payload(conn, 'new', r, c)

    # 3) 收容所复健（缺陷 B2 的出口）：正常队列清空后，给学生一个把顽固词捞回来的机会。
    #    没有这一步，lapses 只增不减、所有投卡路径都带 lapses < 阈值，
    #    进了收容所的词连"秒认"都取不到 —— 收容所是一道只进不出的门。
    if _rehab_left(conn) > 0:
        r = conn.execute(
            'SELECT c.word_id, c.card, c.reps, c.lapses, w.word, w.variants, w.gloss, w.teacher_note, w.p, w.is_head, w.syll, w.book '
            'FROM cards c JOIN words w ON w.id = c.word_id '
            'WHERE c.lapses >= ? ORDER BY c.due ASC LIMIT 1', (SHELTER_THRESHOLD,)).fetchone()
        if r is not None:
            p = _payload(conn, 'review', r, c)
            p['rehab'] = True
            p['card']['rehab'] = True
            return p

    # 4) 无到期无新词: 看最早将来到期（同样排除钉子户与今日已评够的卡，
    #    否则它们会绕过收容所/上限被投出）
    r = conn.execute(
        'SELECT c.word_id, c.due, c.card FROM cards c WHERE c.lapses < ? AND ' +
        _capped_word_ids_sql() + ' ORDER BY c.due ASC LIMIT 1',
        (SHELTER_THRESHOLD, beijing_day_start_iso(), MAX_REVIEWS_PER_WORD_PER_DAY)).fetchone()
    if r is not None:
        wait = fsrs_api.due_in_seconds(json.loads(r['card']))
        if force or wait <= 0:
            rr = conn.execute(
                'SELECT c.word_id, c.card, c.reps, c.lapses, w.word, w.variants, w.gloss, w.teacher_note, w.p, w.is_head, w.syll, w.book '
                'FROM cards c JOIN words w ON w.id = c.word_id '
                'WHERE c.word_id = ?', (r['word_id'],)).fetchone()
            return _payload(conn, 'review', rr, c)
        # 学习步内短等待（≤15 分钟）优先于探针，别打断当天复查循环
        if wait <= 900:
            return {'mode': 'wait', 'wait_seconds': int(wait) + 1,
                    'next_due': r['due'], 'counts': c}
        # 下一张还远：插延时探针（方案 A4），答对不改间隔
        pr = _pick_probe_card(conn)
        if pr is not None:
            p = _payload(conn, 'review', pr, c)
            p['probe'] = True
            p['card']['probe'] = True
            return p
        return {'mode': 'wait', 'wait_seconds': int(wait) + 1,
                'next_due': r['due'], 'counts': c}

    # 5) 库里没有任何可投卡：仍可探针；否则 done
    pr = _pick_probe_card(conn)
    if pr is not None:
        p = _payload(conn, 'review', pr, c)
        p['probe'] = True
        p['card']['probe'] = True
        return p
    return {'mode': 'done', 'counts': c}


def _new_reserve_due(conn, c: dict) -> bool:
    """新词保底插队（缺陷 B3/B6）：该不该让一张新词插到复习前面。

    只在"复习永远清不完"时才有意义 —— 那种学生每张卡反复卡壳，
    到期队列一直非空，于是 next_card 第 1 优先级永远命中，新词永远排不上。
    实测 all_slow 12 天只学了 30 词、tiny/overload 的累计再也不动。
    规则：每学 1 个新词，允许它前面先积压 NEW_RESERVE_AFTER 张复习；
    有额度、且积压已超，就把新词插进来，保证每天都有增量。
    """
    if c['new_today'] >= c['new_limit']:
        return False
    if c['reviews_today'] < (c['new_today'] + 1) * NEW_RESERVE_AFTER:
        return False
    # 确认真有新词可取，免得空转（与第 2 优先级同口径，只做存在性判断）
    probes = probe_ids_today(conn, now_iso())
    marks = (','.join('?' * len(probes))) or '-1'
    book_sql = ''
    if c.get('track') == 'beginner':
        book_sql = ' AND (w.book = 1 OR w.book IS NULL) '
    r = conn.execute(
        'SELECT w.id FROM words w LEFT JOIN cards c2 ON c2.word_id = w.id '
        'WHERE c2.word_id IS NULL AND w.is_head = 1 ' + book_sql +
        'AND (w.screened != 1 OR w.id IN (' + marks + ')) LIMIT 1',
        probes).fetchone()
    return r is not None


def _payload(conn, mode, row, c) -> dict:
    card = {
        'word_id': row['word_id'],
        'word': row['word'],
        'variants': json.loads(row['variants']) if 'variants' in row.keys() else [],
        'gloss': row['gloss'],
        'teacher_note': row['teacher_note'] if 'teacher_note' in row.keys() else None,
        'phonetic': row['p'] if 'p' in row.keys() else None,
        'syll': row['syll'] if 'syll' in row.keys() else None,
        'book': row['book'] if 'book' in row.keys() else None,
    }
    # 词族（模块 2）：族长卡背面携带族员（词形+音标+释义），族员不单独建卡
    is_head = row['is_head'] if 'is_head' in row.keys() else 0
    if is_head:
        fam = conn.execute(
            'SELECT word, p, gloss FROM words WHERE family_id=? AND is_head=0 ORDER BY word',
            (row['word_id'],)).fetchall()
        card['family'] = [{'word': f['word'], 'p': f['p'], 'gloss': f['gloss']}
                          for f in fam]
    else:
        card['family'] = []
    if 'reps' in row.keys():
        stored = json.loads(row['card'])
        card['reps'] = row['reps']
        card['lapses'] = row['lapses']
        card['state'] = fsrs_api.card_state_str(stored)
        card['due_in'] = int(fsrs_api.due_in_seconds(stored))
    else:
        card['reps'] = 0
        card['lapses'] = 0
        card['state'] = 'new'
    # 前端封顶提示（方案 A）：新词首次见面封顶模糊；前 EASY_MIN_REPS 次不见秒懂
    card['first_cap'] = (mode == 'new') or (card['reps'] == 0 and card['state'] == 'new')
    card['easy_cap'] = card['reps'] < EASY_MIN_REPS
    return {'mode': mode, 'card': card, 'counts': c}


def do_review(conn, word_id: int, rating: int, dur_ms=None, kind=None, slow=None,
              probe=None) -> dict:
    """评分并返回下一张卡。dur_ms: 翻面→评分耗时；kind: 求助类型；slow: 慢卡标记；
    probe: 是否延时探针（答对不改 due）。"""
    if rating not in (1, 2, 3, 4):
        return {'error': 'rating must be 1..4'}
    r = conn.execute('SELECT id FROM words WHERE id=?', (word_id,)).fetchone()
    if r is None:
        return {'error': 'word_id not found'}
    # dur_ms 清洗：非负、上限 10 分钟（异常值置 NULL）
    if dur_ms is not None:
        try:
            dur_ms = int(dur_ms)
            if dur_ms < 0 or dur_ms > 600000:
                dur_ms = None
        except (TypeError, ValueError):
            dur_ms = None
    # kind 白名单（方案 A 增 first_cap / easy_cap / probe）
    if kind not in ('seen', 'taught', 'timeout', 'first_cap', 'easy_cap', 'probe'):
        kind = None
    # slow 清洗：仅接受 1（翻面>10秒自动降级），其余置 NULL
    slow = 1 if slow in (1, '1', True) else None
    is_probe = probe in (1, '1', True) or kind == 'probe'
    card = db.load_card(conn, word_id)
    reps_before = 0
    if card is not None:
        row_reps = conn.execute(
            'SELECT reps FROM cards WHERE word_id=?', (word_id,)).fetchone()
        reps_before = row_reps['reps'] if row_reps else 0
    # A1：新词第一次评分（尚无卡）最高「模糊」——翻面后短期记忆不能当「记得」
    # 系统自动超时(slow=1)本来就是 2，不受影响。
    if card is None and rating > 2 and not slow:
        rating = 2
        if kind not in ('seen', 'taught'):
            kind = 'first_cap'
    # A2：前 EASY_MIN_REPS 次见面不允许「秒懂」
    if reps_before < EASY_MIN_REPS and rating == 4 and not slow:
        rating = 3
        if kind not in ('seen', 'taught', 'timeout', 'first_cap'):
            kind = 'easy_cap'
    # 门控：今日首次评一张"当天之前就存在、且当时已到期"的卡，才计入 due_done。
    # 必须排除当天新建的卡（缺陷②）：新学卡的学习步当天就会到期，
    # 若算进"清旧账"，分子会被自己当天的新卡灌水
    # （实测 due_done=122 / due_at_start=37 = 330%），门控便永远不触发，
    # 学生一边过载、一边被系统评为"超额完成"。
    # 探针不算清旧账（它抽的是未到期卡）。
    if card is not None and not is_probe:
        today = beijing_day_start_iso()
        already = conn.execute(
            'SELECT COUNT(*) c FROM reviews WHERE word_id=? AND ts>=?', (word_id, today)).fetchone()['c']
        if already == 0:
            row = conn.execute('SELECT due, created_at FROM cards WHERE word_id=?', (word_id,)).fetchone()
            if row and row['due'] <= now_iso() and (row['created_at'] or '') < today:
                _meta_set(conn, 'due_done', int(get_meta(conn, 'due_done', '0')) + 1)
    old_due = None
    old_card_json = None
    if is_probe and card is not None:
        old_due = card.get('due')
        old_card_json = dict(card)
        kind = 'probe'
    if card is None:
        card = fsrs_api.new_card()
    # 探针答对：保留率记账，due 恢复原值（不大幅改间隔）
    if is_probe and rating >= 3 and old_card_json is not None:
        updated = dict(old_card_json)
        # 仍刷新 last_review，避免同一张被连续抽
        updated['last_review'] = datetime.now(timezone.utc).isoformat()
        if old_due:
            updated['due'] = old_due
        db.save_card(conn, word_id, updated, rating, dur_ms, kind, slow)
        _bump_probe(conn, True)
        conn.commit()
        return {'ok': True, 'state': fsrs_api.card_state_str(updated),
                'due_in': int(fsrs_api.due_in_seconds(updated)), 'probe': True,
                'probe_kept_due': True}
    # 系统代评（背面 10s slow / 正面 5s timeout）：不算学生主动「模糊」，调度要分开
    is_auto = bool(slow) or kind == 'timeout'
    # 当天已有主动模糊次数（不含本条）：用于「再插一次」与「别无限循环」
    n_active_hard = 0
    if not is_auto and not is_probe:
        n_active_hard = _count_active_hard_today(conn, word_id)
    updated = fsrs_api.review_card(
        card, rating,
        beginner=(get_meta(conn, 'track', 'normal') == 'beginner'),
        desired_retention=_desired_retention(conn),
        auto=is_auto)
    # 墨墨式半懂：当天第一次主动模糊 → ~15 分钟再出（fsrs_api 已做）；
    # 当天第二次主动模糊 → 下一学习日（避免 15 分钟循环）；
    # 当天模糊过后点记得/秒懂 → 也压到下一学习日（保证明天见一面）。
    if not is_auto and not is_probe:
        if rating == 2 and n_active_hard >= 1:
            updated = fsrs_api.cap_due_next_study_day(updated)
        elif rating >= 3 and n_active_hard >= 1:
            updated = fsrs_api.cap_due_next_study_day(updated)
    db.save_card(conn, word_id, updated, rating, dur_ms, kind, slow)
    if is_probe:
        _bump_probe(conn, rating >= 3)
        conn.commit()
    # 收容所复健结算（缺陷 B2）：这张卡进来时 lapses 已到阈值，说明它是复健抽检。
    # 答对(>=3)就把 lapse 往回退，让它退出收容所、回到每日队列 —— 这是唯一的出口；
    # 答错则维持收容，明天还有抽检机会（每日上限 REHAB_PER_DAY）。
    after = conn.execute('SELECT lapses FROM cards WHERE word_id=?', (word_id,)).fetchone()
    if after and after['lapses'] >= SHELTER_THRESHOLD and not is_probe:
        _bump_rehab(conn)
        if rating >= 3:
            conn.execute('UPDATE cards SET lapses=? WHERE word_id=?',
                         (max(0, after['lapses'] - REHAB_SUCCESS_RELEASE), word_id))
            conn.commit()
    # 快筛冒头复核（模块 1）：休眠词(screened=1)以普通卡出现后——
    #   评"忘了"(rating=1) → 撤销休眠，正常入池（screened=3）
    #   评"记得"(rating>=3) → 续休眠 30~60 天（自报膨胀纠偏：记得就继续不用学）
    #   Hard(rating=2) → 撤销休眠入池（半懂比不懂更该学）
    screened = conn.execute('SELECT screened FROM words WHERE id=?', (word_id,)).fetchone()
    if screened and screened['screened'] == 1:
        if rating == 1:
            conn.execute('UPDATE words SET screened=3, screen_due=NULL WHERE id=?', (word_id,))
        elif rating >= 3:
            due = datetime.now(timezone.utc) + timedelta(days=random.randint(SCREEN_DUE_MIN_DAYS, SCREEN_DUE_MAX_DAYS))
            conn.execute('UPDATE words SET screen_due=? WHERE id=?', (due.isoformat(), word_id))
        else:
            conn.execute('UPDATE words SET screened=3, screen_due=NULL WHERE id=?', (word_id,))
        conn.commit()
    out = {'ok': True, 'state': fsrs_api.card_state_str(updated),
           'due_in': int(fsrs_api.due_in_seconds(updated))}
    if is_probe:
        out['probe'] = True
    return out


def _pct(vals, p):
    """分位数（p 0~100，近邻法）。vals 升序，空返回 None。"""
    if not vals:
        return None
    k = max(0, min(len(vals) - 1, round(p / 100 * (len(vals) - 1))))
    return vals[k]


def teacher_stats(conn, limit=20) -> dict:
    """
    教师易错词清单（T06 最小闭环）：
    - mistakes_top: Hard/Again(rating<=2) 次数 Top N 词（教师介入起点）
    - slowest_top : 每词翻面→评分时延均值 Top N（模块 5 慢卡预警，依赖 T04 dur_ms）
    - duration_pct: 全局时延 P50/P75/P95（为 P75>8s 告警铺垫）
    """
    rows = conn.execute(
        'SELECT w.id, w.word, w.gloss, w.teacher_note, COUNT(*) c FROM reviews r JOIN words w ON w.id = r.word_id '
        'WHERE r.rating <= 2 GROUP BY r.word_id ORDER BY c DESC LIMIT ?', (limit,)).fetchall()
    mistakes_top = [{'word_id': r['id'], 'word': r['word'], 'gloss': r['gloss'],
                     'teacher_note': r['teacher_note'], 'errors': r['c']}
                    for r in rows]

    rows = conn.execute(
        'SELECT w.id, w.word, w.gloss, w.teacher_note, AVG(r.dur_ms) avg_ms, COUNT(*) n FROM reviews r '
        'JOIN words w ON w.id = r.word_id WHERE r.dur_ms IS NOT NULL '
        'GROUP BY r.word_id ORDER BY avg_ms DESC LIMIT ?', (limit,)).fetchall()
    slowest_top = [{'word_id': r['id'], 'word': r['word'], 'gloss': r['gloss'],
                    'teacher_note': r['teacher_note'],
                    'avg_ms': round(r['avg_ms']), 'n': r['n']} for r in rows]

    durs = sorted(r['d'] for r in conn.execute(
        'SELECT dur_ms d FROM reviews WHERE dur_ms IS NOT NULL').fetchall())
    duration_pct = {
        'count': len(durs),
        'p50': _pct(durs, 50), 'p75': _pct(durs, 75), 'p95': _pct(durs, 95),
    }
    return {'mistakes_top': mistakes_top, 'slowest_top': slowest_top,
            'duration_pct': duration_pct, 'limit': limit}


def shelter_list(conn) -> list:
    """钉子户收容所：连续 Again(lapses) >= SHELTER_THRESHOLD 的词（不进正常队列）。"""
    rows = conn.execute(
        'SELECT w.id, w.word, w.gloss, w.teacher_note, c.lapses, c.reps FROM cards c '
        'JOIN words w ON w.id = c.word_id WHERE c.lapses >= ? '
        'ORDER BY c.lapses DESC, w.id ASC', (SHELTER_THRESHOLD,)).fetchall()
    return [{'word_id': r['id'], 'word': r['word'], 'gloss': r['gloss'],
             'teacher_note': r['teacher_note'],
             'lapses': r['lapses'], 'reps': r['reps']} for r in rows]


def set_teacher_note(conn, word_id: int, text: str):
    """教师批注（T09）：写入 words.teacher_note，空串=清除。返回 ok 或 error。

    长度上限：批注是学生卡片背面的一条提示，不是作文本。此前没有上限，老师
    粘贴一整段就会把学生端卡片撑到几屏高，把"看一眼就过"的节奏毁掉。
    超长按字符截断并回报 truncated，不静默吞掉。
    """
    r = conn.execute('SELECT id FROM words WHERE id=?', (word_id,)).fetchone()
    if r is None:
        return {'error': 'word_id not found'}
    text = (text or '').strip()
    truncated = len(text) > TEACHER_NOTE_MAX
    if truncated:
        text = text[:TEACHER_NOTE_MAX]
    conn.execute('UPDATE words SET teacher_note=? WHERE id=?', (text or None, word_id))
    conn.commit()
    return {'ok': True, 'word_id': word_id, 'teacher_note': text or None,
            'truncated': truncated, 'max': TEACHER_NOTE_MAX}


def speed_next(conn, exclude_id=None) -> dict:
    """站立秒认取卡（模块 6 R2）：只投旧词（已建卡族长），不投新词、不投钉子户。
    策略：到期卡优先（最过期者）；无到期卡则随机抽一张已学旧词热身。
    exclude_id: 跳过刚评完的那张，避免连出同词。
    返回 {'mode':'speed','card':{...}} 或 {'mode':'done'}。"""
    now = now_iso()
    # 1) 到期旧词优先
    r = conn.execute(
        'SELECT c.word_id, w.word, w.gloss FROM cards c JOIN words w ON w.id = c.word_id '
        'WHERE c.due <= ? AND c.lapses < ? AND w.is_head = 1 AND c.word_id != ? '
        'ORDER BY c.due ASC LIMIT 1', (now, SHELTER_THRESHOLD, exclude_id or -1)).fetchone()
    # 2) 无到期：随机抽已学旧词（秒认热身，不打乱正常到期节奏）
    if r is None:
        r = conn.execute(
            'SELECT c.word_id, w.word, w.gloss FROM cards c JOIN words w ON w.id = c.word_id '
            'WHERE c.lapses < ? AND w.is_head = 1 AND c.word_id != ? '
            'ORDER BY RANDOM() LIMIT 1', (SHELTER_THRESHOLD, exclude_id or -1)).fetchone()
    if r is None:
        return {'mode': 'done'}
    return {'mode': 'speed',
            'card': {'word_id': r['word_id'], 'word': r['word'], 'gloss': r['gloss']}}


# ================= 鼓励弹窗 L3 软基建（第 10.3 节） =================
# 8 类触发 + CAP/日 + 冷却 + 保底；里程碑必须"恰好跨过"（防 >= 天天弹）。
# 存储：meta 表 popup_last_<type>=最后弹出日期(北京YYYY-MM-DD)、popup_count_<date>=当日已弹数。
POPUP_CAP = 2                       # 每日弹窗合计上限
MILESTONES = (500, 1000, 1500, 2000, 2500, 2900)  # 已学词数里程碑（词族口径近似）
POPUP_COOLDOWN_DAYS = {             # 各类冷却（天）
    'milestone': 0, 'day6': 999, 'day12': 999, 'day13': 999,  # 一次性事件用大冷却
    'lowday': 3, 'sweetspot': 7, 'hardword': 2, 'weekly': 7, 'fallback': 0,
}
HARDWORD_PROB = 0.15                # 硬词攻克触发概率
HARDWORD_LAPSES = 3                 # "钉子词"门槛：历史 Again 次数
FALLBACK_GAP_DAYS = 3               # 连续 N 天零触达 → 第 N+1 天保底


def beijing_today(offset_days: int = 0) -> str:
    """北京今天(或偏移)的日期串 YYYY-MM-DD，用于冷却与计数键。"""
    d = datetime.now(timezone.utc) + BEIJING + timedelta(days=offset_days)
    return d.date().isoformat()


def _meta_set(conn, key, value):
    conn.execute('INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)', (key, str(value)))


def _settle(conn) -> None:
    """兜底收尾：任何未提交的写事务都在返回响应前提交。

    读接口（如 /api/next）在稳态下可能只 _meta_set 不 commit，遗留的写事务会
    独占 SQLite 写锁，导致第二个写入方（教师端/备份/脚本）全部 database is locked。
    """
    try:
        if conn.in_transaction:
            conn.commit()
    except Exception:
        pass


# ---- 快筛（模块 1）：新词首次自报三态，认识休眠、模糊快班、不认识入池 ----
SCREEN_NO_KNOW_STOP = 200   # 连续 N 词无"认识"→ 提前终止快筛。
# 原为 130，对中等水平学生偏紧：实测高中生（词汇量约 1500）在 id=860 处就被截停，
# 剩下的词里夹着大量"其实认识"的，全部被当全新词从零学，白费功夫（缺陷⑥）。
# 放宽到 200，配合 screen_pending 的续筛与教师端重置，把"停下还是继续"交回学生。
# 方案 C4：首次标「认识」→ 7~14 天全量抽查；通过后再进 30~60 天长休眠
SCREEN_FIRST_MIN_DAYS = 7
SCREEN_FIRST_MAX_DAYS = 14
SCREEN_DUE_MIN_DAYS = 30    # 复核通过后的长休眠
SCREEN_DUE_MAX_DAYS = 60
SCREEN_RESURFACE_DAY_CAP = 40  # 到期认识词单日最多冒头张数（尽量全量）
SCREEN_HIST_MAX = 30        # 自报历史栈深度（供「撤销上一词」用）


def _screen_hist(conn) -> list:
    """最近若干次自报的记录 [{'w': word_id, 'a': answer}, ...]。

    存在 meta 里而不是前端 JS 变量里：一刷新页面就丢的撤销等于没有，
    学生"误点了"往往正是在手速快、来回翻的时候。
    """
    try:
        h = json.loads(get_meta(conn, 'screen_hist', '[]'))
        return h if isinstance(h, list) else []
    except ValueError:
        return []


def _screen_hist_push(conn, word_id: int, answer: str) -> None:
    h = _screen_hist(conn)
    h.append({'w': word_id, 'a': answer})
    _meta_set(conn, 'screen_hist', json.dumps(h[-SCREEN_HIST_MAX:], ensure_ascii=False))


def screen_next(conn) -> dict:
    """取下一张待筛词（未筛族长，词频序）。零基础只筛第一册。"""
    r = conn.execute(
        'SELECT w.id word_id, w.word, w.variants, w.gloss, w.p FROM words w '
        'WHERE w.screened = 0 AND w.is_head = 1' + _screen_book_cond(conn) +
        ' ORDER BY w.id ASC LIMIT 1').fetchone()
    if r is None:
        return {'mode': 'done', 'screen_done': True, 'progress': screen_progress(conn)}
    return {
        'mode': 'screen',
        'card': {
            'word_id': r['word_id'], 'word': r['word'], 'p': r['p'],
            'variants': json.loads(r['variants']) if r['variants'] else [],
        },
        'progress': screen_progress(conn),
    }


def screen_submit(conn, word_id: int, answer: str) -> dict:
    """三态入库：know→首次 7~14 天抽查休眠；fuzzy→标记快班(暂入正常池)；no→清标记。
    返回 {'ok':..,'terminated':..,'know_streak':..}——terminated=True 表示连续无认识已达终止线。"""
    if answer not in ('know', 'fuzzy', 'no'):
        return {'error': 'answer must be know|fuzzy|no'}
    r = conn.execute('SELECT id, is_head FROM words WHERE id=?', (word_id,)).fetchone()
    if r is None or not r['is_head']:
        return {'error': 'word not found or not head'}
    streak = int(get_meta(conn, 'screen_no_known_streak', '0'))
    if answer == 'know':
        # 方案 C4：先短休眠做首次全量抽查，通过后再由 review 路径续 30~60 天
        days = random.randint(SCREEN_FIRST_MIN_DAYS, SCREEN_FIRST_MAX_DAYS)
        due = datetime.now(timezone.utc) + timedelta(days=days)
        conn.execute('UPDATE words SET screened=1, screen_due=? WHERE id=?',
                     (due.isoformat(), word_id))
        streak = 0
    elif answer == 'fuzzy':
        conn.execute('UPDATE words SET screened=2, screen_due=NULL WHERE id=?', (word_id,))
        streak += 1
    else:  # no
        conn.execute('UPDATE words SET screened=3, screen_due=NULL WHERE id=?', (word_id,))
        streak += 1
    _meta_set(conn, 'screen_no_known_streak', streak)
    _meta_set(conn, 'screened_done', 1)  # 至少筛过一词，快筛会话不再重置
    _screen_hist_push(conn, word_id, answer)   # 供「撤销上一词」
    conn.commit()
    terminated = streak >= SCREEN_NO_KNOW_STOP
    if terminated:
        _meta_set(conn, 'screen_terminated', 1)
        conn.commit()
    return {'ok': True, 'terminated': terminated, 'know_streak': streak}


def screen_should_start(conn) -> bool:
    """快筛前置判定：新用户（无任何评分历史）且未做过首进询问且从未筛过词。
    已有学习数据的老库不触发（快筛只服务于第一次进系统的学生）。"""
    intro = get_meta(conn, 'screened_intro', '')
    started = get_meta(conn, 'screened_done', '0')
    reviews_n = conn.execute('SELECT COUNT(*) c FROM reviews').fetchone()['c']
    cards_n = conn.execute('SELECT COUNT(*) c FROM cards').fetchone()['c']
    return (not intro) and (started == '0') and reviews_n == 0 and cards_n == 0


def _screen_book_cond(conn, alias: str = '') -> str:
    """快筛的册别过滤：零基础只筛第一册。

    必须与 screen_next 口径一致。原先 screen_progress 不带这个过滤，
    零基础学生的分母是全部 3380 词、而他只会被投第一册的 730 词，
    left 永远清不到 0 —— 顶栏会常驻「继续快筛 2650」。
    """
    if get_meta(conn, 'track', 'normal') != 'beginner':
        return ''
    p = (alias + '.') if alias else ''
    return ' AND (%sbook = 1 OR %sbook IS NULL) ' % (p, p)


def screen_left(conn) -> int:
    """还没自报过的族长数。"""
    return conn.execute(
        'SELECT COUNT(*) c FROM words WHERE screened = 0 AND is_head = 1'
        + _screen_book_cond(conn)).fetchone()['c']


def screen_redoable(conn, scope: str = 'know') -> int:
    """可重新筛的词数：已自报过、但还没真正开始学（没建卡）的族长。

    建过卡的词已有真实学习记录（可能正是冒头复核把它救回来的），
    重筛只会让学生困惑，一律排除。
    """
    cond = 'screened = 1' if scope != 'all' else 'screened != 0'
    return conn.execute(
        'SELECT COUNT(*) c FROM words w WHERE w.is_head = 1 AND ' + cond
        + ' AND w.id NOT IN (SELECT word_id FROM cards)'
        + _screen_book_cond(conn, 'w')).fetchone()['c']


def screen_pending(conn) -> bool:
    """顶栏「快筛」入口是否可用 —— 只表示"还有活可干"，不等于"要自动弹引导"。

    终止(terminated)、跳过(skipped) 只该让系统闭嘴，不该把入口锁死。原先两者
    都直接 return False，造成两条真实的死路（用户反馈「误点了回不去」正是它）：
      · 误点「跳过，直接学」→ intro='skipped'，几千个词再也筛不了
        （实测正式库正是此状态：screened_intro=skipped、待筛 3380、按钮不显示）
      · 连续不认识触发早停 → 提示语让他"点顶栏「⚡继续快筛」"，而按钮恰好被藏了
    现在只要「还有没筛的词」或「有标了认识、还没开始学的词可重筛」，入口就留着。
    自动弹引导仍由 screen_should_start 控制（它要求"全新用户"，不会主动打扰老学生）。
    """
    return screen_left(conn) > 0 or screen_redoable(conn, 'know') > 0


def screen_progress(conn) -> dict:
    """快筛进度（供 UI 与重置入口显示）。"""
    total = conn.execute('SELECT COUNT(*) c FROM words WHERE is_head=1'
                         + _screen_book_cond(conn)).fetchone()['c']
    left = screen_left(conn)
    return {'total': total, 'screened': total - left, 'left': left,
            'know': screen_redoable(conn, 'know'),
            'redo_all': screen_redoable(conn, 'all'),
            'undoable': len(_screen_hist(conn)),
            'intro': get_meta(conn, 'screened_intro', ''),
            'skipped': get_meta(conn, 'screened_intro', '') == 'skipped',
            'terminated': get_meta(conn, 'screen_terminated', '0') == '1'}


def screen_undo(conn) -> dict:
    """撤销上一次自报（「误点了」的直接解法）：把那个词放回待筛池。

    历史栈存在 meta.screen_hist，所以刷新页面、换设备都还能撤。
    撤销「不认识/模糊」时把"连续无认识"计数一并回退 —— 否则撤了词、早停还卡着
    （streak 已到 200），点一下又被终止，等于没救回来。
    """
    h = _screen_hist(conn)
    if not h:
        return {'error': 'nothing to undo'}
    top = h.pop()
    word_id, answer = top.get('w'), top.get('a')
    r = conn.execute('SELECT is_head, word FROM words WHERE id=?', (word_id,)).fetchone()
    if r is None or not r['is_head']:
        return {'error': 'word not found or not head'}
    conn.execute('UPDATE words SET screened=0, screen_due=NULL WHERE id=?', (word_id,))
    if answer in ('no', 'fuzzy'):
        streak = max(0, int(get_meta(conn, 'screen_no_known_streak', '0')) - 1)
        _meta_set(conn, 'screen_no_known_streak', streak)
        if streak < SCREEN_NO_KNOW_STOP:
            _meta_set(conn, 'screen_terminated', 0)
    _meta_set(conn, 'screen_hist', json.dumps(h, ensure_ascii=False))
    _meta_set(conn, 'screened_done', 1)
    conn.commit()
    return {'ok': True, 'word_id': word_id, 'word': r['word'] or '',
            'progress': screen_progress(conn)}


def screen_redo(conn, scope: str = 'know') -> dict:
    """重新筛词（用户反馈「误点了回不去」的正解）。

    scope='know'（默认）：把标了「认识」的词放回待筛池。误点最常见、也最伤 ——
      标成认识后词会休眠 30~60 天，期间只有 5% 概率冒头复核，等于这几十天白丢。
    scope='all'：连「模糊/不认识」一起放回，整轮重筛。
    两者都跳过已建卡的词（已经真正在学，重筛只会造成困惑），
    并清掉早停标记与连续计数，让重筛从头顺利跑完。
    """
    if scope not in ('know', 'all'):
        return {'error': 'scope must be know|all'}
    cond = 'screened = 1' if scope == 'know' else 'screened != 0'
    cur = conn.execute(
        'UPDATE words SET screened=0, screen_due=NULL WHERE is_head = 1 AND ' + cond
        + ' AND id NOT IN (SELECT word_id FROM cards)'
        + _screen_book_cond(conn))
    n = cur.rowcount
    _meta_set(conn, 'screen_no_known_streak', 0)
    _meta_set(conn, 'screen_terminated', 0)
    _meta_set(conn, 'screen_hist', '[]')     # 结果已清零，旧的撤销栈失效
    _meta_set(conn, 'screened_done', 1)      # 保证入口继续可用
    conn.commit()
    return {'ok': True, 'scope': scope, 'reset': n, 'progress': screen_progress(conn)}


def screen_resume(conn) -> dict:
    """明确「接着筛」：清早停标记与连续计数，让学生再拿一轮。

    没有这一步，被早停的学生点进来筛一个词就又立刻触发终止（streak 还是 200），
    等于按钮能点、点了没用。
    """
    _meta_set(conn, 'screen_no_known_streak', 0)
    _meta_set(conn, 'screen_terminated', 0)
    _meta_set(conn, 'screened_done', 1)
    conn.commit()
    return {'ok': True, 'progress': screen_progress(conn)}


def screen_reset(conn) -> dict:
    """重置快筛状态（教师端入口）。

    清掉终止标记与「跳过」选择，并把「已开筛」置回真。
    不动已筛结果（words.screened），学生可接着筛；要彻底重来用 screen_redo('all')
    或 scripts/reset_db.py。
    """
    conn.execute("DELETE FROM meta WHERE key IN ('screen_terminated','screened_intro')")
    conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('screened_done','1')")
    conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('screen_no_known_streak','0')")
    conn.commit()
    return {'ok': True, 'progress': screen_progress(conn)}


# ---- 拼读小课（模块 8）----
PHONICS_PATH = os.path.join(ROOT, 'sources', 'danci', 'data', 'phonics_rules.json')
_PHONICS_CACHE = None


def load_phonics_rules() -> dict:
    global _PHONICS_CACHE
    if _PHONICS_CACHE is None:
        with open(PHONICS_PATH, encoding='utf-8') as f:
            _PHONICS_CACHE = json.load(f)
    return _PHONICS_CACHE


def phonics_day_index(conn) -> int:
    d = int(get_meta(conn, 'phonics_day', '1'))
    return max(1, min(15, d))


def syll_mode_for(conn) -> str:
    """音节脚手架：1~2 周 always，3~4 周 tap，5 周起 hide。非零基础 hide。"""
    if get_meta(conn, 'track', 'normal') != 'beginner':
        return 'hide'
    fd = _first_card_day(conn)
    if not fd:
        return 'always'
    try:
        d0 = datetime.strptime(fd, '%Y-%m-%d').date()
        d1 = datetime.strptime(_today_str(), '%Y-%m-%d').date()
        week = (d1 - d0).days // 7 + 1
    except ValueError:
        return 'always'
    if week <= 2:
        return 'always'
    if week <= 4:
        return 'tap'
    return 'hide'


def _phonics_learned(conn) -> set:
    """学过的拼读规则全集（跨日持久，不随自然日重置）。

    原先只看 phonics_done_<日期>：学生当天多做的一课，第二天会被清空、
    要求重做一遍（L6）。改成全局集合后，学会的规则永久算数。
    """
    return set(json.loads(get_meta(conn, 'phonics_learned', '[]')))


def phonics_today(conn) -> dict:
    """今日拼读课：按 phonics_day 取 2~3 条规则。"""
    data = load_phonics_rules()
    day = phonics_day_index(conn)
    rules = [r for r in data['rules'] if r['day'] == day]
    # 全局已学 ∪ 当日已学（后者兼容旧数据，避免升级瞬间丢进度）
    done = _phonics_learned(conn) | set(
        json.loads(get_meta(conn, 'phonics_done_' + _today_str(), '[]')))
    out = []
    for r in rules:
        exs = []
        for w in r.get('examples', []):
            row = conn.execute(
                'SELECT word, gloss, p FROM words WHERE lower(word)=lower(?)', (w,)).fetchone()
            exs.append({
                'word': w,
                'gloss': row['gloss'] if row else '',
                'p': row['p'] if row else None,
            })
        out.append({
            'id': r['id'], 'title': r['title'], 'tip': r['tip'],
            'grapheme': r['grapheme'], 'examples': exs, 'fakes': r.get('fakes', []),
            'done': r['id'] in done,
        })
    all_done = bool(out) and all(x['done'] for x in out)
    return {
        'day': day, 'total_days': int(data.get('meta', {}).get('days', 15)),
        'rules': out, 'all_done': all_done,
        'required': get_meta(conn, 'track', 'normal') == 'beginner',
        'priority': json.loads(get_meta(conn, 'phonics_priority', '[]')),
    }


def phonics_complete(conn, rule_id: str) -> dict:
    """完成一条规则：记入全局已学 + 加入互锁优先列表；当日全完成后 phonics_day+1。"""
    if not rule_id:
        return {'error': 'rule_id required'}
    data = load_phonics_rules()
    ids = {r['id'] for r in data['rules']}
    if rule_id not in ids:
        return {'error': 'unknown rule'}
    today = _today_str()
    # 全局已学（跨日持久，避免次日重做）+ 当日已学（兼容旧数据与当日进度展示）
    learned = _phonics_learned(conn)
    learned.add(rule_id)
    _meta_set(conn, 'phonics_learned', json.dumps(sorted(learned), ensure_ascii=False))
    key = 'phonics_done_' + today
    done = json.loads(get_meta(conn, key, '[]'))
    if rule_id not in done:
        done.append(rule_id)
        _meta_set(conn, key, json.dumps(done, ensure_ascii=False))
    prio = json.loads(get_meta(conn, 'phonics_priority', '[]'))
    if rule_id not in prio and rule_id != 'review_mix':
        prio.append(rule_id)
        # 只保留最近 6 条，避免优先集过大
        prio = prio[-6:]
        _meta_set(conn, 'phonics_priority', json.dumps(prio, ensure_ascii=False))
    day = phonics_day_index(conn)
    day_ids = [r['id'] for r in data['rules'] if r['day'] == day]
    if day_ids and all(i in learned for i in day_ids):
        if get_meta(conn, 'phonics_advanced_' + today, '0') != '1':
            nxt = min(15, day + 1)
            _meta_set(conn, 'phonics_day', nxt)
            _meta_set(conn, 'phonics_advanced_' + today, '1')
    conn.commit()
    return {'ok': True, 'today': phonics_today(conn)}


def _popup_count_today(conn) -> int:
    return int(get_meta(conn, 'popup_count_' + beijing_today(), '0'))


def _last_popup_any(conn) -> str:
    """最近一次任意弹窗的日期串（保底用），无则 ''。"""
    r = conn.execute(
        "SELECT MAX(value) v FROM meta WHERE key LIKE 'popup_last_%'").fetchone()
    return (r['v'] or '') if r else ''


def _days_since(date_str: str) -> int:
    """date_str(YYYY-MM-DD) 距北京今天的天数；空串返回大数。"""
    if not date_str:
        return 10 ** 9
    try:
        d0 = datetime.strptime(date_str, '%Y-%m-%d').date()
        d1 = datetime.strptime(beijing_today(), '%Y-%m-%d').date()
        return (d1 - d0).days
    except ValueError:
        return 10 ** 9


def _cooled_down(conn, ptype: str) -> bool:
    """该类型是否已过冷却期。"""
    cd = POPUP_COOLDOWN_DAYS.get(ptype, 0)
    if cd == 0:
        return True
    return _days_since(get_meta(conn, 'popup_last_' + ptype, '')) >= cd


def _fire(conn, ptype: str, text: str) -> dict:
    """记录触发并返回弹窗载荷。"""
    today = beijing_today()
    _meta_set(conn, 'popup_last_' + ptype, today)
    _meta_set(conn, 'popup_count_' + today, _popup_count_today(conn) + 1)
    _meta_set(conn, 'popup_any_last', today)
    conn.commit()
    return {'type': ptype, 'text': text}


def _learned_words(conn) -> int:
    return conn.execute('SELECT COUNT(*) c FROM cards').fetchone()['c']


def _today_retention(conn):
    """当日成功率 (Good+Easy)/总评分；无评分返回 None。"""
    today = beijing_day_start_iso()
    total = conn.execute('SELECT COUNT(*) c FROM reviews WHERE ts >= ?', (today,)).fetchone()['c']
    if not total:
        return None
    good = conn.execute(
        'SELECT COUNT(*) c FROM reviews WHERE ts >= ? AND rating >= 3', (today,)).fetchone()['c']
    return good / total


def _first_card_day(conn) -> str:
    """首卡学习日期(北京 YYYY-MM-DD)，无卡返回 ''。"""
    r = conn.execute('SELECT MIN(created_at) m FROM cards').fetchone()
    if not r or not r['m']:
        return ''
    dt = datetime.fromisoformat(r['m'])
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (dt + BEIJING).date().isoformat()


def maybe_popup(conn, last_rating: int = None, last_word_id: int = None) -> dict:
    """组装 /api/next 或 /api/review 响应时调用，返回 {type,text} 或 None。
    按优先级检查 8 类触发，受 CAP 与冷却约束；全不命中则检查保底。
    last_rating/last_word_id: 刚评分后的上下文（硬词攻克用）。"""
    if _popup_count_today(conn) >= POPUP_CAP:
        return None
    today = beijing_today()
    learned = _learned_words(conn)

    # 1) 里程碑：恰好跨过（prev < milestone <= learned）。prev=昨日快照 popup_prev_words
    prev = int(get_meta(conn, 'popup_prev_words', '0'))
    for ms in MILESTONES:
        if prev < ms <= learned and _cooled_down(conn, 'milestone'):
            _meta_set(conn, 'popup_prev_words', learned)  # 跨过即结清，防同日内重复弹
            return _fire(conn, 'milestone',
                         '里程碑！你已学 %d 词，跨过 %d 大关。词汇地基正在成型。' % (learned, ms))

    # 2~4) 日期类（首卡日起第 N 天，一次性）
    first = _first_card_day(conn)
    if first:
        day_n = _days_since(first) + 1  # 学习第几天(1起)
        if day_n == 6 and _cooled_down(conn, 'day6'):
            return _fire(conn, 'day6', '接下来几天会变难，这是所有人共同的遗忘曲线，别慌。')
        if day_n == 12 and _cooled_down(conn, 'day12'):
            return _fire(conn, 'day12', '最难的低谷你已经走出来了，曲线开始回升。')
        if day_n == 13 and _cooled_down(conn, 'day13'):
            return _fire(conn, 'day13', '最难的头两周你已经过去了。')

    # 5~6) retention 类（按日）
    ret = _today_retention(conn)
    if ret is not None:
        if ret < 0.75 and _cooled_down(conn, 'lowday'):
            return _fire(conn, 'lowday', '今天忘得多很正常——你的遗忘曲线和所有人一样。')
        if 0.80 <= ret <= 0.90 and _cooled_down(conn, 'sweetspot'):
            # 前一日不在甜区才弹（避免滞留甜区天天弹）
            y = get_meta(conn, 'popup_yesterday_sweet', '0')
            if y != '1':
                _meta_set(conn, 'popup_yesterday_sweet', '1')
                return _fire(conn, 'sweetspot', '你在最佳学习区间（80~90%），保持！')
        else:
            _meta_set(conn, 'popup_yesterday_sweet', '0')

    # 7) 硬词攻克：刚评 Good/Easy 且该词历史 Again 多
    if last_rating and last_rating >= 3 and last_word_id and _cooled_down(conn, 'hardword'):
        lapses = conn.execute(
            'SELECT lapses FROM cards WHERE word_id=?', (last_word_id,)).fetchone()
        if lapses and lapses['lapses'] >= HARDWORD_LAPSES:
            import random
            if random.random() < HARDWORD_PROB:
                return _fire(conn, 'hardword', '这个钉子词你拿下了。')

    # 8) 周报：距首卡每满 7 天
    if first and _days_since(first) >= 7 and _cooled_down(conn, 'weekly'):
        if _days_since(get_meta(conn, 'popup_last_weekly', '')) >= 7:
            return _fire(conn, 'weekly', '坚持一周了。和上周的自己比，你在变强。')

    # 保底：连续 FALLBACK_GAP_DAYS 天零触达 → 第 N+1 天发通用弹窗
    last_any = _last_popup_any(conn)
    if _days_since(last_any) >= FALLBACK_GAP_DAYS and learned > 0:
        return _fire(conn, 'fallback', '每天清空到期，就是在进步。')

    # 兜底提交：上面的 sweetspot else 分支只写了 meta 没有 _fire，
    # 若不在此收尾，未提交的写事务会一直挂在连接上，把整个库锁住（读接口锁库 Bug）。
    _settle(conn)
    return None


# ---------------- HTTP ----------------

MIME = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
        '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon', '.woff2': 'font/woff2'}


class Handler(BaseHTTPRequestHandler):
    server_version = 'VocabServer/1.0'
    protocol_version = 'HTTP/1.1'

    def log_message(self, fmt, *args):
        print('[%s] %s' % (datetime.now(timezone.utc).strftime('%H:%M:%S'), fmt % args))

    # ---- helpers ----
    def _json(self, obj, code=200):
        # 兜底：任何路由返回响应前先收尾未提交的写事务，防止读接口把库写锁住
        with _LOCK:
            _settle(_CONN)
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _file(self, rel_path: str):
        path = os.path.normpath(os.path.join(ROOT, rel_path))
        if not path.startswith(ROOT) or not os.path.isfile(path):
            self._json({'error': 'not found'}, 404)
            return
        ext = os.path.splitext(path)[1].lower()
        with open(path, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', MIME.get(ext, 'application/octet-stream'))
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        # Content-Length 可能被写成垃圾值，直接 int() 会 ValueError 并掐断连接
        n = as_int(self.headers.get('Content-Length'), 0, 0, MAX_BODY_BYTES)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode('utf-8'))
        except Exception:
            return {}

    # ---- routes ----
    def do_GET(self):
        try:
            return self._route_get()
        except Exception as e:  # 兜底（缺陷 B1）：任何未预期异常回 500 JSON，而不是断连
            return self._fail(e)

    def do_POST(self):
        try:
            return self._route_post()
        except Exception as e:
            return self._fail(e)

    def _fail(self, e):
        traceback.print_exc()
        try:
            self._json({'error': 'internal error', 'detail': str(e)[:200]}, 500)
        except Exception:
            pass  # 响应头可能已发出，此时只能放弃

    def _route_get(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path in ('/', '/danci', '/danci/'):
            return self._file('danci/index.html')
        if u.path.startswith('/danci/'):
            # danci 目录下静态文件（教师页 teacher.html 等），_file 内置路径穿越防护
            return self._file(u.path.lstrip('/'))
        if u.path == '/api/next':
            with _LOCK:
                res = next_card(_CONN, force=q.get('force') == ['1'])
                pp = maybe_popup(_CONN)
                if pp:
                    res['popup'] = pp
                return self._json(res)
        if u.path == '/api/speed/next':
            with _LOCK:
                ex = as_int(q.get('exclude', [None])[0], None, 1, SQLITE_MAX_INT)
                return self._json(speed_next(_CONN, exclude_id=ex))
        if u.path == '/api/screen/next':
            # 快筛取词（模块 1）
            with _LOCK:
                return self._json(screen_next(_CONN))
        if u.path == '/api/screen/start':
            # 快筛前置判定：是否需要走首进询问+快筛流程；pending=存量快筛可续
            with _LOCK:
                return self._json({'should_start': screen_should_start(_CONN),
                                   'pending': screen_pending(_CONN),
                                   'progress': screen_progress(_CONN)})
        if u.path == '/api/phonics/today':
            with _LOCK:
                return self._json(phonics_today(_CONN))
        if u.path == '/api/stats':
            with _LOCK:
                c = counts(_CONN)
                st = {}
                for r in _CONN.execute(
                        "SELECT CASE rating WHEN 1 THEN 'again' WHEN 2 THEN 'hard' "
                        "WHEN 3 THEN 'good' WHEN 4 THEN 'easy' ELSE '?' END k, COUNT(*) c "
                        "FROM reviews GROUP BY k"):
                    st[r['k']] = r['c']
                c['rating_hist'] = st
                return self._json(c)
        if u.path == '/api/teacher/stats':
            with _LOCK:
                # 非法 limit 原先会让 int() 抛异常掐断连接；现在回落 20 并钳到 1..200
                lim = as_int(q.get('limit', [None])[0], 20, 1, 200)
                return self._json(teacher_stats(_CONN, limit=lim))
        if u.path == '/api/shelter':
            with _LOCK:
                return self._json({'words': shelter_list(_CONN),
                                   'threshold': SHELTER_THRESHOLD})
        m = re.fullmatch(r'/api/word/(\d+)', u.path)
        if m:
            wid = as_int(m.group(1), None)
            if wid is None or wid < 1 or wid > SQLITE_MAX_INT:
                # 超范围（原先 OverflowError 掐断连接）/ 0 —— 都当不存在，不要钳位成别的词
                return self._json({'error': 'not found'}, 404)
            with _LOCK:
                w = db.get_word(_CONN, wid)
                return self._json(w if w else {'error': 'not found'}, 200 if w else 404)
        return self._json({'error': 'not found'}, 404)

    def _route_post(self):
        u = urlparse(self.path)
        body = self._body()
        if u.path == '/api/review':
            with _LOCK:
                res = do_review(_CONN, body.get('word_id'), body.get('rating'),
                                body.get('dur_ms'), body.get('kind'), body.get('slow'),
                                body.get('probe'))
            if 'error' in res:
                return self._json(res, 400)
            with _LOCK:
                res['next'] = next_card(_CONN)
                pp = maybe_popup(_CONN, last_rating=body.get('rating'),
                                 last_word_id=body.get('word_id'))
                if pp:
                    res['popup'] = pp
            return self._json(res)
        if u.path == '/api/screen':
            # 快筛三态入库（模块 1）：know=认识休眠 / fuzzy=模糊 / no=不认识
            with _LOCK:
                res = screen_submit(_CONN, body.get('word_id'), body.get('answer'))
            if 'error' in res:
                return self._json(res, 400)
            with _LOCK:
                res['next'] = screen_next(_CONN) if not res['terminated'] else {'mode': 'done'}
                res['progress'] = screen_progress(_CONN)
            return self._json(res)
        if u.path == '/api/phonics/complete':
            with _LOCK:
                res = phonics_complete(_CONN, body.get('rule_id'))
            if 'error' in res:
                return self._json(res, 400)
            return self._json(res)
        if u.path == '/api/screen/reset':
            # 快筛重置入口（L4）：清终止/跳过标记，让快筛可重新续做
            with _LOCK:
                return self._json(screen_reset(_CONN))
        if u.path == '/api/screen/undo':
            # 撤销上一词（误点的即时救回）：从服务端自报历史栈里弹出最后一个词
            with _LOCK:
                res = screen_undo(_CONN)
            if 'error' in res:
                return self._json(res, 400)
            return self._json(res)
        if u.path == '/api/screen/redo':
            # 重新筛词：scope=know 只放回标了「认识」的词；all 连模糊/不认识一起放回
            with _LOCK:
                res = screen_redo(_CONN, body.get('scope') or 'know')
            if 'error' in res:
                return self._json(res, 400)
            return self._json(res)
        if u.path == '/api/screen/resume':
            # 明确「接着筛」：清早停标记与连续计数
            with _LOCK:
                return self._json(screen_resume(_CONN))
        if u.path == '/api/extra_dose':
            # 赶进度（学生主动「再学一组」）：把今天的新词上限再加一个档位。
            # 只加今天，不改档位；门控/限流时拒绝（理由见 grant_extra_dose）。
            with _LOCK:
                res = grant_extra_dose(_CONN)
            if 'error' in res:
                return self._json(res, 409)
            return self._json(res)
        if u.path == '/api/config':
            with _LOCK:
                if 'new_per_day' in body:
                    # 非法值必须报错（缺陷 B1）：原先 `body.get('new_per_day') or DEFAULT_NORMAL`
                    # 会把 0 / None / true / "abc" 一律吞成默认 60 —— 学生点"10 词"却静默变成 60。
                    if 'new_per_day' in body and not is_int_like(body['new_per_day']):
                        return self._json({'error': 'new_per_day must be an integer'}, 400)
                    # 零基础天花板更低（BEGINNER_CAP）：防止误把档位拉满、与防过载定位冲突（L8）
                    cap = BEGINNER_CAP if get_meta(_CONN, 'track', 'normal') == 'beginner' else GEAR_MAX
                    gear = max(GEAR_MIN, min(cap, clamp_gear(body['new_per_day'])))
                    _meta_set(_CONN, 'new_per_day', gear)
                    _meta_set(_CONN, 'gear_manual', '1')  # 手选档位后停止自动爬坡
                    _meta_set(_CONN, 'gear_advice', '')   # 学生自己动手了，撤销建议
                    _meta_set(_CONN, 'squeeze_days', 0)   # 重新计时，别刚改完就再降一档
                    _meta_set(_CONN, 'gear_intent', 0)    # 学生自己定了档位，清掉"自动降档前的原档"
                    _meta_set(_CONN, 'recover_days', 0)
                if body.get('gear_auto'):
                    # 恢复自动爬坡（L8 的后悔药）：清掉手选标记，零基础回落到爬坡梯内
                    _meta_set(_CONN, 'gear_manual', '0')
                    if get_meta(_CONN, 'track', 'normal') == 'beginner':
                        cur = _gear(_CONN)
                        _meta_set(_CONN, 'new_per_day', min(BEGINNER_CAP, cur))
                    _meta_set(_CONN, 'ramp_anchor', _today_str())
                    _meta_set(_CONN, 'gear_advice', '')
                    _meta_set(_CONN, 'squeeze_days', 0)
                    _meta_set(_CONN, 'gear_intent', 0)
                    _meta_set(_CONN, 'recover_days', 0)
                if body.get('ack_advice'):
                    # 学生已经看过"连续几天学不上新词"的提示
                    _meta_set(_CONN, 'gear_advice', '')
                if 'desired_retention' in body:
                    # 方案 C2：目标保持率 0.9（牢记）/ 0.85（轻负）
                    try:
                        _set_desired_retention(_CONN, body['desired_retention'])
                    except ValueError as e:
                        return self._json({'error': str(e)}, 400)
                # T05 快筛埋点（模块 1 前置）+ 零基础编组
                if 'screened_intro' in body:
                    val = str(body['screened_intro'])[:40]
                    _meta_set(_CONN, 'screened_intro', val)
                    apply_track_from_intro(_CONN, val)
                _CONN.commit()
            return self._json({
                'ok': True,
                'track': get_meta(_CONN, 'track', 'normal'),
                'new_per_day': _gear(_CONN),
                'gear_manual': get_meta(_CONN, 'gear_manual', '0') == '1',
                'desired_retention': _desired_retention(_CONN),
            })
        if u.path == '/api/teacher/release':
            # 收容所释放（缺陷 B2）：教师把顽固词放回学生队列。没有这条，收容所只进不出。
            wid = as_int(body.get('word_id'), None, 1, SQLITE_MAX_INT)
            if wid is None:
                return self._json({'error': 'word_id must be a positive integer'}, 400)
            with _LOCK:
                ok = db.release_from_shelter(_CONN, wid, to_lapses=0)
            if not ok:
                return self._json({'error': 'word_id not found'}, 404)
            return self._json({'ok': True, 'word_id': wid, 'released': True})
        if u.path == '/api/teacher/note':
            # 入参校验（与 release 同规矩）：这条此前漏了 as_int，超大整数会让
            # sqlite3 抛 OverflowError 变成 500，而不是干净地报 400。
            wid = as_int(body.get('word_id'), None, 1, SQLITE_MAX_INT)
            if wid is None:
                return self._json({'error': 'word_id must be a positive integer'}, 400)
            with _LOCK:
                res = set_teacher_note(_CONN, wid, body.get('text'))
            if 'error' in res:
                return self._json(res, 400)
            return self._json(res)
        if u.path == '/api/teacher/online':
            # 教师在线徽标（模块6）：minutes 分钟内标记教师在线；0=下线
            minutes = as_int(body.get('minutes'), 0, 0, 24 * 60)
            until = int(datetime.now(timezone.utc).timestamp()) + minutes * 60 if minutes else 0
            with _LOCK:
                _meta_set(_CONN, 'teacher_online_until', str(until))
                _CONN.commit()
            return self._json({'ok': True, 'teacher_online_until': until, 'minutes': minutes})
        return self._json({'error': 'not found'}, 404)


def main():
    global _CONN
    _CONN = db.ensure_ready()
    print(f'vocab server: http://0.0.0.0:{PORT}/danci/  (db={db.db_path()})')
    httpd = ThreadingHTTPServer(('', PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nbye')


if __name__ == '__main__':
    main()