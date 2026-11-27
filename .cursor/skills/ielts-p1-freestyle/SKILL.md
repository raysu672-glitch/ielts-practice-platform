---
name: ielts-p1-freestyle
description: >-
  雅思口语 Part 1 可控 Freestyle：共享生活素材库、同一题多套素材、同一素材挂多题。
  当要写/改 P1 示范、增减素材、对齐五类四步、或避免硬套素材时使用。
  对应仓库 scripts/p1_material_bank.py、scripts/p1_packs/、refresh_p1_samples.py。
---
用共享生活素材库答雅思口语 Part 1：步骤名称不动，换的是步骤下面的素材。同一题换素材就是不同回答；同一条素材可以挂到多道相关题上。

## 硬规则

1. **五大题型、每类四步官方名称一律不动。** 换题型时，仍用该题型自己的四步去填，不另起一套步骤。
2. 用户口头说的「来源或起源」「频率」，对应的是事实陈述类的「来源或举例」「频次」。行为习惯类仍用「原因 / 时间线+行为描述 / 影响」。
3. **只把在雅思哥 / 易答官网上实际看到的题面当官网原文。** 未登录往往只能看到话题标题，加「口语题库」里每题一道示范小问。第三方题单不可冒充雅思哥原文。未看到的小问不要编造。
4. **示范目标 Band 6 能开口口语**，不要词块硬拼，不要写成小作文。
5. **对不上的题不要硬套素材。** 例如黄色自行车可以挂到童年活动、一天中学、公园、疲倦后怎么放松；不要默认挂到拾金不昧、折纸、名字等题。
6. **选题单位是「题」不是「话题」。** 同一话题下各题重点不同，可用不同素材；共享库可跨题复用，但某题对不上就不出现。优先写 `QUESTION_KIT_ALLOW`（`p1_material_bank.py`）；通常每题 **2 套**合法料即可，不必同话题硬凑同一套，也**不必凑满 3 套**。
7. **先扣题，再轻带素材。** 示范主线必须直接回答题干；素材只润色举例/场景，绝不能抢成「书桌专题 / 笔记专题 / 素材故事」。
8. **按单题预览页做，做完一题复核一题。** 对齐 `sources/kouyulianxi/p1-freestyle-preview.html`：答题思路 → 四步词卡 → 示范；不要批量灌模板后才检查。

## Band 6 用词与句式（强制）

**要用（日常可说）：** busy, tired, useful, interesting, a bit hard, happy, OK, clear, job, degree, internship, classes, library, walk, bike, short videos。

**少用/不用（偏书面或偏难）：** purposeful, ambitious, optimistic, productive, structured, engaged, energising, surprisingly, graduate hire, trainee, analyst, specialise/specialize, formal internship, recommendations, margin notes, huddles, not impulsive, FOMO, data-driven, fascinating, personalised。

**句式（看意图，不机械数句号）：**
- 示范须覆盖本题型四步：正面 → 举例/原因 → 频次/时间线 → 感受/影响（对比类则两面+感受）。
- **优先约四句、一步一句**；正面可拆成两句短句（如 `I'm a student. I don't have a job yet.`），不算跑偏。
- 先正面回答题干，再带素材细节。
- 身份题开句点明 student / work；选专业/几年后用简单 job / internship / degree 说法。

反例：`get a trainee or analyst job` / `The tidy habit supports the work`。  
正例：`I'm a student. I don't have a job yet.` / `In a few years I want to finish my degree and find a job.`

## 答题流程

1. 记下官方题面（完整问句，含问号）和话题。
2. 判断五类之一，写出该类官方四步标题。
3. 按**本题**选能扣题的套装（可与同话题其它题不同）；至少两套；写入/核对 `QUESTION_KIT_ALLOW`。
4. 按四步填词卡；感受/影响常承接前一步动机。
5. 写成 Band 6 口语；复核：扣题、不硬套、不超难、四步意图齐。
6. 一题过关再下一题；改完 `refresh_p1_samples.py` + packs/full_fit/qa_fit 审计 + bump `?v=`。

## 落地进度（改别的话题时接着做）

| 状态 | 话题 |
|---|---|
| 已试点 | 当前仓库内全部 P1 话题均已写入题级 `QUESTION_KIT_ALLOW`（含 Opportunities / Science 补全）；示范按题拆套 + Band 6 口语 |
| 复盘时 | 单题预览页抽查；新季加题仍按「题级选材 → pack → 复核 → refresh」 |

新季加题后不要默认「全库已改完」；只保证当季已挂白名单的题达标。

## 五类官方步骤（不可改名）

