#!/usr/bin/env python3
"""Deploy the IELTS practice platform to a Linux server.

The script intentionally reads all credentials from environment variables.
It backs up the existing remote deployment before replacing code files.
"""

from __future__ import annotations

import argparse
import os
import shlex
import sys
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Iterable

import paramiko


ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "sources"
SCRIPTS_DIR = ROOT / "scripts"
LOGO_SRC = ROOT / "logo.png"
DATA_DIR = ROOT / "data"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


SERVER_HOST = env("IELTS_DEPLOY_HOST")
SERVER_PORT = int(env("IELTS_DEPLOY_PORT", "22"))
SERVER_USER = env("IELTS_DEPLOY_USER", "root")
SERVER_PASSWORD = os.environ.get("IELTS_DEPLOY_PASSWORD")
SERVER_KEY = env("IELTS_DEPLOY_KEY")
DOMAIN = env("IELTS_DEPLOY_DOMAIN", "training.oyenglish.com.cn")
DEPLOY_DIR = env("IELTS_DEPLOY_DIR", "/var/www/ielts")
BACKUP_DIR = env("IELTS_BACKUP_DIR", "/root/ielts_backups")
SERVICE_PORT = int(env("IELTS_SERVICE_PORT", "49182"))
CERTBOT_EMAIL = env("IELTS_CERTBOT_EMAIL")


def log(message: str) -> None:
    print(f"[deploy] {message}", flush=True)


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def ensure_safe_remote_dir() -> None:
    if DEPLOY_DIR.startswith("/var/www/"):
        return
    if env("IELTS_DEPLOY_ALLOW_UNSAFE_DIR") == "1":
        return
    raise RuntimeError(
        "IELTS_DEPLOY_DIR must be under /var/www/ unless "
        "IELTS_DEPLOY_ALLOW_UNSAFE_DIR=1 is set."
    )


def run(ssh: paramiko.SSHClient, command: str, check: bool = True, timeout: int = 180) -> str:
    log(f"  $ {command}")
    _, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if out.strip():
        print(out.rstrip())
    if err.strip():
        print(err.rstrip(), file=sys.stderr)
    exit_code = stdout.channel.recv_exit_status()
    if check and exit_code != 0:
        raise RuntimeError(f"Remote command failed with exit {exit_code}: {command}")
    return out


def connect() -> paramiko.SSHClient:
    if not SERVER_HOST:
        raise RuntimeError("Missing IELTS_DEPLOY_HOST.")
    if not SERVER_PASSWORD and not SERVER_KEY:
        raise RuntimeError("Set IELTS_DEPLOY_PASSWORD or IELTS_DEPLOY_KEY before deploying.")

    log(f"Connecting to {SERVER_USER}@{SERVER_HOST}:{SERVER_PORT} ...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect_kwargs = {
        "hostname": SERVER_HOST,
        "port": SERVER_PORT,
        "username": SERVER_USER,
        "timeout": 30,
        "allow_agent": False,
        "look_for_keys": False,
    }
    if SERVER_KEY:
        connect_kwargs["key_filename"] = SERVER_KEY
    if SERVER_PASSWORD:
        connect_kwargs["password"] = SERVER_PASSWORD
    ssh.connect(**connect_kwargs)
    log("Connected")
    return ssh


