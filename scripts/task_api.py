"""Task system API helpers (MVP).

Caller enforces session identity. All dates use Asia/Shanghai calendar days.
"""

from __future__ import annotations

import json
import sqlite3
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")
DEFAULT_WEEKDAY_MINUTES = 40
DEFAULT_WEEKEND_MINUTES = 90
DEFAULT_UNITS_PER_DAY = 1
PACK_TOLERANCE = 1.15
PACK_MODE_TIME_BUDGET = "time_budget"
PACK_MODE_UNITS_PER_DAY = "units_per_day"
PACK_MODES = (PACK_MODE_TIME_BUDGET, PACK_MODE_UNITS_PER_DAY)
UNITS_PREVIEW_DAYS = 14
GENDU_MODULE = "listening_p4_speed"
GENDU_PASS_SCORE = 70
GENDU_DAILY_PRACTICES = 3
GENDU_ASSIGNMENT_DAYS = 30  # starts_on .. starts_on+29 inclusive

READING_SETS = [
    (1, "入门基础篇"),
    (2, "学术核心篇"),
    (3, "阅读高频篇"),
    (4, "动词进阶篇"),
    (5, "形容词扩展篇"),
    (6, "名词辨析篇"),
    (7, "副词强化篇"),
    (8, "因果逻辑篇"),
    (9, "对比转折篇"),
    (10, "程度修饰篇"),
    (11, "时间序列篇"),
    (12, "数量比例篇"),
    (13, "情感态度篇"),
    (14, "科技学术篇"),
    (15, "环境生态篇"),
    (16, "社会文化篇"),
    (17, "经济商业篇"),
    (18, "教育学习篇"),
    (19, "健康医疗篇"),
    (20, "法律政治篇"),
    (21, "艺术媒体篇"),
    (22, "自然科学篇"),
    (23, "综合提升篇"),
]

# Hearing 1000-word bank: 1000 words / 20 per group → 50 units (MVP seed).
DICTATION_GROUP_COUNT = 50
LISTENING_BASIC_GROUP_COUNT = 41
LISTENING_SYNONYM_QUESTION_COUNT = 120
LISTENING_SYNONYM_PER_UNIT = 5
SENTENCE_COUNT = 60
SENTENCE_PER_UNIT = 5
SPEAKING_P2_APPLY_QUESTION_COUNT = 56
SPEAKING_P2_APPLY_PER_UNIT = 5

WRITING_PHRASE_CATEGORIES = [
    ("__foundation__", "基础必背"),
    ("小作文词伙一", "小作文词伙一"),
    ("小作文词伙二", "小作文词伙二"),
    ("小作文词伙三", "小作文词伙三"),
    ("暴力犯罪类", "暴力犯罪类"),
    ("家庭旅游类", "家庭旅游类"),
    ("健康饮食类", "健康饮食类"),
    ("媒体广告类", "媒体广告类"),
    ("能源环保类", "能源环保类"),
    ("品格教育类", "品格教育类"),
    ("人文历史类", "人文历史类"),
    ("商业职场类", "商业职场类"),
    ("网络科技类", "网络科技类"),
    ("政府社会类", "政府社会类"),
]
SPEAKING_COMPLEX_PATTERNS = [f"p{i}" for i in range(1, 8)]
SPEAKING_COMPLEX_ADV = [f"a{i}" for i in range(1, 11)]
SPEAKING_P2_MATERIALS = [
    ("yumeng", "朋友·雨萌"),
    ("sun", "明星·孙颖莎"),
    ("movie", "影视·夏洛特烦恼"),
    ("badminton", "运动·羽毛球"),
    ("bear", "动物·熊"),
    ("basketball", "运动·篮球"),
    ("tianchi", "地点·天池"),
    ("robot", "科技·机器人"),
]
LISTENING_GENDU_LESSONS = [
    ("p1", "C4T1S1", "学校出行"),
    ("p1", "C4T2S1", "学生住宿"),
    ("p1", "C4T3S1", "合租搬家"),
    ("p1", "C4T4S1", "假期安排"),
    ("p1", "C5T1S1", "旅行咨询"),
    ("p1", "C5T2S1", "大学图书馆"),
    ("p1", "C5T3S1", "旅馆咨询"),
    ("p1", "C5T4S1", "住宿登记"),
    ("p1", "C6T1S1", "体育中心"),
    ("p1", "C6T2S1", "博物馆参观"),
    ("p1", "C6T3S1", "开银行账户"),
    ("p1", "C6T4S1", "会议预订"),
    ("p4", "C4T1S4", "城市景观"),
    ("p4", "C4T2S4", "儿童语言"),
    ("p4", "C4T3S4", "鲨鱼"),
    ("p4", "C4T4S4", "斯特拉迪瓦里小提琴"),
    ("p4", "C5T1S4", "职业态度"),
    ("p4", "C5T2S4", "绿色产品"),
    ("p4", "C5T3S4", "电影研究"),
    ("p4", "C5T4S4", "南极"),
    ("p4", "C6T1S4", "气候与冰"),
    ("p4", "C6T2S4", "伊卡洛斯与飞行"),
    ("p4", "C6T3S4", "地图史"),
    ("p4", "C6T4S4", "亚洲狮"),
]
_REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TASK_UNIT_COUNTS = {
    "reading_synonym": 23,
    "dictation": 50,
    "listening_basic": 41,
    "listening_synonym": 24,
    "sentence": 12,
    "writing_phrase": 14,
    "writing_translate": 23,
    "listening_p4_speed": 24,
    "speaking_complex": 17,
    "speaking_p1": 24,
    "speaking_p2_material": 8,
    "speaking_p2_apply": 12,
}


def _task_units_seed_complete(conn: sqlite3.Connection) -> bool:
    rows = conn.execute(
        """
        SELECT module_type, COUNT(*) AS c FROM task_units
        WHERE is_active=1
        GROUP BY module_type
        """
    ).fetchall()
    got = {r["module_type"]: int(r["c"]) for r in rows}
    for mt, n in EXPECTED_TASK_UNIT_COUNTS.items():
        if got.get(mt, 0) < n:
            return False
    return True


def china_ymd(now: Optional[datetime] = None) -> str:
    dt = now or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d")


def is_weekend(ymd: str) -> bool:
    d = datetime.strptime(ymd, "%Y-%m-%d").date()
    return d.weekday() >= 5


def default_effective_from(now: Optional[datetime] = None) -> str:
    """Default pending/draft effective date: tomorrow (Asia/Shanghai)."""
    today = datetime.strptime(china_ymd(now), "%Y-%m-%d").date()
    return (today + timedelta(days=1)).strftime("%Y-%m-%d")


