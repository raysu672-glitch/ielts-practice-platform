# 雅思练习平台需求实现方案

## 目标与边界

| 项目 | 处理方式 |
|---|---|
| 学习进度对库 | 主站优先读写本地 SQLite API，学习记录进入 `study_sessions` |
| 测试进度对库 | 各测试模块通过 `postMessage` 上报，主站统一写入 `test_records` |
| 学习时长 | 记录本次时长、模块总时长、总学习时长、每日模块时长、每日总时长 |
| 教师端查询 | 教师端按模块查看测试成绩、达标线、达标次数、学习时长和每日时长 |
| 音频问题 | 答案句听写音频改为多路径尝试，失败后回退 TTS |
| 教师端入口 | 支持 `/tinglidanciceshi/?role=teacher` 或 `#teacher` 直达教师登录 |
| 学生端免登录 | 学生登录后本地缓存 7 天，退出时清除 |
| 页面调整 | 不大改原前台设计，只做必要功能接入和无 emoji 清理 |

## 数据库方案

当前本地实现使用 `scripts/local_server.py` 提供 SQLite API，数据库文件为 `data/ielts_local.db`。前端仍保留 Supabase 备用配置，但在同域 `/api/db` 可用时优先使用本地数据库。

| 表/视图 | 作用 | 关键字段 |
|---|---|---|
| `students` | 学生账号、目标分数和状态 | `student_id`、`name`、`password`、`target_score`、`status` |
| `pass_standards` | 各模块按目标分数配置达标线 | `module_type`、`module_name`、`score_6`、`score_6_5`、`score_7` |
| `test_records` | 所有模块测试记录 | `module_type`、`score`、`pass_threshold`、`is_passed`、`duration_seconds` |
| `study_sessions` | 学习时长明细；旧数据中的 `test` 会话不参与任何学习时长汇总 | `module_type`、`session_kind`、`duration_seconds`、`created_at` |
| `wrong_words` | 听力1000词错词 | `word`、`wrong_count`、`correct_streak`、`is_mastered` |
| `daily_module_study_time` | 每日每模块学习时长汇总 | `student_id`、`study_date`、`module_type`、`duration_seconds` |
| `daily_total_study_time` | 每日总学习时长汇总 | `student_id`、`study_date`、`duration_seconds` |
| `student_module_test_summary` | 学生模块测试汇总 | `best_score`、`avg_score`、`passed_count` |

## 前端数据流

| 流程 | 数据流 |
|---|---|
| 学生登录 | `students` 校验成功后写入 `localStorage`，有效期 7 天 |
| 学生进入主页 | 查询 `test_records`、`study_sessions`、`wrong_words`，按 `module_type` 聚合 |
| 主站内听力测试 | 测试完成后调用 `saveModuleTestRecord()`，测试成绩和测试时长只写入 `test_records` |
| iframe 学习模块 | 主站打开 iframe 时追加学生和模块参数；模块按增量上报，关闭时等待子页保存，未上报模块再由主站兜底 |
| iframe 测试模块 | 只有完成测试并发送 `completed: true` 的 `genericTestComplete` 才写入 `test_records` |
| 学生/教师学习时长 | 统一只聚合 `study_sessions.session_kind='study'`；空值按旧版学习会话兼容 |
| 学生历史 | 显示模块名称、测试类型、测试时长和可用错题详情，模块测试不再误标为错题测试 |
| 教师端进度 | 测试统计按 `test_records.module_type` 聚合，学习时长按过滤后的学习会话聚合 |

## 模块编码

