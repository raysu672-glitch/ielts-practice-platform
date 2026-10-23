#!/usr/bin/env python3
"""Step 1: backup production DBs before deploy."""
from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

import paramiko

ROOT = Path(__file__).resolve().parents[1]
HOST = "47.103.199.114"
USER = "root"
REMOTE_DIR = "/var/www/ielts/data"
PEM = next(Path(r"D:\Download").glob("*.pem"))


def main() -> None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = ROOT / "backups" / f"aliyun_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    print(f"DIR={dest} PEM={PEM}", flush=True)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, key_filename=str(PEM), timeout=30)
    sftp = ssh.open_sftp()
    try:
        names = [n for n in sftp.listdir(REMOTE_DIR) if n.endswith(".db")]
        if not names:
            raise SystemExit(f"no .db under {REMOTE_DIR}")
        for name in sorted(names):
            local = dest / name
            print(f"get {name} ...", flush=True)
            sftp.get(f"{REMOTE_DIR}/{name}", str(local))
            print(f"  -> {local.stat().st_size} bytes", flush=True)
    finally:
        sftp.close()
        ssh.close()

    lines = []
    for db in sorted(dest.glob("*.db")):
        h = hashlib.sha256(db.read_bytes()).hexdigest()
        lines.append(f"{h}  {db.name}")
        print(db.name, h)
    (dest / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK backup={dest}")


if __name__ == "__main__":
    main()
