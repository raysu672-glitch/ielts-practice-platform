# 其他训练捷径：真实操作分析（2026-10-10 ~ 10-19）

数据：`aliyun_20261019_155050/ielts_local.db`
句子翻译已改，本报告聚焦其余模块。

## 1. 近10天完成任务按模块

- `listening_basic` rule=`four_stage_completed` done_study: 186
- `reading_synonym` rule=`all_subgroups_once` done_study: 87
- `writing_phrase` rule=`phrases_once` done_study: 74
- `listening_p4_speed` rule=`asr_ge_70` done_study: 72
- `writing_translate` rule=`items_once` done_study: 37
- `listening_synonym` rule=`questions_once` done_study: 36
- `sentence` rule=`sentences_once` done_study: 27
- `dictation` rule=`four_stage_completed` done_study: 17
- `speaking_complex` rule=`three_tracks` done_study: 9

## 2. 跟读：完成日分数分布（有真实证据）

- 跟读事件日（≥3次）：72 天次
- 疑似凑次数（≥2次<10分，或均分<40且含极低分）：**5** 天次
- 均分≥70：42 天次

### 凑次数样例（按均分升序，最多20）
- 宋知宸(2025118) 2026-10-10: [76.3, 0.2, 0.2] 均分25.6 极低分×2 最高76.3
- 宋知宸(2025118) 2026-10-11: [79.0, 1.3, 2.0] 均分27.4 极低分×2 最高79.0
- 蔡璐阳(2025171) 2026-10-14: [3.0, 84.8, 5.0] 均分30.9 极低分×2 最高84.8
- 蔡璐阳(2025171) 2026-10-12: [87.1, 2.9, 2.9] 均分31.0 极低分×2 最高87.1
- 韩彦平(2025123) 2026-10-11: [0.0, 24.4, 75.6] 均分33.3 极低分×1 最高75.6

### 任务状态 vs 跟读分

- daily 跟读相关 done 行：72
- 其中 best_score<40：1
  - 茗琬 2026-10-17 count=0 best=None mod=listening_p4_speed

## 3. 同义替换：完成速度（activity）

- `synonym.group_done`: 1384
- `task.scope_progress`: 916
- `task.exit`: 212
- `task.open`: 161
- `task.complete_ok`: 122

### study_sessions 同义相关时长

- `listening_synonym`: n=53 avg=142s <60s=22 <180s=42 avg_groups=0.0 avg_score=None
- `reading_synonym`: n=161 avg=524s <60s=31 <180s=33 avg_groups=0.0 avg_score=None

### 同义会话：组数多且时长短

- （无：阈值≥5 且 <15s/组）

## 4. 词伙 / 听写 / 基础词：短时完成

### 写作词伙（时长 1–120s 样例）
- 史雯玄 2026-10-16: 3s words=0 groups=0 score=None `writing_phrase`/写作词伙
- 宋知宸 2026-10-15: 4s words=0 groups=0 score=None `writing_phrase`/写作词伙
- 何佳懿 2026-10-10: 5s words=0 groups=0 score=None `writing_phrase`/写作词伙
- 贺煦雯 2026-10-11: 5s words=0 groups=0 score=None `writing_phrase`/写作词伙
- 测试学生 2026-10-12: 5s words=20 groups=0 score=None `writing_phrase`/写作词伙
- 贺煦雯 2026-10-10: 8s words=20 groups=0 score=None `writing_phrase`/写作词伙
- 贺煦雯 2026-10-10: 8s words=20 groups=0 score=None `writing_phrase`/写作词伙
- 程舒彦 2026-10-11: 8s words=20 groups=0 score=None `writing_phrase`/写作词伙

### 听写（时长 1–120s 样例）
- 贺煦雯 2026-10-10: 3s words=0 groups=0 score=None `dictation`/听力1000词
- 王志睿 2026-10-17: 3s words=0 groups=0 score=None `dictation`/听力1000词
- 贺煦雯 2026-10-10: 4s words=0 groups=0 score=None `dictation`/听力1000词
- 田雨涵 2026-10-14: 4s words=0 groups=0 score=None `dictation`/听力1000词
- 曹雅淇 2026-10-17: 4s words=20 groups=0 score=None `dictation`/听力1000词
- 王志睿 2026-10-17: 4s words=0 groups=0 score=None `dictation`/听力1000词
- 王志睿 2026-10-17: 5s words=0 groups=0 score=None `dictation`/听力1000词
- 程舒彦 2026-10-12: 6s words=0 groups=0 score=None `dictation`/听力1000词

