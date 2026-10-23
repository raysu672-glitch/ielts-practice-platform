# -*- coding: utf-8 -*-
"""Sync only sources/jianyazhenti/exam-data/**/keys/*.json to Aliyun.

Does NOT run full deploy.py (avoids uploading unrelated WIP sources).
exam-data is gitignored; this is the intended hot-sync path for answer keys.
"""
from __future__ import annotations

import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ai_config import load_env_file  # noqa: E402

LOCAL_EXAM = ROOT / "sources" / "jianyazhenti" / "exam-data"


def env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def connect_ssh():
    import paramiko

    host = env("IELTS_DEPLOY_HOST")
    if not host:
        raise SystemExit("未设置 IELTS_DEPLOY_HOST")
    key = env("IELTS_DEPLOY_KEY")
    password = os.environ.get("IELTS_DEPLOY_PASSWORD")
    if not key and not password:
        raise SystemExit("需要 IELTS_DEPLOY_KEY 或 IELTS_DEPLOY_PASSWORD")

    print(
        f"Connecting {env('IELTS_DEPLOY_USER', 'root')}@{host}:{env('IELTS_DEPLOY_PORT', '22')} ...",
        flush=True,
    )
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kwargs = {
        "hostname": host,
        "port": int(env("IELTS_DEPLOY_PORT", "22") or "22"),
        "username": env("IELTS_DEPLOY_USER", "root") or "root",
        "timeout": 45,
        "banner_timeout": 45,
        "auth_timeout": 45,
        "allow_agent": False,
        "look_for_keys": False,
    }
    if key:
        key_path = Path(key)
        if not key_path.is_file():
            raise SystemExit(f"SSH key not found: {key}")
        kwargs["key_filename"] = str(key_path)
    else:
        kwargs["password"] = password
    ssh.connect(**kwargs)
    print("Connected", flush=True)
    return ssh


def backup_dbs(ssh) -> Path:
    import sqlite3

    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts").rstrip("/")
    data_dir = f"{base}/data"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = ROOT / "backups" / f"aliyun_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Backup dir: {dest}")

    _, stdout, _ = ssh.exec_command(
        f"for f in {data_dir}/*.db; do [ -f \"$f\" ] && echo \"$f $(stat -c%s \"$f\")\"; done",
        timeout=60,
    )
    listing = [ln for ln in stdout.read().decode("utf-8", "replace").splitlines() if ln.strip()]
    if not listing:
        raise SystemExit(f"No .db under {data_dir}")

    sftp = ssh.open_sftp()
    sums = []
    try:
        for line in listing:
            remote_path, size = line.rsplit(" ", 1)
            name = Path(remote_path).name
            local = dest / name
            print(f"  pull {remote_path} ({int(size)/1024/1024:.2f} MB)")
            sftp.get(remote_path, str(local))
            digest = hashlib.sha256(local.read_bytes()).hexdigest()
            sums.append(f"{digest}  {name}")
            # quick sanity
            conn = sqlite3.connect(str(local))
            try:
                n = conn.execute(
                    "SELECT count(*) FROM sqlite_master WHERE type='table'"
                ).fetchone()[0]
            finally:
                conn.close()
            print(f"    sha256={digest[:16]}... tables={n}")
    finally:
        sftp.close()
    (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(f"DB backup OK -> {dest}")
    return dest


def ensure_remote_dir(sftp, remote_dir: str) -> None:
    parts = PurePosixPath(remote_dir).parts
    cur = ""
    for part in parts:
        if part == "/":
            cur = "/"
            continue
        cur = f"{cur.rstrip('/')}/{part}"
        try:
            sftp.stat(cur)
        except OSError:
            sftp.mkdir(cur)


def sync_keys(ssh) -> int:
    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts").rstrip("/")
    remote_exam = f"{base}/sources/jianyazhenti/exam-data"
    files = sorted(LOCAL_EXAM.glob("academic*/keys/*/*.json"))
    if not files:
        raise SystemExit(f"No local key files under {LOCAL_EXAM}")

    # Prefetch remote dirs with one mkdir -p
    dirs = sorted({str(PurePosixPath(remote_exam) / f.relative_to(LOCAL_EXAM).parent) for f in files})
    mkdir_cmd = "mkdir -p " + " ".join(f"'{d}'" for d in dirs)
    print(f"Ensuring {len(dirs)} remote key dirs ...", flush=True)
    _, stdout, stderr = ssh.exec_command(mkdir_cmd, timeout=60)
    if stdout.channel.recv_exit_status() != 0:
        raise RuntimeError(stderr.read().decode("utf-8", "replace"))

    sftp = ssh.open_sftp()
    uploaded = 0
    try:
        for local in files:
            rel = local.relative_to(LOCAL_EXAM).as_posix()
            remote = f"{remote_exam}/{rel}"
            sftp.put(str(local), remote)
            uploaded += 1
            if uploaded % 50 == 0 or uploaded == len(files):
                print(f"  uploaded {uploaded}/{len(files)}", flush=True)
        _, stdout, _ = ssh.exec_command(
            f"chmod -R a+rX {remote_exam}/*/keys; "
            f"chown -R www-data:www-data {remote_exam}/*/keys 2>/dev/null || true",
            timeout=120,
        )
        stdout.channel.recv_exit_status()
    finally:
        sftp.close()
    print(f"Uploaded {uploaded} key JSON files to {remote_exam}/**/keys/", flush=True)
    return uploaded


def verify_sample(ssh) -> None:
    """Spot-check a few fixed answers on the remote filesystem."""
    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts").rstrip("/")
    checks = [
        (
            f"{base}/sources/jianyazhenti/exam-data/academic16/keys/listening/655.json",
            '"1": "park"',
        ),
        (
            f"{base}/sources/jianyazhenti/exam-data/academic16/keys/listening/658.json",
            '"40": "sheep"',
        ),
        (
            f"{base}/sources/jianyazhenti/exam-data/academic10/keys/reading/787.json",
            '"2": "viii"',
        ),
        (
            f"{base}/sources/jianyazhenti/exam-data/academic4/keys/reading/1444.json",
            '"40": "B"',
        ),
    ]
    for path, needle in checks:
        cmd = f"python3 -c \"import pathlib; t=pathlib.Path({path!r}).read_text(encoding='utf-8'); print('OK' if {needle!r} in t else 'MISS'); print('garbage' if 'ieltszone' in t.lower() or 'elementor' in t.lower() else 'clean')\""
        _, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        out = stdout.read().decode("utf-8", "replace").strip()
        err = stderr.read().decode("utf-8", "replace").strip()
        print(f"  verify {Path(path).name}: {out or err}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    load_env_file(ROOT / ".env.deploy", override=True)
    ssh = connect_ssh()
    try:
        backup_dbs(ssh)
        sync_keys(ssh)
        print("Spot-checking remote keys ...")
        verify_sample(ssh)
        print("DONE: keys-only sync")
        return 0
    finally:
        ssh.close()


if __name__ == "__main__":
    raise SystemExit(main())
