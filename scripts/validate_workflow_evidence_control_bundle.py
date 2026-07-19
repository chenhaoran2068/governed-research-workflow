#!/usr/bin/env python3
"""Validate a metadata-only workflow and evidence control bundle.

The validator opens only a caller-selected bundle JSON and optional baseline
JSON below an explicit root. It never follows pointers, contacts services,
reads data, scans a directory, creates a baseline, or writes output files.
"""

from __future__ import annotations

import argparse
import hashlib
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
BUNDLE_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "workflow_evidence_control_bundle.schema.json"
)
BASELINE_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "workflow_evidence_control_baseline.schema.json"
)
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"
IDENTITY_METHOD_ID = "workflow_evidence_control_canonical_json_sha256_v1"
PROBLEM_EVIDENCE_STATES = {"missing", "unknown", "stale", "conflicting", "superseded"}
UNRESOLVED_DOWNSTREAM_STATES = {
    "downstream_unassessed",
    "downstream_reassessment_required",
}
REQUIRED_VERIFICATION_NON_CLAIMS = {
    "source_semantic_support",
    "human_approval",
    "gate_passage",
    "compliance",
    "scientific_truth",
    "release_readiness",
}
FORBIDDEN_MACHINE_POSITIVE_SCOPE_TERMS = {
    "citation entailment",
    "semantic support",
    "human approval",
    "gate passage",
    "compliance finding",
    "scientific truth",
    "release readiness",
}


class DuplicateJsonKeyError(ValueError):
    """Raised when JSON object parsing would otherwise silently overwrite a key."""


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
        output = {"code": self.code, "message": self.message}
        if self.record_id is not None:
            output["record_id"] = self.record_id
        return output


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
        raw_text = path.read_text(encoding="utf-8")
        parsed = json.loads(raw_text, object_pairs_hook=_reject_duplicate_keys)
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


