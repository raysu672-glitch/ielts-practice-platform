"""
Python 后端接口验证脚本
自动启动服务，测试完自动关闭
"""

import subprocess
import sys
import time
import urllib.request
import urllib.error
import json
import os
import signal

BASE_URL = "http://localhost:3000"
server_process = None


def start_server():
    global server_process
    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # 等待服务启动
    output = ""
    start_time = time.time()
    while time.time() - start_time < 10:
        line = server_process.stdout.readline()
        if line:
            output += line
            if "服务启动于" in line or "Uvicorn running" in line:
                return
        time.sleep(0.1)

    raise RuntimeError(f"服务启动超时\n{output}")


def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


def request(path, method="GET", body=None):
    url = f"{BASE_URL}{path}"
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"status": resp.status, "body": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": json.loads(e.read().decode("utf-8"))}


def run_tests():
    print("启动 Python 后端服务...\n")
    start_server()

    try:
        print("开始验证后端接口...\n")

        # 1. 健康检查
        print("1. 健康检查")
        health = request("/api/health")
        print(f"  状态: {health['status']}")
        print(f"  响应: {health['body']}")
        assert health["status"] == 200 and health["body"].get("status") == "ok", "健康检查失败"

        # 2. 缺少 essay 参数
        print("\n2. 参数校验 - 缺少 essay")
        missing = request("/api/grammar-check", "POST", {"existingErrors": []})
        print(f"  状态: {missing['status']}")
        print(f"  响应: {missing['body']}")
        assert missing["status"] == 400, "缺少 essay 时应返回 400"

        # 3. 正常请求结构（无 API key 时返回空数组）
        print("\n3. 正常请求结构")
        sample_essay = "Many student think that study abroad is good."
        normal = request("/api/grammar-check", "POST", {
            "essay": sample_essay,
            "existingErrors": [
                {"sentenceIndex": 0, "matchedText": "Many student"}
            ]
        })
        print(f"  状态: {normal['status']}")
        print(f"  响应: {json.dumps(normal['body'], ensure_ascii=False, indent=2)}")
        assert normal["status"] == 200, "正常请求应返回 200"
        assert normal["body"].get("success") is True, "应返回 success=true"
        assert isinstance(normal["body"].get("data"), list), "data 应为数组"

        print("\n✅ Python 后端接口结构验证通过")
        print("\n下一步：填入 AI_API_KEY（或 SILICONFLOW_API_KEY）后，用真实 AI 调用再测一次。")
    finally:
        stop_server()


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        stop_server()
        sys.exit(1)
