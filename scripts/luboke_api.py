"""Recorded-course catalog: subjects + lesson details. Video files stay on OSS."""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

from oss_sign import is_safe_oss_key

ROOT = Path(__file__).resolve().parents[1]
SEED_CATALOG_PATH = ROOT / "sources" / "luboke" / "courses.json"
RUNTIME_CATALOG_PATH = ROOT / "data" / "luboke_courses.json"

# Seed subjects for brand-new catalogs only. Teachers may add/rename/remove freely.
DEFAULT_SUBJECTS = [
    {"id": "listening", "name": "听力"},
    {"id": "reading", "name": "阅读"},
    {"id": "writing", "name": "写作"},
    {"id": "speaking", "name": "口语"},
]


def catalog_path() -> Path:
    if RUNTIME_CATALOG_PATH.is_file():
        return RUNTIME_CATALOG_PATH
    return SEED_CATALOG_PATH


def normalize_oss_key(raw: str) -> str:
    key = str(raw or "").strip().replace("\\", "/").lstrip("/")
    if not key:
        return ""
    if "/" not in key:
        key = "courses/" + key
    return key


def _slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", str(text or "").strip()).strip("-").lower()
    return value[:40]


def _subject_id(name: str, existing: set[str], preferred: str = "") -> str:
    candidate = str(preferred or "").strip()
    if not candidate or not re.fullmatch(r"[a-zA-Z0-9_-]{1,48}", candidate):
        base = _slug(name)
        if not base:
            digest = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
            base = f"s{digest}"
        candidate = base
    if candidate not in existing:
        return candidate
    return f"{candidate}-{int(time.time())}"


def _course_id(subject_id: str, title: str, existing: set[str]) -> str:
    base = _slug(title) or "lesson"
    candidate = f"{subject_id}-{base}"
    if candidate not in existing:
        return candidate
    return f"{candidate}-{int(time.time())}"


def _empty_subjects() -> list[dict[str, Any]]:
    return [{"id": item["id"], "name": item["name"], "courses": []} for item in DEFAULT_SUBJECTS]


def _normalize_course(item: dict[str, Any], *, subject_id: str, seen: set[str]) -> dict[str, Any] | None:
    title = str(item.get("title") or "").strip()
    oss_key = normalize_oss_key(str(item.get("oss_key") or ""))
    if not title or not is_safe_oss_key(oss_key):
        return None
    course_id = str(item.get("id") or "").strip() or _course_id(subject_id, title, seen)
    if course_id in seen:
        course_id = _course_id(subject_id, title, seen)
    seen.add(course_id)
    return {
        "id": course_id,
        "title": title,
        "duration": str(item.get("duration") or "").strip(),
        "summary": str(item.get("summary") or item.get("detail") or "").strip(),
        "oss_key": oss_key,
    }


def parse_catalog(raw: Any, *, seed_defaults: bool = False) -> dict[str, Any]:
    """Parse catalog JSON.

    When ``subjects`` is present, trust that list (teachers own the subject list).
    Empty / legacy flat catalogs may seed the four default subjects.
    """
    if not isinstance(raw, dict):
        return {"subjects": _empty_subjects() if seed_defaults else []}

    seen_courses: set[str] = set()
    grouped = raw.get("subjects")
    if isinstance(grouped, list):
        subjects: list[dict[str, Any]] = []
        seen_subjects: set[str] = set()
        for item in grouped:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()
            preferred_id = str(item.get("id") or "").strip()
            if not name and not preferred_id:
                continue
            if not name:
                name = preferred_id
            subject_id = _subject_id(name, seen_subjects, preferred_id)
            seen_subjects.add(subject_id)
            bucket: dict[str, Any] = {"id": subject_id, "name": name, "courses": []}
            for course in item.get("courses") or []:
                if not isinstance(course, dict):
                    continue
                normalized = _normalize_course(course, subject_id=subject_id, seen=seen_courses)
                if normalized:
                    bucket["courses"].append(normalized)
            subjects.append(bucket)
        if subjects:
            return {"subjects": subjects}
        return {"subjects": _empty_subjects() if seed_defaults else []}

    # Legacy flat ``courses`` list → put under 阅读
    subjects = _empty_subjects()
    by_id = {item["id"]: item for item in subjects}
    for item in raw.get("courses") or []:
        if not isinstance(item, dict):
            continue
        subject_id = str(item.get("subject_id") or "reading").strip() or "reading"
        if subject_id not in by_id:
            subject_id = "reading"
        normalized = _normalize_course(item, subject_id=subject_id, seen=seen_courses)
        if normalized:
            by_id[subject_id]["courses"].append(normalized)
    return {"subjects": subjects}


def load_catalog(path: Path | str | None = None) -> dict[str, Any]:
    catalog_file = Path(path) if path is not None else catalog_path()
    if not catalog_file.is_file():
        return parse_catalog({}, seed_defaults=True)
    return parse_catalog(json.loads(catalog_file.read_text(encoding="utf-8")), seed_defaults=True)


def flatten_courses(catalog: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    data = catalog if catalog is not None else load_catalog()
    courses: list[dict[str, Any]] = []
    for subject in data.get("subjects") or []:
        for course in subject.get("courses") or []:
            item = dict(course)
            item["subject_id"] = subject["id"]
            item["subject_name"] = subject.get("name") or subject["id"]
            courses.append(item)
    return courses


def load_courses(catalog_path: Path | str | None = None) -> list[dict[str, Any]]:
    return flatten_courses(load_catalog(catalog_path))


def public_course(course: dict[str, Any]) -> dict[str, Any]:
    public = {
        "id": course["id"],
        "title": course["title"],
        "duration": course.get("duration") or "",
        "summary": course.get("summary") or "",
    }
    if course.get("subject_id"):
        public["subject_id"] = course["subject_id"]
        public["subject_name"] = course.get("subject_name") or ""
    return public


def public_catalog(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    data = catalog if catalog is not None else load_catalog()
    subjects = []
    for subject in data.get("subjects") or []:
        subjects.append(
            {
                "id": subject["id"],
                "name": subject.get("name") or subject["id"],
                "courses": [public_course(course) for course in subject.get("courses") or []],
            }
        )
    return {"subjects": subjects}


def get_course(courses: list[dict[str, Any]], course_id: str) -> dict[str, Any] | None:
    wanted = str(course_id or "").strip()
    if not wanted:
        return None
    for course in courses:
        if course["id"] == wanted:
            return course
    return None


def save_catalog(payload: dict[str, Any], path: Path | str | None = None) -> dict[str, Any]:
    catalog = parse_catalog(payload, seed_defaults=False)
    if not catalog["subjects"]:
        raise ValueError("请至少保留一个科目")
    target = Path(path) if path is not None else RUNTIME_CATALOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(target)
    return catalog
