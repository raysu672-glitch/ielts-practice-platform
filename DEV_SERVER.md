# 本地开发服务

## 环境变量

首次创建本地数据库前设置管理员密码（`admin` 账号仅在库中不存在时插入；未设置则跳过创建并打印警告）。任选其一：

```powershell
$env:IELTS_ADMIN_PASSWORD="你的管理员密码"
```

```bash
export IELTS_ADMIN_PASSWORD='你的管理员密码'
```

或复制 `config/admin.env.example` → `config/admin.env` 并填写 `IELTS_ADMIN_PASSWORD`。

已有 `data/ielts_local.db` 需改管理员密码时，`teachers.password` 存 PBKDF2 哈希：

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from password_utils import hash_password; print(hash_password('你的新密码'))"
```

```sql
UPDATE teachers SET password='<上一步输出的哈希>' WHERE teacher_id='admin';
```

| 服务 | 端口 | 启动命令 | 备注 |
|---|---:|---|---|
| 本地静态页 + SQLite API | 49182 | `python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db` | 主站访问 `http://127.0.0.1:49182/tinglidanciceshi/`；教师入口 `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher`；`/api/writing/*` 代理到写作后端 |
| 作文批改 FastAPI | 8080 | `cd sources/xiezuopigai/ielts-writing-backend && python -m uvicorn main:app --host 127.0.0.1 --port 8080` | AI 统一读仓库根 `config/ai.env`（见 `config/ai.env.example`）；主站可自动拉起 |
| 回归验证服务 | 49247 | `python scripts/local_server.py --host 127.0.0.1 --port 49247 --static-dir sources --db data/verification_tracking.db` | 使用数据库副本验证统计和历史，不修改正式本地数据；验证结束后停止 |

## 本地测试账号

| 类型 | 账号/入口 | 密码 |
|---|---|---|
| 管理员 | 入口 `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher`；账号 `admin` | 由 `IELTS_ADMIN_PASSWORD` 在首次建库时设定 |
| 教师（张晓东） | 同上入口；账号 `zhangxiaodong`（仅 `--host 127.0.0.1` 时自动创建） | 初始密码 `123456` |
| 作文批改教师端（仅批改） | `http://127.0.0.1:49182/tinglidanciceshi/?role=writing` | `xiezuo8805` |
| 学生端 | `2025001` | `123456` |
| 新增学生 | 教师端添加后生成学号，如 `2025002` | 由 API 返回的一次性初始密码 |

## 维护备注

| 项目 | 说明 |
|---|---|
| 端口选择 | `49182` 是本项目固定高位端口，避免使用 `3000`、`5173`、`8000` 等常见默认端口 |
| 数据库 | 本地数据库为 `data/ielts_local.db`，已被 `.gitignore` 排除 |
| 部署 | 服务器部署命令和环境变量见 `DEPLOY.md` |
| Session 鉴权（P0） | 学生/教师登录走 `/api/auth/*/login`，HttpOnly Cookie；未登录访问 `/api/db` 返回 401 |
