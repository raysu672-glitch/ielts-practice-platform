# 写作词伙测试

本目录是写作词伙测试模块，用于英文拼写测试，完成后向主站上报结果。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试页主体、题目生成、结果统计和上报逻辑 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/xiezuocihuoceshi/` |
| 主站模式 | iframe |
| `module_type` | `writing_phrase` |
| 测试上报 | `postMessage` 发送 `genericTestComplete` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 题量口径 | 调整题量时同步确认结果页和上报总数 |
| 上报字段 | 保持 `score`、`correct_count`、`total_count`、`duration_seconds` 可用 |
| 验证方式 | 完成一次测试后，在教师端查看写作词伙测试记录 |
