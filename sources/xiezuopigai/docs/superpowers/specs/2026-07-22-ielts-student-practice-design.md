# 雅思写作学生自动改错训练页设计文档

## 1. 背景与目标

### 1.1 问题背景

当前项目已有两个 HTML 原型：

- `ielts-grammar-coach-prototype.html`：学生改错视图，侧重单题推进与老师审核。
- `ielts-sentence-checkpoints-prototype.html`：老师工作台，支持老师手动为每句添加检查点。

这两个原型验证了"逐句全改"的教学流程，但检查点均由老师手动创建，学生无法独立完成训练。

### 1.2 本次目标

新增一个独立的学生训练页面 `ielts-student-practice.html`，实现：

1. 学生输入名字并上传/粘贴自己的作文。
2. 系统通过前端规则库自动识别作文中的常见语法错误。
3. 学生按四层阶梯完成每个检查点：自己找错 → 标红错误位置 → 提示错误类型 → 查看正确答案与规则。
4. 练习结果保存到 Supabase，便于后续统计与语法画像。

## 2. 功能范围

### 2.1 包含功能

- 学生名字输入。
- 作文粘贴与 `.txt` 文件上传。
- 自动按句子拆分作文。
- 前端规则库扫描，自动生成检查点（至少 50 条规则）。
- 逐句展示检查点，四层提示阶梯。
- 学生答案输入与正确性比对。
- 即时统计：完成率、错误类型分布、提示依赖度。
- 练习结果保存到 Supabase（essays + practice_results 两张表）。
- 响应式布局，适配桌面与平板。

### 2.2 不包含功能

- 学生登录/认证（仅用名字标识）。
- AI 自动生成检查点（本次采用前端规则匹配）。
- 老师审核界面（保留原有老师工作台，未来可扩展）。
- 跨作文的复发率追踪（本次仅保存单篇结果，画像功能后续迭代）。

## 3. 技术方案

### 3.1 技术栈

- 前端：原生 HTML + CSS + TypeScript（单文件原型）。
- 后端/BaaS：Supabase（PostgreSQL + REST API）。
- 错误检测：前端正则/关键词规则库，无需外部 AI API。

### 3.2 方案选择说明

选择"新建独立学生训练页"而非改造老师工作台，原因是：

- 学生自动训练与老师手动创建检查点是两条不同流程，分开后职责清晰。
- 保留老师工作台，未来可扩展为"AI 生成检查点 + 老师审核"模式。
- 减少原有原型中的老师相关交互残留。

## 4. 页面流程与信息架构

页面为单页应用，分为四个阶段：

### 阶段 1：开始

- 输入学生名字（必填）。
- 粘贴作文或上传 `.txt` 文件。
- 点击"开始改错"进入检测阶段。

### 阶段 2：检测

- 显示加载状态："正在扫描语法错误..."
- 前端规则库逐句扫描作文。
- 生成检查点列表。
- 检测完成后自动进入训练阶段。

### 阶段 3：训练

三栏布局：

- **左栏：作文句子列表**
  - 显示所有句子。
  - 当前句高亮。
  - 已完成句子标记为完成。
  - 点击可切换当前句。

- **中栏：当前句检查点训练**
  - 显示当前句子。
  - 每个检查点一个卡片，包含：
    - 学生修改输入框（初始为空）。
    - "提示位置"按钮：标红错误单词/短语。
    - "提示类型"按钮：显示错误类型。
    - "查看答案"按钮：显示参考修改和规则说明。
    - "提交"按钮：保存学生答案。

- **右栏：即时统计**
  - 完成率、错误类型分布、平均提示层级。
  - 当前学习状态提示。

### 阶段 4：报告

- 显示本篇练习总结：
  - 总检查点数。
  - 已完成数。
  - 各错误类型数量。
  - 平均提示层级。
  - 建议复习点。
- 提供"再练一篇"按钮。
- 自动将结果保存到 Supabase。

## 5. 规则库设计

### 5.1 规则对象结构

```typescript
interface GrammarRule {
  id: string;           // 规则唯一标识，如 "subject-verb-people-who"
  category: string;     // 错误类别，如 "主谓一致"
  pattern: RegExp;      // 匹配正则
  extractHighlight: (match: RegExpMatchArray, sentence: string) => string; // 标红内容
  question: string;     // 开放问题
  hints: string[];      // 分层提示，长度通常为 2-3 条
  answer: string;       // 参考修改后的完整句子（动态替换生成）
  explanation: string;  // 规则说明
}
```

### 5.2 规则分类与数量

规则库总计约 55 条，覆盖 10 个类别：

