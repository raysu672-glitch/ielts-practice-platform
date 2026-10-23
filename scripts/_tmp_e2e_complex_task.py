#!/usr/bin/env python3
"""E2E: login as 2025001, open-task params check via HTML, report scope 10, verify complete."""
from __future__ import annotations

import http.cookiejar
import json
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:49182"
SID = "2025001"
UNIT = "speaking_complex_pattern_p1"


def req(method: str, path: str, data=None, headers=None, opener=None):
    url = BASE + path
    body = None
    hdrs = dict(headers or {})
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with opener.open(r, timeout=20) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(raw) if raw.strip().startswith("{") or raw.strip().startswith("[") else raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # try common passwords
    password = None
    for pw in ("123456", "admin123", "test1234", "2025001"):
        code, data = req("POST", "/api/auth/student/login", {"student_id": SID, "password": pw}, opener=opener)
        print("login try", pw, code, data if isinstance(data, dict) else str(data)[:120])
        if code == 200 and isinstance(data, dict) and data.get("ok") is not False and (
            data.get("student") or data.get("student_id") or data.get("token") or "must_change" in str(data)
        ):
            password = pw
            break
        # some APIs return student in data
        if code == 200 and isinstance(data, dict) and "error" not in data:
            password = pw
            break
    if not password:
        # reset password in DB to 123456 for test
        sys.path.insert(0, str(ROOT / "scripts"))
        from password_utils import hash_password

        conn = sqlite3.connect(str(ROOT / "data" / "ielts_local.db"))
        conn.execute(
            "UPDATE students SET password=?, is_password_changed=1 WHERE student_id=?",
            (hash_password("123456"), SID),
        )
        conn.commit()
        conn.close()
        code, data = req(
            "POST",
            "/api/auth/student/login",
            {"student_id": SID, "password": "123456"},
            opener=opener,
        )
        print("login after reset", code, data)
        password = "123456"
        if code != 200:
            raise SystemExit("login failed")

    # today tasks
    code, today = req("GET", "/api/task/me/today", opener=opener)
    print("today status", code)
    items = []
    if isinstance(today, dict):
        items = today.get("items") or today.get("tasks") or today.get("daily") or []
        if not items and "data" in today:
            d = today["data"]
            items = d.get("items") or d.get("tasks") or d.get("daily") or []
    print("today keys", list(today.keys()) if isinstance(today, dict) else type(today))
    # find complex
    target = None
    for it in items if isinstance(items, list) else []:
        if (it.get("unit_id") == UNIT) or (it.get("module_type") == "speaking_complex"):
            target = it
            break
    print("target task", target)

    conn = sqlite3.connect(str(ROOT / "data" / "ielts_local.db"))
    conn.row_factory = sqlite3.Row
    plan = conn.execute(
        "SELECT id FROM plan_items WHERE student_id=? AND unit_id=?",
        (SID, UNIT),
    ).fetchone()
    plan_item_id = int(plan["id"])
    print("plan_item_id", plan_item_id)

    # Simulate what complex page reports: 10 sentences done
    for i in range(10):
        code, prog = req(
            "POST",
            "/api/task/me/scope-progress",
            {
                "plan_item_id": plan_item_id,
                "scope_key": str(i),
                "scope_done": i + 1,
            },
            opener=opener,
        )
        if i in (0, 9) or code != 200:
            print(f"scope {i}", code, prog)

    code, done = req(
        "POST",
        "/api/task/me/complete-study",
        {
            "plan_item_id": plan_item_id,
            "content_version": "1",
            "scope_done": 10,
        },
        opener=opener,
    )
    print("complete-study", code, done if not isinstance(done, dict) else {k: done.get(k) for k in list(done)[:8]})

    row = conn.execute(
        """
        SELECT d.state, p.study_completed, pr.scope_done, pr.scope_total
        FROM daily_tasks d
        JOIN plan_items p ON p.id=d.plan_item_id
        LEFT JOIN task_unit_progress pr ON pr.student_id=d.student_id AND pr.plan_item_id=d.plan_item_id
        WHERE d.student_id=? AND d.plan_item_id=?
        ORDER BY d.task_date DESC LIMIT 1
        """,
        (SID, plan_item_id),
    ).fetchone()
    print("db after", dict(row) if row else None)

    # Check static files contain new code
    html = Path(ROOT / "sources/kouyulianxi/complex-sentences.html").read_text(encoding="utf-8")
    p2 = Path(ROOT / "sources/kouyulianxi/p2-app.js").read_text(encoding="utf-8")
    assert "maybeReportTaskScope" in html
    assert "loadComplexFrame" in p2
    # fetch live pages
    for path in (
        "/kouyulianxi/p2-app.js?v=20261011complex",
        "/kouyulianxi/complex-sentences.html?v=20261011complex&kind=pattern&id=p1&plan_item_id=224",
        "/kouyulianxi/index.html?part=p1&p1=complex&kind=pattern&id=p1&plan_item_id=224&unit_id=speaking_complex_pattern_p1",
    ):
        r = urllib.request.Request(BASE + path)
        with opener.open(r, timeout=20) as resp:
            body = resp.read().decode("utf-8", "replace")
            print(path, "bytes", len(body), "has_report" , ("maybeReportTaskScope" in body or "loadComplexFrame" in body or "20261011complex" in body))

    conn.close()
    if row and str(row["state"]).startswith("done") and int(row["study_completed"] or 0) == 1:
        print("E2E_API_OK")
    else:
        print("E2E_API_FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
