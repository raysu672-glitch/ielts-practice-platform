# 服务器迁移与域名配置文档

本文档用于将当前雅思练习平台迁移到客户公司 Debian 服务器，并配置域名正常访问。项目当前是静态 HTML/JS/CSS 多模块站点，数据本地使用 SQLite；如以后继续使用 Supabase，可保留原 Supabase 配置作为备用。

## 交付目录

| 路径 | 说明 |
|---|---|
| `sources/tinglidanciceshi/` | 主站、学生端、教师端、听力1000词学习/测试、数据库 SQL |
| `sources/tongyitihuan/` | 阅读同义替换学习 |
| `sources/tongyitihuanceshi/` | 阅读同义替换测试 |
| `sources/xiezuocihuo/` | 写作词伙学习 |
| `sources/xiezuocihuoceshi/` | 写作词伙测试 |
| `sources/changnanju/` | 长难句学习 |
| `sources/changnanjuceshi/` | 长难句测试 |
| `sources/daanjutingxie/` | 听力同义替换/答案句听写学习，包含音频目录 |
| `sources/daanjutingxieceshi/` | 听力同义替换测试 |
| `sources/juzifanyixin/` | 写作句子翻译学习 |
| `sources/P4gendu/` | 听力 P4 跟读 |
| `scripts/local_server.py` | 静态文件服务和 SQLite API |
| `data/ielts_local.db` | 本地 SQLite 数据库文件，首次启动自动创建；真实数据库不提交到 GitHub |
| 音频文件 | 只在本地或服务器本地维护，不提交 GitHub，不随默认部署包上传 |

## 推荐服务器目录结构

| 服务器路径 | 对应本地目录 | 访问路径 |
|---|---|---|
| `/var/www/ielts/tinglidanciceshi/` | `sources/tinglidanciceshi/` | `/tinglidanciceshi/` |
| `/var/www/ielts/tongyitihuan/` | `sources/tongyitihuan/` | `/tongyitihuan/` |
| `/var/www/ielts/tongyitihuanceshi/` | `sources/tongyitihuanceshi/` | `/tongyitihuanceshi/` |
| `/var/www/ielts/xiezuocihuo/` | `sources/xiezuocihuo/` | `/xiezuocihuo/` |
| `/var/www/ielts/xiezuocihuoceshi/` | `sources/xiezuocihuoceshi/` | `/xiezuocihuoceshi/` |
| `/var/www/ielts/changnanju/` | `sources/changnanju/` | `/changnanju/` |
| `/var/www/ielts/changnanjuceshi/` | `sources/changnanjuceshi/` | `/changnanjuceshi/` |
| `/var/www/ielts/daanjutingxie/` | `sources/daanjutingxie/` | `/daanjutingxie/` |
| `/var/www/ielts/daanjutingxieceshi/` | `sources/daanjutingxieceshi/` | `/daanjutingxieceshi/` |
| `/var/www/ielts/juzifanyixin/` | `sources/juzifanyixin/` | `/juzifanyixin/` |
| `/var/www/ielts/P4gendu/` | `sources/P4gendu/` | `/P4gendu/` |
| `/var/www/ielts/scripts/` | `scripts/` | 服务脚本 |
| `/var/www/ielts/data/` | `data/` | SQLite 数据库 |

主站建议访问地址为：

```text
https://客户域名/tinglidanciceshi/
https://客户域名/tinglidanciceshi/?role=teacher
```

## SQLite 本地数据库

| 步骤 | 操作 |
|---|---|
| 1 | 安装 Python 3 |
| 2 | 启动 `scripts/local_server.py` |
| 3 | 首次启动自动创建 `data/ielts_local.db` |
| 4 | 自动初始化 `students`、`pass_standards`、`test_records`、`study_sessions`、`word_mastery`、`wrong_words` |
| 5 | 自动创建测试学生 `2025001`，密码 `123456` |

本地启动命令：

```bash
python scripts/local_server.py --host 127.0.0.1 --port 49182 --static-dir sources --db data/ielts_local.db
```

Debian 服务器建议由 systemd 启动，并由 Nginx 反向代理到 Python 服务。

## Supabase 备用配置

如果客户后续要求继续使用 Supabase，可执行以下步骤：

| 步骤 | 操作 |
|---|---|
| 1 | 登录 Supabase 项目后台 |
| 2 | 打开 SQL Editor |
| 3 | 执行 `sources/tinglidanciceshi/supabase_schema.sql` |
| 4 | 替换主站里的 `SUPABASE_URL` 和 `SUPABASE_KEY` |

当前前端 Supabase 备用配置位于：

```text
sources/tinglidanciceshi/index.html
```

