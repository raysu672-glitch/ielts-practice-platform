#!/bin/bash
set -e

# P4 跟读测试后端 - Debian/Ubuntu 一键部署脚本
# 运行前请确保：
# 1. 本脚本在服务器上执行
# 2. backend 目录已上传到 /root/p4-backend-temp（或修改 SRC_DIR）
# 3. 已在 p4-backend.service 中填入腾讯云 SecretId 和 SecretKey

SRC_DIR="/root/p4-backend-temp"
APP_DIR="/opt/p4-backend"
SERVICE_FILE="/etc/systemd/system/p4-backend.service"

echo "=== P4 后端部署脚本 ==="

# 1. 安装依赖
echo "[1/6] 安装系统依赖..."
apt-get update
apt-get install -y python3 python3-pip python3-venv ffmpeg curl

# 2. 创建应用目录
echo "[2/6] 创建应用目录..."
mkdir -p "$APP_DIR"

# 3. 复制后端代码
if [ ! -d "$SRC_DIR" ]; then
    echo "错误：找不到源码目录 $SRC_DIR"
    echo "请先把 backend 目录上传到 $SRC_DIR"
    exit 1
fi

echo "[3/6] 复制后端代码..."
cp -r "$SRC_DIR"/* "$APP_DIR/"

# 4. 创建 Python 虚拟环境
echo "[4/6] 创建虚拟环境并安装依赖..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_tencent.txt

# 5. 安装 systemd 服务
echo "[5/6] 安装 systemd 服务..."
if [ -f "$APP_DIR/p4-backend.service" ]; then
    cp "$APP_DIR/p4-backend.service" "$SERVICE_FILE"
    systemctl daemon-reload
    systemctl enable p4-backend
else
    echo "错误：找不到 p4-backend.service 文件"
    exit 1
fi

# 6. 启动服务
echo "[6/6] 启动后端服务..."
systemctl restart p4-backend

echo ""
echo "=== 部署完成 ==="
echo "查看状态: systemctl status p4-backend"
echo "查看日志: journalctl -u p4-backend -f"
echo "测试接口: curl http://<你的服务器公网IP>:8000/"
