# 答案句听写测试

本目录是答案句听写测试模块，从答案句题库中抽题测试，完成后向主站上报测试结果。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试页主体、题库、选项判定、结果详情和上报逻辑 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/daanjutingxieceshi/` |
| 主站模式 | iframe |
| `module_type` | `listening_synonym` |
| 测试上报 | `postMessage` 发送 `genericTestComplete` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 抽题数量 | 调整题量时同步检查结果页和总分计算 |
| 上报字段 | 保持 `score`、`correct_count`、`total_count`、`duration_seconds` 可用 |
| 验证方式 | 完成一次测试后，在教师端查看听力同义替换测试记录 |
