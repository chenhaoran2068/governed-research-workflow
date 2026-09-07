#!/usr/bin/env python3
"""Shared bounded helpers for paper repository candidate tooling."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_ROOT = ROOT / "system" / "09_schemas_records_and_templates"
DRIVE_PATH = re.compile(r"(?i)(?<![A-Za-z0-9])(?:[A-Z]:[\\/])")
PRIVATE_UNIX_PATH = re.compile(r"/(?:Users|home)/[^/<\s]+/")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
TOKEN_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
TEXT_SUFFIXES = {
    "", ".c", ".cff", ".cfg", ".conf", ".cpp", ".css", ".csv", ".gitignore",
    ".h", ".html", ".ini", ".ipynb", ".java", ".jl", ".js", ".json",
    ".lock", ".md", ".m", ".ps1", ".py", ".r", ".rmd", ".rs", ".sh",
    ".sql", ".tex", ".toml", ".ts", ".txt", ".xml", ".yaml", ".yml",
}
DISALLOWED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
DISALLOWED_SEQUENCES = {("renv", "library"), ("renv", "staging")}


class DuplicateJsonKeyError(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def safe_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.replace("\\", "/").split("#", 1)[0]
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return False
    return all(part not in {"", ".", ".."} for part in normalized.split("/"))


def is_reparse_or_symlink(path: Path) -> bool:
    if path.is_symlink():
        return True
    stat = path.lstat()
    attributes = getattr(stat, "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & flag)


def has_linked_parent(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if is_reparse_or_symlink(current):
            return True
    return False


def is_disallowed_relative(path: Path) -> bool:
    parts = tuple(part.casefold() for part in path.parts)
    if any(part in DISALLOWED_PARTS for part in parts):
        return True
    return any(parts[index:index + len(sequence)] == sequence for sequence in DISALLOWED_SEQUENCES for index in range(len(parts)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan_text(path: Path) -> list[tuple[str, str]]:
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Dockerfile", "Makefile"}:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    findings: list[tuple[str, str]] = []
    if PRIVATE_KEY.search(text):
        findings.append(("private_key", "private-key material detected"))
    for pattern in TOKEN_PATTERNS:
        if pattern.search(text):
            findings.append(("secret_pattern", "credential-like token detected"))
            break
    if DRIVE_PATH.search(text) or PRIVATE_UNIX_PATH.search(text):
        findings.append(("private_path", "machine-specific absolute path detected"))
    if re.search(r"<(?:study-id|candidate-id|paper-or-output-id|release-profile|RFC3339 timestamp)>", text):
        findings.append(("unresolved_placeholder", "required template placeholder remains"))
    return findings
