#!/usr/bin/env python3
"""备份线上数据库到本地 backups/aliyun_YYYYMMDD_HHMMSS/。

发布清单第 1 步。deploy.py 的整站 tar 备份不能替代本步。

策略（加速日常上线）
------------------
1. 判断要不要重拉主库 ielts_local.db：
   - 默认：若「今天」已有完整可用备份（完整性 ok + SHA256），则复用，不重拉 ~200MB；
   - 若本次改动触及后端/库相关路径，或指定 --fresh-main / --force，则强制重拉。
2. 真要拉主库（及其他较大 .db）时：服务器先 SQLite 快照，再 gzip 后下载，本机解压。
3. 写作库等小文件始终拉取（体积小，成本可忽略）。

用法
----
  python scripts/backup_remote_db.py
  python scripts/backup_remote_db.py --fresh-main
  python scripts/backup_remote_db.py --force
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import os
import shlex
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUPS = ROOT / "backups"

# 触及这些路径时，默认强制重拉主库（避免复用过期快照）
DB_RISK_PREFIXES = (
    "scripts/local_server.py",
    "scripts/teacher_api.py",
    "scripts/task_api.py",
    "scripts/session_auth.py",
    "scripts/password_utils.py",
    "scripts/jianya_api.py",
    "scripts/luboke_api.py",
    "scripts/vocab/",
    "scripts/wrong_items",
    "sources/xiezuopigai/ielts-writing-backend/",
)

# 主库大于该阈值才走 gzip（字节）
COMPRESS_MIN_BYTES = 8 * 1024 * 1024
# 「小库」始终拉取的上限
ALWAYS_PULL_MAX_BYTES = 5 * 1024 * 1024


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


def remote_exec(ssh, command: str, timeout: int = 300) -> tuple[str, str, int]:
    _, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    code = stdout.channel.recv_exit_status()
    return out, err, code


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
    out, err, _ = remote_exec(ssh, command, timeout=300)
    if "snapshot-ok" in out:
        print(f"    {out.strip()}")
        return True
    print(f"    快照输出: {out.strip()} {err.strip()}")
    return False


def remote_gzip(ssh, source: str, dest_gz: str) -> bool:
    """gzip -1 优先速度；失败返回 False。"""
    cmd = (
        f"rm -f {shlex.quote(dest_gz)}; "
        f"gzip -1 -c {shlex.quote(source)} > {shlex.quote(dest_gz)} && "
        f"echo gzip-ok $(stat -c%s {shlex.quote(dest_gz)})"
    )
    out, err, code = remote_exec(ssh, cmd, timeout=600)
    if code == 0 and "gzip-ok" in out:
        print(f"    {out.strip()}")
        return True
    print(f"    gzip 失败: {out.strip()} {err.strip()}")
    return False


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def db_integrity_ok(path: Path) -> bool:
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
            return integrity == "ok"
        finally:
            conn.close()
    except Exception:  # noqa: BLE001
        return False


def summarize_main_db(path: Path) -> str:
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            tables = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            parts = []
            for t in ("students", "activity_events", "daily_tasks", "plan_items"):
                if t in tables:
                    n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    parts.append(f"{t}={n}")
            return ", ".join(parts) or "（无业务表）"
        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001
        return f"读表失败: {exc}"


def today_prefix() -> str:
    return datetime.now().strftime("%Y%m%d")


def find_today_main_backup() -> Path | None:
    """返回今天最新一份带可用 ielts_local.db 的备份目录。"""
    prefix = f"aliyun_{today_prefix()}"
    if not BACKUPS.exists():
        return None
    dirs = sorted(
        [p for p in BACKUPS.iterdir() if p.is_dir() and p.name.startswith(prefix)],
        key=lambda p: p.name,
        reverse=True,
    )
    for d in dirs:
        main = d / "ielts_local.db"
        if not main.exists() or main.stat().st_size < 1024 * 1024:
            continue
        if db_integrity_ok(main):
            return d
    return None


def git_changed_paths() -> list[str]:
    """相对 origin/main（或 HEAD）的变更路径，失败则返回空（保守不强制）。"""
    cmds = [
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "diff", "--name-only", "--cached"],
    ]
    paths: set[str] = set()
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        except Exception:  # noqa: BLE001
            continue
        for line in out.splitlines():
            line = line.strip().replace("\\", "/")
            if line:
                paths.add(line)
    return sorted(paths)


def changes_need_fresh_main(paths: list[str]) -> bool:
    for p in paths:
        for prefix in DB_RISK_PREFIXES:
            if p == prefix or p.startswith(prefix):
                return True
        # 其他 scripts 下业务 py（排除备份/部署/一次性探查）
        if p.startswith("scripts/") and p.endswith(".py"):
            name = Path(p).name
            if name.startswith("_"):
                continue
            if name in ("deploy.py", "backup_remote_db.py"):
                continue
            if "api" in name or name in (
                "local_server.py",
                "session_auth.py",
                "password_utils.py",
            ):
                return True
    return False


def pull_db(
    ssh,
    sftp,
    remote_path: str,
    size: int,
    dest_dir: Path,
    stamp: str,
    *,
    use_gzip: bool,
) -> tuple[str, str]:
    """下载一个远程 db，返回 (文件名, sha256)。"""
    name = Path(remote_path).name
    local = dest_dir / name
    snap = f"/tmp/ielts_db_snapshot_{stamp}_{name}"
    print(f"  快照 {remote_path} ({size / 1024 / 1024:.2f} MB)")
    snapshot_ok = remote_sqlite_backup(ssh, remote_path, snap)
    source = snap if snapshot_ok else remote_path
    if not snapshot_ok:
        print("    在线快照失败，改为直接拉取热文件")

    try:
        if use_gzip and size >= COMPRESS_MIN_BYTES:
            gz_remote = f"{source}.gz"
            print("    压缩传输 (gzip -1) ...")
            if remote_gzip(ssh, source, gz_remote):
                gz_local = dest_dir / f"{name}.gz"
                sftp.get(gz_remote, str(gz_local))
                remote_exec(ssh, f"rm -f {shlex.quote(gz_remote)}", timeout=30)
                print(f"    下载压缩包 {gz_local.stat().st_size / 1024 / 1024:.2f} MB，解压中...")
                with gzip.open(gz_local, "rb") as src, open(local, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                gz_local.unlink(missing_ok=True)
            else:
                print("    压缩失败，回退明文下载")
                sftp.get(source, str(local))
        else:
            sftp.get(source, str(local))
    finally:
        if snapshot_ok:
            remote_exec(ssh, f"rm -f {shlex.quote(snap)}", timeout=30)

    digest = sha256_file(local)
    print(f"    sha256 {digest[:16]}...  本地 {local.stat().st_size} 字节")
    return name, digest


def list_remote_dbs(ssh, base: str) -> list[tuple[str, int]]:
    data_dir = f"{base.rstrip('/')}/data"
    writing_db = (
        f"{base.rstrip('/')}/sources/xiezuopigai/ielts-writing-backend/ielts_data.db"
    )
    cmd = (
        f"for f in {data_dir}/*.db {shlex.quote(writing_db)}; do "
        f'[ -f "$f" ] && echo "$f $(stat -c%s "$f")"; '
        f"done"
    )
    out, _, _ = remote_exec(ssh, cmd, timeout=60)
    rows: list[tuple[str, int]] = []
    for ln in out.splitlines():
        ln = ln.strip()
        if not ln or " " not in ln:
            continue
        path, size_s = ln.rsplit(" ", 1)
        try:
            rows.append((path, int(size_s)))
        except ValueError:
            continue
    # 去重（同名保留更大/先出现）
    seen: dict[str, tuple[str, int]] = {}
    for path, size in rows:
        name = Path(path).name
        if name not in seen:
            seen[name] = (path, size)
    return list(seen.values())


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="备份线上 SQLite 到本地 backups/aliyun_*")
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重拉全部库（忽略当日复用）",
    )
    parser.add_argument(
        "--fresh-main",
        action="store_true",
        help="强制重拉主库 ielts_local.db（小库仍按常规则）",
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="下载时不 gzip（调试用）",
    )
    args = parser.parse_args()

    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts") or "/var/www/ielts"
    changed = git_changed_paths()
    risk = changes_need_fresh_main(changed)
    fresh_main = bool(args.force or args.fresh_main or risk)

    print("变更路径数:", len(changed))
    if changed:
        preview = ", ".join(changed[:12])
        more = "" if len(changed) <= 12 else f" …(+{len(changed) - 12})"
        print(f"  {preview}{more}")
    print(
        "主库策略:",
        "强制重拉" if fresh_main else "可复用当日备份",
        f"(force={args.force}, fresh-main={args.fresh_main}, db-risk={risk})",
    )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUPS / f"aliyun_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    print(f"备份目录: {dest}")

    reused_from: Path | None = None
    if not fresh_main:
        reused_from = find_today_main_backup()
        if reused_from:
            print(f"复用今日主库备份: {reused_from.name}/ielts_local.db")
        else:
            print("今日无可用主库备份，将重拉主库")
            fresh_main = True

    ssh = connect_ssh()
    sums: list[str] = []
    try:
        remote_dbs = list_remote_dbs(ssh, base)
        if not remote_dbs:
            raise SystemExit(f"服务器 {base}/data 下没有 .db 文件")

        sftp = ssh.open_sftp()
        try:
            for remote_path, size in remote_dbs:
                name = Path(remote_path).name
                is_main = name == "ielts_local.db"

                if is_main and reused_from and not fresh_main:
                    src = reused_from / "ielts_local.db"
                    local = dest / "ielts_local.db"
                    shutil.copy2(src, local)
                    digest = sha256_file(local)
                    sums.append(f"{digest}  {name}")
                    print(
                        f"  {name}: 复用 {reused_from.name} "
                        f"({local.stat().st_size / 1024 / 1024:.2f} MB) "
                        f"sha256 {digest[:16]}..."
                    )
                    print(f"    {summarize_main_db(local)}")
                    # 顺带复制当日 SHA 备注
                    note = dest / "REUSED_FROM.txt"
                    note.write_text(
                        f"ielts_local.db reused from {reused_from}\n"
                        f"reason: same-day backup + no db-risk paths\n",
                        encoding="utf-8",
                    )
                    continue

                # 小库始终拉；大库按策略拉
                if (not is_main) and size > ALWAYS_PULL_MAX_BYTES and not args.force:
                    # 非主库但很大：仍拉（少见）
                    pass

                name, digest = pull_db(
                    ssh,
                    sftp,
                    remote_path,
                    size,
                    dest,
                    stamp,
                    use_gzip=not args.no_compress,
                )
                sums.append(f"{digest}  {name}")
                local = dest / name
                if not db_integrity_ok(local):
                    print(f"  {name}: 完整性失败")
                    raise SystemExit(1)
                if name == "ielts_local.db":
                    print(f"  {name}: 完整性 ok，{summarize_main_db(local)}")
                else:
                    print(f"  {name}: 完整性 ok")
        finally:
            sftp.close()

        if not (dest / "ielts_local.db").exists():
            raise SystemExit("备份结果缺少 ielts_local.db")

        (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
        print(f"\n已写入 {dest / 'SHA256SUMS'}")
        print("第 1 步完成。")
        print(f"BACKUP_DIR={dest.as_posix()}")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
