#!/usr/bin/env python3
"""备份线上数据库到本地 backups/aliyun_YYYYMMDD_HHMMSS/。

发布清单第 1 步。deploy.py 的整站 tar 备份不能替代本步（它把 DB 一起打进
tar，回滚粒度太粗；这里单独留存可直接替换回去的 .db 文件 + SHA256 校验）。

用法
----
  python scripts/backup_remote_db.py
"""
from __future__ import annotations

import hashlib
import io
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUPS = ROOT / "backups"


def env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def connect_ssh():
    import paramiko

    host = env("IELTS_DEPLOY_HOST")
    if not host:
        raise SystemExit("未设置 IELTS_DEPLOY_HOST。")
    key = env("IELTS_DEPLOY_KEY")
    password = os.environ.get("IELTS_DEPLOY_PASSWORD")
    if not key and not password:
        raise SystemExit("需要 IELTS_DEPLOY_KEY 或 IELTS_DEPLOY_PASSWORD。")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kwargs = {
        "hostname": host,
        "port": int(env("IELTS_DEPLOY_PORT", "22") or "22"),
        "username": env("IELTS_DEPLOY_USER", "root") or "root",
        "timeout": 30,
        "allow_agent": False,
        "look_for_keys": False,
    }
    if key:
        kwargs["key_filename"] = key
    else:
        kwargs["password"] = password
    ssh.connect(**kwargs)
    return ssh


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts") or "/var/www/ielts"
    data_dir = f"{base.rstrip('/')}/data"

    ssh = connect_ssh()
    try:
        _, stdout, _ = ssh.exec_command(
            f"ls -1 {data_dir}/*.db 2>/dev/null; echo '---'; "
            f"for f in {data_dir}/*.db; do [ -f \"$f\" ] && echo \"$f $(stat -c%s \"$f\")\"; done",
            timeout=60,
        )
        out = stdout.read().decode("utf-8", "replace").strip()
        listing = [ln for ln in out.splitlines() if ln and ln != "---" and " " in ln]
        if not listing:
            print(f"服务器 {data_dir} 下没有 .db 文件")
            return

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = BACKUPS / f"aliyun_{stamp}"
        dest.mkdir(parents=True, exist_ok=True)
        print(f"备份目录: {dest}")

        sftp = ssh.open_sftp()
        sums: list[str] = []
        try:
            for line in listing:
                remote_path, size = line.rsplit(" ", 1)
                name = Path(remote_path).name
                local = dest / name
                print(f"  拉取 {remote_path} ({int(size) / 1024 / 1024:.2f} MB)")
                sftp.get(remote_path, str(local))
                digest = hashlib.sha256(local.read_bytes()).hexdigest()
                sums.append(f"{digest}  {name}")
                print(f"    sha256 {digest[:16]}...  本地 {local.stat().st_size} 字节")
        finally:
            sftp.close()

        # 行数概览，便于确认备份内容可用
        import sqlite3

        for line in listing:
            name = Path(line.rsplit(" ", 1)[0]).name
            db = dest / name
            try:
                conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
                tables = [r[0] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                counts = []
                for t in ("students", "activity_events", "daily_tasks", "plan_items"):
                    if t in tables:
                        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                        counts.append(f"{t}={n}")
                conn.close()
                print(f"  {name}: 完整性 ok，{', '.join(counts) or '（无业务表）'}")
            except Exception as exc:  # noqa: BLE001
                print(f"  {name}: 校验失败 {exc}")

        (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
        print(f"\n已写入 {dest / 'SHA256SUMS'}")
        print("第 1 步完成。")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
