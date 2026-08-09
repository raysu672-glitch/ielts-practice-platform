# 听力1000词 / 听力基础词汇与主站

本目录是平台主入口，包含学生登录、教师后台、听力1000词与听力基础词汇学习/测试、SQLite/Supabase 数据适配和外部模块 iframe 容器。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 主站、学生端、教师端、测试流程、外部模块接入 |
| `listening.html` | 听力1000词分组学习页 |
| `listening_basic.html` | 听力基础词汇分组学习页（逻辑同听力1000词） |
| `dictation-test.html` | 独立听写测试页，保留兼容 |
| `local_db_client.js` | 将前端原 Supabase 调用适配到同域 `/api/db` |
| `supabase_schema.sql` | Supabase 备用建表脚本 |
| `logo.png` | 主站品牌图 |
| `audio/words/` | 听力1000词单词音频，本地/服务器本地维护，不提交 GitHub |
| `audio/basic_words/` | 听力基础词汇单词音频，本地/服务器本地维护，不提交 GitHub |

## 数据关系

| 行为 | 数据表 |
|---|---|
| 学生登录、改密码 | `students` |
| 听力测试结果 | `test_records` |
| 学习时长和测试时长 | `study_sessions` |
| 错词记录 | `wrong_words`、`word_mastery` |
| 教师端达标线 | `pass_standards` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 模块配置 | 外部模块入口和 `module_type` 在 `index.html` 内集中维护 |
| 本地数据库 | 优先请求 `/api/db`，不可用时才回退 Supabase |
| 音频资源 | `audio/` 目录被 `.gitignore` 排除；服务器需要音频时单独同步 |
| 教师入口 | 使用 `/tinglidanciceshi/?role=teacher` |
| 验证方式 | 修改后访问学生端、教师端、`/api/health`，并完成一次测试记录写入 |
