# 线上各模块测试通过情况（test_records）

| 模块 | 尝试 | 通过 | 通过率 | 均分 | 中位 | 最高 | 阈值 | 0 分次数 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| reading_synonym | 197 | 81 | 41.1% | 58.1 | 74.0 | 100.0 | 79 | 4 |
| dictation (random) | 93 | 8 | 8.6% | 62.6 | 62.0 | 94.0 | 81 | 1 |
| sentence | 81 | 64 | 79.0% | 82.7 | 88.0 | 100.0 | 74 | 3 |
| writing_phrase | 23 | 4 | 17.4% | 38.7 | 45.0 | 75.0 | 69 | 6 |
| speaking (speaking_ai_score) | 20 | 8 | 40.0% | 5.8 | 6.0 | 6.5 | 6 | 0 |
| listening_synonym | 15 | 5 | 33.3% | 62.7 | 60.0 | 90.0 | 81 | 0 |
| listening_basic (random) | 13 | 0 | 0.0% | 40.9 | 44.0 | 74.0 | 81 | 1 |
| writing_translate | 11 | 0 | 0.0% | 0.0 | 0.0 | 0.0 | 70 | 11 |
| listening_p4_speed | 2 | 0 | 0.0% | 40.4 | 40.4 | 71.2 | 80 | 0 |
| listening_basic (stage_test) | 1 | 1 | 100.0% | 85.0 | 85.0 | 85.0 | 80 | 0 |
| mock_reading (mock_exam) | 1 | 0 | 0.0% | 70.0 | 70.0 | 70.0 | 80 | 0 |
| reading_p1 (mock_exam) | 1 | 1 | 100.0% | 11.0 | 11.0 | 11.0 | 11 | 0 |
| reading_p2 (mock_exam) | 1 | 0 | 0.0% | 8.0 | 8.0 | 8.0 | 10 | 0 |
| reading_p3 (mock_exam) | 1 | 1 | 100.0% | 9.0 | 9.0 | 9.0 | 6 | 0 |

## 通过率为 0 或极低（尝试 >= 5）的模块
  - **listening_basic**：尝试 13 次，0 次通过，均分 40.9，阈值 81
  - **writing_translate**：尝试 11 次，0 次通过，均分 0.0，阈值 70

## plan_items 阶段测未通过数（按模块）
  - listening_basic: 5 个，通过 1 个
  - reading_synonym: 4 个，通过 0 个