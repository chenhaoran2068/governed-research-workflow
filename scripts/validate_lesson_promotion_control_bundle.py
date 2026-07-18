#!/usr/bin/env python3
"""Read-only structural validation for lesson-promotion control metadata."""

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
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "lesson_promotion_control_bundle.schema.json"
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"
EXPECTED_DECISION_BY_STATUS = {
    "local_only": "keep_local",
    "deferred": "defer",
    "rejected": "reject",
    "approved_for_integration": "approve_for_integration",
    "integrated": "approve_for_integration",
    "withdrawn": "withdraw",
    "superseded": "supersede",
}


class DuplicateJsonKeyError(ValueError):
    """Reject JSON parsing that would silently overwrite a prior key."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(key)
        result[key] = value
    return result


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
    try:
        return distribution_version("jsonschema")
    except PackageNotFoundError:
        return None


def _dependency_issue() -> ValidationIssue | None:
    if Draft202012Validator is None or FormatChecker is None:
        return ValidationIssue("not_assessed_dependency", f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is unavailable.")
    if _installed_jsonschema_version() != REQUIRED_JSONSCHEMA_VERSION:
        return ValidationIssue("not_assessed_dependency", f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is not installed.")
    return None


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _is_direct_indirection(path: Path) -> bool:
    return path.is_symlink() or _is_reparse_point(path)


def _contains_indirection(path: Path, *, stop_at: Path) -> bool:
    current = path
    while True:
        if _is_direct_indirection(current):
            return True
        if current == stop_at:
            return False
        if current.parent == current:
            return True
        current = current.parent


def _load_json(path: Path) -> tuple[dict[str, Any] | None, ValidationIssue | None]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except DuplicateJsonKeyError as error:
        return None, ValidationIssue("duplicate_json_key", f"Duplicate JSON key {str(error)!r} is not allowed.")
    except UnicodeDecodeError:
        return None, ValidationIssue("invalid_encoding", "JSON must be UTF-8.")
    except json.JSONDecodeError as error:
        return None, ValidationIssue("invalid_json", f"Invalid JSON: {error.msg}.")
    except OSError as error:
        return None, ValidationIssue("not_assessed_io", f"JSON could not be read safely: {error.strerror or error}.")
    if not isinstance(parsed, dict):
        return None, ValidationIssue("invalid_json_root", "JSON root must be an object.")
    return parsed, None


def _resolve_root(root_argument: Path) -> tuple[Path | None, ValidationIssue | None]:
    requested = root_argument.expanduser()
    if _is_direct_indirection(requested):
        return None, ValidationIssue("unsafe_root_path", "--root must not be a symbolic link or Windows reparse point.")
    try:
        root = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue("not_assessed_root", "--root could not be resolved safely.")
    if not root.is_dir():
        return None, ValidationIssue("invalid_root", "--root must resolve to a directory.")
    return root, None


def _safe_relative_json_path(raw_path: str, root: Path) -> tuple[Path | None, ValidationIssue | None]:
    if not raw_path or "\\" in raw_path:
        return None, ValidationIssue("unsafe_input_path", "--bundle must be a nonempty portable relative path using '/'.")
    posix_path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive or ".." in posix_path.parts:
        return None, ValidationIssue("unsafe_input_path", "--bundle must remain below --root without absolute or parent-traversal segments.")
    candidate = root.joinpath(*posix_path.parts)
    if _contains_indirection(candidate, stop_at=root):
        return None, ValidationIssue("unsafe_input_path", "--bundle must not use a symbolic link or Windows reparse point.")
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue("not_assessed_input", "--bundle could not be resolved safely.")
    try:
        resolved.relative_to(root)
    except ValueError:
        return None, ValidationIssue("unsafe_input_path", "--bundle resolves outside --root.")
    if not resolved.is_file() or _is_direct_indirection(resolved):
        return None, ValidationIssue("invalid_input", "--bundle must resolve to a regular file.")
    return resolved, None


def _schema_issues(instance: dict[str, Any], schema: dict[str, Any]) -> list[ValidationIssue]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return [dependency_issue]
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
    except SchemaError as error:
        return [ValidationIssue("not_assessed_schema", f"Bundled schema could not be used safely: {error.message}.")]
    return [
        ValidationIssue("schema_validation", error.message)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def _record_index(records: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[ValidationIssue]]:
    indexed: dict[str, dict[str, Any]] = {}
    issues: list[ValidationIssue] = []
    for record in records:
        record_id = record["record_id"]
        if record_id in indexed:
            issues.append(ValidationIssue("duplicate_record_id", "Record identifiers must be unique.", record_id))
        else:
            indexed[record_id] = record
    return indexed, issues


def _record_of_type(records: dict[str, dict[str, Any]], record_id: str | None, expected_type: str, owner: str, label: str) -> tuple[dict[str, Any] | None, list[ValidationIssue]]:
    if record_id is None:
        return None, [ValidationIssue("missing_record_reference", f"{label} is required for this lifecycle status.", owner)]
    record = records.get(record_id)
    if record is None:
        return None, [ValidationIssue("unknown_record_reference", f"{label} does not identify a record in the bundle.", owner)]
    if record["record_type"] != expected_type:
        return None, [ValidationIssue("wrong_record_type", f"{label} must identify a {expected_type} record.", owner)]
    return record, []


def _cross_record_issues(records: dict[str, dict[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for record_id, record in records.items():
        if record["record_type"] == "human_decision":
            candidate, candidate_issues = _record_of_type(records, record["candidate_id"], "lesson_candidate", record_id, "candidate_id")
            issues.extend(candidate_issues)
            if candidate is not None and candidate["human_decision_id"] != record_id:
                issues.append(ValidationIssue("unlinked_human_decision", "A human decision must be linked from its candidate.", record_id))
        elif record["record_type"] == "integration_verification":
            candidate, candidate_issues = _record_of_type(records, record["candidate_id"], "lesson_candidate", record_id, "candidate_id")
            decision, decision_issues = _record_of_type(records, record["human_decision_id"], "human_decision", record_id, "human_decision_id")
            issues.extend(candidate_issues + decision_issues)
            if candidate is not None and candidate["integration_verification_id"] != record_id:
                issues.append(ValidationIssue("unlinked_integration_verification", "An integration verification must be linked from its candidate.", record_id))
            if decision is not None and decision["candidate_id"] != record["candidate_id"]:
                issues.append(ValidationIssue("integration_decision_mismatch", "The integration decision must name the same candidate.", record_id))
        elif record["record_type"] == "change_event":
            candidate, candidate_issues = _record_of_type(records, record["candidate_id"], "lesson_candidate", record_id, "candidate_id")
            decision, decision_issues = _record_of_type(records, record["human_decision_id"], "human_decision", record_id, "human_decision_id")
            issues.extend(candidate_issues + decision_issues)
            if decision is not None and decision["candidate_id"] != record["candidate_id"]:
                issues.append(ValidationIssue("change_event_decision_mismatch", "The change-event decision must name the same candidate.", record_id))
            if record["change_type"] == "withdrawal" and decision is not None and decision["disposition"] != "withdraw":
                issues.append(ValidationIssue("withdrawal_disposition_mismatch", "A withdrawal event requires disposition withdraw.", record_id))
            if record["change_type"] == "supersession" and decision is not None and decision["disposition"] != "supersede":
                issues.append(ValidationIssue("supersession_disposition_mismatch", "A supersession event requires disposition supersede.", record_id))
            if record["change_type"] == "supersession" and candidate is not None and record["successor_candidate_id"] != candidate["superseded_by_candidate_id"]:
                issues.append(ValidationIssue("supersession_successor_mismatch", "A supersession event must name the candidate's declared successor.", record_id))
            if record["change_type"] != "supersession" and record["successor_candidate_id"] is not None:
                issues.append(ValidationIssue("unexpected_change_successor", "Only a supersession event may name a successor candidate.", record_id))
    for record_id, record in records.items():
        if record["record_type"] != "lesson_candidate":
            continue
        for observation_id in record["observation_ids"]:
            observation, reference_issues = _record_of_type(records, observation_id, "observation", record_id, "observation_ids")
            issues.extend(reference_issues)
            if observation is not None and observation["record_type"] != "observation":
                issues.append(ValidationIssue("wrong_record_type", "observation_ids must identify observation records.", record_id))

        status = record["lifecycle_status"]
        decision_id = record["human_decision_id"]
        if status == "under_review":
            if decision_id is not None:
                issues.append(ValidationIssue("under_review_has_decision", "under_review must not claim a recorded disposition.", record_id))
        else:
            decision, decision_issues = _record_of_type(records, decision_id, "human_decision", record_id, "human_decision_id")
            issues.extend(decision_issues)
            if decision is not None:
                if decision["candidate_id"] != record_id:
                    issues.append(ValidationIssue("decision_candidate_mismatch", "The human decision must name this candidate.", record_id))
                expected_disposition = EXPECTED_DECISION_BY_STATUS[status]
                if decision["disposition"] != expected_disposition:
                    issues.append(ValidationIssue("decision_disposition_mismatch", f"{status} requires disposition {expected_disposition}.", record_id))

        verification_id = record["integration_verification_id"]
        if status == "integrated":
            verification, verification_issues = _record_of_type(records, verification_id, "integration_verification", record_id, "integration_verification_id")
            issues.extend(verification_issues)
            if verification is not None:
                if verification["candidate_id"] != record_id or verification["human_decision_id"] != decision_id:
                    issues.append(ValidationIssue("integration_reference_mismatch", "Integration verification must name this candidate and its decision.", record_id))
                if verification["integration_status"] != "verified":
                    issues.append(ValidationIssue("integration_not_verified", "integrated requires integration_status verified.", record_id))
        elif verification_id is not None:
            issues.append(ValidationIssue("unexpected_integration_verification", "Only integrated candidates may declare an integration verification.", record_id))

        successor_id = record["superseded_by_candidate_id"]
        if status == "superseded":
            successor, successor_issues = _record_of_type(records, successor_id, "lesson_candidate", record_id, "superseded_by_candidate_id")
            issues.extend(successor_issues)
            if successor is not None and successor["record_id"] == record_id:
                issues.append(ValidationIssue("self_supersession", "A candidate cannot supersede itself.", record_id))
            matching_events = [
                event for event in records.values()
                if event["record_type"] == "change_event"
                and event["candidate_id"] == record_id
                and event["human_decision_id"] == decision_id
                and event["change_type"] == "supersession"
                and event["successor_candidate_id"] == successor_id
            ]
            if not matching_events:
                issues.append(ValidationIssue("missing_supersession_event", "superseded requires a matching supersession change event.", record_id))
        elif successor_id is not None:
            issues.append(ValidationIssue("unexpected_successor", "Only superseded candidates may declare a successor.", record_id))

        if status == "withdrawn":
            matching_events = [
                event for event in records.values()
                if event["record_type"] == "change_event"
                and event["candidate_id"] == record_id
                and event["human_decision_id"] == decision_id
                and event["change_type"] == "withdrawal"
            ]
            if not matching_events:
                issues.append(ValidationIssue("missing_withdrawal_event", "withdrawn requires a matching withdrawal change event.", record_id))
    issues.extend(_supersession_cycle_issues(records))
    return issues


def _supersession_cycle_issues(records: dict[str, dict[str, Any]]) -> list[ValidationIssue]:
    """Reject loops that would make a replacement chain non-reviewable."""
    graph = {
        record_id: record["superseded_by_candidate_id"]
        for record_id, record in records.items()
        if record["record_type"] == "lesson_candidate" and record["lifecycle_status"] == "superseded"
    }
    issues: list[ValidationIssue] = []
    visited: set[str] = set()
    for start in graph:
        current = start
        path: set[str] = set()
        while current in graph:
            if current in path:
                issues.append(ValidationIssue("supersession_cycle", "Supersession candidates must not form a cycle.", start))
                break
            if current in visited:
                break
            path.add(current)
            successor = graph[current]
            if successor is None:
                break
            current = successor
        visited.update(path)
    return issues


def _status(issues: list[ValidationIssue]) -> str:
    if any(issue.code.startswith("not_assessed") for issue in issues):
        return "not_assessed"
    return "invalid" if issues else "valid"


def _result(issues: list[ValidationIssue], checked_record_count: int) -> dict[str, Any]:
    return {
        "result": _status(issues),
        "checked_record_count": checked_record_count,
        "issues": [issue.as_dict() for issue in issues],
        "checks_performed": [
            "explicit_root_and_relative_input_path_safety",
            "duplicate_json_key_refusal",
            "schema_validation",
            "record_identifier_and_cross_record_lifecycle_checks"
        ],
        "explicit_non_claims": [
            "data_or_pointer_target_access",
            "external_service_action",
            "human_identity_or_actual_authorization",
            "automatic_promotion_or_target_mutation",
            "scientific_compliance_gate_submission_or_release_decision",
            "tamper_proof_storage_or_same_authority_rewrite_prevention"
        ]
    }


def validate_bundle(root_argument: Path, bundle_relative_path: str) -> dict[str, Any]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return _result([dependency_issue], 0)
    root, root_issue = _resolve_root(root_argument)
    if root_issue is not None:
        return _result([root_issue], 0)
    assert root is not None
    bundle_path, bundle_path_issue = _safe_relative_json_path(bundle_relative_path, root)
    if bundle_path_issue is not None:
        return _result([bundle_path_issue], 0)
    assert bundle_path is not None
    bundle, bundle_issue = _load_json(bundle_path)
    if bundle_issue is not None:
        return _result([bundle_issue], 0)
    schema, schema_issue = _load_json(SCHEMA_PATH)
    if schema_issue is not None:
        return _result([schema_issue], 0)
    assert bundle is not None and schema is not None
    issues = _schema_issues(bundle, schema)
    records: dict[str, dict[str, Any]] = {}
    if not issues:
        records, index_issues = _record_index(bundle["records"])
        issues.extend(index_issues)
        if not issues:
            issues.extend(_cross_record_issues(records))
    return _result(issues, len(records))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only validator for lesson-promotion control metadata.")
    parser.add_argument("--root", type=Path, required=True, help="Explicit root containing the selected bundle JSON.")
    parser.add_argument("--bundle", required=True, help="Portable relative path to one bundle JSON below --root.")
    args = parser.parse_args()
    result = validate_bundle(args.root, args.bundle)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"valid": 0, "invalid": 1, "not_assessed": 2}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
