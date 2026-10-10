#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db.py — SQLite 数据层：建表、导入词表、卡片读写
设计要点：
- words 表：词表一次性导入，只读（id 顺序 = 词频降序 = 学习顺序）
- cards 表：懒创建，首次见到某词评分时才建行（无行 = 未学过）
- reviews 表：全部评分历史（统计用）
- 卡片本体以 FSRS Card 的 JSON 形式整列存储（to_dict/from_dict 直接互转）
"""
import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone

_PLATFORM_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
_DEFAULT_DB_PATH = os.path.join(_PLATFORM_ROOT, 'data', 'vocab.db')
_JSON_PATH = os.path.join(_PLATFORM_ROOT, 'sources', 'danci', 'data', 'vocab3500.json')

BEIJING = timedelta(hours=8)
# 学习日界（缺陷 B4）：凌晨 4 点前算"前一天"。
# 为什么不是 0 点：new_today 是 created_at >= 今天的实时计数，过了 0 点就归零，
# 于是 23:58 开工的学生会在会话中途被"刷新"额度 —— 实测 10 分钟内学了 80 个新词
# （额度 60），且 due_at_start / due_done / 疲劳的"昨天"全部错位到相邻日期。
# 把日界挪到 4 点，"深夜连着学"自然归属同一个学习日；这也是 SRS 类工具的通行做法。
DAY_CUTOFF_HOUR = 4
# 钉子户判定（缺陷 B2）：同一个词单日最多计 2 次 lapse。
# lapses >= 6 就进收容所，而新词的学习步是 60s/600s —— 若不限单日次数，
# 学生会在 5 分钟内把一个刚见面的词"连忘 6 次"直接送进收容所，
# 连"今天再试一次"的机会都没有。限成 2 次/日后，凑够 6 次至少需要跨 3 天，
# 这才是"反复忘"而不是"一次没学会"。
MAX_LAPSE_PER_DAY = 2


def _now_bj() -> datetime:
    """当前北京时间（naive，仅用于取日界）。"""
    return datetime.now(timezone.utc) + BEIJING


def _study_day_anchor(offset_days: int = 0) -> datetime:
    """当前学习日的起点（北京时间 naive）。offset_days 可前后偏移。"""
    b = _now_bj()
    if b.hour < DAY_CUTOFF_HOUR:
        b = b - timedelta(days=1)
    b = b + timedelta(days=offset_days)
    return b.replace(hour=DAY_CUTOFF_HOUR, minute=0, second=0, microsecond=0)


def study_day_str(offset_days: int = 0) -> str:
    """学习日的标签（YYYY-MM-DD）= 该学习日所在日历日。"""
    return _study_day_anchor(offset_days).date().isoformat()


def study_day_start_iso(offset_days: int = 0) -> str:
    """学习日起点对应的 UTC 时刻，ISO 字符串（用于和 reviews.ts 比较）。"""
    return (_study_day_anchor(offset_days) - BEIJING).isoformat(timespec='seconds')

SCHEMA = """
CREATE TABLE IF NOT EXISTS words (
    id       INTEGER PRIMARY KEY,        -- 1..N, 即词频降序的学习顺序
    word     TEXT NOT NULL UNIQUE,
    variants TEXT NOT NULL DEFAULT '[]', -- JSON 数组字符串
    gloss    TEXT NOT NULL,
    freq     INTEGER,                    -- 词频计数, NULL=未匹配
    teacher_note TEXT,                   -- 教师批注（"老师说"，T09）
    family_id INTEGER,                   -- 词族 ID = 族长 word.id（模块 2）
    is_head  INTEGER NOT NULL DEFAULT 1, -- 1=族长(建卡) 0=族员(仅同卡背面展示)
    p        TEXT,                       -- 音标（ECDICT phonetic）
    ex       TEXT,                       -- 例句（预留，ECDICT csv 无，后续 stardict 补）
    syll     TEXT,                       -- 音节切分（预留，phonics）
    irr      TEXT,                       -- 不规则变化 go→went→gone（预留）
    book     INTEGER,                    -- 册号：1=高频800 2=其余（模块 2 分册）
    pos      TEXT                        -- 词性（ECDICT，族卡展示用）
);
CREATE TABLE IF NOT EXISTS cards (
    word_id     INTEGER PRIMARY KEY REFERENCES words(id),
    card        TEXT NOT NULL,           -- FSRS Card dict (JSON)
    due         TEXT NOT NULL,           -- 冗余列: card.due ISO 字符串, 便于 SQL 查询
    created_at  TEXT NOT NULL,
    last_rating INTEGER,
    reps        INTEGER NOT NULL DEFAULT 0,
    lapses      INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_cards_due ON cards(due);
CREATE INDEX IF NOT EXISTS idx_cards_created ON cards(created_at);
CREATE TABLE IF NOT EXISTS reviews (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES words(id),
    rating  INTEGER NOT NULL,            -- 1..4
    ts      TEXT NOT NULL,
    dur_ms  INTEGER,                     -- 翻面→评分耗时毫秒（慢卡/快卡分析，模块 5/6 数据地基）
    kind    TEXT,                        -- 求助/降级标记：NULL=正常评分 'seen'=见过但想不起 'taught'=教我（模块 7 三键） 'timeout'=正面 5 秒没翻面、本次封顶模糊
    slow    INTEGER                      -- 1=翻面>10秒自动降级的慢卡（模块 5）
);
-- reviews 索引（性能）：这张表是唯一会无限增长的表，而几乎所有热路径都在按
-- "某个词在某天之后评过几次" 过滤：
--   · _due_queue 的关联子查询   → 每张卡都要数一次该词的当日评分
--   · _capped_word_ids_sql()    → 同上（B3 的同卡当日上限）
--   · reviews_today / _success_rate / 快慢卡统计 → 按 ts 扫今天
-- 没有索引时 SQLite 只能靠"自动索引"临时兜底（每次查询重建一遍，白烧 CPU），
-- 或者直接对 cards × reviews 做嵌套扫。这里建两个覆盖索引把它固定下来。
CREATE INDEX IF NOT EXISTS idx_reviews_word_ts ON reviews(word_id, ts);
CREATE INDEX IF NOT EXISTS idx_reviews_ts ON reviews(ts);
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def db_path() -> str:
    """数据库路径：环境变量 VOCAB_DB 优先（README 承诺的隔离手段，便于测试/多实例）。

    必须每次调用时读环境变量，不能固化在模块常量里，否则子进程改环境不生效。
    """
    return os.path.abspath(os.environ.get('VOCAB_DB') or _DEFAULT_DB_PATH)


def connect(path=None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=None) -> sqlite3.Connection:
    """建表。返回连接。"""
    path = path or db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    conn.commit()
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    """旧库增量迁移：缺列则 ALTER 补齐（幂等）。"""
    cols = {r['name'] for r in conn.execute('PRAGMA table_info(reviews)')}
    if 'dur_ms' not in cols:
        conn.execute('ALTER TABLE reviews ADD COLUMN dur_ms INTEGER')
    if 'kind' not in cols:
        conn.execute('ALTER TABLE reviews ADD COLUMN kind TEXT')
    if 'slow' not in cols:
        conn.execute('ALTER TABLE reviews ADD COLUMN slow INTEGER')
    wcols = {r['name'] for r in conn.execute('PRAGMA table_info(words)')}
    if 'teacher_note' not in wcols:
        conn.execute('ALTER TABLE words ADD COLUMN teacher_note TEXT')
    # T11 词族 + wordlist 字段（模块 2）
    for col, ddl in (('family_id', 'ALTER TABLE words ADD COLUMN family_id INTEGER'),
                     ('is_head', 'ALTER TABLE words ADD COLUMN is_head INTEGER NOT NULL DEFAULT 1'),
                     ('p', 'ALTER TABLE words ADD COLUMN p TEXT'),
                     ('ex', 'ALTER TABLE words ADD COLUMN ex TEXT'),
                     ('syll', 'ALTER TABLE words ADD COLUMN syll TEXT'),
                     ('irr', 'ALTER TABLE words ADD COLUMN irr TEXT'),
                     ('book', 'ALTER TABLE words ADD COLUMN book INTEGER'),
                     ('pos', 'ALTER TABLE words ADD COLUMN pos TEXT')):
        if col not in wcols:
            conn.execute(ddl)
    # T05+T10 快筛（模块 1）：screened 0=未筛 1=认识休眠 2=模糊 3=不认识；screen_due=休眠冒头到期
    for col, ddl in (('screened', 'ALTER TABLE words ADD COLUMN screened INTEGER NOT NULL DEFAULT 0'),
                     ('screen_due', 'ALTER TABLE words ADD COLUMN screen_due TEXT'),
                     ('phonics', 'ALTER TABLE words ADD COLUMN phonics TEXT')):  # 拼读规则 id JSON 列表
        if col not in wcols:
            conn.execute(ddl)


def import_words(conn: sqlite3.Connection, json_path=None) -> int:
    """导入词表。若 words 表非空则跳过（幂等）。返回导入条数。"""
    json_path = json_path or os.path.abspath(_JSON_PATH)
    n = conn.execute('SELECT COUNT(*) AS c FROM words').fetchone()['c']
    if n > 0:
        return 0
    with open(json_path, encoding='utf-8') as f:
        entries = json.load(f)
    rows = [
        (i + 1, e['word'], json.dumps(e.get('variants', []), ensure_ascii=False),
         e['gloss'], e.get('freq'))
        for i, e in enumerate(entries)
    ]
    conn.executemany('INSERT INTO words(id, word, variants, gloss, freq) VALUES(?,?,?,?,?)', rows)
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES('imported_at', ?)",
        (datetime.now(timezone.utc).isoformat(timespec='seconds'),))
    conn.commit()
    return len(rows)


