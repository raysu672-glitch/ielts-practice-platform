# 听力 P4 跟读倍速测试

本目录是听力 Part 4 跟读测试模块。学生跟读整段音频后，录音上传到腾讯云 ASR 后端评分，结果通过 `postMessage` 回传主站写入 `test_records`。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试入口、录音、上传评分、结果展示与主站上报 |
| `config.js` | 后端 `API_BASE` 配置 |
| `C4T1S4.mp3` | 跟读音频；本地/服务器本地维护，不提交 GitHub |
| `backend/` | 独立 ASR 后端参考代码（线上已部署，不由本站静态服务运行） |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/P4genduceshi/` |
| 主站模式 | iframe（`mode=test`） |
| `module_type` | `listening_p4_speed` |
| 测试上报 | `postMessage: genericTestComplete` |
| 评分后端 | 同源主站 `/api/p4/transcribe`（由 `local_server.py` 转发到 ASR） |
| 上游 ASR | 默认 `https://p4.oyenglish.com.cn`，可用环境变量 `IELTS_P4_ASR_BASE` 覆盖 |

## 维护注意

| 项目 | 要求 |
|---|---|
| 麦克风 | 主站 iframe 需 `allow="microphone; autoplay"` |
| 音频资源 | 音频不进 Git；部署后需单独放到本目录 |
| 后端 | 页面只请求主站 Python 服务；腾讯云密钥仍只在上游 ASR 服务器环境变量中 |
| 验证方式 | 从主站点「测试」，完成跟读后确认分数写入学生历史 |