如需启用 Supabase 备用数据源，不要把真实 URL 和 key 写入仓库，可在页面加载前注入：

```js
window.IELTS_SUPABASE_URL = '...';
window.IELTS_SUPABASE_KEY = '...';
```

当前本地/服务器模式会优先连接同域 `/api/db` SQLite API，只有在没有本地 API 适配器且已提供上述 Supabase 配置时才会回退 Supabase。

## Nginx 反向代理配置示例

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://127.0.0.1:49182;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

配置 HTTPS 后建议将 80 跳转到 443。

## 域名配置

| 项目 | 配置 |
|---|---|
| DNS A 记录 | 将主域名或子域名指向客户服务器公网 IP |
| DNS CNAME | 如使用 CDN 或云厂商负载均衡，按厂商要求配置 |
| HTTPS 证书 | 使用客户证书或 Let's Encrypt |
| 访问入口 | 学生入口 `/tinglidanciceshi/`，教师入口 `/tinglidanciceshi/?role=teacher` |

## 上传与发布步骤

| 步骤 | 操作 |
|---|---|
| 1 | 在服务器创建 `/var/www/ielts` |
| 2 | 备份当前 `/var/www/ielts` |
| 3 | 上传 `sources/`、`scripts/`、`logo.png` 到 `/var/www/ielts/`，默认跳过音频文件 |
| 4 | 默认保留服务器 `data/ielts_local.db` 和服务器本地音频目录，不要用本地数据库覆盖线上数据 |
| 5 | 保持目录名与当前相对路径一致 |
| 6 | 如线上需要音频，单独用 SFTP、`scp` 或 `rsync` 同步服务器本地音频目录 |
| 7 | 启动或重启 `scripts/local_server.py` 对应的 systemd 服务 |
| 8 | 配置 Nginx 反向代理和 HTTPS |
| 9 | 用学生账号测试学习、测试、退出、7 天免登录 |
| 10 | 用教师入口查看测试记录、模块进度、每日时长 |

## 自动部署脚本

项目根目录提供 `scripts/deploy.py`，用于覆盖部署当前代码。脚本会先在服务器备份当前部署目录，再上传代码文件；默认不上传本地数据库，也不上传音频文件。

| 环境变量 | 说明 |
|---|---|
| `IELTS_DEPLOY_HOST` | 服务器地址 |
| `IELTS_DEPLOY_USER` | SSH 用户，默认 `root` |
| `IELTS_DEPLOY_PASSWORD` | SSH 密码；也可改用 `IELTS_DEPLOY_KEY` |
| `IELTS_DEPLOY_KEY` | SSH 私钥路径 |
| `IELTS_DEPLOY_DOMAIN` | 域名，默认 `training.oyenglish.com.cn` |
| `IELTS_DEPLOY_DIR` | 服务器部署目录，默认 `/var/www/ielts` |

```bash
python scripts/deploy.py
```

更多 GitHub 推送、备份、回滚和验收说明见项目根目录 `DEPLOY.md`。

## 音频本地维护策略

| 音频目录 | 维护方式 | 说明 |
|---|---|---|
| `sources/tinglidanciceshi/audio/` | 本地/服务器本地维护 | 听力1000词单词音频，不进入 GitHub |
| `sources/daanjutingxie/A听力答案句/` | 本地/服务器本地维护 | 答案句听写音频，不进入 GitHub |
| `sources/P4gendu/C4T1S4.mp3` | 本地/服务器本地维护 | P4 跟读音频，不进入 GitHub |

默认部署脚本会保留服务器已有音频目录。如果服务器缺少音频，页面会按模块逻辑使用 TTS 或外部音频地址兜底；需要原始音频体验时，部署后手动同步上述音频路径。

## 上线验收清单

| 检查项 | 预期结果 |
|---|---|
| 学生登录 | 正常进入学生主页 |
| 学生免登录 | 登录后 7 天内再次访问自动进入学生主页 |
| 学生退出 | 退出后不再自动登录 |
| 教师入口 | `?role=teacher` 直接显示教师登录 |
| 添加学生 | 教师端添加学生成功，新学生初始密码为 `123456` |
| 听力1000词测试 | 生成 `test_records` 和 `study_sessions` |
| 外部测试模块 | 阅读同义替换、写作词伙、长难句、听力同义替换测试都写入 `test_records` |
| 学习时长 | 学习页关闭后写入 `study_sessions` |
| 教师进度 | 可按模块查看最高分、测试次数、达标次数、模块总时长、今日模块时长 |
| 学生详情 | 可查看每日模块时长和每日总时长 |
| 音频播放 | 答案句听写优先播放音频文件，失败时回退 TTS |
| 页面符号 | 页面无 emoji |
