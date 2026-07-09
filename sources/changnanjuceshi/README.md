# 长难句测试

本目录是长难句测试模块，用于结构填空和结果统计，完成后向主站上报测试结果。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试页主体、题目、答案判定、结果详情和上报逻辑 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/changnanjuceshi/` |
| 主站模式 | iframe |
| `module_type` | `sentence` |
| 测试上报 | `postMessage` 发送 `genericTestComplete` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 判分口径 | 修改题目数量时同步检查正确率计算 |
| 上报字段 | 保持 `score`、`correct_count`、`total_count`、`duration_seconds` 可用 |
| 验证方式 | 完成测试后，在教师端“学习进度”按长难句模块筛选 |
