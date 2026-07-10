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

---

# 排查发现

## 当前任务

| 项目 | 内容 |
|---|---|
| 目标 | 修复阅读时长、学生学习进度和历史记录，并推送、覆盖部署、线上验证 |
| 主分支 | `main`，当前与 `origin/main` 一致 |
| 技术栈 | Python 本地/API 服务 + 静态 HTML/JavaScript 多模块 |
| 主要入口 | `sources/tinglidanciceshi/index.html`、`scripts/local_server.py` |
| 部署资料 | `scripts/deploy.py`、`DEPLOY.md`、`docs/deployment-migration.md` |

## 待补充发现

后续按模块记录事件上报、数据库写入、聚合查询和页面渲染的实际问题及修复依据。

## 用户截图证据

| 页面 | 现象 | 初步核对方向 |
|---|---|---|
| 教师后台 → 学习进度 → 阅读同义替换详情 | 顶部“本模块学习时长”为 `16分43秒`，与汇总表该模块“学习时长”完全一致；同页显示测试 21 次、最高分 11% | 检查模块详情是否把学习/测试会话混合累计，是否因重复上报或历史数据兼容导致时长偏大 |
| 汇总表 | 多个模块即使测试次数为 0，也显示“进行中”和学习时长 | 检查状态是否只依据时长判断，以及学生页面进度/历史是否把“打开过页面”等同于有效学习 |

## 已确认根因

| 问题 | 代码证据 | 线上数据证据 | 结论 |
|---|---|---|---|
| 测试时长混入学习时长 | `saveModuleTestRecord()` 把测试同时写入 `study_sessions(session_kind='test')`；所有学习时长汇总未过滤 `session_kind` | 学生 `2025001` 的阅读同义替换：学习 `394秒` + 测试会话 `609秒` = `1003秒`，正好是截图的 `16分43秒` | 学习时长应只统计 `study`；正确阅读学习时长应为 `6分34秒` |
| 听力1000词同样被混算 | 学生/教师汇总复用相同未过滤逻辑 | 听力学习 `427秒` + 测试 `251秒` = 截图的 `11分18秒` | 正确学习时长应为 `7分7秒` |
| 听力学习累计值可能重复上报 | `listening.html` 的完成组、返回分组、卸载都会发送累计 `totalSeconds`，主站每次均追加一条 | 本地数据存在同模块多条学习会话；代码无法区分累计值与增量值 | 需要把听力上报改为增量并处理 `requestSave` |
| 学生历史类型标注错误 | `loadStudentHistory()` 仅把 `random` 标为随机测试，其余全部标为“错题测试” | 通用模块使用 `test_type='module_test'` | 阅读/写作/长难句等模块测试在学生历史中会被误标为错题测试 |
| 学生历史缺少模块上下文 | 历史列表未展示 `module_name/module_type`，图表混合所有模块 | 多模块测试共用同一历史页 | 学生无法判断某条分数属于哪个模块 |
| 学生标签切换依赖隐式全局事件 | `switchStudentTab(tab)` 使用未传入的 `event.target`；从表格“历史”按钮调用时会把按钮误设为 active | 浏览器兼容性和选中状态不稳定 | 改为显式事件或按 tab 名定位标签 |

## 本地浏览器回归

| 验证项 | 数据条件 | 结果 |
|---|---|---|
| 教师汇总阅读时长 | 学生 `2025003` 有阅读学习 `12秒`、测试会话 `27秒` | 页面只显示 `12秒`，未再显示混合值 `39秒` |
| 教师详情阅读时长 | 同上 | 顶部“本模块学习时长”和表格均为 `12秒` |
| 学生进度 | 同一数据库副本 | 阅读同义替换行显示 `12秒`，测试次数仍独立显示为 6 次 |
| 学生历史类型 | 6 条 `module_test` | 显示“阅读同义替换 / 模块测试”，不再误标“错题测试” |
| 学生历史标签 | 从学习进度切换到历史 | `history` 标签正确获得 `active`，无隐式全局 `event` 依赖 |
| 浏览器异常 | Playwright `pageerror` | 0 个 |

截图：`teacher-tracking-fixed.png`、`student-history-fixed.png`。

## 线上部署与回归

| 项目 | 结果 |
|---|---|
| 目标服务器 | `47.103.199.114`，部署目录 `/var/www/ielts`，服务端口 `49182` |
| 整站备份 | `/root/ielts_backups/ielts_20260710_164003.tar.gz` |
| 数据库副本 | `/var/www/ielts/data/ielts_local.db.tracking_fix_20260710_164010.bak` |
| 清理结果 | 测试镜像会话 12 条、双写学习会话 7 条、未完成/重复阅读测试 26 条 |
| 阅读同义替换 | 学生 `2025001`：学习时长 `5分18秒`、有效测试 1 次、最高分 11% |
| 听力1000词 | 学习时长从混合值修正为 `5分51秒`，测试时长保留在历史记录中 |
| 学生历史 | 仅剩有效记录；显示“听力1000词/随机测试”和“阅读同义替换/模块测试” |
| 服务状态 | `ielts`、`nginx` 均为 active；内网健康检查和主站均返回 200 |
| 浏览器回归 | 教师汇总/详情、学生进度/历史全部通过，`pageerror` 为 0 |

线上截图：`online-teacher-tracking-fixed.png`、`online-student-history-fixed.png`（验证后未纳入 Git）。

## GitHub 状态

本地提交为 `4c03ae2 Fix learning time and student history tracking`。当前 GitHub CLI 账号 `baifagg` 对远端 `raysu672-glitch/ielts-practice-platform` 无写权限，推送返回 403；本机未发现仓库所有者凭据或可用 GitHub SSH Key。
