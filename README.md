# 雅思练习平台

这是一个面向雅思基础训练的多模块学习平台。项目由静态前端模块、主站学生/教师入口、Python SQLite API 服务和部署脚本组成。

## 项目结构

| 路径 | 说明 |
|---|---|
| `sources/` | 前端静态站点与各学习/测试模块，每个模块独立维护 |
| `sources/tinglidanciceshi/` | 主站入口：学生端、教师端、模块 iframe 容器 |
| `sources/tinglidanciceshi/css/main.css` | 主站样式 |
| `sources/tinglidanciceshi/js/` | 主站脚本（见下方「主站前端拆分」） |
| `scripts/local_server.py` | 本地静态文件服务和 SQLite API |
| `scripts/deploy.py` | Linux 服务器覆盖部署脚本，凭据从环境变量读取 |
| `scripts/repair_tracking_data.py` | 清理旧版重复学习会话、测试镜像会话和未完成阅读测试记录 |
| `tests/` | 时长统计、历史类型和数据修复回归测试 |
| `data/` | 本地运行数据库目录，不提交真实数据库 |
| `docs/` | 架构、前台清单、部署迁移等项目文档 |
| `DEV_SERVER.md` | 本地开发服务端口、启动方式与测试账号 |
| `DEPLOY.md` | GitHub 推送与服务器部署流程 |

## 主站前端拆分

主站 `index.html` 只保留页面结构；样式与脚本按职责拆分，避免改教师端误伤学生端：

| 文件 | 职责 |
|---|---|
| `css/main.css` | 主站样式 |
| `js/local_db_client.js` | `/api/db` 前端适配（兼容原 Supabase 调用风格） |
| `js/tracking.js` | 学习/测试时长工具与保存 |
| `js/modules.js` | 模块配置、词表/词伙数据与模块工具 |
| `js/app.js` | 数据库初始化、通用 UI、入口路由 |
| `js/teacher.js` | 教师登录与后台（含管理员管理教师账号） |
| `js/student.js` | 学生登录、学习与测试 |

## 学习模块

| 模块 | 目录 | 类型 | 维护文档 |
|---|---|---|---|
| 听力1000词 | `sources/tinglidanciceshi/` | 主站、学生端、教师端、学习、测试 | `sources/tinglidanciceshi/README.md` |
| 听力基础词汇 | `sources/tinglidanciceshi/` | 与听力1000词同逻辑的学习/测试（词库不同） | `sources/tinglidanciceshi/README.md` |
| 阅读同义替换学习 | `sources/tongyitihuan/` | 学习 | `sources/tongyitihuan/README.md` |
| 阅读同义替换测试 | `sources/tongyitihuanceshi/` | 测试 | `sources/tongyitihuanceshi/README.md` |
| 写作词伙学习 | `sources/xiezuocihuo/` | 学习 | `sources/xiezuocihuo/README.md` |
| 写作词伙测试 | `sources/xiezuocihuoceshi/` | 测试 | `sources/xiezuocihuoceshi/README.md` |
| 长难句学习 | `sources/changnanju/` | 学习 | `sources/changnanju/README.md` |
| 长难句测试 | `sources/changnanjuceshi/` | 测试 | `sources/changnanjuceshi/README.md` |
| 答案句听写学习 | `sources/daanjutingxie/` | 学习 | `sources/daanjutingxie/README.md` |
| 答案句听写测试 | `sources/daanjutingxieceshi/` | 测试 | `sources/daanjutingxieceshi/README.md` |
| 写作句子翻译 | `sources/juzifanyixin/` | 学习 | `sources/juzifanyixin/README.md` |
| 听力 P4 跟读（学习） | `sources/P4gendu/` | 学习 | `sources/P4gendu/README.md` |
| 听力 P4 跟读（测试） | `sources/P4genduceshi/` | 测试 | `sources/P4genduceshi/README.md` |
| 口语练习 | `sources/kouyulianxi/` | 学习 + AI 评分 | `sources/kouyulianxi/README.md` |
| 作文批改 | `sources/xiezuopigai/` | 学习 + 教师批改 + 学生历史 | `sources/xiezuopigai/README.md` |

