#!/usr/bin/env python3
"""Validate one caller-supplied metadata-only integrity audit bundle.

The validator reads only the explicit bundle JSON and the bundled schema. It
does not enumerate a directory, follow declared references, contact a service,
run Git, create report files, or change the supplied bundle.
"""

from __future__ import annotations

import argparse
import json
import stat
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:  # pragma: no cover
    Draft202012Validator = None
    FormatChecker = None
    SchemaError = Exception


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "integrity_audit_bundle.schema.json"
)
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"


class DuplicateJsonKeyError(ValueError):
    """Raised when JSON parsing would silently overwrite an object key."""


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


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(key)
        result[key] = value
    return result


def _installed_jsonschema_version() -> str | None:
    try:
        return distribution_version("jsonschema")
    except PackageNotFoundError:
        return None


def _dependency_issue() -> ValidationIssue | None:
    if Draft202012Validator is None or FormatChecker is None:
        return ValidationIssue(
            "not_assessed_dependency",
            f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is unavailable.",
        )
    if _installed_jsonschema_version() != REQUIRED_JSONSCHEMA_VERSION:
        return ValidationIssue(
            "not_assessed_dependency",
            f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is not installed.",
        )
    return None


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _contains_indirection(path: Path) -> bool:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current = current / component
        if current.is_symlink() or _is_reparse_point(current):
            return True
    return False


def _safe_bundle_path(raw_path: Path) -> tuple[Path | None, ValidationIssue | None]:
    requested = raw_path.expanduser()
    if not requested.is_absolute() or ".." in requested.parts:
        return None, ValidationIssue(
            "unsafe_bundle_path",
            "--bundle must be an absolute physical path without parent traversal.",
        )
    if _contains_indirection(requested):
        return None, ValidationIssue(
            "unsafe_bundle_path",
            "--bundle must not traverse a symbolic link or Windows reparse point.",
        )
    try:
        resolved = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue(
            "not_assessed_bundle_path",
            "--bundle could not be resolved safely.",
        )
    if resolved.suffix.lower() != ".json" or not resolved.is_file():
        return None, ValidationIssue(
            "invalid_bundle_path",
            "--bundle must resolve to one regular JSON file.",
        )
    return resolved, None


def _load_json(path: Path) -> tuple[dict[str, Any] | None, ValidationIssue | None]:
    try:
        parsed = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except DuplicateJsonKeyError as error:
        return None, ValidationIssue(
            "duplicate_json_key",
            f"Duplicate JSON key {str(error)!r} is not allowed.",
        )
    except UnicodeDecodeError:
        return None, ValidationIssue("invalid_encoding", "JSON must be UTF-8.")
    except json.JSONDecodeError as error:
        return None, ValidationIssue("invalid_json", f"Invalid JSON: {error.msg}.")
    except OSError as error:
        return None, ValidationIssue(
            "not_assessed_io",
            f"JSON could not be read safely: {error.strerror or error}.",
        )
    if not isinstance(parsed, dict):
        return None, ValidationIssue("invalid_json_root", "JSON root must be an object.")
    return parsed, None


def _schema_issues(
    instance: dict[str, Any], schema: dict[str, Any]
) -> list[ValidationIssue]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return [dependency_issue]
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
    except SchemaError as error:
        return [
            ValidationIssue(
                "not_assessed_schema",
                f"Bundled schema could not be used safely: {error.message}.",
            )
        ]
    return [
        ValidationIssue(
            "schema_validation",
            f"{'.'.join(str(item) for item in error.absolute_path) or '<root>'}: {error.message}",
        )
        for error in sorted(
            validator.iter_errors(instance), key=lambda error: list(error.absolute_path)
        )
    ]


def _unique_ids(
    records: list[dict[str, Any]], id_field: str, label: str
) -> tuple[set[str], list[ValidationIssue]]:
    values: set[str] = set()
    issues: list[ValidationIssue] = []
    for record in records:
        record_id = record.get(id_field)
        if not isinstance(record_id, str):
            continue
        if record_id in values:
            issues.append(
                ValidationIssue(
                    "duplicate_record_id",
                    f"{label} ID is used more than once.",
                    record_id,
                )
            )
        values.add(record_id)
    return values, issues


