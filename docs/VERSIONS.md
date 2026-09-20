# 版本记录

## 判分放宽：写作翻译改「规则四径」+ 词伙答案支持「多写法」（2026-09-20 第五次修订）

学生反馈：「阶段测试过不去」这条查下去，除了重测次数和阶段测排法，
**判分本身**也是元凶。线上数据里有两类题是「数学上过不去」的：

### 一、写作句子翻译：逐字全等 → 规则四径（`juzifanyixinceshi`）

旧实现 `isChineseMatch()` 是「去标点与空格后**逐字全等**」。可这题的题型是
**看英文写中文**，学生必须把参考译文一字不差默写出来才算对——换个说法
（哪怕意思完全正确）一律 0 分。线上 11 次提交，11 次 0.0 分。

新实现 `gradeChinese()` 走四道闸，全过才算对：

| 闸 | 口径 | 治什么 |
| --- | --- | --- |
| ① 内容覆盖 | `bag 命中字符 / 参考长度 ≥ 0.75` | 漏译、只写半句 |
| ② 语序一致 | `LCS / bag 命中 ≥ 0.85` | 词都对但语序颠倒 |
| ③ 逻辑关系 | 参考里的连接词，答案里必须有同组词（因为≈由于、所以≈因此…） | 把因果/转折关系丢了 |
| ④ 关键信息 | 参考里的数字、百分比、英文专名必须出现 | 漏掉硬信息点 |

外加长度比下限 `≥ 0.6`，防止「只写开头几个字」靠内容覆盖蒙分。

判错时前端会把 `reasons` 逐条显示给学生（「内容覆盖只有 52%，漏译较多」
「少了逻辑关系词：因为」），而不是只丢一句「不正确」。

**已知边界（产品已确认接受）**：细粒度语法（缺「的/了/着」、量词错、搭配错）
和幅度较大的同义改写，规则法既挡不住也放不过；语序颠倒、漏译、逻辑丢失能挡住。
本次不接 AI 判分。

### 二、词伙答案：`/` 被当成唯一答案 → 拆成「多写法」（`xiezuocihuo*`）

题库里有 **11 条**用 `/` 表示「两种说法都行」：

```
climb steadily/solidly · continue to increase / soar · remain stable/steady
in the final phase/stage · curb crime / deter crime · consumer goods /products
digital/online dating · dip/drop to only 2.5% · a modest dip/drop over the last decade
be ethically wrong / theoretically wrong · the elderly / the senior population
```

数据没拆开，旧逻辑把整串当成唯一答案：「a/b」被规范化成「a b」，
学生写 a 或 b **都判错** —— 这些题永远拿不到分（线上 6 次 0 分提交）。

现在按 `/` 拆成多个可接受答案，**任一命中即算对**（纯放宽，不会误伤）：

- `climb steadily/solidly` → `climb steadily` / `climb solidly`
- `a modest dip/drop over the last decade` → `a modest dip over…` / `a modest drop over…`
- `consumer goods /products` → `consumer goods` / `consumer products`
- `be ethically wrong / theoretically wrong` → `be ethically wrong` / `be theoretically wrong`

展示也改了：`a/b` 渲染成「a 或 b」，学生一眼能看出两种说法都算对。

**实现方式**：这套 helper 原来在三个页面各抄了一份（词伙学习页、词伙测试页、
主站模块练习），这次**合并到 `sources/shared/phrase_answer.js`**，三处共用，
避免以后只改一处又留两个坑。`modules.js` 里不再有 `phraseXxx` 定义，
改为在页面里先引共享文件。

### 三、`listening_basic` 达标线：本轮**不动**

线上通过率也是 0%，但成因与上面两条不同（是达标线定得比学生实际分数高），
需要单独立项调参，本轮先按住不发布。

### 四、发布清单里的前端测试命令升级

`node tests/test_tracking_utils.js` → **`node tests/run_js_tests.js`**
（自动跑 `tests/` 下所有 `test_*.js`，本次新增
`test_writing_translate_match.js`、`test_phrase_multi_answer.js`）。