def canonical_json_bytes(instance: dict[str, Any]) -> bytes:
    """Return the only admitted canonical representation for baseline identity."""
    return json.dumps(
        instance,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_json_sha256(instance: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(instance)).hexdigest()


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


def _resolve_root(root_argument: Path) -> tuple[Path | None, ValidationIssue | None]:
    requested = root_argument.expanduser()
    if not requested.is_absolute() or ".." in requested.parts:
        return None, ValidationIssue("unsafe_root_path", "--root must be an absolute physical path without parent-traversal segments.")
    current = Path(requested.anchor)
    for component in requested.parts[1:]:
        current = current / component
        if _is_direct_indirection(current):
            return None, ValidationIssue("unsafe_root_path", "--root must not contain a symbolic link or Windows reparse point.")
    try:
        root = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue("not_assessed_root", "--root could not be resolved safely.")
    if not root.is_dir():
        return None, ValidationIssue("invalid_root", "--root must resolve to a directory.")
    return root, None


def _safe_relative_json_path(raw_path: str, root: Path, label: str) -> tuple[Path | None, ValidationIssue | None]:
    if not raw_path or "\\" in raw_path:
        return None, ValidationIssue("unsafe_input_path", f"{label} must be a nonempty portable relative path using '/'.")
    posix_path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive or ".." in posix_path.parts:
        return None, ValidationIssue("unsafe_input_path", f"{label} must not be absolute, drive-qualified, or contain '..'.")
    candidate = root.joinpath(*posix_path.parts)
    if _contains_indirection(candidate, stop_at=root):
        return None, ValidationIssue("unsafe_input_path", f"{label} must not traverse a symbolic link or Windows reparse point.")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        return None, ValidationIssue("missing_or_outside_input", f"{label} must resolve to an existing regular file under --root.")
    if resolved.suffix.lower() != ".json" or not resolved.is_file():
        return None, ValidationIssue("invalid_input_file", f"{label} must resolve to a regular JSON file.")
    return resolved, None


def _safe_pointer_issue(pointer: dict[str, Any], record_id: str) -> ValidationIssue | None:
    value = pointer["pointer_value"]
    pointer_type = pointer["pointer_type"]
    if value != value.strip() or "\x00" in value or "\r" in value or "\n" in value:
        return ValidationIssue("unsafe_pointer", "Pointer values must be single-line bounded identifiers without control characters.", record_id)
    if pointer_type == "public_url":
        if not (value.startswith("https://") or value.startswith("http://")):
            return ValidationIssue("unsafe_pointer", "A public_url pointer must use http:// or https://.", record_id)
        if any(token in value for token in ("@", "?", "#")):
            return ValidationIssue("unsafe_pointer", "A public_url pointer must not include credentials, query parameters, or fragments.", record_id)
    elif value.startswith("/") or value.startswith("\\") or (len(value) > 1 and value[1] == ":") or "\\" in value:
        return ValidationIssue("unsafe_pointer", "Non-URL pointer values must not be absolute or Windows path-like.", record_id)
    return None


def _record_index(records: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[ValidationIssue]]:
    indexed: dict[str, dict[str, Any]] = {}
    issues: list[ValidationIssue] = []
    for record in records:
        record_id = record.get("record_id")
        if not isinstance(record_id, str):
            continue
        if record_id in indexed:
            issues.append(ValidationIssue("duplicate_record_id", "record_id is used more than once.", record_id))
            continue
        indexed[record_id] = record
    return indexed, issues


def _require_record_type(
    records: dict[str, dict[str, Any]],
    target_id: str,
    expected_type: str,
    owner_id: str,
    field_name: str,
) -> ValidationIssue | None:
    target = records.get(target_id)
    if target is None:
        return ValidationIssue("missing_record_reference", f"{field_name} references an unknown record {target_id!r}.", owner_id)
    if target["record_type"] != expected_type:
        return ValidationIssue("wrong_record_type", f"{field_name} must reference {expected_type}, not {target['record_type']}.", owner_id)
    return None


def _generic_reference_issues(
    records: dict[str, dict[str, Any]],
    owner_id: str,
    references: list[str],
    field_name: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for target_id in references:
        if target_id == owner_id:
            issues.append(ValidationIssue("self_record_reference", f"{field_name} must not reference its own record.", owner_id))
        elif target_id not in records:
            issues.append(ValidationIssue("missing_record_reference", f"{field_name} references an unknown record {target_id!r}.", owner_id))
    return issues


def _cross_record_issues(records: dict[str, dict[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    graph: dict[str, set[str]] = {record_id: set() for record_id in records}

    for record_id, record in records.items():
        record_type = record["record_type"]
        if record_type == "evidence_reference_record":
            pointer_issue = _safe_pointer_issue(record["canonical_pointer"], record_id)
            if pointer_issue is not None:
                issues.append(pointer_issue)
        elif record_type == "assertion_evidence_relation_record":
            assertion_issue = _require_record_type(records, record["assertion_id"], "assertion_record", record_id, "assertion_id")
            evidence_issue = _require_record_type(records, record["evidence_id"], "evidence_reference_record", record_id, "evidence_id")
            for issue in (assertion_issue, evidence_issue):
                if issue is not None:
                    issues.append(issue)
            graph[record_id].update({record["assertion_id"], record["evidence_id"]})
            evidence = records.get(record["evidence_id"])
            if (
                record["declared_support_scope"] == "exact"
                and (evidence is None or not evidence.get("exact_locator"))
            ):
                issues.append(ValidationIssue("missing_exact_locator", "An exact-support relation requires a nonempty exact_locator on its evidence record.", record_id))
            if record["assessment_state"] == "invalidated" and not record["invalidation_reference"]:
                issues.append(ValidationIssue("missing_invalidation_reference", "An invalidated relation requires an invalidation reference.", record_id))
            if evidence is not None and evidence["availability_currentness"] in PROBLEM_EVIDENCE_STATES and record["prerequisite_status"] == "satisfied":
                issues.append(ValidationIssue("unsatisfied_evidence_prerequisite", "Unknown, missing, stale, conflicting, or superseded evidence cannot be represented as a satisfied prerequisite.", record_id))
            if record["assessment_state"] == "invalidated" and record["prerequisite_status"] == "satisfied":
                issues.append(ValidationIssue("invalidated_relation_satisfied", "An invalidated relation cannot be represented as a satisfied prerequisite.", record_id))
        elif record_type == "verification_event_record":
            target_ids = record["target_record_ids"]
            input_ids = record["input_record_ids"]
            issues.extend(_generic_reference_issues(records, record_id, target_ids, "target_record_ids"))
            issues.extend(_generic_reference_issues(records, record_id, input_ids, "input_record_ids"))
            graph[record_id].update(target_ids)
            graph[record_id].update(input_ids)
            missing_non_claims = REQUIRED_VERIFICATION_NON_CLAIMS.difference(record["explicit_non_claims"])
            if missing_non_claims:
                issues.append(ValidationIssue("incomplete_verification_non_claims", "Verification records must explicitly retain all bounded non-claims.", record_id))
            normalized_positive_scope = record["positive_scope"].lower()
            if any(term in normalized_positive_scope for term in FORBIDDEN_MACHINE_POSITIVE_SCOPE_TERMS):
                issues.append(ValidationIssue("forbidden_machine_claim", "A machine verification positive_scope must not claim semantic support, human approval, Gate passage, compliance, scientific truth, or release readiness.", record_id))
            diagnostic = record["diagnostic_pointer"]
            if diagnostic is not None:
                pointer_issue = _safe_pointer_issue(diagnostic, record_id)
                if pointer_issue is not None:
                    issues.append(pointer_issue)
        elif record_type == "human_decision_record":
            target_ids = record["target_record_ids"]
            basis_ids = record["decision_basis_record_ids"]
            issues.extend(_generic_reference_issues(records, record_id, target_ids, "target_record_ids"))
            issues.extend(_generic_reference_issues(records, record_id, basis_ids, "decision_basis_record_ids"))
            graph[record_id].update(target_ids)
            graph[record_id].update(basis_ids)
            if record["outcome"] == "approved":
                for basis_id in basis_ids:
                    basis = records.get(basis_id)
                    if basis and basis["record_type"] == "assertion_evidence_relation_record" and basis["prerequisite_status"] != "satisfied":
                        issues.append(ValidationIssue("approved_decision_with_unsatisfied_basis", "An approved decision cannot use a declared relation whose prerequisite is not satisfied.", record_id))
        elif record_type == "revision_and_impact_record":
            changed_object_id = record["changed_object_id"]
            if changed_object_id == record_id:
                issues.append(ValidationIssue("self_record_reference", "changed_object_id must not reference the revision record itself.", record_id))
            elif changed_object_id not in records:
                issues.append(ValidationIssue("missing_record_reference", "changed_object_id must reference a record in this bundle.", record_id))
            graph[record_id].add(changed_object_id)
            downstream_ids = record["affected_downstream_object_ids"]
            issues.extend(_generic_reference_issues(records, record_id, downstream_ids, "affected_downstream_object_ids"))
            graph[record_id].update(downstream_ids)
            if record["creation_mode"] == "initial_creation":
                changed_object = records.get(changed_object_id)
                if changed_object is not None and changed_object["record_revision"] != 1:
                    issues.append(ValidationIssue("invalid_initial_creation", "initial_creation must target a record at record_revision 1.", record_id))
            if record["authorization"]["state"] == "approved" and not record["authorization"]["reference"]:
                issues.append(ValidationIssue("missing_authorization_reference", "Approved revision authorization requires a reference.", record_id))
            if record["downstream_impact_state"] in UNRESOLVED_DOWNSTREAM_STATES:
                for downstream_id in downstream_ids:
                    downstream = records.get(downstream_id)
                    if downstream is not None and _is_consequentially_current(downstream):
                        issues.append(ValidationIssue("downstream_reassessment_not_complete", "A declared downstream object needing reassessment cannot be represented as current or approved.", record_id))

    issues.extend(_circular_reference_issues(graph))
    return issues


def _is_consequentially_current(record: dict[str, Any]) -> bool:
    if record["record_type"] == "assertion_record":
        return record["lifecycle"] == "current"
    if record["record_type"] == "assertion_evidence_relation_record":
        return record["prerequisite_status"] == "satisfied"
    if record["record_type"] == "verification_event_record":
        return record["result"] == "machine_pass"
    if record["record_type"] == "human_decision_record":
        return record["outcome"] == "approved"
    return False


def _circular_reference_issues(graph: dict[str, set[str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            issues.append(ValidationIssue("circular_record_reference", "Record references must not form a cycle.", node))
            return
        if node in visited or node not in graph:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for record_id in graph:
        visit(record_id)
    return issues


def _declared_findings(records: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    findings = {
        "evidence_non_current_record_ids": [],
        "invalidated_relation_record_ids": [],
        "expired_human_decision_record_ids": [],
        "pending_or_unknown_revision_authorization_record_ids": [],
        "downstream_reassessment_record_ids": [],
    }
    for record_id, record in records.items():
        if record["record_type"] == "evidence_reference_record" and record["availability_currentness"] in PROBLEM_EVIDENCE_STATES:
            findings["evidence_non_current_record_ids"].append(record_id)
        elif record["record_type"] == "assertion_evidence_relation_record" and record["assessment_state"] == "invalidated":
            findings["invalidated_relation_record_ids"].append(record_id)
        elif record["record_type"] == "human_decision_record" and record["outcome"] == "expired":
            findings["expired_human_decision_record_ids"].append(record_id)
        elif record["record_type"] == "revision_and_impact_record":
            if record["authorization"]["state"] in {"pending", "unknown"}:
                findings["pending_or_unknown_revision_authorization_record_ids"].append(record_id)
            if record["downstream_impact_state"] in UNRESOLVED_DOWNSTREAM_STATES:
                findings["downstream_reassessment_record_ids"].append(record_id)
    return findings


def _status_from_issues(issues: list[ValidationIssue]) -> str:
    if any(issue.code.startswith("not_assessed") for issue in issues):
        return "not_assessed"
    return "invalid" if issues else "valid"


def _initial_baseline_status(baseline_relative_path: str | None) -> str:
    """Keep an omitted baseline distinct from an unassessable supplied one."""
    return "not_assessed" if baseline_relative_path is not None else "not_supplied"


def _result(
    structural_issues: list[ValidationIssue],
    *,
    checked_record_count: int,
    baseline_status: str,
    baseline_issues: list[ValidationIssue],
    findings: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    structural_status = _status_from_issues(structural_issues)
    all_issues = structural_issues + baseline_issues
    if structural_status == "not_assessed" or baseline_status == "not_assessed":
        result = "not_assessed"
    elif structural_status == "invalid" or baseline_status == "mismatch":
        result = "invalid"
    else:
        result = "valid"
    return {
        "result": result,
        "structural_status": structural_status,
        "baseline_status": baseline_status,
        "checked_record_count": checked_record_count,
        "issues": [issue.as_dict() for issue in all_issues],
        "declared_findings": findings or _declared_findings({}),
        "checks_performed": [
            "explicit_root_and_relative_input_path_safety",
            "duplicate_json_key_refusal",
            "bundle_and_record_schema_validation",
            "cross_record_reference_and_state_checks",
            "optional_canonical_baseline_comparison"
        ],
        "explicit_non_claims": [
            "data_or_pointer_target_access",
            "external_service_action",
            "source_semantic_support",
            "human_identity_or_actual_authorization",
            "compliance_gate_submission_or_release_readiness",
            "scientific_truth",
            "tamper_proof_storage_or_same_authority_rewrite_prevention"
        ]
    }


def validate_bundle(
    root_argument: Path,
    bundle_relative_path: str,
    baseline_relative_path: str | None = None,
) -> dict[str, Any]:
    """Perform only the documented structural checks for explicit JSON inputs."""
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return _result([dependency_issue], checked_record_count=0, baseline_status=_initial_baseline_status(baseline_relative_path), baseline_issues=[])

    root, root_issue = _resolve_root(root_argument)
    if root_issue is not None:
        return _result([root_issue], checked_record_count=0, baseline_status=_initial_baseline_status(baseline_relative_path), baseline_issues=[])
    assert root is not None
    bundle_path, bundle_path_issue = _safe_relative_json_path(bundle_relative_path, root, "--bundle")
    if bundle_path_issue is not None:
        return _result([bundle_path_issue], checked_record_count=0, baseline_status=_initial_baseline_status(baseline_relative_path), baseline_issues=[])
    assert bundle_path is not None

    bundle, bundle_load_issue = _load_json(bundle_path)
    if bundle_load_issue is not None:
        return _result([bundle_load_issue], checked_record_count=0, baseline_status=_initial_baseline_status(baseline_relative_path), baseline_issues=[])
    assert bundle is not None
    bundle_schema, bundle_schema_issue = _load_json(BUNDLE_SCHEMA_PATH)
    baseline_schema, baseline_schema_issue = _load_json(BASELINE_SCHEMA_PATH)
    internal_issues = [issue for issue in (bundle_schema_issue, baseline_schema_issue) if issue is not None]
    if internal_issues:
        return _result(internal_issues, checked_record_count=0, baseline_status=_initial_baseline_status(baseline_relative_path), baseline_issues=[])
    assert bundle_schema is not None and baseline_schema is not None

    structural_issues = _schema_issues(bundle, bundle_schema, "bundle")
    records: dict[str, dict[str, Any]] = {}
    if not structural_issues:
        records, record_index_issues = _record_index(bundle["records"])
        structural_issues.extend(record_index_issues)
        if not structural_issues:
            structural_issues.extend(_cross_record_issues(records))

    baseline_status = "not_supplied"
    baseline_issues: list[ValidationIssue] = []
    if baseline_relative_path is not None:
        if structural_issues:
            baseline_status = "not_assessed"
        else:
            baseline_path, baseline_path_issue = _safe_relative_json_path(baseline_relative_path, root, "--baseline-manifest")
            if baseline_path_issue is not None:
                baseline_status = "not_assessed" if baseline_path_issue.code.startswith("not_assessed") else "mismatch"
                baseline_issues.append(baseline_path_issue)
            else:
                assert baseline_path is not None
                baseline, baseline_load_issue = _load_json(baseline_path)
                if baseline_load_issue is not None:
                    baseline_status = "not_assessed" if baseline_load_issue.code.startswith("not_assessed") else "mismatch"
                    baseline_issues.append(baseline_load_issue)
                else:
                    assert baseline is not None
                    baseline_issues.extend(_schema_issues(baseline, baseline_schema, "baseline manifest"))
                    if baseline_issues:
                        baseline_status = "not_assessed" if any(issue.code.startswith("not_assessed") for issue in baseline_issues) else "mismatch"
                    else:
                        identity_matches = (
                            baseline["bundle_id"] == bundle["bundle_id"]
                            and baseline["bundle_revision"] == bundle["bundle_revision"]
                            and baseline["identity_method_id"] == IDENTITY_METHOD_ID
                            and baseline["canonical_content_sha256"] == canonical_json_sha256(bundle)
                        )
                        if identity_matches:
                            baseline_status = "match"
                        else:
                            baseline_status = "mismatch"
                            baseline_issues.append(ValidationIssue("baseline_mismatch", "The supplied bundle differs from the supplied baseline under the declared canonical JSON SHA-256 method."))

    return _result(
        structural_issues,
        checked_record_count=len(records),
        baseline_status=baseline_status,
        baseline_issues=baseline_issues,
        findings=_declared_findings(records),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only validator for a metadata-only workflow and evidence control bundle.")
    parser.add_argument("--root", type=Path, required=True, help="Explicit root containing the bundle and optional baseline JSON.")
    parser.add_argument("--bundle", required=True, help="Portable relative path to the bundle JSON below --root.")
    parser.add_argument("--baseline-manifest", default=None, help="Optional portable relative path to the baseline JSON below --root.")
    args = parser.parse_args()
    result = validate_bundle(args.root, args.bundle, args.baseline_manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"valid": 0, "invalid": 1, "not_assessed": 2}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
