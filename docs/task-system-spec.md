# 任务系统 · Agent 实施说明（定稿）

> **读者**：实现本功能的 Agent / 开发者  
> **产品流程与助教/学生/监控说明**：见 [`task-system-overview.md`](task-system-overview.md)  
> **助教班级总览线框**：见 [`task-system-teacher-dashboard-wireframe.md`](task-system-teacher-dashboard-wireframe.md)  
> **状态**：产品讨论定稿，可按本文直接设计表结构、API 与 UI  
> **更新日期**：2026-08-27  
> **仓库**：雅思练习平台（`sources/tinglidanciceshi` + `scripts/local_server.py` SQLite）  
> **原则**：未写明的细节按本文「默认取值」实现；禁止发明与本文冲突的自动排课逻辑。

---

## 0. 一句话与边界

**助教为人排「学 + 阶段测」有序总清单并设每生周中/周末时长；系统只按预算装箱成今日任务；学完打勾、测达标才过关；助教改清单/画像默认明天生效；单元换题导致重学则立刻插回今日并优先。**

### 0.1 必须做

- 单元目录、学生计划清单、时间画像、今日任务装箱、学/测完成态、助教工作台、学生今日任务 UI、模块深链「只开一单元」、换题升版本并重置完成态。

### 0.2 明确不做（首版）

- 算法自动决定学哪一科/哪几个单元  
- 学生改时间画像或总清单  
- 助教按日历逐日拖任务  
- 班级模板继承（允许「复制某生」快捷方式）  
- 学完自动插入测试  
- 正确率未达标禁止打勾（P4 跟读 ≥70% 除外）  
- 作文批改进单元体系  
- 口语 P3、小初/高中/核心词、语法、阅读听力整套、写作大小作文单元化（暂不规划）  
- 换题后让学生继续刷已下架老题  
- 换题自动作废阶段测过关  

### 0.3 时区

所有「今日 / 昨日 / 周中 / 周末」按 **Asia/Shanghai** 日历日计算（与现有 `TrackingUtils.getChinaYmd` 一致）。

---

## 1. 已定决策速查

| ID | 决策 |
|----|------|
| D1 | 清单无日期；系统按日从队首装箱 |
| D2 | 进度分母 = 该生计划内条目数（非全库） |
| D3 | 时间画像每生一份：周中分钟 + 周末分钟 |
| D4 | 助教改清单/画像 → **明天生效**；今日已释放锁定 |
| D5 | 任务打勾 = 学完；过关 = 阶段测达标 |
| D6 | 默认每学 **3** 个 study 提醒插阶段测（可配置 2～3）；仅建议+一键插入，不自动塞 |
| D7 | 换题：unit_id 不变，升 content_version；已完成→未完成；立刻插回今日优先 |
| D8 | 今日任务优先级：换题重学 → 昨日未完成 → 今日新释放 |
| D9 | 装箱容差：预算 × 1.15；队首单条超预算仍至少放 1 条；换题重学可强制放入（可超预算） |
| D10 | 暂停 = 不参与释放但仍占分母 Y；移出计划才改 Y |
| D11 | 未过关测试当日最多重测 **2** 次（默认） |
| D12 | 学生端显示「计划已更新，明天生效」（有 pending 变更时） |
| D13 | MVP 不提供「紧急立刻重算今日」 |
| D14 | 口语在进度上按 **子块** 分列（复合句 / P1 / P2 素材 / P2 套题），助教单元库同样分列 |
| D15 | **双轨进度**：计划轨（X/Y、A/B）与测试轨（`MODULES` %/分/个）**不合并、不互写** |
| D16 | 任务 `module_type` 经 **`parent_module`** 映射到主站 `MODULES.id`；口语四子块均映射 `speaking` |
| D17 | 未纳入计划的 `parent_module`：进度表 **灰显 +「暂未安排」**；学生 **不可** 从进度表进学习 |
| D18 | 学生端 **三块分区**：① 今日任务 ② 我的计划进度 ③ 测试与能力（见 §11.2） |
| D19 | **任务模式**：模块页只展示 `content_ref` 范围内题量；页内进度 **本单元** 计数，**不**显示模块全库总量 |
| D20 | **今日完成口径**：`done_fail`（测未过关）**不算**今日完成；测挂 +1；完成率分母仍含该条 |
| D21 | **阶段测写库**：写入 `test_records` 且 `record_kind=stage_test`；**测试轨 %/分只统计非 stage 记录** |
| D22 | **自由练（MVP）**：`in_plan` 科目仍可进自由入口，弹窗建议走今日任务；自由练 **不** 打勾任务 |
| D23 | **积压** = 曾进入过某日 `daily_tasks` 且至今未完成的条数；未生成过 daily 的队首 **不算**积压 |
| D24 | **队首测挂死**：重测次数用尽仍未过关 → **不自动跳过**；标红；助教可移队尾 / 插复习 / 重置重测次数 |
| D25 | **任务模式导航**：禁止模块内「下一课/下一单元」；仅当前 `content_ref`（含 P4） |
| D26 | **清单去重**：同一学生 live/draft 清单内 **禁止** 重复 `unit_id`（study）；拖入提示「已在计划中」 |
| D27 | **`scope_done` 服务端为准**：存服务端（plan_item 旁路表或 JSON）；模块上报增量；页头读服务端 |
| D28 | **全部 paused** = 无有效计划 → 班级总览 ⚪；文案 **「计划已暂停」**（区别于「未排计划」） |
| D29 | **紧急重算今日**：MVP **不做**（维持 D13）；仅文档预留 admin 接口注释 |
| D30 | **③ 查看详情**：仅历史成绩只读；**禁止**从详情进模块学习 |

---

## 2. 与现有代码的关系

| 现有 | 用法 |
|------|------|
| `MODULES` / `pass_standards` / `students.target_score` | **测试轨**：模块名、测试达标线、`bestScore` |
| `study_sessions` | 时长统计仍用；**单元打勾以任务完成上报为准**，不要仅靠时长推断 |
| `test_records` | 阶段测交卷 + **测试轨**最高分；`is_passed` + 达标线判定过关 |
| `sources/tinglidanciceshi/js/modules.js` | `MODULES` 定义；进度表行 id = `parent_module` |
| `sources/tinglidanciceshi/js/student.js` / `teacher.js` | 学生三块分区 / 任务计划 Tab / 学习进度 Tab |
| `scripts/local_server.py` + `student_api.py` + `teacher_api.py` | 新表与 API |
| 各模块学习/测试页 | 支持深链参数，只展示指定单元；完成后 `postMessage` 或调 API |

**双轨铁律（D15）**：

- **计划轨**：`plan_items` + `daily_tasks` → 学习 X/Y、过关 A/B  
- **测试轨**：`test_records` + `MODULES` → 测试 % / 个 / 分  
- **禁止**用计划 X/Y 回写 `bestScore`；**禁止**用 `bestScore` 自动打勾 `study_completed`  
- 两轨通过 `parent_module` 关联同一科目，界面 **分行展示**，不做合并进度条