| 类别 | 数量 | 示例 |
|------|------|------|
| 主谓一致 | 8 | people who lives, the cost are, there is many, the number of students are |
| 冠词使用 | 8 | a important, an university, the education (general), go to school vs go to the school |
| 动词形式 | 8 | spend time to do, enjoy to swim, avoid to do, made him to cry |
| 时态语态 | 6 | yesterday I go, if I will see, the homework did by me, I have went |
| 比较级最高级 | 5 | more healthier, more easier, most fastest, more better |
| 介词搭配 | 6 | depend of, discuss about, different than, married with |
| 名词单复数 | 4 | many student, informations, childs, peoples |
| 形容词副词 | 3 | work hardly, drive careless, speak loud |
| 句子结构 | 4 | run-on sentence, sentence fragment, although...but, however without comma |
| 易混淆词 | 3 | your/you're, its/it's, then/than |

### 5.3 规则匹配策略

1. 按句子逐个扫描。
2. 每个句子可能命中多条规则，每条规则生成一个独立检查点。
3. 同一位置命中多条规则时，按优先级只保留一条（避免重复提示）。
4. 规则采用宽松匹配，宁可漏报也不错报，避免打击学生信心。

### 5.4 答案生成

参考修改通过正则替换动态生成：

- 对于明确替换类错误（如 lives → live），使用 `sentence.replace(pattern, correction)`。
- 对于需要上下文判断的错误（如冠词），提供通用修改模板。
- 若无法生成合理修改，显示规则说明并提示学生参考老师建议。

## 6. 学生交互流程（四层阶梯）

每个检查点的交互分为四层：

### 第 1 层：独立判断

- 只显示原始句子。
- 学生自己找出错误并修改。
- 输入框为空，等待学生填写。
- 按钮："我不知道错在哪"。

### 第 2 层：标红位置

- 学生点击"我不知道错在哪"后：
  - 错误单词/短语标红显示。
  - 不显示错误类型。
- 学生再次尝试修改。
- 按钮："提示错误类型"。

### 第 3 层：提示类型

- 学生点击"提示错误类型"后：
  - 显示错误类型，如"这是一个主谓一致问题"。
  - 可能附带一个定位提示。
- 学生再次尝试修改。
- 按钮："查看答案"。

### 第 4 层：正确答案与规则

- 学生点击"查看答案"后：
  - 显示参考修改后的完整句子。
  - 显示规则说明。
- 学生可复制答案或继续下一题。

### 正确性判断

- 学生每次提交答案后，与 `answer` 进行简单文本比对。
- 完全一致标记为"正确"。
- 部分一致（如仅改了核心错误）标记为"基本正确"。
- 不一致标记为"需复习"。
- 最终保存时使用最高提示层级作为 `hint_level`。

## 7. Supabase 表结构

### 7.1 `essays` 表

存储学生上传的作文元信息。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | 作文唯一标识 |
| student_name | text | NOT NULL | 学生输入的名字 |
| original_text | text | NOT NULL | 原始作文文本 |
| sentences | jsonb | NOT NULL | 拆分后的句子数组，包含 text 和 checkpoints |
| checkpoint_count | int | NOT NULL DEFAULT 0 | 检查点总数 |
| created_at | timestamptz | NOT NULL DEFAULT now() | 创建时间 |

### 7.2 `practice_results` 表

存储每个检查点的练习结果。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | 结果唯一标识 |
| essay_id | uuid | NOT NULL REFERENCES essays(id) | 关联作文 |
| student_name | text | NOT NULL | 学生名字（冗余，便于查询） |
| sentence_index | int | NOT NULL | 句子序号 |
| checkpoint_index | int | NOT NULL | 检查点序号 |
| rule_id | text | NOT NULL | 命中的规则标识 |
| rule_type | text | NOT NULL | 错误类型 |
| hint_level | int | NOT NULL DEFAULT 0 | 学生使用的最高提示层级（0-3） |
| student_answer | text | | 学生最后一次提交的答案 |
| is_correct | boolean | | 是否正确 |
| created_at | timestamptz | NOT NULL DEFAULT now() | 创建时间 |

### 7.3 索引建议

- `practice_results(essay_id)`：按作文查询结果。
- `practice_results(student_name)`：按学生查询历史记录。

## 8. 数据持久化流程

### 8.1 保存时机

1. 作文上传并检测完成后，立即插入 `essays` 表。
2. 学生完成每个检查点时，立即插入或更新 `practice_results` 表。
3. 学生点击"完成训练"时，再次批量保存所有未保存结果（兜底）。

### 8.2 错误处理

- 所有 Supabase 操作使用 `try-catch` 包裹。
- 保存失败时在页面右下角显示 Toast 提示："保存失败，请检查网络连接"。
- 不允许静默失败，错误信息打印到控制台。
- 若保存失败，本地状态保留，学生可继续练习，待网络恢复后重试。