### 基础词（时长 1–120s 样例）
- 贺煦雯 2026-10-10: 3s words=50 groups=12 score=None `listening_basic`/听力基础词汇
- 张雪萌 2026-10-11: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 周晓阳 2026-10-12: 3s words=50 groups=0 score=None `listening_basic`/听力基础词汇
- 周晓阳 2026-10-12: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 金娜钰 2026-10-15: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 王皓佟 2026-10-15: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 金娜钰 2026-10-16: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 蔡璐阳 2026-10-17: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇

### basic（时长 1–120s 样例）
- 贺煦雯 2026-10-10: 3s words=50 groups=12 score=None `listening_basic`/听力基础词汇
- 张雪萌 2026-10-11: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 周晓阳 2026-10-12: 3s words=50 groups=0 score=None `listening_basic`/听力基础词汇
- 周晓阳 2026-10-12: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 金娜钰 2026-10-15: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 王皓佟 2026-10-15: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 金娜钰 2026-10-16: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇
- 蔡璐阳 2026-10-17: 3s words=0 groups=0 score=None `listening_basic`/听力基础词汇

### 长难句（时长 1–120s 样例）
- 王志睿 2026-10-17: 3s words=0 groups=0 score=None `sentence`/长难句分析
- 王志睿 2026-10-10: 4s words=0 groups=0 score=None `sentence`/长难句分析
- 贺煦雯 2026-10-10: 4s words=0 groups=0 score=None `sentence`/长难句分析
- 贺煦雯 2026-10-11: 4s words=0 groups=0 score=None `sentence`/长难句分析
- 谷韵涵 2026-10-12: 4s words=0 groups=0 score=None `sentence`/长难句分析
- 贺煦雯 2026-10-10: 6s words=0 groups=0 score=None `sentence`/长难句分析
- 廉昕 2026-10-13: 6s words=0 groups=0 score=None `sentence`/长难句分析
- 廉昕 2026-10-13: 9s words=0 groups=0 score=None `sentence`/长难句分析

### 复杂句（时长 1–120s 样例）
- 陈俣暄 2026-10-17: 4s words=1 groups=0 score=None `speaking_complex`/speaking_complex
- 王若溪 2026-10-10: 10s words=0 groups=0 score=None `speaking_complex`/speaking_complex
- 王若溪 2026-10-10: 15s words=0 groups=0 score=None `speaking_complex`/speaking_complex
- 陈俣暄 2026-10-17: 21s words=0 groups=0 score=None `speaking_complex`/speaking_complex

### 口语（时长 1–120s 样例）
- 周雅文 2026-10-13: 2s words=0 groups=0 score=None `speaking`/口语练习
- 陈俣暄 2026-10-17: 4s words=1 groups=0 score=None `speaking_complex`/speaking_complex
- 王若溪 2026-10-10: 10s words=0 groups=0 score=None `speaking_complex`/speaking_complex
- 王若溪 2026-10-10: 15s words=0 groups=0 score=None `speaking_complex`/speaking_complex
- 贺煦雯 2026-10-10: 19s words=1 groups=0 score=None `speaking`/口语练习
- 陈俣暄 2026-10-17: 21s words=0 groups=0 score=None `speaking_complex`/speaking_complex
- 叶梓晗 2026-10-10: 22s words=1 groups=0 score=None `speaking`/口语练习
- 田雨涵 2026-10-12: 27s words=1 groups=0 score=None `speaking`/口语练习

## 5. 各 module_type 会话时长分布（近10天）

