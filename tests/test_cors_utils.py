import os
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cors_utils import cors_headers_for_origin, is_allowed_cors_origin


class CorsUtilsTests(unittest.TestCase):
    def test_allows_production_origin(self) -> None:
        origin = "https://training.oyenglish.com.cn"
        self.assertTrue(is_allowed_cors_origin(origin))
        headers = cors_headers_for_origin(origin)
        self.assertEqual(headers["Access-Control-Allow-Origin"], origin)
        self.assertEqual(headers["Access-Control-Allow-Credentials"], "true")

    def test_allows_localhost_http_any_port(self) -> None:
        for origin in (
            "http://127.0.0.1:49182",
            "http://localhost:49247",
            "http://[::1]:49182",
        ):
            with self.subTest(origin=origin):
                self.assertTrue(is_allowed_cors_origin(origin))
                self.assertIn("Access-Control-Allow-Origin", cors_headers_for_origin(origin))

    def test_rejects_untrusted_origin(self) -> None:
        origin = "https://evil.example"
        self.assertFalse(is_allowed_cors_origin(origin))
        self.assertEqual(cors_headers_for_origin(origin), {})

    def test_rejects_origin_spoofing_localhost(self) -> None:
        self.assertFalse(is_allowed_cors_origin("http://evil.localhost"))
        self.assertFalse(is_allowed_cors_origin("http://localhost.evil.com"))

    def test_rejects_missing_or_wildcard_origin(self) -> None:
        self.assertFalse(is_allowed_cors_origin(""))
        self.assertEqual(cors_headers_for_origin(None), {})
        self.assertEqual(cors_headers_for_origin(""), {})

    def test_extra_origins_from_env(self) -> None:
        previous = os.environ.get("IELTS_CORS_ORIGINS")
        os.environ["IELTS_CORS_ORIGINS"] = "https://staging.example,https://preview.example"
        try:
            self.assertTrue(is_allowed_cors_origin("https://staging.example"))
            self.assertFalse(is_allowed_cors_origin("https://other.example"))
        finally:
            if previous is None:
                os.environ.pop("IELTS_CORS_ORIGINS", None)
            else:
                os.environ["IELTS_CORS_ORIGINS"] = previous


if __name__ == "__main__":
    unittest.main()
