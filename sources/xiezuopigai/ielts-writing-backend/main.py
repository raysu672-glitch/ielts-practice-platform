"""
IELTS Writing Grammar API (Python/FastAPI)
AI-powered grammar supplement service
"""

import json
import logging
import os
import re
import sqlite3
import traceback
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
# 仓库根目录：.../sources/xiezuopigai/ielts-writing-backend -> ../../..
_PROJECT_ROOT = os.path.abspath(os.path.join(_BACKEND_DIR, "..", "..", ".."))
# 平台统一 AI 配置优先；模块本地 .env 仅作兼容回退
load_dotenv(os.path.join(_PROJECT_ROOT, "config", "ai.env"), override=False)
load_dotenv(os.path.join(_BACKEND_DIR, ".env"), override=False)
load_dotenv(override=False)  # 兼容进程环境 / systemd EnvironmentFile

logger = logging.getLogger("ielts-backend")

# ===== 数据库 =====
DB_PATH = os.path.join(_BACKEND_DIR, "ielts_data.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS practice_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_id TEXT DEFAULT '',
            essay TEXT NOT NULL,
            checkpoints TEXT NOT NULL,
            total_stats TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("PRAGMA table_info(practice_records)")
    cols = {row[1] for row in c.fetchall()}
    migrations = {
        "student_id": "ALTER TABLE practice_records ADD COLUMN student_id TEXT DEFAULT ''",
        "teacher_revision": "ALTER TABLE practice_records ADD COLUMN teacher_revision TEXT DEFAULT ''",
        "teacher_comment": "ALTER TABLE practice_records ADD COLUMN teacher_comment TEXT DEFAULT ''",
        "teacher_updated_at": "ALTER TABLE practice_records ADD COLUMN teacher_updated_at TIMESTAMP",
        "student_feedback_seen_at": "ALTER TABLE practice_records ADD COLUMN student_feedback_seen_at TIMESTAMP",
        "topic": "ALTER TABLE practice_records ADD COLUMN topic TEXT DEFAULT ''",
    }
    for col, sql in migrations.items():
        if col not in cols:
            c.execute(sql)
    conn.commit()
    conn.close()
    logger.info("数据库初始化完成: %s", DB_PATH)


init_db()

# ===== 配置 =====
PORT = int(os.getenv("PORT", "8080"))
# 前端 HTML 默认在 backend 目录的上一级，可用环境变量覆盖
FRONTEND_HTML = os.getenv(
    "FRONTEND_HTML",
    os.path.join(_BACKEND_DIR, "..", "ielts-student-practice.html"),
)
# 优先 AI_*（DeepSeek），兼容旧 SILICONFLOW_* 变量名
SILICONFLOW_API_KEY = os.getenv("AI_API_KEY") or os.getenv("SILICONFLOW_API_KEY", "")
SILICONFLOW_BASE_URL = (
    os.getenv("AI_BASE_URL")
    or os.getenv("SILICONFLOW_BASE_URL")
    or "https://api.deepseek.com"
)
SILICONFLOW_MODEL = (
    os.getenv("AI_MODEL")
    or os.getenv("SILICONFLOW_MODEL")
    or "deepseek-v4-flash"
)

# ===== AI 检测参数 =====
# deepseek-v4-flash 默认会开 thinking；若不关闭，reasoning 会占满 max_tokens，导致 content 为空
MAX_TOKENS_DEFAULT = int(os.getenv("AI_MAX_TOKENS", "4000"))
MAX_TOKENS_RETRY = int(os.getenv("AI_MAX_TOKENS_RETRY", "6000"))
MAX_ERRORS_REQUESTED = int(os.getenv("AI_MAX_ERRORS", "14"))
MAX_ERRORS_RETRY = int(os.getenv("AI_MAX_ERRORS_RETRY", "10"))
AI_THINKING = (os.getenv("AI_THINKING", "disabled") or "disabled").strip().lower()
AI_CHUNK_CHARS = int(os.getenv("AI_CHUNK_CHARS", "900"))
# 语法+词汇错误 ≤ 该值则本题结束（次数不设上限）
WRITING_PASS_ERROR_MAX = max(0, int(os.getenv("WRITING_PASS_ERROR_MAX", "3")))


def normalize_topic_key(topic: str) -> str:
    """题目规范化 key：去首尾空白并折叠中间空白，用于同题聚合。"""
    return re.sub(r"\s+", " ", (topic or "").strip()).lower()


def is_teacher_reviewed(revision: str, comment: str) -> bool:
    return bool(str(revision or "").strip() or str(comment or "").strip())


def count_grammar_vocab_errors(checkpoints) -> int:
    """统计语法/词汇类检查点数量（本产品检查点均为语法或词汇错误）。"""
    if checkpoints is None:
        return 0
    if isinstance(checkpoints, str):
        try:
            checkpoints = json.loads(checkpoints)
        except Exception:
            return 0
    if not isinstance(checkpoints, list):
        return 0
    return len(checkpoints)


def is_topic_completed_by_errors(error_count: int) -> bool:
    return int(error_count or 0) <= WRITING_PASS_ERROR_MAX


def split_sentences(text: str) -> List[str]:
    """按句号等断句，但保留小数点、省略号和常见缩写中的点号。"""
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if not text:
        return []

    protected: List[str] = []

    def stash(match: re.Match) -> str:
        protected.append(match.group(0))
        return f"§§{len(protected) - 1}§§"

    work = text
    work = re.sub(r"(?<=\d)\.(?=\d)", stash, work)
    work = re.sub(r"\.{2,}", stash, work)
    work = re.sub(
        r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|approx|fig|eq|No|Vol|pp)\.",
        stash,
        work,
        flags=re.I,
    )
    work = re.sub(r"\b(?:e\.g|i\.e)\.", stash, work, flags=re.I)

    parts = re.findall(r"[^.!?。！？]+[.!?。！？]?", work)
    sentences: List[str] = []
    for part in parts:
        restored = part.strip()
        if not restored:
            continue
        restored = re.sub(
            r"§§(\d+)§§",
            lambda m: protected[int(m.group(1))],
            restored,
        )
        sentences.append(restored)

    return sentences or [text]