| 题型 | 官方步骤（按顺序） |
|---|---|
| 事实陈述类 | 正面回答 / 来源或举例 / 频次 / 感受 |
| 喜好类 | 正面回答 / 原因或时间 / 频次 / 感受 |
| 行为习惯类 | 正面回答 / 原因 / 时间线+行为描述 / 影响 |
| 观点类 | 正面回答 / 举例或原因 / 作用或影响 / 感受 |
| 对比类 | 正面回答 / 选项1的特点与作用 / 选项2的特点与作用 / 个人感受 |

默认填槽：

- 事实陈述：正面用语 → 来源/细节（可带行为） → 时间/频次 → 感受
- 喜好：正面用语 → 原因或时间 → 频次 → 感受
- 行为习惯：正面用语 → 原因 → 时间线+行为描述 → 影响
- 观点：正面用语 → 举例或原因 → 作用或影响 → 感受
- 对比：正面用语 → 选项1 → 选项2 → 个人感受

## 共享素材怎么准备

库里是可复用的生活条目，不属于某一道题。基本类型：

- `affirm` 正面用语：Yes / definitely / not really / it depends
- `behavior` 行为/爱好：ride my bike to school；go cycling in the park；take the subway；watch short videos；hang out with friends
- `origin` 来源/细节：a small yellow bike my mum bought me as a junior-high birthday gift；a subway station about a ten-minute walk from home
- `time` 时间/频次：every day；at weekends；after dinner；in junior high
- `feeling` 感受/影响：really convenient；saves time；to keep fit；helps me unwind

生活套装可一次选中，也必须能拆开重配：

- **每天骑车上学**：妈妈的黄色小自行车 + 每天骑去上学 + 通勤方便
- **周末公园骑行**：同一辆车 + 周末在公园骑一小时 + 锻炼、放松
- **地铁通勤**：家附近地铁/公交 + 每天上学 + 方便省时
- **刷短视频/聚会**：看短视频或和朋友出去 + 晚饭后/周末 + 解压放松

词块只是提示用词，不能用词块拼接代替口语示范，也不要把套装再写成第二篇冻结范文。

## 踩坑清单（本轮已验证，必须遵守）

### 不要硬挂的素材

| 素材 | 不要挂到 | 原因 |
|---|---|---|
| `tidy_desk_habit`（书桌整洁） | Work or studies 各题（身份/选专业/难点/喜欢/一天/几年后） | 一提就变整洁专题，文不对题 |
| `handwritten_notes_paper`（手写笔记） | 同上；凑第三套时尤其违和 | 「必须有第三套」是假需求 |
| 短视频 `douyin_scroll_habit` | 「童年如何解闷」类题 | 童年场景不自然 |
| 学校实验室等 | 「科学如何影响日常生活」 | 课堂实验 ≠ 日常生活 |
| `subway_bus_commute` | 「童年汽车旅程」类题 | 答成大巴/地铁 = 没答 car |

### 同一话题也要按题拆套

示例（已写入 `QUESTION_KIT_ALLOW`）：

- Work or studies 身份/日常 → 上课图书馆 + 商科日常  
- Work or studies 几年后 → 商科日常 + 校园机会通知（不是图书馆硬凑）  
- Feeling bored 童年 → 黄自行车 + 公园（去掉短视频）  
- Cars 有无车/怎么出行 → 地铁通勤 + 全家开车乘客  
- Cars 童年车程 → 全家开车 + 回乡小吃车程（**不要**地铁包）  
- Watch 各题 → 普通表礼物 + 手机看时间（两套对立答法即可）  
- Home 住哪/和谁 → 宿舍生活 + 父母家（**不要**书桌整洁抢戏）  
- Tiredness 影响学习 → 图书馆上课 + 公园恢复；为何很多人累 → 短视频熬夜 + 户外少  
- Travelling 靠窗 → 地铁/火车窗位 + 全家车后座窗（**不要**硬挂骑车）  
- City 天气 → 地铁通勤 + 查天气工具（**不要**广告屏）  
- Area 住多久 → 宿舍 + 地铁择居（公园只作设施/喜好题）  
- Politeness → 说谢谢 + 耐心老师（**不要**昵称抢戏）  
- Clothing 童年谁选衣 → T恤外套/卫衣（镜子留给「花时间选衣」）  
- Social media 常用 App → 微信小红书 + 抖音（聚会喜剧勿硬凑第三套）  
- Ads 童年广告 → 地铁屏/电视糖果歌（勿写成刷小红书）  

### 示范质检（写完必过）

