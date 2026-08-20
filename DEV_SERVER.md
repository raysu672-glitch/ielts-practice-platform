# 本地开发服务

| 服务 | 端口 | 启动命令 | 备注 |
|---|---:|---|---|
| 本地静态页 + SQLite API | 49182 | `python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db` | 主站访问 `http://127.0.0.1:49182/tinglidanciceshi/`；教师入口 `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher`；`/api/writing/*` 代理到写作后端 |
| 作文批改 FastAPI | 8080 | `cd sources/xiezuopigai/ielts-writing-backend && python -m uvicorn main:app --host 127.0.0.1 --port 8080` | AI 统一读仓库根 `config/ai.env`（见 `config/ai.env.example`）；主站可自动拉起 |
| 回归验证服务 | 49247 | `python scripts/local_server.py --host 127.0.0.1 --port 49247 --static-dir sources --db data/verification_tracking.db` | 使用数据库副本验证统计和历史，不修改正式本地数据；验证结束后停止 |

## 本地测试账号

| 类型 | 账号/入口 | 密码 |
|---|---|---|
| 管理员 | 入口 `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher`；账号 `admin` | `sjdh4405`（存于 DB `teachers` 表） |
| 教师（张晓东） | 同上入口；账号 `zhangxiaodong`（教研校长 / 阅读、写作） | 初始密码 `123456` |
| 作文批改教师端（仅批改） | `http://127.0.0.1:49182/tinglidanciceshi/?role=writing` | `xiezuo8805` |
| 学生端 | `2025001` | `123456` |
| 新增学生 | 教师端添加后生成学号，如 `2025002` | `123456` |

## 维护备注

| 项目 | 说明 |
|---|---|
| 端口选择 | `49182` 是本项目固定高位端口，避免使用 `3000`、`5173`、`8000` 等常见默认端口 |
| 数据库 | 本地数据库为 `data/ielts_local.db`，已被 `.gitignore` 排除 |
| 部署 | 服务器部署命令和环境变量见 `DEPLOY.md` |
