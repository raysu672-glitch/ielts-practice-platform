# 入学摸底

约 40 分钟四科连续摸底（听力听写 / 阅读同义 / 写作词伙+翻译 / 口语现场录），生成分科雅思区间预估与排课分档，供助教安排基础训练。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 页面壳与样式 |
| `app.js` | 流程、计时、做题、录音、报告、上报 |
| `scoring.js` | 正确率 / AI 档 → 区间与分档映射 |
| `questions_a.js` | 套别 A 固定题 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/xinshengmodi/` |
| 主站模式 | iframe（学生端「入学摸底」按钮） |
| 访客临时入口 | `/xinshengmodi/?guest=1`（无需学号；填姓名后开考） |
| `module_type` | `placement` |
| 正式生上报 | `postMessage` → `genericTestComplete` |
| 访客上报 | `POST /api/placement/guest-submit` → 教师端「入学摸底」页 |
| 调试减题 | `?debug=1` |

## 判分

| 科目 | 方式 |
|---|---|
| 听力 | 预生成 MP3（`audio/L*.mp3`，进入本科时预加载）+ 关键词覆盖部分分；缺音频回退浏览器 TTS |
| 阅读 / 词伙 | 前端规则 |
| 翻译 | 复用 `juzifanyixinceshi/match.js` |
| 口语 | `/api/p4/transcribe` + `/api/ai/messages`；失败则启发式 + 置信度「低」 |

## 维护注意

| 项目 | 要求 |
|---|---|
| 听力音频 | `python scripts/gen_placement_listening_audio.py`（edge-tts）；或从答案句 CDN 拉同文 mp3 到 `audio/`。`*.mp3` 不进 Git |
| 题库 | 套别 A 固定，勿改为全库随机，否则映射表失效 |
| 进度表 | `placement` 模块带 `placement: true`，不参与普通达标汇总与错题本 |
| 验证 | 学生端点「入学摸底」走完；教师端测试记录可见一条入学摸底 |
