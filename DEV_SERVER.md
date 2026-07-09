# 本地开发服务

| 服务 | 端口 | 启动命令 | 备注 |
|---|---:|---|---|
| 本地静态页 + SQLite API | 49182 | `python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db` | 主站访问 `http://127.0.0.1:49182/tinglidanciceshi/`；教师入口 `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher` |

## 本地测试账号

| 类型 | 账号/入口 | 密码 |
|---|---|---|
| 教师端 | `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher` | `sjdh4405` |
| 学生端 | `2025001` | `123456` |
| 新增学生 | 教师端添加后生成学号，如 `2025002` | `123456` |

## 维护备注

| 项目 | 说明 |
|---|---|
| 端口选择 | `49182` 是本项目固定高位端口，避免使用 `3000`、`5173`、`8000` 等常见默认端口 |
| 数据库 | 本地数据库为 `data/ielts_local.db`，已被 `.gitignore` 排除 |
| 部署 | 服务器部署命令和环境变量见 `DEPLOY.md` |
