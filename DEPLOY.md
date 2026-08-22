# 部署维护文档

本文档记录新仓库推送、服务器覆盖部署、备份和回滚方式。不要把 GitHub Token、服务器密码、SSH 私钥写入仓库文件。

## 发布流程（强制）

功能改动一律按下面 **六步** 顺序，**禁止跳步，禁止先改阿里云再回写本地**：

### 1. 备份数据库

部署前先把线上 SQLite 拉到本地，**不要**只依赖 `deploy.py` 的整站 tar 备份。

```powershell
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$dir = "backups/aliyun_$stamp"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
# 用已配置的 SSH 密钥/密码，将服务器 /var/www/ielts/data/*.db 下载到 $dir
# 示例（密钥路径按本机实际修改）：
# scp -i "你的.pem" root@服务器IP:/var/www/ielts/data/*.db $dir/
Get-FileHash "$dir\*.db" -Algorithm SHA256 | Tee-Object -FilePath "$dir\SHA256SUMS"
```

### 2. 本地跑测试

```powershell
python -m compileall scripts tests
python -m unittest discover -s tests -p "test_*.py" -v
node tests/test_tracking_utils.js
```

任一项失败则停止，不得继续 push / 部署。

### 3. 推 GitHub

合并到 `main` 并推送：`git push origin main`（或 PR 合并后由 GitHub 推送）。

### 4. 服务器拉取 / 部署

push 到 `main` 后，GitHub Actions 会自动运行 `scripts/deploy.py`。也可在仓库 **Actions → Deploy to Aliyun → Run workflow** 手动触发。

本地紧急热修仍可用 `python scripts/deploy.py`，但事后必须立刻补 commit 并 push 到 `main`，保证 GitHub 与线上一致。不要直接在服务器上改业务代码。

默认部署**不会**覆盖线上 `data/*.db`、`config/ai.env` 与音频文件。

### 5. 检查 `/api/health`

```powershell
curl https://training.oyenglish.com.cn/api/health
# 或 SSH 到服务器后：
# curl http://127.0.0.1:49182/api/health
```

预期返回含 `ok: true`。

### 6. 学生端和教师端各测一遍

| 端 | 入口 | 最低验收 |
|---|---|---|
| 学生端 | `https://training.oyenglish.com.cn/tinglidanciceshi/` | 页面可开、登录/进入模块正常 |
| 教师端 | `https://training.oyenglish.com.cn/tinglidanciceshi/?role=teacher` | 教师登录页可开、可登录 |

任一步失败：停止发布，修复后从失败步重跑。

### GitHub Actions 自动部署（一次性配置）

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 中新增：

| Secret | 必填 | 说明 |
|---|---|---|
| `IELTS_DEPLOY_HOST` | 是 | 服务器公网 IP 或域名 |
| `IELTS_DEPLOY_KEY` | 是 | SSH 私钥全文（含 `BEGIN`/`END` 行） |
| `IELTS_DEPLOY_USER` | 否 | 默认 `root` |
| `IELTS_DEPLOY_PORT` | 否 | 默认 `22` |
| `IELTS_DEPLOY_DOMAIN` | 否 | 默认 `training.oyenglish.com.cn` |

用 GitHub CLI 一次性写入示例（PowerShell）：

```powershell
gh secret set IELTS_DEPLOY_HOST --body "你的服务器IP"
gh secret set IELTS_DEPLOY_USER --body "root"
gh secret set IELTS_DEPLOY_KEY < "d:\Download\雅思训练.pem"
```

自动部署**不会**覆盖线上 `data/*.db`、`config/ai.env` 与音频文件。更换 AI Key 仍需本机执行：`python scripts/deploy.py --sync-ai-env`。

## GitHub 推送

| 项目 | 说明 |
|---|---|
| 仓库名称 | 建议使用 `ielts-practice-platform` |
| 可见性 | 默认私有仓库 |
| 认证方式 | 使用 `gh auth login`、系统凭据管理或临时环境变量 |
| 不提交内容 | `.env`、`config/ai.env`、`config/admin.env`、`*.pem`、`data/*.db`、音频文件、`sources/_zips/`、`sources/_extract/`、本地截图 |

## 平台统一 AI 配置

当前与后续凡需 AI 介入的功能，统一走 DeepSeek（`config/ai.env`），不要在各模块各自散落 Key/模型。

| 项目 | 说明 |
|---|---|
| 本地文件 | `config/ai.env`（从 `config/ai.env.example` 复制） |
| 服务器文件 | `/var/www/ielts/config/ai.env` |
| 变量 | `AI_API_KEY`、`AI_BASE_URL`、`AI_MODEL` |
| 当前默认 | `https://api.deepseek.com` + `deepseek-v4-flash` |
| 默认部署 | **不会**覆盖服务器上的 `config/ai.env` |
| 首次/更换 Key | `python scripts/deploy.py --sync-ai-env` |

systemd 通过 `EnvironmentFile=-/var/www/ielts/config/ai.env` 注入；写作后端也会优先读取该文件。

## 管理员初始密码（`IELTS_ADMIN_PASSWORD`）

`admin` 账号**不在代码中写死密码**。仅在新库首次插入 `teachers` 行时使用环境变量中的明文，入库前经 PBKDF2 哈希；`ON CONFLICT DO NOTHING` 不会覆盖已有库。

| 项目 | 说明 |
|---|---|
| 本地文件 | `config/admin.env`（从 `config/admin.env.example` 复制） |
| 服务器文件 | `/var/www/ielts/config/admin.env` |
| 变量 | `IELTS_ADMIN_PASSWORD` |
| 默认部署 | **不会**覆盖服务器上的 `config/admin.env` |
| 首次/更换 | `python scripts/deploy.py --sync-admin-env`（或部署前设置 `$env:IELTS_ADMIN_PASSWORD`） |