| 模块 | `module_type` | 学习页 | 测试页 |
|---|---|---|---|
| 听力1000词 | `dictation` | `tinglidanciceshi/listening.html` | 主站内置测试 |
| 听力基础词汇 | `listening_basic` | `tinglidanciceshi/listening_basic.html` | 主站内置测试（同听力1000词逻辑） |
| 阅读同义替换 | `reading_synonym` | `tongyitihuan/index.html` | `tongyitihuanceshi/index.html` |
| 写作词伙 | `writing_phrase` | `xiezuocihuo/index.html` | `xiezuocihuoceshi/index.html` |
| 长难句分析 | `sentence` | `changnanju/index.html` | `changnanjuceshi/index.html` |
| 听力同义替换 | `listening_synonym` | `daanjutingxie/index.html` | `daanjutingxieceshi/index.html` |
| 写作句子翻译 | `writing_translate` | `juzifanyixin/index.html` | 暂无 |
| 听力P4跟读倍速 | `listening_p4_speed` | `P4gendu/index.html` | `P4genduceshi/index.html` |

## 已实现文件

| 文件 | 改动 |
|---|---|
| `sources/tinglidanciceshi/index.html` | 统一学习/测试保存函数、学生 7 天免登录、教师入口、教师端模块统计、iframe 参数和消息处理 |
| `sources/tinglidanciceshi/local_db_client.js` | 本地 SQLite API 前端适配器，兼容 `db.from(...).select/insert/update` 调用 |
| `sources/tinglidanciceshi/tracking_utils.js` | 学习会话过滤、时长汇总、历史类型和详情解析公共函数 |
| `scripts/local_server.py` | 本地静态文件服务和 SQLite API，适合 Debian 部署 |
| `scripts/repair_tracking_data.py` | 一次性清理旧版测试镜像会话、双写学习会话和阅读测试退出重复记录 |
| `sources/tinglidanciceshi/supabase_schema.sql` | 扩展测试记录、学习时长、模块汇总和每日时长视图 |
| `sources/tongyitihuanceshi/index.html` | 阅读同义替换测试完成上报 |
| `sources/xiezuocihuoceshi/index.html` | 写作词伙测试完成上报 |
| `sources/changnanjuceshi/index.html` | 长难句测试完成上报 |
| `sources/daanjutingxieceshi/index.html` | 听力同义替换测试完成上报，结果页去除 emoji |
| `sources/P4gendu/index.html` | 听力 P4 跟读学习 |
| `sources/P4genduceshi/index.html` | 听力 P4 跟读测试完成上报；依赖 `config.js` 中的 ASR 后端 |
| `docs/frontend-inventory.md` | 前台页面、版块、组件、作用清单 |
| `docs/deployment-migration.md` | 服务器迁移、Supabase、域名和验收说明 |

## 上线前配置项

| 配置项 | 位置 | 说明 |
|---|---|---|
| SQLite 数据库 | `data/ielts_local.db` | 本地服务首次启动自动创建；上线前确认数据备份策略 |
| 服务端口 | `scripts/local_server.py` | 默认建议由 Nginx 反向代理到 `49182` |
| Supabase URL | `window.IELTS_SUPABASE_URL` | 备用配置；仅在不用本地 SQLite API 时按运行环境注入 |
| Supabase Key | `window.IELTS_SUPABASE_KEY` | 备用配置；仅在不用本地 SQLite API 时按运行环境注入，不写入仓库 |
| 教师密码 | `verifyTeacherPassword()` | 当前仍为页面内静态密码，生产可改为读取 `teacher_config` |
| 域名 | Nginx 或客户服务器面板 | 将域名指向静态站目录 |
| HTTPS | Nginx 或客户服务器面板 | 配置证书并强制 HTTPS |

## 变更历史

### 2026-07-10 - 学习时长与学生历史口径修复

| 项目 | 内容 |
|---|---|
| 变更内容 | 学习时长排除测试会话；测试时长保留在测试记录；修复 iframe 重复/累计上报、未完成阅读测试计数、学生历史类型和标签切换 |
| 变更理由 | 线上截图中的阅读 `16分43秒` 实际是学习 `394秒` 与测试会话 `609秒` 的混合值，且 21 次测试包含退出页产生的重复记录 |
| 影响范围 | 学生进度、学生历史、教师进度汇总/详情、听力/阅读/写作模块上报、部署数据修复 |
| 安全边界 | 主站只接受同源且来自当前 iframe 的消息，并以当前登录学生和当前模块为准，不信任子页传入的学生或模块标识 |
