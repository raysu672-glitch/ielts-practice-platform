# -*- coding: utf-8 -*-
"""修复「跟读误换课」抹掉的历史每日任务。

背景（2026-09-18 修复的 bug）：跟读过关后本应「次日换篇」，但系统在回填
「昨日」时误判成新的一天而立刻换篇，于是把**昨天整天的任务删掉重建**：
  - 学生当天已完成的记录被抹掉，换成另一批未完成任务 → 昨日任务显示未完成
  - 新课文被塞进尚未布置的历史日期 → 幽灵任务 → 假积压

本脚本以「换篇前」的备份为准，对发生换篇的那一天做修复：
  - 跟读行：只保留换篇前那一篇（换篇本不该发生在当天）；练习次数按事件表重算
  - 其它行：换篇后新写入（写入日晚于当天）的删除；换篇前有、现在没有的还原；
    两边都有的保留现状（学生之后可能又做完了）

先 dry-run（默认），确认后加 --apply：
    python scripts/repair_gendu_swap_days.py --old backups/aliyun_XXXX PATH [--apply]

换篇后旧课的上报会被「请跟读当前指定课文」拒掉，日志里留下尝试、事件表里没有
分数。若老师确认当天做满了 3 遍，可加 --credit-attempts 按操作日志的跟读尝试次数
（上限 3）把被 bug 吃掉的那一次补回来。
"""
from __future__ import annotations

import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task_api import GENDU_MODULE, GENDU_DAILY_PRACTICES  # noqa: E402

SHANGHAI = ZoneInfo("Asia/Shanghai")
DEFAULT_DB = "data/ielts_local.db"
COLS = (
    "student_id",
    "task_date",
    "plan_item_id",
    "priority_class",
    "sort_in_day",
    "state",
    "locked",
    "forced",
    "created_at",
    "gendu_practice_count",
    "gendu_best_score",
)


def sh_ymd(raw: str | None) -> str | None:
    if not raw:
        return None
    text = str(raw)
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text[:10] if len(text) >= 10 else None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d")


def _load_rows(conn: sqlite3.Connection) -> dict[tuple[str, str], list[sqlite3.Row]]:
    out: dict[tuple[str, str], list[sqlite3.Row]] = {}
    for r in conn.execute(
        f"SELECT id, {', '.join(COLS)} FROM daily_tasks "
        "ORDER BY student_id, task_date, sort_in_day"
    ):
        out.setdefault((str(r["student_id"]), str(r["task_date"])), []).append(r)
    return out


def find_swap_days(
    old: dict[tuple[str, str], list[sqlite3.Row]],
    new: dict[tuple[str, str], list[sqlite3.Row]],
    gendu_units: dict[int, str],
) -> list[tuple[str, str]]:
    """找出「换篇当天」：(学生, 日期) 里跟读课被换成了另一篇。"""
    days: list[tuple[str, str]] = []
    for key, new_rows in new.items():
        old_rows = old.get(key)
        if not old_rows:
            continue
        old_gendu = {gendu_units.get(int(r["plan_item_id"])) for r in old_rows}
        new_gendu = {gendu_units.get(int(r["plan_item_id"])) for r in new_rows}
        old_gendu.discard(None)
        new_gendu.discard(None)
        if old_gendu and new_gendu and old_gendu != new_gendu:
            days.append(key)
    return sorted(days)


def _gendu_attempts_on(conn: sqlite3.Connection, student_id: str, day: str) -> int:
    """当天的跟读尝试次数（按操作日志 task.open 计）。

    换篇后旧课的上报会被「请跟读当前指定课文」拒掉，日志里留下了尝试、事件表里
    却没有分数。用于把这类被 bug 吃掉的那一次补回来。
    """
    n = 0
    for r in conn.execute(
        """
        SELECT created_at FROM activity_events
        WHERE actor_id=? AND action='task.open' AND module_type=?
        """,
        (student_id, GENDU_MODULE),
    ):
        if sh_ymd(r["created_at"]) == day:
            n += 1
    return n


