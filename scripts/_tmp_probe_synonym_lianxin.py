#!/usr/bin/env python3
import sqlite3
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
c = sqlite3.connect(r"file:backups/aliyun_20261019_155050/ielts_local.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
SH = ZoneInfo("Asia/Shanghai")
rows = c.execute(
    """
    SELECT created_at, action, summary, detail_json
    FROM activity_events
    WHERE actor_id='2025114' AND created_at>='2026-10-14T16:00:00.000Z'
      AND created_at<'2026-10-15T16:00:00.000Z'
      AND (action LIKE '%synonym%' OR module_type='reading_synonym')
    ORDER BY created_at
    """
).fetchall()
print("count", len(rows))
prev = None
for r in rows:
    dt = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")).astimezone(SH)
    gap = ""
    if prev:
        gap = f" +{(dt-prev).total_seconds():.1f}s"
    print(dt.strftime("%H:%M:%S"), r["action"], gap, (r["summary"] or "")[:40])
    prev = dt
