"""Aliyun OSS V1 signed GET URLs. Stdlib only; secrets stay in env / config/oss.env."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any
from xml.etree import ElementTree as ET

DEFAULT_BUCKET = "oyenglish-luboke"
DEFAULT_ENDPOINT = "oss-cn-shanghai.aliyuncs.com"
DEFAULT_EXPIRES_SECONDS = 7200


def oss_settings() -> dict[str, Any]:
    expires_raw = (os.environ.get("OSS_SIGN_EXPIRES") or "").strip()
    try:
        expires_seconds = int(expires_raw) if expires_raw else DEFAULT_EXPIRES_SECONDS
    except ValueError:
        expires_seconds = DEFAULT_EXPIRES_SECONDS
    if expires_seconds < 60:
        expires_seconds = 60
    if expires_seconds > 86400:
        expires_seconds = 86400
    return {
        "access_key_id": (os.environ.get("OSS_ACCESS_KEY_ID") or "").strip(),
        "access_key_secret": (os.environ.get("OSS_ACCESS_KEY_SECRET") or "").strip(),
        "bucket": (os.environ.get("OSS_BUCKET") or DEFAULT_BUCKET).strip() or DEFAULT_BUCKET,
        "endpoint": (os.environ.get("OSS_ENDPOINT") or DEFAULT_ENDPOINT).strip() or DEFAULT_ENDPOINT,
        "expires_seconds": expires_seconds,
    }


def oss_configured(settings: dict[str, Any] | None = None) -> bool:
    cfg = settings if settings is not None else oss_settings()
    return bool(cfg["access_key_id"] and cfg["access_key_secret"] and cfg["bucket"])


def is_safe_oss_key(oss_key: str) -> bool:
    key = str(oss_key or "").strip().lstrip("/")
    if not key or "\\" in key or ".." in key.split("/"):
        return False
    if key.startswith("/") or ":" in key:
        return False
    return True


def sign_get_url(
    oss_key: str,
    *,
    expires_at: int | None = None,
    settings: dict[str, Any] | None = None,
) -> str:
    cfg = settings if settings is not None else oss_settings()
    if not oss_configured(cfg):
        raise RuntimeError("OSS 未配置")
    key = str(oss_key or "").strip().lstrip("/")
    if not is_safe_oss_key(key):
        raise ValueError("无效的文件路径")
    expires = int(expires_at if expires_at is not None else time.time() + int(cfg["expires_seconds"]))
    resource = f"/{cfg['bucket']}/{key}"
    string_to_sign = f"GET\n\n\n{expires}\n{resource}"
    digest = hmac.new(
        cfg["access_key_secret"].encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    signature = urllib.parse.quote(base64.b64encode(digest).decode("ascii"), safe="")
    encoded_key = urllib.parse.quote(key, safe="/")
    access_key_id = urllib.parse.quote(cfg["access_key_id"], safe="")
    endpoint = str(cfg["endpoint"]).strip().lstrip("https://").lstrip("http://")
    return (
        f"https://{cfg['bucket']}.{endpoint}/{encoded_key}"
        f"?OSSAccessKeyId={access_key_id}&Expires={expires}&Signature={signature}"
    )


def list_object_keys(
    prefix: str = "courses/",
    *,
    settings: dict[str, Any] | None = None,
) -> list[str]:
    cfg = settings if settings is not None else oss_settings()
    if not oss_configured(cfg):
        raise RuntimeError("OSS 未配置")
    endpoint = str(cfg["endpoint"]).strip().lstrip("https://").lstrip("http://")
    keys: list[str] = []
    marker = ""
    # OSS 单次最多返回 1000 个，这里用 marker 分页把 courses/ 下所有视频都拉回来。
    for _ in range(20):
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        resource = f"/{cfg['bucket']}/"
        string_to_sign = f"GET\n\n\n{date}\n{resource}"
        digest = hmac.new(
            cfg["access_key_secret"].encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
        signature = base64.b64encode(digest).decode("ascii")
        params = {"prefix": prefix, "max-keys": "1000"}
        if marker:
            params["marker"] = marker
        query = urllib.parse.urlencode(params)
        url = f"https://{cfg['bucket']}.{endpoint}/?{query}"
        req = urllib.request.Request(url)
        req.add_header("Date", date)
        req.add_header("Authorization", f"OSS {cfg['access_key_id']}:{signature}")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                xml = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"无法列出 OSS 文件（{exc.code}）") from exc
        root = ET.fromstring(xml)
        batch: list[str] = []
        truncated = False
        next_marker = ""
        for el in root.iter():
            tag = el.tag
            if tag.endswith("IsTruncated") and el.text:
                truncated = el.text.strip().lower() == "true"
            elif tag.endswith("NextMarker") and el.text:
                next_marker = el.text.strip()
            elif tag.endswith("Key") and el.text:
                key = el.text.strip()
                if key.endswith("/") or key == prefix.rstrip("/"):
                    continue
                if is_safe_oss_key(key):
                    batch.append(key)
        keys.extend(batch)
        if not truncated or not batch:
            break
        marker = next_marker or batch[-1]
    return keys
