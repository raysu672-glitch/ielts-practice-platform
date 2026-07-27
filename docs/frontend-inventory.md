# 前台页面与组件清单

本文档只记录当前前台页面、版块、组件、作用和数据流，供后续前端优化 agent 接手使用；不包含新的视觉设计方案。

## 主站入口

| 页面/版块 | 文件 | 主要作用 | 关键组件 | 数据与交互 |
|---|---|---|---|---|
| 身份选择页 | `sources/tinglidanciceshi/index.html` | 学生入口、教师入口分流 | `entryScreen`、学生入口按钮、教师入口按钮 | `?role=teacher` 或 `#teacher` 直达教师登录；默认尝试恢复学生 7 天登录态 |
| 学生登录页 | `sources/tinglidanciceshi/index.html` | 学生用学号和密码登录 | `studentLoginScreen`、学号输入、密码输入、登录按钮 | 查询 Supabase `students`；登录成功后写入 7 天本地登录态 |
| 教师登录页 | `sources/tinglidanciceshi/index.html` | 教师后台入口 | `teacherLoginScreen`、教师密码输入、确认按钮 | 当前使用页面内教师密码校验，成功后进入教师后台 |

## 学生端

| 页面/版块 | 文件 | 主要作用 | 关键组件 | 数据与交互 |
|---|---|---|---|---|
| 学生主页 | `sources/tinglidanciceshi/index.html` | 展示学生学习进度和历史记录入口 | `studentHome`、顶部学生信息、改密码、退出、学生页签 | 加载 `test_records`、`study_sessions`、`wrong_words` |
| 学习进度表 | `sources/tinglidanciceshi/index.html` | 按模块展示达标线、测试进度、学习时长、操作按钮 | `progressTable`、进度条、状态徽标、测试/学习/历史按钮 | 按 `module_type` 汇总测试最高分、达标次数、模块学习时长、总学习时长、今日学习时长 |
| 历史记录 | `sources/tinglidanciceshi/index.html` | 查看学生测试记录和错题历史 | `studentTabHistory`、`historyChart`、`studentHistoryList` | 查询学生自己的 `test_records` 和 `wrong_words` |
| 听力1000词测试 | `sources/tinglidanciceshi/index.html` | 本页内完成听写随机测试/错题测试 | `testScreen`、进度条、题号、计时、答案输入、提交、跳过 | 完成后写入 `test_records`，同时写入 `study_sessions` 的 `session_kind='test'` |
| 听力1000词学习 | `sources/tinglidanciceshi/listening.html` 嵌入主站 iframe | 四阶段单词学习 | 阶段指示器、组选择、听写区、拼写区、重测区、结果区 | 通过 `postMessage` 上报 `listeningStudyComplete` 或 `listeningStudyTime`，主站写入 `study_sessions` |
| 外部模块容器 | `sources/tinglidanciceshi/index.html` | 嵌入阅读、写作、长难句、听力同义替换等模块 | `genericScreen`、`genericIframe`、返回按钮 | 打开时追加 `student_id`、`module_type`、`module_name`、`mode` 参数；接收 `genericStudyComplete` 和 `genericTestComplete` |

## 教师端

| 页面/版块 | 文件 | 主要作用 | 关键组件 | 数据与交互 |
|---|---|---|---|---|
| 教师后台框架 | `sources/tinglidanciceshi/index.html` | 教师端主界面 | `teacherDashboard`、顶部标题、退出按钮、四个页签 | 页签包括学生管理、测试记录、学习进度、达标标准 |
| 学生管理 | `sources/tinglidanciceshi/index.html` | 添加、导入、导出、禁用、重置学生 | `tabStudents`、添加学生、批量导入、导出按钮、学生表格 | 读写 Supabase `students` |
| 测试记录 | `sources/tinglidanciceshi/index.html` | 按学生筛选并查看测试记录 | `tabRecords`、学生筛选下拉、记录表格 | 查询 `test_records`，显示模块、类型、时间、用时、正确率、达标状态 |
| 学习进度 | `sources/tinglidanciceshi/index.html` | 教师查询各学生模块进度和时长 | `tabProgress`、模块选择、学生搜索、进度汇总表、学生详情表 | 按 `module_type` 汇总 `test_records` 和 `study_sessions`；详情页展示每日模块时长和每日总时长 |
| 达标标准 | `sources/tinglidanciceshi/index.html` | 管理各模块 6/6.5/7 分目标达标线 | `tabStandards`、标准输入框 | 读写 `pass_standards` |

