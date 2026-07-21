#!/usr/bin/env python3
"""Read-only structural validation for one named synthetic exchange-pilot receipt.

The validator reads exactly the supplied receipt, its named v0.10 package
manifest, and the five package records named by that manifest. It performs no
directory discovery, transfer, network action, or write.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from validate_voluntary_experience_package import (  # noqa: E402
    RECORD_KEYS,
    ValidationIssue,
    _contains_indirection,
    _load_json,
    _safe_named_record,
    _schema_issues,
    validate_experience_package,
)


ROOT = SCRIPT_ROOT.parent
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "synthetic_experience_exchange_pilot_receipt.schema.json"
HASH_ALGORITHM = "sha256(posix_relative_path+nul+utf8_json_lf_bytes+nul; case_sensitive_ordinal_sort)"


def _result(status: str, issues: list[ValidationIssue], checked_record_count: int, package_tree_sha256: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "result": status,
        "checked_record_count": checked_record_count,
        "issues": [issue.as_dict() for issue in issues],
    }
    if package_tree_sha256 is not None:
        result["package_tree_sha256"] = package_tree_sha256
    return result


def _schema_issue_status(issues: list[ValidationIssue]) -> str:
    """Keep unavailable or malformed validation dependencies distinct from bad input."""
    return "not_assessed" if any(issue.code.startswith("not_assessed_") for issue in issues) else "structurally_invalid"


def _safe_receipt_path(receipt_path: Path) -> tuple[Path | None, ValidationIssue | None]:
    requested = receipt_path.expanduser()
    lexical_requested = requested if requested.is_absolute() else Path.cwd() / requested
    if _contains_indirection(lexical_requested, stop_at=lexical_requested.parent):
        return None, ValidationIssue("refused_boundary", "The explicit receipt or its direct directory must not traverse a symbolic link or reparse point.")
    try:
        resolved = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue("refused_boundary", "The explicit receipt path could not be resolved safely.")
    if not resolved.is_file() or resolved.suffix.lower() != ".json":
        return None, ValidationIssue("refused_boundary", "The explicit receipt must be a regular JSON file.")
    return resolved, None


def _package_paths(manifest_path: Path, manifest: dict[str, Any]) -> tuple[dict[str, Path] | None, ValidationIssue | None]:
    paths: dict[str, Path] = {"experience-package.json": manifest_path}
    for key in RECORD_KEYS:
        path, issue = _safe_named_record(manifest["records"][key], manifest_path.parent)
        if issue is not None:
            return None, ValidationIssue(issue.code, issue.message, key)
        assert path is not None
        paths[manifest["records"][key]] = path
    return paths, None


def _package_tree_hash(paths: dict[str, Path]) -> str:
    """Hash validated metadata JSON with portable LF line endings.

    The package validator has already required UTF-8 JSON. Normalizing only
    physical CRLF/CR line endings prevents a cross-platform Git checkout from
    changing the declared package identity while leaving JSON content and its
    escaped control characters intact.
    """
    digest = hashlib.sha256()
    for relative_path in sorted(paths):
        digest.update(relative_path.encode("ascii"))
        digest.update(b"\0")
        raw_bytes = paths[relative_path].read_bytes()
        normalized_bytes = raw_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        digest.update(normalized_bytes)
        digest.update(b"\0")
    return digest.hexdigest()


def _relationship_issues(receipt: dict[str, Any], manifest: dict[str, Any], records: dict[str, dict[str, Any]], package_hash: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if receipt["package_id"] != manifest["package_id"]:
        issues.append(ValidationIssue("package_identity_mismatch", "Receipt package_id must equal the named manifest package_id."))
    if receipt["package_revision"] != manifest["package_revision"]:
        issues.append(ValidationIssue("package_revision_mismatch", "Receipt package_revision must equal the named manifest package_revision."))
    if receipt["package_tree_hash_algorithm"] != HASH_ALGORITHM:
        issues.append(ValidationIssue("hash_algorithm_mismatch", "Receipt must use the fixed package-tree hash algorithm."))
    if receipt["package_tree_sha256"] != package_hash:
        issues.append(ValidationIssue("package_hash_mismatch", "Receipt package_tree_sha256 must equal the declared package-tree bytes."))
    correction = records["correction_or_withdrawal_record"]
    declared_state = receipt["declared_correction_or_withdrawal_state"]
    if correction["request_state"] != declared_state:
        issues.append(ValidationIssue("correction_state_mismatch", "Receipt correction state must equal the package correction-or-withdrawal record."))
    if declared_state == "no_request" and receipt["future_governed_use_state"] != "not_requested":
        issues.append(ValidationIssue("future_use_state_mismatch", "A no_request package must keep future governed use not_requested."))
    if declared_state == "human_disposition_recorded":
        if correction["requested_action"] != "correction" or not correction["accountable_human_decision_reference"]:
            issues.append(ValidationIssue("invalid_correction_linkage", "A correction disposition requires action correction and a represented human decision."))
        if receipt["future_governed_use_state"] != "not_requested":
            issues.append(ValidationIssue("future_use_state_mismatch", "A correction disposition cannot represent stopped future governed use."))
    if declared_state == "future_use_stopped":
        if correction["requested_action"] != "withdrawal" or correction["future_use_state"] != "stopped_after_human_decision" or not correction["accountable_human_decision_reference"]:
            issues.append(ValidationIssue("invalid_future_use_stop", "A future-use stop requires the matching withdrawal representation and decision reference."))
        if receipt["future_governed_use_state"] != "stopped_after_human_decision":
            issues.append(ValidationIssue("future_use_state_mismatch", "A future-use-stop package must represent stopped_after_human_decision."))
    return issues


def validate_exchange_pilot(receipt_path: Path) -> dict[str, Any]:
    receipt_path, receipt_path_issue = _safe_receipt_path(receipt_path)
    if receipt_path_issue is not None:
        return _result("refused_boundary", [receipt_path_issue], 0)
    assert receipt_path is not None
    receipt, receipt_issue = _load_json(receipt_path)
    schema, schema_issue = _load_json(SCHEMA_PATH)
    if receipt_issue or schema_issue:
        return _result("not_assessed", [issue for issue in (receipt_issue, schema_issue) if issue is not None], 0)
    raw_manifest_path = receipt.get("package_manifest_path")
    if isinstance(raw_manifest_path, str):
        _, preflight_issue = _safe_named_record(raw_manifest_path, receipt_path.parent)
        if preflight_issue is not None and preflight_issue.code == "refused_boundary":
            return _result(
                "refused_boundary",
                [ValidationIssue(preflight_issue.code, preflight_issue.message, "package_manifest_path")],
                0,
            )
    schema_issues = _schema_issues(receipt, schema, "exchange-pilot receipt")
    if schema_issues:
        return _result(_schema_issue_status(schema_issues), schema_issues, 0)
    manifest_path, manifest_path_issue = _safe_named_record(receipt["package_manifest_path"], receipt_path.parent)
    if manifest_path_issue is not None:
        status = "refused_boundary" if manifest_path_issue.code == "refused_boundary" else "structurally_invalid"
        return _result(status, [ValidationIssue(manifest_path_issue.code, manifest_path_issue.message, "package_manifest_path")], 0)
    assert manifest_path is not None
    package_result = validate_experience_package(manifest_path)
    if package_result["result"] != "structurally_valid":
        return _result(package_result["result"], [ValidationIssue(issue["code"], issue["message"], issue.get("record_key")) for issue in package_result["issues"]], package_result["checked_record_count"])
    manifest, manifest_issue = _load_json(manifest_path)
    if manifest_issue is not None:
        return _result("not_assessed", [manifest_issue], 0)
    paths, paths_issue = _package_paths(manifest_path, manifest)
    if paths_issue is not None:
        status = "refused_boundary" if paths_issue.code == "refused_boundary" else "structurally_invalid"
        return _result(status, [paths_issue], 0)
    assert paths is not None
    records: dict[str, dict[str, Any]] = {}
    for key in RECORD_KEYS:
        path = paths[manifest["records"][key]]
        record, record_issue = _load_json(path)
        if record_issue is not None:
            return _result("structurally_invalid", [ValidationIssue(record_issue.code, record_issue.message, key)], len(records))
        assert record is not None
        records[key] = record
    package_hash = _package_tree_hash(paths)
    issues = _relationship_issues(receipt, manifest, records, package_hash)
    return _result("structurally_invalid" if issues else "structurally_valid", issues, 1 + len(records), package_hash)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only structural validator for one named synthetic exchange-pilot receipt.")
    parser.add_argument("receipt_path", type=Path, help="Explicit path to exchange-pilot-receipt.json.")
    result = validate_exchange_pilot(parser.parse_args().receipt_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"structurally_valid": 0, "structurally_invalid": 1, "not_assessed": 2, "refused_boundary": 3}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
