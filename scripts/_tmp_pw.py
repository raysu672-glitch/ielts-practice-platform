import sqlite3
import sys

sys.path.insert(0, "scripts")
from password_utils import verify_password  # noqa: E402

c = sqlite3.connect("data/_stage_test_demo.db")
c.row_factory = sqlite3.Row
for r in c.execute("SELECT * FROM teachers"):
    ok = verify_password("123456", r["password"])
    print(r["teacher_id"], "| password==123456:", ok, "| changed:", r["is_password_changed"])