## 阶段测：不限重测次数 + 不算任务量 + 考挂只留测挂着（2026-09-20 第四次修订，第六次修订改口径）

学生反馈：「阶段测试过不去，他的任务也完成了，学不了了啊」。查下去发现是**三件事叠在一起**。

**第一件（已修）：每天 2 次的重测上限把学生锁死。**

`submit_stage_test` 里有一道 `attempts >= 2` 的拦截，考不过就直接抛
「今日重测次数已用尽，请联系助教」。对「本来就考不过」的学生，这是最坏的组合：
过不去、又不让再考。

- **删掉拦截**：阶段测**不限重测次数**，想考几次考几次，当天可连续重考。
- 常量 `STAGE_TEST_DAILY_ATTEMPTS`（=2）删除，换成
  **`STAGE_TEST_ATTENTION_FAILS`（=3）**，语义从「今天还能考几次」变成
  「累计考了几次还没过 → 提醒助教」。
- `stage_tests_pending` 不再返回 `attempts_left_today` / `retry_exhausted`，
  改为返回 `needs_attention`（累计提交次数 ≥3 且未过）。
- `_stage_retry_exhausted_count()` → `_stage_needs_attention_count()`：
  口径从「今天的 `test_attempt_count_today`」改成「`test_records` 的**累计**提交次数」——
  次数跨天归零，用当天计数根本看不出「反复考不过」。
- 教师端徽章 `重测用尽` → `多次未过`（tooltip 与明细弹窗文案同步改写）。
- 回归测试：`test_stage_test_retries_are_unlimited`（同一天连考 7 次全部接受）、
  `test_stage_needs_attention_is_flagged_not_red`（标记亮起但灯不变红）。

**第二件（已修）：阶段测**不算任务量**，不占装箱名额、不进完成率、不参与红黄灯。**

测过不了会一直挂在任务列表里。如果它还算完成率，这部分学生的「昨日任务」就**永远**
差一条：天天黄灯，严重点天天红灯——**怎么做都翻不了身**，指标反而失去了信号意义。

- **不占配额**：`_units_pack_picks` 里把阶段测从配额池里摘出来，单独成池。
  只要该科当天配额 > 0、且它覆盖的学习单元都学完（或今天一起派），测就**跟着一起派下去**，
  不再和学单元抢名额。以前 quota=1 时会出现「今天排测、明天才排学」的轮换。
- **不算任务量**：`day_task_progress()` 直接 `skip item_type='test'`——既不进分子也不进分母。
  `day_unfinished_count()`（积压）与 `_row_status_for_overview()`（红黄灯）共用它，自动同步。
- 连带效果：昨天**只**排了阶段测、学生没考 → 昨天 0/0 → 🟢（此前是 🔴）。
  测的欠账看「待通过阶段测」列，不再污染完成率。
- 回归测试：`test_day_unfinished_count_ignores_tests_and_residue`、
  `test_failed_stage_test_not_counted_as_backlog`、`test_test_only_day_stays_green`、
  `test_stage_test_missing_yesterday_keeps_row_green`。
  > **推翻了当天早些时候的第三次修订**（那份把测按普通任务计），见下节。

**第三件（已改口径）：「清单学完就没内容可学了」——只留测挂着，不重排科目任务。**

用探针 `scripts/_probe_stuck_test.py` 复现（quota=2，4 个学习单元 + 1 个覆盖前两单元的测）：

```text
08-10  学[单元1] 学[单元2]
08-11  测[U1–U2 阶段测] 学[单元3]      ← 测和新单元同时派出
08-12  测[U1–U2 阶段测] 学[单元4]
08-13  测[U1–U2 阶段测]               ← 学习全做完，从此每天只有这一条
08-14 ~ 08-23  测[U1–U2 阶段测]       ← 无限重复
```

