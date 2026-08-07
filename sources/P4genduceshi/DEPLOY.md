# P4 跟读测试 - 部署指南

> 目标：前端用 GitHub Pages，后端用你的阿里云 Debian 服务器。
> 后端用 **8000 端口**，和现有网站的 80/443 端口不冲突。

---

## 目录

1. [准备后端代码](#1-准备后端代码)
2. [上传后端到服务器](#2-上传后端到服务器)
3. [配置腾讯云密钥](#3-配置腾讯云密钥)
4. [运行部署脚本](#4-运行部署脚本)
5. [放行 8000 端口](#5-放行-8000-端口)
6. [部署前端到 GitHub Pages](#6-部署前端到-github-pages)
7. [修改前端 API 地址](#7-修改前端-api-地址)
8. [测试](#8-测试)
9. [常用命令](#9-常用命令)

---

## 1. 准备后端代码

在你的 Windows 电脑上，进入项目目录：

```powershell
cd g:\P4跟读\P4genduceshi
```

确认 `backend` 目录里有这些文件：

```
backend/
├── app_tencent.py          # 腾讯云 ASR 后端
├── app.py                  # 本地 Whisper 后端（备用）
├── requirements_tencent.txt
├── p4-backend.service      # systemd 服务文件
├── deploy.sh               # 一键部署脚本
├── ffmpeg.exe              # 音频处理
└── models/
    └── small.en.pb         # Whisper 模型（本地版用）
```

---

## 2. 上传后端到服务器

### 2.1 把整个 backend 目录打包

在 Windows PowerShell 里执行：

```powershell
cd g:\P4跟读\P4genduceshi
Compress-Archive -Path backend -DestinationPath backend.zip -Force
```

会生成 `backend.zip` 文件。

### 2.2 把压缩包传到服务器

你可以用任意方式上传，比如：

- **FinalShell / Xshell / WinSCP** 等工具直接拖拽上传
- **SCP 命令**（如果你本地有 scp）：

```bash
scp backend.zip root@你的服务器IP:/root/
```

### 2.3 在服务器上解压

SSH 连接服务器后执行：

```bash
cd /root
unzip -o backend.zip
mv backend p4-backend-temp
```

---

## 3. 配置腾讯云密钥

编辑服务器上的服务文件：

```bash
nano /root/p4-backend-temp/p4-backend.service
```

把里面的：

```
Environment="TENCENT_SECRET_ID=你的SecretId"
Environment="TENCENT_SECRET_KEY=你的SecretKey"
```

改成你真实的密钥，例如：

```
Environment="TENCENT_SECRET_ID=YOUR_SECRET_ID_HERE"
Environment="TENCENT_SECRET_KEY=YOUR_SECRET_KEY_HERE"
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

---

## 4. 运行部署脚本

给脚本执行权限并运行：

```bash
cd /root/p4-backend-temp
chmod +x deploy.sh
./deploy.sh
```

脚本会自动完成：

- 安装 Python、ffmpeg 等依赖
- 创建 `/opt/p4-backend` 应用目录
- 创建 Python 虚拟环境
- 安装 Python 依赖
- 注册 systemd 服务并启动

看到 `=== 部署完成 ===` 就是成功了。

### 查看状态

```bash
systemctl status p4-backend
```

### 查看日志

```bash
journalctl -u p4-backend -f
```

---

## 5. 放行 8000 端口

### 5.1 阿里云安全组放行

1. 登录 [阿里云 ECS 控制台](https://ecs.console.aliyun.com/)
2. 找到你的服务器，点击「安全组」
3. 点击「配置规则」→「入方向」→「手动添加」
4. 添加一条规则：
   - 协议类型：自定义 TCP
   - 端口范围：8000/8000
   - 授权对象：0.0.0.0/0
   - 描述：P4 backend
5. 保存

### 5.2 服务器防火墙放行（如果开了 ufw）

```bash
ufw allow 8000/tcp
ufw reload
```

或者如果是 `iptables`：

```bash
iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
```

---

## 6. 部署前端到 GitHub Pages

### 6.1 创建 GitHub 仓库

1. 打开 [GitHub](https://github.com/)，新建仓库，名字叫 `P4genduceshi`
2. 不要勾选 README，保持空仓库

### 6.2 把本地代码推送到 GitHub

在 Windows PowerShell 里执行：

```powershell
cd g:\P4跟读\P4genduceshi
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin https://github.com/你的GitHub用户名/P4genduceshi.git
git push -u origin main
```

### 6.3 开启 GitHub Pages

1. 进入仓库页面，点击「Settings」
2. 左侧选择「Pages」
3. Source 选择「Deploy from a branch」
4. Branch 选择「main」，文件夹选择「/(root)」
5. 点击 Save

等待几分钟后，会生成一个网址：

```
https://你的GitHub用户名.github.io/P4genduceshi/
```

---

## 7. 修改前端 API 地址

编辑本地 `config.js`：

```javascript
window.API_CONFIG = {
    API_BASE: 'http://你的服务器公网IP:8000'
};
```

然后重新提交并推送：

```powershell
cd g:\P4跟读\P4genduceshi
git add config.js
git commit -m "update api base"
git push
```

等待 GitHub Pages 自动更新（一般 1-2 分钟）。

---

## 8. 测试

### 8.1 测试后端

在浏览器或命令行访问：

```
http://你的服务器公网IP:8000/
```

应该返回：

```json
{"message":"P4 Shadow Reading Backend (Tencent ASR) is running"}
```

### 8.2 测试前端

打开 GitHub Pages 地址：

```
https://你的GitHub用户名.github.io/P4genduceshi/
```

点击「开始测试」，跟读完整段音频，看是否能正常出分。

---

## 9. 常用命令

| 命令 | 作用 |
|---|---|
| `systemctl status p4-backend` | 查看后端运行状态 |
| `systemctl start p4-backend` | 启动后端 |
| `systemctl stop p4-backend` | 停止后端 |
| `systemctl restart p4-backend` | 重启后端 |
| `journalctl -u p4-backend -f` | 实时查看日志 |
| `netstat -tlnp \| grep 8000` | 查看 8000 端口是否在监听 |

---

## 常见问题

### Q: 后端启动失败，提示找不到 ffmpeg？

A: 部署脚本已经会安装 ffmpeg。如果还是失败，手动安装：

```bash
apt-get update
apt-get install -y ffmpeg
```

### Q: 前端提示「识别失败」？

A: 检查：

1. 服务器 8000 端口是否放行
2. `config.js` 里的 `API_BASE` 是否填对了服务器公网 IP
3. 后端服务是否正常运行：`systemctl status p4-backend`

### Q: 服务器上已有网站，会不会冲突？

A: 不会。现有网站一般用 80/443 端口，后端用 8000 端口，互不干扰。