## 外部学习模块

| 模块 | 文件 | 学生端作用 | 主要组件 | 当前接入方式 |
|---|---|---|---|---|
| 阅读同义替换学习 | `sources/tongyitihuan/index.html` | 同义词组学习练习 | 词组练习区、进度、反馈、完成区 | iframe 打开；通过 `genericStudyComplete` 或主站兜底时长写入学习记录 |
| 写作词伙学习 | `sources/xiezuocihuo/index.html` | 写作词伙分类学习 | 分类、词伙卡片、练习流程 | iframe 打开；未主动上报时由主站按 iframe 打开时长兜底 |
| 长难句学习 | `sources/changnanju/index.html` | 长难句结构学习 | 句子展示、分析内容、练习区 | iframe 打开；由主站按 iframe 打开时长记录 |
| 答案句听写学习 | `sources/daanjutingxie/index.html` | 听力答案句原句播放和同义替换练习 | 组选择、音频播放、选项、反馈、结果页 | iframe 打开；音频优先使用本地/部署路径，失败回退 TTS |
| 写作句子翻译学习 | `sources/juzifanyixin/index.html` | 写作句子翻译练习 | 翻译题、答案区、反馈区 | iframe 打开；由主站按 iframe 打开时长记录 |
| P4 跟读学习 | `sources/P4gendu/index.html` | 听力 P4 跟读倍速训练 | 音频、跟读控制、倍速控制 | iframe 打开；由主站按 iframe 打开时长记录 |

## 外部测试模块

| 模块 | 文件 | 学生端作用 | 主要组件 | 测试上报 |
|---|---|---|---|---|
| 阅读同义替换测试 | `sources/tongyitihuanceshi/index.html` | 无提示同义替换测试 | 词网格、计时、组完成区、结果页 | 完成后发送 `genericTestComplete`，模块为 `reading_synonym` |
| 写作词伙测试 | `sources/xiezuocihuoceshi/index.html` | 20 题英文拼写测试 | 中文题干、输入框、结果表 | 完成后发送 `genericTestComplete`，模块为 `writing_phrase` |
| 长难句测试 | `sources/changnanjuceshi/index.html` | 5 句结构填空测试 | 句子卡片、填空、检查、结果详情 | 完成后发送 `genericTestComplete`，模块为 `sentence` |
| 听力同义替换测试 | `sources/daanjutingxieceshi/index.html` | 10 题答案句同义替换选择测试 | 题干、选项、结果详情 | 完成后发送 `genericTestComplete`，模块为 `listening_synonym` |
| 听力 P4 跟读测试 | `sources/P4genduceshi/index.html` | 跟读整段音频并上传 ASR 评分 | 开始测试、进度条、分数、录音回放 | 完成后发送 `genericTestComplete`，模块为 `listening_p4_speed` |

## 数据表对应关系

| 前台行为 | 数据表 | 关键字段 |
|---|---|---|
| 学生登录 | `students` | `student_id`、`password`、`status`、`target_score` |
| 学习会话 | `study_sessions` | `student_id`、`module_type`、`module_name`、`session_kind`、`duration_seconds`、`created_at` |
| 测试完成 | `test_records` | `student_id`、`module_type`、`module_name`、`score`、`pass_threshold`、`is_passed`、`duration_seconds` |
| 听写错题 | `wrong_words` | `student_id`、`word`、`wrong_count`、`correct_streak`、`is_mastered` |
| 模块达标线 | `pass_standards` | `module_type`、`module_name`、`score_6`、`score_6_5`、`score_7` |