def _ensure_phonics(conn: sqlite3.Connection) -> None:
    """全新安装后补跑拼读打标（幂等）：有音标但无 phonics 标签时构建一次。

    拼读打标要靠音标做校验（见 build_phonics 的三重过滤），所以必须先跑完
    build_family.py 的 ECDICT 富化。这里若发现音标还没回填，只给提示不硬跑，
    免得打出一库空标签、让人误以为拼读已就绪。
    """
    try:
        total = conn.execute('SELECT COUNT(*) c FROM words').fetchone()['c']
        if total == 0:
            return
        n = conn.execute(
            "SELECT COUNT(*) c FROM words WHERE phonics IS NOT NULL AND phonics!='[]'").fetchone()['c']
        if n > 0:
            return
        ipa = conn.execute(
            "SELECT COUNT(*) c FROM words WHERE p IS NOT NULL AND p!=''").fetchone()['c']
        if ipa == 0:
            print('[phonics] 词库尚无音标，跳过拼读打标。'
                  '请先运行 python scripts/setup.py（或 scripts/build_family.py）')
            return
        from . import build_phonics  # 同包，延迟导入避免与 db 形成循环依赖
        st = build_phonics.tag_words(conn)
        conn.commit()
        print(f'[phonics] 首次构建完成：打标 {st["tagged"]}/{st["total"]} 词、'
              f'音节 {st["syll"]} 词、不规则 {st["irr"]} 词')
    except Exception as e:  # 打标失败不应阻塞服务启动
        print(f'[phonics] 构建跳过（不影响背词主流程）: {e}')


