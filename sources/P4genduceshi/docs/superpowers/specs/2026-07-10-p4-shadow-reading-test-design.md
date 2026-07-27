# P4 跟读测试网站设计文档

## 1. 项目背景与目标

基于 `raysu672-glitch/P4gendu` 影子跟读练习工具，新建独立仓库 `P4genduceshi`，实现一个**P4 跟读测试页面**。学生在浏览器中打开页面后，点击唯一的“测试”按钮，原音频和学生录音同时开始；音频播放结束后自动停止录音，系统通过浏览器语音识别将学生录音转文字，并与原文进行 LCS 比对，最终给出百分制分数和录音回放。

## 2. 范围与阶段

### 阶段 A（本设计）：单文件原型验证
- 所有 HTML、CSS、JS 内嵌在 `index.html` 中。
- 仅支持内置课程 `C4T1S4 - Urban Landscape`。
- 目标：快速在本地跑通核心流程，验证语音识别 + LCS 评分效果。

### 阶段 B（后续）：三文件结构
- 验证通过后，将 `index.html` 拆分为 `index.html`、`styles.css`、`script.js`。
- 保留相同功能和数据，优化可维护性。

## 3. 文件结构（阶段 A）

```
P4genduceshi/
├── index.html          # 包含全部 HTML + CSS + JS
├── C4T1S4.mp3          # 从 P4gendu 复制的音频文件
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-07-10-p4-shadow-reading-test-design.md
```

## 4. 功能需求

### 4.1 页面布局

1. **顶部标题区**：显示“P4 跟读测试”及当前课程名 `C4T1S4 - Urban Landscape`。
2. **评分标准说明**：在“测试”按钮下方用文字说明评分规则。
3. **“测试”按钮**：页面唯一主按钮，状态随流程变化：
   - 准备阶段：显示“开始测试”。
   - 测试中：显示“测试中...”并禁用，防止重复点击。
   - 评分中：显示“正在评分...”。
   - 测试完成：显示“重新测试”。
4. **原文显示区**：全程显示英文原文，便于学生跟读。
5. **进度条**：显示当前音频/录音进度。
6. **结果区**：测试结束后显示分数（如 `85%`）和学生录音播放器。
7. **历史记录区**：列出最近几次测试的分数和时间戳。

### 4.2 核心流程

1. 用户点击“开始测试”。
2. 请求麦克风权限，创建 `MediaRecorder`。
3. 同时启动：
   - `audioPlayer.play()` 播放 `C4T1S4.mp3`。
   - `mediaRecorder.start()` 开始录音。
4. 监听 `audioPlayer.ended` 事件：
   - 调用 `mediaRecorder.stop()` 停止录音。
   - 进入“评分中”状态。
5. 使用 `webkitSpeechRecognition` / `SpeechRecognition` 将录音转文字。
6. 对原文和识别结果预处理：转小写、去掉标点。
7. 使用 LCS 算法计算最长公共单词序列长度。
8. 计算分数：
   ```
   score = round((lcsLength / originalWords.length) * 100)
   ```
9. 显示分数、录音回放，并将 `{score, timestamp}` 写入 `localStorage`。
10. 用户可点击“重新测试”再次进行。

### 4.3 评分标准

- **预处理规则**：
  - 统一转换为小写。
  - 使用正则表达式移除常见标点：`.,!?;:'"()-`。
- **分词规则**：按空白字符 `split(/\s+/)`。
- **匹配规则**：以单词为单位计算最长公共子序列（LCS）。
- **得分规则**：
  ```
  得分 = LCS 长度 / 原文单词总数 × 100，四舍五入到整数。
  ```
- **示例**：
  - 原文 100 词，识别结果与原文最长公共子序列 85 词，则得分 85%。

## 5. 技术实现

### 5.1 技术栈

- 纯前端静态页面，无后端。
- HTML5、CSS3、原生 JavaScript。
- Web Speech API（`SpeechRecognition`）用于语音识别。
- MediaRecorder API 用于录音。

### 5.2 关键 API

| API | 用途 |
|---|---|
| `navigator.mediaDevices.getUserMedia({ audio: true })` | 获取麦克风权限 |
| `MediaRecorder` | 录制学生音频 |
| `Audio` / `<audio>` | 播放原音频 |
| `SpeechRecognition` / `webkitSpeechRecognition` | 将学生录音转为文字 |
| `localStorage` | 保存测试历史 |

### 5.3 状态管理

使用全局状态对象管理测试流程：

```javascript
const state = {
  isTesting: false,
  isScoring: false,
  audioPlayer: null,
  mediaRecorder: null,
  recordedChunks: [],
  recognition: null,
  currentLesson: { ... },
  userRecordingBlob: null,
  lastResult: null
};
```

### 5.4 LCS 算法

```javascript
function lcsLength(arr1, arr2) {
  const m = arr1.length;
  const n = arr2.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (arr1[i - 1] === arr2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[m][n];
}
```

## 6. 错误处理

| 场景 | 处理方式 |
|---|---|
| 浏览器不支持 `SpeechRecognition` | 提示换用 Chrome / Edge / Safari，并给出原始录音回放。 |
| 麦克风权限被拒绝 | 提示检查浏览器权限设置，按钮恢复可用。 |
| 音频加载失败 | 提示刷新页面重试。 |
| 语音识别未返回结果 | 本次测试按 0 分处理，允许重新测试。 |
| 测试过程中用户刷新页面 | 录音丢失，不保存结果，回到准备状态。 |

## 7. 本地验证计划

1. 将 `C4T1S4.mp3` 复制到 `P4genduceshi/` 目录。
2. 用本地服务器启动（推荐 `python -m http.server`，因为部分浏览器对 `file://` 协议限制麦克风访问）。
3. 分别进行三类测试：
   - **正常朗读**：观察分数是否接近 90% 以上。
   - **故意漏读部分单词**：观察分数是否明显下降。
   - **故意多读/改词**：观察分数变化是否合理。
4. 检查历史记录是否正确写入 `localStorage`。
5. 验证录音回放是否正常。

## 8. 阶段 B 规划

阶段 A 验证通过后，将 `index.html` 拆分为：

```
P4genduceshi/
├── index.html
├── styles.css
├── script.js
└── C4T1S4.mp3
```

拆分时不改变功能逻辑，仅做代码组织优化。

## 9. 非目标（本阶段不做）

- 不接入后端或第三方语音识别服务。
- 不支持多课程切换。
- 不支持自定义上传音频/文本。
- 不推送到 GitHub（阶段 A 仅在本地验证）。
