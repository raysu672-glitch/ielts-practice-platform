# 一、残留行检查：条目已完成，daily_tasks 还留着 todo/in_progress？

  **残留行 = 79 条**（条目已达标，却还挂在某天的 todo）
  按状态：{'todo': 79}

| 日期 | 条目 | 模块 | 类型 | 状态 |
|---|---:|---|---|---|
| 2026-09-19 | 609 | dictation | study | todo |
| 2026-09-19 | 625 | reading_synonym | study | todo |
| 2026-09-19 | 644 | speaking_p1 | study | todo |
| 2026-09-19 | 660 | listening_synonym | study | todo |
| 2026-09-19 | 679 | sentence | study | todo |
| 2026-09-19 | 690 | listening_basic | study | todo |
| 2026-09-19 | 698 | writing_phrase | study | todo |
| 2026-09-19 | 711 | writing_translate | study | todo |
| 2026-09-19 | 722 | speaking_complex | study | todo |
| 2026-09-19 | 730 | listening_p4_speed | study | todo |
| 2026-09-22 | 730 | listening_p4_speed | study | todo |
| 2026-09-25 | 612 | dictation | test | todo |
| 2026-09-25 | 628 | reading_synonym | test | todo |
| 2026-09-25 | 647 | speaking_p1 | test | todo |
| 2026-09-25 | 663 | listening_synonym | test | todo |
| 2026-09-25 | 682 | sentence | test | todo |
| 2026-09-25 | 730 | listening_p4_speed | study | todo |
| 2026-09-28 | 614 | dictation | study | todo |
| 2026-09-28 | 630 | reading_synonym | study | todo |
| 2026-09-28 | 649 | speaking_p1 | study | todo |

  这些行的 `task_date` 都在「今天 + 昨天」回写窗口之外 ——
  学生当天确实断更，后来补做时回写窗口已够不到，属于刻意保留（不洗白）。

## 这些残留行会影响哪些显示

  - `backlog_plan_item_ids`：按 `plan_items` 完成标志过滤 → **不影响积压数**
  - `_today_task_counts`：只算「今天/昨天」两天 → **不影响（窗口外的天不展示）**
  - 教师端回看历史某天：会看到那天未完成 → 这是设计意图

# 二、积压口径 vs 派发口径是否自洽

- 积压（统计口径）= 5 条

| 条目 | 模块 | 配额(周中/周末) | 未来 7 天能否被派到 |
|---:|---|---|---|
| 714 | writing_translate | 0/1 | 03-20、03-21 |
| 715 | writing_translate | 0/1 | 03-20、03-21 |
| 716 | writing_translate | 0/1 | 03-20、03-21 |
| 718 | writing_translate | 0/1 | 03-20、03-21 |
| 721 | writing_translate | 0/1 | 03-20、03-21 |

## 结论
  积压里 5 条都在 `writing_translate`（周中 0 / 周末 1）。
  工作日永远派不到；周末每天最多派 1 条，5 条需要 5 个周末，
  而其中 3 条是阶段测，判分 0% 通过 → 即使派到也过不了。
  ⇒ 这 5 条在现有规则下是**数学上无法清除**的。