def normalize_effective_from(raw: Any, *, now: Optional[datetime] = None) -> str:
    today = china_ymd(now)
    if raw is None or raw == "":
        return default_effective_from(now)
    if not isinstance(raw, str):
        raise ValueError("生效日期格式应为 YYYY-MM-DD")
    try:
        datetime.strptime(raw, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("生效日期格式应为 YYYY-MM-DD") from exc
    if raw < today:
        raise ValueError("生效日期不能早于今天")
    return raw


def _row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return dict(row)


def ensure_task_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS task_units (
            unit_id TEXT PRIMARY KEY,
            module_type TEXT NOT NULL,
            parent_module TEXT NOT NULL,
            unit_no INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_ref TEXT NOT NULL DEFAULT '{}',
            est_minutes INTEGER NOT NULL DEFAULT 15,
            content_version TEXT NOT NULL DEFAULT '1',
            completion_rule TEXT NOT NULL DEFAULT '',
            study_url TEXT NOT NULL DEFAULT '',
            test_url TEXT NOT NULL DEFAULT '',
            is_active INTEGER NOT NULL DEFAULT 1,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS student_time_profiles (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            weekday_minutes INTEGER NOT NULL DEFAULT 40,
            weekend_minutes INTEGER NOT NULL DEFAULT 90,
            stage_test_every_n INTEGER NOT NULL DEFAULT 3,
            pack_mode TEXT NOT NULL DEFAULT 'time_budget',
            pending_weekday_minutes INTEGER,
            pending_weekend_minutes INTEGER,
            pending_stage_test_every_n INTEGER,
            pending_pack_mode TEXT,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS student_module_daily_quota (
            student_id TEXT NOT NULL REFERENCES students(student_id),
            module_type TEXT NOT NULL,
            weekday_units INTEGER NOT NULL DEFAULT 1,
            weekend_units INTEGER NOT NULL DEFAULT 1,
            pending_weekday_units INTEGER,
            pending_weekend_units INTEGER,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            PRIMARY KEY (student_id, module_type)
        );

        CREATE TABLE IF NOT EXISTS plan_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            sort_order INTEGER NOT NULL DEFAULT 0,
            item_type TEXT NOT NULL CHECK (item_type IN ('study', 'test')),
            unit_id TEXT,
            module_type TEXT NOT NULL DEFAULT '',
            test_unit_ids TEXT NOT NULL DEFAULT '[]',
            test_title TEXT NOT NULL DEFAULT '',
            est_minutes INTEGER,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paused', 'removed')),
            study_completed INTEGER NOT NULL DEFAULT 0,
            study_completed_version TEXT,
            test_passed INTEGER NOT NULL DEFAULT 0,
            test_attempt_count_today INTEGER NOT NULL DEFAULT 0,
            test_attempt_ymd TEXT,
            need_refresh INTEGER NOT NULL DEFAULT 0,
            last_completed_at TEXT,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_plan_items_student
            ON plan_items(student_id, sort_order);

        CREATE TABLE IF NOT EXISTS plan_items_draft (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            sort_order INTEGER NOT NULL DEFAULT 0,
            item_type TEXT NOT NULL CHECK (item_type IN ('study', 'test')),
            unit_id TEXT,
            module_type TEXT NOT NULL DEFAULT '',
            test_unit_ids TEXT NOT NULL DEFAULT '[]',
            test_title TEXT NOT NULL DEFAULT '',
            est_minutes INTEGER,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paused', 'removed')),
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_plan_items_draft_student
            ON plan_items_draft(student_id, sort_order);

        CREATE TABLE IF NOT EXISTS daily_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            task_date TEXT NOT NULL,
            plan_item_id INTEGER NOT NULL REFERENCES plan_items(id),
            priority_class TEXT NOT NULL DEFAULT 'fresh'
                CHECK (priority_class IN ('content_refresh', 'carry_over', 'fresh')),
            sort_in_day INTEGER NOT NULL DEFAULT 0,
            state TEXT NOT NULL DEFAULT 'todo'
                CHECK (state IN ('todo', 'in_progress', 'done_study',
                                 'done_pass', 'done_fail')),
            locked INTEGER NOT NULL DEFAULT 1,
            forced INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            UNIQUE(student_id, task_date, plan_item_id)
        );
        CREATE INDEX IF NOT EXISTS idx_daily_tasks_student_date
            ON daily_tasks(student_id, task_date);

        CREATE TABLE IF NOT EXISTS plan_draft_meta (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            saved_ymd TEXT NOT NULL,
            effective_from TEXT,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS task_unit_progress (
            student_id TEXT NOT NULL,
            plan_item_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            scope_done INTEGER NOT NULL DEFAULT 0,
            scope_total INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            PRIMARY KEY (student_id, plan_item_id)
        );

        CREATE TABLE IF NOT EXISTS student_plan_pause (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            pause_from TEXT NOT NULL,
            resume_on TEXT NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS student_gendu_assignment (
            student_id TEXT PRIMARY KEY REFERENCES students(student_id),
            start_unit_id TEXT NOT NULL,
            current_unit_id TEXT NOT NULL,
            starts_on TEXT NOT NULL,
            ends_on TEXT NOT NULL,
            passed_current INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );

        CREATE TABLE IF NOT EXISTS gendu_practice_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            unit_id TEXT NOT NULL,
            plan_item_id INTEGER,
            task_date TEXT NOT NULL,
            score REAL NOT NULL,
            created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        );
        CREATE INDEX IF NOT EXISTS idx_gendu_practice_student_date
            ON gendu_practice_events(student_id, task_date);
        """
    )
    _migrate_task_effective_columns(conn)
    conn.commit()


def _migrate_task_effective_columns(conn: sqlite3.Connection) -> None:
    tables = {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if "student_time_profiles" in tables:
        cols = {
            r[1]
            for r in conn.execute("PRAGMA table_info(student_time_profiles)").fetchall()
        }
        if "pending_effective_from" not in cols:
            conn.execute(
                "ALTER TABLE student_time_profiles ADD COLUMN pending_effective_from TEXT"
            )
        if "pack_mode" not in cols:
            conn.execute(
                "ALTER TABLE student_time_profiles ADD COLUMN pack_mode TEXT NOT NULL DEFAULT 'time_budget'"
            )
        if "pending_pack_mode" not in cols:
            conn.execute(
                "ALTER TABLE student_time_profiles ADD COLUMN pending_pack_mode TEXT"
            )
    if "student_module_daily_quota" not in tables:
        conn.execute(
            """
            CREATE TABLE student_module_daily_quota (
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT NOT NULL,
                weekday_units INTEGER NOT NULL DEFAULT 1,
                weekend_units INTEGER NOT NULL DEFAULT 1,
                pending_weekday_units INTEGER,
                pending_weekend_units INTEGER,
                updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
                PRIMARY KEY (student_id, module_type)
            )
            """
        )
    if "plan_draft_meta" in tables:
        cols = {
            r[1] for r in conn.execute("PRAGMA table_info(plan_draft_meta)").fetchall()
        }
        if "effective_from" not in cols:
            conn.execute(
                "ALTER TABLE plan_draft_meta ADD COLUMN effective_from TEXT"
            )
    if "student_plan_pause" not in tables:
        conn.execute(
            """
            CREATE TABLE student_plan_pause (
                student_id TEXT PRIMARY KEY REFERENCES students(student_id),
                pause_from TEXT NOT NULL,
                resume_on TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
                updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            )
            """
        )
    if "student_gendu_assignment" not in tables:
        conn.execute(
            """
            CREATE TABLE student_gendu_assignment (
                student_id TEXT PRIMARY KEY REFERENCES students(student_id),
                start_unit_id TEXT NOT NULL,
                current_unit_id TEXT NOT NULL,
                starts_on TEXT NOT NULL,
                ends_on TEXT NOT NULL,
                passed_current INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
                updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            )
            """
        )
    if "gendu_practice_events" not in tables:
        conn.execute(
            """
            CREATE TABLE gendu_practice_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                unit_id TEXT NOT NULL,
                plan_item_id INTEGER,
                task_date TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_gendu_practice_student_date
                ON gendu_practice_events(student_id, task_date)
            """
        )
    if "daily_tasks" in tables:
        dt_cols = {
            r[1] for r in conn.execute("PRAGMA table_info(daily_tasks)").fetchall()
        }
        if "gendu_practice_count" not in dt_cols:
            conn.execute(
                "ALTER TABLE daily_tasks ADD COLUMN gendu_practice_count INTEGER NOT NULL DEFAULT 0"
            )
        if "gendu_best_score" not in dt_cols:
            conn.execute(
                "ALTER TABLE daily_tasks ADD COLUMN gendu_best_score REAL"
            )


def _draft_meta_effective_from(meta: Optional[dict[str, Any]], today: str) -> Optional[str]:
    if not meta:
        return None
    if meta.get("effective_from"):
        return str(meta["effective_from"])
    saved = meta.get("saved_ymd")
    if not saved:
        return default_effective_from()
    if saved < today:
        return today
    saved_day = datetime.strptime(saved, "%Y-%m-%d").date()
    return (saved_day + timedelta(days=1)).strftime("%Y-%m-%d")


def _profile_pending_due(row: dict[str, Any], task_date: str) -> bool:
    has_pending = any(
        row.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
            "pending_pack_mode",
        )
    )
    if not has_pending and not _quotas_have_pending(row.get("module_quotas") or []):
        return False
    eff = row.get("pending_effective_from")
    if eff:
        return str(eff) <= task_date
    updated = (row.get("updated_at") or "")[:10]
    if updated and updated >= task_date:
        return False
    return True


def _quotas_have_pending(quotas: list[dict[str, Any]]) -> bool:
    for q in quotas:
        if q.get("pending_weekday_units") is not None:
            if int(q["pending_weekday_units"]) != int(q.get("weekday_units") or DEFAULT_UNITS_PER_DAY):
                return True
        if q.get("pending_weekend_units") is not None:
            if int(q["pending_weekend_units"]) != int(q.get("weekend_units") or DEFAULT_UNITS_PER_DAY):
                return True
    return False


def _pending_effective_from_summary(
    conn: sqlite3.Connection, student_id: str, *, pending_plan_change: bool
) -> Optional[str]:
    if not pending_plan_change:
        return None
    today = china_ymd()
    dates: list[str] = []
    draft_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=?", (student_id,)
    ).fetchone()["c"]
    if draft_n:
        meta = conn.execute(
            "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
            (student_id,),
        ).fetchone()
        eff = _draft_meta_effective_from(dict(meta) if meta else None, today)
        if eff:
            dates.append(eff)
    tp = ensure_time_profile(conn, student_id)
    if any(
        tp.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
            "pending_pack_mode",
        )
    ) or _quotas_have_pending(tp.get("module_quotas") or []):
        eff = tp.get("pending_effective_from")
        if eff:
            dates.append(str(eff))
        else:
            dates.append(default_effective_from())
    return min(dates) if dates else default_effective_from()


def _upsert_task_unit(
    conn: sqlite3.Connection,
    *,
    unit_id: str,
    module_type: str,
    parent_module: str,
    unit_no: int,
    title: str,
    content_ref: dict[str, Any],
    est_minutes: int,
    completion_rule: str,
    study_url: str,
) -> None:
    conn.execute(
        """
        INSERT INTO task_units (
            unit_id, module_type, parent_module, unit_no, title,
            content_ref, est_minutes, content_version, completion_rule,
            study_url, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, '1', ?, ?, 1)
        ON CONFLICT(unit_id) DO UPDATE SET
            module_type=excluded.module_type,
            parent_module=excluded.parent_module,
            unit_no=excluded.unit_no,
            title=excluded.title,
            content_ref=excluded.content_ref,
            est_minutes=excluded.est_minutes,
            completion_rule=excluded.completion_rule,
            study_url=excluded.study_url,
            is_active=1
        """,
        (
            unit_id,
            module_type,
            parent_module,
            unit_no,
            title,
            json.dumps(content_ref, ensure_ascii=False),
            est_minutes,
            completion_rule,
            study_url,
        ),
    )


def _load_p1_question_keys() -> list[str]:
    path = _REPO_ROOT / "sources" / "kouyulianxi" / "p1-data.js"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    marker = "P1_DATA ="
    i = text.find(marker)
    if i < 0:
        return []
    start = text.find("{", i)
    end = text.rfind("};")
    if start < 0 or end < 0:
        return []
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return []
    keys: list[str] = []
    for cat in data.get("categories") or []:
        cid = cat.get("id")
        for q in cat.get("questions") or []:
            keys.append(f"{cid}:{q.get('id')}")
    return keys


def _load_translation_items() -> list[dict[str, Any]]:
    path = _REPO_ROOT / "sources" / "juzifanyixin" / "translation_data.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def seed_mvp_units(conn: sqlite3.Connection) -> None:
    """Idempotent seed for all task-plan subjects (excludes writing_correction).

    Skips work when all expected module counts are already present — important
    because /api/task/units calls this on every request.
    """
    if _task_units_seed_complete(conn):
        return
    for set_id, name in READING_SETS:
        scope_total = 5 if set_id == 23 else 10
        _upsert_task_unit(
            conn,
            unit_id=f"reading_synonym_u{set_id:02d}",
            module_type="reading_synonym",
            parent_module="reading_synonym",
            unit_no=set_id,
            title=f"单元{set_id} · {name}",
            content_ref={"setId": set_id, "scope_total": scope_total},
            est_minutes=15,
            completion_rule="all_subgroups_once",
            study_url=f"../tongyitihuan/index.html?unit={set_id}",
        )

    for i in range(DICTATION_GROUP_COUNT):
        unit_no = i + 1
        _upsert_task_unit(
            conn,
            unit_id=f"dictation_u{unit_no:02d}",
            module_type="dictation",
            parent_module="dictation",
            unit_no=unit_no,
            title=f"第{unit_no}组",
            content_ref={"groupIndex": i, "scope_total": 20},
            est_minutes=25,
            completion_rule="four_stage_completed",
            study_url=f"listening.html?group={i}",
        )

    for i in range(LISTENING_BASIC_GROUP_COUNT):
        unit_no = i + 1
        _upsert_task_unit(
            conn,
            unit_id=f"listening_basic_u{unit_no:02d}",
            module_type="listening_basic",
            parent_module="listening_basic",
            unit_no=unit_no,
            title=f"第{unit_no}组",
            content_ref={"groupIndex": i, "scope_total": 50},
            est_minutes=35,
            completion_rule="four_stage_completed",
            study_url=f"listening_basic.html?group={i}",
        )

    for i in range(0, LISTENING_SYNONYM_QUESTION_COUNT, LISTENING_SYNONYM_PER_UNIT):
        unit_no = i // LISTENING_SYNONYM_PER_UNIT + 1
        qids = list(range(i + 1, i + LISTENING_SYNONYM_PER_UNIT + 1))
        _upsert_task_unit(
            conn,
            unit_id=f"listening_synonym_u{unit_no:02d}",
            module_type="listening_synonym",
            parent_module="listening_synonym",
            unit_no=unit_no,
            title=f"第{unit_no}单元 · 题{qids[0]}-{qids[-1]}",
            content_ref={
                "questionIds": qids,
                "startId": qids[0],
                "endId": qids[-1],
                "scope_total": len(qids),
            },
            est_minutes=12,
            completion_rule="questions_once",
            study_url=f"../daanjutingxie/index.html?startId={qids[0]}&endId={qids[-1]}",
        )

    for i in range(0, SENTENCE_COUNT, SENTENCE_PER_UNIT):
        unit_no = i // SENTENCE_PER_UNIT + 1
        nums = list(range(i + 1, i + SENTENCE_PER_UNIT + 1))
        _upsert_task_unit(
            conn,
            unit_id=f"sentence_u{unit_no:02d}",
            module_type="sentence",
            parent_module="sentence",
            unit_no=unit_no,
            title=f"第{unit_no}单元 · 句{nums[0]}-{nums[-1]}",
            content_ref={"sentenceNums": nums, "scope_total": len(nums)},
            est_minutes=20,
            completion_rule="sentences_once",
            study_url=f"../changnanju/index.html?from={nums[0]}&to={nums[-1]}",
        )

    for idx, (cat_id, cat_name) in enumerate(WRITING_PHRASE_CATEGORIES, start=1):
        _upsert_task_unit(
            conn,
            unit_id=f"writing_phrase_u{idx:02d}",
            module_type="writing_phrase",
            parent_module="writing_phrase",
            unit_no=idx,
            title=cat_name,
            content_ref={"categoryId": cat_id, "scope_total": 1},
            est_minutes=20,
            completion_rule="category_round_once",
            study_url=f"../xiezuocihuo/index.html?categoryId={cat_id}",
        )

    by_cat: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for it in _load_translation_items():
        cat = str(it.get("category") or "未分类")
        by_cat.setdefault(cat, []).append(it)
    t_no = 0
    for cat, rows in by_cat.items():
        n = len(rows)
        chunks = [rows] if n <= 10 else [rows[j : j + 5] for j in range(0, n, 5)]
        for chunk in chunks:
            t_no += 1
            indexes = [int(x.get("id") or 0) for x in chunk]
            _upsert_task_unit(
                conn,
                unit_id=f"writing_translate_u{t_no:02d}",
                module_type="writing_translate",
                parent_module="writing_translate",
                unit_no=t_no,
                title=f"{cat} · {len(chunk)}句",
                content_ref={
                    "category": cat,
                    "itemIds": indexes,
                    "itemIndexes": list(range(len(chunk))),
                    "scope_total": len(chunk),
                },
                est_minutes=15,
                completion_rule="items_once",
                study_url=(
                    f"../juzifanyixin/index.html?category={cat}"
                    f"&ids={','.join(str(x) for x in indexes)}"
                ),
            )

    for idx, (part, code, topic) in enumerate(LISTENING_GENDU_LESSONS, start=1):
        unit_id = "listening_p4_u01" if code == "C4T1S4" else f"listening_gendu_{code.lower()}"
        _upsert_task_unit(
            conn,
            unit_id=unit_id,
            module_type="listening_p4_speed",
            parent_module="listening_p4_speed",
            unit_no=idx,
            title=f"{'P1' if part == 'p1' else 'P4'} · {code} · {topic}",
            content_ref={"lessonId": code, "part": part, "scope_total": 1},
            est_minutes=15,
            completion_rule="asr_ge_70",
            study_url=f"../P4genduceshi/index.html?lessonId={code}&part={part}",
        )

    c_no = 0
    for pid in SPEAKING_COMPLEX_PATTERNS:
        c_no += 1
        _upsert_task_unit(
            conn,
            unit_id=f"speaking_complex_pattern_{pid}",
            module_type="speaking_complex",
            parent_module="speaking",
            unit_no=c_no,
            title=f"复合句 · 句型{pid}",
            content_ref={"kind": "pattern", "id": pid, "scope_total": 10},
            est_minutes=25,
            completion_rule="three_tracks",
            study_url=f"/kouyulianxi/index.html?part=p1&p1=complex&kind=pattern&id={pid}",
        )
    for aid in SPEAKING_COMPLEX_ADV:
        c_no += 1
        _upsert_task_unit(
            conn,
            unit_id=f"speaking_complex_adv_{aid}",
            module_type="speaking_complex",
            parent_module="speaking",
            unit_no=c_no,
            title=f"复合句 · 词组{aid}",
            content_ref={"kind": "adv", "id": aid, "scope_total": 10},
            est_minutes=25,
            completion_rule="three_tracks",
            study_url=f"/kouyulianxi/index.html?part=p1&p1=complex&kind=adv&id={aid}",
        )

    p1_keys = _load_p1_question_keys()
    if not p1_keys:
        for cat, n in (
            ("shishi", 75),
            ("xihao", 69),
            ("xingwei", 30),
            ("guandian", 31),
            ("duibi", 26),
        ):
            for qid in range(1, n + 1):
                p1_keys.append(f"{cat}:{qid}")
    for i in range(0, len(p1_keys), 10):
        chunk = p1_keys[i : i + 10]
        unit_no = i // 10 + 1
        _upsert_task_unit(
            conn,
            unit_id=f"speaking_p1_u{unit_no:02d}",
            module_type="speaking_p1",
            parent_module="speaking",
            unit_no=unit_no,
            title=f"P1 第{unit_no}单元 · {len(chunk)}题",
            content_ref={"questionKeys": chunk, "scope_total": len(chunk)},
            est_minutes=30,
            completion_rule="questions_practiced",
            study_url="/kouyulianxi/index.html?part=p1&keys=" + ",".join(chunk),
        )

    for idx, (mid, mname) in enumerate(SPEAKING_P2_MATERIALS, start=1):
        _upsert_task_unit(
            conn,
            unit_id=f"speaking_p2_mat_{mid}",
            module_type="speaking_p2_material",
            parent_module="speaking",
            unit_no=idx,
            title=mname,
            content_ref={"materialId": mid, "scope_total": 1},
            est_minutes=20,
            completion_rule="material_once",
            study_url=f"/kouyulianxi/index.html?part=p2&mode=memorize&material={mid}",
        )

    for i in range(0, SPEAKING_P2_APPLY_QUESTION_COUNT, SPEAKING_P2_APPLY_PER_UNIT):
        unit_no = i // SPEAKING_P2_APPLY_PER_UNIT + 1
        indexes = list(
            range(i, min(i + SPEAKING_P2_APPLY_PER_UNIT, SPEAKING_P2_APPLY_QUESTION_COUNT))
        )
        _upsert_task_unit(
            conn,
            unit_id=f"speaking_p2_apply_u{unit_no:02d}",
            module_type="speaking_p2_apply",
            parent_module="speaking",
            unit_no=unit_no,
            title=f"P2套题 第{unit_no}单元 · {len(indexes)}题",
            content_ref={"questionIndexes": indexes, "scope_total": len(indexes)},
            est_minutes=25,
            completion_rule="apply_once",
            study_url=(
                f"/kouyulianxi/index.html?part=p2&mode=apply"
                f"&from={indexes[0]}&to={indexes[-1]}"
            ),
        )

    conn.commit()


def list_units(conn: sqlite3.Connection, module_type: Optional[str] = None) -> list[dict[str, Any]]:
    if module_type:
        rows = conn.execute(
            "SELECT * FROM task_units WHERE is_active=1 AND module_type=? ORDER BY unit_no",
            (module_type,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM task_units WHERE is_active=1 ORDER BY module_type, unit_no"
        ).fetchall()
    out = []
    for row in rows:
        d = dict(row)
        try:
            d["content_ref"] = json.loads(d.get("content_ref") or "{}")
        except json.JSONDecodeError:
            d["content_ref"] = {}
        out.append(d)
    return out


def list_module_quotas(conn: sqlite3.Connection, student_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM student_module_daily_quota WHERE student_id=? ORDER BY module_type",
        (student_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def ensure_module_quota(
    conn: sqlite3.Connection, student_id: str, module_type: str
) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT * FROM student_module_daily_quota
        WHERE student_id=? AND module_type=?
        """,
        (student_id, module_type),
    ).fetchone()
    if row:
        return dict(row)
    conn.execute(
        """
        INSERT INTO student_module_daily_quota (
            student_id, module_type, weekday_units, weekend_units
        ) VALUES (?, ?, ?, ?)
        """,
        (student_id, module_type, DEFAULT_UNITS_PER_DAY, DEFAULT_UNITS_PER_DAY),
    )
    conn.commit()
    return dict(
        conn.execute(
            """
            SELECT * FROM student_module_daily_quota
            WHERE student_id=? AND module_type=?
            """,
            (student_id, module_type),
        ).fetchone()
    )


def _quota_row_units(
    row: Optional[dict[str, Any]],
    task_date: str,
    *,
    prefer_pending: bool = False,
) -> int:
    if not row:
        return DEFAULT_UNITS_PER_DAY
    weekend = is_weekend(task_date)
    if weekend:
        if prefer_pending and row.get("pending_weekend_units") is not None:
            return max(0, int(row["pending_weekend_units"]))
        return max(0, int(row.get("weekend_units") or DEFAULT_UNITS_PER_DAY))
    if prefer_pending and row.get("pending_weekday_units") is not None:
        return max(0, int(row["pending_weekday_units"]))
    return max(0, int(row.get("weekday_units") or DEFAULT_UNITS_PER_DAY))


def _pending_quotas_apply_on(
    conn: sqlite3.Connection, student_id: str, day: str
) -> bool:
    """True when pending module quotas should be used for calendar day ``day``."""
    tp = ensure_time_profile(conn, student_id)
    eff = tp.get("pending_effective_from")
    return bool(eff) and str(day) >= str(eff)


def _resolve_units_quota_map(
    conn: sqlite3.Connection,
    student_id: str,
    day: str,
    plan_items: list[dict[str, Any]],
    *,
    quota_overrides: Optional[dict[str, dict[str, int]]] = None,
    override_from: Optional[str] = None,
) -> dict[str, int]:
    """Live quotas before生效日；生效日及以后用 pending，或教师表单 overrides。"""
    if quota_overrides and override_from and str(day) >= str(override_from):
        return _module_quota_map(
            conn,
            student_id,
            day,
            plan_items,
            quota_overrides=quota_overrides,
            prefer_pending=False,
        )
    return _module_quota_map(
        conn,
        student_id,
        day,
        plan_items,
        prefer_pending=_pending_quotas_apply_on(conn, student_id, day),
    )


def _module_quota_map(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
    plan_items: list[dict[str, Any]],
    *,
    quota_overrides: Optional[dict[str, dict[str, int]]] = None,
    prefer_pending: bool = False,
) -> dict[str, int]:
    """module_type -> units allowed this calendar day."""
    overrides = quota_overrides or {}
    rows = {r["module_type"]: r for r in list_module_quotas(conn, student_id)}
    modules = []
    seen: set[str] = set()
    for it in plan_items:
        mt = str(it.get("module_type") or "other")
        if mt not in seen:
            seen.add(mt)
            modules.append(mt)
    out: dict[str, int] = {}
    for mt in modules:
        ov = overrides.get(mt) or {}
        if is_weekend(task_date):
            if "weekend_units" in ov:
                out[mt] = max(0, int(ov["weekend_units"]))
                continue
        elif "weekday_units" in ov:
            out[mt] = max(0, int(ov["weekday_units"]))
            continue
        out[mt] = _quota_row_units(rows.get(mt), task_date, prefer_pending=prefer_pending)
    return out


def _effective_pack_mode(
    profile: dict[str, Any],
    *,
    mode_override: Optional[str] = None,
    prefer_pending: bool = False,
) -> str:
    if mode_override in PACK_MODES:
        return mode_override
    if prefer_pending and profile.get("pending_pack_mode") in PACK_MODES:
        return str(profile["pending_pack_mode"])
    mode = profile.get("pack_mode") or PACK_MODE_TIME_BUDGET
    return mode if mode in PACK_MODES else PACK_MODE_TIME_BUDGET


def apply_pending_quotas(conn: sqlite3.Connection, student_id: str) -> None:
    rows = list_module_quotas(conn, student_id)
    for row in rows:
        updates = []
        params: list[Any] = []
        if row.get("pending_weekday_units") is not None:
            updates.append("weekday_units=?")
            params.append(row["pending_weekday_units"])
            updates.append("pending_weekday_units=NULL")
        if row.get("pending_weekend_units") is not None:
            updates.append("weekend_units=?")
            params.append(row["pending_weekend_units"])
            updates.append("pending_weekend_units=NULL")
        if updates:
            params.extend([student_id, row["module_type"]])
            conn.execute(
                f"UPDATE student_module_daily_quota SET {', '.join(updates)}, "
                f"updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') "
                f"WHERE student_id=? AND module_type=?",
                params,
            )


def _serialize_quota_rows(rows: list[dict[str, Any]]) -> str:
    return json.dumps(
        [
            {
                "module_type": r.get("module_type"),
                "weekday_units": int(r.get("weekday_units") or DEFAULT_UNITS_PER_DAY),
                "weekend_units": int(r.get("weekend_units") or DEFAULT_UNITS_PER_DAY),
            }
            for r in rows
        ],
        sort_keys=True,
        ensure_ascii=False,
    )


def _quotas_changed(old_rows: list[dict[str, Any]], new_rows: list[dict[str, Any]]) -> bool:
    return _serialize_quota_rows(old_rows) != _serialize_quota_rows(new_rows)


def ensure_time_profile(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM student_time_profiles WHERE student_id=?", (student_id,)
    ).fetchone()
    if row:
        d = dict(row)
        d["pack_mode"] = d.get("pack_mode") or PACK_MODE_TIME_BUDGET
        d["module_quotas"] = list_module_quotas(conn, student_id)
        return d
    conn.execute(
        """
        INSERT INTO student_time_profiles (student_id, weekday_minutes, weekend_minutes)
        VALUES (?, ?, ?)
        """,
        (student_id, DEFAULT_WEEKDAY_MINUTES, DEFAULT_WEEKEND_MINUTES),
    )
    conn.commit()
    d = dict(
        conn.execute(
            "SELECT * FROM student_time_profiles WHERE student_id=?", (student_id,)
        ).fetchone()
    )
    d["pack_mode"] = d.get("pack_mode") or PACK_MODE_TIME_BUDGET
    d["module_quotas"] = list_module_quotas(conn, student_id)
    return d


def apply_pending_profile(conn: sqlite3.Connection, student_id: str, task_date: str) -> None:
    """Merge pending minutes into live fields (call on first access of a new day)."""
    row = ensure_time_profile(conn, student_id)
    updates = []
    params: list[Any] = []
    if row.get("pending_weekday_minutes") is not None:
        updates.append("weekday_minutes=?")
        params.append(row["pending_weekday_minutes"])
        updates.append("pending_weekday_minutes=NULL")
    if row.get("pending_weekend_minutes") is not None:
        updates.append("weekend_minutes=?")
        params.append(row["pending_weekend_minutes"])
        updates.append("pending_weekend_minutes=NULL")
    if row.get("pending_stage_test_every_n") is not None:
        updates.append("stage_test_every_n=?")
        params.append(row["pending_stage_test_every_n"])
        updates.append("pending_stage_test_every_n=NULL")
    if row.get("pending_pack_mode") is not None:
        updates.append("pack_mode=?")
        params.append(row["pending_pack_mode"])
        updates.append("pending_pack_mode=NULL")
    if updates:
        params.append(student_id)
        conn.execute(
            f"UPDATE student_time_profiles SET {', '.join(updates)}, "
            f"updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE student_id=?",
            params,
        )
    apply_pending_quotas(conn, student_id)


def get_time_profile(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    return ensure_time_profile(conn, student_id)


def put_time_profile(
    conn: sqlite3.Connection, student_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Write pending values; effective_from defaults to tomorrow."""
    ensure_time_profile(conn, student_id)
    weekday = payload.get("weekday_minutes")
    weekend = payload.get("weekend_minutes")
    every_n = payload.get("stage_test_every_n")
    pack_mode = payload.get("pack_mode")
    if pack_mode is not None and pack_mode not in PACK_MODES:
        raise ValueError("pack_mode 须为 time_budget 或 units_per_day")
    effective_from = normalize_effective_from(payload.get("effective_from"))
    conn.execute(
        """
        UPDATE student_time_profiles SET
            pending_weekday_minutes = COALESCE(?, pending_weekday_minutes),
            pending_weekend_minutes = COALESCE(?, pending_weekend_minutes),
            pending_stage_test_every_n = COALESCE(?, pending_stage_test_every_n),
            pending_pack_mode = COALESCE(?, pending_pack_mode),
            pending_effective_from = ?,
            updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id = ?
        """,
        (weekday, weekend, every_n, pack_mode, effective_from, student_id),
    )
    module_quotas = payload.get("module_quotas")
    if isinstance(module_quotas, list):
        for q in module_quotas:
            mt = q.get("module_type")
            if not mt:
                continue
            ensure_module_quota(conn, student_id, str(mt))
            wd_u = q.get("weekday_units")
            we_u = q.get("weekend_units")
            conn.execute(
                """
                UPDATE student_module_daily_quota SET
                    pending_weekday_units = COALESCE(?, pending_weekday_units),
                    pending_weekend_units = COALESCE(?, pending_weekend_units),
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
                WHERE student_id=? AND module_type=?
                """,
                (wd_u, we_u, student_id, str(mt)),
            )
    today = china_ymd()
    if payload.get("effective") == "today" or effective_from <= today:
        apply_pending_profile(conn, student_id, today)
        conn.execute(
            "UPDATE student_time_profiles SET pending_effective_from=NULL WHERE student_id=?",
            (student_id,),
        )
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, today),
        )
    conn.commit()
    return get_time_profile(conn, student_id)


def _parse_json_list(raw: Any) -> list[Any]:
    if isinstance(raw, list):
        return raw
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _plan_progress(conn: sqlite3.Connection, student_id: str) -> dict[str, dict[str, int]]:
    """module_type -> {study_x, study_y, pass_a, pass_b}."""
    rows = conn.execute(
        """
        SELECT module_type, item_type, status, study_completed, test_passed
        FROM plan_items WHERE student_id=? AND status!='removed'
        """,
        (student_id,),
    ).fetchall()
    prog: dict[str, dict[str, int]] = {}
    for row in rows:
        mt = row["module_type"] or ""
        if mt not in prog:
            prog[mt] = {"study_x": 0, "study_y": 0, "pass_a": 0, "pass_b": 0}
        if row["item_type"] == "study":
            prog[mt]["study_y"] += 1
            if row["study_completed"]:
                prog[mt]["study_x"] += 1
        elif row["item_type"] == "test":
            prog[mt]["pass_b"] += 1
            if row["test_passed"]:
                prog[mt]["pass_a"] += 1
    return prog


def effective_plan_status(conn: sqlite3.Connection, student_id: str) -> str:
    """none | all_paused | active (D28). Schedule pause → all_paused while active."""
    expire_plan_pause_if_due(conn, student_id)
    if is_plan_schedule_paused(conn, student_id, china_ymd()):
        rows = conn.execute(
            "SELECT 1 FROM plan_items WHERE student_id=? AND status!='removed' LIMIT 1",
            (student_id,),
        ).fetchone()
        return "all_paused" if rows else "none"
    rows = conn.execute(
        "SELECT status FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchall()
    if not rows:
        return "none"
    if all(r["status"] == "paused" for r in rows):
        return "all_paused"
    if any(r["status"] == "pending" for r in rows):
        return "active"
    return "all_paused"


def _parse_ymd_strict(raw: Any, *, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} 须为 YYYY-MM-DD")
    try:
        datetime.strptime(raw.strip(), "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field} 须为 YYYY-MM-DD") from exc
    return raw.strip()


def get_plan_pause(
    conn: sqlite3.Connection, student_id: str, *, on_date: Optional[str] = None
) -> Optional[dict[str, Any]]:
    """Return pause row enriched with active/upcoming flags, or None."""
    expire_plan_pause_if_due(conn, student_id, on_date=on_date)
    row = conn.execute(
        "SELECT * FROM student_plan_pause WHERE student_id=?",
        (student_id,),
    ).fetchone()
    if not row:
        return None
    d = dict(row)
    day = on_date or china_ymd()
    pause_from = str(d["pause_from"])
    resume_on = str(d["resume_on"])
    d["active"] = pause_from <= day < resume_on
    d["upcoming"] = pause_from > day
    return d


def is_plan_schedule_paused(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> bool:
    pause = get_plan_pause(conn, student_id, on_date=task_date)
    return bool(pause and pause.get("active"))


def expire_plan_pause_if_due(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    on_date: Optional[str] = None,
) -> bool:
    """Auto-clear pause when resume_on has arrived. Returns True if cleared."""
    day = on_date or china_ymd()
    row = conn.execute(
        "SELECT resume_on FROM student_plan_pause WHERE student_id=?",
        (student_id,),
    ).fetchone()
    if not row:
        return False
    if str(row["resume_on"]) <= day:
        conn.execute("DELETE FROM student_plan_pause WHERE student_id=?", (student_id,))
        conn.commit()
        return True
    return False


def put_plan_pause(
    conn: sqlite3.Connection, student_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Set / replace schedule pause. reason required; resume_on > pause_from >= today."""
    ensure_task_tables(conn)
    today = china_ymd()
    pause_from = _parse_ymd_strict(payload.get("pause_from"), field="暂停起始日")
    resume_on = _parse_ymd_strict(payload.get("resume_on"), field="恢复日期")
    reason = str(payload.get("reason") or "").strip()
    if not reason:
        raise ValueError("请填写暂停原因")
    if len(reason) > 500:
        raise ValueError("暂停原因请控制在 500 字以内")
    if pause_from < today:
        raise ValueError("暂停起始日不能早于今天")
    if resume_on <= pause_from:
        raise ValueError("恢复日期须晚于暂停起始日")
    live_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchone()["c"]
    if live_n < 1:
        raise ValueError("该生尚无生效清单，无法暂停")
    conn.execute(
        """
        INSERT INTO student_plan_pause (student_id, pause_from, resume_on, reason, updated_at)
        VALUES (?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        ON CONFLICT(student_id) DO UPDATE SET
            pause_from=excluded.pause_from,
            resume_on=excluded.resume_on,
            reason=excluded.reason,
            updated_at=excluded.updated_at
        """,
        (student_id, pause_from, resume_on, reason),
    )
    # Clear daily tasks inside the pause window from today forward.
    clear_from = max(pause_from, today)
    conn.execute(
        """
        DELETE FROM daily_tasks
        WHERE student_id=? AND task_date>=? AND task_date<?
        """,
        (student_id, clear_from, resume_on),
    )
    conn.commit()
    return get_plan(conn, student_id)


def clear_plan_pause(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    """Cancel pause early (resume immediately)."""
    conn.execute("DELETE FROM student_plan_pause WHERE student_id=?", (student_id,))
    conn.commit()
    return get_plan(conn, student_id)


# --- Listening gendu (跟读) assignment ---------------------------------------

def _ymd_plus_days(ymd: str, days: int) -> str:
    return (
        datetime.strptime(ymd, "%Y-%m-%d").date() + timedelta(days=days)
    ).strftime("%Y-%m-%d")


def _gendu_unit_or_raise(conn: sqlite3.Connection, unit_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM task_units WHERE unit_id=? AND is_active=1", (unit_id,)
    ).fetchone()
    if not row:
        raise ValueError("跟读单元不存在")
    if str(row["module_type"]) != GENDU_MODULE:
        raise ValueError("请选择听力跟读单元")
    return dict(row)


def _next_gendu_unit_id(
    conn: sqlite3.Connection, current_unit_id: str
) -> Optional[str]:
    cur = conn.execute(
        "SELECT unit_no FROM task_units WHERE unit_id=? AND module_type=?",
        (current_unit_id, GENDU_MODULE),
    ).fetchone()
    if not cur:
        return None
    nxt = conn.execute(
        """
        SELECT unit_id FROM task_units
        WHERE module_type=? AND is_active=1 AND unit_no>?
        ORDER BY unit_no LIMIT 1
        """,
        (GENDU_MODULE, int(cur["unit_no"])),
    ).fetchone()
    return str(nxt["unit_id"]) if nxt else None


def _ensure_gendu_plan_item(
    conn: sqlite3.Connection, student_id: str, unit_id: str
) -> int:
    """Ensure one pending live plan_item for the current gendu unit; soft-remove others."""
    unit = _gendu_unit_or_raise(conn, unit_id)
    conn.execute(
        """
        UPDATE plan_items SET status='removed',
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id=? AND module_type=? AND item_type='study'
          AND status='pending' AND unit_id!=?
        """,
        (student_id, GENDU_MODULE, unit_id),
    )
    existing = conn.execute(
        """
        SELECT id FROM plan_items
        WHERE student_id=? AND unit_id=? AND item_type='study' AND status='pending'
        ORDER BY id DESC LIMIT 1
        """,
        (student_id, unit_id),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE plan_items SET
                study_completed=0,
                study_completed_version=NULL,
                need_refresh=0,
                module_type=?,
                est_minutes=?,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE id=?
            """,
            (GENDU_MODULE, int(unit.get("est_minutes") or 15), int(existing["id"])),
        )
        return int(existing["id"])
    max_so = conn.execute(
        "SELECT COALESCE(MAX(sort_order), -1) AS m FROM plan_items WHERE student_id=?",
        (student_id,),
    ).fetchone()["m"]
    cur = conn.execute(
        """
        INSERT INTO plan_items (
            student_id, sort_order, item_type, unit_id, module_type,
            est_minutes, status, study_completed
        ) VALUES (?, ?, 'study', ?, ?, ?, 'pending', 0)
        """,
        (
            student_id,
            int(max_so) + 1,
            unit_id,
            GENDU_MODULE,
            int(unit.get("est_minutes") or 15),
        ),
    )
    return int(cur.lastrowid)


def _raw_gendu_assignment(
    conn: sqlite3.Connection, student_id: str
) -> Optional[dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM student_gendu_assignment WHERE student_id=?",
        (student_id,),
    ).fetchone()
    return dict(row) if row else None


def get_gendu_assignment(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    on_date: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    ensure_task_tables(conn)
    row = _raw_gendu_assignment(conn, student_id)
    if not row:
        return None
    day = on_date or china_ymd()
    starts_on = str(row["starts_on"])
    ends_on = str(row["ends_on"])
    unit = conn.execute(
        "SELECT title, unit_no FROM task_units WHERE unit_id=?",
        (row["current_unit_id"],),
    ).fetchone()
    start_unit = conn.execute(
        "SELECT title, unit_no FROM task_units WHERE unit_id=?",
        (row["start_unit_id"],),
    ).fetchone()
    out = dict(row)
    out["passed_current"] = bool(row.get("passed_current"))
    out["active"] = starts_on <= day <= ends_on
    out["upcoming"] = starts_on > day
    out["expired"] = day > ends_on
    out["current_title"] = (unit["title"] if unit else "") or row["current_unit_id"]
    out["current_unit_no"] = int(unit["unit_no"]) if unit else None
    out["start_title"] = (start_unit["title"] if start_unit else "") or row["start_unit_id"]
    out["daily_required"] = GENDU_DAILY_PRACTICES
    out["pass_score"] = GENDU_PASS_SCORE
    return out


def put_gendu_assignment(
    conn: sqlite3.Connection, student_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Teacher starts / resets a 30-day gendu assignment from a chosen unit."""
    ensure_task_tables(conn)
    seed_mvp_units(conn)
    start_unit_id = str(payload.get("start_unit_id") or "").strip()
    if not start_unit_id:
        raise ValueError("请选择起始跟读课")
    _gendu_unit_or_raise(conn, start_unit_id)
    today = china_ymd()
    starts_on = payload.get("starts_on")
    if starts_on:
        starts_on = _parse_ymd_strict(starts_on, field="开始日期")
    else:
        starts_on = today
    ends_on = _ymd_plus_days(starts_on, GENDU_ASSIGNMENT_DAYS - 1)
    conn.execute(
        """
        INSERT INTO student_gendu_assignment (
            student_id, start_unit_id, current_unit_id, starts_on, ends_on,
            passed_current, updated_at
        ) VALUES (?, ?, ?, ?, ?, 0, strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        ON CONFLICT(student_id) DO UPDATE SET
            start_unit_id=excluded.start_unit_id,
            current_unit_id=excluded.current_unit_id,
            starts_on=excluded.starts_on,
            ends_on=excluded.ends_on,
            passed_current=0,
            updated_at=excluded.updated_at
        """,
        (student_id, start_unit_id, start_unit_id, starts_on, ends_on),
    )
    _ensure_gendu_plan_item(conn, student_id, start_unit_id)
    # Rebuild today's pack if already materialized
    conn.execute(
        "DELETE FROM daily_tasks WHERE student_id=? AND task_date>=?",
        (student_id, today),
    )
    conn.commit()
    asg = get_gendu_assignment(conn, student_id)
    return {"gendu_assignment": asg, "plan": get_plan(conn, student_id)}


def clear_gendu_assignment(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    ensure_task_tables(conn)
    conn.execute(
        "DELETE FROM student_gendu_assignment WHERE student_id=?", (student_id,)
    )
    conn.execute(
        """
        UPDATE plan_items SET status='removed',
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id=? AND module_type=? AND status='pending'
        """,
        (student_id, GENDU_MODULE),
    )
    today = china_ymd()
    conn.execute(
        """
        DELETE FROM daily_tasks
        WHERE student_id=? AND task_date>=?
          AND plan_item_id IN (
            SELECT id FROM plan_items WHERE student_id=? AND module_type=?
          )
        """,
        (student_id, today, student_id, GENDU_MODULE),
    )
    conn.commit()
    return {"gendu_assignment": None, "plan": get_plan(conn, student_id)}


def advance_gendu_if_needed(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> bool:
    """If current lesson passed (≥70%), advance pointer for this calendar day."""
    asg = _raw_gendu_assignment(conn, student_id)
    if not asg or not int(asg.get("passed_current") or 0):
        return False
    starts_on = str(asg["starts_on"])
    ends_on = str(asg["ends_on"])
    if task_date < starts_on or task_date > ends_on:
        return False
    # Advance only on a day after the pass was recorded (次日起).
    # If daily tasks for today already exist for current unit, wait — but when
    # building a new day, passed_current means yesterday (or earlier) hit 70%.
    # Heuristic: if today already has a daily_task for current unit with practices,
    # don't advance mid-day. Only advance when materializing a fresh day OR when
    # no daily row yet for current unit today.
    current_unit = str(asg["current_unit_id"])
    today_row = conn.execute(
        """
        SELECT d.id, d.gendu_practice_count
        FROM daily_tasks d
        JOIN plan_items p ON p.id = d.plan_item_id
        WHERE d.student_id=? AND d.task_date=? AND p.unit_id=?
        LIMIT 1
        """,
        (student_id, task_date, current_unit),
    ).fetchone()
    if today_row and int(today_row["gendu_practice_count"] or 0) > 0:
        return False
    # If today already locked with this unit and count=0, still advance if passed
    # (new day, not yet practiced). If locked mid-day from earlier materialize
    # before pass, rematerialize is rare — delete today's gendu daily and advance.
    next_id = _next_gendu_unit_id(conn, current_unit)
    if not next_id:
        # Last lesson: keep practicing until ends_on; clear flag so we don't loop.
        conn.execute(
            """
            UPDATE student_gendu_assignment SET passed_current=0,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE student_id=?
            """,
            (student_id,),
        )
        conn.commit()
        return False
    # Complete old plan item(s) for current unit
    conn.execute(
        """
        UPDATE plan_items SET study_completed=1,
            last_completed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id=? AND unit_id=? AND item_type='study' AND status='pending'
        """,
        (student_id, current_unit),
    )
    conn.execute(
        """
        DELETE FROM daily_tasks
        WHERE student_id=? AND task_date=?
          AND plan_item_id IN (
            SELECT id FROM plan_items WHERE student_id=? AND unit_id=?
          )
        """,
        (student_id, task_date, student_id, current_unit),
    )
    conn.execute(
        """
        UPDATE student_gendu_assignment SET
            current_unit_id=?, passed_current=0,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id=?
        """,
        (next_id, student_id),
    )
    _ensure_gendu_plan_item(conn, student_id, next_id)
    conn.commit()
    return True


def _gendu_aware_plan_items(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
    plan_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """When assignment active, only current gendu unit; when expired/upcoming, drop gendu."""
    advance_gendu_if_needed(conn, student_id, task_date)
    asg = _raw_gendu_assignment(conn, student_id)
    if not asg:
        return plan_items
    starts_on = str(asg["starts_on"])
    ends_on = str(asg["ends_on"])
    non_gendu = [
        it for it in plan_items if str(it.get("module_type") or "") != GENDU_MODULE
    ]
    if task_date < starts_on or task_date > ends_on:
        return non_gendu
    current_unit = str(asg["current_unit_id"])
    pid = _ensure_gendu_plan_item(conn, student_id, current_unit)
    row = conn.execute(
        """
        SELECT p.*, u.title AS unit_title
        FROM plan_items p
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE p.id=?
        """,
        (pid,),
    ).fetchone()
    if not row:
        return non_gendu
    item = dict(row)
    # Keep current lesson packable until pointer advances
    item["study_completed"] = 0
    return non_gendu + [item]


def report_gendu_practice(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    plan_item_id: int,
    score: float,
    task_date: Optional[str] = None,
) -> dict[str, Any]:
    """Record one follow-read attempt; day done at 3; pass (≥70%) unlocks next-day advance."""
    ensure_task_tables(conn)
    task_date = task_date or china_ymd()
    try:
        score_f = float(score)
    except (TypeError, ValueError) as exc:
        raise ValueError("识别率无效") from exc
    if score_f < 0 or score_f > 100:
        raise ValueError("识别率须在 0–100")
    asg = _raw_gendu_assignment(conn, student_id)
    if not asg:
        raise ValueError("尚未安排听力跟读作业")
    if not (str(asg["starts_on"]) <= task_date <= str(asg["ends_on"])):
        raise ValueError("跟读作业不在有效期内")
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    if str(item["module_type"]) != GENDU_MODULE:
        raise ValueError("非听力跟读任务")
    if str(item["unit_id"]) != str(asg["current_unit_id"]):
        raise ValueError("请跟读当前指定课文")
    # Ensure today's daily row exists
    build_daily_tasks(conn, student_id, task_date)
    daily = conn.execute(
        """
        SELECT * FROM daily_tasks
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (student_id, task_date, plan_item_id),
    ).fetchone()
    if not daily:
        raise ValueError("今日未安排该跟读任务")
    conn.execute(
        """
        INSERT INTO gendu_practice_events
            (student_id, unit_id, plan_item_id, task_date, score)
        VALUES (?, ?, ?, ?, ?)
        """,
        (student_id, item["unit_id"], plan_item_id, task_date, score_f),
    )
    count = int(daily["gendu_practice_count"] or 0) + 1
    best = daily["gendu_best_score"]
    best_f = score_f if best is None else max(float(best), score_f)
    new_state = daily["state"]
    if count >= GENDU_DAILY_PRACTICES and new_state not in ("done_study", "done_pass"):
        new_state = "done_study"
    conn.execute(
        """
        UPDATE daily_tasks SET
            gendu_practice_count=?,
            gendu_best_score=?,
            state=?
        WHERE id=?
        """,
        (count, best_f, new_state, int(daily["id"])),
    )
    if score_f >= GENDU_PASS_SCORE:
        conn.execute(
            """
            UPDATE student_gendu_assignment SET passed_current=1,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE student_id=?
            """,
            (student_id,),
        )
    conn.commit()
    today_data = get_today(conn, student_id) if task_date == china_ymd() else {
        "items": _enrich_daily(conn, student_id, task_date),
        "gendu_assignment": get_gendu_assignment(conn, student_id, on_date=task_date),
    }
    return {
        "practice_count": count,
        "required": GENDU_DAILY_PRACTICES,
        "best_score": best_f,
        "day_complete": count >= GENDU_DAILY_PRACTICES,
        "passed_lesson": score_f >= GENDU_PASS_SCORE
        or bool(_raw_gendu_assignment(conn, student_id).get("passed_current")),
        "today": today_data,
    }


def get_plan(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    maybe_apply_pending_for_today(conn, student_id, china_ymd())
    live = [
        dict(r)
        for r in conn.execute(
            """
            SELECT p.*, u.title AS unit_title, u.content_ref, u.content_version,
                   u.study_url, u.est_minutes AS unit_est_minutes
            FROM plan_items p
            LEFT JOIN task_units u ON u.unit_id = p.unit_id
            WHERE p.student_id=? AND p.status!='removed'
            ORDER BY p.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    draft = [
        dict(r)
        for r in conn.execute(
            """
            SELECT d.*, u.title AS unit_title
            FROM plan_items_draft d
            LEFT JOIN task_units u ON u.unit_id = d.unit_id
            WHERE d.student_id=? AND d.status!='removed'
            ORDER BY d.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    for item in live + draft:
        item["test_unit_ids"] = _parse_json_list(item.get("test_unit_ids"))
        if item.get("content_ref"):
            try:
                item["content_ref"] = json.loads(item["content_ref"])
            except (json.JSONDecodeError, TypeError):
                pass
    tp = get_time_profile(conn, student_id)
    pending_change = bool(draft) or _profile_has_real_pending(tp)
    draft_order_issues = _stage_test_order_issues(draft) if draft else []
    today = china_ymd()
    meta_row = conn.execute(
        "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
        (student_id,),
    ).fetchone()
    meta = dict(meta_row) if meta_row else None
    draft_effective_from = (
        _draft_meta_effective_from(meta, today) if draft else None
    )
    pending_profile_effective_from = (
        tp.get("pending_effective_from")
        if _profile_has_real_pending(tp)
        else None
    )
    return {
        "live": live,
        "draft": draft,
        "draft_pending": bool(draft),
        "progress": _plan_progress(conn, student_id),
        "plan_status": effective_plan_status(conn, student_id),
        "plan_pause": get_plan_pause(conn, student_id),
        "pending_plan_change": pending_change,
        "draft_effective_from": draft_effective_from,
        "pending_profile_effective_from": pending_profile_effective_from,
        "pending_effective_from": _pending_effective_from_summary(
            conn, student_id, pending_plan_change=pending_change
        ),
        "draft_order_issues": draft_order_issues,
        "time_profile": tp,
        "gendu_assignment": get_gendu_assignment(conn, student_id),
    }


def _profile_has_real_pending(tp: dict[str, Any]) -> bool:
    if tp.get("pending_pack_mode") is not None:
        if str(tp["pending_pack_mode"]) != str(tp.get("pack_mode") or PACK_MODE_TIME_BUDGET):
            return True
    if tp.get("pending_weekday_minutes") is not None:
        if int(tp["pending_weekday_minutes"]) != int(tp.get("weekday_minutes") or 0):
            return True
    if tp.get("pending_weekend_minutes") is not None:
        if int(tp["pending_weekend_minutes"]) != int(tp.get("weekend_minutes") or 0):
            return True
    if tp.get("pending_stage_test_every_n") is not None:
        if int(tp["pending_stage_test_every_n"]) != int(tp.get("stage_test_every_n") or 0):
            return True
    if _quotas_have_pending(tp.get("module_quotas") or []):
        return True
    return False


def _study_unit_ids_in_plan(conn: sqlite3.Connection, student_id: str, table: str) -> set[str]:
    rows = conn.execute(
        f"""
        SELECT unit_id FROM {table}
        WHERE student_id=? AND item_type='study' AND status!='removed' AND unit_id IS NOT NULL
        """,
        (student_id,),
    ).fetchall()
    return {r["unit_id"] for r in rows if r["unit_id"]}


def put_plan_draft(
    conn: sqlite3.Connection,
    student_id: str,
    items: list[dict[str, Any]],
    *,
    effective_from: Optional[str] = None,
) -> dict[str, Any]:
    """Replace draft list. Enforces D26 unique unit_id for study items."""
    seen: set[str] = set()
    for it in items:
        if it.get("item_type") == "study" and it.get("status", "pending") != "removed":
            uid = it.get("unit_id")
            if not uid:
                raise ValueError("study 条目必须有 unit_id")
            if uid in seen:
                raise ValueError(f"该单元已在计划中: {uid}")
            seen.add(uid)
            unit = conn.execute(
                "SELECT unit_id, module_type FROM task_units WHERE unit_id=?", (uid,)
            ).fetchone()
            if not unit:
                raise ValueError(f"未知单元: {uid}")

    items = normalize_stage_test_positions(items)
    conn.execute("DELETE FROM plan_items_draft WHERE student_id=?", (student_id,))
    for idx, it in enumerate(items):
        item_type = it.get("item_type") or "study"
        unit_id = it.get("unit_id")
        module_type = it.get("module_type") or ""
        if item_type == "study" and unit_id:
            u = conn.execute(
                "SELECT module_type, est_minutes FROM task_units WHERE unit_id=?", (unit_id,)
            ).fetchone()
            if u:
                module_type = u["module_type"]
        status = it.get("status") or "pending"
        conn.execute(
            """
            INSERT INTO plan_items_draft (
                student_id, sort_order, item_type, unit_id, module_type,
                test_unit_ids, test_title, est_minutes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                idx,
                item_type,
                unit_id,
                module_type,
                json.dumps(it.get("test_unit_ids") or [], ensure_ascii=False),
                it.get("test_title") or "",
                it.get("est_minutes"),
                status,
            ),
        )
    eff_ymd = normalize_effective_from(effective_from)
    conn.execute(
        """
        INSERT INTO plan_draft_meta (student_id, saved_ymd, effective_from)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            saved_ymd=excluded.saved_ymd,
            effective_from=excluded.effective_from,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        """,
        (student_id, china_ymd(), eff_ymd),
    )
    # First plan (live empty): apply immediately so student is not stuck a day with no tasks.
    live_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchone()["c"]
    today = china_ymd()
    if live_n == 0 or eff_ymd <= today:
        apply_draft_to_live(conn, student_id)
        conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
        if eff_ymd == today and live_n > 0:
            conn.execute(
                "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
                (student_id, today),
            )
    conn.commit()
    # Belt-and-suspenders: due drafts/profile must merge even if caller skipped the branch.
    maybe_apply_pending_for_today(conn, student_id, today)
    return get_plan(conn, student_id)


def apply_draft_to_live(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    """Promote draft → live. Preserves completion state for matching unit_id study items."""
    draft = conn.execute(
        "SELECT * FROM plan_items_draft WHERE student_id=? ORDER BY sort_order",
        (student_id,),
    ).fetchall()
    if not draft:
        return get_plan(conn, student_id)

    old = {
        r["unit_id"]: dict(r)
        for r in conn.execute(
            """
            SELECT * FROM plan_items
            WHERE student_id=? AND item_type='study' AND unit_id IS NOT NULL
            """,
            (student_id,),
        ).fetchall()
        if r["unit_id"]
    }

    # Soft-remove live rows not in draft (keep history for backlog refs: mark removed)
    conn.execute(
        "UPDATE plan_items SET status='removed', updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') "
        "WHERE student_id=? AND status!='removed'",
        (student_id,),
    )

    for idx, d in enumerate(draft):
        d = dict(d)
        unit_id = d.get("unit_id")
        prev = old.get(unit_id) if d["item_type"] == "study" and unit_id else None
        conn.execute(
            """
            INSERT INTO plan_items (
                student_id, sort_order, item_type, unit_id, module_type,
                test_unit_ids, test_title, est_minutes, status,
                study_completed, study_completed_version, test_passed,
                need_refresh
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                student_id,
                idx,
                d["item_type"],
                unit_id,
                d["module_type"],
                d.get("test_unit_ids") or "[]",
                d.get("test_title") or "",
                d.get("est_minutes"),
                d.get("status") or "pending",
                (prev or {}).get("study_completed") or 0,
                (prev or {}).get("study_completed_version"),
                0 if d["item_type"] == "test" else 0,
            ),
        )

    conn.execute("DELETE FROM plan_items_draft WHERE student_id=?", (student_id,))
    conn.commit()
    return get_plan(conn, student_id)


def maybe_apply_pending_for_today(conn: sqlite3.Connection, student_id: str, task_date: str) -> None:
    """On first access of task_date: merge profile/draft pending if effective_from is due."""
    row = ensure_time_profile(conn, student_id)
    # Drop stale pending_* that equal live (avoids false「待生效」banner).
    if not _profile_has_real_pending(row) and any(
        row.get(k) is not None
        for k in (
            "pending_weekday_minutes",
            "pending_weekend_minutes",
            "pending_stage_test_every_n",
            "pending_pack_mode",
            "pending_effective_from",
        )
    ):
        conn.execute(
            """
            UPDATE student_time_profiles SET
                pending_weekday_minutes=NULL,
                pending_weekend_minutes=NULL,
                pending_stage_test_every_n=NULL,
                pending_pack_mode=NULL,
                pending_effective_from=NULL,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE student_id=?
            """,
            (student_id,),
        )
        conn.execute(
            """
            UPDATE student_module_daily_quota SET
                pending_weekday_units=NULL,
                pending_weekend_units=NULL,
                updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
            WHERE student_id=?
            """,
            (student_id,),
        )
        row = ensure_time_profile(conn, student_id)
    if _profile_pending_due(row, task_date):
        old_wd = int(row["weekday_minutes"])
        old_we = int(row["weekend_minutes"])
        old_mode = row.get("pack_mode") or PACK_MODE_TIME_BUDGET
        old_quotas = list_module_quotas(conn, student_id)
        apply_pending_profile(conn, student_id, task_date)
        conn.execute(
            "UPDATE student_time_profiles SET pending_effective_from=NULL WHERE student_id=?",
            (student_id,),
        )
        merged = ensure_time_profile(conn, student_id)
        schedule_changed = (
            int(merged["weekday_minutes"]) != old_wd
            or int(merged["weekend_minutes"]) != old_we
            or (merged.get("pack_mode") or PACK_MODE_TIME_BUDGET) != old_mode
            or _quotas_changed(old_quotas, merged.get("module_quotas") or [])
        )
        if schedule_changed:
            conn.execute(
                "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
                (student_id, task_date),
            )
    draft_count = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=?", (student_id,)
    ).fetchone()["c"]
    if not draft_count:
        # Orphan meta without draft rows
        conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
        conn.commit()
        return
    meta = conn.execute(
        "SELECT saved_ymd, effective_from FROM plan_draft_meta WHERE student_id=?",
        (student_id,),
    ).fetchone()
    eff = _draft_meta_effective_from(dict(meta) if meta else None, task_date)
    if not eff or eff > task_date:
        conn.commit()
        return
    apply_draft_to_live(conn, student_id)
    conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
    if eff == task_date:
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, task_date),
        )
    conn.commit()


def _budget_minutes(
    profile: dict[str, Any],
    task_date: str,
    *,
    weekday_override: Optional[int] = None,
    weekend_override: Optional[int] = None,
    prefer_pending: bool = False,
) -> int:
    """Resolve daily pack budget; overrides (teacher form) win over pending/live."""
    weekend = is_weekend(task_date)
    if weekend:
        if weekend_override is not None:
            return max(0, int(weekend_override))
        if prefer_pending and profile.get("pending_weekend_minutes") is not None:
            return int(profile["pending_weekend_minutes"])
        return int(profile["weekend_minutes"])
    if weekday_override is not None:
        return max(0, int(weekday_override))
    if prefer_pending and profile.get("pending_weekday_minutes") is not None:
        return int(profile["pending_weekday_minutes"])
    return int(profile["weekday_minutes"])


def _est_minutes(conn: sqlite3.Connection, plan_item: dict[str, Any]) -> int:
    if plan_item.get("est_minutes"):
        return int(plan_item["est_minutes"])
    if plan_item.get("unit_id"):
        u = conn.execute(
            "SELECT est_minutes FROM task_units WHERE unit_id=?", (plan_item["unit_id"],)
        ).fetchone()
        if u:
            return int(u["est_minutes"])
    return 15 if plan_item.get("item_type") == "study" else 20


def _item_done(item: dict[str, Any]) -> bool:
    if item.get("item_type") == "study":
        return bool(item.get("study_completed"))
    return bool(item.get("test_passed"))


def backlog_plan_item_ids(conn: sqlite3.Connection, student_id: str) -> list[int]:
    """D23: items that appeared in some daily_tasks and are still unfinished."""
    rows = conn.execute(
        """
        SELECT DISTINCT d.plan_item_id
        FROM daily_tasks d
        JOIN plan_items p ON p.id = d.plan_item_id
        WHERE d.student_id=?
          AND p.status != 'removed'
          AND (
            (p.item_type='study' AND p.study_completed=0)
            OR (p.item_type='test' AND p.test_passed=0)
          )
        ORDER BY d.task_date, d.sort_in_day
        """,
        (student_id,),
    ).fetchall()
    return [r["plan_item_id"] for r in rows]


def _session_study_date_expr() -> str:
    return "date(COALESCE(ended_at, created_at), '+8 hours')"


def sum_today_study_seconds(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
) -> int:
    try:
        row = conn.execute(
            f"""
            SELECT COALESCE(SUM(duration_seconds), 0) AS total
            FROM study_sessions
            WHERE student_id=?
              AND session_kind='study'
              AND {_session_study_date_expr()} = ?
            """,
            (student_id, task_date),
        ).fetchone()
        return int(row["total"] or 0) if row else 0
    except sqlite3.OperationalError:
        return 0


def sum_total_study_seconds(conn: sqlite3.Connection, student_id: str) -> int:
    try:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(duration_seconds), 0) AS total
            FROM study_sessions
            WHERE student_id=?
              AND session_kind='study'
            """,
            (student_id,),
        ).fetchone()
        return int(row["total"] or 0) if row else 0
    except sqlite3.OperationalError:
        return 0


def sum_today_study_by_plan_item(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
) -> dict[int, int]:
    try:
        rows = conn.execute(
            f"""
            SELECT plan_item_id, COALESCE(SUM(duration_seconds), 0) AS total
            FROM study_sessions
            WHERE student_id=?
              AND session_kind='study'
              AND plan_item_id IS NOT NULL
              AND {_session_study_date_expr()} = ?
            GROUP BY plan_item_id
            """,
            (student_id, task_date),
        ).fetchall()
        return {int(r["plan_item_id"]): int(r["total"]) for r in rows}
    except sqlite3.OperationalError:
        return {}


def _minutes_from_seconds(seconds: int) -> float:
    return round(max(0, int(seconds)) / 60, 1)


def _interleave_by_module(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Round-robin across module_type; preserve sort_order within each module.

    When only one module is present, return global sort_order (unchanged behavior).
    Module cycle order = order each subject first appears in the plan (sort_order).
    """
    if not items:
        return []
    by_mod: dict[str, list[dict[str, Any]]] = {}
    mod_first: dict[str, int] = {}
    for item in items:
        mt = str(item.get("module_type") or "other")
        if mt not in by_mod:
            by_mod[mt] = []
            mod_first[mt] = int(item.get("sort_order") or 0)
        by_mod[mt].append(item)
    if len(by_mod) <= 1:
        return sorted(items, key=lambda x: int(x.get("sort_order") or 0))
    module_keys = sorted(by_mod.keys(), key=lambda m: mod_first[m])
    queues = {m: list(by_mod[m]) for m in module_keys}
    out: list[dict[str, Any]] = []
    while True:
        progressed = False
        for m in module_keys:
            if not queues[m]:
                continue
            out.append(queues[m].pop(0))
            progressed = True
        if not progressed:
            break
    return out


def normalize_stage_test_positions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Place each stage test after the last study unit it covers; drop exact duplicates."""
    out = [dict(x) for x in items if x.get("item_type") != "test"]
    tests = [dict(x) for x in items if x.get("item_type") == "test"]
    seen_cov: set[frozenset[str]] = set()
    unique_tests: list[dict[str, Any]] = []
    for test in tests:
        covers = frozenset(_parse_json_list(test.get("test_unit_ids")) or [])
        if not covers or covers in seen_cov:
            continue
        seen_cov.add(covers)
        unique_tests.append(test)

    keyed: list[tuple[int, int, int, dict[str, Any]]] = []
    for test in unique_tests:
        covers = set(_parse_json_list(test.get("test_unit_ids")) or [])
        indices = [
            i
            for i, st in enumerate(out)
            if st.get("item_type") == "study" and st.get("unit_id") in covers
        ]
        if not indices:
            keyed.append((len(out), 0, 0, test))
            continue
        keyed.append((max(indices), min(indices), len(covers), test))

    keyed.sort(key=lambda row: (row[0], row[1], row[2]))
    for last_si, _first_si, _n, test in reversed(keyed):
        out.insert(last_si + 1, test)
    return out


def _stage_test_order_issues(items: list[dict[str, Any]]) -> list[str]:
    """Human-readable warnings when a test appears before units it covers."""
    issues: list[str] = []
    study_seen: set[str] = set()
    for idx, it in enumerate(items):
        if it.get("item_type") == "study" and it.get("unit_id"):
            study_seen.add(it["unit_id"])
        elif it.get("item_type") == "test":
            covers = set(_parse_json_list(it.get("test_unit_ids")) or [])
            missing = [u for u in covers if u not in study_seen]
            if missing:
                title = it.get("test_title") or "阶段测"
                issues.append(f"第{idx + 1}条「{title}」排在部分学习单元之前")
    return issues


def _plan_items_from_draft_rows(rows: list) -> list[dict[str, Any]]:
    plan_items: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        d = dict(row)
        d["id"] = -(i + 1)
        d["study_completed"] = 0
        d["test_passed"] = 0
        d["need_refresh"] = 0
        d["test_unit_ids"] = _parse_json_list(d.get("test_unit_ids"))
        plan_items.append(d)
    return plan_items


def _plan_items_from_payload(
    conn: sqlite3.Connection, items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    plan_items: list[dict[str, Any]] = []
    for i, it in enumerate(items):
        if it.get("status") == "removed":
            continue
        d = dict(it)
        d["id"] = -(i + 1)
        d["study_completed"] = int(d.get("study_completed") or 0)
        d["test_passed"] = int(d.get("test_passed") or 0)
        d["need_refresh"] = int(d.get("need_refresh") or 0)
        d["test_unit_ids"] = _parse_json_list(d.get("test_unit_ids"))
        if d.get("item_type") == "study" and d.get("unit_id"):
            u = conn.execute(
                "SELECT title, est_minutes, module_type FROM task_units WHERE unit_id=?",
                (d["unit_id"],),
            ).fetchone()
            if u:
                d["unit_title"] = u["title"]
                d["unit_est_minutes"] = u["est_minutes"]
                if not d.get("module_type"):
                    d["module_type"] = u["module_type"]
        plan_items.append(d)
    return plan_items


def _hydrate_plan_items_with_live(
    conn: sqlite3.Connection, student_id: str, plan_items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Attach live plan_item ids / completion flags so previews match student packing."""
    live_rows = [
        dict(r)
        for r in conn.execute(
            """
            SELECT p.*, u.title AS unit_title
            FROM plan_items p
            LEFT JOIN task_units u ON u.unit_id = p.unit_id
            WHERE p.student_id=? AND p.status!='removed'
            ORDER BY p.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    by_unit: dict[str, dict[str, Any]] = {}
    tests: list[dict[str, Any]] = []
    for row in live_rows:
        row["test_unit_ids"] = _parse_json_list(row.get("test_unit_ids"))
        if row.get("item_type") == "study" and row.get("unit_id"):
            by_unit[str(row["unit_id"])] = row
        elif row.get("item_type") == "test":
            tests.append(row)

    def _test_key(ids: list[Any]) -> str:
        return "\u0001".join(sorted(str(x) for x in (ids or [])))

    used_live: set[int] = set()
    for d in plan_items:
        live = None
        if d.get("item_type") == "study" and d.get("unit_id"):
            live = by_unit.get(str(d["unit_id"]))
        elif d.get("item_type") == "test":
            key = _test_key(d.get("test_unit_ids") or [])
            for t in tests:
                if int(t["id"]) in used_live:
                    continue
                if _test_key(t.get("test_unit_ids") or []) == key:
                    live = t
                    break
        if not live:
            continue
        used_live.add(int(live["id"]))
        d["id"] = int(live["id"])
        d["study_completed"] = int(live.get("study_completed") or 0)
        d["test_passed"] = int(live.get("test_passed") or 0)
        d["need_refresh"] = int(live.get("need_refresh") or 0)
        d["status"] = live.get("status") or d.get("status") or "pending"
        if live.get("unit_title"):
            d["unit_title"] = live["unit_title"]
    return plan_items


def _schedule_day_from_daily(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> Optional[dict[str, Any]]:
    rows = conn.execute(
        "SELECT 1 FROM daily_tasks WHERE student_id=? AND task_date=? LIMIT 1",
        (student_id, task_date),
    ).fetchone()
    if not rows:
        return None
    enriched = _enrich_daily(conn, student_id, task_date)
    if not enriched:
        return {
            "task_date": task_date,
            "items": [],
            "units_total": 0,
            "source": "actual",
        }
    return {
        "task_date": task_date,
        "items": [
            {
                "title": x.get("title"),
                "module_type": x.get("module_type"),
                "item_type": x.get("item_type"),
                "est_minutes": x.get("est_minutes"),
                "priority_class": x.get("priority_class"),
                "state": x.get("state"),
            }
            for x in enriched
        ],
        "units_total": len(enriched),
        "source": "actual",
    }


def _aligned_units_schedule(
    conn: sqlite3.Connection,
    student_id: str,
    plan_items: list[dict[str, Any]],
    *,
    start_date: str,
    quota_resolver,
    days: int = UNITS_PREVIEW_DAYS,
) -> list[dict[str, Any]]:
    """Schedule aligned with student: today uses locked daily_tasks when present."""
    today = china_ymd()
    plan_items = _gendu_aware_plan_items(conn, student_id, start_date, list(plan_items))
    released = {pid for pid in _released_plan_item_ids(conn, student_id) if pid > 0}
    schedule: list[dict[str, Any]] = []
    cursor = start_date
    left = days

    if cursor <= today and left > 0:
        actual = _schedule_day_from_daily(conn, student_id, today)
        if actual is not None:
            schedule.append(actual)
            left -= 1
            cursor = (
                datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
            ).strftime("%Y-%m-%d")
        else:
            backlog = {
                pid
                for pid in backlog_plan_item_ids(conn, student_id)
                if pid > 0
            }
            picks = _units_pack_picks(
                plan_items,
                task_date=today,
                quota_map=quota_resolver(today),
                backlog_ids=backlog,
                released_ids=released,
            )
            schedule.append(
                {
                    "task_date": today,
                    "items": _units_pack_to_preview_items(conn, picks),
                    "units_total": len(picks),
                    "source": "simulated",
                }
            )
            for item, _p, _f in picks:
                if _should_release_plan_item(item):
                    released.add(int(item["id"]))
            left -= 1
            cursor = (
                datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
            ).strftime("%Y-%m-%d")

    if left > 0:
        rest = _preview_units_schedule(
            conn,
            plan_items,
            cursor,
            quota_resolver=quota_resolver,
            days=left,
            initial_released=released,
            initial_backlog=set(),
        )
        schedule.extend(rest)
    while schedule and not (schedule[-1].get("items") or []):
        schedule.pop()
    return schedule


def _simulate_daily_pack(
    conn: sqlite3.Connection,
    plan_items: list[dict[str, Any]],
    backlog_items: list[dict[str, Any]],
    budget: int,
    tolerance: float,
) -> dict[str, Any]:
    result: list[dict[str, Any]] = []
    used = 0.0
    in_result: set[int] = set()

    def _try_add(item: dict[str, Any], prio: str) -> bool:
        nonlocal used
        pid = int(item["id"])
        if pid in in_result:
            return False
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            return False
        if used == 0 and est > budget:
            result.append({"item": item, "priority_class": prio})
            in_result.add(pid)
            return True
        result.append({"item": item, "priority_class": prio})
        in_result.add(pid)
        used += est
        return True

    for item in _interleave_by_module(backlog_items):
        if used >= tolerance:
            break
        _try_add(item, "carry_over")

    fresh = [it for it in plan_items if not _item_done(it) and int(it["id"]) not in in_result]
    for item in _interleave_by_module(fresh):
        if used >= tolerance:
            break
        pid = int(item["id"])
        if pid in in_result:
            continue
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            break
        if used == 0 and est > budget:
            result.append({"item": item, "priority_class": "fresh"})
            in_result.add(pid)
            break
        result.append({"item": item, "priority_class": "fresh"})
        in_result.add(pid)
        used += est
        if used >= tolerance:
            break

    modules = {r["item"].get("module_type") for r in result if r["item"].get("module_type")}
    out_items = []
    for r in result:
        it = r["item"]
        title = it.get("unit_title") or it.get("test_title") or it.get("unit_id") or "任务"
        if it.get("item_type") == "test":
            title = it.get("test_title") or title
        out_items.append(
            {
                "title": title,
                "module_type": it.get("module_type"),
                "item_type": it.get("item_type"),
                "est_minutes": _est_minutes(conn, it),
                "priority_class": r["priority_class"],
            }
        )
    return {
        "est_total_minutes": sum(x["est_minutes"] for x in out_items),
        "rotated": len(modules) > 1,
        "items": out_items,
    }


def _quota_overrides_from_payload(
    module_quotas: Any,
) -> dict[str, dict[str, int]]:
    if not isinstance(module_quotas, list):
        return {}
    out: dict[str, dict[str, int]] = {}
    for q in module_quotas:
        if not isinstance(q, dict):
            continue
        mt = str(q.get("module_type") or "")
        if not mt:
            continue
        entry: dict[str, int] = {}
        if q.get("weekday_units") is not None:
            entry["weekday_units"] = max(0, int(q["weekday_units"]))
        if q.get("weekend_units") is not None:
            entry["weekend_units"] = max(0, int(q["weekend_units"]))
        if entry:
            out[mt] = entry
    return out


def preview_daily_pack_items(
    conn: sqlite3.Connection,
    student_id: str,
    items: list[dict[str, Any]],
    task_date: Optional[str] = None,
    *,
    weekday_minutes: Optional[int] = None,
    weekend_minutes: Optional[int] = None,
    pack_mode: Optional[str] = None,
    module_quotas: Optional[list[dict[str, Any]]] = None,
    effective_from: Optional[str] = None,
) -> dict[str, Any]:
    """Preview packing for a draft item list (saved or unsaved).

    Units mode aligns with the student: today uses locked daily_tasks when present;
    draft rows are hydrated with live plan_item ids so released/backlog match.
    Quotas follow 生效日：之前用已生效，之后用 pending / 表单试算。
    """
    task_date = task_date or china_ymd()
    profile = ensure_time_profile(conn, student_id)
    mode = _effective_pack_mode(
        profile,
        mode_override=pack_mode,
        prefer_pending=pack_mode is None,
    )
    plan_items = _hydrate_plan_items_with_live(
        conn, student_id, _plan_items_from_payload(conn, items)
    )
    quota_overrides = _quota_overrides_from_payload(module_quotas)
    override_from = None
    if quota_overrides:
        raw_eff = (
            effective_from
            or profile.get("pending_effective_from")
            or task_date
        )
        try:
            datetime.strptime(str(raw_eff), "%Y-%m-%d")
            override_from = str(raw_eff)
        except (TypeError, ValueError):
            override_from = task_date
    if mode == PACK_MODE_UNITS_PER_DAY:

        def _quota_for(day: str) -> dict[str, int]:
            return _resolve_units_quota_map(
                conn,
                student_id,
                day,
                plan_items,
                quota_overrides=quota_overrides or None,
                override_from=override_from,
            )

        schedule = _aligned_units_schedule(
            conn,
            student_id,
            plan_items,
            start_date=task_date,
            quota_resolver=_quota_for,
        )
        quota_map = _quota_for(task_date)
        today_row = next(
            (d for d in schedule if d.get("task_date") == task_date),
            schedule[0] if schedule else None,
        )
        today_items = (today_row or {}).get("items") or []
        return {
            "source": "draft_items_aligned",
            "task_date": task_date,
            "pack_mode": PACK_MODE_UNITS_PER_DAY,
            "module_quotas": quota_map,
            "schedule": schedule,
            "items": today_items,
            "units_total": len(today_items),
            "est_total_minutes": sum(int(x.get("est_minutes") or 0) for x in today_items),
            "rotated": len({x.get("module_type") for x in today_items if x.get("module_type")})
            > 1,
            "aligned": True,
            "quota_override_from": override_from,
        }
    budget = _budget_minutes(
        profile,
        task_date,
        weekday_override=weekday_minutes,
        weekend_override=weekend_minutes,
        prefer_pending=weekday_minutes is None and weekend_minutes is None,
    )
    tolerance = budget * PACK_TOLERANCE
    sim = _simulate_daily_pack(conn, plan_items, [], budget, tolerance)
    return {
        "source": "draft_items",
        "task_date": task_date,
        "pack_mode": PACK_MODE_TIME_BUDGET,
        "budget_minutes": budget,
        **sim,
    }


def preview_daily_pack(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
    *,
    source: str = "live",
    pack_mode: Optional[str] = None,
    module_quotas: Optional[list[dict[str, Any]]] = None,
    weekday_minutes: Optional[int] = None,
    weekend_minutes: Optional[int] = None,
) -> dict[str, Any]:
    """Simulate daily boxing (multi-module rotation). Live + existing daily → actual today."""
    task_date = task_date or china_ymd()
    maybe_apply_pending_for_today(conn, student_id, task_date)
    profile = ensure_time_profile(conn, student_id)
    mode = _effective_pack_mode(
        profile,
        mode_override=pack_mode,
        prefer_pending=pack_mode is None,
    )
    quota_overrides = _quota_overrides_from_payload(module_quotas)

    if source == "live":
        existing = conn.execute(
            "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, task_date),
        ).fetchone()
        if existing and int(existing["c"]) > 0:
            daily = _enrich_daily(conn, student_id, task_date)
            modules = {d.get("module_type") for d in daily if d.get("module_type")}
            base = {
                "source": "live_locked",
                "task_date": task_date,
                "pack_mode": mode,
                "est_total_minutes": sum(d.get("est_minutes") or 0 for d in daily),
                "rotated": len(modules) > 1,
                "units_total": len(daily),
                "items": [
                    {
                        "title": d.get("title"),
                        "module_type": d.get("module_type"),
                        "item_type": d.get("item_type"),
                        "est_minutes": d.get("est_minutes"),
                        "priority_class": d.get("priority_class"),
                    }
                    for d in daily
                ],
            }
            if mode == PACK_MODE_UNITS_PER_DAY:
                return base
            budget = _budget_minutes(profile, task_date)
            return {**base, "budget_minutes": budget}

    if source == "draft":
        rows = conn.execute(
            """
            SELECT d.*, u.title AS unit_title, u.est_minutes AS unit_est_minutes
            FROM plan_items_draft d
            LEFT JOIN task_units u ON u.unit_id = d.unit_id
            WHERE d.student_id=? AND d.status='pending'
            ORDER BY d.sort_order
            """,
            (student_id,),
        ).fetchall()
        plan_items = _plan_items_from_draft_rows(rows)
        backlog_items: list[dict[str, Any]] = []
    else:
        plan_items = [
            dict(r)
            for r in conn.execute(
                """
                SELECT p.*, u.title AS unit_title
                FROM plan_items p
                LEFT JOIN task_units u ON u.unit_id = p.unit_id
                WHERE p.student_id=? AND p.status='pending'
                ORDER BY p.sort_order
                """,
                (student_id,),
            ).fetchall()
        ]
        backlog_items = []
        for pid in backlog_plan_item_ids(conn, student_id):
            item_row = conn.execute("SELECT * FROM plan_items WHERE id=?", (pid,)).fetchone()
            if item_row and item_row["status"] == "pending":
                item = dict(item_row)
                if not _item_done(item):
                    backlog_items.append(item)

    if mode == PACK_MODE_UNITS_PER_DAY:
        prefer = not quota_overrides and pack_mode is None and source == "draft"

        def _quota_for(day: str) -> dict[str, int]:
            if source == "draft":
                return _module_quota_map(
                    conn,
                    student_id,
                    day,
                    plan_items,
                    quota_overrides=quota_overrides,
                    prefer_pending=prefer,
                )
            return _resolve_units_quota_map(
                conn,
                student_id,
                day,
                plan_items,
                quota_overrides=quota_overrides or None,
                override_from=(
                    profile.get("pending_effective_from") or task_date
                    if quota_overrides
                    else None
                ),
            )

        if source == "draft":
            # Saved draft only: ideal from scratch (no live released state).
            quota_map = _quota_for(task_date)
            sim = _simulate_units_pack(
                conn,
                plan_items,
                task_date=task_date,
                quota_map=quota_map,
                backlog_items=[],
                released_ids=set(),
            )
            schedule = _preview_units_schedule(
                conn,
                plan_items,
                task_date,
                quota_resolver=_quota_for,
            )
            return {
                "source": "draft",
                "task_date": task_date,
                "pack_mode": PACK_MODE_UNITS_PER_DAY,
                "module_quotas": quota_map,
                "schedule": schedule,
                **sim,
            }

        # Live plan: same algorithm as student today + upcoming.
        schedule = _aligned_units_schedule(
            conn,
            student_id,
            plan_items,
            start_date=task_date,
            quota_resolver=_quota_for,
        )
        quota_map = _quota_for(task_date)
        today_row = next(
            (d for d in schedule if d.get("task_date") == task_date),
            schedule[0] if schedule else None,
        )
        today_items = (today_row or {}).get("items") or []
        return {
            "source": "live_aligned",
            "task_date": task_date,
            "pack_mode": PACK_MODE_UNITS_PER_DAY,
            "module_quotas": quota_map,
            "schedule": schedule,
            "items": today_items,
            "units_total": len(today_items),
            "est_total_minutes": sum(int(x.get("est_minutes") or 0) for x in today_items),
            "rotated": len({x.get("module_type") for x in today_items if x.get("module_type")})
            > 1,
            "aligned": True,
        }

    budget = _budget_minutes(
        profile,
        task_date,
        weekday_override=weekday_minutes,
        weekend_override=weekend_minutes,
        prefer_pending=(
            weekday_minutes is None
            and weekend_minutes is None
            and source == "draft"
        ),
    )
    tolerance = budget * PACK_TOLERANCE
    sim = _simulate_daily_pack(conn, plan_items, backlog_items, budget, tolerance)
    return {
        "source": source if source != "live" else "live",
        "task_date": task_date,
        "pack_mode": PACK_MODE_TIME_BUDGET,
        "budget_minutes": budget,
        **sim,
    }


def _released_plan_item_ids(conn: sqlite3.Connection, student_id: str) -> set[int]:
    rows = conn.execute(
        "SELECT DISTINCT plan_item_id FROM daily_tasks WHERE student_id=?",
        (student_id,),
    ).fetchall()
    return {int(r["plan_item_id"]) for r in rows}


def _module_order_from_items(items: list[dict[str, Any]]) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()
    for it in sorted(items, key=lambda x: int(x.get("sort_order") or 0)):
        mt = str(it.get("module_type") or "other")
        if mt not in seen:
            seen.add(mt)
            order.append(mt)
    return order


def _units_pack_picks(
    plan_items: list[dict[str, Any]],
    *,
    task_date: str,
    quota_map: dict[str, int],
    backlog_ids: set[int],
    released_ids: set[int],
) -> list[tuple[dict[str, Any], str, bool]]:
    """Return (item, priority_class, forced) for one calendar day.

    Per module: take up to ``quota`` items — backlog first (oldest sort_order),
    then fresh. Backlog beyond today's quota stays for later days (not dumped
    all at once after a heavy weekend).
    """
    active = [
        dict(it)
        for it in plan_items
        if it.get("status", "pending") == "pending" and not _item_done(it)
    ]
    refresh: list[dict[str, Any]] = []
    for it in sorted(active, key=lambda x: int(x.get("sort_order") or 0)):
        if it.get("item_type") == "study" and it.get("need_refresh") and not it.get("study_completed"):
            refresh.append(it)
    refresh_ids = {int(it["id"]) for it in refresh}

    pool: list[dict[str, Any]] = []
    meta: dict[int, tuple[str, bool]] = {}
    for mt in _module_order_from_items(active):
        quota = max(0, int(quota_map.get(mt, DEFAULT_UNITS_PER_DAY)))
        mod_items = [
            it
            for it in active
            if str(it.get("module_type") or "other") == mt and int(it["id"]) not in refresh_ids
        ]
        backlog_mod = [
            it for it in mod_items if int(it["id"]) in backlog_ids
        ]
        backlog_mod.sort(key=lambda x: int(x.get("sort_order") or 0))
        fresh_mod = [
            it
            for it in mod_items
            if int(it["id"]) not in backlog_ids and int(it["id"]) not in released_ids
        ]
        fresh_mod.sort(key=lambda x: int(x.get("sort_order") or 0))
        take_backlog = backlog_mod[:quota]
        slots = max(0, quota - len(take_backlog))
        for it in take_backlog:
            pid = int(it["id"])
            meta[pid] = ("carry_over", False)
            pool.append(it)
        for it in fresh_mod[:slots]:
            pid = int(it["id"])
            meta[pid] = ("fresh", False)
            pool.append(it)

    result: list[tuple[dict[str, Any], str, bool]] = []
    for it in refresh:
        result.append((it, "content_refresh", True))
    for it in _interleave_by_module(pool):
        pid = int(it["id"])
        prio, forced = meta.get(pid, ("fresh", False))
        result.append((it, prio, forced))
    return result


def _units_pack_to_preview_items(
    conn: sqlite3.Connection, picks: list[tuple[dict[str, Any], str, bool]]
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item, prio, _forced in picks:
        title = item.get("unit_title") or item.get("test_title") or item.get("unit_id") or "任务"
        if item.get("item_type") == "test":
            title = item.get("test_title") or title
        out.append(
            {
                "title": title,
                "module_type": item.get("module_type"),
                "item_type": item.get("item_type"),
                "est_minutes": _est_minutes(conn, item),
                "priority_class": prio,
            }
        )
    return out


def _simulate_units_pack(
    conn: sqlite3.Connection,
    plan_items: list[dict[str, Any]],
    *,
    task_date: str,
    quota_map: dict[str, int],
    backlog_items: Optional[list[dict[str, Any]]] = None,
    released_ids: Optional[set[int]] = None,
) -> dict[str, Any]:
    backlog_ids = {int(it["id"]) for it in (backlog_items or [])}
    released = set(released_ids or [])
    picks = _units_pack_picks(
        plan_items,
        task_date=task_date,
        quota_map=quota_map,
        backlog_ids=backlog_ids,
        released_ids=released,
    )
    out_items = _units_pack_to_preview_items(conn, picks)
    modules = {x.get("module_type") for x in out_items if x.get("module_type")}
    per_module: dict[str, int] = {}
    for x in out_items:
        mt = str(x.get("module_type") or "other")
        per_module[mt] = per_module.get(mt, 0) + 1
    return {
        "est_total_minutes": sum(x["est_minutes"] for x in out_items),
        "rotated": len(modules) > 1,
        "items": out_items,
        "units_total": len(out_items),
        "units_by_module": per_module,
    }


def _should_release_plan_item(item: dict[str, Any]) -> bool:
    """Gendu current lesson repeats daily until pass — do not consume from released set."""
    return str(item.get("module_type") or "") != GENDU_MODULE


def _preview_units_schedule(
    conn: sqlite3.Connection,
    plan_items: list[dict[str, Any]],
    start_date: str,
    *,
    quota_resolver,
    days: int = UNITS_PREVIEW_DAYS,
    initial_released: Optional[set[int]] = None,
    initial_backlog: Optional[set[int]] = None,
) -> list[dict[str, Any]]:
    """Simulate forward release for teacher multi-day preview.

    Assumes the student completes each simulated day's tasks so the calendar
    shows planned queue progression (virtual consumption), not endless carry-over.
    Real backlog is only applied on the first preview day when provided.
    """
    released = set(initial_released or [])
    done_ids = {int(it["id"]) for it in plan_items if _item_done(it)}
    schedule: list[dict[str, Any]] = []
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    for offset in range(days):
        day = (start + timedelta(days=offset)).strftime("%Y-%m-%d")
        quota_map = quota_resolver(day)
        if offset == 0:
            if initial_backlog is not None:
                backlog_ids = set(initial_backlog)
            elif released:
                backlog_ids = {pid for pid in released if pid not in done_ids}
            else:
                backlog_ids = set()
        else:
            backlog_ids = set()
        picks = _units_pack_picks(
            plan_items,
            task_date=day,
            quota_map=quota_map,
            backlog_ids=backlog_ids,
            released_ids=released,
        )
        items = _units_pack_to_preview_items(conn, picks)
        schedule.append({"task_date": day, "items": items, "units_total": len(items)})
        for item, _prio, _forced in picks:
            if _should_release_plan_item(item):
                released.add(int(item["id"]))
        if not picks and all(_item_done(it) or int(it["id"]) in released for it in plan_items):
            break
    return schedule


def _build_daily_tasks_time_budget(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    task_date = task_date or china_ymd()
    profile = ensure_time_profile(conn, student_id)
    budget = (
        int(profile["weekend_minutes"])
        if is_weekend(task_date)
        else int(profile["weekday_minutes"])
    )
    tolerance = budget * PACK_TOLERANCE

    existing = conn.execute(
        """
        SELECT * FROM daily_tasks WHERE student_id=? AND task_date=?
        ORDER BY sort_in_day
        """,
        (student_id, task_date),
    ).fetchall()
    if existing:
        # Already materialized for today — return as-is (MVP locked)
        return _enrich_daily(conn, student_id, task_date)

    result: list[tuple[int, str, bool]] = []  # plan_item_id, priority, forced
    used = 0.0
    in_result: set[int] = set()

    # 1) content refresh
    refresh_rows = conn.execute(
        """
        SELECT * FROM plan_items
        WHERE student_id=? AND status='pending' AND item_type='study'
          AND need_refresh=1 AND study_completed=0
        ORDER BY sort_order
        """,
        (student_id,),
    ).fetchall()
    for row in refresh_rows:
        item = dict(row)
        pid = item["id"]
        if pid in in_result:
            continue
        result.append((pid, "content_refresh", True))
        in_result.add(pid)
        used += _est_minutes(conn, item)

    # 2) backlog carry-over (interleave when multiple subjects)
    backlog_items: list[dict[str, Any]] = []
    for pid in backlog_plan_item_ids(conn, student_id):
        if pid in in_result:
            continue
        item_row = conn.execute("SELECT * FROM plan_items WHERE id=?", (pid,)).fetchone()
        if not item_row or item_row["status"] != "pending":
            continue
        item = dict(item_row)
        if _item_done(item):
            continue
        backlog_items.append(item)
    for item in _interleave_by_module(backlog_items):
        pid = item["id"]
        if pid in in_result:
            continue
        result.append((pid, "carry_over", False))
        in_result.add(pid)
        used += _est_minutes(conn, item)

    # 3) pack fresh items — multi-subject plans rotate by module (not strict global queue)
    live = conn.execute(
        """
        SELECT * FROM plan_items
        WHERE student_id=? AND status='pending'
        ORDER BY sort_order
        """,
        (student_id,),
    ).fetchall()
    fresh_candidates: list[dict[str, Any]] = []
    for row in live:
        item = dict(row)
        if _item_done(item):
            continue
        if item["id"] in in_result:
            continue
        fresh_candidates.append(item)
    for item in _interleave_by_module(fresh_candidates):
        est = _est_minutes(conn, item)
        if used > 0 and used + est > tolerance:
            break
        if used == 0 and est > budget:
            result.append((item["id"], "fresh", False))
            in_result.add(item["id"])
            break
        result.append((item["id"], "fresh", False))
        in_result.add(item["id"])
        used += est
        if used >= tolerance:
            break

    for sort_i, (pid, prio, forced) in enumerate(result):
        conn.execute(
            """
            INSERT INTO daily_tasks (
                student_id, task_date, plan_item_id, priority_class,
                sort_in_day, state, locked, forced
            ) VALUES (?, ?, ?, ?, ?, 'todo', 1, ?)
            """,
            (student_id, task_date, pid, prio, sort_i, 1 if forced else 0),
        )

    conn.commit()
    return _enrich_daily(conn, student_id, task_date)


def _materialize_daily_picks(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: str,
    picks: list[tuple[dict[str, Any], str, bool]],
) -> None:
    for sort_i, (item, prio, forced) in enumerate(picks):
        conn.execute(
            """
            INSERT INTO daily_tasks (
                student_id, task_date, plan_item_id, priority_class,
                sort_in_day, state, locked, forced
            ) VALUES (?, ?, ?, ?, ?, 'todo', 1, ?)
            """,
            (student_id, task_date, int(item["id"]), prio, sort_i, 1 if forced else 0),
        )


def _ensure_gendu_in_existing_daily(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> None:
    """If assignment active but today's locked pack lacks current gendu, append it."""
    asg = get_gendu_assignment(conn, student_id, on_date=task_date)
    if not asg or not asg.get("active"):
        if asg and (asg.get("expired") or asg.get("upcoming")):
            conn.execute(
                """
                DELETE FROM daily_tasks
                WHERE student_id=? AND task_date=?
                  AND plan_item_id IN (
                    SELECT id FROM plan_items
                    WHERE student_id=? AND module_type=?
                  )
                """,
                (student_id, task_date, student_id, GENDU_MODULE),
            )
            conn.commit()
        return
    current_unit = str(asg["current_unit_id"])
    pid = _ensure_gendu_plan_item(conn, student_id, current_unit)
    has = conn.execute(
        """
        SELECT 1 FROM daily_tasks
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (student_id, task_date, pid),
    ).fetchone()
    if has:
        return
    conn.execute(
        """
        DELETE FROM daily_tasks
        WHERE student_id=? AND task_date=?
          AND plan_item_id IN (
            SELECT id FROM plan_items
            WHERE student_id=? AND module_type=? AND id!=?
          )
        """,
        (student_id, task_date, student_id, GENDU_MODULE, pid),
    )
    max_sort = conn.execute(
        """
        SELECT COALESCE(MAX(sort_in_day), -1) AS m FROM daily_tasks
        WHERE student_id=? AND task_date=?
        """,
        (student_id, task_date),
    ).fetchone()["m"]
    conn.execute(
        """
        INSERT INTO daily_tasks (
            student_id, task_date, plan_item_id, priority_class,
            sort_in_day, state, locked, forced
        ) VALUES (?, ?, ?, 'fresh', ?, 'todo', 1, 0)
        """,
        (student_id, task_date, pid, int(max_sort) + 1),
    )
    conn.commit()


def _build_daily_tasks_units(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    task_date = task_date or china_ymd()
    advanced = advance_gendu_if_needed(conn, student_id, task_date)
    if advanced:
        conn.execute(
            "DELETE FROM daily_tasks WHERE student_id=? AND task_date=?",
            (student_id, task_date),
        )
        conn.commit()

    existing = conn.execute(
        """
        SELECT * FROM daily_tasks WHERE student_id=? AND task_date=?
        ORDER BY sort_in_day
        """,
        (student_id, task_date),
    ).fetchall()
    if existing:
        _ensure_gendu_in_existing_daily(conn, student_id, task_date)
        return _enrich_daily(conn, student_id, task_date)

    live = [
        dict(r)
        for r in conn.execute(
            """
            SELECT p.*, u.title AS unit_title
            FROM plan_items p
            LEFT JOIN task_units u ON u.unit_id = p.unit_id
            WHERE p.student_id=? AND p.status='pending'
            ORDER BY p.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    live = _gendu_aware_plan_items(conn, student_id, task_date, live)
    backlog_ids = set(backlog_plan_item_ids(conn, student_id))
    released_ids = _released_plan_item_ids(conn, student_id)
    quota_map = _module_quota_map(conn, student_id, task_date, live)
    asg = get_gendu_assignment(conn, student_id, on_date=task_date)
    if asg and asg.get("active"):
        quota_map[GENDU_MODULE] = max(1, int(quota_map.get(GENDU_MODULE) or 1))
    picks = _units_pack_picks(
        live,
        task_date=task_date,
        quota_map=quota_map,
        backlog_ids=backlog_ids,
        released_ids=released_ids,
    )
    _materialize_daily_picks(conn, student_id, task_date, picks)
    conn.commit()
    return _enrich_daily(conn, student_id, task_date)


def build_daily_tasks(
    conn: sqlite3.Connection,
    student_id: str,
    task_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    task_date = task_date or china_ymd()
    maybe_apply_pending_for_today(conn, student_id, task_date)
    expire_plan_pause_if_due(conn, student_id, on_date=task_date)
    if is_plan_schedule_paused(conn, student_id, task_date):
        existing = conn.execute(
            "SELECT 1 FROM daily_tasks WHERE student_id=? AND task_date=? LIMIT 1",
            (student_id, task_date),
        ).fetchone()
        if existing:
            return _enrich_daily(conn, student_id, task_date)
        return []
    profile = ensure_time_profile(conn, student_id)
    mode = _effective_pack_mode(profile)
    if mode == PACK_MODE_UNITS_PER_DAY:
        return _build_daily_tasks_units(conn, student_id, task_date)
    return _build_daily_tasks_time_budget(conn, student_id, task_date)


def clear_daily_schedule(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    """Clear locked daily tasks and the student's live/draft plan queue."""
    daily_n = conn.execute(
        "SELECT COUNT(*) AS c FROM daily_tasks WHERE student_id=?",
        (student_id,),
    ).fetchone()["c"]
    plan_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchone()["c"]
    draft_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=?",
        (student_id,),
    ).fetchone()["c"]
    conn.execute("DELETE FROM daily_tasks WHERE student_id=?", (student_id,))
    conn.execute(
        """
        UPDATE plan_items SET status='removed',
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE student_id=? AND status!='removed'
        """,
        (student_id,),
    )
    conn.execute("DELETE FROM plan_items_draft WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM plan_draft_meta WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM student_plan_pause WHERE student_id=?", (student_id,))
    conn.execute(
        "DELETE FROM student_gendu_assignment WHERE student_id=?", (student_id,)
    )
    conn.commit()
    return {
        "student_id": student_id,
        "deleted": int(daily_n),
        "cleared_plan_items": int(plan_n),
        "cleared_draft_items": int(draft_n),
    }


# --- Class overview (teacher board) ------------------------------------------

_MODULE_BRIEF_LABELS = {
    "reading_synonym": "阅",
    "dictation": "听",
    "listening_basic": "听基",
    "listening_synonym": "听替",
    "sentence": "长难",
    "writing_phrase": "词伙",
    "writing_translate": "翻译",
    "listening_p4_speed": "跟读",
}

_SPEAKING_PREFIX = "speaking_"

# Wireframe defaults (§5.1)
_OVERVIEW_EVENING_HOUR = 20
_OVERVIEW_ZERO_DONE_HOUR = 16
_OVERVIEW_YELLOW_HOUR = 14
_OVERVIEW_YELLOW_MINUTES_HOUR = 18
_OVERVIEW_RED_RATE = 0.5
_OVERVIEW_BACKLOG_RED = 3
_OVERVIEW_TEST_FAIL_RED = 2
_OVERVIEW_GHOST_DAYS = 7
_OVERVIEW_MINUTES_RED_RATIO = 0.25
_OVERVIEW_MINUTES_YELLOW_RATIO = 0.5


def _is_speaking_module(mt: str) -> bool:
    return str(mt or "").startswith(_SPEAKING_PREFIX) or str(mt or "") == "speaking"


def _plan_progress_brief(progress: dict[str, dict[str, int]]) -> list[dict[str, Any]]:
    """Compress plan-track study X/Y into at most 2 abbrevs + +N."""
    buckets: list[tuple[str, str, int, int]] = []
    speak_x = 0
    speak_y = 0
    for mt, p in (progress or {}).items():
        sx = int(p.get("study_x") or 0)
        sy = int(p.get("study_y") or 0)
        if sy <= 0:
            continue
        if _is_speaking_module(mt):
            speak_x += sx
            speak_y += sy
            continue
        label = _MODULE_BRIEF_LABELS.get(mt, mt[:2] if mt else "?")
        buckets.append((mt, label, sx, sy))
    if speak_y > 0:
        buckets.append(("speaking", "口", speak_x, speak_y))
    # Prefer modules with incomplete work, then higher remaining
    buckets.sort(key=lambda b: (0 if b[2] < b[3] else 1, -(b[3] - b[2]), b[1]))
    brief: list[dict[str, Any]] = []
    for mt, label, sx, sy in buckets[:2]:
        brief.append(
            {
                "module_type": mt,
                "label": label,
                "study_x": sx,
                "study_y": sy,
                "text": f"{label}{sx}/{sy}",
            }
        )
    extra = len(buckets) - len(brief)
    if extra > 0:
        brief.append({"module_type": "_more", "label": f"+{extra}", "text": f"+{extra}"})
    return brief


def _today_task_counts(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> tuple[int, int, int]:
    """Return (done, total, done_fail). Read-only; empty if not materialized."""
    rows = conn.execute(
        """
        SELECT state FROM daily_tasks
        WHERE student_id=? AND task_date=?
        """,
        (student_id, task_date),
    ).fetchall()
    total = len(rows)
    done = 0
    fail = 0
    for r in rows:
        st = r["state"] or ""
        if st in ("done_study", "done_pass"):
            done += 1
        elif st == "done_fail":
            fail += 1
    return done, total, fail


def _content_refresh_count(conn: sqlite3.Connection, student_id: str) -> int:
    row = conn.execute(
        """
        SELECT COUNT(*) AS c FROM plan_items
        WHERE student_id=? AND status='pending' AND item_type='study'
          AND need_refresh=1 AND study_completed=0
        """,
        (student_id,),
    ).fetchone()
    return int(row["c"] or 0)


def _test_fail_count(conn: sqlite3.Connection, student_id: str, task_date: str) -> int:
    """Unpassed stage tests still on plan (+ today done_fail plan items counted once)."""
    row = conn.execute(
        """
        SELECT COUNT(*) AS c FROM plan_items
        WHERE student_id=? AND status='pending' AND item_type='test' AND test_passed=0
        """,
        (student_id,),
    ).fetchone()
    return int(row["c"] or 0)


def _has_hard_test_fail(conn: sqlite3.Connection, student_id: str, task_date: str) -> bool:
    """R5: any unpassed test with today's attempts >= 2, or fail count >= threshold."""
    rows = conn.execute(
        """
        SELECT test_attempt_count_today, test_attempt_ymd
        FROM plan_items
        WHERE student_id=? AND status='pending' AND item_type='test' AND test_passed=0
        """,
        (student_id,),
    ).fetchall()
    if len(rows) >= _OVERVIEW_TEST_FAIL_RED:
        return True
    for r in rows:
        attempts = int(r["test_attempt_count_today"] or 0)
        if r["test_attempt_ymd"] == task_date and attempts >= _OVERVIEW_TEST_FAIL_RED:
            return True
    return False


def _ghost_zero_streak(
    conn: sqlite3.Connection, student_id: str, task_date: str, days: int = _OVERVIEW_GHOST_DAYS
) -> bool:
    """R6: consecutive calendar days with tasks and 0% completion."""
    end = datetime.strptime(task_date, "%Y-%m-%d").date()
    for i in range(days):
        day = (end - timedelta(days=i)).strftime("%Y-%m-%d")
        done, total, _fail = _today_task_counts(conn, student_id, day)
        if total < 1:
            return False
        if done > 0:
            return False
    return True


def _row_status_for_overview(
    *,
    plan_status: str,
    today_done: int,
    today_total: int,
    today_minutes: int,
    budget_minutes: int,
    backlog: int,
    content_refresh: int,
    test_fail: int,
    hard_test_fail: bool,
    ghost: bool,
    pending_plan_change: bool,
    hour: int,
    schedule_paused: bool = False,
    schedule_pause_upcoming: bool = False,
) -> str:
    if schedule_paused or schedule_pause_upcoming:
        # 已标明暂停原因，不占用「建议跟进」黄灯
        return "none"
    if plan_status in ("none", "all_paused"):
        return "none"
    rate = (today_done / today_total) if today_total > 0 else None
    # Red
    if (
        hour >= _OVERVIEW_EVENING_HOUR
        and rate is not None
        and rate < _OVERVIEW_RED_RATE
        and today_total >= 1
    ):
        return "red"
    if hour >= _OVERVIEW_ZERO_DONE_HOUR and rate == 0.0 and today_total >= 2:
        return "red"
    if backlog >= _OVERVIEW_BACKLOG_RED:
        return "red"
    if content_refresh >= 1:
        return "red"
    if hard_test_fail:
        return "red"
    if ghost:
        return "red"
    if (
        hour >= _OVERVIEW_EVENING_HOUR
        and today_total >= 1
        and budget_minutes > 0
        and today_minutes < budget_minutes * _OVERVIEW_MINUTES_RED_RATIO
    ):
        return "red"
    # Yellow
    if hour >= _OVERVIEW_YELLOW_HOUR and rate is not None and rate < _OVERVIEW_RED_RATE:
        return "yellow"
    if backlog in (1, 2):
        return "yellow"
    if test_fail == 1:
        return "yellow"
    if (
        hour >= _OVERVIEW_YELLOW_MINUTES_HOUR
        and today_total >= 1
        and budget_minutes > 0
        and today_minutes < budget_minutes * _OVERVIEW_MINUTES_YELLOW_RATIO
    ):
        return "yellow"
    if pending_plan_change:
        return "yellow"
    if today_total > 0:
        return "green"
    return "green"


def _student_overview_row(
    conn: sqlite3.Connection,
    student_id: str,
    name: str,
    task_date: str,
    *,
    hour: int,
) -> dict[str, Any]:
    plan_status = effective_plan_status(conn, student_id)
    progress = _plan_progress(conn, student_id)
    today_done, today_total, _today_fail = _today_task_counts(conn, student_id, task_date)
    yday = (
        datetime.strptime(task_date, "%Y-%m-%d").date() - timedelta(days=1)
    ).strftime("%Y-%m-%d")
    yesterday_done, yesterday_total, _yfail = _today_task_counts(conn, student_id, yday)
    profile = ensure_time_profile(conn, student_id)
    budget = _budget_minutes(profile, task_date)
    secs = sum_today_study_seconds(conn, student_id, task_date)
    today_minutes = int(round(secs / 60.0)) if secs else 0
    y_secs = sum_today_study_seconds(conn, student_id, yday)
    yesterday_minutes = int(round(y_secs / 60.0)) if y_secs else 0
    total_secs = sum_total_study_seconds(conn, student_id)
    total_minutes = int(round(total_secs / 60.0)) if total_secs else 0
    backlog = len(backlog_plan_item_ids(conn, student_id))
    content_refresh = _content_refresh_count(conn, student_id)
    test_fail = _test_fail_count(conn, student_id, task_date)
    hard_test_fail = _has_hard_test_fail(conn, student_id, task_date)
    draft_n = conn.execute(
        "SELECT COUNT(*) AS c FROM plan_items_draft WHERE student_id=? AND status!='removed'",
        (student_id,),
    ).fetchone()["c"]
    tp = profile
    pending_change = bool(draft_n) or _profile_has_real_pending(tp)
    pending_from = (
        _pending_effective_from_summary(conn, student_id, pending_plan_change=pending_change)
        if pending_change
        else None
    )
    ghost = False
    if plan_status == "active" and today_total >= 1 and today_done == 0:
        ghost = _ghost_zero_streak(conn, student_id, task_date)
    pause = get_plan_pause(conn, student_id, on_date=task_date)
    schedule_paused = bool(pause and pause.get("active"))
    schedule_pause_upcoming = bool(pause and pause.get("upcoming"))
    row_status = _row_status_for_overview(
        plan_status=plan_status,
        today_done=today_done,
        today_total=today_total,
        today_minutes=today_minutes,
        budget_minutes=budget,
        backlog=backlog,
        content_refresh=content_refresh,
        test_fail=test_fail,
        hard_test_fail=hard_test_fail,
        ghost=ghost,
        pending_plan_change=pending_change,
        hour=hour,
        schedule_paused=schedule_paused,
        schedule_pause_upcoming=schedule_pause_upcoming,
    )
    brief = _plan_progress_brief(progress)
    return {
        "student_id": student_id,
        "name": name,
        "plan_status": plan_status,
        "today_done": today_done,
        "today_total": today_total,
        "yesterday_done": yesterday_done,
        "yesterday_total": yesterday_total,
        "yesterday_incomplete": bool(
            yesterday_total > 0 and yesterday_done < yesterday_total
        ),
        "today_minutes": today_minutes,
        "yesterday_minutes": yesterday_minutes,
        "total_minutes": total_minutes,
        "budget_minutes": budget,
        "backlog": backlog,
        "content_refresh": content_refresh,
        "test_fail": test_fail,
        "plan_progress_brief": brief,
        "progress": progress,
        "pending_plan_change": pending_change,
        "pending_effective_from": pending_from,
        "plan_pause": pause,
        "row_status": row_status,
    }


def class_overview(
    conn: sqlite3.Connection,
    *,
    task_date: Optional[str] = None,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    """Read-only class board. Does NOT materialize daily_tasks."""
    ensure_task_tables(conn)
    if task_date:
        try:
            datetime.strptime(task_date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("日期格式应为 YYYY-MM-DD") from exc
    task_date = task_date or china_ymd(now)
    dt = now or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    hour = dt.astimezone(SHANGHAI).hour
    students = conn.execute(
        """
        SELECT student_id, name FROM students
        WHERE COALESCE(status, 'active') = 'active'
        ORDER BY student_id DESC
        """
    ).fetchall()
    rows = [
        _student_overview_row(
            conn, r["student_id"], r["name"] or "", task_date, hour=hour
        )
        for r in students
    ]
    rows.sort(key=lambda row: str(row.get("student_id") or ""), reverse=True)
    today_all_done = sum(
        1
        for r in rows
        if int(r.get("today_total") or 0) > 0
        and int(r.get("today_done") or 0) >= int(r.get("today_total") or 0)
    )
    yesterday_incomplete = sum(1 for r in rows if r.get("yesterday_incomplete"))
    need_attention = sum(1 for r in rows if r.get("row_status") == "red")
    no_plan = sum(1 for r in rows if r.get("plan_status") == "none")
    plan_paused = sum(
        1
        for r in rows
        if (r.get("plan_pause") or {}).get("active")
        or (r.get("plan_pause") or {}).get("upcoming")
    )
    return {
        "task_date": task_date,
        "generated_at": dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M"),
        "students": rows,
        "stats": {
            "total": len(rows),
            "today_all_done": today_all_done,
            "yesterday_incomplete": yesterday_incomplete,
            "need_attention": need_attention,
            "no_plan": no_plan,
            "plan_paused": plan_paused,
        },
    }


def _scope_for_unit(content_ref: Any) -> tuple[int, str]:
    ref = content_ref
    if isinstance(ref, str):
        try:
            ref = json.loads(ref)
        except json.JSONDecodeError:
            ref = {}
    if not isinstance(ref, dict):
        ref = {}
    total = int(ref.get("scope_total") or 0)
    if not total and "setId" in ref:
        total = 5 if int(ref["setId"]) == 23 else 10
    if not total and "groupIndex" in ref:
        total = 20
    unit = "组"
    if "groupIndex" in ref:
        unit = "词"
    return total, unit


def _enrich_daily(
    conn: sqlite3.Connection, student_id: str, task_date: str
) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT d.*, p.item_type, p.unit_id, p.module_type, p.test_title,
               p.test_unit_ids, p.study_completed, p.test_passed, p.need_refresh,
               p.est_minutes AS plan_est,
               u.title AS unit_title, u.content_ref, u.content_version, u.study_url,
               u.est_minutes AS unit_est
        FROM daily_tasks d
        JOIN plan_items p ON p.id = d.plan_item_id
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE d.student_id=? AND d.task_date=?
        ORDER BY d.sort_in_day
        """,
        (student_id, task_date),
    ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        scope_total, scope_unit = _scope_for_unit(item.get("content_ref"))
        prog = conn.execute(
            """
            SELECT scope_done, scope_total FROM task_unit_progress
            WHERE student_id=? AND plan_item_id=?
            """,
            (student_id, item["plan_item_id"]),
        ).fetchone()
        scope_done = int(prog["scope_done"]) if prog else 0
        if prog and prog["scope_total"]:
            scope_total = int(prog["scope_total"])
        study_url = item.get("study_url") or ""
        if study_url and item.get("id"):
            sep = "&" if "?" in study_url else "?"
            study_url = (
                f"{study_url}{sep}task_id={item['id']}"
                f"&plan_item_id={item['plan_item_id']}"
            )
        title = item.get("unit_title") or item.get("test_title") or "任务"
        if item.get("need_refresh"):
            title = f"{title}（内容已更新）"
        gendu_count = int(item.get("gendu_practice_count") or 0)
        entry = {
                "daily_task_id": item["id"],
                "plan_item_id": item["plan_item_id"],
                "task_date": task_date,
                "item_type": item["item_type"],
                "unit_id": item.get("unit_id"),
                "module_type": item.get("module_type"),
                "title": title,
                "state": item["state"],
                "priority_class": item["priority_class"],
                "forced": bool(item["forced"]),
                "content_version": item.get("content_version") or "1",
                "content_ref": (
                    json.loads(item["content_ref"])
                    if isinstance(item.get("content_ref"), str) and item.get("content_ref")
                    else item.get("content_ref")
                ),
                "scope_label": "本单元",
                "scope_done": scope_done,
                "scope_total": scope_total,
                "scope_unit": scope_unit,
                "study_url": study_url,
                "est_minutes": item.get("plan_est") or item.get("unit_est") or 15,
            }
        if str(item.get("module_type") or "") == GENDU_MODULE:
            entry["gendu_practice_count"] = gendu_count
            entry["gendu_required"] = GENDU_DAILY_PRACTICES
            entry["gendu_best_score"] = item.get("gendu_best_score")
            entry["scope_done"] = gendu_count
            entry["scope_total"] = GENDU_DAILY_PRACTICES
            entry["scope_unit"] = "次"
            entry["scope_label"] = "今日跟读"
        out.append(entry)
    return out


def get_today(conn: sqlite3.Connection, student_id: str) -> dict[str, Any]:
    task_date = china_ymd()
    items = build_daily_tasks(conn, student_id, task_date)
    profile = ensure_time_profile(conn, student_id)
    budget = (
        int(profile["weekend_minutes"])
        if is_weekend(task_date)
        else int(profile["weekday_minutes"])
    )
    plan = get_plan(conn, student_id)
    status = plan["plan_status"]
    actual_seconds = sum_today_study_seconds(conn, student_id, task_date)
    by_item_seconds = sum_today_study_by_plan_item(conn, student_id, task_date)
    for item in items:
        pid = item.get("plan_item_id")
        if pid is not None:
            item["actual_minutes"] = _minutes_from_seconds(by_item_seconds.get(int(pid), 0))
        else:
            item["actual_minutes"] = 0.0
    empty_msg = None
    if not items:
        if status == "none":
            empty_msg = "今日暂无任务，请联系助教"
        elif status == "all_paused":
            empty_msg = "计划已暂停，请联系助教"
        else:
            empty_msg = "今日暂无任务，请联系助教"
    upcoming = _student_upcoming_bundle(conn, student_id, task_date=task_date)
    pause = get_plan_pause(conn, student_id, on_date=task_date)
    if pause and pause.get("active"):
        empty_msg = "计划已暂停，请联系助教"
    return {
        "task_date": task_date,
        "pack_mode": _effective_pack_mode(profile),
        "budget_minutes": budget,
        "est_total_minutes": sum(i.get("est_minutes") or 0 for i in items),
        "actual_total_minutes": _minutes_from_seconds(actual_seconds),
        "units_total": len(items),
        "items": items,
        "progress": plan["progress"],
        "plan_status": status,
        "plan_pause": pause,
        "gendu_assignment": get_gendu_assignment(conn, student_id, on_date=task_date),
        "pending_plan_change": plan["pending_plan_change"],
        "pending_effective_from": plan.get("pending_effective_from"),
        "empty_message": empty_msg,
        "upcoming_schedule": upcoming["upcoming_schedule"],
        "remaining_plan": upcoming["remaining_plan"],
    }


def _plan_item_preview_title(conn: sqlite3.Connection, item: dict[str, Any]) -> str:
    title = item.get("unit_title") or item.get("test_title") or item.get("unit_id") or "任务"
    if item.get("item_type") == "test":
        title = item.get("test_title") or title
    if not item.get("unit_title") and item.get("unit_id"):
        u = conn.execute(
            "SELECT title FROM task_units WHERE unit_id=?", (item["unit_id"],)
        ).fetchone()
        if u and u["title"]:
            title = u["title"]
    return str(title)


def _remaining_plan_items(
    conn: sqlite3.Connection, plan_items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for it in plan_items:
        if it.get("status") not in (None, "pending"):
            continue
        if _item_done(it):
            continue
        out.append(
            {
                "plan_item_id": int(it["id"]),
                "item_type": it.get("item_type"),
                "module_type": it.get("module_type"),
                "unit_id": it.get("unit_id"),
                "title": _plan_item_preview_title(conn, it),
                "sort_order": int(it.get("sort_order") or 0),
            }
        )
    return out


def _preview_time_budget_schedule(
    conn: sqlite3.Connection,
    plan_items: list[dict[str, Any]],
    start_date: str,
    *,
    profile: dict[str, Any],
    days: int = UNITS_PREVIEW_DAYS,
    initial_released: Optional[set[int]] = None,
) -> list[dict[str, Any]]:
    """Forward pack preview for time_budget (read-only, assumes daily completion)."""
    released = set(initial_released or [])
    schedule: list[dict[str, Any]] = []
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    active = [
        it
        for it in plan_items
        if (it.get("status") == "pending" or it.get("status") is None)
        and not _item_done(it)
    ]
    for offset in range(days):
        day = (start + timedelta(days=offset)).strftime("%Y-%m-%d")
        budget = _budget_minutes(profile, day)
        tolerance = budget * PACK_TOLERANCE
        remaining = [it for it in active if int(it["id"]) not in released]
        if not remaining:
            break
        picks: list[dict[str, Any]] = []
        used = 0.0
        in_result: set[int] = set()
        for it in remaining:
            if it.get("need_refresh"):
                est = _est_minutes(conn, it)
                if used > 0 and used + est > tolerance:
                    continue
                picks.append(it)
                in_result.add(int(it["id"]))
                used += est
        pool = [it for it in remaining if int(it["id"]) not in in_result]
        for it in _interleave_by_module(pool):
            est = _est_minutes(conn, it)
            if used > 0 and used + est > tolerance:
                continue
            picks.append(it)
            in_result.add(int(it["id"]))
            used += est
        if not picks:
            break
        for it in picks:
            released.add(int(it["id"]))
        schedule.append(
            {
                "task_date": day,
                "items": [
                    {
                        "title": _plan_item_preview_title(conn, it),
                        "module_type": it.get("module_type"),
                        "item_type": it.get("item_type"),
                        "est_minutes": _est_minutes(conn, it),
                    }
                    for it in picks
                ],
                "units_total": len(picks),
            }
        )
    return schedule


def _student_upcoming_bundle(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    task_date: Optional[str] = None,
    days: int = UNITS_PREVIEW_DAYS,
) -> dict[str, Any]:
    """Read-only future schedule + remaining plan queue (does not write daily_tasks)."""
    task_date = task_date or china_ymd()
    tomorrow = (
        datetime.strptime(task_date, "%Y-%m-%d").date() + timedelta(days=1)
    ).strftime("%Y-%m-%d")
    plan_items = [
        dict(r)
        for r in conn.execute(
            """
            SELECT p.*, u.title AS unit_title
            FROM plan_items p
            LEFT JOIN task_units u ON u.unit_id = p.unit_id
            WHERE p.student_id=? AND p.status='pending'
            ORDER BY p.sort_order
            """,
            (student_id,),
        ).fetchall()
    ]
    for it in plan_items:
        it["test_unit_ids"] = _parse_json_list(it.get("test_unit_ids"))
    remaining = _remaining_plan_items(conn, plan_items)
    profile = ensure_time_profile(conn, student_id)
    mode = _effective_pack_mode(profile)
    if mode == PACK_MODE_UNITS_PER_DAY:
        # Align with teacher: simulate from today (locked daily if any), then drop today.
        full = _aligned_units_schedule(
            conn,
            student_id,
            plan_items,
            start_date=task_date,
            quota_resolver=lambda day: _resolve_units_quota_map(
                conn, student_id, day, plan_items
            ),
            days=days + 1,
        )
        schedule = [d for d in full if (d.get("task_date") or "") >= tomorrow]
    else:
        released = _released_plan_item_ids(conn, student_id)
        schedule = _preview_time_budget_schedule(
            conn,
            plan_items,
            tomorrow,
            profile=profile,
            days=days,
            initial_released=released,
        )
    while schedule and not schedule[-1].get("items"):
        schedule.pop()
    return {
        "upcoming_schedule": schedule,
        "remaining_plan": remaining,
    }

def update_scope_progress(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    *,
    scope_done: Optional[int] = None,
    delta: Optional[int] = None,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    unit = None
    if item["unit_id"]:
        unit = conn.execute(
            "SELECT * FROM task_units WHERE unit_id=?", (item["unit_id"],)
        ).fetchone()
    scope_total, _ = _scope_for_unit(unit["content_ref"] if unit else {})
    existing = conn.execute(
        "SELECT * FROM task_unit_progress WHERE student_id=? AND plan_item_id=?",
        (student_id, plan_item_id),
    ).fetchone()
    current = int(existing["scope_done"]) if existing else 0
    if scope_done is not None:
        current = max(0, int(scope_done))
    elif delta is not None:
        current = max(0, current + int(delta))
    if scope_total:
        current = min(current, scope_total)
    conn.execute(
        """
        INSERT INTO task_unit_progress (student_id, plan_item_id, unit_id, scope_done, scope_total)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id, plan_item_id) DO UPDATE SET
            scope_done=excluded.scope_done,
            scope_total=excluded.scope_total,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        """,
        (student_id, plan_item_id, item["unit_id"] or "", current, scope_total),
    )
    conn.commit()
    return {"scope_done": current, "scope_total": scope_total}


def complete_study(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    content_version: str,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    if item["item_type"] != "study":
        raise ValueError("非学习条目")
    unit = conn.execute(
        "SELECT * FROM task_units WHERE unit_id=?", (item["unit_id"],)
    ).fetchone()
    if unit and str(unit["content_version"]) != str(content_version):
        raise ValueError("内容版本已更新，请刷新后重学")

    scope_total = 0
    if unit:
        scope_total, _ = _scope_for_unit(unit["content_ref"])
    if scope_total and unit and unit["module_type"] == "reading_synonym":
        prog = conn.execute(
            "SELECT scope_done FROM task_unit_progress WHERE student_id=? AND plan_item_id=?",
            (student_id, plan_item_id),
        ).fetchone()
        done = int(prog["scope_done"]) if prog else 0
        if done < scope_total:
            raise ValueError(f"请先完成本单元全部 {scope_total} 组练习（当前 {done}/{scope_total}）")

    # Gendu: day complete needs 3 practices; never mark plan study_completed here
    # (lesson advance is driven by ≥70% + next-day pointer).
    if unit and str(unit["module_type"]) == GENDU_MODULE:
        today = china_ymd()
        daily = conn.execute(
            """
            SELECT gendu_practice_count, state FROM daily_tasks
            WHERE student_id=? AND task_date=? AND plan_item_id=?
            """,
            (student_id, today, plan_item_id),
        ).fetchone()
        count = int(daily["gendu_practice_count"] or 0) if daily else 0
        if count < GENDU_DAILY_PRACTICES:
            raise ValueError(
                f"听力跟读当日需完成 {GENDU_DAILY_PRACTICES} 次（当前 {count}/{GENDU_DAILY_PRACTICES}）"
            )
        conn.execute(
            """
            UPDATE daily_tasks SET state='done_study'
            WHERE student_id=? AND task_date=? AND plan_item_id=?
            """,
            (student_id, today, plan_item_id),
        )
        conn.commit()
        return get_today(conn, student_id)

    conn.execute(
        """
        UPDATE plan_items SET
            study_completed=1,
            study_completed_version=?,
            need_refresh=0,
            last_completed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE id=?
        """,
        (content_version, plan_item_id),
    )
    today = china_ymd()
    conn.execute(
        """
        UPDATE daily_tasks SET state='done_study'
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (student_id, today, plan_item_id),
    )
    if unit:
        scope_total, _ = _scope_for_unit(unit["content_ref"])
        update_scope_progress(
            conn, student_id, plan_item_id, scope_done=scope_total or 1
        )
    conn.commit()
    return get_today(conn, student_id)


def submit_stage_test(
    conn: sqlite3.Connection,
    student_id: str,
    plan_item_id: int,
    score: float,
    *,
    threshold: float,
    details: Any = None,
) -> dict[str, Any]:
    item = conn.execute(
        "SELECT * FROM plan_items WHERE id=? AND student_id=?",
        (plan_item_id, student_id),
    ).fetchone()
    if not item:
        raise ValueError("计划条目不存在")
    if item["item_type"] != "test":
        raise ValueError("非测试条目")

    today = china_ymd()
    attempts = int(item["test_attempt_count_today"] or 0)
    if item["test_attempt_ymd"] != today:
        attempts = 0
    if attempts >= 2 and not item["test_passed"]:
        raise ValueError("今日重测次数已用尽，请联系助教")

    passed = score >= threshold
    attempts += 1
    conn.execute(
        """
        UPDATE plan_items SET
            test_passed=?,
            test_attempt_count_today=?,
            test_attempt_ymd=?,
            last_completed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
        WHERE id=?
        """,
        (1 if passed else 0, attempts, today, plan_item_id),
    )
    state = "done_pass" if passed else "done_fail"
    conn.execute(
        """
        UPDATE daily_tasks SET state=?
        WHERE student_id=? AND task_date=? AND plan_item_id=?
        """,
        (state, student_id, today, plan_item_id),
    )
    # D21: write test_records with stage_test kind
    conn.execute(
        """
        INSERT INTO test_records (
            student_id, module_type, module_name, test_type,
            score, correct_count, total_count, is_passed, pass_threshold,
            details
        ) VALUES (?, ?, ?, 'stage_test', ?, 0, 0, ?, ?, ?)
        """,
        (
            student_id,
            item["module_type"] or "reading_synonym",
            item["test_title"] or "阶段测",
            float(score),
            1 if passed else 0,
            float(threshold),
            json.dumps(details if details is not None else {}, ensure_ascii=False),
        ),
    )
    conn.commit()
    return {
        "passed": passed,
        "score": score,
        "threshold": threshold,
        "attempts_today": attempts,
        "today": get_today(conn, student_id),
    }


def insert_stage_test(
    conn: sqlite3.Connection,
    student_id: str,
    *,
    unit_ids: list[str],
    after_sort_order: Optional[int] = None,
    test_title: str = "",
) -> dict[str, Any]:
    """Insert a stage test into draft, immediately after the last covered study unit."""
    if not unit_ids:
        raise ValueError("unit_ids 不能为空")
    units = []
    for uid in unit_ids:
        u = conn.execute("SELECT * FROM task_units WHERE unit_id=?", (uid,)).fetchone()
        if not u:
            raise ValueError(f"未知单元: {uid}")
        units.append(dict(u))
    module_types = {u["module_type"] for u in units}
    if len(module_types) > 1:
        raise ValueError("阶段测只能覆盖同一科目，请勿跨科勾选")
    module_type = units[0]["module_type"]
    title = test_title or (
        f"{units[0]['title']}–{units[-1]['title']} 阶段测"
        if len(units) > 1
        else f"{units[0]['title']} 阶段测"
    )

    plan = get_plan(conn, student_id)
    source = plan["draft"] if plan["draft"] else plan["live"]
    items = []
    for it in source:
        items.append(
            {
                "item_type": it["item_type"],
                "unit_id": it.get("unit_id"),
                "module_type": it.get("module_type"),
                "test_unit_ids": it.get("test_unit_ids") or [],
                "test_title": it.get("test_title") or "",
                "est_minutes": it.get("est_minutes"),
                "status": it.get("status") or "pending",
            }
        )

    unit_id_set = set(unit_ids)
    last_idx = -1
    found: set[str] = set()
    for i, it in enumerate(items):
        if it.get("item_type") == "study" and it.get("unit_id") in unit_id_set:
            last_idx = i
            found.add(it["unit_id"])
    missing = unit_id_set - found
    if missing:
        raise ValueError("请先将所有覆盖单元加入清单后再插测")

    # Reject duplicate test covering exact same units
    for it in items:
        if it.get("item_type") != "test":
            continue
        existing = set(_parse_json_list(it.get("test_unit_ids")) or [])
        if existing == unit_id_set:
            raise ValueError("已有相同范围的阶段测，请勿重复插入")

    insert_at = last_idx + 1
    if after_sort_order is not None:
        insert_at = min(int(after_sort_order) + 1, len(items))

    items.insert(
        insert_at,
        {
            "item_type": "test",
            "unit_id": None,
            "module_type": module_type,
            "test_unit_ids": unit_ids,
            "test_title": title,
            "est_minutes": 20,
            "status": "pending",
        },
    )
    items = normalize_stage_test_positions(items)
    return put_plan_draft(conn, student_id, items)


def plan_status_for_parent(conn: sqlite3.Connection, student_id: str, parent_module: str) -> str:
    rows = conn.execute(
        """
        SELECT p.id, u.parent_module, p.module_type
        FROM plan_items p
        LEFT JOIN task_units u ON u.unit_id = p.unit_id
        WHERE p.student_id=? AND p.status!='removed'
        """,
        (student_id,),
    ).fetchall()
    for r in rows:
        pm = r["parent_module"] or r["module_type"]
        if r["module_type"] and r["module_type"].startswith("speaking"):
            pm = "speaking"
        if pm == parent_module:
            return "in_plan"
    return "not_in_plan"
