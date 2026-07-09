# 写作词伙学习

本目录是写作词伙分类学习模块，提供词伙记忆、分类练习和学习流程。

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 学习页入口和页面容器 |
| `categories.js` | 词伙分类数据 |
| `game.js` | 练习流程和交互逻辑 |
| `game_test.js` | 简单脚本测试入口 |
| `index_part1.txt`、`index_part2.txt`、`test.txt` | 历史拆分/调试文件，修改前确认是否仍被使用 |

## 接入方式

| 项目 | 配置 |
|---|---|
| 访问路径 | `/xiezuocihuo/` |
| 主站模式 | iframe |
| `module_type` | `writing_phrase` |
| 学习记录 | 主站根据 iframe 打开时长写入 `study_sessions` |

## 维护注意

| 项目 | 要求 |
|---|---|
| 数据维护 | 新增词伙优先改 `categories.js` |
| 逻辑维护 | 练习状态和计分逻辑在 `game.js` |
| 验证方式 | 从主站进入学习页，完成一次练习并返回主页 |
