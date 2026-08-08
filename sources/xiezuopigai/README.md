# 雅思写作自动改错训练系统

## 项目简介

学生粘贴雅思作文 → 系统自动检测语法错误 → 学生逐句按四层提示阶梯完成改错训练。

错误检测采用**双层机制**：
1. **前端规则引擎**：正则规则覆盖冠词、主谓一致、时态、介词等常见错误，即时运行
2. **AI 补充检测**：调用 DeepSeek 官方 API（`deepseek-v4-flash`），找出规则未覆盖的错误（异步，不阻塞页面）

## 技术栈

| 层 | 技术 | 说明 |
|---|---|---|
| 前端 | 原生 HTML + CSS + JavaScript | 单文件，无构建工具，无框架依赖 |
| 后端 | Python + FastAPI | 提供 AI 语法检测 API + 静态页面托管 |
| AI | DeepSeek API | deepseek-v4-flash，兼容 OpenAI 格式 |

## 文件结构

```
.
├── ielts-student-practice.html   # 前端主文件（2167 行，含 72 条规则）
├── ielts-writing-backend/
│   ├── main.py                   # FastAPI 后端（AI 检测 + 页面托管 + 练习记录）
│   ├── teacher.html              # 老师查看页
│   ├── requirements.txt          # Python 依赖
│   ├── .env                      # 本地环境变量（含 API Key，不上传）
│   ├── .env.example              # 环境变量模板（DeepSeek）
│   ├── server.js                 # [已废弃] 旧 Node.js 后端，勿用
│   ├── routes/grammar.js         # [已废弃] 旧 Node.js 路由
│   ├── services/siliconflow.js   # [已废弃] 旧 Node.js AI 服务
│   └── package.json              # [已废弃] 旧 Node.js 依赖
├── docs/
│   └── superpowers/specs/
│       └── 2026-07-22-ielts-student-practice-design.md  # 设计文档
├── ielts-student-practice-screenshots/  # UI 截图（7 张）
└── README.md                     # 本文件
```

> **注意**：`ielts-writing-backend/` 下的 `server.js`、`routes/`、`services/`、`package.json` 是早期 Node.js 版本的遗留文件，后端已切换为 Python（`main.py`）。这些文件可以安全删除。

## 快速启动

### 1. 安装依赖

```bash
cd ielts-writing-backend
pip install -r requirements.txt
```

### 2. 配置环境变量

平台统一配置在仓库根目录 `config/ai.env`（模板见 `config/ai.env.example`）。  
当前与后续 AI 功能都走这里的 Key/模型，改配置只改这一处。

```env
AI_API_KEY=你的DeepSeek_API_Key
AI_BASE_URL=https://api.deepseek.com
AI_MODEL=deepseek-v4-flash
```

模块目录下的 `.env` 仅作本地兼容回退。  
> API Key 申请：https://platform.deepseek.com  
> 也兼容旧变量名 `SILICONFLOW_API_KEY` / `SILICONFLOW_BASE_URL` / `SILICONFLOW_MODEL`。

### 3. 启动服务

```bash
cd ielts-writing-backend
python main.py
```

启动后访问 http://localhost:8080 即可使用。

后端同时提供：
- `GET /` — 返回前端页面
- `GET /api/health` — 健康检查
- `POST /api/grammar-check` — AI 语法检测接口

## 核心机制说明

### 前端规则引擎

72 条规则定义在 `ielts-student-practice.html` 的 JavaScript 中，每条规则结构：

```javascript
{
  id: "article-a-before-consonant",
  category: "冠词使用",
  pattern: /正则表达式/,
  question: "引导学生发现错误的问句",
  hints: ["渐进式提示1", "提示2"],
  answer: "正确答案",
  explanation: "错误原因说明"
}
```

规则覆盖的类别：冠词使用、主谓一致、动词时态、介词搭配、代词、比较级、名词复数等。

### AI 补充检测流程

```
学生提交作文
  │
  ├─ 1. 前端规则引擎即时扫描 → 生成检查点 → 显示训练页面
  │
  └─ 2. 异步调用 POST /api/grammar-check
         │
         ├─ 发送：作文全文 + 规则已检测到的错误位置
         ├─ AI 返回：JSON 格式的补充错误列表
         ├─ 首次失败 → 自动重试（提高 max_tokens、减少错误数）
         └─ 合并到前端检查点 → 刷新页面
```

### AI 调用参数（main.py）

```python
MAX_TOKENS_DEFAULT = 4500
MAX_TOKENS_RETRY = 6000
MAX_ERRORS_REQUESTED = 12
MAX_ERRORS_RETRY = 8
```

### 四层提示阶梯

| 层级 | 内容 | 触发方式 |
|---|---|---|
| 第 1 层 | 学生自己找错并修改 | 默认 |
| 第 2 层 | 标红错误位置 | 点击"我不知道错在哪" |
| 第 3 层 | 提示错误类型 | 点击"提示错误类型" |
| 第 4 层 | 显示正确答案和规则说明 | 点击"查看答案" |

### 前端关键函数

| 函数 | 位置 | 作用 |
|---|---|---|
| `splitEssayIntoSentences()` | ~L1613 | 按标点拆分作文为句子 |
| `generateCheckpoints()` | ~L1646 | 对单句执行规则匹配，生成检查点 |
| `fetchAiSupplements()` | ~L1682 | 调用后端 AI 接口 |
| `adaptAiCheckpoint()` | ~L1664 | 将 AI 返回的错误适配为前端检查点格式 |
| `startPractice()` | ~L2022 | 核心入口：拆句 → 规则检测 → 显示 → AI 补充 |

## 已知问题与待优化

1. **sentenceIndex 对齐**：后端已用 `originalSentence` 对齐句子索引，极端长句仍可能偶发偏差
2. **无完整账号体系**：学生目前用名字标识，老师页 `/teacher` 可查看练习记录，正式登录后台待完善
3. **API Key 勿提交**：真实 `.env` 已在 `.gitignore` 中，仓库只保留 `.env.example`

## API 接口文档

### POST /api/grammar-check

**请求体：**
```json
{
  "essay": "学生作文全文",
  "existingErrors": [
    {
      "sentenceIndex": 0,
      "matchedText": "前端已检测到的错误文本",
      "ruleId": "rule-id"
    }
  ]
}
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "ai-supplement-0",
      "category": "主谓一致",
      "question": "这句话中的主谓一致是否正确？",
      "hints": ["提示1", "提示2"],
      "explanation": "错误原因说明",
      "corrected": "修正后的文本",
      "aiDetected": true,
      "sentenceIndex": 1,
      "matchedText": "错误文本片段"
    }
  ],
  "meta": {
    "aiDetected": 2,
    "ruleDetected": 1
  }
}
```

## Cursor 开发建议

1. **前端开发**：直接编辑 `ielts-student-practice.html`，无需构建工具，浏览器刷新即可预览
2. **后端开发**：编辑 `ielts-writing-backend/main.py`，`python main.py` 启动，支持 `--reload` 热重载
3. **本地测试**：后根目录运行 `python main.py`，访问 http://localhost:8080
4. **规则扩展**：在 HTML 中搜索 `category:` 找到规则数组，按相同格式添加新规则
5. **AI 调优**：修改 `main.py` 中的 `build_prompt()` 和 `MAX_TOKENS_*` 常量

## 原始设计文档

完整设计文档见 `docs/superpowers/specs/2026-07-22-ielts-student-practice-design.md`。