systemd 同时加载 `config/admin.env`。未设置时服务仍可启动，但**不会**自动创建 `admin` 账号。

已有库改管理员密码（`password` 列为哈希）：

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from password_utils import hash_password; print(hash_password('你的新密码'))"
```

```sql
UPDATE teachers SET password='<上一步哈希>' WHERE teacher_id='admin';
```

临时环境变量示例：

```powershell
$env:GITHUB_TOKEN="你的 GitHub Token"
```

## 部署环境变量

| 变量 | 必填 | 说明 |
|---|---|---|
| `IELTS_DEPLOY_HOST` | 是 | 服务器地址 |
| `IELTS_DEPLOY_PORT` | 否 | SSH 端口，默认 `22` |
| `IELTS_DEPLOY_USER` | 否 | SSH 用户，默认 `root` |
| `IELTS_DEPLOY_PASSWORD` | 二选一 | SSH 密码 |
| `IELTS_DEPLOY_KEY` | 二选一 | SSH 私钥路径 |
| `IELTS_DEPLOY_DOMAIN` | 否 | 站点域名，默认 `training.oyenglish.com.cn` |
| `IELTS_DEPLOY_DIR` | 否 | 服务器部署目录，默认 `/var/www/ielts` |
| `IELTS_BACKUP_DIR` | 否 | 服务器备份目录，默认 `/root/ielts_backups` |
| `IELTS_SERVICE_PORT` | 否 | Python 服务端口，默认 `49182` |
| `IELTS_P4_ASR_BASE` | 否 | P4 跟读评分上游地址，默认 `https://p4.oyenglish.com.cn` |
| `IELTS_CERTBOT_EMAIL` | 仅首次 HTTPS | Let's Encrypt 邮箱 |

## 覆盖部署

默认部署会执行以下动作：

| 步骤 | 动作 |
|---|---|
| 1 | SSH 连接目标服务器 |
| 2 | 将当前 `/var/www/ielts` 打包备份到 `/root/ielts_backups/` |
| 3 | 上传 `sources/`、`scripts/`、`logo.png`，但默认跳过 `mp3/wav/m4a/ogg` |
| 4 | 覆盖服务器上的代码文件，但不覆盖 `data/ielts_local.db`，也不清空服务器本地音频目录 |
| 5 | 重写并重启 `ielts` systemd 服务 |
| 6 | 重写 Nginx 反向代理配置 |
| 7 | 检查 `/api/health` 和主站页面 |

```powershell
python scripts/deploy.py
```

修复 2026-07-10 之前由重复上报产生的测试会话、重复学习会话和未完成阅读测试记录时，使用：

```powershell
python scripts/deploy.py --repair-tracking-data
```

该参数会在远程代码和数据库目录完成整站备份后，停止 `ielts` 服务，运行一次性数据修复，再由部署流程重启服务。修复脚本还会在数据库同目录保留一份带时间戳的 `.bak` 副本。

首次部署或需要补齐系统依赖时：

```powershell
python scripts/deploy.py --provision
```

只有明确要用本地数据库替换线上数据库时，才使用：

```powershell
python scripts/deploy.py --include-data
```

## 音频文件

音频文件只在本地或服务器本地维护，不提交到 GitHub，也不随默认部署包上传。

| 本地路径 | 线上对应路径 | 说明 |
|---|---|---|
| `sources/tinglidanciceshi/audio/` | `/var/www/ielts/sources/tinglidanciceshi/audio/` | 听力1000词（`words/`）与听力基础词汇（`basic_words/`）音频 |
| `sources/daanjutingxie/A听力答案句/` | `/var/www/ielts/sources/daanjutingxie/A听力答案句/` | 答案句听写音频 |
| `sources/P4gendu/C4T1S4.mp3` | `/var/www/ielts/sources/P4gendu/C4T1S4.mp3` | P4 跟读学习音频 |
| `sources/P4genduceshi/C4T1S4.mp3` | `/var/www/ielts/sources/P4genduceshi/C4T1S4.mp3` | P4 跟读测试音频 |

服务器需要音频时，部署后用 SFTP、`scp` 或 `rsync` 单独同步到上述相对路径。代码部署脚本会保留服务器已有音频目录；如果服务器没有这些文件，相关页面会使用浏览器 TTS 或外部音频地址作为兜底，具体取决于模块实现。

## 回滚

服务器备份文件位于 `/root/ielts_backups/`，格式类似：

```text
/root/ielts_backups/ielts_YYYYMMDD_HHMMSS.tar.gz
```

回滚示例：

```bash
systemctl stop ielts
rm -rf /var/www/ielts
tar -xzf /root/ielts_backups/ielts_YYYYMMDD_HHMMSS.tar.gz -C /var/www
chown -R www-data:www-data /var/www/ielts
systemctl start ielts
systemctl restart nginx
```

## 验收清单

| 检查项 | 命令或入口 | 预期 |
|---|---|---|
| 服务状态 | `systemctl is-active ielts nginx` | 均为 `active` |
| API 健康检查 | `curl http://127.0.0.1:49182/api/health` | 返回 `ok: true` |
| 学生端 | `/tinglidanciceshi/` | 页面正常打开 |
| 教师端 | `/tinglidanciceshi/?role=teacher` | 教师登录页正常打开 |
| 数据保护 | 检查 `/var/www/ielts/data/ielts_local.db` | 数据库未被无意覆盖 |
