#!/usr/bin/env python3
"""Read-only structural validation for experience-reference index metadata."""

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
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError:  # pragma: no cover - exercised by the CLI environment.
    Draft202012Validator = None
    SchemaError = Exception


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIRECTORY = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates"
VOCABULARY_SCHEMA = SCHEMA_DIRECTORY / "controlled_experience_vocabulary.schema.json"
INVENTORY_SCHEMA = SCHEMA_DIRECTORY / "experience_source_inventory.schema.json"
DECISION_SCHEMA = SCHEMA_DIRECTORY / "experience_mapping_decision.schema.json"
INDEX_SCHEMA = SCHEMA_DIRECTORY / "experience_reference_index.schema.json"
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"


class DuplicateJsonKeyError(ValueError):
    """Reject JSON parsing that would silently overwrite a key."""


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
    if Draft202012Validator is None:
        return ValidationIssue("not_assessed_dependency", "jsonschema is unavailable.")
    if _installed_jsonschema_version() != REQUIRED_JSONSCHEMA_VERSION:
        return ValidationIssue(
            "not_assessed_dependency",
            f"Required dependency jsonschema=={REQUIRED_JSONSCHEMA_VERSION} is unavailable.",
        )
    return None


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _is_indirection(path: Path) -> bool:
    return path.is_symlink() or _is_reparse_point(path)


def _safe_direct_json_path(raw_path: str, option: str) -> tuple[Path | None, ValidationIssue | None]:
    requested = Path(raw_path).expanduser()
    if not requested.is_absolute() or ".." in requested.parts:
        return None, ValidationIssue("unsafe_input_path", f"{option} must be an absolute path without parent traversal.")
    current = Path(requested.anchor)
    for component in requested.parts[1:]:
        current = current / component
        if _is_indirection(current):
            return None, ValidationIssue("unsafe_input_path", f"{option} must not contain a symbolic link or reparse point.")
    try:
        resolved = requested.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, ValidationIssue("not_assessed_input", f"{option} could not be resolved safely.")
    if not resolved.is_file() or _is_indirection(resolved) or resolved.suffix.lower() != ".json":
        return None, ValidationIssue("invalid_input", f"{option} must identify a regular JSON file.")
    return resolved, None


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