---

## 3. 核心对象模型

### 3.1 单元目录 Unit（全平台主数据）

稳定主键：`unit_id`（字符串，全局唯一，换题不改）。

建议命名：`{module_or_sub}_{u}{nn}`，例如：

- `reading_synonym_u01` … `u23`
- `dictation_u01` …
- `listening_synonym_u01` …
- `speaking_complex_pattern_p1`（句型用 pattern id）
- `speaking_complex_adv_a1`（词组用 adv id）
- `speaking_p1_u01` …
- `speaking_p2_mat_yumeng`
- `speaking_p2_apply_u01` …

| 字段 | 类型 | 说明 |
|------|------|------|
| `unit_id` | TEXT PK | 稳定 ID |
| `module_type` | TEXT | 进度聚合用；口语子块用：`speaking_complex` / `speaking_p1` / `speaking_p2_material` / `speaking_p2_apply`（见 §5） |
| `parent_module` | TEXT | 归属主站 MODULES.id，口语均为 `speaking` |
| `unit_no` | INT | 展示序号（同 module_type 内从 1 递增） |
| `title` | TEXT | 展示名 |
| `content_ref` | TEXT/JSON | 模块深链定位（见 §5） |
| `est_minutes` | INT | 预估分钟（装箱用） |
| `content_version` | TEXT | 如 `20260825a` 或单调整数 |
| `completion_rule` | TEXT | 枚举，见 §6 |
| `study_url` | TEXT | 学习页路径（可含 query 模板） |
| `test_url` | TEXT | 可选；阶段测用 |
| `is_active` | INT | 1=现行目录可见 |
| `updated_at` | TEXT | ISO |

换题只更新 `content_ref` 指向的现行内容 + `content_version` + `updated_at`，**不改** `unit_id`。

### 3.2 时间画像 StudentTimeProfile

每生一行。

| 字段 | 说明 | 默认 |
|------|------|------|
| `student_id` | PK | |
| `weekday_minutes` | 周一～五每日 | **40** |
| `weekend_minutes` | 周六日每日 | **90** |
| `stage_test_every_n` | 连续 study 多久建议插测 | **3** |
| `pending_weekday_minutes` 等 | 待明天生效的值 | NULL=无 pending |
| `updated_at` | | |

生效逻辑：每天上海时区 0 点后首次访问（或定时）把 pending 合并进正式字段。

### 3.3 计划清单 PlanItem

每生有序列表。无日期字段。

| 字段 | 说明 |
|------|------|
| `id` | PK |
| `student_id` | |
| `sort_order` | 从 0 递增；队首最小 |
| `item_type` | `study` \| `test` |
| `unit_id` | study 必填；test 可空若用范围 |
| `module_type` | 冗余便于过滤 |
| `test_unit_ids` | JSON 数组；阶段测覆盖的 unit_id 列表 |
| `test_title` | 如「同义替换 U6–U8 阶段测」 |
| `est_minutes` | 可覆盖目录默认 |
| `status` | `pending` \| `paused` \| `removed` |
| `study_completed` | 0/1；仅 study；相对**当前** content_version |
| `study_completed_version` | 完成时的 content_version |
| `test_passed` | 0/1；仅 test |
| `test_attempt_count_today` | 当日重测计数 |
| `last_completed_at` | |
| `created_at` / `updated_at` | |

**生效副本**：助教编辑写 `plan_items_draft`（或 `plan_revision` + pending 标记）；每日生效时 draft → live。今日锁定的「已释放」条目不受 draft 排序删除影响（见 §7）。

简化实现也可：live 表 + `effective_from` 日期；改动写入 future 行。Agent 任选一种，但必须满足「明天生效」与「今日锁定」。

**清单去重（D26）**：同一 `student_id` 的 live 与 draft 中，`item_type=study` 且 `status!=removed` 时 **`unit_id` 唯一**。  
`PUT plan` / 拖入若重复 → `409` 或前端拦截，文案「该单元已在计划中」。单元库已排项灰显/不可再拖。  
阶段测 `test` 不按 `unit_id` 去重（可覆盖不同范围）；但同一组 `test_unit_ids` 完全相同的测建议去重（首版可仅前端提示）。

### 3.4 今日任务 DailyTask

按学生 + 上海日期物化（推荐），避免每次重算导致跳动。

| 字段 | 说明 |
|------|------|
| `id` | PK |
| `student_id` | |
| `task_date` | `YYYY-MM-DD` 上海 |
| `plan_item_id` | FK |
| `priority_class` | `content_refresh` \| `carry_over` \| `fresh` |
| `sort_in_day` | 日内序 |
| `state` | `todo` \| `in_progress` \| `done_study` \| `done_pass` \| `done_fail`（测未过关） |
| `locked` | 1=今日锁定（助教改清单不能摘掉） |
| `forced` | 1=换题强制插入（可超预算） |
| `created_at` | |

**生成时机**：学生打开今日任务 / 助教预览 / 换题 hook；同一 `student_id+task_date` 幂等：已有 locked 行保留，再按算法补齐。

### 3.5 内容版本归档（建议）

`unit_content_archive(unit_id, content_version, snapshot_json, archived_at)`  
换题时把旧 content_ref 快照写入；学生任务不读归档。

### 3.6 换题事件

`unit_content_bump(unit_id, old_version, new_version, bumped_at, operator)`  
触发：所有 `study_completed=1` 且 `study_completed_version != new_version` 的 PlanItem → `study_completed=0`；并为每个受影响且「今日有学籍/活跃」的学生执行 §8 插今日。

---

## 4. 进度口径（实现必须一致）

对每个 `module_type`（口语按子块）：

```text
学习 X = COUNT(plan study items WHERE status!=removed AND study_completed=1)
学习 Y = COUNT(plan study items WHERE status!=removed)   // 含 paused
过关 A = COUNT(plan test items WHERE status!=removed AND test_passed=1)
过关 B = COUNT(plan test items WHERE status!=removed)
```

界面文案：**「计划学习 X/Y · 过关 A/B」**，禁止写成全库分数。

### 4.1 双轨进度与 `parent_module`（实现必须一致）

#### 4.1.1 轨道定义

| 轨道 | 指标 | 数据来源 | 展示位置 |
|------|------|----------|----------|
| **计划轨** | 学习 X/Y、过关 A/B | `plan_items`（§4 公式） | ① 今日任务、② 我的计划进度、班级总览「计划进度(简)」、助教计划页模块摘要左列 |
| **测试轨** | 测试 % / 个 / 分、`bestScore`、是否达标 | `test_records` + `MODULES.targets` + `pass_standards` | ③ 测试与能力、助教学习进度 Tab、助教计划页模块摘要右列 |

#### 4.1.2 `parent_module` 映射表

任务单元 `module_type` → 主站 `MODULES.id`（`units.parent_module` 冗余存储，便于查询）：

