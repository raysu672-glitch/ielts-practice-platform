import os
import re
import sys
import time
import base64
import tempfile
import shutil
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 腾讯云 SDK
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

# 让后端能找到当前目录的 ffmpeg.exe（完整版）
APP_DIR = Path(__file__).resolve().parent
os.environ["PATH"] = str(APP_DIR) + os.pathsep + os.environ.get("PATH", "")

app = FastAPI(title="P4 Shadow Reading Backend - Tencent ASR")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 腾讯云配置 ====================
TENCENT_SECRET_ID = os.environ.get("TENCENT_SECRET_ID", "")
TENCENT_SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "")
TENCENT_REGION = os.environ.get("TENCENT_REGION", "ap-shanghai")

if not TENCENT_SECRET_ID or not TENCENT_SECRET_KEY:
    print("警告：未设置 TENCENT_SECRET_ID / TENCENT_SECRET_KEY，/transcribe 接口将无法调用")
    _cred = None
else:
    _cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)

_http_profile = HttpProfile(reqTimeout=60)
_client_profile = ClientProfile(httpProfile=_http_profile)

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


def get_asr_client():
    if _cred is None:
        raise RuntimeError("腾讯云密钥未配置，请先设置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY 环境变量")
    return asr_client.AsrClient(_cred, TENCENT_REGION, _client_profile)


def compress_audio(input_path: Path, output_path: Path):
    """如果音频超过 5MB，压缩成 mp3（16k mono，64k）"""
    ffmpeg_cmd = shutil.which("ffmpeg")
    if not ffmpeg_cmd:
        raise RuntimeError("找不到 ffmpeg.exe")
    import subprocess
    subprocess.run(
        [
            ffmpeg_cmd, "-y", "-nostdin", "-i", str(input_path),
            "-ar", "16000", "-ac", "1", "-b:a", "64k", str(output_path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def submit_asr_task(audio_bytes: bytes) -> int:
    client = get_asr_client()
    req = models.CreateRecTaskRequest()
    req.EngineModelType = "16k_en"
    req.ChannelNum = 1
    req.ResTextFormat = 0
    req.SourceType = 1
    req.Data = base64.b64encode(audio_bytes).decode("utf-8")
    req.DataLen = len(audio_bytes)

    resp = client.CreateRecTask(req)
    return resp.Data.TaskId


def poll_asr_result(task_id: int, timeout: int = 300) -> str:
    client = get_asr_client()
    start = time.time()
    while time.time() - start < timeout:
        req = models.DescribeTaskStatusRequest()
        req.TaskId = task_id
        resp = client.DescribeTaskStatus(req)
        status = resp.Data.Status

        if status == 2:  # success
            return resp.Data.Result or ""
        elif status == 3:  # failed
            raise RuntimeError(f"腾讯云识别失败：{resp.Data.ErrorMsg}")

        time.sleep(2)

    raise TimeoutError("等待腾讯云识别结果超时")


def clean_asr_result(raw: str) -> str:
    """去掉时间戳标记，如 [0:0.020,0:2.380]"""
    cleaned = re.sub(r"\[\d+:\d+\.\d+,\d+:\d+\.\d+\]\s*", "", raw)
    cleaned = cleaned.replace("\n", " ")
    return cleaned.strip()


# ==================== API ====================
@app.get("/")
def root():
    return {"message": "P4 Shadow Reading Backend (Tencent ASR) is running"}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    start = time.time()

    suffix = Path(file.filename or "recording.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        content = await file.read()
        tmp_in.write(content)
        input_path = Path(tmp_in.name)

    try:
        # 腾讯云 Data 字段限制 5MB，先检查，超限就压缩
        audio_bytes = input_path.read_bytes()
        if len(audio_bytes) > 5 * 1024 * 1024:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
                mp3_path = Path(tmp_mp3.name)
            compress_audio(input_path, mp3_path)
            audio_bytes = mp3_path.read_bytes()

        if len(audio_bytes) > 5 * 1024 * 1024:
            raise ValueError("音频文件超过 5MB，无法通过腾讯云 ASR 直接上传")

        # 提交任务并轮询结果
        task_id = submit_asr_task(audio_bytes)
        raw_result = poll_asr_result(task_id)
        recognized_text = clean_asr_result(raw_result)

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

    except TencentCloudSDKException as e:
        return JSONResponse({"error": f"腾讯云 SDK 错误：{e}"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": f"处理失败：{str(e)}"}, status_code=500)

    finally:
        for p in (input_path, mp3_path if 'mp3_path' in locals() else None):
            try:
                if p and p.exists():
                    os.unlink(p)
            except Exception:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