def tar_filter(include_data: bool):
    excluded_prefixes = {
        "sources/_zips",
        "sources/_extract",
        ".git",
        ".agents",
        ".browser-ops",
        ".claude",
        ".nezha",
    }

    def _filter(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
        name = info.name.replace("\\", "/")
        if any(name == prefix or name.startswith(prefix + "/") for prefix in excluded_prefixes):
            return None
        if not include_data and (name == "data" or name.startswith("data/")):
            return None
        if Path(name).suffix.lower() in AUDIO_EXTENSIONS or "/audio/" in name:
            return None
        if "__pycache__" in name or name.endswith((".pyc", ".pyo", ".log")):
            return None
        return info

    return _filter


def add_existing(tar: tarfile.TarFile, paths: Iterable[tuple[Path, str]], include_data: bool) -> None:
    filter_func = tar_filter(include_data)
    for local_path, archive_name in paths:
        if local_path.exists():
            tar.add(str(local_path), arcname=archive_name, filter=filter_func)


def backup_remote(ssh: paramiko.SSHClient) -> str:
    log("Backing up current remote deployment...")
    deploy_path = PurePosixPath(DEPLOY_DIR)
    parent = str(deploy_path.parent)
    base = deploy_path.name
    command = (
        "set -eu; "
        f"if [ -d {shell_quote(DEPLOY_DIR)} ]; then "
        f"mkdir -p {shell_quote(BACKUP_DIR)}; "
        f"backup={shell_quote(BACKUP_DIR)}/ielts_$(date +%Y%m%d_%H%M%S).tar.gz; "
        f"tar -czf \"$backup\" -C {shell_quote(parent)} {shell_quote(base)}; "
        "echo \"$backup\"; "
        "else echo 'no-existing-deploy-dir'; fi"
    )
    result = run(ssh, command, timeout=600).strip().splitlines()
    backup_path = result[-1] if result else ""
    log(f"Remote backup: {backup_path}")
    return backup_path


def upload_files(ssh: paramiko.SSHClient, include_data: bool) -> None:
    log("Packing and uploading project files...")
    sftp = ssh.open_sftp()
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        with tarfile.open(tmp_path, "w:gz") as tar:
            add_existing(
                tar,
                [
                    (SOURCES_DIR, "sources"),
                    (SCRIPTS_DIR, "scripts"),
                    (LOGO_SRC, "logo.png"),
                    (DATA_DIR, "data"),
                ],
                include_data=include_data,
            )

        log(f"  Uploading {tmp_path.stat().st_size // 1024} KB ...")
        sftp.put(str(tmp_path), "/tmp/ielts_deploy.tar.gz")
    finally:
        tmp_path.unlink(missing_ok=True)
        sftp.close()

    run(ssh, f"mkdir -p {shell_quote(DEPLOY_DIR)}")
    cleanup_targets = f"{shell_quote(DEPLOY_DIR)}/scripts {shell_quote(DEPLOY_DIR)}/logo.png"
    if include_data:
        cleanup_targets += f" {shell_quote(DEPLOY_DIR)}/data"
    run(ssh, f"rm -rf {cleanup_targets}")
    run(ssh, f"tar -xzf /tmp/ielts_deploy.tar.gz -C {shell_quote(DEPLOY_DIR)} --overwrite", timeout=600)
    run(ssh, "rm -f /tmp/ielts_deploy.tar.gz")
    log("Upload complete")


def install_deps(ssh: paramiko.SSHClient) -> None:
    log("Installing system dependencies...")
    run(ssh, "apt-get update -qq", timeout=600)
    run(
        ssh,
        "apt-get install -y -qq nginx python3 python3-pip certbot python3-certbot-nginx ufw fail2ban",
        timeout=1200,
    )
    log("Dependencies installed")


def setup_systemd(ssh: paramiko.SSHClient) -> None:
    log("Configuring systemd service...")
    service = f"""[Unit]
Description=IELTS Practice Platform Python Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory={DEPLOY_DIR}
ExecStart=/usr/bin/python3 {DEPLOY_DIR}/scripts/local_server.py \\
    --host 127.0.0.1 \\
    --port {SERVICE_PORT} \\
    --static-dir {DEPLOY_DIR}/sources \\
    --db {DEPLOY_DIR}/data/ielts_local.db
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
    run(ssh, f"mkdir -p {shell_quote(DEPLOY_DIR)}/data")
    run(ssh, f"chown -R www-data:www-data {shell_quote(DEPLOY_DIR)}")

    sftp = ssh.open_sftp()
    try:
        with sftp.open("/etc/systemd/system/ielts.service", "w") as remote_file:
            remote_file.write(service)
    finally:
        sftp.close()

    run(ssh, "systemctl daemon-reload")
    run(ssh, "systemctl enable ielts")
    run(ssh, "systemctl restart ielts")
    time.sleep(2)
    run(ssh, "systemctl is-active ielts")
    log("systemd service ready")


def setup_nginx(ssh: paramiko.SSHClient) -> None:
    log("Configuring Nginx...")
    nginx_conf = f"""server {{
    listen 80;
    listen [::]:80;
    server_name {DOMAIN} www.{DOMAIN};

    location /.well-known/acme-challenge/ {{
        root /var/www/certbot;
    }}

    location / {{
        proxy_pass http://127.0.0.1:{SERVICE_PORT};
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }}
}}
"""
    sftp = ssh.open_sftp()
    try:
        with sftp.open("/etc/nginx/sites-available/ielts", "w") as remote_file:
            remote_file.write(nginx_conf)
    finally:
        sftp.close()

    run(ssh, "ln -sf /etc/nginx/sites-available/ielts /etc/nginx/sites-enabled/ielts", check=False)
    run(ssh, "rm -f /etc/nginx/sites-enabled/default", check=False)
    run(ssh, "nginx -t")
    run(ssh, "systemctl restart nginx")
    log("Nginx ready")


def setup_https(ssh: paramiko.SSHClient) -> None:
    if not CERTBOT_EMAIL:
        log("Skipping HTTPS setup because IELTS_CERTBOT_EMAIL is not set.")
        return
    log("Requesting or renewing Let's Encrypt certificate...")
    run(ssh, "mkdir -p /var/www/certbot")
    result = run(
        ssh,
        f"certbot --nginx -d {shell_quote(DOMAIN)} --non-interactive --agree-tos "
        f"--email {shell_quote(CERTBOT_EMAIL)} --redirect 2>&1 || true",
        check=False,
        timeout=600,
    )
    if any(marker in result for marker in ("Congratulations", "Certificate not yet due", "Successfully")):
        log("HTTPS is configured")
    else:
        log("HTTPS setup did not report success. Check DNS and certbot logs if needed.")
    run(ssh, "systemctl is-enabled certbot.timer 2>/dev/null || true", check=False)


def setup_firewall(ssh: paramiko.SSHClient) -> None:
    log("Configuring firewall...")
    run(ssh, "ufw default deny incoming")
    run(ssh, "ufw default allow outgoing")
    run(ssh, "ufw allow 22/tcp comment 'SSH'")
    run(ssh, "ufw allow 80/tcp comment 'HTTP'")
    run(ssh, "ufw allow 443/tcp comment 'HTTPS'")
    run(ssh, "ufw --force enable")
    run(ssh, "ufw status")
    log("Firewall ready")


def verify_deployment(ssh: paramiko.SSHClient) -> None:
    log("Running remote verification...")
    run(ssh, f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{SERVICE_PORT}/api/health")
    run(ssh, f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{SERVICE_PORT}/tinglidanciceshi/")
    run(ssh, "systemctl is-active ielts nginx")
    log("Remote verification complete")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy IELTS practice platform")
    parser.add_argument(
        "--provision",
        action="store_true",
        help="Install packages and configure Nginx/HTTPS/firewall",
    )
    parser.add_argument(
        "--include-data",
        action="store_true",
        help="Upload local data directory and replace remote data",
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip remote backup")
    parser.add_argument("--skip-nginx", action="store_true", help="Do not rewrite Nginx config")
    parser.add_argument("--skip-systemd", action="store_true", help="Do not rewrite or restart systemd service")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ensure_safe_remote_dir()

    ssh = connect()
    try:
        if args.provision:
            install_deps(ssh)
        if not args.no_backup:
            backup_remote(ssh)
        upload_files(ssh, include_data=args.include_data)
        if not args.skip_systemd:
            setup_systemd(ssh)
        if args.provision and not args.skip_nginx:
            setup_nginx(ssh)
            setup_https(ssh)
            setup_firewall(ssh)
        elif not args.skip_nginx:
            setup_nginx(ssh)
            setup_https(ssh)
        verify_deployment(ssh)
        print("\n" + "=" * 60)
        print("Deployment complete")
        print(f"Site: https://{DOMAIN}/tinglidanciceshi/")
        print(f"Teacher: https://{DOMAIN}/tinglidanciceshi/?role=teacher")
        print("=" * 60)
        return 0
    finally:
        ssh.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
