# 口语练习（kouyulianxi）

雅思口语练习模块：Part 1（步骤 + 线索 + 素材 + 录音 AI 评分）与 Part 2（先背素材，再套题）。页面内可切换 P1/P2。

来源仓库：https://github.com/raysu672-glitch/kouyulianxi

## 接入主站

| 项目 | 值 |
|---|---|
| 访问路径 | `/kouyulianxi/` |
| 主站模式 | iframe（学习 / 测试） |
| `module_type` | `speaking` |
| 主站入口 | `/kouyulianxi/index.html` |
| 学习记录 | 录音结束/退出时 `postMessage: genericStudyComplete` → `study_sessions`（`words_tested`=本段新练题数，`duration_seconds`=录音时长） |
| 测试记录 | P1 在测试模式下完成 AI 评分后 `postMessage: genericTestComplete`（Band 分） |

## 语音与评分接口

| 能力 | 接口 / 逻辑 |
|---|---|
| 题目英音 | 本地预生成 `audio/<category>/<id>.mp3`（`audio/manifest.js`）；缺失时回退浏览器 TTS |
| 录音转写 | `POST /api/p4/transcribe`（`local_server.py` 代理到 `https://p4.oyenglish.com.cn/transcribe`） |
| AI Key / 模型 | `GET /api/config`（读 `config/ai.env` 的 `AI_API_KEY` / `AI_BASE_URL` / `AI_MODEL`） |
| AI 评分 | 浏览器调用 DeepSeek Anthropic 兼容接口；四维取平均为 Overall Band |

前端配置见 `config.js`：

```js
window.API_CONFIG = { TRANSCRIBE_PATH: '/api/p4/transcribe' };
```

## 主要文件

| 文件 | 作用 |
|---|---|
| `index.html` / `style.css` / `app.js` | P1 页面与练习逻辑（录音、转写、AI 评分） |
| `p1-data.js` | P1 题库、线索与素材分层提示 |
| `p2-app.js` / `p2-data.js` | P2 背素材 + 套题 |
| `audio/` | P1 预生成英音题目（mp3 不提交 GitHub） |
| `config.js` | ASR 接口路径 |

## 维护注意

| 项目 | 要求 |
|---|---|
| 音频资源 | `*.mp3` 已被 `.gitignore` 排除；本地/服务器需单独放置 `audio/` |
| AI 配置 | Key 只维护在 `config/ai.env`，不要写进前端仓库 |
| 验证方式 | 从主站学习进度进入「口语练习」，确认可切换 P1/P2、听题、录音转写与 AI 评分 |
