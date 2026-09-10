import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from oss_sign import is_safe_oss_key, oss_configured, sign_get_url  # noqa: E402


SAMPLE_SETTINGS = {
    "access_key_id": "LTAItestkey",
    "access_key_secret": "secret-for-tests",
    "bucket": "oyenglish-luboke",
    "endpoint": "oss-cn-shanghai.aliyuncs.com",
    "expires_seconds": 7200,
}


class OssSignTests(unittest.TestCase):
    def test_rejects_path_traversal(self) -> None:
        self.assertFalse(is_safe_oss_key("../secret.mp4"))
        self.assertFalse(is_safe_oss_key("courses/../../etc/passwd"))
        self.assertTrue(is_safe_oss_key("courses/测试1-1如何阅读长难句.mp4"))

    def test_sign_url_contains_params_and_encodes_chinese(self) -> None:
        url = sign_get_url(
            "courses/测试1-1如何阅读长难句.mp4",
            expires_at=2000000000,
            settings=SAMPLE_SETTINGS,
        )
        self.assertTrue(url.startswith("https://oyenglish-luboke.oss-cn-shanghai.aliyuncs.com/courses/"))
        self.assertIn("%E6%B5%8B%E8%AF%95", url)
        self.assertIn("OSSAccessKeyId=LTAItestkey", url)
        self.assertIn("Expires=2000000000", url)
        self.assertIn("Signature=", url)
        self.assertNotIn("secret-for-tests", url)

    def test_same_inputs_same_signature(self) -> None:
        a = sign_get_url("courses/a.mp4", expires_at=2000000000, settings=SAMPLE_SETTINGS)
        b = sign_get_url("courses/a.mp4", expires_at=2000000000, settings=SAMPLE_SETTINGS)
        self.assertEqual(a, b)

    def test_configured_requires_keys(self) -> None:
        self.assertTrue(oss_configured(SAMPLE_SETTINGS))
        empty = dict(SAMPLE_SETTINGS)
        empty["access_key_secret"] = ""
        self.assertFalse(oss_configured(empty))

    def test_missing_config_raises(self) -> None:
        blank = dict(SAMPLE_SETTINGS)
        blank["access_key_id"] = ""
        blank["access_key_secret"] = ""
        with self.assertRaises(RuntimeError):
            sign_get_url("courses/a.mp4", expires_at=2000000000, settings=blank)


if __name__ == "__main__":
    unittest.main()
