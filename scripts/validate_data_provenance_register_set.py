#!/usr/bin/env python3
"""Validate a metadata-only Data And Provenance Register Set.

The validator reads only an explicitly supplied index JSON, package-bundled
schemas, and the regular JSON entry files named by that index. It does not
inspect a source locator, data payload, URL, credential, or unlisted file.
"""

from __future__ import annotations

import argparse
import json
import stat
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:  # pragma: no cover - exercised by the CLI environment.
    Draft202012Validator = None
    FormatChecker = None
    SchemaError = Exception


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "data_provenance_register_set_index.schema.json"
)
ENTRY_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "data_provenance_register.schema.json"
)
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    record_id: str | None = None

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.record_id is not None:
            result["record_id"] = self.record_id
        return result


def _installed_jsonschema_version() -> str | None:
    """Return the installed jsonschema distribution version, if available."""
    try:
        return distribution_version("jsonschema")
    except PackageNotFoundError:
        return None


def _dependency_issue() -> ValidationIssue | None:
    """Keep the validator's runtime contract aligned with requirements.txt."""
    if Draft202012Validator is None or FormatChecker is None:
        return ValidationIssue(
            "not_assessed_dependency",
            f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is unavailable.",
        )
    installed_version = _installed_jsonschema_version()
    if installed_version != REQUIRED_JSONSCHEMA_VERSION:
        return ValidationIssue(
            "not_assessed_dependency",
            f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is not installed.",
        )
    return None


def _is_reparse_point(path: Path) -> bool:
    """Return true for Windows reparse points without following them."""
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _contains_indirection(path: Path, *, stop_at: Path | None = None) -> bool:
    """Refuse symlinks or reparse points from path through an optional root."""
    current = path
    while True:
        if current.is_symlink() or _is_reparse_point(current):
            return True
        if stop_at is not None and current == stop_at:
            return False
        if current.parent == current:
            return False
        current = current.parent


def _is_direct_indirection(path: Path) -> bool:
    """Refuse only a supplied path that is itself a link or reparse point."""
    return path.is_symlink() or _is_reparse_point(path)