| `module_type` | `parent_module` | 进度表展示名 |
|---------------|-----------------|--------------|
| `reading_synonym` | `reading_synonym` | 阅读同义替换 |
| `dictation` | `dictation` | 听力1000词 |
| `listening_basic` | `listening_basic` | 听力基础词汇 |
| `listening_synonym` | `listening_synonym` | 听力同义替换 |
| `sentence` | `sentence` | 长难句分析 |
| `writing_phrase` | `writing_phrase` | 写作词伙 |
| `writing_translate` | `writing_translate` | 写作句子翻译 |
| `listening_p4_speed` | `listening_p4_speed` | 听力P4跟读倍速 |
| `speaking_complex` | `speaking` | 口语练习（汇总） |
| `speaking_p1` | `speaking` | 同上 |
| `speaking_p2_material` | `speaking` | 同上 |
| `speaking_p2_apply` | `speaking` | 同上 |

**口语**：

- 计划轨：四子块 **分别** 算 X/Y（`module_type` 级）  
- 班级总览「口 X/Y」= 四子块计划 **学** 条完成合计 / 计划 **学** 条总数合计（**不是** 口语分数）  
- 测试轨：进度表仍 **1 行** `speaking`，单位 **分**

#### 4.1.3 「未纳入计划」判定 `plan_status`

```text
function planStatus(student_id, parent_module):
  items = plan_items WHERE student_id AND status != 'removed'
          AND (item.module_type 的 parent_module == parent_module
               OR item.module_type IN speaking 子块且 parent_module == 'speaking')
  if COUNT(items WHERE item_type IN ('study','test')) == 0:
    return 'not_in_plan'   // 暂未安排
  return 'in_plan'         // 已纳入计划
```

**仅存在于 `MODULES`、无任务单元的科目**（如基础语法、小初单词）：`plan_status = not_in_plan`，只在测试轨出现。

#### 4.1.4 未纳入计划 · UI 与交互（硬规则）

| 端 | 条件 | 样式 | 交互 |
|----|------|------|------|
| 学生 ③ 测试与能力 | `plan_status=not_in_plan` | 行灰显（`#f5f5f5` 或 `opacity:0.55`）；文案 **暂未安排** | **无**「去学习」/模块入口；可看历史测试分（若有） |
| 学生 ①② | `not_in_plan` | 不出现该科 | — |
| 助教学习进度 Tab | `not_in_plan` | 灰显 + 标签「暂未安排」 | 行点击 **不** 进模块学习；Tooltip + 可选「去排计划」 |
| 班级总览 | `not_in_plan` | 计划进度(简) **不显示**该科 | — |

纳入计划后：恢复正常色；计划轨出现 X/Y；学生主路径仍走 ① 今日任务。

#### 4.1.5 阶段测 vs 模块总测

| 类型 | 轨道 | 字段 |
|------|------|------|
| 清单内阶段测 `item_type=test` | 计划轨过关 A/B | `plan_items.test_passed` |
| 进度表模块测试 / 随机测 | 测试轨 | `test_records` → `bestScore` |
| 两者 | **不互相覆盖** | API 与 UI 文案区分「计划过关」与「测试进度」 |

---

## 5. 各科单元划分与 content_ref（已定）

### 5.1 阅读同义替换 `reading_synonym`

- 切法：现有 `GROUP_SETS` 一大组 = 1 单元  
- 数量：**23**  
- `content_ref`：`{ "setId": 1..23 }`  
- 学习页：`../tongyitihuan/index.html?unit=<setId>&task_id=<id>`  
- 打勾：该大组内全部小组至少练完 1 轮  
- 默认 `est_minutes`：**15**

### 5.2 听力1000词 `dictation`

- 切法：现有每组 20 词 = 1 单元  
- 数量：`ceil(词数/20)`（约 50）  
- `content_ref`：`{ "groupIndex": 0-based }`  
- 学习页：听力学习页 `?group=<n>&task_id=`  
- 打勾：四阶段流程走完（与现 `groupStatus=completed` 一致）  
- `est_minutes`：**25**

### 5.3 听力基础词汇 `listening_basic`

- 切法：每组 50 词 = 1 单元  
- `content_ref`：`{ "groupIndex": 0-based }`  
- 打勾：同四阶段  
- `est_minutes`：**35**

### 5.4 听力同义替换 `listening_synonym`

- 切法：**每 5 题 = 1 单元**（实现时把现「每组 10 题」改切或映射：原组 i 的前 5 / 后 5 → 两单元）  
- 约 120 题 → **约 24** 单元  
- `content_ref`：`{ "questionIds": [...] }` 或 `{ "startId", "endId" }`  
- 打勾：该单元题目答完一遍（不论对错）  
- `est_minutes`：**12**

### 5.5 长难句 `sentence`

- 切法：60 句按题号，**每 5 句 = 1 单元** → **12**  
- `content_ref`：`{ "sentenceNums": [1,2,3,4,5] }`  
- 打勾：单元内每句拆解步骤走完  
- `est_minutes`：**20**

### 5.6 写作词伙 `writing_phrase`

- 切法：每个分类入口 = 1 单元  
- 含：`__foundation__`（基础必背）+ `categories.js` 中 13 类 → **14**  
- `content_ref`：`{ "categoryId": "__foundation__" | "小作文词伙一" | ... }`  
- 打勾：该分类学习浏览完成 + 练习一轮做完  
- `est_minutes`：**20**

### 5.7 写作句子翻译 `writing_translate`

- 数据：`translation_data.json`，按 `category`  
- 规则：主题句数 **≤10 → 整类 1 单元**；**>10 → 类内每 5 句 1 单元**（最后不足 5 亦成一单元）  
- 现估约 **23** 单元  
- `content_ref`：`{ "category": "...", "itemIndexes": [..] }`  
- 打勾：单元内题全部完成一遍  
- `est_minutes`：**15**

### 5.8 听力 P4 跟读 `listening_p4_speed`

- 切法：1 篇课文 = 1 单元；后续篇目入库即增单元  
- 打勾：**跟读流程完成且识别率 ≥ 70%**（本模块例外，带质量门槛）  
- ≥70% 后允许进入下一篇（产品规则；清单释放仍由计划决定，但模块内导航可解锁下一课）  
- `content_ref`：`{ "lessonId": 1 }`  
- `est_minutes`：**15**

### 5.9 口语子块（均 `parent_module=speaking`）

#### 5.9.1 复合句 `speaking_complex`

- 句型 `PATTERNS`：7 个，每型 10 句；词组 `ADV`：10 个，每组 10 句  
- **每个句型或词组 = 1 单元**；单元内必须完成 **拼装 + 跟读 + 脱口而出** 三轨才打勾  
- 数量：**17**  
- `content_ref`：`{ "kind": "pattern"|"adv", "id": "p1"|"a1"|... }`  
- 学习页：`/kouyulianxi/` → P1 复合句闯关深链  
- `est_minutes`：**25**

#### 5.9.2 P1 题型 `speaking_p1`

