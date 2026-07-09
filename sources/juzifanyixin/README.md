# 写作句子翻译

本目录是写作句子翻译学习模块，用于句子翻译练习和答案反馈。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 学习页主体、题目展示和交互逻辑 |
| `translation_data.json` | 翻译题库数据 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/juzifanyixin/` |
| 主站模式 | iframe |
| `module_type` | `writing_translate` |
| 学习记录 | 主站根据 iframe 打开时长写入 `study_sessions` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 数据维护 | 新增题目优先修改 `translation_data.json` |
| 编码要求 | JSON 文件保持 UTF-8，提交前检查格式合法 |
| 验证方式 | 从主站进入学习页，确认题库加载和答案展示正常 |
