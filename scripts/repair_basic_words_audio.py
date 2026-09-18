#!/usr/bin/env python3
"""修复「听力基础词汇」音频内容与词形不符的问题。

背景
----
词表（listening_basic.html / modules.js）曾被一次 `l` -> `i` 的字体/编码问题污染，
例如 land -> iand、lanes -> ianes、laptops -> iaptops、legroom -> iegroom。
这些词条的 mp3 是**按拼错的词**生成的，后来 `fix_listening_basic_typos.py`
只做了「改词表 + 重命名 mp3 文件」，**没有重新生成音频内容**，
于是 land.mp3 里念的仍然是 "iand"（听起来像 "End"），学生自然觉得读音不对。

判据
----
audio/basic_words/_manifest.json 记录的是「用哪些词条生成过音频」。
若某个词的**当前拼写**不在 manifest 里，说明对应 mp3 的音频内容并非按当前词形
生成（而是从旧名重命名来的），需要重做。

用法
----
  # 1) 只列出可疑词，不写任何文件（默认）
  python scripts/repair_basic_words_audio.py

  # 2) 本地重新生成音频
  python scripts/repair_basic_words_audio.py --generate

  # 3) 本地生成 + 上传到服务器（替换 mp3 并合并 _manifest.json）
  python scripts/repair_basic_words_audio.py --generate --upload

上传所需的服务器信息沿用 scripts/deploy.py 的环境变量：
IELTS_DEPLOY_HOST / IELTS_DEPLOY_PORT / IELTS_DEPLOY_USER /
IELTS_DEPLOY_KEY 或 IELTS_DEPLOY_PASSWORD / IELTS_DEPLOY_DIR
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTENING_BASIC = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"
AUDIO_DIR = ROOT / "sources" / "tinglidanciceshi" / "audio" / "basic_words"
MANIFEST_NAME = "_manifest.json"

# 与 scripts/gen_tts_words.py 完全一致，保证音色/语速与其它音频统一
VOICE = "en-GB-SoniaNeural"
RATE = "+0%"
VOLUME = "+0%"


def load_all_words() -> list[str]:
    html = LISTENING_BASIC.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[[\s\S]*?\]);", html)
    if not m:
        raise SystemExit("listening_basic.html 里找不到 ALL_WORDS")
    return [w["word"] for w in json.loads(m.group(1))]


def deploy_env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def connect_ssh():
    import paramiko

    host = deploy_env("IELTS_DEPLOY_HOST")
    if not host:
        raise SystemExit("未设置 IELTS_DEPLOY_HOST，无法访问服务器。")
    key = deploy_env("IELTS_DEPLOY_KEY")
    password = os.environ.get("IELTS_DEPLOY_PASSWORD")
    if not key and not password:
        raise SystemExit("需要 IELTS_DEPLOY_KEY 或 IELTS_DEPLOY_PASSWORD。")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kwargs = {
        "hostname": host,
        "port": int(deploy_env("IELTS_DEPLOY_PORT", "22") or "22"),
        "username": deploy_env("IELTS_DEPLOY_USER", "root") or "root",
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


def remote_audio_dir() -> str:
    base = deploy_env("IELTS_DEPLOY_DIR", "/var/www/ielts") or "/var/www/ielts"
    return f"{base.rstrip('/')}/sources/tinglidanciceshi/audio/basic_words"


def fetch_manifest_from_server() -> list[str]:
    ssh = connect_ssh()
    sftp = ssh.open_sftp()
    try:
        with sftp.open(f"{remote_audio_dir()}/{MANIFEST_NAME}", "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
    finally:
        sftp.close()
        ssh.close()
    return data


def load_manifest(from_server: bool, out_dir: Path | None = None) -> list[str]:
    if from_server:
        return fetch_manifest_from_server()
    path = (out_dir or AUDIO_DIR) / MANIFEST_NAME
    if not path.is_file():
        raise SystemExit(
            f"本地找不到 {path}。\n"
            "可以先用 --manifest-from-server 从服务器读取，或直接加 --upload 让脚本自动拉取。"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def find_suspects(words: list[str], manifest: list[str]) -> list[str]:
    """当前拼写不在 manifest 里 => 音频内容不是按当前词形生成的。"""
    done = set(manifest)
    return [w for w in words if w not in done]


async def _generate_one(word: str, out_dir: Path, sem: asyncio.Semaphore) -> bool:
    import edge_tts

    out = out_dir / f"{word}.mp3"
    async with sem:
        for attempt in range(3):
            try:
                await edge_tts.Communicate(word, VOICE, rate=RATE, volume=VOLUME).save(str(out))
                return True
            except Exception as exc:  # noqa: BLE001 - 网络抖动，重试
                if attempt == 2:
                    print(f"  生成失败 [{word}]: {exc}", flush=True)
                    return False
                await asyncio.sleep(1.5 * (attempt + 1))
    return False


def generate(words: list[str], out_dir: Path, force: bool) -> list[str]:
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        raise SystemExit("未安装 edge-tts。请先执行：pip install edge-tts") from None

    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [w for w in words if force or not (out_dir / f"{w}.mp3").is_file()]
    if not todo:
        print(f"本地已有全部 {len(words)} 个音频，无需生成（如需强制重做请加 --force）。")
        return []

    async def runner() -> None:
        sem = asyncio.Semaphore(6)
        await asyncio.gather(*[_generate_one(w, out_dir, sem) for w in todo])

    print(f"开始生成 {len(todo)} 个音频 -> {out_dir}")
    asyncio.run(runner())
    ok = [w for w in todo if (out_dir / f"{w}.mp3").is_file()]
    print(f"生成完成：{len(ok)}/{len(todo)}")
    return ok


def upload(words: list[str], manifest: list[str], out_dir: Path) -> None:
    ssh = connect_ssh()
    sftp = ssh.open_sftp()
    remote = remote_audio_dir()
    try:
        print(f"上传 {len(words)} 个 mp3 -> {remote}")
        sent = 0
        for w in words:
            local = out_dir / f"{w}.mp3"
            if not local.is_file():
                print(f"  跳过（本地缺文件）: {w}")
                continue
            sftp.put(str(local), f"{remote}/{w}.mp3")
            sent += 1
        print(f"已上传 {sent} 个。")

        merged = sorted(set(manifest) | set(words))
        tmp = out_dir / MANIFEST_NAME
        tmp.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(merged, ensure_ascii=False, indent=1)
        tmp.write_text(payload, encoding="utf-8")
        with sftp.open(f"{remote}/{MANIFEST_NAME}", "wb") as f:
            f.write(payload.encode("utf-8"))
        print(f"已更新服务器 {MANIFEST_NAME}（{len(merged)} 条）。")
    finally:
        sftp.close()
        ssh.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="修复听力基础词汇音频内容与词形不符的问题")
    parser.add_argument("--generate", action="store_true", help="本地重新生成可疑词的音频")
    parser.add_argument("--force", action="store_true", help="配合 --generate：即使已存在也重做")
    parser.add_argument("--upload", action="store_true", help="上传音频到服务器并合并 manifest")
    parser.add_argument("--manifest-from-server", action="store_true",
                        help="从服务器读取 _manifest.json 作为判据")
    parser.add_argument("--out-dir", default="", help=f"音频输出目录（默认 {AUDIO_DIR}）")
    parser.add_argument("--list-file", default="", help="把可疑词清单写入该文件")
    parser.add_argument("--include-from", default="",
                        help="只处理该文件里列出的词（每行一个），用于定向修复")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else AUDIO_DIR

    words = load_all_words()
    print(f"词表：{LISTENING_BASIC.name} 共 {len(words)} 词")

    from_server = args.manifest_from_server or args.upload
    manifest = load_manifest(from_server, out_dir)
    print(f"manifest：{len(manifest)} 条（来源：{'服务器' if from_server else '本地'}）")

    if args.include_from:
        wanted = [ln.strip() for ln in Path(args.include_from).read_text(encoding="utf-8").splitlines()]
        wanted = [w for w in wanted if w]
        known = set(words)
        missing = [w for w in wanted if w not in known]
        if missing:
            print(f"注意：以下词不在当前词表里，已忽略：{missing}")
        wanted_set = set(wanted) & known
        suspects = [w for w in words if w in wanted_set]
        print(f"\n定向修复：指定 {len(wanted)} 个，匹配到词表内 {len(suspects)} 个。")
    else:
        suspects = find_suspects(words, manifest)
        print(f"\n可疑词 {len(suspects)} 个（当前拼写不在 manifest 里，音频内容可能仍是旧拼写）：")
    for i, w in enumerate(suspects, 1):
        print(f"  {i:3d}. {w}")
    if not suspects:
        print("  无。")

    if args.list_file:
        Path(args.list_file).write_text(
            "\n".join(f"{i}. {w}" for i, w in enumerate(suspects, 1)) + "\n", encoding="utf-8")
        print(f"\n清单已写入 {args.list_file}")

    if not (args.generate or args.upload):
        print("\n（仅列出，未做任何修改。加 --generate 生成，加 --upload 上传。）")
        return

    generated = generate(suspects, out_dir, args.force) if args.generate else []
    if args.upload:
        to_upload = generated or [w for w in suspects if (out_dir / f"{w}.mp3").is_file()]
        if not to_upload:
            print("没有可上传的音频。")
            return
        if not args.generate and len(to_upload) != len(suspects):
            print(f"注意：本地只找到 {len(to_upload)}/{len(suspects)} 个音频文件。")
        upload(to_upload, manifest, out_dir)


if __name__ == "__main__":
    main()
