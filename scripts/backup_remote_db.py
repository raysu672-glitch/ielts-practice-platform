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
import shlex
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


def remote_sqlite_backup(ssh, source: str, dest: str) -> bool:
    """Ask the server to write a consistent SQLite snapshot. Returns False on failure."""
    code = (
        "import os,sqlite3,sys;"
        "p=sys.argv[2];"
        "os.path.exists(p) and os.remove(p);"
        "src=sqlite3.connect(sys.argv[1], timeout=120);"
        "dst=sqlite3.connect(p);"
        "src.backup(dst); dst.close(); src.close();"
        "print('snapshot-ok', os.path.getsize(p))"
    )
    command = f"python3 -c {shlex.quote(code)} {shlex.quote(source)} {shlex.quote(dest)}"
    _, stdout, stderr = ssh.exec_command(command, timeout=300)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    if "snapshot-ok" in out:
        print(f"    {out.strip()}")
        return True
    print(f"    快照输出: {out.strip()} {err.strip()}")
    return False


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
                snapshot = f"/tmp/ielts_db_snapshot_{stamp}_{name}"
                # 线上库一直在写。直接 sftp 热文件会抄到写了一半的页，恢复时校验失败。
                # 用 SQLite 在线备份先落一份一致的快照，再下载那份。
                print(f"  快照 {remote_path} ({int(size) / 1024 / 1024:.2f} MB)")
                snapshot_ok = remote_sqlite_backup(ssh, remote_path, snapshot)
                local = dest / name
                source = snapshot if snapshot_ok else remote_path
                if not snapshot_ok:
                    print("    在线快照失败，改为直接拉取热文件")
                sftp.get(source, str(local))
                if snapshot_ok:
                    ssh.exec_command(f"rm -f {snapshot}", timeout=30)
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
                integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
                tables = [r[0] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                counts = []
                for t in ("students", "activity_events", "daily_tasks", "plan_items"):
                    if t in tables:
                        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                        counts.append(f"{t}={n}")
                conn.close()
                detail = ", ".join(counts) or "（无业务表）"
                if integrity != "ok":
                    print(f"  {name}: 完整性失败 {integrity}；{detail}")
                    raise SystemExit(1)
                print(f"  {name}: 完整性 ok，{detail}")
            except Exception as exc:  # noqa: BLE001
                print(f"  {name}: 校验失败 {exc}")

        (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
        print(f"\n已写入 {dest / 'SHA256SUMS'}")
        print("第 1 步完成。")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
