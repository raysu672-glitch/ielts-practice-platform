import os
import re
import sys
import tempfile
import time
import shutil
from pathlib import Path

# 加载本地 whisper / torch 等依赖（安装到了 C:\w\p）
sys.path.insert(0, r'C:\w\p')

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper

# 让后端能找到当前目录的 ffmpeg.exe（完整版）
APP_DIR = Path(__file__).resolve().parent
os.environ["PATH"] = str(APP_DIR) + os.pathsep + os.environ.get("PATH", "")

app = FastAPI(title="P4 Shadow Reading Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 原文数据 ====================
ORIGINAL_TEXT = (
    "Good day, ladies and gentlemen. I have been asked today to talk to you about the urban landscape. "
    "There are two major areas that I will focus on in my talk: how vegetation can have a significant effect on urban climate, "
    "and how we can better plan our cities using trees to provide a more comfortable environment for us to live in. "
    "Trees can have a significant impact on our cities. They can make a city, as a whole, a bit less windy or a bit more windy, "
    "if that's what you want. They can make it a bit cooler if it's a hot summer day in an Australian city, "
    "or they can make it a bit more humid if it's a dry inland city. "
    "On the local scale - that is, in particular areas within the city - trees can make the local area more shady, "
    "cooler, more humid and much less windy. In fact trees and planting of various kinds can be used to make city streets "
    "actually less dangerous in particular areas. How do trees do all that, you ask? "
    "Well, the main difference between a tree and a building is a tree has got an internal mechanism to keep the temperature regulated. "
    "It evaporates water through its leaves and that means that the temperature of the leaves is never very far from our own body temperature. "
    "The temperature of a building surface on a hot sunny day can easily be twenty degrees more than our temperature. "
    "Trees, on the other hand, remain cooler than buildings because they sweat. "
    "This means that they can humidify the air and cool it - a property which can be exploited to improve the local climate. "
    "Trees can also help break the force of winds. The reason that high buildings make it windier at ground level is that, "
    "as the wind goes higher and higher, it goes faster and faster. When the wind hits the building, it has to go somewhere. "
    "Some of it goes over the top and some goes around the sides of the building, forcing those high level winds down to ground level. "
    "That doesn't happen when you have trees. Trees filter the wind and considerably reduce it, "
    "preventing those very large strong gusts that you so often find around tall buildings. "
    "Another problem in built-up areas is that traffic noise is intensified by tall buildings. "
    "By planting a belt of trees at the side of the road, you can make things a little quieter, "
    "but much of the vehicle noise still goes through the trees. "
    "Trees can also help reduce the amount of noise in the surroundings, although the effect is not as large as people like to think. "
    "Low-frequency noise, in particular, just goes through the trees as though they aren't there. "
    "Although trees can significantly improve the local climate, they do however take up a lot of space. "
    "There are root systems to consider and branches blocking windows and so on. "
    "It may therefore be difficult to fit trees into the local landscape. "
    "There is not a great deal you can do if you have what we call a street canyon - a whole set of high-rises enclosed in a narrow street. "
    "Trees need water to grow. They also need some sunlight to grow and you need room to put them. "
    "If you have the chance of knocking buildings down and replacing them, then suddenly you can start looking at different ways to design the streets and to introduce."
)


def normalize_text(text: str) -> str:
    return re.sub(r"[.,!?;:'\"()\-]", "", text.lower())


def tokenize(text: str) -> list:
    return [w for w in normalize_text(text).split() if w]


def lcs_length(a: list, b: list) -> int:
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# ==================== 加载 Whisper 模型 ====================
MODEL_PATH = APP_DIR / "models" / "small.en.pb"
print(f"Loading Whisper model from {MODEL_PATH} ...")
_model = whisper.load_model(str(MODEL_PATH))
print("Whisper model loaded.")


@app.get("/")
def root():
    return {"message": "P4 Shadow Reading Backend is running"}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    start = time.time()

    # 保存上传文件
    suffix = Path(file.filename or "recording.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        content = await file.read()
        tmp_in.write(content)
        input_path = tmp_in.name

    try:
        # Whisper 可以直接读取 webm/opus，但为了稳定先转成 wav
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            wav_path = tmp_wav.name

        ffmpeg_cmd = shutil.which("ffmpeg")
        if not ffmpeg_cmd:
            raise RuntimeError("ffmpeg not found in PATH")

        import subprocess
        subprocess.run(
            [
                ffmpeg_cmd, "-y", "-nostdin", "-i", input_path,
                "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Whisper 识别
        result = _model.transcribe(wav_path, language="en", task="transcribe")
        recognized_text = result.get("text", "").strip()

        # LCS 算分
        orig_words = tokenize(ORIGINAL_TEXT)
        rec_words = tokenize(recognized_text)
        matched = lcs_length(orig_words, rec_words)
        total = len(orig_words)
        score = round(matched / total * 100, 1) if total > 0 else 0.0

        return JSONResponse(
            {
                "score": score,
                "matched": matched,
                "total": total,
                "recognizedText": recognized_text,
                "elapsedSeconds": round(time.time() - start, 1),
            }
        )

    finally:
        for p in (input_path, wav_path):
            try:
                os.unlink(p)
            except Exception:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