- 全库题目 **跨类连续** 排序，**每 10 题 = 1 单元**（约 235 题 → 约 24）  
- 顺序：按 `p1-data.js` 中 categories 数组顺序，类内 questions 顺序拼接后切片  
- `content_ref`：`{ "questionKeys": ["catId:qid", ...] }`（10 个）  
- 打勾：10 题均至少 1 次有效练习（有录音/识别结果，空点不算）  
- `est_minutes`：**30**

#### 5.9.3 P2 素材 `speaking_p2_material`

- `P2_DATA.materials` 每个素材 = 1 单元（现 **8**）  
- `content_ref`：`{ "materialId": "yumeng"|... }`  
- 打勾：该素材背诵/学习流程完成（与现「素材」模式完成标准对齐；实现时对齐现 UI 完成标记）  
- `est_minutes`：**20**

#### 5.9.4 P2 套题 `speaking_p2_apply`

- `P2_DATA.questions` **每 5 题 = 1 单元**（54 题 → **11**；最后一单元可不足 5）  
- `content_ref`：`{ "questionIndexes": [0,1,2,3,4] }`（0-based）  
- 打勾：该 5 题套题练习完成一遍  
- `est_minutes`：**25**

### 5.10 排除与暂不规划

- `writing_correction`：不纳入  
- 口语 P3、单词语法未上线模块等：不建单元、单元库不展示  

---

## 6. 完成与过关状态机

### 6.1 Study 条目

```text
todo → in_progress → completed(study_completed=1, version=当前)
```

换题 bump：

```text
completed → todo（study_completed=0），并插入今日 content_refresh
```

上报接口必须带：`unit_id`, `content_version`, `task_id`/`plan_item_id`。  
若 `content_version` 落后于目录当前版本 → 拒绝完成或要求刷新后再提交。

### 6.2 Test 条目

```text
todo → submitted
  ├─ score >= threshold → test_passed=1, daily.state=done_pass (过关，算今日完成)
  └─ else → test_passed=0, daily.state=done_fail；当日 attempt < 2 可重测；
             否则提示联系助教（队首测挂死，见 §7.1 / D24）
```

`threshold` = `pass_standards` 中该 `module_type`（或 parent）对应该生 `target_score` 的分数。  
阶段测 `module_type` 用覆盖单元的 `parent_module` 对应主站模块（如 reading_synonym）。

范围抽题：能做则按 `test_unit_ids` 抽；不能则整卷测，范围仅作文案与进度标记（首版允许）。

**今日完成口径（D20）**：

| `daily_tasks.state` | 计入今日完成率分子 | 测挂列 |
|--------------------|--------------------|--------|
| `done_study` | ✓ | — |
| `done_pass` | ✓ | — |
| `done_fail` | **✗** | ✓ |
| `todo` / `in_progress` | ✗ | — |

完成率 = 分子条数 ÷ 今日总条数（分母含 `done_fail`）。

**阶段测写库（D21）**：`submit-test` 写入 `test_records`，字段含 `record_kind='stage_test'`（或等价标记）。  
**测试轨**（③、学习进度 Tab、`bestScore`）**只聚合** `record_kind` 为空或 `module_test` / `random` 等非 stage 记录；计划过关 A/B 只看 `plan_items.test_passed`。

### 6.3 禁止

- 仅打开页面 / 时长到点自动完成  
- 未走完模块流程的客户端「强制完成」（除非教师管理员工具，首版不做）

---

## 7. 每日装箱算法（必须按此实现）

输入：`student_id`, `task_date`（上海 YMD）

```text
function buildDailyTasks(student_id, task_date):
  profile = loadEffectiveTimeProfile(student_id, task_date)  // 已合并当天应生效的 pending
  budget = isWeekend(task_date) ? profile.weekend_minutes : profile.weekday_minutes
  tolerance = budget * 1.15

  existing = loadDailyTasks(student_id, task_date)
  // 保留已有 locked/forced 行；清掉未 locked 的 fresh 后重算时可重生成 —— MVP：首次生成后 locked=1

  result = []
  used = 0

  // 1) 换题重学：plan study 未完成且标记 need_content_refresh 或今日 bump 列表
  for item in contentRefreshQueue(student_id):
    result.append(item, priority=content_refresh, forced=true)
    used += est(item)

  // 2) 积压 carry-over（D23）：曾进入过任意日 daily_tasks、至今未完成的 plan_item
  //    （含昨日未完、多日积压、换题重学未完）；未生成过 daily 的队首不算积压
  for item in backlogUnfinished(student_id):
    if already_in(result, item): continue
    result.append(item, priority=carry_over)
    used += est(item)

  // 3) 从 live 清单队首装箱（D25 装箱补全）
  for item in livePlanOrdered(student_id):
    if item.status in (paused, removed): continue
    if item.item_type == study and item.study_completed == 1: continue
    if item.item_type == test and item.test_passed == 1: continue
    if already_in(result, item): continue
    // 队首测挂死（D24）：重测已满且未过关 → 仍可进入今日（标红），但不得自动跳过挡后面；
    // 助教工具：移队尾 / 插复习 / 重置 test_attempt_count
    if used > 0 and used + est(item) > tolerance: break
    if used == 0 and est(item) > budget:
      result.append(item, priority=fresh)  // 至少 1 条，可超预算
      break
    result.append(item, priority=fresh)
    used += est(item)
    if used >= tolerance: break

  persistDailyTasks(student_id, task_date, result)  // 写入后 locked=1
  return result
```

助教改清单：只改 draft；**不删除**当日已 locked 的 daily 行。  
次日 `buildDailyTasks` 使用新 live 清单。  
0 点后合并 pending 画像/清单 **只影响次日装箱**，不重算当日已 locked 行（D13）。

### 7.1 积压与队首测挂死（D23 / D24）

```text
backlog_count = COUNT(distinct plan_item_id WHERE
  exists daily_tasks row for this plan_item on some task_date <= today
  AND plan_item not completed:
    study → study_completed=0
    test  → test_passed=0
)
```

- **不算积压**：从未进过任何日 `daily_tasks` 的清单队首（学生未登录导致未装箱）  
- **队首测挂死**：`test` 当日 `test_attempt_count_today` 已达上限且 `test_passed=0`  
  - **不**自动跳过、**不**自动插复习  
  - 班级总览测挂/标红；助教计划页提供：**移到队尾** / **插入复习学单元** / **重置重测次数**（当日可再测）

---

## 8. 换题流程（Agent 必实现）

```text
function bumpUnitContent(unit_id, new_content_ref, new_version, operator):
  old = loadUnit(unit_id)
  archive(unit_id, old.content_version, old.content_ref)
  updateUnit(unit_id, content_ref=new_content_ref, content_version=new_version)

  for each plan_item WHERE unit_id AND item_type=study AND study_completed=1:
    set study_completed=0, clear study_completed_version
    mark need_refresh

  today = chinaYmd(now)
  for each affected student_id:
    ensureDailyTask(student_id, today, plan_item, priority=content_refresh, forced=true, prepend=true)
    // 即使预算已满也写入
```

