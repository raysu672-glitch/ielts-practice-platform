# P4 跟读测试 - 后端说明

本目录包含两个后端版本，二选一即可。

## 版本对比

| 文件 | 识别方式 | 服务器要求 | 特点 |
|---|---|---|---|
| `app.py` | 本地 Whisper small.en | 内存 ≥ 4G 较稳 | 完全免费，离线可用，首启慢 |
| `app_tencent.py` | 腾讯云 ASR 录音文件识别 | 2 核 2G 足够 | 按量计费，识别快，无需下载模型 |

## 腾讯云 ASR 版（推荐 2 核 2G 服务器）

### 1. 开通服务

1. 登录 [腾讯云语音识别控制台](https://console.cloud.tencent.com/asr)
2. 开通「录音文件识别」服务
3. 进入 [API 密钥管理](https://console.cloud.tencent.com/cam/capi) 创建 SecretId 和 SecretKey
4. （可选）关闭后付费，使用每月 10 小时免费额度

### 2. 安装依赖

```bash
cd g:\P4跟读\P4genduceshi\backend
python -m pip install -r requirements_tencent.txt
```

### 3. 配置密钥

**方式一：命令行临时设置（测试用）**

```powershell
$env:TENCENT_SECRET_ID="你的 SecretId"
$env:TENCENT_SECRET_KEY="你的 SecretKey"
$env:TENCENT_REGION="ap-shanghai"
```

**方式二：PowerShell 永久配置（推荐）**

```powershell
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_ID", "你的 SecretId", "User")
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_KEY", "你的 SecretKey", "User")
[Environment]::SetEnvironmentVariable("TENCENT_REGION", "ap-shanghai", "User")
```

设置后需要重新打开终端。

### 4. 启动后端

```bash
cd g:\P4跟读\P4genduceshi\backend
python -m uvicorn app_tencent:app --host 0.0.0.0 --port 8000
```

### 5. 启动前端

```bash
cd g:\P4跟读\P4genduceshi
python -m http.server 8080
```

浏览器打开：http://localhost:8080

### 6. 费用说明

- 每月免费 10 小时录音文件识别额度
- 超出后约 1.75 元/小时（后付费）
- 4 分钟音频一次约 0.12 元

## 本地 Whisper 版

适合配置较高的服务器或本机测试。

```bash
cd g:\P4跟读\P4genduceshi\backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

首次启动会自动加载 `models/small.en.pb`（约 466MB），需要 4G 以上内存更稳。

## 前端 API 地址

前端 `index.html` 中的 `API_BASE` 默认是：

```javascript
const API_BASE = 'http://localhost:8000';
```

部署到服务器时，改成你的后端地址即可。