def ensure_ready(path=None) -> sqlite3.Connection:
    """建表 + 导入 + 拼读打标（幂等）。local_server 启动时调用。"""
    conn = init_db(path)
    import_words(conn)
    _ensure_phonics(conn)
    return conn


def get_word(conn: sqlite3.Connection, word_id: int) -> dict:
    r = conn.execute('SELECT * FROM words WHERE id=?', (word_id,)).fetchone()
    if r is None:
        return None
    d = dict(r)
    d['variants'] = json.loads(d['variants'])
    return d


def load_card(conn: sqlite3.Connection, word_id: int) -> dict:
    """返回 FSRS Card dict, 无行(未学过)返回 None。"""
    r = conn.execute('SELECT card FROM cards WHERE word_id=?', (word_id,)).fetchone()
    return json.loads(r['card']) if r else None


def save_card(conn: sqlite3.Connection, word_id: int, card_dict: dict, rating: int,
              dur_ms: int = None, kind: str = None, slow: int = None):
    """新建或更新卡片 + 记录一次评分历史。调用方负责 fsrs 调度。
    kind: 求助/降级标记（'seen'/'taught'/'timeout'）；slow: 1=翻面>10秒自动降级的慢卡（模块 5）。"""
    ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
    card_json = json.dumps(card_dict, ensure_ascii=False)
    due = card_dict.get('due', '')
    # lapse 单日封顶（缺陷 B2）：先数今天已经记过几次 Again，够 MAX_LAPSE_PER_DAY 就不再累加。
    # 不封顶的话，新词 5 分钟内连忘 6 次就直接进收容所（且永不释放）。
    lapse_inc = 0
    if rating == 1:
        n_today = conn.execute(
            'SELECT COUNT(*) c FROM reviews WHERE word_id=? AND rating=1 AND ts >= ?',
            (word_id, study_day_start_iso())).fetchone()['c']
        if n_today < MAX_LAPSE_PER_DAY:
            lapse_inc = 1
    cur = conn.execute(
        'UPDATE cards SET card=?, due=?, last_rating=?, reps=reps+1, lapses=lapses+? WHERE word_id=?',
        (card_json, due, rating, lapse_inc, word_id))
    if cur.rowcount == 0:  # 懒建卡
        conn.execute(
            'INSERT INTO cards(word_id, card, due, created_at, last_rating, reps, lapses) VALUES(?,?,?,?,?,?,?)',
            (word_id, card_json, due, ts, rating, 1, lapse_inc))
    conn.execute('INSERT INTO reviews(word_id, rating, ts, dur_ms, kind, slow) VALUES(?,?,?,?,?,?)',
                 (word_id, rating, ts, dur_ms, kind, slow))
    conn.commit()


