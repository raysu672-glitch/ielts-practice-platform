# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ai_config import load_env_file  # noqa: E402


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    load_env_file(ROOT / ".env.deploy", override=True)
    import paramiko

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=os.environ["IELTS_DEPLOY_HOST"],
        port=int(os.environ.get("IELTS_DEPLOY_PORT") or 22),
        username=os.environ.get("IELTS_DEPLOY_USER") or "root",
        key_filename=os.environ["IELTS_DEPLOY_KEY"],
        timeout=30,
        allow_agent=False,
        look_for_keys=False,
    )
    base = (os.environ.get("IELTS_DEPLOY_DIR") or "/var/www/ielts").rstrip("/")
    checks = [
        ("academic16/keys/listening/655.json", {"1": "park", "10": "199"}),
        ("academic16/keys/listening/658.json", {"34": "economic", "40": "sheep"}),
        ("academic10/keys/reading/787.json", {"2": "viii"}),
        ("academic4/keys/reading/1444.json", {"40": "B"}),
    ]
    sftp = ssh.open_sftp()
    try:
        for rel, expect in checks:
            path = f"{base}/sources/jianyazhenti/exam-data/{rel}"
            with sftp.open(path, "r") as f:
                data = json.loads(f.read().decode("utf-8"))
            ans = data.get("answers") or {}
            junk = any(
                x in str(ans).lower()
                for x in ("ieltszone", "elementor", "simplyielts", "wp-content")
            )
            ok = all(ans.get(k) == v for k, v in expect.items())
            print(f"SSH {rel}: ok={ok} junk={junk} got={ {k: ans.get(k) for k in expect} }")
    finally:
        sftp.close()
        ssh.close()

    domain = os.environ.get("IELTS_DEPLOY_DOMAIN") or "training.oyenglish.com.cn"
    for rel, expect in checks:
        url = f"https://{domain}/exam-data/{rel}"
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                data = json.loads(r.read().decode("utf-8"))
            ans = data.get("answers") or {}
            junk = any(
                x in str(ans).lower()
                for x in ("ieltszone", "elementor", "simplyielts", "wp-content")
            )
            ok = all(ans.get(k) == v for k, v in expect.items())
            print(f"HTTP {rel}: ok={ok} junk={junk} got={ {k: ans.get(k) for k in expect} }")
        except Exception as exc:
            print(f"HTTP {rel}: FAIL {exc}")

    # health
    with urllib.request.urlopen(f"https://{domain}/api/health", timeout=20) as r:
        print("health", r.read().decode()[:200])


if __name__ == "__main__":
    main()