关键结论：**不是阶段测挡住了学习**。学习单元还在时，测和新单元会同时派下去，
队列不会因为测没通过而停住。真正的原因是**清单里的学习单元全部做完、
系统没有更多内容可发**，测只是最后剩下的那一条。

**一度实现的解法（同日晚些时候废除）：考挂 → 把覆盖单元打回未完成强制重学。**

- 曾新增 `_schedule_restudy_for_failed_test()`：把覆盖单元置成
  `study_completed=0, need_refresh=1, refresh_reason='restudy'`，并 `restudy_count += 1`，
  学生端任务标题标**「需重学」**；另配 `RESTUDY_MAX_ROUNDS`（=3）轮数封顶。
  复用现成的 `need_refresh` 机制 —— **不新增清单条目**，不破坏「同一学生禁止重复 `unit_id`」（D26）。
- 还新增过 `_ensure_restudy_in_existing_daily()`：当天 `daily_tasks` 已锁定时把重学单元补进当天。

**为什么废除（第六次修订）**：30 天模拟显示这套机制把学生**钉在原地**，而不是解出来。

```text
dictation_u01~u03 各被自动重学 3 轮（正好撞上 RESTUDY_MAX_ROUNDS 封顶）
10-09 之后「新发学习」=0；学生每天在「重学同一批单元 + 十几条考挂的测」之间循环
停下原因固定是「时间不够（前 13 分钟，下一条要 35 分钟）」
```

学生本人的说法是同一个现象：「过不去 → 被排回来重学 → 又过不去」。
重学不是解法；**想再学，学生自己从「学习进度」里点对应模块的学习按钮就能进去**，
不需要系统替他重排科目任务。

**现在的口径**：

- 考挂**只把那条阶段测留在清单里**：`status='pending'`、`test_passed=0`、
  当天 `daily_tasks` 记 `done_fail`，不限次数重考；
- **科目任务不重排**：覆盖的学习单元保持 `study_completed=1`，不再被打回未完成；
- `_schedule_restudy_for_failed_test()`、`RESTUDY_MAX_ROUNDS`、
  `_ensure_restudy_in_existing_daily()` 一并删除；`restudy_count` 列与
  `_plan_progress().restudy_n` 保留为**历史字段**（兼容早期数据，正常恒为 0）；
- `_ensure_refresh_in_existing_daily()` 只服务「换题后当天插回今日」这一件事；
- 「考太多次还没过」继续由 `STAGE_TEST_ATTENTION_FAILS`（=3）+ 教师端「多次未过」徽章承载。
- 回归测试：`test_failed_stage_test_only_keeps_test_pending`、
  `test_failed_stage_test_does_not_add_rows_to_today`、
  `test_failed_test_leaves_titles_and_progress_clean`。
- 探针复验（`scripts/_sim_stage_test_board.py` 末段）：学习单元一旦打勾就不会再被排回来，
  末段只剩「测 测 测」——与「只留测挂着」的预期一致。

## 阶段测按普通任务一样计 + 「重测用尽」标记（2026-09-20 第三次修订）

> **整节已被第四次修订推翻**，保留只为追溯当时的判断：当时认为「昨天派了测没考、
> 看板却显示绿色」会误导助教，于是把测按普通任务计。实践证明代价更大——
> 考不过的学生从此永远完不成「昨日任务」。正确的做法是让测**不进完成率**，
> 由「待通过阶段测」列单独承载。

- **阶段测回归普通任务口径**：`day_task_progress()` 现在对 `item_type='test'` 单独判
  「完成」——`state='done_pass'` **或** `plan_items.test_passed=1` 都算做完；
  派了没考、考了没过（`test_passed` 仍为 0）都算没做完。
  `day_unfinished_count()`（积压）与 `_row_status_for_overview()`（红黄灯）共用它，
  两边不会再打架。
