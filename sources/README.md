# 前端模块目录

`sources/` 是线上静态站点根目录。主站位于 `tinglidanciceshi/`，其他学习和测试模块通过 iframe 接入主站。

## 模块划分

| 模块 | 目录 | `module_type` | 页面入口 | 数据上报 |
|---|---|---|---|---|
| 听力1000词 | `tinglidanciceshi/` | `dictation`、`dictation_learn` | `/tinglidanciceshi/` | 主站直接写入 SQLite/Supabase 适配层 |
| 阅读同义替换学习 | `tongyitihuan/` | `reading_synonym` | `/tongyitihuan/` | 主站记录 iframe 学习时长 |
| 阅读同义替换测试 | `tongyitihuanceshi/` | `reading_synonym` | `/tongyitihuanceshi/` | `postMessage: genericTestComplete` |
| 写作词伙学习 | `xiezuocihuo/` | `writing_phrase` | `/xiezuocihuo/` | 主站记录 iframe 学习时长 |
| 写作词伙测试 | `xiezuocihuoceshi/` | `writing_phrase` | `/xiezuocihuoceshi/` | `postMessage: genericTestComplete` |
| 长难句学习 | `changnanju/` | `sentence` | `/changnanju/` | 主站记录 iframe 学习时长 |
| 长难句测试 | `changnanjuceshi/` | `sentence` | `/changnanjuceshi/` | `postMessage: genericTestComplete` |
| 答案句听写学习 | `daanjutingxie/` | `listening_synonym` | `/daanjutingxie/` | 主站记录 iframe 学习时长 |
| 答案句听写测试 | `daanjutingxieceshi/` | `listening_synonym` | `/daanjutingxieceshi/` | `postMessage: genericTestComplete` |
| 写作句子翻译 | `juzifanyixin/` | `writing_translate` | `/juzifanyixin/` | 主站记录 iframe 学习时长 |
| 听力 P4 跟读学习 | `P4gendu/` | `listening_p4_speed` | `/P4gendu/` | 主站记录 iframe 学习时长 |
| 听力 P4 跟读测试 | `P4genduceshi/` | `listening_p4_speed` | `/P4genduceshi/` | `postMessage: genericTestComplete`（跟读匹配率 %） |
| 口语练习 | `kouyulianxi/` | `speaking` | `/kouyulianxi/` | 学习时长；P1 AI Band → `genericTestComplete` |
| 作文批改 | `xiezuopigai/` | `writing_correction` | `/xiezuopigai/ielts-student-practice.html` | 练习完成后写入写作后端；教师批改见 `ielts-writing-backend/teacher.html`；主站 `/api/writing/*` 代理 |
## 维护规则

| 规则 | 说明 |
|---|---|
| 保持目录名稳定 | 目录名就是线上访问路径，改名会影响主站跳转和历史链接 |
| 公共接入集中维护 | 学生、教师、进度、测试记录逻辑集中在 `tinglidanciceshi/index.html` |
| 模块内改动独立验证 | 修改某个模块后，至少访问对应页面和主站 iframe 入口 |
| 不部署归档目录 | `_zips/` 和 `_extract/` 是历史包和临时解压目录，已被 `.gitignore` 排除 |
| 不提交生产数据 | 数据库文件在 `data/`，不属于静态模块源码 |
| 不提交音频 | `mp3/wav/m4a/ogg` 音频只在本地或服务器本地维护，默认不进入 GitHub 和部署包 |
