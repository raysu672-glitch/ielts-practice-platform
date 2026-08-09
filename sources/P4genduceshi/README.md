# 听力 P4 跟读测试

本目录是听力 Part 4 **跟读测试**模块：播放原文并录音跟读，后端 ASR 识别后按匹配率计分。

主站模块 `listening_p4_speed`：

| 环节 | 目录 | 说明 |
|---|---|---|
| 学习 | `sources/P4gendu/` | 倍速跟读练习 |
| 测试 | `sources/P4genduceshi/` | 跟读录音打分（本目录） |

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 测试页（录音、上传、出分） |
| `config.js` | 前端配置（后端地址等） |
| `backend/` | 可选独立 ASR 后端（腾讯云等） |
| `DEPLOY.md` | 部署说明 |

## 接入

| 项目 | 值 |
|---|---|
| 访问路径 | `/P4genduceshi/` |
| 主站 `test_url` | `../P4genduceshi/index.html` |
| 达标单位 | `%`（跟读匹配率） |
| 上报 | `postMessage: genericTestComplete` |
