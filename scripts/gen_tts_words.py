"""
批量生成雅思听力1000词的 TTS 音频文件
使用 edge-tts，声音：en-GB-SoniaNeural（英式英语，适合雅思初级学习）
输出目录：sources/tinglidanciceshi/audio/words/
"""
import asyncio
import json
import re
import sys
import os
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("ERROR: edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

# 配置
VOICE = "en-GB-SoniaNeural"   # 英式英语，女声，清晰适合雅思初学者
RATE = "-10%"                  # 稍慢一点，适合初级学习者
VOLUME = "+0%"

BASE_DIR = Path(__file__).parent.parent
HTML_FILE = BASE_DIR / "sources" / "tinglidanciceshi" / "listening.html"
OUT_DIR = BASE_DIR / "sources" / "tinglidanciceshi" / "audio" / "words"
MANIFEST_FILE = OUT_DIR / "_manifest.json"

def extract_words(html_path: Path) -> list[str]:
    """从 listening.html 提取 ALL_WORDS 词汇表"""
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"const ALL_WORDS = (\[.*?\]);", text, re.DOTALL)
    if not m:
        raise ValueError("ALL_WORDS not found in listening.html")
    words_data = json.loads(m.group(1))
    return [w["word"] for w in words_data]


async def generate_one(word: str, out_path: Path, semaphore: asyncio.Semaphore) -> bool:
    """生成单个单词的 MP3，返回是否成功"""
    async with semaphore:
        try:
            communicate = edge_tts.Communicate(word, VOICE, rate=RATE, volume=VOLUME)
            await communicate.save(str(out_path))
            return True
        except Exception as e:
            print(f"  FAIL [{word}]: {e}", flush=True)
            return False


async def main():
    # 提取词汇
    print(f"Reading words from: {HTML_FILE}")
    words = extract_words(HTML_FILE)
    print(f"Total words: {len(words)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 读取已有 manifest，跳过已完成的
    if MANIFEST_FILE.exists():
        done = set(json.loads(MANIFEST_FILE.read_text(encoding="utf-8")))
    else:
        done = set()

    pending = [(w, OUT_DIR / f"{w}.mp3") for w in words if w not in done]
    print(f"Already done: {len(done)}, Pending: {len(pending)}")

    if not pending:
        print("All words already generated!")
        return

    # 并发生成，限制并发数避免被限流
    semaphore = asyncio.Semaphore(8)
    total = len(pending)
    success = 0

    tasks = []
    for word, path in pending:
        tasks.append((word, asyncio.create_task(generate_one(word, path, semaphore))))

    for i, (word, task) in enumerate(tasks):
        ok = await task
        if ok:
            done.add(word)
            success += 1
        # 每 50 个保存一次 manifest
        if (i + 1) % 50 == 0:
            MANIFEST_FILE.write_text(json.dumps(sorted(done)), encoding="utf-8")
            print(f"  Progress: {i+1}/{total} ({success} OK)", flush=True)

    # 最终保存
    MANIFEST_FILE.write_text(json.dumps(sorted(done)), encoding="utf-8")
    print(f"\nDone: {success}/{total} succeeded")
    print(f"Output: {OUT_DIR}")
    if total - success > 0:
        print(f"Failed: {total - success} words. Re-run script to retry.")


if __name__ == "__main__":
    asyncio.run(main())
