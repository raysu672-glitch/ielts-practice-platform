import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from password_utils import (  # noqa: E402
    hash_password,
    is_password_hashed,
    verify_password,
)


class PasswordUtilsTests(unittest.TestCase):
    def test_hash_and_verify(self) -> None:
        stored = hash_password("secret-pass")
        self.assertTrue(is_password_hashed(stored))
        self.assertTrue(verify_password("secret-pass", stored))
        self.assertFalse(verify_password("wrong-pass", stored))

    def test_legacy_plaintext_verify(self) -> None:
        self.assertFalse(is_password_hashed("123456"))
        self.assertTrue(verify_password("123456", "123456"))
        self.assertFalse(verify_password("654321", "123456"))

    def test_hashes_are_unique(self) -> None:
        a = hash_password("same")
        b = hash_password("same")
        self.assertNotEqual(a, b)
        self.assertTrue(verify_password("same", a))
        self.assertTrue(verify_password("same", b))


if __name__ == "__main__":
    unittest.main()