# ===== 数据模型 =====
class ExistingError(BaseModel):
    sentenceIndex: int
    matchedText: str
    ruleId: Optional[str] = None


class GrammarCheckRequest(BaseModel):
    essay: str
    existingErrors: List[ExistingError] = []


class AiError(BaseModel):
    originalSentence: str = ""
    matchedText: str = ""
    category: str = "语法错误"
    question: str = "请找出并修正这处错误"
    hints: List[str] = []
    explanation: str = ""
    corrected: str = ""
    # 兼容旧格式：如果 AI 仍返回 sentenceIndex，后端会优先用 originalSentence 对齐
    sentenceIndex: Optional[int] = None

    @classmethod
    def from_ai_dict(cls, err: dict) -> Optional["AiError"]:
        if not isinstance(err, dict):
            return None
        hints = err.get("hints") or []
        if isinstance(hints, str):
            hints = [hints] if hints.strip() else []
        elif not isinstance(hints, list):
            hints = [str(hints)]
        hints = [str(h) for h in hints if h is not None and str(h).strip()]
        matched = str(err.get("matchedText") or "").strip()
        original = str(err.get("originalSentence") or "").strip()
        if not matched and not original:
            return None
        try:
            return cls(
                originalSentence=original or matched,
                matchedText=matched or original,
                category=str(err.get("category") or "语法错误"),
                question=str(err.get("question") or "请找出并修正这处错误"),
                hints=hints or ["留意语法形式是否正确"],
                explanation=str(err.get("explanation") or ""),
                corrected=str(err.get("corrected") or original or matched),
                sentenceIndex=err.get("sentenceIndex"),
            )
        except Exception:
            return None


class GrammarCheckResponse(BaseModel):
    success: bool
    data: List[dict]
    meta: dict


