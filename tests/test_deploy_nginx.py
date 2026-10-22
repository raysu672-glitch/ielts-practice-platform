import sys
import types
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# 发布工作流先跑测试、后装 paramiko。这里只检查生成的 nginx 文本。
sys.modules.setdefault("paramiko", types.ModuleType("paramiko"))

from deploy import SERVICE_PORT, build_nginx_conf  # noqa: E402


class DeployNginxBodySizeTests(unittest.TestCase):
    def test_p4_upload_location_allows_full_passage(self) -> None:
        for with_https in (False, True):
            conf = build_nginx_conf(with_https=with_https)
            with self.subTest(with_https=with_https):
                start = conf.index("location /api/p4/")
                end = conf.index("location / {", start)
                block = conf[start:end]
                self.assertIn("client_max_body_size 32m;", block)
                self.assertIn("client_body_timeout 300s;", block)
                self.assertIn(f"proxy_pass http://127.0.0.1:{SERVICE_PORT};", block)
                self.assertNotIn("client_max_body_size", conf[end:])

    def test_http_redirect_does_not_proxy_uploads(self) -> None:
        conf = build_nginx_conf(with_https=True)
        redirect, _, https = conf.partition("listen 443 ssl;")
        self.assertIn("return 301 https://$host$request_uri;", redirect)
        self.assertNotIn("location /api/p4/", redirect)
        self.assertIn("location /api/p4/", https)