- **「重测用尽」独立标记**：新增常量 `STAGE_TEST_DAILY_ATTEMPTS = 2`（原先硬编码在
  `submit_stage_test` 里），并新增 `_stage_retry_exhausted_count()`。
  `class-overview` 多返回一个 `stage_test_retry_exhausted` 字段；
  `stage-tests` 明细每项多返回 `retry_exhausted`。
  教师端「待通过阶段测」列在有此项时显示红字 **`N 项 重测用尽`**，
  明细弹窗该行状态显示 **「今日已考 2 次仍未过」**。
  **它不影响红黄灯**——灯只看昨天；`重测用尽` 是「今天已经考不动了，请助教介入」的提示。
  > **已被第四次修订推翻**：重测上限干脆取消，标记改名为 `多次未过`；
  > 上面那条「阶段测按普通任务计」也一并推翻（改为不算任务量）。
- 回归测试：新增「阶段测失败仍算积压」「只排测的一天没做→红灯」「昨天全做完但今天
  两次没考过→绿 + `retry_exhausted=1`」，并把原先锁定旧行为的
  `test_day_unfinished_count_ignores_residue_and_tests` /
  `test_stage_tests_never_drive_red` 改成新口径。

## 修掉「配额 0 被静默改成 1」（2026-09-20）

`0` 是合法配额（表示当天不排这科），但代码里有多处用 `value or DEFAULT_UNITS_PER_DAY`
兜底——Python 里 `0` 是 falsy，于是 **`周中 0` 会被悄悄改成 `1`**，造成两个用户可见问题：

- **把某科从「仅周末」改回「周中也排」，改了没反应**：`_quotas_have_pending()` 判不出
  `0 → 1` 的差异，`_profile_has_real_pending()` 认为没有待生效变更，pending 永不应用，
  该科周中再也回不来。反向 `1 → 0` 同样漏判，且当天任务不重建。
- 新增 `_units_or_default()`：只在 `None` 时回落默认，`0` 原样保留（负数夹到 0）。

顺带确认并加锁：**「只排周末」（周中 0 / 周末 1）本来就是支持的**——界面配额输入
`min="0"`，后端 `max(0, ...)`。新增 3 个回归测试覆盖：只排周末可用、
`0 → 1` 能检测并应用、`1 → 0` 能检测并重建当天任务。

## 积压改为「昨天那批没做完的」+ 红黄灯只看昨天（2026-09-20）

学生反馈两轮：

1. 第一轮「当天任务都完成了，看板还显示积压」——根因是看板积压用的是**历史累计存量**
   （曾进过 daily 且至今未完成），把够不到配额的旧欠账、配额为 0 派不出去的死锁条目、
   一直考不过的阶段测都算了进去。
2. 第二轮澄清口径：**「今天的任务没做完是正常的，不该算积压」**——所以第一轮改成
   「当天没做完的条数」也不对，那样白天看一眼就永远是「有积压」。

- **看板积压口径**：`day_unfinished_count()` 只回看**昨天**一天。昨天派的任务里没做完的
  才算积压；昨天那批本身就含「前天积压过来的 carry_over」，所以只要昨天都做完了，
  积压必须为 0。已完成条目的残留 `todo` 行不计入。（阶段测的取舍见上方第三/第四次修订：
  先按普通任务计，后改为**不算任务量、不计入**。）
- **打包器口径不动**：`backlog_plan_item_ids()` 仍是「今天以前派过仍未完成」，
  只服务 carry_over 优先装箱。两个口径刻意分开，代码里已加注释说明。
- **红黄灯大简化，只剩两条规则**（`_row_status_for_overview`）：
  - 昨天有任务、**一条都没做** → 🔴
  - 昨天有任务、**做了一部分没做完** → 🟡
  - 昨天全做完 / 昨天没排任务 → 🟢
  原先的时段阈值（16:00 / 14:00 / 20:00 / 18:00）、完成率比例、积压条数、
  时长比例、换题重学、反复考不过、连续零完成、待生效排程**全部取消**，
  相关常量与 `_has_hard_test_fail` / `_test_fail_today_count` / `_ghost_zero_streak`
  三个判定函数一并删除。
  - 为什么改用「昨天」：今天的任务还在进行中，用它判红会整天误报；昨天已结束，
    做没做完是一锤定音的事实，不会随时间漂移，老师也不用等到下午才看到红灯。