# ===== 服务层 =====
class SiliconFlowClient:
    """OpenAI 兼容 API 封装（默认 DeepSeek）"""

    def __init__(self):
        self.api_key = SILICONFLOW_API_KEY
        self.base_url = SILICONFLOW_BASE_URL.rstrip("/")
        self.model = SILICONFLOW_MODEL
        self.client = httpx.AsyncClient(timeout=300.0)

    def build_prompt(
        self, essay: str, existing_positions: List[dict], max_errors: int = MAX_ERRORS_REQUESTED
    ) -> str:
        return f"""你是严格的 IELTS 写作语法批改老师。请仔细检查下面整段作文，尽可能找出真实语法错误。
重点：拼写、大小写、名词单复数、动词形式/时态、主谓一致、冠词、介词、搭配、句子结构。
不要放过明显错误；不要只检查开头；不要改写整篇风格；不要把正确表达当错误。
注意：文中的小数（如 50.1）不是句号。

作文：
{essay}

已检测（跳过这些片段，不要重复报）：
{existing_positions}

只返回 JSON：
{{
  "errors": [
    {{
      "originalSentence": "必须从作文中原样复制的完整原句",
      "matchedText": "出错片段（尽量短）",
      "category": "拼写错误/大小写错误/名词单复数/动词形式/主谓一致/冠词使用/搭配错误/句子结构",
      "question": "简短引导问句",
      "hints": ["一句短提示"],
      "explanation": "不超过40字说明",
      "corrected": "修正后完整句子"
    }}
  ]
}}

规则：最多 {max_errors} 个；originalSentence 必须能在作文中找到；explanation 不超过40字；hints 只要1条；不要重复；can not / whereas / From my perspective 正确勿报；确实没有错误才返回 {{"errors": []}}。
"""

    async def check_grammar(
        self, essay: str, existing_errors: List[ExistingError]
    ) -> tuple:
        """返回 (errors, failed, message)。长文按句分块检测，避免只覆盖开头。"""
        if not self.api_key or self.api_key in (
            "your_siliconflow_api_key_here",
            "your_deepseek_api_key_here",
        ):
            return [], True, "未配置 AI API Key"

        sentences = split_sentences(essay)
        chunks: List[str] = []
        buf: List[str] = []
        buf_len = 0
        for sent in sentences:
            extra = len(sent) + (1 if buf else 0)
            if buf and buf_len + extra > AI_CHUNK_CHARS:
                chunks.append(" ".join(buf))
                buf = [sent]
                buf_len = len(sent)
            else:
                buf.append(sent)
                buf_len += extra
        if buf:
            chunks.append(" ".join(buf))
        if not chunks:
            chunks = [essay]

        existing_positions = [
            {"sentenceIndex": e.sentenceIndex, "text": e.matchedText}
            for e in existing_errors
        ]
        seen_keys = {
            (e.matchedText or "").strip().lower()
            for e in existing_errors
            if (e.matchedText or "").strip()
        }

        all_errors: List[AiError] = []
        any_success = False
        last_fail_message = ""

        for chunk_idx, chunk in enumerate(chunks):
            chunk_existing = [
                pos
                for pos in existing_positions
                if (pos.get("text") or "") and str(pos.get("text")).lower() in chunk.lower()
            ]
            # 已检出片段也传给后续块，减少重复
            for err in all_errors:
                if err.matchedText:
                    chunk_existing.append(
                        {"sentenceIndex": -1, "text": err.matchedText}
                    )

            per_chunk_max = MAX_ERRORS_REQUESTED
            result = await self._call_ai(
                chunk,
                chunk_existing,
                max_tokens=MAX_TOKENS_DEFAULT,
                max_errors=per_chunk_max,
            )
            if result is None:
                logger.warning(
                    "分块 AI 检测失败，重试中 chunk=%s/%s ...",
                    chunk_idx + 1,
                    len(chunks),
                )
                result = await self._call_ai(
                    chunk,
                    chunk_existing,
                    max_tokens=MAX_TOKENS_RETRY,
                    max_errors=MAX_ERRORS_RETRY,
                )
            if result is None:
                last_fail_message = "AI 分析超时或返回异常，请稍后重试"
                continue

            any_success = True
            for err in result:
                key = (err.matchedText or "").strip().lower()
                if key and key in seen_keys:
                    continue
                if key:
                    seen_keys.add(key)
                all_errors.append(err)

        if not any_success:
            return [], True, last_fail_message or "AI 分析超时或返回异常，请稍后重试"

        logger.info(
            "AI 分块检测完成: chunks=%s errors=%s",
            len(chunks),
            len(all_errors),
        )
        return all_errors, False, ""

    def _parse_ai_content(self, content: str) -> List[AiError]:
        """解析 AI JSON；若被截断则尽量抢救已完整的错误对象。"""
        try:
            result = json.loads(content)
            errors = result.get("errors", []) if isinstance(result, dict) else []
            parsed = []
            for err in errors:
                item = AiError.from_ai_dict(err) if isinstance(err, dict) else None
                if item:
                    parsed.append(item)
            return parsed
        except json.JSONDecodeError:
            pass

        # 抢救截断 JSON：提取 errors 数组里已经完整的对象
        salvaged = []
        start = content.find('"errors"')
        if start < 0:
            raise json.JSONDecodeError("缺少 errors 字段", content, 0)

        bracket = content.find("[", start)
        if bracket < 0:
            raise json.JSONDecodeError("缺少 errors 数组", content, 0)

        i = bracket + 1
        while i < len(content):
            while i < len(content) and content[i] in " \n\r\t,":
                i += 1
            if i >= len(content) or content[i] == "]":
                break
            if content[i] != "{":
                break
            depth = 0
            in_str = False
            escape = False
            j = i
            while j < len(content):
                ch = content[j]
                if in_str:
                    if escape:
                        escape = False
                    elif ch == "\\":
                        escape = True
                    elif ch == '"':
                        in_str = False
                else:
                    if ch == '"':
                        in_str = True
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            try:
                                obj = json.loads(content[i : j + 1])
                                item = AiError.from_ai_dict(obj) if isinstance(obj, dict) else None
                                if item:
                                    salvaged.append(item)
                            except Exception:
                                pass
                            i = j + 1
                            break
                j += 1
            else:
                break

        if not salvaged:
            raise json.JSONDecodeError("无法从截断内容抢救错误", content, 0)

        logger.warning("JSON 被截断，已抢救 %s 个完整错误", len(salvaged))
        return salvaged

    async def _call_ai(
        self,
        essay: str,
        existing_positions: List[dict],
        max_tokens: int,
        max_errors: int,
    ) -> Optional[List[AiError]]:
        """单次 AI 调用。成功返回错误列表，失败返回 None（供上层重试）。"""
        prompt = self.build_prompt(essay, existing_positions, max_errors=max_errors)

        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是 IELTS 语法纠错助手。只返回完整 JSON，字段尽量简短，不要输出 markdown。",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": max_tokens,
                "response_format": {"type": "json_object"},
            }
            # DeepSeek V4：默认 thinking 会吃掉输出额度，导致 content 为空
            if AI_THINKING in ("0", "false", "off", "disabled", "no"):
                payload["thinking"] = {"type": "disabled"}
            elif AI_THINKING in ("1", "true", "on", "enabled", "yes"):
                payload["thinking"] = {"type": "enabled"}

            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            choice = (data.get("choices") or [{}])[0]
            message = choice.get("message") or {}
            content = (message.get("content") or "").strip()
            finish_reason = choice.get("finish_reason")
            usage = data.get("usage") or {}
            reasoning_tokens = (
                (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")
            )

            if not content:
                raise ValueError(
                    "AI 返回内容为空"
                    f"（finish_reason={finish_reason}, reasoning_tokens={reasoning_tokens}）。"
                    "若使用 deepseek-v4-flash，请关闭 thinking 或增大 max_tokens。"
                )

            parsed = self._parse_ai_content(content)
            logger.info(
                "AI 检测成功：返回 %s 个错误（max_tokens=%s, finish=%s, reasoning_tokens=%s）",
                len(parsed),
                max_tokens,
                finish_reason,
                reasoning_tokens,
            )
            return parsed

        except json.JSONDecodeError as exc:
            logger.warning("JSON 解析失败（max_tokens=%s）: %s", max_tokens, exc)
            return None
        except Exception as exc:
            logger.warning("AI 调用异常（max_tokens=%s）: %s: %s", max_tokens, type(exc).__name__, exc)
            logger.debug(traceback.format_exc())
            return None


siliconflow_client = SiliconFlowClient()


# ===== 句子对齐 =====
def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def align_sentence_index(ai_error: AiError, sentences: List[str]) -> Optional[int]:
    """根据 originalSentence 找到最匹配的句子索引。"""
    if not sentences:
        return None

    orig = _normalize(ai_error.originalSentence)

    # 1. 精确匹配
    for i, sent in enumerate(sentences):
        if _normalize(sent) == orig:
            return i

    # 2. 包含匹配：originalSentence 是某句的子串，或反之
    for i, sent in enumerate(sentences):
        n = _normalize(sent)
        if orig in n or n in orig:
            return i

    # 3. 用 matchedText 定位
    mt = _normalize(ai_error.matchedText)
    for i, sent in enumerate(sentences):
        if mt and mt in _normalize(sent):
            return i

    return None


# ===== 应用生命周期 =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await siliconflow_client.client.aclose()


app = FastAPI(
    title="IELTS Writing Grammar API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== 中间件 =====
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"[{datetime.utcnow().isoformat()}] {request.method} {request.url.path}")
    return await call_next(request)


# ===== 路由 =====
@app.get("/")
def root():
    """返回前端页面"""
    if os.path.exists(FRONTEND_HTML):
        return FileResponse(FRONTEND_HTML, media_type="text/html")
    return {"name": "IELTS Writing Grammar API", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "aiConfigured": bool(SILICONFLOW_API_KEY),
    }


@app.post("/api/grammar-check")
async def grammar_check(payload: GrammarCheckRequest):
    essay = payload.essay.strip()
    if not essay:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "缺少 essay 参数或为空"},
        )

    ai_errors, ai_failed, ai_message = await siliconflow_client.check_grammar(
        essay, payload.existingErrors
    )

    # 后端按与前端一致的规则切句，用 originalSentence 对齐索引
    sentences = split_sentences(essay)
    logger.info(
        "grammar-check essay_len=%s sentences=%s ai_raw=%s failed=%s",
        len(essay),
        len(sentences),
        len(ai_errors),
        ai_failed,
    )

    formatted = []
    seen = set()
    for idx, err in enumerate(ai_errors):
        si = align_sentence_index(err, sentences)
        if si is None:
            logger.warning(
                "AI 错误无法对齐，回退到句0: %s",
                (err.originalSentence or "")[:60],
            )
            si = 0

        # 去重：同一句 + 同一错误片段只保留一个
        key = (si, err.matchedText.lower().strip())
        if key in seen:
            logger.info("AI 重复错误已过滤: 句%s - %s", si, err.matchedText[:40])
            continue
        seen.add(key)

        formatted.append(
            {
                "id": f"ai-supplement-{idx}",
                "category": err.category or "AI检测",
                "pattern": None,
                "question": err.question or "这句话是否有语法问题？",
                "hints": err.hints
                if err.hints
                else [
                    "提示：请仔细检查这句话的语法结构。",
                    "提示：注意词汇搭配和时态一致性。",
                ],
                "explanation": err.explanation or "",
                "getAnswer": None,
                "corrected": err.corrected or "",
                "aiDetected": True,
                "sentenceIndex": si,
                "matchedText": err.matchedText or "",
            }
        )

    logger.info("grammar-check formatted=%s", len(formatted))
    return {
        "success": True,
        "data": formatted,
        "meta": {
            "aiDetected": len(formatted),
            "ruleDetected": len(payload.existingErrors),
            "aiFailed": ai_failed,
            "aiMessage": ai_message,
        },
    }