测试过关字段 **不动**。

---

## 9. API 草案（路径可微调，语义不可少）

鉴权：学生 token / 教师 session（与现网一致）。

### 9.1 目录

- `GET /api/task/units?module_type=` → 单元列表（助教库）  
- `POST /api/task/units/:unit_id/bump`（教师）→ body: content_ref, content_version；执行 §8  

### 9.2 时间画像

- `GET /api/task/students/:id/time-profile`  
- `PUT /api/task/students/:id/time-profile` → 写入 pending，明天生效；或 `effective=tomorrow`  
- `POST /api/task/students/:id/time-profile/copy-from/:fromId`  

### 9.3 计划

- `GET /api/task/students/:id/plan` → live + draft 摘要 + 各 `module_type` 计划轨 X/Y A/B + **`module_summary[]`**（双列，见下）  
- `PUT /api/task/students/:id/plan` → 全量/增量更新 draft（排序、增删、暂停）；**重复 unit_id → 409（D26）**  
- `POST /api/task/students/:id/plan/insert-stage-test` → body: unit_ids[], after_sort_order?  
- `POST /api/task/students/:id/plan/apply-draft` → 仅管理员测试用；生产靠日期生效  
- （D29 预留勿实现）`POST /api/task/students/:id/rebuild-today?only=todo` 

**`module_summary[]` 元素**（助教计划页双列、与学生 ② 区同源）：

```json
{
  "module_type": "reading_synonym",
  "parent_module": "reading_synonym",
  "title": "阅读同义替换",
  "plan_status": "in_plan",
  "plan_study_x": 5, "plan_study_y": 8,
  "plan_pass_a": 1, "plan_pass_b": 3,
  "test_score": 78, "test_target": 80, "test_unit": "percent",
  "test_passed": false
}
```

口语子块多条 + 可选汇总行 `{ "parent_module": "speaking", "module_type": null, "test_score": 6.0, ... }`。

### 9.3.1 班级总览（教师）

- `GET /api/task/class-overview?filters=` → 学生行列表（见线框 §3）  
  - 字段：`today_done`, `today_total`, `today_minutes`, `budget_minutes`, `backlog`, `content_refresh`, `test_fail`, `plan_progress_brief[]`, `row_status`（red/yellow/green/none）  
  - `plan_progress_brief[]`：**仅计划轨**，最多 2 条缩写 + `+N`；**不含**测试 %

### 9.3.2 学习进度 Tab（测试轨 + 计划状态）

扩展现有教师进度 API 或新增：

- `GET /api/teacher/progress?student_id=` → 每行增加 **`plan_status`**: `in_plan` | `not_in_plan`  
- 前端：`not_in_plan` 行灰显、禁跳转学习；`in_plan` 行为与现网一致

### 9.4 今日任务（学生）

- `GET /api/task/me/today` → 生成或返回当日任务 + 预计分钟 + **计划轨**各 module 进度 + `pending_plan_change`  
  - 每条 `study`/`test` 含 **`scope_*`** 字段（§10.1），供模块页与本单元进度条使用  
- `GET /api/task/me/plan-progress` → ② 我的计划进度：仅 `plan_status=in_plan` 的 `module_summary[]`（无今日条目明细）  
- `GET /api/task/me/test-ability` → ③ 测试与能力：遍历 `MODULES`，每行含 `plan_status`、测试分/目标、是否达标  
- `POST /api/task/me/items/:plan_item_id/complete-study` → body: content_version, evidence?  
- `POST /api/task/me/items/:plan_item_id/scope-progress` → body: `{ scope_done }` 或 `{ delta }`（D27）  
- `POST /api/task/me/items/:plan_item_id/submit-test` → body: score, details；写 `test_records`（`record_kind=stage_test`）+ 更新 `test_passed` / daily `done_pass|done_fail`（D20/D21）  

助教计划页（队首测挂死，D24）：

- `POST /api/task/students/:id/plan-items/:plan_item_id/move-to-tail`  
- `POST /api/task/students/:id/plan-items/:plan_item_id/reset-test-attempts`  
- （插复习仍走现有 insert / 拖入 study）

### 9.5 建议

- `GET /api/task/students/:id/suggestions` → `{ type: "insert_stage_test", module_type, unit_ids, message }`  

---

## 10. 深链与模块改造清单

每个学习页必须：

1. 读取 `unit` / `group` / `setId` / `categoryId` / **`task_id` / `plan_item_id` / `unit_id`** 等 query  
2. 若存在 `task_id` 或 `plan_item_id` → 进入 **任务模式**（§10.1）  
3. **隐藏**单元外入口（或不可点）  
4. 完成时向父页 `postMessage`：

```json
{
  "type": "taskUnitComplete",
  "unit_id": "...",
  "content_version": "...",
  "task_id": "...",
  "plan_item_id": "...",
  "payload": {}
}
```

5. 测试页类似 `taskTestComplete` + score  

**模块改造优先级（MVP）**：`tongyitihuan` + `listening.html(dictation)` → 再铺开其余已定模块。  
**Phase 2 必改 UI**：`listening_synonym`（5 题/单元 vs 原 10 题/组）、`sentence`、`speaking_p1`（任务 scope 切片）。

父页 `student.js` 监听后调 `complete-study` API 并刷新今日列表。

### 10.1 任务模式（Task Scope）与页内进度

任务单元粒度与模块 **原生导航粒度** 常不一致（如阅读 23 大组 vs 225 小组、听力同义 5 题/单元 vs 10 题/组、口语 P1 10 题/单元 vs 235 题全库）。**不强行统一数字**，采用 **计划层 + 内容层 + 测试层** 三套口径并存：

| 层级 | 回答什么 | 展示位置 | 示例 |
|------|----------|----------|------|
| **计划层** | 助教排的第几个任务单元 | ① 今日任务组头、② 计划进度 | 计划学习 **5/8** |
| **内容层** | 本单元内做到哪 | 模块页（任务模式）页头/进度条 | **本单元 3/10 组**、**2/5 题** |
| **测试层** | 模块测试考得怎样 | ③ 测试与能力 | 测试 **78%** / 80% |

**铁律**：

- 任务模式下模块页 **只** 显示内容层（`content_ref` 范围内）；**禁止**显示模块全库总量（如「80/235 题」「第 3/12 组」指全库）。  
- 任务打勾以 `complete-study` + `plan_items.study_completed` 为准；**禁止**用模块全库完成率推断任务完成。  
- 自由练模式仍用模块原生进度；与任务模式 **分开展示**。

#### 10.1.1 任务模式检测与 UI 约定

```text
function isTaskMode():
  return query has task_id OR plan_item_id OR unit_id (from task deep link)

if isTaskMode():
  load only content_ref slice
  hide global module home / other units
  disable "下一课/下一单元/下一组" navigation  // D25，含 P4
  header = "今日任务 · {module_title} · {unit_title}"
  progress label = "本单元"   // 固定文案，不用「总进度」
  progress = scope_done / scope_total + scope_unit  // scope_total 按 content_ref 动态算（如阅读 U23=5）
else:
  existing free-practice UI unchanged
```

