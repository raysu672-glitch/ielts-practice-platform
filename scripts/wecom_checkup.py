"""WeCom learning-group digest for local full student checkup (read-only)."""

from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")

GROUP_HINT_RE = re.compile(r"学习群|打卡群|一对一|一对二|1v1|1v2|提高群", re.I)
CLASS_GROUP_RE = re.compile(r"^\d{8}.+班")
CHECKIN_KW = ("打卡", "完成", "任务", "扇贝", "学习系统", "已完成", "今日任务")
NUDGE_KW = ("催", "记得", "别忘", "今天", "尽快", "抓紧", "作业", "默写", "截图", "请")
PROMISE_KW = ("忘了", "记下", "今天记", "明天", "马上", "好的", "收到", "抱歉", "对不起")
ASSIGN_KW = ("扇贝", "词表", "默写", "写作", "跟读", "听力", "阅读", "任务一", "任务二", "打卡内容")
# Internal corp accounts often start with 168885…; external/student-ish with 7881…
TEACHER_ID_PREFIXES = ("168885",)


def open_ro(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def extract_utf8_fragments(blob: Any, *, max_len: int = 400) -> str:
    """Pull printable UTF-8 text from WeCom protobuf message blobs."""
    if blob is None:
        return ""
    if isinstance(blob, str):
        text = blob
    elif isinstance(blob, (bytes, bytearray, memoryview)):
        raw = bytes(blob)
        text = raw.decode("utf-8", errors="ignore")
    else:
        return ""
    # Drop mostly-control protobuf noise; keep CJK / ascii printables.
    cleaned = []
    for ch in text:
        o = ord(ch)
        if ch in "\n\r\t":
            cleaned.append(" ")
        elif o >= 32 or (0x4E00 <= o <= 0x9FFF):
            cleaned.append(ch)
    out = "".join(cleaned)
    out = re.sub(r"\s+", " ", out).strip()
    if len(out) > max_len:
        return out[: max_len - 1] + "…"
    return out


def _is_teacher_sender(sender_id: Any) -> bool:
    sid = str(sender_id or "")
    return any(sid.startswith(p) for p in TEACHER_ID_PREFIXES)


def match_learning_groups(
    session_conn: sqlite3.Connection,
    student_name: str,
) -> list[dict[str, Any]]:
    """Find learning groups whose title contains the student name."""
    name = str(student_name or "").strip()
    if not name or len(name) < 2:
        return []
    rows = session_conn.execute(
        """
        SELECT id, name, last_message_time, create_time
        FROM conversation_table
        WHERE name LIKE ?
        ORDER BY last_message_time DESC
        """,
        (f"%{name}%",),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        gname = str(r["name"] or "")
        if name not in gname:
            continue
        # Class big-groups without personal learning hint are skipped unless
        # the personal name is clearly the subject (already required above).
        if CLASS_GROUP_RE.match(gname) and not GROUP_HINT_RE.search(gname):
            continue
        if not GROUP_HINT_RE.search(gname) and "雅思" not in gname and "打卡" not in gname:
            # Still keep if name is in title and looks like personal group.
            if "学习" not in gname and "一对" not in gname:
                continue
        out.append(
            {
                "conversation_id": str(r["id"]),
                "name": gname,
                "last_message_time": int(r["last_message_time"] or 0),
                "create_time": int(r["create_time"] or 0),
            }
        )
    return out


def pick_primary_group(
    candidates: list[dict[str, Any]],
) -> tuple[Optional[dict[str, Any]], str]:
    """Prefer recent personal learning/check-in groups; return confidence."""
    if not candidates:
        return None, "none"
    if len(candidates) == 1:
        return candidates[0], "unique"
    # Prefer 打卡群 / 一对一 over multi-name shared groups when possible.
    scored: list[tuple[int, dict[str, Any]]] = []
    for g in candidates:
        score = int(g.get("last_message_time") or 0)
        n = str(g.get("name") or "")
        if "打卡群" in n:
            score += 10_000_000
        if GROUP_HINT_RE.search(n):
            score += 1_000_000
        # Penalize multi-student titles a bit (two CJK names jammed).
        if len(re.findall(r"[\u4e00-\u9fff]{2,4}", n)) >= 3:
            score -= 500_000
        scored.append((score, g))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1], "multi_pick_latest"


def _ts_to_cn(ts: int) -> str:
    if not ts:
        return ""
    try:
        # WeCom send_time is unix seconds.
        if ts > 10_000_000_000:
            ts = ts // 1000
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(SHANGHAI)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (OverflowError, OSError, ValueError):
        return str(ts)


def _analyze_conversation_messages(
    rows: list[Any],
    voice_map: dict[int, str],
    *,
    group_label: str,
    max_samples: int,
) -> dict[str, Any]:
    student_msgs = 0
    teacher_msgs = 0
    checkin_msgs = 0
    nudge_msgs = 0
    promise_msgs = 0
    assign_msgs = 0
    last_student_ts = 0
    checkin_days: set[str] = set()
    student_speak_days: set[str] = set()
    samples: list[str] = []
    # response delay: after teacher msg, next student msg lag (hours)
    delays_h: list[float] = []
    pending_teacher_ts: Optional[int] = None

    # Process oldest->newest for delay, but samples newest first later
    chronological = sorted(rows, key=lambda r: int(r["send_time"] or 0))
    for r in chronological:
        mid = int(r["message_id"] or 0)
        ts = int(r["send_time"] or 0)
        is_teacher = _is_teacher_sender(r["sender_id"])
        text = voice_map.get(mid) or extract_utf8_fragments(r["content"])
        if is_teacher:
            teacher_msgs += 1
            pending_teacher_ts = ts
            if text and any(k in text for k in NUDGE_KW):
                nudge_msgs += 1
            if text and any(k in text for k in ASSIGN_KW):
                assign_msgs += 1
        else:
            student_msgs += 1
            if ts > last_student_ts:
                last_student_ts = ts
            day = _ts_to_cn(ts)[:10]
            if day:
                student_speak_days.add(day)
            if pending_teacher_ts and ts >= pending_teacher_ts:
                delays_h.append((ts - pending_teacher_ts) / 3600.0)
                pending_teacher_ts = None
            if text and any(k in text for k in PROMISE_KW):
                promise_msgs += 1
        if text and any(k in text for k in CHECKIN_KW):
            checkin_msgs += 1
            day = _ts_to_cn(ts)[:10]
            if day:
                checkin_days.add(day)

    for r in sorted(rows, key=lambda x: int(x["send_time"] or 0), reverse=True):
        if len(samples) >= max_samples:
            break
        mid = int(r["message_id"] or 0)
        ts = int(r["send_time"] or 0)
        role = "老师侧" if _is_teacher_sender(r["sender_id"]) else "学生侧"
        text = voice_map.get(mid) or extract_utf8_fragments(r["content"])
        if not text:
            continue
        samples.append(f"{_ts_to_cn(ts)} | {group_label} | {role} | {text}")

    stale_days = None
    if last_student_ts:
        last_dt = datetime.fromtimestamp(last_student_ts, tz=timezone.utc)
        stale_days = max(0, (datetime.now(timezone.utc) - last_dt).days)

    avg_delay = round(sum(delays_h) / len(delays_h), 2) if delays_h else None
    return {
        "window_messages": len(rows),
        "student_messages": student_msgs,
        "teacher_messages": teacher_msgs,
        "checkin_related_messages": checkin_msgs,
        "nudge_related_messages": nudge_msgs,
        "promise_related_messages": promise_msgs,
        "assign_related_messages": assign_msgs,
        "checkin_days": sorted(checkin_days),
        "checkin_days_count": len(checkin_days),
        "student_speak_days": sorted(student_speak_days),
        "last_student_message_at": _ts_to_cn(last_student_ts),
        "days_since_last_student_message": stale_days,
        "student_reply_delay_hours_avg": avg_delay,
        "student_reply_delay_samples": len(delays_h),
        "sample_lines": samples,
    }


def build_wecom_group_summary(
    wecom_dir: Path | str,
    *,
    student_name: str,
    days: int = 14,
    max_samples: int = 50,
    merge_all_groups: bool = True,
) -> dict[str, Any]:
    """Match student learning group(s) and compress recent chat for AI."""
    root = Path(wecom_dir)
    days = max(1, min(int(days or 14), 30))
    max_samples = max(5, min(int(max_samples or 50), 100))
    empty: dict[str, Any] = {
        "student_name": student_name,
        "days": days,
        "match_confidence": "none",
        "primary_group": None,
        "candidates": [],
        "per_group": [],
        "stats": {},
        "checkin_days": [],
        "sample_lines": [],
        "error": None,
    }
    session_path = root / "session.db"
    message_path = root / "message.db"
    if not session_path.is_file() or not message_path.is_file():
        empty["error"] = f"缺少 session.db 或 message.db：{root}"
        return empty

    session_conn = open_ro(session_path)
    try:
        candidates = match_learning_groups(session_conn, student_name)
    finally:
        session_conn.close()

    primary, confidence = pick_primary_group(candidates)
    empty["candidates"] = [
        {"conversation_id": c["conversation_id"], "name": c["name"]} for c in candidates
    ]
    empty["match_confidence"] = confidence
    if not primary:
        empty["error"] = "未匹配到学习群"
        return empty
    empty["primary_group"] = {
        "conversation_id": primary["conversation_id"],
        "name": primary["name"],
    }

    groups = candidates if merge_all_groups else [primary]
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_ts = int(cutoff.timestamp())

    msg_conn = open_ro(message_path)
    try:
        voice_map = {
            int(r["message_id"]): str(r["text"] or "")
            for r in msg_conn.execute(
                "SELECT message_id, text FROM msg_voice2text WHERE text IS NOT NULL AND text != ''"
            )
        }
        per_group: list[dict[str, Any]] = []
        all_checkin_days: set[str] = set()
        all_samples: list[str] = []
        totals = {
            "window_messages": 0,
            "student_messages": 0,
            "teacher_messages": 0,
            "checkin_related_messages": 0,
            "nudge_related_messages": 0,
            "promise_related_messages": 0,
            "assign_related_messages": 0,
        }
        last_student_ts = 0
        delay_vals: list[float] = []
        delay_n = 0

        per_sample_cap = max(8, max_samples // max(1, len(groups)))
        for g in groups:
            rows = msg_conn.execute(
                """
                SELECT message_id, sender_id, content_type, send_time, content
                FROM message_table
                WHERE conversation_id = ? AND send_time >= ?
                ORDER BY send_time DESC
                LIMIT 800
                """,
                (g["conversation_id"], cutoff_ts),
            ).fetchall()
            label = str(g["name"] or g["conversation_id"])[:40]
            analyzed = _analyze_conversation_messages(
                list(rows), voice_map, group_label=label, max_samples=per_sample_cap
            )
            per_group.append(
                {
                    "conversation_id": g["conversation_id"],
                    "name": g["name"],
                    "stats": {
                        k: analyzed[k]
                        for k in (
                            "window_messages",
                            "student_messages",
                            "teacher_messages",
                            "checkin_related_messages",
                            "nudge_related_messages",
                            "promise_related_messages",
                            "assign_related_messages",
                            "checkin_days_count",
                            "last_student_message_at",
                            "days_since_last_student_message",
                            "student_reply_delay_hours_avg",
                        )
                    },
                }
            )
            for k in totals:
                totals[k] += int(analyzed.get(k) or 0)
            all_checkin_days.update(analyzed.get("checkin_days") or [])
            all_samples.extend(analyzed.get("sample_lines") or [])
            # track latest student across groups
            at = analyzed.get("last_student_message_at") or ""
            if at:
                try:
                    dt = datetime.strptime(at, "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=SHANGHAI
                    )
                    ts = int(dt.astimezone(timezone.utc).timestamp())
                    if ts > last_student_ts:
                        last_student_ts = ts
                except ValueError:
                    pass
            if analyzed.get("student_reply_delay_hours_avg") is not None:
                n = int(analyzed.get("student_reply_delay_samples") or 0)
                if n:
                    delay_vals.append(
                        float(analyzed["student_reply_delay_hours_avg"]) * n
                    )
                    delay_n += n
    finally:
        msg_conn.close()

    stale_days = None
    if last_student_ts:
        last_dt = datetime.fromtimestamp(last_student_ts, tz=timezone.utc)
        stale_days = max(0, (datetime.now(timezone.utc) - last_dt).days)

    empty["per_group"] = per_group
    empty["checkin_days"] = sorted(all_checkin_days)
    empty["stats"] = {
        **totals,
        "groups_analyzed": len(groups),
        "checkin_days_count": len(all_checkin_days),
        "checkin_days": sorted(all_checkin_days),
        "last_student_message_at": _ts_to_cn(last_student_ts),
        "days_since_last_student_message": stale_days,
        "student_reply_delay_hours_avg": round(sum(delay_vals) / delay_n, 2)
        if delay_n
        else None,
    }
    # newest samples first across groups
    empty["sample_lines"] = all_samples[:max_samples]
    return empty


def format_wecom_summary_prompt(summary: dict[str, Any]) -> str:
    lines = [
        f"企微匹配置信度：{summary.get('match_confidence')}",
        f"统计窗口：近 {summary.get('days')} 天",
    ]
    if summary.get("error"):
        lines.append(f"企微错误/缺口：{summary.get('error')}")
    primary = summary.get("primary_group") or {}
    if primary:
        lines.append(f"主群偏好：{primary.get('name')} ({primary.get('conversation_id')})")
    per = summary.get("per_group") or []
    if per:
        lines.append("分群统计：")
        for g in per:
            st = g.get("stats") or {}
            lines.append(
                f"- {g.get('name')}: 消息{st.get('window_messages')} "
                f"学生{st.get('student_messages')}/老师{st.get('teacher_messages')} "
                f"打卡相关{st.get('checkin_related_messages')} "
                f"催促类{st.get('nudge_related_messages')} "
                f"布置类{st.get('assign_related_messages')} "
                f"承诺/忘了类{st.get('promise_related_messages')} "
                f"打卡天{st.get('checkin_days_count')} "
                f"最近学生 {st.get('last_student_message_at')} "
                f"回复延迟均{st.get('student_reply_delay_hours_avg')}h"
            )
    stats = summary.get("stats") or {}
    if stats:
        lines.append(
            "合并统计："
            f"群数 {stats.get('groups_analyzed')} · "
            f"消息 {stats.get('window_messages')} · "
            f"学生侧 {stats.get('student_messages')} · "
            f"老师侧 {stats.get('teacher_messages')} · "
            f"打卡相关 {stats.get('checkin_related_messages')} · "
            f"催促 {stats.get('nudge_related_messages')} · "
            f"布置 {stats.get('assign_related_messages')} · "
            f"承诺/忘了 {stats.get('promise_related_messages')} · "
            f"打卡天 {stats.get('checkin_days_count')} "
            f"{stats.get('checkin_days')} · "
            f"最近学生发言 {stats.get('last_student_message_at')} · "
            f"距今 {stats.get('days_since_last_student_message')} 天 · "
            f"回复延迟均 {stats.get('student_reply_delay_hours_avg')} h"
        )
    lines.append("群聊样本（新→旧，含群名）：")
    lines.extend(summary.get("sample_lines") or [])
    text = "\n".join(str(x) for x in lines)
    if len(text) > 12000:
        return text[:11900] + "\n…(截断)"
    return text