# ===== 练习题生成 =====
class ExerciseRequest(BaseModel):
    category: str
    example_sentence: str
    example_error: str
    example_corrected: str


class Exercise(BaseModel):
    question: str
    options: List[str]
    answer: int
    explanation: str


@app.post("/api/generate-exercises")
async def generate_exercises(payload: ExerciseRequest):
    """根据错误类型生成 3 道针对性练习题"""
    prompt = f"""根据以下 IELTS 学生的语法错误，生成 3 道针对性的练习题。

**错误类型：** {payload.category}
**原句：** {payload.example_sentence}
**错误片段：** {payload.example_error}
**正确写法：** {payload.example_corrected}

请生成 3 道练习题，帮助学生巩固这个语法点。题型为选择题，每题 4 个选项。

**请只返回以下 JSON 格式，不要添加任何其他内容：**

{{
  "exercises": [
    {{
      "question": "题目（包含一个语法错误的句子）",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "answer": 0,
      "explanation": "解析说明"
    }},
    {{
      "question": "题目2",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "answer": 1,
      "explanation": "解析说明"
    }},
    {{
      "question": "题目3",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "answer": 2,
      "explanation": "解析说明"
    }}
  ]
}}

要求：
1. 题目要针对 "{payload.category}" 这个错误类型。
2. 每题有且只有一个正确答案，answer 是正确选项的索引（0-3）。
3. 题目难度适中，与 IELTS 写作水平相当。
4. explanation 控制在 60 字以内。
"""

    try:
        response = await siliconflow_client.client.post(
            f"{siliconflow_client.base_url}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {siliconflow_client.api_key}",
            },
            json={
                "model": siliconflow_client.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的 IELTS 语法练习题生成助手。根据学生的错误类型生成针对性的选择题。只返回 JSON 格式，不要返回其他内容。",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.5,
                "max_tokens": 4000,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content")

        if not content:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "AI 返回内容为空"},
            )

        result = json.loads(content)
        exercises = result.get("exercises", [])
        parsed = [Exercise(**ex) for ex in exercises if isinstance(ex, dict)]

        return {
            "success": True,
            "data": [ex.dict() for ex in parsed],
            "meta": {"category": payload.category, "count": len(parsed)},
        }

    except Exception as exc:
        logger.error("练习题生成失败: %s: %s", type(exc).__name__, exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"练习题生成失败: {type(exc).__name__}"},
        )


