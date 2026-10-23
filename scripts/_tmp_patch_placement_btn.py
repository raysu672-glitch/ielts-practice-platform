# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "sources/tinglidanciceshi/index.html"
t = p.read_text(encoding="utf-8")
needle = 'onclick="showChangePasswordModal()">'
idx = t.find(needle)
if idx < 0:
    raise SystemExit("button not found")
# find closing </button> after this onclick
end = t.find("</button>", idx)
if end < 0:
    raise SystemExit("close not found")
insert_at = end + len("</button>")
btn = '<button class="btn btn-secondary btn-sm" onclick="openPlacementTest()">入学摸底</button>'
if "openPlacementTest()" in t:
    print("already patched")
else:
    t = t[:insert_at] + btn + t[insert_at:]
    p.write_text(t, encoding="utf-8")
    print("patched at", insert_at)