## 本地运行

主站（静态页 + SQLite API）：

```powershell
python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db
```

作文批改依赖独立的写作 FastAPI（默认 `127.0.0.1:8080`）。`local_server.py` 会把 `/api/writing/*` 代理到该服务，并在未运行时尝试自动启动。也可手动启动：

```powershell
cd sources/xiezuopigai/ielts-writing-backend
python -m uvicorn main:app --host 127.0.0.1 --port 8080
```

| 入口 | 地址 |
|---|---|
| 学生端 | `http://127.0.0.1:49182/tinglidanciceshi/` |
| 教师端 | `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher` |
| 作文批改教师端 | `http://127.0.0.1:49182/tinglidanciceshi/?role=writing`（密码见 `DEV_SERVER.md`） |
| 健康检查 | `http://127.0.0.1:49182/api/health` |
| 作文批改练习 | `http://127.0.0.1:49182/xiezuopigai/ielts-student-practice.html` |
| P4 跟读测试 | `http://127.0.0.1:49182/P4genduceshi/` |

首次启动会自动创建 `data/ielts_local.db` 并写入种子数据。删除该文件可重置本地库。

## 本地测试账号

凭证存在 SQLite（`students` / `teachers` 表），不写死在前端。完整说明见 `DEV_SERVER.md`。

| 类型 | 账号 | 密码 |
|---|---|---|
| 管理员 | `admin`（入口 `?role=teacher`） | `sjdh4405` |
| 教师示例 | `zhangxiaodong`（教研校长 / 阅读、写作） | 初始 `123456` |
| 学生 | `2025001` | `123456`（首次登录会要求改密） |
| 作文批改教师端 | 仅密码入口 `?role=writing` | `xiezuo8805` |

管理员登录后可在「教师账号」页签添加教师（姓名、账号、职位、科目；初始密码 `123456`）。

## 部署维护

**注意：** push 到 `main` 会触发 GitHub Actions 自动部署阿里云。功能验证阶段可先推功能分支，确认后再合并 `main`。

部署脚本不会读取仓库中的明文密码。执行部署前先设置环境变量：

```powershell
$env:IELTS_DEPLOY_HOST="服务器地址"
$env:IELTS_DEPLOY_USER="root"
$env:IELTS_DEPLOY_PASSWORD="服务器密码"
$env:IELTS_DEPLOY_DOMAIN="training.oyenglish.com.cn"
python scripts/deploy.py
```

若服务器包含 2026-07-10 之前产生的重复追踪数据，首次发布修复版时使用：

```powershell
python scripts/deploy.py --repair-tracking-data
```

更完整的 GitHub 推送、备份、部署和回滚流程见 `DEPLOY.md`。

## 维护原则

| 原则 | 要求 |
|---|---|
| 模块隔离 | 每个训练模块只修改自己的目录；主站公共接入在 `js/modules.js`，教师/学生逻辑分文件维护 |
| 教师凭证 | 教师账号密码存 `teachers` 表，由管理员后台维护，不写死在前端 |
| 数据保护 | 默认不提交或覆盖 `data/*.db`，线上部署前必须备份 |
| 音频保护 | `*.mp3`、`sources/tinglidanciceshi/audio/`、`sources/daanjutingxie/A听力答案句/` 只在本地或服务器本地维护，不提交 GitHub |
| 凭据保护 | GitHub Token、服务器密码、SSH 私钥只放环境变量或系统凭据管理 |
| AI 统一来源 | Key/模型只维护在 `config/ai.env`（服务器同路径）；默认部署不覆盖，首次用 `--sync-ai-env` |
| 验证优先 | 修改后至少运行 Python 语法检查、本地健康检查和关键页面 HTTP 检查 |

## 回归测试

```powershell
python -m compileall scripts tests
python -m unittest discover -s tests -p "test_*.py" -v
node tests/test_tracking_utils.js
```