# ===== 学生数据保存与查询 =====
class CheckpointRecord(BaseModel):
    sentenceIndex: int
    checkpointIndex: int
    category: str
    errorText: str
    correctedText: str
    hintLevelUsed: int  # 0=自己改好, 1=提示后改好, 2=看答案
    timeSpent: int  # 秒
    studentAnswer: str


class PracticeRecord(BaseModel):
    studentName: str
    essay: str
    checkpoints: List[CheckpointRecord]
    totalStats: dict
    studentId: Optional[str] = ""
    topic: Optional[str] = ""


RECORD_SELECT_SQL = """
    SELECT id, student_name, student_id, essay, topic, checkpoints, total_stats, created_at,
           teacher_revision, teacher_comment, teacher_updated_at, student_feedback_seen_at
    FROM practice_records
"""


def serialize_practice_row(row: sqlite3.Row) -> dict:
    revision = row["teacher_revision"] or ""
    comment = row["teacher_comment"] or ""
    teacher_updated = row["teacher_updated_at"] or ""
    seen_at = row["student_feedback_seen_at"] or ""
    teacher_reviewed = is_teacher_reviewed(revision, comment)
    has_unseen = False
    if teacher_reviewed:
        if not seen_at:
            has_unseen = True
        elif teacher_updated and str(seen_at) < str(teacher_updated):
            has_unseen = True
    keys = set(row.keys())
    topic = (row["topic"] if "topic" in keys else "") or ""
    topic_key = normalize_topic_key(topic)
    checkpoints = json.loads(row["checkpoints"])
    error_count = count_grammar_vocab_errors(checkpoints)
    return {
        "id": row["id"],
        "studentName": row["student_name"],
        "studentId": row["student_id"] or "",
        "topic": topic,
        "topicKey": topic_key,
        "essay": row["essay"],
        "checkpoints": checkpoints,
        "totalStats": json.loads(row["total_stats"]),
        "createdAt": row["created_at"],
        "teacherRevision": revision,
        "teacherComment": comment,
        "teacherUpdatedAt": teacher_updated,
        "teacherReviewed": teacher_reviewed,
        "studentFeedbackSeenAt": seen_at,
        "hasUnseenFeedback": has_unseen,
        "attempt": 1,
        "attemptCount": 1,
        "errorCount": error_count,
        "passErrorMax": WRITING_PASS_ERROR_MAX,
        "topicCompleted": is_topic_completed_by_errors(error_count),
        "canRewrite": False,
    }