页头示例：

```text
今日任务 · 阅读同义替换 · 单元 6（入门基础篇）
本单元：3/10 组已完成
```

#### 10.1.2 今日任务 API · `scope_*` 字段

`GET /api/task/me/today` 每条学习/测试条目建议返回：

```json
{
  "plan_item_id": 42,
  "item_type": "study",
  "unit_id": "reading_synonym_u06",
  "title": "单元 6 · 入门基础篇",
  "module_type": "reading_synonym",
  "content_ref": { "setId": 6 },
  "scope_label": "本单元",
  "scope_total": 10,
  "scope_done": 3,
  "scope_unit": "组",
  "scope_hint": "大组内 10 个练习组各至少练 1 轮",
  "study_url": "../tongyitihuan/index.html?setId=6&task_id=..."
}
```

| 字段 | 说明 |
|------|------|
| `scope_total` | 本 `content_ref` 内 countable 子项总数 |
| `scope_done` | 学生在本单元内已完成子项数；**以服务端为准（D27）** |
| `scope_unit` | 展示单位：`组` / `题` / `句` / `词` / `分类` 等 |
| `scope_hint` | 可选；完成规则一句话（助教/学生可读） |

#### 10.1.2a `scope_done` 存储（D27）

推荐表 `task_unit_progress`（或 `plan_items.scope_json`）：

| 字段 | 说明 |
|------|------|
| `student_id` + `plan_item_id`（或 `unit_id`） | 主键 |
| `scope_done` | INT |
| `scope_total` | INT（可冗余自 content_ref） |
| `updated_at` | |

- 模块内每完成一子项：`POST /api/task/me/items/:id/scope-progress` → `{ delta: 1 }` 或 `{ scope_done: n }`  
- `GET /api/task/me/today` 的 `scope_*` **读服务端**，不以 localStorage 为准  
- MVP：可只存计数，不必每题明细；打勾仍走 `complete-study` + `content_version`  
- 换设备 / 清缓存后页头进度与服务器一致  

模块页用 `scope_*` 渲染页内进度；**计划 X/Y 仅在任务列表组头**，不在模块页与 `scope_*` 混在同一进度条。

#### 10.1.3 各科：原生粒度 vs 任务单元 vs 任务模式显示

| `module_type` | 模块原生 UI | 任务 1 单元 | 任务模式页内进度 | 打勾条件 |
|---------------|-------------|-------------|------------------|----------|
| `reading_synonym` | 225 小组 + 23 大组入口 | 1 `GROUP_SETS` 大组（多数 10 小组；**U23=5**） | **n/m 组**（`scope_total` 动态） | 大组内全部小组各至少练 1 轮 |
| `dictation` | 20 词/组 | 1 组（20 词） | 四阶段进度（与现网一致） | 四阶段 `completed` |
| `listening_basic` | 50 词/组 | 1 组 | 同 dictation | 同 dictation |
| `listening_synonym` | **12 组 × 10 题** | **5 题/单元**（一组拆两单元） | **2/5 题**；标题可写「单元 2（原第 1 组 · 题 6–10）」 | 单元内 5 题各答完一遍 |
| `sentence` | 60 句列表 | 5 句/单元 | **2/5 句**；导航锁定句号范围 | 单元内每句拆解步骤走完 |
| `writing_phrase` | 14 分类 | 1 分类 | 分类内练习进度 | 该分类学习+练习一轮完成 |
| `writing_translate` | 按 category | ≤10 句整类或每 5 句 | **n/m 句** | 单元内题全部完成一遍 |
| `listening_p4_speed` | 多篇课文 | 1 篇 | 跟读识别率 | ≥70% 且流程完成；**任务模式禁下一篇**（D25） |
| `speaking_complex` | 句型/词组各 10 句 | 1 句型或词组 | 拼装+跟读+脱口而出三轨 | 三轨均完成 |
| `speaking_p1` | **235 题**全库 | **10 题/单元** | **7/10 题**；**不**显示 80/235 | 10 题各至少 1 次有效练习 |
| `speaking_p2_material` | 8 素材 | 1 素材 | 素材内步骤 | 与现 P2 素材完成标准对齐 |
| `speaking_p2_apply` | 54 题 | 5 题/单元 | **3/5 题** | 5 题套题完成一遍 |

**听力同义**（`listening_synonym`）：首页文案「每组 10 题」在任务模式下 **必须** 改为「本单元 5 题」或子模式入口；不可仍展示 12 组全选网格。

#### 10.1.4 完成后回写模块局部状态（推荐）

任务单元 `complete-study` 成功时，除更新 `plan_items` 外，**建议**将 `content_ref` 覆盖的内容在模块原生存储中标为已完成（如 `localStorage`、现有完成标记）：

- 避免学生日后 **自由练** 时重复做同一批题/组  
- **不**因此自动增加计划 X/Y（X/Y 只来自 `plan_items`）  
- **不**回写测试轨 `bestScore`

实现方式：模块 `taskUnitComplete` 处理函数内调用既有「标记小组/题完成」逻辑，范围限定在 `content_ref`。

#### 10.1.5 禁止（任务模式）

- **禁止**把任务单元映射为模块首页「第 N 组」按钮且题量仍按 10 题/组（听力同义）  
- **禁止**任务模式下展示可点击的全模块目录  
- **禁止**用 `scope_done/scope_total` 与计划 `X/Y` 画在同一条进度条上  
- **禁止**用模块全库 % 触发 `study_completed=1`  
- **禁止**任务模式下「下一课 / 下一单元 / 下一组」导航（D25；含 P4 ≥70% 后解锁下一篇）

### 10.2 自由练与任务路径（D22 · MVP）

- **短期（MVP）**：学生主页 ① 下方 **保留** 原模块自由入口  
- 进入 `parent_module` 且 `plan_status=in_plan` 的自由入口时：弹窗提示「建议从今日任务进入」；可「仍要自由练」或「去今日任务」  
- 自由练完成 **不** 调用 `complete-study`，**不** 改 `plan_items.study_completed`  
- `study_sessions` 建议带可选 `plan_item_id`（任务路径有值；自由练为空），便于日后拆分「任务时长 vs 自由时长」  
- **中期/V3**：可改为 `in_plan` 科目禁止自由入口（见 overview §7.4）  
- 学生 ③「查看详情」：**仅** 历史测试成绩只读，**禁止** 从详情进模块学习（D30）  
- **中期/V3**：可改为 `in_plan` 科目禁止自由入口（见 overview §7.4）  

### 10.3 无有效计划 / 计划已暂停（D28）

```text
function rowPlanStatus(student_id):
  items = live plan WHERE status != removed
  if count(items) == 0:
    return none          // 未排计划 · ⚪ · 文案「未排计划」
  if count(items WHERE status == pending) == 0
     and count(items WHERE status == paused) >= 1:
    return all_paused    // 计划已暂停 · ⚪ · 文案「计划已暂停」
  return active          // 有可释放条目
```

