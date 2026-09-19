#!/usr/bin/env python3
"""把「听力基础词汇」音频整体发布到服务器。

背景
----
`sources/tinglidanciceshi/audio/basic_words/` 里的音频不进 git（体积大），
`scripts/deploy.py` 的默认部署也会刻意跳过音频目录。所以要单独发布。

历史教训
--------
早期用 `rename_basic_words_audio_server.sh` 只**改文件名**不重新生成内容，
导致 land.mp3 里念的还是拼错的 "iand"；还有几批音频用了 `-10%` 慢速，
与后来统一的 `+0%` 混在一起，学生听到同组内语速忽快忽慢。
所以发布前务必确认本地音频是**用当前词表 + 统一参数**重新生成的。

用法
----
  python scripts/upload_basic_words_audio.py                # 打包上传并校验
  python scripts/upload_basic_words_audio.py --dry-run      # 只打包，不上传

服务器信息沿用 scripts/deploy.py 的环境变量：
  IELTS_DEPLOY_HOST / IELTS_DEPLOY_PORT / IELTS_DEPLOY_USER /
  IELTS_DEPLOY_PASSWORD 或 IELTS_DEPLOY_KEY / IELTS_DEPLOY_DIR
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "sources" / "tinglidanciceshi" / "audio" / "basic_words"
HTML = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"
MANIFEST = "_manifest.json"

# 因词形修正/重命名而遗留的孤儿音频，发布时顺手删掉
ORPHANS = ["graduate.mp3", "painting.mp3"]


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


def remote_dir() -> str:
    base = env("IELTS_DEPLOY_DIR", "/var/www/ielts") or "/var/www/ielts"
    return f"{base.rstrip('/')}/sources/tinglidanciceshi/audio/basic_words"


def local_words() -> list[str]:
    html = io.open(HTML, encoding="utf-8").read()
    return [w["word"] for w in json.loads(
        re.search(r"const ALL_WORDS = (\[[\s\S]*?\]);", html).group(1))]


def build_archive(out: Path, words: list[str]) -> tuple[int, list[str]]:
    """把词表对应的 mp3 + manifest 打成一个 tar.gz。"""
    missing = [w for w in words if not (AUDIO_DIR / f"{w}.mp3").is_file()]
    with tarfile.open(out, "w:gz") as tar:
        for w in words:
            f = AUDIO_DIR / f"{w}.mp3"
            if f.is_file():
                tar.add(str(f), arcname=f"{w}.mp3")
        # manifest 重写为当前词表，避免累积已废弃的旧名
        man = AUDIO_DIR / MANIFEST
        man.write_text(json.dumps(sorted(words), ensure_ascii=False, indent=1), encoding="utf-8")
        tar.add(str(man), arcname=MANIFEST)
    return len(words) - len(missing), missing


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="发布听力基础词汇音频到服务器")
    ap.add_argument("--dry-run", action="store_true", help="只打包，不上传")
    args = ap.parse_args()

    words = local_words()
    print(f"当前词表 {len(words)} 个词；本地音频目录 {AUDIO_DIR}")

    tmp = ROOT / "_tmp_basic_words_audio.tar.gz"
    n_ok, missing = build_archive(tmp, words)
    size_mb = tmp.stat().st_size / 1024 / 1024
    print(f"打包完成：{n_ok} 个 mp3，{size_mb:.1f} MB -> {tmp.name}")
    if missing:
        print(f"⚠️ 本地缺 {len(missing)} 个音频，请先跑：python scripts/gen_tts_words.py --basic --force")
        print("   " + ", ".join(missing[:12]))
        raise SystemExit(1)

    if args.dry_run:
        print("（--dry-run，未上传）")
        return

    ssh = connect_ssh()
    sftp = ssh.open_sftp()
    remote = remote_dir()
    remote_tar = f"/tmp/{tmp.name}"
    try:
        print(f"上传 -> {remote_tar}")
        sftp.put(str(tmp), remote_tar)

        cmd = " && ".join([
            f"mkdir -p '{remote}'",
            f"tar -xzf '{remote_tar}' -C '{remote}'",
            f"rm -f '{remote_tar}'",
            " && ".join(f"rm -f '{remote}/{o}'" for o in ORPHANS),
            f"ls '{remote}'/*.mp3 | wc -l",
        ])
        _, stdout, stderr = ssh.exec_command(cmd, timeout=600)
        out = stdout.read().decode("utf-8", "replace").strip()
        err = stderr.read().decode("utf-8", "replace").strip()
        if err:
            print("stderr:", err[-500:])
        print(f"服务器音频目录现有 mp3 数量：{out}")
    finally:
        sftp.close()
        ssh.close()
        try:
            tmp.unlink()
        except OSError:
            pass
    print("发布完成。")


if __name__ == "__main__":
    main()