def attach_attempt_meta(records: List[dict]) -> List[dict]:
    """为同学生同题记录附加 attempt / errorCount / canRewrite（错误≤阈值则结束）。"""
    from collections import defaultdict

    groups = defaultdict(list)
    for rec in records:
        sid = rec.get("studentId") or ""
        key = rec.get("topicKey") or ""
        groups[(sid, key)].append(rec)

    for (_sid, topic_key), items in groups.items():
        ordered = sorted(
            items,
            key=lambda r: (str(r.get("createdAt") or ""), int(r.get("id") or 0)),
        )
        count = len(ordered)
        for idx, rec in enumerate(ordered):
            error_count = count_grammar_vocab_errors(rec.get("checkpoints"))
            completed = is_topic_completed_by_errors(error_count)
            rec["attempt"] = idx + 1
            rec["attemptCount"] = count
            rec["errorCount"] = error_count
            rec["passErrorMax"] = WRITING_PASS_ERROR_MAX
            rec["topicCompleted"] = completed
            rec["canRewrite"] = False

        if not topic_key:
            continue
        latest = ordered[-1]
        # 老师已批改，且语法词汇错误仍 > 阈值，才可再写（次数不限）
        latest["canRewrite"] = bool(
            latest.get("teacherReviewed") and not latest.get("topicCompleted")
        )

    return records