def main() -> int:
    argv = sys.argv[1:]
    apply = "--apply" in argv
    credit_attempts = "--credit-attempts" in argv
    rest = [a for a in argv if a not in ("--apply", "--credit-attempts")]
    old_path = None
    if "--old" in rest:
        i = rest.index("--old")
        old_path = rest[i + 1]
        del rest[i : i + 2]
    db_path = rest[0] if rest else DEFAULT_DB
    if not old_path:
        print("必须提供 --old <换篇前的备份 db>")
        return 2
    for p in (old_path, db_path):
        if not Path(p).exists():
            print(f"文件不存在: {p}")
            return 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    old_conn = sqlite3.connect(old_path)
    old_conn.row_factory = sqlite3.Row

    if apply:
        stamp = datetime.now(SHANGHAI).strftime("%Y%m%d_%H%M%S")
        safety = Path(db_path).with_name(
            f"{Path(db_path).stem}.before_repair_{stamp}.db"
        )
        shutil.copyfile(db_path, safety)
        print(f"当前库已备份到: {safety}")

    gendu_units = {
        int(r["id"]): str(r["unit_id"])
        for r in conn.execute(
            "SELECT id, unit_id FROM plan_items WHERE module_type='listening_p4_speed'"
        )
    }
    old_rows = _load_rows(old_conn)
    new_rows = _load_rows(conn)
    days = find_swap_days(old_rows, new_rows, gendu_units)
    print(f"\n发现 {len(days)} 个「跟读被换篇」的日期: {days}")

    to_delete: list[int] = []
    to_insert: list[tuple] = []
    for key in days:
        sid, day = key
        cur = {int(r["plan_item_id"]): r for r in new_rows.get(key, [])}
        prev = {int(r["plan_item_id"]): r for r in old_rows.get(key, [])}
        old_units = {gendu_units.get(pid) for pid in prev}
        old_units.discard(None)
        for pid, r in cur.items():
            unit = gendu_units.get(pid)
            if unit:
                # 换篇当天：跟读只应保留换篇前那一篇
                if unit not in old_units:
                    to_delete.append(int(r["id"]))
                continue
            if pid in prev:
                continue
            if (sh_ymd(r["created_at"]) or "") > day:
                to_delete.append(int(r["id"]))
        for pid, r in prev.items():
            unit = gendu_units.get(pid)
            if not unit and pid in cur:
                continue  # 非跟读且两边都有 → 保留现状
            if unit and unit in old_units and pid in cur:
                continue  # 跟读且已是正确的篇章
            row = {c: r[c] for c in COLS}
            if unit:
                agg = conn.execute(
                    """
                    SELECT COUNT(*) AS c, MAX(score) AS best
                    FROM gendu_practice_events
                    WHERE student_id=? AND unit_id=? AND task_date=?
                    """,
                    (sid, unit, day),
                ).fetchone()
                cnt = int(agg["c"] or 0) if agg else 0
                row["gendu_practice_count"] = cnt
                row["gendu_best_score"] = float(agg["best"]) if cnt and agg["best"] is not None else None
                if credit_attempts:
                    attempts = _gendu_attempts_on(conn, sid, day)
                    need = min(GENDU_DAILY_PRACTICES, max(cnt, attempts))
                    if need > cnt:
                        print(
                            f"     （补记）{sid} @ {day} {unit}: 出分 {cnt} 次，"
                            f"日志尝试 {attempts} 次 → 记为 {need}/{GENDU_DAILY_PRACTICES}"
                        )
                        cnt = need
                        row["gendu_practice_count"] = cnt
                if cnt >= GENDU_DAILY_PRACTICES and row["state"] not in (
                    "done_study",
                    "done_pass",
                ):
                    row["state"] = "done_study"
            to_insert.append(tuple(row[c] for c in COLS))

    def unit_of(pid: int) -> str:
        return gendu_units.get(pid) or f"pid{pid}"

    print(f"将删除 {len(to_delete)} 行（误换课重建塞进来的）")
    print(f"将还原 {len(to_insert)} 行（学生真实的当日记录）")
    for key in days:
        sid, day = key
        print(f"\n  学号 {sid} @ {day}")
        for r in new_rows.get(key, []):
            if int(r["id"]) in to_delete:
                print(f"     删除  {unit_of(int(r['plan_item_id'])):26s} state={r['state']}")
        for tup in to_insert:
            if tup[0] == sid and tup[1] == day:
                print(f"     还原  {unit_of(int(tup[2])):26s} state={tup[5]}")

    if not apply:
        print(
            "\n（dry-run）确认后加 --apply 执行；"
            "如需按操作日志补记被换篇吃掉的跟读次数，加 --credit-attempts。"
        )
        return 0
    conn.executemany("DELETE FROM daily_tasks WHERE id=?", [(i,) for i in to_delete])
    if to_insert:
        ph = ", ".join("?" for _ in COLS)
        conn.executemany(
            f"INSERT INTO daily_tasks ({', '.join(COLS)}) VALUES ({ph})", to_insert
        )
    conn.commit()
    print(f"\n完成：删除 {len(to_delete)} 行，还原 {len(to_insert)} 行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
