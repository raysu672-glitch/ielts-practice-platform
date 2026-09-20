"""给模拟学生「李哲」排一套学习计划（对齐学情档案里的 P0–P3 提分优先级）。

关键前提：平台的装箱算法 `task_api._interleave_by_module` 会 **按科目轮转**，
科目顺序 = 该科在清单里首次出现的顺序。因此「优先级」在平台上体现为：

  1. **轮转位次**——排在越前的科目，每天越先被装箱；
  2. **单元配额**——排入的单元越多，能推进的周期越长。

李哲的画像：工作日 90 分钟 / 周末 180 分钟 → 周末约 9 科全轮一遍，
工作日只轮到前 5 科。所以轮转位次按「每天都要做」的顺序设计：

  1 听力1000词   25′  ← 词汇底座，每天
  2 阅读同义替换 15′  ← 同义替换主线，每天
  3 口语P1       30′  ← 唯一必须每天开口的项
  4 听力同义替换 12′  ← 同义替换主线，每天
  5 长难句分析   20′  ← 输入能力
  6 听力基础词汇 35′  ← 词汇补量（周末）
  7 写作词伙     15′  ← 产出（周末）
  8 写作句子翻译 15′  ← 产出（周末）
  9 口语复合句   25′  ← 口语进阶（周末）

每学满 3 个单元插一次阶段测；阶段测位置由 `normalize_stage_test_positions`
归位到最后一个被覆盖单元之后。单元 id 全部从 `task_units` 按 `unit_no` 取。

注意：听力P4跟读（`listening_p4_speed`）走独立的 30 天跟读任务机制
（`student_gendu_assignment`），不放进这份清单，避免两套进度互相干扰。

用法
----
    python scripts/plan_mock_student.py                 # 预览，不写库
    python scripts/plan_mock_student.py --apply         # 写库并生成今日任务
    python scripts/plan_mock_student.py --apply --reset # 先清空该生既有计划
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import task_api as ta  # noqa: E402

DEFAULT_DB = ROOT / "data" / "ielts_local.db"
DEFAULT_STUDENT_ID = "2026001"
STAGE_TEST_EVERY_N = 3

# 按分钟装箱（time_budget）已下线：排程只按「每科每日单元配额」。
# 工作日只轮到 5 个主线科目、周末 9 科全开，近似原来的 90′ / 180′ 节奏。
WEEKDAY_MODULES = {
    "dictation",
    "reading_synonym",
    "speaking_p1",
    "listening_synonym",
    "sentence",
}

# (module_type, 排入单元数, 轮转位次说明)
PLAN_MODULES = [
    ("dictation", 12, "词汇底座 · 工作日也轮到"),
    ("reading_synonym", 14, "同义替换主线 · 工作日也轮到"),
    ("speaking_p1", 12, "每日开口 · 工作日也轮到"),
    ("listening_synonym", 14, "同义替换主线 · 工作日也轮到"),
    ("sentence", 8, "长难句 · 工作日也轮到"),
    ("listening_basic", 6, "词汇补量 · 主要在周末"),
    ("writing_phrase", 10, "写作产出 · 主要在周末"),
    ("writing_translate", 8, "写作产出 · 主要在周末"),
    ("speaking_complex", 6, "口语进阶 · 主要在周末"),
]

MODULE_NAMES = {
    "dictation": "听力1000词",
    "listening_basic": "听力基础词汇",
    "reading_synonym": "阅读同义替换",
    "listening_synonym": "听力同义替换",
    "sentence": "长难句分析",
    "writing_phrase": "写作词伙",
    "writing_translate": "写作句子翻译",
    "speaking_p1": "口语P1",
    "speaking_complex": "口语复合句",
}

RESET_TABLES = [
    "daily_tasks",
    "plan_items",
    "plan_items_draft",
    "plan_draft_meta",
    "task_unit_progress",
    "student_attention_state",
    "student_attention_events",
    "student_gendu_assignment",
    "gendu_practice_events",
]


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()
        is not None
    )


def fetch_unit_ids(conn: sqlite3.Connection, module_type: str, count: int) -> list[str]:
    rows = conn.execute(
        """
        SELECT unit_id FROM task_units
        WHERE module_type = ? AND is_active = 1
        ORDER BY unit_no LIMIT ?
        """,
        (module_type, count),
    ).fetchall()
    ids = [str(r["unit_id"]) for r in rows]
    if len(ids) < count:
        raise SystemExit(
            f"[ERROR] {module_type} 只有 {len(ids)} 个可用单元，排不下 {count} 个"
        )
    return ids


def first_gendu_unit(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        """
        SELECT unit_id FROM task_units
        WHERE module_type = ? AND is_active = 1
        ORDER BY unit_no LIMIT 1
        """,
        (ta.GENDU_MODULE,),
    ).fetchone()
    if not row:
        raise SystemExit("[ERROR] 库里没有可用的听力跟读单元")
    return str(row["unit_id"])


def attach_gendu(conn: sqlite3.Connection, student_id: str, start_unit_id: str) -> dict:
    """挂 30 天听力P4跟读任务（平台自己的 gendu 机制，不进清单）。"""
    return ta.put_gendu_assignment(
        conn, student_id, {"start_unit_id": start_unit_id}
    )["gendu_assignment"]


def build_items(conn: sqlite3.Connection) -> list[dict]:
    """按 PLAN_MODULES 顺序生成清单；同科内单元顺序推进，每 3 单元插一次阶段测。"""
    items: list[dict] = []
    for module_type, count, _note in PLAN_MODULES:
        units = fetch_unit_ids(conn, module_type, count)
        for unit_id in units:
            items.append({"item_type": "study", "unit_id": unit_id})
        for start in range(0, len(units), STAGE_TEST_EVERY_N):
            chunk = units[start : start + STAGE_TEST_EVERY_N]
            if len(chunk) < 2:
                continue
            items.append(
                {
                    "item_type": "test",
                    "module_type": module_type,
                    "test_unit_ids": chunk,
                    "test_title": (
                        f"{MODULE_NAMES[module_type]} "
                        f"U{start + 1}–U{start + len(chunk)} 阶段测"
                    ),
                }
            )
    return items


def reset_plan(conn: sqlite3.Connection, student_id: str) -> list[str]:
    touched: list[str] = []
    for table in RESET_TABLES:
        if not table_exists(conn, table):
            continue
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if "student_id" not in cols:
            continue
        cur = conn.execute(f"DELETE FROM {table} WHERE student_id = ?", (student_id,))
        if cur.rowcount:
            touched.append(f"{table}({cur.rowcount})")
    conn.commit()
    return touched


def quota_payload() -> list[dict]:
    """各科每日配额（装箱唯一依据）。

    工作日：只有主线 5 科各 1 单元；周末：9 科各 1 单元。
    跟读（listening_p4_speed）不在这里——它由 gendu 机制每天保证 1 条。
    """
    return [
        {
            "module_type": module_type,
            "weekday_units": 1 if module_type in WEEKDAY_MODULES else 0,
            "weekend_units": 1,
        }
        for module_type, _count, _note in PLAN_MODULES
    ]


def quota_summary() -> str:
    weekday = len(WEEKDAY_MODULES)
    weekend = len(PLAN_MODULES)
    return f"工作日 {weekday} 科 × 1 单元 / 周末 {weekend} 科 × 1 单元"


def print_pack(items: list[dict], label: str) -> None:
    total = sum(int(x.get("est_minutes") or 0) for x in items)
    kinds = sum(1 for x in items if x.get("item_type") == "study")
    print(f"\n{label}：{len(items)} 条（{kinds} 学）· 约 {total} 分钟")
    for it in items:
        kind = "学" if it.get("item_type") == "study" else "测"
        print(
            f"  {kind} · {str(it.get('title') or it.get('unit_id')):<40}"
            f" {it.get('est_minutes')}′  {it.get('state') or it.get('priority_class') or ''}"
        )


def describe(conn: sqlite3.Connection, student_id: str) -> None:
    plan = ta.get_plan(conn, student_id)
    prog = plan.get("progress") or {}
    print("\n计划轨（学 X/Y · 过关 A/B）：")
    for module_type, _count, _note in PLAN_MODULES:
        p = prog.get(module_type)
        if not p:
            continue
        print(
            f"  {MODULE_NAMES[module_type]:<12} 学 {p['study_x']}/{p['study_y']}"
            f" · 过关 {p['pass_a']}/{p['pass_b']}"
        )

    today = ta.get_today(conn, student_id)
    profile = ta.get_time_profile(conn, student_id)
    items = today.get("items") or []
    print(
        f"\n今日任务（{today.get('task_date')}）· 预算 工作日 {profile.get('weekday_minutes')}′"
        f" / 周末 {profile.get('weekend_minutes')}′ · 装箱模式 {profile.get('pack_mode')}"
    )
    for it in items:
        kind = "学" if it.get("item_type") == "study" else "测"
        print(
            f"  {kind} · {str(it.get('title') or it.get('unit_id')):<40}"
            f" {it.get('est_minutes')}′  {it.get('state')}"
        )

    upcoming = today.get("upcoming_schedule") or []
    if upcoming:
        print("\n后续预览（装箱模拟）：")
        for day in upcoming[:7]:
            titles = [str(x.get("title") or x.get("unit_id")) for x in day.get("items") or []]
            mins = sum(int(x.get("est_minutes") or 0) for x in day.get("items") or [])
            print(f"  {day.get('task_date')} 约 {mins}′ → {'、'.join(titles[:9])}")


def main() -> int:
    parser = argparse.ArgumentParser(description="给李哲排学习计划")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--student-id", default=DEFAULT_STUDENT_ID)
    parser.add_argument("--apply", action="store_true", help="真正写库（默认只预览）")
    parser.add_argument("--reset", action="store_true", help="先清空该生既有计划")
    parser.add_argument("--date", help="预览某一天（YYYY-MM-DD），默认今天")
    parser.add_argument("--gendu", action="store_true", help="同时挂 30 天听力P4跟读任务")
    parser.add_argument("--gendu-start", help="跟读起始单元 id（默认第一篇）")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"[ERROR] 数据库不存在：{args.db}")
        return 1

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    ta.ensure_task_tables(conn)

    row = conn.execute(
        "SELECT name, target_score, status FROM students WHERE student_id = ?",
        (args.student_id,),
    ).fetchone()
    if not row:
        print(f"[ERROR] 学号不存在：{args.student_id}，先跑 scripts/seed_mock_student.py")
        return 1

    items = build_items(conn)
    study_n = sum(1 for x in items if x["item_type"] == "study")

    print(f"学生：{row['name']}（{args.student_id}）· 目标 {row['target_score']} · {row['status']}")
    print(f"清单：{study_n} 学 + {len(items) - study_n} 测 = {len(items)} 条")
    print("\n轮转位次（越靠前越先装箱）：")
    for i, (module_type, count, note) in enumerate(PLAN_MODULES, 1):
        print(f"  {i} {MODULE_NAMES[module_type]:<12} ×{count:<3} {note}")

    preview = ta.preview_daily_pack_items(
        conn, args.student_id, items, task_date=args.date, module_quotas=quota_payload()
    )
    day = args.date or "今天"
    print_pack(
        preview.get("items") or [],
        f"[dry-run] {day} 排程（{quota_summary()}）",
    )

    if not args.apply:
        print("\n[dry-run] 未写库。加 --apply 执行。")
        return 0

    if args.reset:
        touched = reset_plan(conn, args.student_id)
        print(f"\n[reset] 已清理：{', '.join(touched) if touched else '无旧计划'}")

    # 装箱只按「每科每日配额」；分钟数已退化为参考预算，不再驱动排程。
    ta.put_time_profile(
        conn,
        args.student_id,
        {"module_quotas": quota_payload(), "effective": "today"},
    )
    print(
        f"\n[quotas] 已设为 {quota_summary()}"
    )

    ta.put_plan_draft(conn, args.student_id, items)
    print("\n[applied] 清单已下发并生成今日任务。")

    if args.gendu:
        start = args.gendu_start or first_gendu_unit(conn)
        asg = attach_gendu(conn, args.student_id, start)
        print(
            f"\n[gendu] 30 天跟读任务：{asg.get('start_title')}（{start}）"
            f"\n  {asg.get('starts_on')} → {asg.get('ends_on')} · "
            f"每日 {asg.get('daily_required')} 次 · 过关线 {asg.get('pass_score')}"
            f"\n  当前课文：{asg.get('current_title')} · 今天生效={asg.get('active')}"
        )

    describe(conn, args.student_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