def fetch_topic_attempts(conn: sqlite3.Connection, student_id: str, topic_key: str) -> List[sqlite3.Row]:
    """取出某学生某题的全部记录（按时间升序）。"""
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        """
        SELECT id, topic, teacher_revision, teacher_comment, checkpoints, created_at
        FROM practice_records
        WHERE student_id = ?
        ORDER BY created_at ASC, id ASC
        """,
        (student_id,),
    )
    rows = []
    for row in c.fetchall():
        if normalize_topic_key(row["topic"] or "") == topic_key:
            rows.append(row)
    return rows


@app.post("/api/save-practice")
async def save_practice(record: PracticeRecord):
    """保存学生的练习记录到数据库"""
    try:
        topic = (record.topic or "").strip()
        topic_key = normalize_topic_key(topic)
        student_id = (record.studentId or "").strip()

        conn = sqlite3.connect(DB_PATH)
        same_topic = []
        if topic_key and student_id:
            same_topic = fetch_topic_attempts(conn, student_id, topic_key)
            if same_topic:
                latest = same_topic[-1]
                latest_errors = count_grammar_vocab_errors(latest["checkpoints"])
                if is_topic_completed_by_errors(latest_errors):
                    conn.close()
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "message": (
                                f"该题目语法/词汇错误已≤{WRITING_PASS_ERROR_MAX}个，本题已结束，不能再提交"
                            ),
                            "errorCount": latest_errors,
                            "passErrorMax": WRITING_PASS_ERROR_MAX,
                            "attemptCount": len(same_topic),
                        },
                    )
                if not is_teacher_reviewed(
                    latest["teacher_revision"] or "",
                    latest["teacher_comment"] or "",
                ):
                    conn.close()
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "message": "该题目上一版尚未批改，请等待老师批改后再提交",
                            "errorCount": latest_errors,
                            "passErrorMax": WRITING_PASS_ERROR_MAX,
                            "attemptCount": len(same_topic),
                        },
                    )

        c = conn.cursor()
        c.execute(
            """
            INSERT INTO practice_records (student_name, student_id, essay, topic, checkpoints, total_stats)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record.studentName,
                student_id,
                record.essay,
                topic,
                json.dumps([cp.dict() for cp in record.checkpoints], ensure_ascii=False),
                json.dumps(record.totalStats, ensure_ascii=False),
            ),
        )
        conn.commit()
        record_id = c.lastrowid
        attempt = (len(same_topic) + 1) if (topic_key and student_id) else 1
        conn.close()
        logger.info(
            "保存练习记录成功: 学生=%s, 学号=%s, 记录ID=%s, attempt=%s",
            record.studentName,
            student_id,
            record_id,
            attempt,
        )
        return {
            "success": True,
            "recordId": record_id,
            "attempt": attempt,
            "passErrorMax": WRITING_PASS_ERROR_MAX,
            "topicKey": topic_key,
        }
    except Exception as exc:
        logger.error("保存练习记录失败: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"保存失败: {type(exc).__name__}"},
        )


@app.get("/api/teacher/records")
async def get_teacher_records(student_id: Optional[str] = None):
    """获取所有学生的练习记录（老师查看）"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if student_id:
            c.execute(
                RECORD_SELECT_SQL + " WHERE student_id = ? ORDER BY created_at DESC",
                (student_id,),
            )
        else:
            c.execute(RECORD_SELECT_SQL + " ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        records = attach_attempt_meta([serialize_practice_row(row) for row in rows])
        return {
            "success": True,
            "data": records,
            "passErrorMax": WRITING_PASS_ERROR_MAX,
        }
    except Exception as exc:
        logger.error("查询练习记录失败: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"查询失败: {type(exc).__name__}"},
        )


@app.get("/api/student/records")
async def get_student_records(student_id: str):
    """学生查看自己已提交的作文列表（按时间倒序）"""
    sid = (student_id or "").strip()
    if not sid:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "缺少学号 student_id"},
        )
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            RECORD_SELECT_SQL + " WHERE student_id = ? ORDER BY created_at DESC",
            (sid,),
        )
        rows = c.fetchall()
        conn.close()
        records = attach_attempt_meta([serialize_practice_row(row) for row in rows])
        unseen_count = sum(1 for r in records if r.get("hasUnseenFeedback"))
        return {
            "success": True,
            "data": records,
            "unseenCount": unseen_count,
            "passErrorMax": WRITING_PASS_ERROR_MAX,
        }
    except Exception as exc:
        logger.error("学生查询练习记录失败: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"查询失败: {type(exc).__name__}"},
        )