def release_from_shelter(conn: sqlite3.Connection, word_id: int, to_lapses: int = 0,
                         due_now: bool = True) -> bool:
    """把词从收容所放回正常队列（缺陷 B2 的出口 + T10 放回即刻可见）。

    收容所原本是单向门：lapses 只增不减，而所有投卡路径都带 `lapses < 阈值`，
    于是进了收容所的词连"秒认"都捞不回来，教师也只能写备注、改不了排期。
    这里提供唯一的出口：把 lapses 压回阈值以下，词即重新进入每日队列。

    due_now：教师是"刚集中讲解完"才点的放回，学生理应下一张就遇到它。
    只压 lapses 不动 due 的话，词会带着当初进收容所时排下的、可能几天后的到期日
    回到队列 —— 教师看到「已放回」、学生几天见不到，这个出口等于虚设。
    """
    r = conn.execute('SELECT card FROM cards WHERE word_id=?', (word_id,)).fetchone()
    if r is None:
        return False
    lapse = max(0, to_lapses)
    if due_now:
        ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
        try:
            card = json.loads(r['card'])
        except (TypeError, ValueError):
            card = {}
        if not isinstance(card, dict):
            card = {}
        card['due'] = ts                      # 与冗余列同步，否则 FSRS 下次读到旧 due
        conn.execute('UPDATE cards SET lapses=?, due=?, card=? WHERE word_id=?',
                     (lapse, ts, json.dumps(card, ensure_ascii=False), word_id))
    else:
        conn.execute('UPDATE cards SET lapses=? WHERE word_id=?', (lapse, word_id))
    conn.commit()
    return True


if __name__ == '__main__':
    c = ensure_ready()
    n = c.execute('SELECT COUNT(*) AS c FROM words').fetchone()['c']
    m = c.execute('SELECT COUNT(*) AS c FROM cards').fetchone()['c']
    f = c.execute('SELECT freq FROM words WHERE freq IS NOT NULL ORDER BY id LIMIT 1').fetchone()
    print(f'db={db_path()}  words={n}  cards={m}  first_freq={f["freq"]}')
    print('word #1:', get_word(c, 1))
    print('word #84:', get_word(c, 84))