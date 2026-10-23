# 判分排查（c1）：判分严格度 vs 达标线 vs 线上实际分数

> 数据来源：线上库备份 `aliyun_20260920_092000`（`_sim_out/online_pass_rates.md`）
> + 本地库 `test_records`。只读排查，**未改动任何代码**。

## 0. 判分在哪算

**所有模块的分数都在学生浏览器里算好，然后 postMessage 给主页面存库。**
服务端只做了两件事：① 达标线不再信客户端（`threshold_for_module`），② 记录分数/对错数。
也就是说，**判分规则本身仍然是前端代码**。改判分 = 改各自模块页的 JS。

| 模块 | 测试页 | 判分实现 | 严格度 |
|------|--------|----------|--------|
| `reading_synonym` | `tongyitihuanceshi` | 选项比对 | 客观 |
| `sentence` | `changnanjuceshi` | 选项/填空比对 | 客观 |
| `listening_synonym` | `daanjutingxieceshi` | 单词/词组比对 | 客观 |
| `writing_phrase` | `xiezuocihuoceshi` | `normalize` 后**字符串全等** | ⚠️ 见 §1 |
| `writing_translate` | `juzifanyixinceshi` | `isChineseMatch` **逐字全等** | ❌ 见 §2 |
| `dictation` / `listening_basic` | 内置听写 | `toLowerCase()` 后**单词全等** | 合理（拼写题） |
| `listening_p4_speed` | `P4genduceshi` | 后端 ASR **词匹配率** | 客观但受识别率限制 |
| `reading_p1–p3` / `listening_p1–p4` | `jianyazhenti` | `grade.ts` 选项比对 | 客观 |

## 1. `writing_phrase`：11 条答案「永远拿不到分」

题库 278 条，其中 **11 条**的 `en` 里含 `/` 或 `()`：

```js
function normalize(s) {
  return s.toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[\/\(\)]/g, ' ')   // ← a/b 变成 'a b'
    .replace(/[.,;:!?'‘’“”]/g, '')
    .replace(/\s+/g, ' ').trim();
}
function isCorrect(user, answer) { return normalize(user) === normalize(answer); }
```

标准答案被规范化成「a b」，学生填 `a` 或 `b` **都判错**，必须把两个说法连着打出来。
命中列表：

- `climb steadily/solidly`
- `continue to increase / soar`
- `a modest dip/drop over the last decade`
- `dip/drop to only 2.5%`
- `remain stable/steady`
- `in the final phase/stage`
- `curb crime / deter crime`
- `be ethically wrong / theoretically wrong`
- `consumer goods /products`
- `digital/online dating`
- `the elderly / the senior population`

**影响量级**：每次抽 20 题，期望撞上 ~0.8 条 → 平均白丢 ~4 分。
达标线 69（6.5 档），所以这不是通过率低的主因（线上 17.4%），但属于**确定性丢分**，
修起来最简单：把答案按 `/` 拆成多个可接受答案。

## 2. `writing_translate`：逐字比对参考译文，通过率 0%

题目是「看英文，写中文」，判分是：

```js
correct = window.TranslateMatch.isChineseMatch(val, q.zh);
// normalizeChinese: 只去空白 + 标点，然后 ua === ca
```

题库 114 句，参考译文长这样：

> `互联网最大的优势在于它极大地简化了人与人之间的沟通。`
> `例如，一些留学的学生无需担心思乡之情带来的困扰，因为他们可以通过 FaceTime 等即时通讯工具与家人保持日常联系。`

学生必须**逐字默写出这段参考中文**才算对。换个说法（哪怕意思完全正确）一律 0 分。

**线上实证**：11 次提交，**11 次 0 分**，均分 0.0，达标线 70 → 通过率 0%。
这不是学生的问题，是判分方式的问题。

## 3. 达标线 vs 实际分数（线上）

| 模块 | 尝试 | 通过率 | 均分 | 中位 | 阈值 | 判定 |
|------|-----:|-------:|-----:|-----:|-----:|------|
| `sentence` | 81 | 79.0% | 82.7 | 88 | 74 | 合理 |
| `reading_synonym` | 197 | 41.1% | 58.1 | 74 | 79 | 偏难，可接受 |
| `speaking` | 20 | 40.0% | 5.8 | 6.0 | 6 | 合理 |
| `listening_synonym` | 15 | 33.3% | 62.7 | 60 | 81 | 偏难 |
| `writing_phrase` | 23 | 17.4% | 38.7 | 45 | 69 | ⚠️ 含 §1 的必错题 |
| `dictation` | 93 | 8.6% | 62.6 | 62 | 81 | ⚠️ 阈值偏高（听写拼写题） |
| `listening_basic` | 13 | **0%** | 40.9 | 44 | 81 | ❌ 13 次 0 过，需人工看题库 |
| `writing_translate` | 11 | **0%** | 0.0 | 0.0 | 70 | ❌ 判分问题（§2） |
| `listening_p4_speed` | 2 | 0% | 40.4 | 40.4 | 80 | 样本太少（ASR 词匹配率） |

`listening_basic` 均分只有 40.9、13 次全不过，和 `dictation`（均分 62.6）差距很大，
**怀疑该模块题库/测试页与 `dictation` 不一致**，需要打开页面实测确认。

## 4. 结论与建议（按性价比排序）

| # | 问题 | 建议 | 风险 |
|---|------|------|------|
| 1 | `writing_phrase` 11 条 `/` 答案必错 | 把 `en` 按 `/` 拆成多个可接受答案，`isCorrect` 改成「任一命中」 | 极低（只放宽） |
| 2 | `writing_translate` 逐字全等 → 0% | 改判分为**关键信息点覆盖**（提取参考译文的实词，算命中比例）或**字符相似度 ≥ 阈值** | 中（要定新口径，且影响自由练） |
| 3 | `dictation` 阈值 81 / 8.6% 通过 | 6.5 档从 80 降到 70（20 词错 6 个以内） | 低（只改 `pass_standards` 一行） |
| 4 | `listening_basic` 0/13 | 人工打开页面实测，确认题目/判分是否正常 | 待查 |
| 5 | 判分全在前端、分数可篡改 | 长期：把关键模块判分搬到服务端 | 高（工程量大） |

前 3 项都是小改动，**建议在本轮发布里一起做**；第 4 项需要先实测。