1. **扣题**：去掉素材细节后，是否仍直接回答该问句？  
2. **四步意图**：正面→举例/原因→频次或时间线→感受/影响是否齐全？（约四句；正面两短句可）  
3. **不抢戏**：素材是否只占举例/场景，没有变成主线故事？  
4. **Band 6**：有无书面大词？学生能否不背稿开口？  
5. **换料换答**：同题两套素材示范不得同文。  
6. **身份/职业**：身份题开句点明学生或工作；几年后题有简单的 degree/job/internship 语言。

## 当季试答示范（2026 年 9–12 月雅思哥公开小问）

下列题面均摘自 https://www.yida.school/question-bank/ 「口语题库」未登录预览（季度标 2026年9-12月）。每题只有一道公开小问；`已练 0/N` 表明还有未公开的小问，不要补编。

### 1. 同一题，换两套素材

**Do you often feel bored?**（Feeling bored，新题，事实陈述类：正面回答 / 来源或举例 / 频次 / 感受）

素材 A（刷短视频/聚会）：

> Not really, to be honest. After a long day I usually watch short videos or hang out with my friends, so I don't get bored easily. I do this most evenings, or at weekends if we have time. It helps me switch off and feel more relaxed.

素材 B（周末公园骑行）：

> Sometimes, especially during the week when I've been sitting in class all day. When that happens, I like to take my bike to the park and go for a ride. I usually do that at weekends, for about an hour. It gives me something to do, and it also helps me unwind.

### 2. 同一条素材，挂到不同题（一套黄自行车）

**Did you have any opportunities to take part in new activities as a child?**（Opportunities，新题，事实陈述类）

> Yes, I did. When I was in junior high, my mum bought me a small yellow bike as a birthday gift, and that was the first time I really started cycling on my own. I rode it to school every day after that, even when the weather wasn't great. It was a new kind of freedom for me, and I found it really convenient.

**Do you remember your first day at secondary school?**（Secondary school，新题，事实陈述类）

> Yes, I remember it quite clearly. That was around the time my mum bought me a small yellow bike as a birthday gift, and I rode it to school on the first day. I was a bit nervous in the morning, but I got there early and didn't get stuck in traffic. It felt like a fresh start, and the bike made me feel a bit more independent.

同一辆车，换成「周末公园」后可再挂到：

**Did you like going to parks as a child?**（Public gardens and parks，保留题，喜好类：正面回答 / 原因或时间 / 频次 / 感受）

> Yes, I really did. There was a park near my home, and it was a nice place to get some fresh air and run around. I used to go there quite often after school, especially at weekends. I have good memories of it, and I still like going to parks now — sometimes I take my bike and ride there for about an hour.

### 3. 换题型时仍用该类自己的四步名

**How important are friends to you?**（Friends，新题，观点类：正面回答 / 举例或原因 / 作用或影响 / 感受）

素材：刷短视频/聚会（步骤不要写成「来源或举例 / 频次」）

> They're really important to me. After a long day, I often hang out with my friends — we'll grab something to eat or just chat for a bit. It helps me relieve stress and forget about study for a while. I feel much more relaxed when I've spent time with them.

**What do you do when you see rubbish on the street?**（Rubbish and recycling，新题，行为习惯类：正面回答 / 原因 / 时间线+行为描述 / 影响）

不硬套自行车故事：

> I usually pick it up if it's not too dirty. I don't like seeing the street messy, especially near where I live. When I notice a bottle or a piece of paper on the pavement, I'll put it in the nearest bin on my way. It's a small thing, but it makes the area nicer, and I feel better doing it.

**Do you prefer to sit by the window when travelling?**（Travelling，新题，对比类：正面回答 / 选项1的特点与作用 / 选项2的特点与作用 / 个人感受）

> I'd say I prefer the window. Sitting by the window, I can look at the scenery, and the journey feels a bit shorter. An aisle seat is easier if I need to get up, but I find it noisier and a bit cramped. Personally, I feel more comfortable by the window, especially on a long trip.

### 4. Work or studies 身份题（Band 6 + 先扣题）

**Do you work or are you a student?**（事实陈述类）

素材：上课与图书馆

> I'm a student. I don't have a job yet. I go to classes in the day and study in the library with friends in the evening. I do that most weekdays, from Monday to Friday. I feel busy, and sometimes a bit tired.

禁止把书桌整洁/手写笔记写成主线。

## 从雅思哥更新当季题

1. 先打 https://next.ieltsbro.com/oral_season/ ，记下季度名、更新日期、P1 新题/保留题标题，以及更新图里的大陆/非大陆分类（若有）。点话题可能跳出应用宝下载页，那里没有小问，停下即可。
2. 再打 https://www.yida.school/question-bank/ 的「口语题库」（不是「新题题库」）。用 全部 / 人物 / 事物 / 事件 / 地点 筛选，未登录每题通常只有一道示范小问。「新题题库」可能是旧季快照，不要和当季混用。
3. 「查看全部题库」、「开始练习」或点话题卡片，通常会弹出微信登录。登录后才能补齐完整小问；没登录就只用已看到的原文试答。
4. 换季后重走上述步骤，更新附录题单和试答；方法本身不变。

