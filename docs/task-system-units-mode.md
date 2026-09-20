# 任务系统 · 按科每日单元数排程

> **与时间模式对照**：[`task-system-spec.md`](task-system-spec.md)（历史「按每日时长装箱」设计）  
> **版本记录**：[`VERSIONS.md`](VERSIONS.md)

## 概述

**装箱只按「按科每日单元数」**：`time_budget`（按周中/周末分钟装箱）已下线。

- 每科独立按清单 `sort_order` 逐日释放；
- 每科可设 **周中每天几个**、**周末每天几个**（周六日共用周末配额）；配额填 `0` 表示当天不排这科，**可以只排周末**（例：周中 `0`、周末 `1`）。`0` 是有效值，不会被当成「未设置」兜底成 `1`。
- 多科同日合并展示，条内顺序仍用多科轮换（`_interleave_by_module`）。

周中/周末**分钟数字段仍保留**（`student_time_profiles.weekday_minutes` / `weekend_minutes`），
但**不再参与装箱，也不再在界面上展示**（每日任务上的「预计时长 / 预算」已全部去掉）。
数据库字段仅为兼容旧数据保留，接口仍会返回，前端不再渲染。
老档案里残留的 `pack_mode = 'time_budget'` 会被忽略，仍按单元配额排程。

## 数据

### `student_time_profiles`

| 字段 | 说明 |
|------|------|
| `pack_mode` | 恒为 `units_per_day`（`time_budget` 仅历史值，读旧数据时忽略） |
| `pending_pack_mode` | 历史字段，不再写入 |

分钟相关字段（`weekday_minutes` / `weekend_minutes`）仅为兼容旧数据保留，不参与装箱、不在界面展示。

### `student_module_daily_quota`

| 字段 | 说明 |
|------|------|
| `student_id`, `module_type` | 主键 |
| `weekday_units` / `weekend_units` | 生效中配额，默认 1 |
| `pending_weekday_units` / `pending_weekend_units` | 待生效 |

仅清单里出现过的科目需要在教师端配置；未配置时按 **1** 计。

## 装箱优先级（D8 延续）

1. **换题重学**（`need_refresh=1`）：强制加入，不计入当日配额。
2. **积压**（D23）：曾进入 **今天之前** 某日 `daily_tasks` 且未完成 → **按科优先装入，但不超过该科当日配额**；多出的积压留待后续日。这里是**打包器**口径，用于决定优先补做谁。
   > **看板「积压」数字口径不同（D23 v4，2026-09-20）**：改为**昨天那批学习任务里还没做完的条数（不含阶段测——测不算任务量）**。今天没做完是正常的、不算积压；昨天派的任务本身含「前天积压过来的 carry_over」，所以昨天都做完了看板积压就必须是 0。阶段测另有一列「待通过阶段测」，其中「累计考 ≥3 次仍未过」显示 `N 项 多次未过`。
   > 打包时阶段测 **不占配额**（2026-09-20 第四次修订）：只要该科当天有配额、且它覆盖的单元都学完了，测就跟着一起派下去。
3. **新释放**：该科尚未出现在任何 `daily_tasks` 的 pending 条，按 `sort_order` 取前 `max(0, quota − 当日该科已装入的积压条数)` 条。

## API

- `GET/PUT /api/task/students/:id/time-profile`：含 `pack_mode`（恒 `units_per_day`）、`module_quotas[]`；PUT 传 `pack_mode='time_budget'` 会被拒绝（400）。
- `POST .../pack-preview`：body 只接受 `pack_mode='units_per_day'`、`module_quotas` 试算；响应含 `schedule[]`（最多 14 天试算）。
- `GET /api/task/me/today`：含 `pack_mode`、`units_total`。

## 教师 UI

任务计划页 → **排程模式**：只剩 **按科每日单元**——

配额表（清单内科目 × 周中/周末每天几个，可填 0 跳过该科）+ 装箱预览（今日 + 后续试算）。

生效日与清单相同：默认明天；选「今天」保存后立即重排今日 `daily_tasks`。

## 听力跟读特例

`listening_p4_speed` 走独立作业表 `student_gendu_assignment`（助教选起点课，默认 30 天窗口）：

- 窗口内每日只释放**当前课**；日练满 3 次记当日完成；识别率 ≥70% 则次日切下一篇。
- API：`PUT/GET .../gendu-assignment`、`POST .../gendu-assignment/clear`、学生 `POST /api/task/me/gendu-practice`。

## 实现入口

- 分支：[`scripts/task_api.py`](../scripts/task_api.py) `build_daily_tasks` → `_build_daily_tasks_units`
- 测试：[`tests/test_task_api.py`](../tests/test_task_api.py) `test_units_mode_*`、`test_gendu_*`