- **阶段测当时不进积压、也不参与红黄灯**：新增 `stage_test_pending` 字段与
  「待通过阶段测」列，点击展开明细（模块、阶段测名、已考次数、最高分、是否考过）。
  新接口 `GET /api/task/students/<id>/stage-tests`。
  > **已被 2026-09-20 第三/四次修订覆盖**：先改为「按普通任务一样计」，
  > 再改为**不算任务量、不进完成率、不参与红黄灯**（见第四次修订）。
- **回归**：单测覆盖「昨天没做→红 / 做一半→黄 / 全做完→绿」，以及
  「昨天全做完时今天一条没做仍是积压 0」。

## 去掉每日任务的时间预计（2026-09-19）

既然装箱只按「按科每日单元配额」，分钟数不再约束任何东西，界面上的时间预计全部下线：

- 学生端「今日任务」：标题右侧只留「单元排程 · 今日 N 条 · 已练 X′」，每条任务只留「已练 X′」；
- 教师端「装箱预览」：改为「今日放出 N 条」，每条不再显示 `(X′)`；
- 教师端班级总览的学生卡片：`今日时长/配额` 改为 `今日已练`（去掉了无意义的配额分母）；
- 清掉了 `taskWeekdayMinutes` / `taskWeekendMinutes` 等已不存在的 DOM 引用与死代码。

后端仍返回 `est_total_minutes` / `budget_minutes`（兼容旧数据），前端不再渲染。

## 学生后续安排（2026-09-02）

学生「今日任务」页增加 **② 后续安排**：按日试算排程 + 全部待完成清单（只读，不预写未来 daily_tasks）。

## 任务单元库扩科（2026-09-02）

`seed_mvp_units` 补齐除作文批改外的已有科目单元：听力基础、听力同义、长难句、写作词伙、写作翻译、P4跟读、口语四子块；合计约 249 个任务单元。

## 班级任务看板（2026-09-02）

教师「任务计划」新增默认子页 **班级总览**：一屏看全班今日完成、积压、换题、测挂与计划进度；点行进入学生计划。接口 `GET /api/task/class-overview`（只读，不装箱）。

## 单元排程（2026-09-01）

在「时间任务」里程碑之上扩展 **双模式** 任务系统：

- **`time_budget`**（原默认，**已于 2026-09-19 下线**）：按周中/周末分钟预算装箱
- **`units_per_day`**（现唯一模式）：按科每日单元数排程，周中/周末两档配额

> **2026-09-19 更新**：按分钟装箱（`time_budget`）全部关闭，装箱只按「按科每日单元配额」。
> 周中/周末分钟仅作参考预算展示；老档案的 `pack_mode='time_budget'` 被忽略并强制按单元配额排程。

规格见 [`task-system-units-mode.md`](task-system-units-mode.md)。

## 时间任务（2026-09-01）

本地可还原里程碑：`git checkout 时间任务`（或 `git switch -c restore/时间任务 时间任务`）。

### 范围

任务系统（时间画像 + 每日装箱 + 学/测完成）本地可用版，主要包括：

- 教师：有序清单 / 生效清单、时长与生效日、装箱预览、阶段测、科目折叠与已完成灰显收起
- 学生：今日任务（已完成项仍全部展示）、计划进度 X/Y、同义替换任务防偷懒（须做完组数）
- 后端：`scripts/task_api.py`、相关 API 与 `tests/test_task_api.py`
- 规格文档：`docs/task-system-*.md`

### 不含

- 未纳入本标签：临时 `_*.txt`、线上 DB 备份目录、promo 视频、口语音频大批量未跟踪文件等

### 说明

当时阿里云仅已上线双 cookie 等更早提交；本里程碑含大量任务系统 WIP，**默认未推送远程**，需要时再单独 `git push` / `git push origin 时间任务`。