## 附录：2026 年 9–12 月公开题面（截至 2026-11-26，未登录）

来源：https://next.ieltsbro.com/oral_season/ （题库更新动态至 10 月 22 日；P1 更新时间曾显示 2026-09-20）；小问来自 https://www.yida.school/question-bank/ 「口语题库」筛选预览。

**P1 新题 17（页序）：** Feeling bored, Computers/tablets, Collecting things, Lost and found, Street market, Opportunities, Secondary school, Paper, Fruit and vegetables, Politeness, Tiredness, Rubbish and recycling, Travelling, Advertisement, Friends, Shoes, Name。

更新图拆分：大陆 11 道 Travelling, Rubbish and recycling, Tiredness, Shoes, Politeness, Fruit and vegetables, Advertisement, Paper, Secondary school, Name, Opportunities；非大陆 6 道 Lost and found, Computers/tablets, Collecting things, Street market, Feeling bored, Friends。

**P1 保留 22：** Watch, Cars, Websites, Mirrors, Public gardens and parks, Shopping, Tidiness, Music, Teachers, Social media, Clothing, The city you live in, Outer space and stars, Morning time, Singing, Science, Headphones, Jokes & Comedies, Work or studies, Home & Accommodation, Hometown, The area you live in。站点未单独标「必考」；Work or studies, Home & Accommodation, Hometown, The area you live in 在保留题里。

**已见公开示范小问（每题仅 1 问）：**

- Feeling bored（0/4）Do you often feel bored?
- Computers/tablets（0/5）Would you like to use a computer or tablet?
- Collecting things（0/4）Do you collect things?
- Lost and found（0/5）What will you do if you find something lost by others?
- Street market（0/4）What do people usually buy on the street market？（全角问号）
- Opportunities（0/4）Did you have any opportunities to take part in new activities as a child?
- Politeness（0/4）How did you learn to be polite as a child?
- Friends（0/9）How important are friends to you?
- Secondary school（0/4）Do you remember your first day at secondary school?
- Paper（0/5）Have you made any crafts with paper?
- Fruit and vegetables（0/5）How often do you eat fruit and vegetables?
- Rubbish and recycling（0/4）What do you do when you see rubbish on the street?
- Tiredness（0/4）Do you often feel tired?
- Travelling（0/4）Do you prefer to sit by the window when travelling?
- Teachers（0/6）Do you have a favorite teacher?
- Work or studies（0/22）What subjects are you studying?
- Shopping（0/4）Do you like shopping?
- Public gardens and parks（0/8）Did you like going to parks as a child?
- The city you live in（0/11）What city do you live in?
- Home & Accommodation（0/17）Who do you live with?
- Hometown（0/15）Have you learned anything about the history of your hometown?
- The area you live in（0/7）Are the people in your neighborhood nice and friendly?

未登录时未见公开小问的新题：Advertisement, Shoes, Name。部分保留题也无公开小问，勿补编。

## 本仓库对接（实现时遵守）

- 五类四步名：`scripts/p1_word_banks_core.py` → `CAT_STEPS`（勿改名）。
- 素材库：`scripts/p1_material_bank.py` → `MATERIALS` + `MATERIAL_TOPIC_ALLOW` + **`QUESTION_KIT_ALLOW`（题级优先）** + 可选 `qHints`。
- **单题制作流程（与 `p1-freestyle-preview.html` 一致，优先）**：在 `scripts/p1_packs/*.py` 为每个 `(题面, kitId)` 写清 `logic` / `kitHint` / `words` / `sample` / `sampleZh`。对不上的素材不要挂进本题。做完一题复核一题。
- 改完跑：`python scripts/refresh_p1_samples.py`；再跑 `audit_p1_packs.py` / `audit_p1_full_fit.py` / `audit_p1_qa_fit.py`（`missing=0`、`misfits=0`、`same_sample=0`）。
- 示范必须跟素材变：优先 freestyle pack → 手写 kit 样本 → kit-story；禁止多素材同文。
- 前端：改数据后 bump `sources/kouyulianxi/index.html` 的 `?v=`；素材切换器在 `app.js`。
- 审计注意：`QUESTION_KIT_ALLOW` 允许跨话题池挂真正扣题的套装；`audit_p1_full_fit` 已认可题级白名单。
