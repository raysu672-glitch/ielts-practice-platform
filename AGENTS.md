# AGENTS.md

## Cursor Cloud specific instructions

雅思练习平台：静态前端（`sources/`）+ Python 标准库实现的静态文件服务 + SQLite API（`scripts/local_server.py`）。命令与端口以 `README.md`、`DEV_SERVER.md`、`DEPLOY.md` 为准，这里只记录非显而易见的注意事项。

### 发布流程（强制）
- 永远：**本地先改 → push 到 GitHub → 再部署阿里云**。
- 禁止先改线上再回写本地；禁止未 push 就部署。细节见 `DEPLOY.md`。

### 运行时依赖
- 本地服务器 `scripts/local_server.py` 只用 Python 标准库，无需任何第三方包即可启动。
- `requirements.txt` 里的 `paramiko` 仅供 `scripts/deploy.py` 部署使用，本地开发/测试用不到。
- 环境里只有 `python3`（没有 `python` 命令），而文档示例写的是 `python`，运行时请改用 `python3`。

### 启动服务
- 启动命令见 `DEV_SERVER.md`（本地端口固定 `49182`，请勿改用 3000/5173/8000 等常见端口）。
- 数据库文件 `data/ielts_local.db` 被 `.gitignore` 排除，首次启动会自动创建并写入种子数据（教师配置、达标标准、测试学生 `2025001`）。删除该文件即可重置数据。

### 测试账号（本地种子数据）
- 学生：学号 `2025001`，密码 `123456`。首次登录会强制要求修改密码后才能进入模块页，这是预期行为，不是 bug。
- 教师入口：`/tinglidanciceshi/?role=teacher`，密码 `sjdh4405`。

### Lint / 测试
- 本仓库没有 ESLint/ruff 等 lint 配置；README 所称“语法检查”即 `python3 -m compileall scripts tests`。
- 回归测试命令见 `README.md`（`python3 -m unittest discover -s tests -p "test_*.py"` 与 `node tests/test_tracking_utils.js`）。

### 不要提交
- `data/*.db`、音频文件（`*.mp3/wav/m4a/ogg` 及 `sources/tinglidanciceshi/audio/` 等）已被 `.gitignore` 排除，服务器缺音频时页面会退化到浏览器 TTS。