### 8.3 确认机制

- Supabase insert/update 必须等待 `await` 完成后才执行后续操作。
- 保存成功后显示 Toast："已保存"。

## 9. 错误处理与用户提示

### 9.1 前端错误

| 场景 | 处理方式 |
|------|----------|
| 学生未输入名字 | 提示"请输入你的名字" |
| 作文为空 | 提示"请先粘贴或上传作文" |
| 未检测到错误 | 提示"系统暂未发现常见语法错误，建议请老师进一步检查" |
| 规则匹配冲突 | 按优先级去重，避免同一位置多个提示 |

### 9.2 网络错误

| 场景 | 处理方式 |
|------|----------|
| Supabase 保存失败 | Toast 提示保存失败，保留本地状态 |
| Supabase 配置缺失 | 页面加载时检测，提示"缺少数据库配置" |

## 10. 成功标准

### 10.1 功能验收

- [ ] 学生输入名字后上传作文，系统自动拆分句子并生成检查点。
- [ ] 至少 50 条规则能命中常见雅思写作错误。
- [ ] 每个检查点支持四层提示阶梯：自己找 → 标红位置 → 提示类型 → 给答案。
- [ ] 学生提交答案后，系统能判断正确性并保存结果。
- [ ] 练习结果成功保存到 Supabase `essays` 和 `practice_results` 表。
- [ ] 报告页显示完成率、错误类型分布、平均提示层级。

### 10.2 技术验收

- [ ] 代码中无 `any` 类型（TypeScript 严格模式）。
- [ ] 所有异步操作有 `try-catch` 错误处理。
- [ ] Supabase 操作有确认等待机制。
- [ ] 响应式布局在 1140px 以下自动变为单栏。

## 11. 风险与限制

### 11.1 前端规则匹配的局限

- 只能覆盖预设的常见错误模式，无法处理复杂语法错误。
- 可能出现误报（如正确句子被规则命中）或漏报。
- 建议在报告页增加免责声明："系统仅检测常见语法问题，复杂错误请让老师人工检查。"

### 11.2 学生答案比对的局限

- 简单文本比对无法判断语义等价（如同义词替换）。
- 后续可引入更宽松的比对策略（如忽略大小写、标点、部分词汇变化）。

## 12. 实现顺序

本次开发采用"先前端，后后端"的顺序：

### 阶段一：前端完整功能

1. 创建 `ielts-student-practice.html`，实现页面骨架与三栏布局。
2. 实现开始阶段：学生名字输入、作文粘贴、`.txt` 上传。
3. 实现句子拆分逻辑。
4. 实现 55 条前端规则库与检查点自动生成。
5. 实现训练阶段：四层提示阶梯交互、学生答案输入、正确性判断。
6. 实现报告阶段：完成率、错误类型分布、平均提示层级统计。
7. 使用浏览器本地状态（内存 + LocalStorage）保存练习进度，模拟后端保存逻辑。

### 阶段二：接入 Supabase 后端

1. 配置 Supabase 客户端。
2. 创建 `essays` 和 `practice_results` 表。
3. 将本地保存逻辑替换为 Supabase insert/update。
4. 添加网络错误处理与重试机制。
5. 验证数据写入成功。

## 13. 后续迭代方向

1. **AI 辅助生成检查点**：当规则库无法覆盖某类错误时，调用 AI API 补充。
2. **老师审核界面**：让老师查看 AI/规则生成的检查点并进行修改确认。
3. **学生语法画像**：基于 `practice_results` 统计高频错误、提示依赖度、复发率。
4. **写前提醒**：根据历史错误自动生成下一篇作文的检查清单。

## 13. 引用来源

规则库设计参考了以下资料中的常见错误分类与示例：

- Typogrammar: Common Grammar Mistakes in IELTS Writing (15-20 Errors + Fixes) [$TRAE_REF](https://typogrammar.com/ielts/common-grammar-mistakes-ielts-writing/)
- Typogrammar: 50 Common Grammar Mistakes in English [$TRAE_REF](https://typogrammar.com/blog/common-grammar-mistakes-in-english/)
- 英国文化协会：10大常见雅思写作失分点 [$TRAE_REF](https://www.britishcouncil.org.tw/english/exam-preparation/ielts-tips/20-common-mistakes/writing)

## 14. 待确认事项

- [ ] Supabase 项目 URL 和 anon key 是否已有？
- [ ] 是否需要在 Supabase 中提前创建上述两张表？
- [ ] 学生名字是否需要做唯一性或格式校验？
- [ ] 是否需要在检测阶段显示"检测中"的 loading 动画？