- 班级总览：`none` 与 `all_paused` 均为 ⚪，**不**因「今日 0 任务」标红  
- 「计划进度(简)」空值：`none` → `未排计划`；`all_paused` → `计划已暂停`  
- 学生无今日任务：`none` →「今日暂无任务，请联系助教」；`all_paused` →「计划已暂停，请联系助教」  

### 10.4 紧急重算今日（D29 · MVP 不做）

- **MVP**：不提供助教/admin「立刻重算今日」按钮（D13）  
- 预留（勿实现）：`POST /api/task/students/:id/rebuild-today?only=todo`  
  - 仅删除/重建当日 `state=todo` 且非 `forced` 的行  
  - 保留 `in_progress` / `done_*` / `forced`  
- 改清单/画像仍 **明天生效**  

---

## 11. UI 需求（验收级）

> 班级总览列定义、标红规则、双轨线框：[`task-system-teacher-dashboard-wireframe.md`](task-system-teacher-dashboard-wireframe.md)

### 11.1 助教「任务计划」

入口：教师端新 Tab「任务计划」；默认子 Tab「班级总览」。

**班级总览**（日常第一屏）：

- 列：状态灯、学号、姓名、今日任务、今日时长、积压、换题、测挂、**计划进度(简)**（仅计划轨）  
- 筛选：今日未完成、有积压、换题重学、测未过关、需关注、无计划  
- 行 Hover：计划轨「学习 X/Y · 过关 A/B」；测试轨摘要 **可选第二段、分行**  
- 点行 → 学生计划页  

单生页：

1. 监控摘要（计划轨，与总览同源）  
2. **模块摘要双列**：左计划 X/Y A/B，右测试 %/分（`not_in_plan` 右列灰显「暂未安排」）  
3. 时间画像编辑（周中/周末）；复制自其他学生  
4. 建议条（连续 N 学未测）  
5. 左：单元库（按 module_type / 口语子块折叠）；已排标记；显示 version/更新日期  
6. 右：有序清单；拖拽；学/测徽章；暂停/移除；插入阶段测对话框  
7. 本周预览只读（基于 **即将生效** 的 draft+画像）  
8. 文案：「修改默认明天生效」；今日锁定条灰显  

**学习进度 Tab**（现有 `tabProgress` 扩展）：

- 新增列 **计划状态**：`已纳入计划` | `暂未安排`  
- `暂未安排`：行灰显（`#f5f5f5` / `opacity:0.55`）、文字 `#999`、禁跳转学习、可选「去排计划」  

权限：教师与 admin；学生只读自己今日与 ②③。

### 11.2 学生端三块分区（自上而下，不可合并指标）

| 区块 | DOM id 建议 | 数据 API | 主操作 |
|------|-------------|----------|--------|
| **① 今日任务** | `#task-today` | `GET /api/task/me/today` | 点学/测；组头显示计划 X/Y · A/B |
| **② 我的计划进度** | `#task-plan-progress` | `GET /api/task/me/plan-progress` | 只读；**仅** `in_plan` 科目 |
| **③ 测试与能力** | `#task-test-ability` | `GET /api/task/me/test-ability` | 可折叠；`in_plan` 可「查看详情」；`not_in_plan` 灰显「暂未安排」**无学习入口** |

**① 今日任务**细节：

- 置顶于学生主页；预计分钟；按模块分组  
- 条目状态按钮；换题重学标「内容已更新」  
- 无任务：提示联系助教  
- 有 pending 计划变更：提示明天生效  

**③ 测试与能力**灰显规则（`plan_status=not_in_plan`）：

```css
/* 建议类名 */
.task-test-row--not-in-plan {
  opacity: 0.55;
  background: #f5f5f5;
  color: #999;
  pointer-events: none; /* 禁模块学习入口；详情按钮若保留则单独放开 */
}
```

- 短期：① 下方可保留原自由模块入口（与 overview §7.4 / D22 一致）  
- **③ 查看详情**：只读历史成绩，无学习入口（D30）  
- **禁止**：单条进度条同时表示 X/Y 与测试 %

### 11.3 学生 · 任务模式模块页（内容层）

从 ① 点「去学习」进入模块时，页面须符合 §10.1：

```text
┌────────────────────────────────────────────────────────────┐
│ ← 返回今日任务                                              │
│ 今日任务 · 阅读同义替换 · 单元 6（入门基础篇）              │
│ 本单元：3/10 组已完成                                       │
├────────────────────────────────────────────────────────────┤
│  （仅 content_ref 内 10 个小组；无其他大组入口）            │
│  … 学习内容 …                                               │
└────────────────────────────────────────────────────────────┘
```

| 元素 | 任务模式 | 自由练模式 |
|------|----------|------------|
| 页头副标题 | **本单元：n/m 组|题|句** | 模块原生（如 80/235 题） |
| 单元/组选择 | 隐藏或禁用范围外 | 全部可选 |
| 返回 | 「返回今日任务」 | 「返回」/ 模块首页 |
| 完成上报 | `postMessage` → `complete-study` | 仅模块本地进度 |

听力同义任务模式线框：

```text
今日任务 · 听力同义替换 · 单元 2（第 1 组 · 题 6–10）
本单元：2/5 题
[题 6] [题 7] …  （仅 5 题，无「12 组」首页）
```

---

## 12. 默认取值汇总（无争议时用此数）

| 项 | 值 |
|----|----|
| 周中分钟 | 40 |
| 周末分钟 | 90 |
| 装箱容差 | 15% |
| 建议插测间隔 | 3 |
| 当日重测上限 | 2 |
| 暂停占 Y | 是 |
| 清单去重 | 同生禁止重复 unit_id（D26） |
| scope_done | 服务端为准（D27） |
| 全部 paused | ⚪「计划已暂停」（D28） |
| 紧急重算今日 | MVP 不做（D29） |
| ③ 详情进学习 | 禁止（D30） |
| 口语进度 | 子块分列（计划轨）；测试轨 1 行 speaking |
| `parent_module` | 见 §4.1.2 |
| `plan_status` 灰显文案 | **暂未安排** |
| 今日完成（测） | `done_fail` **不算**完成（D20） |
| 阶段测写库 | `record_kind=stage_test`；不进测试轨聚合（D21） |
| 自由练 MVP | 可进 + 弹窗；不打勾（D22） |
| 积压 | 曾进 daily 且未完成（D23） |
| 队首测挂死 | 不自动跳过；助教工具（D24） |
| 任务模式导航 | 禁下一课（D25） |
| est_minutes | 见 §5 各科 |

---

## 13. 建议实现分期（Agent 执行顺序）

### Phase 0 — 文档与骨架

- [ ] 建表迁移（profile / units / plan / daily_task / archive）  
- [ ] 种子：至少导入 `reading_synonym` 23 + `dictation` 全组单元行  