- `listening_basic`: n=374 avg=956s 0s=0 <1′=117 1–5′=22 ≥5′=235
- `listening_p4_speed`: n=189 avg=380s 0s=0 <1′=47 1–5′=65 ≥5′=77
- `reading_synonym`: n=161 avg=524s 0s=0 <1′=31 1–5′=14 ≥5′=116
- `writing_phrase`: n=111 avg=678s 0s=0 <1′=16 1–5′=9 ≥5′=86
- `sentence`: n=71 avg=474s 0s=0 <1′=13 1–5′=37 ≥5′=21
- `writing_translate`: n=59 avg=841s 0s=0 <1′=12 1–5′=4 ≥5′=43
- `listening_synonym`: n=53 avg=142s 0s=0 <1′=22 1–5′=24 ≥5′=7
- `dictation`: n=38 avg=204s 0s=0 <1′=20 1–5′=5 ≥5′=13
- `vocab`: n=24 avg=54s 0s=0 <1′=17 1–5′=7 ≥5′=0
- `listening_p1`: n=4 avg=15s 0s=0 <1′=4 1–5′=0 ≥5′=0
- `speaking`: n=4 avg=18s 0s=0 <1′=4 1–5′=0 ≥5′=0
- `speaking_complex`: n=4 avg=12s 0s=0 <1′=4 1–5′=0 ≥5′=0
- `reading_p1`: n=2 avg=8s 0s=0 <1′=2 1–5′=0 ≥5′=0
- `writing_correction`: n=2 avg=18s 0s=0 <1′=2 1–5′=0 ≥5′=0
- `placement`: n=1 avg=163s 0s=0 <1′=0 1–5′=1 ≥5′=0
- `reading_p3`: n=1 avg=4s 0s=0 <1′=1 1–5′=0 ≥5′=0

## 6. activity_events 高频 action

- `translate.step_submit` / writing_translate: 1464
- `synonym.group_done` / reading_synonym: 1384
- `sentence.drag_result` / sentence: 974
- `task.scope_progress` / reading_synonym: 882
- `sentence.abc_submit` / sentence: 758
- `task.open` / listening_p4_speed: 343
- `task.open` / listening_basic: 271
- `translate.open` / writing_translate: 270
- `auth.login` / : 234
- `task.scope_progress` / writing_translate: 229
- `translate.sentence_done` / writing_translate: 229
- `sentence.open` / sentence: 205
- `task.exit` / listening_p4_speed: 186
- `task.complete_ok` / listening_basic: 172
- `sentence.translate_submit` / sentence: 158
- `task.exit` / reading_synonym: 158
- `sentence.analysis_open` / sentence: 148
- `task.scope_progress` / sentence: 148
- `task.open` / reading_synonym: 110
- `task.open` / writing_phrase: 106
- `task.exit` / writing_phrase: 105
- `task.scope_progress` / speaking_complex: 92
- `task.scope_progress` / writing_phrase: 90
- `task.complete_ok` / reading_synonym: 88
- `task.complete_ok` / writing_phrase: 74
- `task.exit` / sentence: 72
- `plan.save` / : 67
- `task.open` / writing_translate: 66
- `task.open` / sentence: 64
- `task.exit` / writing_translate: 60
- `task.exit` / listening_synonym: 54
- `task.open` / listening_synonym: 51
- `task.complete_ok` / writing_translate: 40
- `translate.unit_done` / writing_translate: 40
- `auth.logout` / : 38
- `task.complete_ok` / listening_synonym: 34
- `task.scope_progress` / listening_synonym: 34
- `sentence.unit_done` / sentence: 29
- `task.complete_ok` / sentence: 29
- `task.exit` / vocab: 24

## 7. 对照：翻译错后速改（仍可见，已做防粘贴）

- 仍命中「错后≤20s改对 ≥30%且≥30次」：**8** 人（防粘贴上线前窗口）
  - 岳浩杰(2025093): 54/118=46%
  - 庞哲文(2025117): 77/169=46%
  - 姜子禄(2025086): 61/146=42%
  - 曹雅淇(2025066): 66/158=42%
  - 商娇龙(2025062): 26/65=40%
  - 张芷玉(2025151): 82/235=35%
  - 王伊泽(2025047): 10/30=33%
  - 王若溪(2025050): 48/149=32%

## 8. 结论（操作证据 × 产品机制）

### 证据最硬（建议优先堵）
1. **跟读 P4**：库内 `gendu_practice_events` 明确存在「一天三次、多次接近 0 分仍完成」。完成条件是次数不是分数。
2. **同义替换**：存在「多组 / 极短时长」会话；机制上点参照词确认可整组认领，错了还 Reveal 答案。
3. **听写/基础词 / 词伙**：代码层无质量门槛；短时会话在会话表里可见（需结合模块名核对）。

### 机制风险大、日志证据偏弱
4. **口语 P2 素材**：自点「已过」即可，无录音门槛。
5. **长难句**：任意翻译可开解析计进度。
6. **口语 P1**：≥1 秒录音即计一题。
7. **通用 API**：`scope-progress` 只认数字，理论上可灌进度（日志未必区分）。

### 相对难走过场
8. **口语复杂句三步**：跟读/脱口需 ASR 分词全对（仍可听音频跟读）。

