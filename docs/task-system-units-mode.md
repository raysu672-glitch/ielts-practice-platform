# 任务系统 · 按科每日单元数排程

> **与时间模式对照**：[`task-system-spec.md`](task-system-spec.md)（按每日时长装箱）  
> **版本记录**：[`VERSIONS.md`](VERSIONS.md)

## 概述

`pack_mode = units_per_day` 时，系统**不再**用周中/周末分钟预算切任务，改为：

- 每科独立按清单 `sort_order` 逐日释放；
- 每科可设 **周中每天几个**、**周末每天几个**（周六日共用周末配额）；
- 多科同日合并展示，条内顺序仍用多科轮换（`_interleave_by_module`）。

默认仍为 `time_budget`（时间装箱），老学生数据零行为变化。

## 数据

### `student_time_profiles`

| 字段 | 说明 |
|------|------|
| `pack_mode` | `time_budget`（默认）或 `units_per_day` |
| `pending_pack_mode` | 待生效模式 |

分钟相关字段在时间模式下继续使用；单元模式下仍保留但不参与装箱。

### `student_module_daily_quota`

| 字段 | 说明 |
|------|------|
| `student_id`, `module_type` | 主键 |
| `weekday_units` / `weekend_units` | 生效中配额，默认 1 |
| `pending_weekday_units` / `pending_weekend_units` | 待生效 |

仅清单里出现过的科目需要在教师端配置；未配置时按 **1** 计。

## 装箱优先级（D8 延续）

1. **换题重学**（`need_refresh=1`）：强制加入，不计入当日配额。
2. **积压**（D23）：曾进入 `daily_tasks` 且未完成 → **按科优先装入，但不超过该科当日配额**；多出的积压留待后续日（看板「积压」总数仍统计全部未完成）。
3. **新释放**：该科尚未出现在任何 `daily_tasks` 的 pending 条，按 `sort_order` 取前 `max(0, quota − 当日该科已装入的积压条数)` 条。

## API

- `GET/PUT /api/task/students/:id/time-profile`：含 `pack_mode`、`module_quotas[]`。
- `POST .../pack-preview`：body 可传 `pack_mode`、`module_quotas` 试算；单元模式响应含 `schedule[]`（最多 14 天试算）。
- `GET /api/task/me/today`：增加 `pack_mode`、`units_total`。

## 教师 UI

任务计划页 → **排程模式**：

- **按每日时长**：原周中/周末分钟 + 保存排程设置。
- **按科每日单元**：配额表（清单内科目 × 周中/周末每天几个）+ 装箱预览（今日 + 后续试算）。

生效日与清单相同：默认明天；选「今天」保存后立即重排今日 `daily_tasks`。

## 实现入口

- 分支：[`scripts/task_api.py`](../scripts/task_api.py) `build_daily_tasks` → `_build_daily_tasks_units`
- 测试：[`tests/test_task_api.py`](../tests/test_task_api.py) `test_units_mode_*`