class StudentAckFeedback(BaseModel):
    studentId: str = ""


@app.post("/api/student/records/{record_id}/ack-feedback")
async def ack_student_feedback(record_id: int, payload: StudentAckFeedback):
    """学生已读老师批改，清除「新批改」提示"""
    sid = (payload.studentId or "").strip()
    if not sid:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "缺少学号 studentId"},
        )
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            "SELECT id, student_id FROM practice_records WHERE id = ?",
            (record_id,),
        )
        row = c.fetchone()
        if not row:
            conn.close()
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "记录不存在"},
            )
        if (row["student_id"] or "") != sid:
            conn.close()
            return JSONResponse(
                status_code=403,
                content={"success": False, "message": "无权操作该记录"},
            )
        seen_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            """
            UPDATE practice_records
            SET student_feedback_seen_at = ?
            WHERE id = ?
            """,
            (seen_at, record_id),
        )
        conn.commit()
        conn.close()
        return {"success": True, "recordId": record_id, "studentFeedbackSeenAt": seen_at}
    except Exception as exc:
        logger.error("确认已读老师批改失败: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"操作失败: {type(exc).__name__}"},
        )


class TeacherFeedback(BaseModel):
    teacherRevision: str = ""
    teacherComment: str = ""


@app.post("/api/teacher/records/{record_id}/feedback")
async def save_teacher_feedback(record_id: int, payload: TeacherFeedback):
    """保存老师对学生作文的修正稿与评语（可反复修改）"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM practice_records WHERE id = ?", (record_id,))
        if not c.fetchone():
            conn.close()
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "记录不存在"},
            )
        updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            """
            UPDATE practice_records
            SET teacher_revision = ?, teacher_comment = ?, teacher_updated_at = ?
            WHERE id = ?
            """,
            (
                payload.teacherRevision or "",
                payload.teacherComment or "",
                updated_at,
                record_id,
            ),
        )
        conn.commit()
        conn.close()
        logger.info("老师评语已保存: record_id=%s", record_id)
        return {
            "success": True,
            "recordId": record_id,
            "teacherUpdatedAt": updated_at,
        }
    except Exception as exc:
        logger.error("保存老师评语失败: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"保存失败: {type(exc).__name__}"},
        )


@app.get("/teacher")
async def teacher_page():
    """老师查看页面"""
    teacher_html = os.path.join(_BACKEND_DIR, "teacher.html")
    if os.path.exists(teacher_html):
        return FileResponse(teacher_html, media_type="text/html")
    return {"message": "老师页面未找到，请创建 teacher.html"}


if __name__ == "__main__":
    import uvicorn

    print(
        """
    ========================================
    IELTS Writing Backend (Python/FastAPI)
    ========================================
    服务启动于: http://localhost:{port}
    健康检查:  http://localhost:{port}/api/health
    语法检查:  POST http://localhost:{port}/api/grammar-check
    ========================================
    """.format(port=PORT)
    )
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
