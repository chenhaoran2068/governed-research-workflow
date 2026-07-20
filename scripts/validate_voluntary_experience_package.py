#!/usr/bin/env python3
"""Read-only structural validator for a voluntary metadata-only experience package.

It reads one explicit manifest, package-bundled schema, and exactly five files
named by that manifest. It never discovers a directory, reads attachments,
contacts a service, or changes a file.
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
except ImportError:  # pragma: no cover
    Draft202012Validator = None
    FormatChecker = None
    SchemaError = Exception


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "voluntary_experience_package.schema.json"
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"
RECORD_KEYS = (
    "observation_record",
    "contribution_scope_record",
    "redaction_and_rights_record",
    "maintainer_review_record",
    "correction_or_withdrawal_record",
)
RECORD_DEFS = {
    "observation_record": "observation_record",
    "contribution_scope_record": "contribution_scope_record",
    "redaction_and_rights_record": "redaction_and_rights_record",
    "maintainer_review_record": "maintainer_review_record",
    "correction_or_withdrawal_record": "correction_or_withdrawal_record",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    record_key: str | None = None

    def as_dict(self) -> dict[str, str]:
        item = {"code": self.code, "message": self.message}
        if self.record_key is not None:
            item["record_key"] = self.record_key
        return item


def _installed_jsonschema_version() -> str | None:
    try:
        return distribution_version("jsonschema")
    except PackageNotFoundError:
        return None


def _dependency_issue() -> ValidationIssue | None:
    if Draft202012Validator is None or FormatChecker is None:
        return ValidationIssue("not_assessed_dependency", "jsonschema is unavailable.")
    if _installed_jsonschema_version() != REQUIRED_JSONSCHEMA_VERSION:
        return ValidationIssue("not_assessed_dependency", f"jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is required.")
    return None


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _contains_indirection(path: Path, *, stop_at: Path | None = None) -> bool:
    current = path
    while True:
        if current.is_symlink() or _is_reparse_point(current):
            return True
        if stop_at is not None and current == stop_at:
            return False
        if current.parent == current:
            return False
        current = current.parent


def _load_json(path: Path) -> tuple[dict[str, Any] | None, ValidationIssue | None]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key {key!r}.")
            result[key] = value
        return result

    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except UnicodeDecodeError:
        return None, ValidationIssue("invalid_encoding", "Metadata JSON must be UTF-8.")
    except ValueError as error:
        return None, ValidationIssue("invalid_json", str(error))
    except json.JSONDecodeError as error:
        return None, ValidationIssue("invalid_json", error.msg)
    except OSError as error:
        return None, ValidationIssue("not_assessed_io", str(error))
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
        return [ValidationIssue("not_assessed_schema", error.message)]
    return [ValidationIssue("schema_validation", f"{subject}: {error.message}") for error in sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))]


def _safe_named_record(raw_path: str, root: Path) -> tuple[Path | None, ValidationIssue | None]:
    if not raw_path or "\\" in raw_path:
        return None, ValidationIssue("refused_boundary", "Record path must be a nonempty portable relative path using '/'.")
    posix = PurePosixPath(raw_path)
    windows = PureWindowsPath(raw_path)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        return None, ValidationIssue("refused_boundary", "Record path must not be absolute, drive-qualified, or contain '..'.")
    candidate = root.joinpath(*posix.parts)
    if _contains_indirection(candidate, stop_at=root):
        return None, ValidationIssue("refused_boundary", "Record path must not traverse a symbolic link or reparse point.")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        return None, ValidationIssue("structurally_invalid", "Named record must resolve to an existing regular file under the manifest root.")
    if not resolved.is_file() or resolved.suffix.lower() != ".json":
        return None, ValidationIssue("structurally_invalid", "Named record must be a regular JSON file.")
    return resolved, None


def _semantic_issues(records: dict[str, dict[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    identifiers = [record["record_id"] for record in records.values() if "record_id" in record]
    if len(identifiers) != len(set(identifiers)):
        issues.append(ValidationIssue("duplicate_record_id", "Every named record must have a distinct record_id."))
    review = records.get("maintainer_review_record", {})
    review_state = review.get("review_state")
    review_reference = review.get("accountable_human_reference")
    decision_basis = review.get("decision_basis_references", [])
    if review_state == "not_reviewed" and (review_reference is not None or decision_basis):
        issues.append(ValidationIssue("invalid_review_state", "not_reviewed must not carry a human reference or decision basis.", "maintainer_review_record"))
    if review_state and review_state != "not_reviewed" and (not review_reference or not decision_basis):
        issues.append(ValidationIssue("invalid_review_state", "A reviewed state requires a human reference and at least one decision basis.", "maintainer_review_record"))
    change = records.get("correction_or_withdrawal_record", {})
    request_state = change.get("request_state")
    requested_action = change.get("requested_action")
    decision_reference = change.get("accountable_human_decision_reference")
    future_use = change.get("future_use_state")
    if request_state == "no_request" and (requested_action != "none" or decision_reference is not None or future_use != "not_requested"):
        issues.append(ValidationIssue("invalid_withdrawal_state", "no_request must use action none, no decision reference, and not_requested future use.", "correction_or_withdrawal_record"))
    if request_state in {"correction_requested", "withdrawal_requested"} and (decision_reference is not None or future_use != "pending_human_decision"):
        issues.append(ValidationIssue("invalid_withdrawal_state", "A pending request cannot represent a human decision or stopped future use.", "correction_or_withdrawal_record"))
    if request_state == "future_use_stopped" and (requested_action != "withdrawal" or not decision_reference or future_use != "stopped_after_human_decision"):
        issues.append(ValidationIssue("invalid_withdrawal_state", "future_use_stopped requires a withdrawal, human decision reference, and stopped_after_human_decision.", "correction_or_withdrawal_record"))
    allowed = {record.get("record_id") for key, record in records.items() if key != "correction_or_withdrawal_record"}
    for record_id in change.get("affected_record_ids", []):
        if record_id not in allowed:
            issues.append(ValidationIssue("invalid_affected_record", "Affected record must reference one of the other declared records.", "correction_or_withdrawal_record"))
    return issues


def _result(status: str, issues: list[ValidationIssue], checked_record_count: int) -> dict[str, Any]:
    return {"result": status, "checked_record_count": checked_record_count, "issues": [issue.as_dict() for issue in issues]}


def validate_experience_package(manifest_path: Path) -> dict[str, Any]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return _result("not_assessed", [dependency_issue], 0)
    requested = manifest_path.expanduser()
    lexical_requested = requested if requested.is_absolute() else Path.cwd() / requested
    # Check the manifest and its declared package root before resolving.  Do not
    # walk through operating-system path aliases such as macOS /var -> /private/var.
    if _contains_indirection(lexical_requested, stop_at=lexical_requested.parent):
        return _result(
            "refused_boundary",
            [
                ValidationIssue(
                    "refused_boundary",
                    "The explicit manifest or its direct package-root directory must not be a symbolic link or reparse point.",
                )
            ],
            0,
        )
    try:
        manifest_path = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return _result("refused_boundary", [ValidationIssue("refused_boundary", "The explicit manifest path could not be resolved safely.")], 0)
    if not manifest_path.is_file() or manifest_path.suffix.lower() != ".json":
        return _result("refused_boundary", [ValidationIssue("refused_boundary", "The explicit manifest must be a regular JSON file.")], 0)
    manifest, load_issue = _load_json(manifest_path)
    schema, schema_issue = _load_json(SCHEMA_PATH)
    if load_issue or schema_issue:
        return _result("not_assessed", [issue for issue in (load_issue, schema_issue) if issue is not None], 0)
    # Classify explicitly supplied escaping/link paths as a boundary refusal
    # before schema validation can reduce them to a generic pattern error.
    preflight_records = manifest.get("records")
    if isinstance(preflight_records, dict):
        for key in RECORD_KEYS:
            raw_path = preflight_records.get(key)
            if isinstance(raw_path, str):
                _, path_issue = _safe_named_record(raw_path, manifest_path.parent)
                if path_issue is not None and path_issue.code == "refused_boundary":
                    return _result("refused_boundary", [ValidationIssue(path_issue.code, path_issue.message, key)], 0)
    issues = _schema_issues(manifest, schema, "manifest")
    if issues:
        return _result("structurally_invalid", issues, 0)
    root = manifest_path.parent
    if _contains_indirection(root):
        return _result("refused_boundary", [ValidationIssue("refused_boundary", "Manifest root must not traverse a symbolic link or reparse point.")], 0)
    records: dict[str, dict[str, Any]] = {}
    named_paths = list(manifest["records"].values())
    if len(named_paths) != len(set(named_paths)):
        return _result("structurally_invalid", [ValidationIssue("duplicate_record_path", "Each named record must use a distinct path.")], 0)
    for key in RECORD_KEYS:
        path, path_issue = _safe_named_record(manifest["records"][key], root)
        if path_issue is not None:
            return _result("refused_boundary" if path_issue.code == "refused_boundary" else "structurally_invalid", [ValidationIssue(path_issue.code, path_issue.message, key)], len(records))
        record, record_issue = _load_json(path)
        if record_issue is not None:
            return _result("structurally_invalid", [ValidationIssue(record_issue.code, record_issue.message, key)], len(records))
        record_schema = {"$ref": f"#/$defs/{RECORD_DEFS[key]}", "$defs": schema["$defs"]}
        record_issues = _schema_issues(record, record_schema, key)
        if record_issues:
            return _result("structurally_invalid", [ValidationIssue(issue.code, issue.message, key) for issue in record_issues], len(records))
        records[key] = record
    issues = _semantic_issues(records)
    return _result("structurally_invalid" if issues else "structurally_valid", issues, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only validator for a voluntary metadata-only experience package.")
    parser.add_argument("manifest_path", type=Path, help="Explicit path to experience-package.json.")
    result = validate_experience_package(parser.parse_args().manifest_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"structurally_valid": 0, "structurally_invalid": 1, "not_assessed": 2, "refused_boundary": 3}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