def _load_json(path: Path) -> tuple[dict[str, Any] | None, ValidationIssue | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return None, ValidationIssue("invalid_encoding", "Metadata JSON must be UTF-8.")
    except json.JSONDecodeError as error:
        return None, ValidationIssue("invalid_json", f"Invalid JSON: {error.msg}.")
    except OSError as error:
        return None, ValidationIssue("not_assessed_io", f"Metadata file could not be read safely: {error.strerror or error}.")
    if not isinstance(data, dict):
        return None, ValidationIssue("invalid_json_root", "Metadata JSON root must be an object.")
    return data, None


def _schema_issues(instance: dict[str, Any], schema: dict[str, Any], subject: str) -> list[ValidationIssue]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return [dependency_issue]
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
    except SchemaError as error:
        return [ValidationIssue("not_assessed_schema", f"Bundled schema could not be used safely: {error.message}.")]
    return [
        ValidationIssue("schema_validation", f"{subject}: {error.message}")
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def _safe_relative_entry_path(raw_path: str, root: Path) -> tuple[Path | None, ValidationIssue | None]:
    if not raw_path or "\\" in raw_path:
        return None, ValidationIssue("unsafe_entry_path", "entry_path must be a nonempty portable relative path using '/'.")
    posix_path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive or ".." in posix_path.parts:
        return None, ValidationIssue("unsafe_entry_path", "entry_path must not be absolute, drive-qualified, or contain '..'.")
    candidate = root.joinpath(*posix_path.parts)
    if _contains_indirection(candidate, stop_at=root):
        return None, ValidationIssue("unsafe_entry_path", "entry_path must not traverse a symbolic link or Windows reparse point.")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        return None, ValidationIssue("missing_or_outside_entry", "entry_path must resolve to an existing regular file under the index root.")
    if resolved.suffix.lower() != ".json" or not resolved.is_file():
        return None, ValidationIssue("invalid_entry_file", "entry_path must resolve to a regular JSON file.")
    return resolved, None


def _relation_issues(records: dict[str, dict[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_edges: set[tuple[str, str, str]] = set()
    for record_id, record in records.items():
        lineage = record["lineage"]
        for direction, reverse in (("upstream_record_ids", "downstream_record_ids"), ("downstream_record_ids", "upstream_record_ids")):
            for related_id in lineage[direction]:
                edge = (record_id, direction, related_id)
                if edge in seen_edges:
                    issues.append(ValidationIssue("duplicate_relation", f"Duplicate {direction} declaration.", record_id))
                    continue
                seen_edges.add(edge)
                if related_id == record_id:
                    issues.append(ValidationIssue("self_relation", "A record must not declare a relationship to itself.", record_id))
                elif related_id not in records:
                    issues.append(ValidationIssue("missing_relation_target", f"Declared related record {related_id!r} is not listed in this register.", record_id))
                elif record_id not in records[related_id]["lineage"][reverse]:
                    issues.append(ValidationIssue("asymmetric_relation", f"Declared relation with {related_id!r} is not reciprocal.", record_id))
    return issues


def _result_from_issues(issues: list[ValidationIssue], checked_entry_count: int) -> dict[str, Any]:
    status = "valid"
    if issues:
        status = "not_assessed" if any(issue.code.startswith("not_assessed") for issue in issues) else "invalid"
    return {
        "result": status,
        "checked_entry_count": checked_entry_count,
        "issues": [issue.as_dict() for issue in issues],
    }


def validate_register_set(index_path: Path) -> dict[str, Any]:
    """Return a JSON-serializable limited structural validation result."""
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return _result_from_issues([dependency_issue], 0)

    requested_index = index_path.expanduser()
    # An explicit index may live under a system-managed alias such as macOS
    # /var. Resolve it to a canonical root, but never follow an index file that
    # is itself a symbolic link or Windows reparse point.
    if _is_direct_indirection(requested_index):
        return _result_from_issues(
            [ValidationIssue("unsafe_index_path", "The index path must not use a symbolic link or Windows reparse point.")],
            0,
        )
    try:
        index_path = requested_index.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return _result_from_issues(
            [ValidationIssue("not_assessed_index", "The explicit index file could not be resolved safely.")],
            0,
        )
    if index_path.suffix.lower() != ".json" or not index_path.is_file():
        return _result_from_issues(
            [ValidationIssue("invalid_index_file", "The explicit index path must be a regular JSON file.")],
            0,
        )

    index, index_load_issue = _load_json(index_path)
    if index_load_issue is not None:
        return _result_from_issues([index_load_issue], 0)

    index_schema, schema_issue = _load_json(INDEX_SCHEMA_PATH)
    entry_schema, entry_schema_issue = _load_json(ENTRY_SCHEMA_PATH)
    internal_issues = [issue for issue in (schema_issue, entry_schema_issue) if issue is not None]
    if internal_issues:
        return _result_from_issues(internal_issues, 0)

    issues = _schema_issues(index, index_schema, "index")
    if issues:
        return _result_from_issues(issues, 0)

    root = index_path.parent
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    records: dict[str, dict[str, Any]] = {}
    for entry in index["entries"]:
        record_id = entry["record_id"]
        entry_path = entry["entry_path"]
        if record_id in seen_ids:
            issues.append(ValidationIssue("duplicate_record_id", "record_id is listed more than once.", record_id))
            continue
        seen_ids.add(record_id)
        if entry_path in seen_paths:
            issues.append(ValidationIssue("duplicate_entry_path", "entry_path is listed more than once.", record_id))
            continue
        seen_paths.add(entry_path)
        resolved_entry, path_issue = _safe_relative_entry_path(entry_path, root)
        if path_issue is not None:
            issues.append(ValidationIssue(path_issue.code, path_issue.message, record_id))
            continue
        record, record_load_issue = _load_json(resolved_entry)
        if record_load_issue is not None:
            issues.append(ValidationIssue(record_load_issue.code, record_load_issue.message, record_id))
            continue
        record_issues = _schema_issues(record, entry_schema, f"entry {record_id}")
        issues.extend(ValidationIssue(issue.code, issue.message, record_id) for issue in record_issues)
        if record.get("record_id") != record_id:
            issues.append(ValidationIssue("record_id_mismatch", "Index record_id does not match the entry record_id.", record_id))
        elif not record_issues:
            records[record_id] = record

    if not issues:
        issues.extend(_relation_issues(records))
    return _result_from_issues(issues, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only validator for a metadata-only Data And Provenance Register Set.")
    parser.add_argument("index_path", type=Path, help="Explicit path to the register-index JSON file.")
    args = parser.parse_args()
    result = validate_register_set(args.index_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"valid": 0, "invalid": 1, "not_assessed": 2}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