def _schema_issues(instance: dict[str, Any], schema_path: Path) -> list[ValidationIssue]:
    dependency_issue = _dependency_issue()
    if dependency_issue is not None:
        return [dependency_issue]
    schema, issue = _load_json(schema_path)
    if issue is not None or schema is None:
        return [ValidationIssue("not_assessed_schema", "Bundled schema could not be read.")]
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except SchemaError as error:
        return [ValidationIssue("not_assessed_schema", f"Bundled schema is invalid: {error.message}.")]
    return [
        ValidationIssue("schema_validation", error.message)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def validate(
    registry_path: str,
    inventory_path: str,
    index_path: str,
    decision_paths: list[str],
) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    checked_paths: list[tuple[str, Path | None, ValidationIssue | None]] = [
        ("--registry", *_safe_direct_json_path(registry_path, "--registry")),
        ("--inventory", *_safe_direct_json_path(inventory_path, "--inventory")),
        ("--index", *_safe_direct_json_path(index_path, "--index")),
    ]
    checked_paths.extend(
        ("--decision-record", *_safe_direct_json_path(raw_path, "--decision-record"))
        for raw_path in decision_paths
    )
    issues.extend(issue for _, _, issue in checked_paths if issue is not None)
    if issues:
        return {"status": "not_assessed", "issues": [issue.as_dict() for issue in issues]}

    loaded: list[dict[str, Any]] = []
    for _, path, _ in checked_paths:
        parsed, issue = _load_json(path)
        if issue is not None:
            issues.append(issue)
        elif parsed is not None:
            loaded.append(parsed)
    if issues:
        return {"status": "invalid", "issues": [issue.as_dict() for issue in issues]}

    registry, inventory, index, *decisions = loaded
    issues.extend(_schema_issues(registry, VOCABULARY_SCHEMA))
    issues.extend(_schema_issues(inventory, INVENTORY_SCHEMA))
    issues.extend(_schema_issues(index, INDEX_SCHEMA))
    for decision in decisions:
        issues.extend(_schema_issues(decision, DECISION_SCHEMA))
    if issues:
        return {"status": "invalid", "issues": [issue.as_dict() for issue in issues]}

    if index["registry_id"] != registry["registry_id"]:
        issues.append(ValidationIssue("registry_identity_mismatch", "The index must name the supplied registry."))
    if index["inventory_id"] != inventory["inventory_id"]:
        issues.append(ValidationIssue("inventory_identity_mismatch", "The index must name the supplied inventory."))
    source_ids = {source["source_id"] for source in inventory["source_records"]}
    term_ids = {term["canonical_term_id"] for term in registry["terms"]}
    decision_by_id: dict[str, dict[str, Any]] = {}
    for decision in decisions:
        decision_id = decision["decision_id"]
        if decision_id in decision_by_id:
            issues.append(ValidationIssue("duplicate_decision_id", "Supplied decision identifiers must be unique.", decision_id))
        else:
            decision_by_id[decision_id] = decision

    entries = index["entries"]
    if index["index_state"] == "active_empty":
        if entries:
            issues.append(ValidationIssue("active_empty_has_entries", "active_empty must not contain mapping entries."))
        if decisions:
            issues.append(ValidationIssue("active_empty_has_decision_input", "active_empty validation does not accept mapping-decision input."))
    elif not entries:
        issues.append(ValidationIssue("active_index_missing_entries", "An active index requires at least one entry."))

    seen_links: set[tuple[str, str]] = set()
    for entry in entries:
        source_id = entry["source_id"]
        decision_id = entry["mapping_decision_id"]
        if source_id not in source_ids:
            issues.append(ValidationIssue("unknown_source_id", "Index entries must name a source in the supplied inventory.", source_id))
        decision = decision_by_id.get(decision_id)
        if decision is None:
            issues.append(ValidationIssue("missing_decision_reference", "Every mapping requires a separately supplied decision record.", decision_id))
        else:
            if decision["decision_state"] != "map":
                issues.append(ValidationIssue("non_mapping_decision", "Only a map decision may support an index entry.", decision_id))
            if not decision["basis_reference_ids"]:
                issues.append(ValidationIssue("missing_decision_basis", "A map decision requires at least one basis reference.", decision_id))
            if decision["source_id"] != source_id:
                issues.append(ValidationIssue("decision_source_mismatch", "Decision and index entry must name the same source.", decision_id))
            if set(decision["term_ids"]) != set(entry["term_ids"]):
                issues.append(ValidationIssue("decision_term_mismatch", "Decision and index entry must name the same term set.", decision_id))
        for term_id in entry["term_ids"]:
            if term_id not in term_ids:
                issues.append(ValidationIssue("unknown_term_id", "Index entries must name a term in the supplied registry.", term_id))
            link = (source_id, term_id)
            if link in seen_links:
                issues.append(ValidationIssue("duplicate_mapping", "A source-term mapping may appear only once.", source_id))
            seen_links.add(link)

    status = "structurally_valid" if not issues else "invalid"
    return {
        "status": status,
        "registry_id": registry.get("registry_id"),
        "inventory_id": inventory.get("inventory_id"),
        "index_id": index.get("index_id"),
        "checked_entry_count": len(entries),
        "checked_decision_count": len(decisions),
        "issues": [issue.as_dict() for issue in issues],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, help="Absolute path to one caller-named vocabulary registry JSON file.")
    parser.add_argument("--inventory", required=True, help="Absolute path to one caller-named source-inventory JSON file.")
    parser.add_argument("--index", required=True, help="Absolute path to one caller-named reference-index JSON file.")
    parser.add_argument("--decision-record", action="append", default=[], help="Absolute path to one caller-named mapping-decision JSON file.")
    args = parser.parse_args()
    result = validate(args.registry, args.inventory, args.index, args.decision_record)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "structurally_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
