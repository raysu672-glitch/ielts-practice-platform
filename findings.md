# 项目发现记录

## 本地目录

| 项目 | 结果 |
|---|---|
| 工作目录 | `F:\PythonTools\雅思练习` |
| Git 状态 | 不是 Git 仓库 |
| 本地文件 | `基础训练网站.xlsx` |
| 源码目录 | 未发现 |

## Excel 模块清单

| 科目 | 学习库 | 学习页面 | 测试库 | 测试页面 |
|---|---|---|---|---|
| 听力单词 | `https://github.com/raysu672-glitch/tinglidanciceshi` | `https://raysu672-glitch.github.io/tinglidanciceshi/` | 有 | 有 |
| 同义替换 | `https://github.com/raysu672-glitch/tongyitihuan` | `https://raysu672-glitch.github.io/tongyitihuan/` | `https://github.com/raysu672-glitch/tongyitihuanceshi` | `https://raysu672-glitch.github.io/tongyitihuanceshi/` |
| 写作词伙 | `https://github.com/raysu672-glitch/xiezuocihuo` | `https://raysu672-glitch.github.io/xiezuocihuo/` | `https://github.com/raysu672-glitch/xiezuocihuoceshi` | `https://raysu672-glitch.github.io/xiezuocihuoceshi/` |
| P4跟读 | `https://github.com/raysu672-glitch/P4gendu` | `https://raysu672-glitch.github.io/P4gendu/` | `?` | 空 |
| 长难句 | `https://github.com/raysu672-glitch/-` | `https://raysu672-glitch.github.io/-/` | `https://github.com/raysu672-glitch/changnanjuceshi` | `https://raysu672-glitch.github.io/changnanjuceshi/` |
| 答案句听写 | `https://github.com/raysu672-glitch/daanjutingxie` | `https://raysu672-glitch.github.io/daanjutingxie/` | `https://github.com/raysu672-glitch/daanjutingxieceshi` | `https://raysu672-glitch.github.io/daanjutingxieceshi/` |
| 句子翻译 | `https://github.com/raysu672-glitch/juzifanyixin` | `https://raysu672-glitch.github.io/juzifanyixin/` | `?` | 空 |

## 初步判断

| 事项 | 判断 |
|---|---|
| 现有形态 | 多个静态 GitHub Pages 模块，而不是单一仓库 |
| 关键改造点 | 需要统一身份、进度、时长、测试记录和教师查询能力 |
| 文档重点 | 记录现有前台页面结构和组件作用，供后续 agent 做视觉优化 |

## 实现发现

| 项目 | 结果 |
|---|---|
| 主站数据入口 | `sources/tinglidanciceshi/index.html` 是学生端、教师端、模块 iframe 容器和 Supabase 统一入口 |
| 本地数据库 | 已新增 SQLite API 服务，主站优先连接同域 `/api/db`，Supabase 只作为备用 |
| 学习时长 | 适合统一落到 `study_sessions`，用 `module_type`、`session_kind`、`duration_seconds` 支持学习、测试、每日汇总 |
| 测试记录 | 适合统一落到 `test_records`，外部测试页通过 `postMessage` 上报，主站计算达标线并写库 |
| 教师端查询 | 原逻辑把非听力模块和听力测试混用，已改为按 `module_type` 过滤 |
| 音频问题 | `daanjutingxie/index.html` 原逻辑只按固定 hostname 切换音频路径，迁移到客户服务器后容易无声；已改为多路径候选和 TTS 回退 |
| 页面规范 | 复扫 `sources/` 未发现 emoji 和常见符号化 emoji 实体 |

## 源码获取

| 项目 | 结果 |
|---|---|
| 获取方式 | `git clone` 失败后改用 GitHub zip 下载 |
| 本地目录 | `sources/` |
| 已获取模块 | `tinglidanciceshi`、`tongyitihuan`、`tongyitihuanceshi`、`xiezuocihuo`、`xiezuocihuoceshi`、`P4gendu`、`changnanju`、`changnanjuceshi`、`daanjutingxie`、`daanjutingxieceshi`、`juzifanyixin` |
| 特殊情况 | `xiezuocihuo` 使用 `master` 分支；`daanjutingxie` 第一次下载失败，重试 `main` 成功；长难句仓库名为 `-`，本地目录命名为 `changnanju` |