### Phase 1 — MVP 闭环

- [ ] 助教：画像 + 清单 draft/live + 明天生效  
- [ ] 装箱 + 学生今日任务 API/UI（含 ①②③ 三块）  
- [ ] 计划轨 X/Y 与测试轨 `plan_status` 分列 API  
- [ ] 阅读同义替换深链 + 完成上报打勾  
- [ ] 手动插阶段测 + test 过关（可先整卷）  
- [ ] 单测：装箱顺序、明天生效、进度 X/Y  

### Phase 2 — 换题与更多模块

- [ ] bump API + 重置完成 + 今日优先插入  
- [ ] 听力词、听力同义替换改切 5 题 + **任务模式 UI**、长难句、词伙、翻译、P4、口语各子块  
- [ ] 建议插测、本周预览、积压标红、**班级总览**（计划轨）  
- [ ] 学习进度 Tab `plan_status` + 暂未安排灰显  

### Phase 3 — 打磨

- [ ] 清单复制、弱化自由入口、阶段测范围抽题、归档查询  

---

## 14. 验收用例（Agent 自测清单）

1. 新学生默认画像 40/90；助教改为 20/60，**当日**今日任务仍按旧预算；**次日**按新预算。  
2. 清单拖入 5 个 study；今日只放出预算内若干；学生不可见未释放项。  
3. 学完一单元 → 打勾 → X/Y 分子 +1；Y 不因全库变化。  
4. 插入阶段测覆盖 3 单元；交卷达线 → A/B 过关 +1；未达线可重测至多 2 次。  
5. 今日任务进行中，助教删除清单队尾未释放项 → 今日列表不变；次日生效。  
6. bump 某已完成 unit → 该生该条未完成 + 今日列表顶部出现「内容已更新」；学完新题再勾。  
7. 换题强制任务在预算已满时仍出现。  
8. paused 项不释放但仍计入 Y。  
9. 周末用 weekend_minutes。  
10. compileall + 现有 unittest + 为本功能新增 API/装箱单测。  
11. **双轨**：同一科目 API 同时返回 `plan_study_x/y` 与 `test_score`，前端分行展示，无合并条。  
12. **暂未安排**：`MODULES` 中某科 `plan_status=not_in_plan` → 学生 ③ 灰显、无学习入口；助教进度 Tab 灰显禁跳转。  
13. **口语**：四子块分别 X/Y；`speaking` 测试轨 1 行分；班级总览「口 X/Y」为学条合计非分数。  
14. **班级总览** `plan_progress_brief` 不含测试 %；Hover 计划轨与测试轨分行。  
15. 纳入计划后：`plan_status` 变 `in_plan`，计划轨出现 X/Y，学生仍从 ① 进学习。  
16. **任务模式**：带 `task_id` 进阅读同义 U6，页头显示「本单元 3/10 组」，**不**显示 225 小组全库进度。  
17. **听力同义**任务模式只出 5 题，进度 **5/5** 后可 `complete-study`；模块首页 12 组网格不可见。  
18. **口语 P1** 任务模式只列 10 题，页头 **7/10 题**；不显示 235 题总量。  
19. `complete-study` 后 `scope_done` 重置或置满，计划 X/Y +1；模块局部完成态可回写，测试 % 不变。  
20. 自由练与任务模式切换：同一模块两种页头文案不混用。  
21. **D20**：测未过关 `done_fail` → 今日完成率分子不含该条，测挂 +1。  
22. **D21**：阶段测写入 `test_records(record_kind=stage_test)` 后，测试轨 bestScore **不变**。  
23. **D22**：自由练不打勾；`in_plan` 进自由入口有弹窗。  
24. **D23/D24**：积压不含「从未进过 daily」的队首；测挂死不自动跳过，助教可移队尾。  
25. **D25**：任务模式 P4 完成 ≥70% 后仍不能进下一篇。  
26. 阅读同义 U23：`scope_total=5`（非 10）。  
27. **D26**：重复拖同一 unit → 拒绝；单元库已排灰显。  
28. **D27**：换设备后 `scope_done` 与服务器一致。  
29. **D28**：全部 paused → 总览 ⚪「计划已暂停」，不标红。  
30. **D30**：③ 详情无「去学习」按钮。  

---

## 15. 关键文件（预期会改）

| 路径 | 工作 |
|------|------|
| `scripts/local_server.py` | 建表、路由 |
| `scripts/student_api.py` / `teacher_api.py` | 或新建 `task_api.py` |
| `sources/tinglidanciceshi/js/student.js` | 三块分区 UI、postMessage、`plan_status` 灰显 |
| `sources/tinglidanciceshi/js/teacher.js` | 任务计划 Tab、班级总览、学习进度 Tab 计划状态列 |
| `sources/tinglidanciceshi/index.html` / css | 布局 |
| `sources/tongyitihuan/index.html` 等各模块页 | 深链与完成上报 |
| `tests/` | 装箱与换题单测 |
| `docs/task-system-spec.md` | 本文 |
| `docs/task-system-overview.md` | 产品总览 |
| `docs/task-system-teacher-dashboard-wireframe.md` | 班级总览与双轨线框 |

---

## 16. 给 Agent 的硬约束

1. **禁止**实现「系统自动挑选今日学哪些科目」；只能从助教清单队首装箱。  
2. **禁止**助教改清单当日抽走学生已释放任务（换题重学除外）。  
3. **禁止**用全库单元数做学生进度分母。  
4. **禁止**换题改 unit_id。  
5. 口语未规划的 P3 等不要臆造单元。  
6. 实现前先跑通 Phase 1 试点模块，再批量改各科深链。  
7. 所有日期用上海时区。  
8. **禁止**合并计划轨与测试轨为一个进度百分比或一条进度条。  
9. **禁止** `not_in_plan` 科目从进度表提供学习入口（学生端）。  
10. **禁止**任务模式下显示模块全库题量/组量作为「总进度」。  
11. **禁止**任务模式下「下一课/下一单元」导航（D25）。  
12. **禁止**用阶段测 `stage_test` 记录抬高测试轨 bestScore（D21）。  
13. **禁止**自由练调用 `complete-study`（D22）。  
14. **禁止**队首测挂死后自动跳过清单顺序（D24）。  
15. **禁止**清单内重复同一 `unit_id` 的 study（D26）。  
16. **禁止**仅用 localStorage 作为 `scope_done` 权威来源（D27）。  
17. **禁止**从学生 ③ 详情进模块学习（D30）。  
18. MVP **禁止**实现「紧急重算今日」（D29）。  
19. 与本文冲突的「优化」先记 TODO，勿擅自改产品规则。  

---

## 17. 一句话总结

**表：单元目录 + 每生画像 + 有序清单 + 日任务物化；算法：换题重学 → 昨日未完 → 队首装箱；完成：学打勾 / 测过关分离；进度：计划轨 X/Y、测试轨 %/分、任务模式本单元 scope 三层并列；单元切分与深链以 §5、§10 为准。**
