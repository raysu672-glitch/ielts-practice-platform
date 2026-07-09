# 阅读同义替换测试

本目录是阅读同义替换测试模块，用于无提示测试模式，完成后向主站上报测试结果。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试页主体、题库、计时、结果页和上报逻辑 |
| `logo.png` | 模块品牌图 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/tongyitihuanceshi/` |
| 主站模式 | iframe |
| `module_type` | `reading_synonym` |
| 测试上报 | `postMessage` 发送 `genericTestComplete` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 分数口径 | 结果分数应保持百分比，主站负责计算达标线 |
| 上报字段 | 保持 `score`、`correct_count`、`total_count`、`duration_seconds` 可用 |
| 验证方式 | 从主站进入测试，完成后在教师端“测试记录”中查看 |