def _cross_record_issues(bundle: dict[str, Any]) -> list[ValidationIssue]:
    observations = bundle["audit_observations"]
    findings = bundle["audit_findings"]
    harness = bundle["audit_harness"]
    corrections = bundle["correction_reassessment_links"]
    operations = bundle["operational_integrity_records"]

    observation_ids, issues = _unique_ids(
        observations, "observation_id", "Observation"
    )
    finding_ids, finding_issues = _unique_ids(findings, "finding_id", "Finding")
    issues.extend(finding_issues)
    correction_ids, correction_issues = _unique_ids(
        corrections, "link_id", "Correction/reassessment link"
    )
    issues.extend(correction_issues)
    operation_ids, operation_issues = _unique_ids(
        operations, "record_id", "Operational record"
    )
    issues.extend(operation_issues)

    identifiers: list[tuple[str, str]] = []
    identifiers.extend((record["observation_id"], "audit_observation") for record in observations)
    identifiers.extend((record["finding_id"], "audit_finding") for record in findings)
    identifiers.extend((record["link_id"], "correction_reassessment_link") for record in corrections)
    identifiers.extend((record["record_id"], "operational_integrity_record") for record in operations)
    identifiers.append((harness["harness_id"], "audit_harness"))

    first_kind_by_id: dict[str, str] = {}
    for identifier, kind in identifiers:
        prior_kind = first_kind_by_id.get(identifier)
        if prior_kind is not None:
            issues.append(
                ValidationIssue(
                    "duplicate_record_id",
                    f"Identifier is reused by {prior_kind} and {kind}.",
                    identifier,
                )
            )
        else:
            first_kind_by_id[identifier] = kind

    all_ids = observation_ids | finding_ids | correction_ids | operation_ids
    harness_id = harness["harness_id"]
    all_ids.add(harness_id)

    declared_input_ids = set(bundle["audit_scope"]["declared_input_record_ids"])
    expected_input_ids = observation_ids | {harness_id}
    if declared_input_ids != expected_input_ids:
        issues.append(
            ValidationIssue(
                "declared_input_mismatch",
                "audit_scope.declared_input_record_ids must name exactly the observations and audit harness.",
            )
        )

    allowed_checker = bundle["audit_scope"]["allowed_checker"]
    if (
        allowed_checker["checker_id"] != harness["checker_id"]
        or allowed_checker["checker_version"] != harness["checker_version"]
    ):
        issues.append(
            ValidationIssue(
                "checker_identity_mismatch",
                "audit_scope.allowed_checker must match audit_harness checker_id and checker_version.",
                harness_id,
            )
        )

    if harness["result"] == "passed" and harness["validity_status"] != "valid":
        issues.append(
            ValidationIssue(
                "unreliable_passed_harness",
                "A passed harness result requires validity_status valid.",
                harness_id,
            )
        )

    finding_by_id = {finding["finding_id"]: finding for finding in findings}
    for finding in findings:
        missing = set(finding["observation_ids"]).difference(observation_ids)
        if missing:
            issues.append(
                ValidationIssue(
                    "missing_observation_reference",
                    f"Finding references unknown observations: {', '.join(sorted(missing))}.",
                    finding["finding_id"],
                )
            )
        if finding["finding_class"] == "stop_required" and not finding["stop_required"]:
            issues.append(
                ValidationIssue(
                    "inconsistent_stop_requirement",
                    "A stop_required finding_class must set stop_required to true.",
                    finding["finding_id"],
                )
            )
        if finding["status"] == "closed" and not any(
            link["prior_finding_id"] == finding["finding_id"]
            and link["latest_rereview_outcome"] == "reviewed"
            for link in corrections
        ):
            issues.append(
                ValidationIssue(
                    "closed_finding_without_rereview",
                    "A closed finding requires a linked correction/reassessment with reviewed outcome.",
                    finding["finding_id"],
                )
            )

    for link in corrections:
        prior_finding_id = link["prior_finding_id"]
        if prior_finding_id not in finding_by_id:
            issues.append(
                ValidationIssue(
                    "missing_finding_reference",
                    "correction_reassessment_link references an unknown finding.",
                    link["link_id"],
                )
            )
        elif link["prior_affected_identity"] != finding_by_id[prior_finding_id]["affected_identity"]:
            issues.append(
                ValidationIssue(
                    "affected_identity_mismatch",
                    "Correction link prior_affected_identity must match its prior finding.",
                    link["link_id"],
                )
            )

    for operation in operations:
        if operation["record_type"] == "worktree_recovery_preflight":
            listed_state = operation["worktree_listed_state"]
            disposition = operation["recovery_disposition"]
            if listed_state in {"active", "locked", "unknown"} and disposition != "stop":
                issues.append(
                    ValidationIssue(
                        "unsafe_worktree_recovery_disposition",
                        "Active, locked, or unknown worktree metadata requires recovery_disposition stop.",
                        operation["record_id"],
                    )
                )
            if (
                listed_state == "prunable"
                and disposition == "separately_authorized_maintenance"
                and operation["physical_worktree_state"] != "missing"
            ):
                issues.append(
                    ValidationIssue(
                        "incomplete_worktree_preflight",
                        "A separately authorized maintenance disposition requires a missing physical worktree.",
                        operation["record_id"],
                    )
                )

    return issues


def validate_bundle_path(raw_path: Path) -> dict[str, Any]:
    """Return a bounded structural result without writing any files."""
    safe_path, path_issue = _safe_bundle_path(raw_path)
    if path_issue is not None:
        return {"status": "not_assessed", "issues": [path_issue.as_dict()]}

    bundle, bundle_issue = _load_json(safe_path)
    if bundle_issue is not None:
        return {"status": "not_assessed", "issues": [bundle_issue.as_dict()]}

    schema, schema_issue = _load_json(SCHEMA_PATH)
    if schema_issue is not None:
        return {"status": "not_assessed", "issues": [schema_issue.as_dict()]}

    issues = _schema_issues(bundle, schema)
    if not issues:
        issues.extend(_cross_record_issues(bundle))

    if any(issue.code.startswith("not_assessed") for issue in issues):
        status = "not_assessed"
    elif issues:
        status = "invalid"
    else:
        status = "valid"

    return {
        "status": status,
        "bundle_id": bundle.get("bundle_id"),
        "issues": [issue.as_dict() for issue in issues],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate one metadata-only governed integrity audit bundle."
    )
    parser.add_argument(
        "--bundle",
        required=True,
        type=Path,
        help="Absolute path to one caller-supplied JSON bundle.",
    )
    args = parser.parse_args(argv)
    result = validate_bundle_path(args.bundle)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "valid" else 2


if __name__ == "__main__":
    raise SystemExit(main())
