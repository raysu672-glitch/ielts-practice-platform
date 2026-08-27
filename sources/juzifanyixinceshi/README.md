# 写作句子翻译测试

本目录是写作句子翻译测试模块：给出英文，学生输入中文；标点可不一致，用词需一致。完成后向主站上报结果。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 测试页、判分、结果统计和上报 |
| `match.js` | 中文比对（忽略空白与标点） |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/juzifanyixinceshi/` |
| 主站模式 | iframe |
| `module_type` | `writing_translate` |
| 题库 | `../juzifanyixin/translation_data.json` |
| 测试上报 | `postMessage` 发送 `genericTestComplete` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 题量口径 | 默认随机 10 句；错题本测试为 5 句（入口未接时不影响本页） |
| 上报字段 | 保持 `scorePercent`、`correctCount`、`totalCount`、`durationSeconds`、`details` |
| 验证方式 | 完成一次测试后，在教师端查看写作句子翻译测试记录 |
