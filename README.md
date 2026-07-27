# 雅思练习平台

这是一个面向雅思基础训练的多模块学习平台。项目由静态前端模块、主站学生/教师入口、Python SQLite API 服务和部署脚本组成。

## 项目结构

| 路径 | 说明 |
|---|---|
| `sources/` | 前端静态站点与各学习/测试模块，每个模块独立维护 |
| `scripts/local_server.py` | 本地静态文件服务和 SQLite API |
| `scripts/deploy.py` | Linux 服务器覆盖部署脚本，凭据从环境变量读取 |
| `scripts/repair_tracking_data.py` | 清理旧版重复学习会话、测试镜像会话和未完成阅读测试记录 |
| `tests/` | 时长统计、历史类型和数据修复回归测试 |
| `data/` | 本地运行数据库目录，不提交真实数据库 |
| `docs/` | 架构、前台清单、部署迁移等项目文档 |
| `DEV_SERVER.md` | 本地开发服务端口与启动方式 |
| `DEPLOY.md` | GitHub 推送与服务器部署流程 |

## 学习模块

| 模块 | 目录 | 类型 | 维护文档 |
|---|---|---|---|
| 听力1000词 | `sources/tinglidanciceshi/` | 主站、学生端、教师端、学习、测试 | `sources/tinglidanciceshi/README.md` |
| 阅读同义替换学习 | `sources/tongyitihuan/` | 学习 | `sources/tongyitihuan/README.md` |
| 阅读同义替换测试 | `sources/tongyitihuanceshi/` | 测试 | `sources/tongyitihuanceshi/README.md` |
| 写作词伙学习 | `sources/xiezuocihuo/` | 学习 | `sources/xiezuocihuo/README.md` |
| 写作词伙测试 | `sources/xiezuocihuoceshi/` | 测试 | `sources/xiezuocihuoceshi/README.md` |
| 长难句学习 | `sources/changnanju/` | 学习 | `sources/changnanju/README.md` |
| 长难句测试 | `sources/changnanjuceshi/` | 测试 | `sources/changnanjuceshi/README.md` |
| 答案句听写学习 | `sources/daanjutingxie/` | 学习 | `sources/daanjutingxie/README.md` |
| 答案句听写测试 | `sources/daanjutingxieceshi/` | 测试 | `sources/daanjutingxieceshi/README.md` |
| 写作句子翻译 | `sources/juzifanyixin/` | 学习 | `sources/juzifanyixin/README.md` |
| 听力 P4 跟读 | `sources/P4gendu/` | 学习 | `sources/P4gendu/README.md` |
| 听力 P4 跟读测试 | `sources/P4genduceshi/` | 测试 | `sources/P4genduceshi/README.md` |

## 本地运行

```powershell
python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db
```

| 入口 | 地址 |
|---|---|
| 学生端 | `http://127.0.0.1:49182/tinglidanciceshi/` |
| 教师端 | `http://127.0.0.1:49182/tinglidanciceshi/?role=teacher` |
| 健康检查 | `http://127.0.0.1:49182/api/health` |

## 部署维护

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
| 模块隔离 | 每个训练模块只修改自己的目录，公共接入逻辑集中在主站 |
| 数据保护 | 默认不提交或覆盖 `data/*.db`，线上部署前必须备份 |
| 音频保护 | `*.mp3`、`sources/tinglidanciceshi/audio/`、`sources/daanjutingxie/A听力答案句/` 只在本地或服务器本地维护，不提交 GitHub |
| 凭据保护 | GitHub Token、服务器密码、SSH 私钥只放环境变量或系统凭据管理 |
| 验证优先 | 修改后至少运行 Python 语法检查、本地健康检查和关键页面 HTTP 检查 |

## 回归测试

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node tests/test_tracking_utils.js
```
