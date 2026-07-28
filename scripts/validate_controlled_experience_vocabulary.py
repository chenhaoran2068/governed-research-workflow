#!/usr/bin/env python3
"""Read-only structural validation for controlled experience-vocabulary metadata."""

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
REQUIRED_JSONSCHEMA_VERSION = "4.26.0"


class DuplicateJsonKeyError(ValueError):
    """Reject a JSON document that would silently overwrite a key."""


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


def _normalise_label(value: str) -> str:
    return " ".join(value.casefold().split())


def _semantic_vocabulary_issues(registry: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    catalog: dict[str, str] = {}
    for item in registry["tag_catalog"]:
        tag = item["tag"]
        if tag in catalog:
            issues.append(ValidationIssue("duplicate_catalog_tag", "A controlled tag may appear only once.", tag))
        else:
            catalog[tag] = item["status"]

    terms: dict[str, dict[str, Any]] = {}
    label_owners: dict[str, str] = {}
    for term in registry["terms"]:
        term_id = term["canonical_term_id"]
        if term_id in terms:
            issues.append(ValidationIssue("duplicate_term_id", "Canonical term identifiers must be unique.", term_id))
            continue
        terms[term_id] = term

        status = term["lifecycle_status"]
        labels = term["preferred_labels"]
        successor = term["successor_term_id"]
        if status in {"candidate", "accepted"}:
            if not labels:
                issues.append(ValidationIssue("missing_preferred_label", "Candidate and accepted terms require a preferred label.", term_id))
            if successor is not None:
                issues.append(ValidationIssue("unexpected_successor", "Candidate and accepted terms must not name a successor.", term_id))
        else:
            if labels:
                issues.append(ValidationIssue("deprecated_canonical_label", "Deprecated, merged, and renamed terms retain aliases but no canonical label.", term_id))
            if successor is None:
                issues.append(ValidationIssue("missing_successor", "Deprecated, merged, and renamed terms require a successor.", term_id))

        languages: set[str] = set()
        for label in labels:
            language = label["language"]
            if language in languages:
                issues.append(ValidationIssue("conflicting_preferred_label", "A term may have one preferred label per language.", term_id))
            languages.add(language)
            key = _normalise_label(label["value"])
            prior_owner = label_owners.get(key)
            if prior_owner is not None:
                issues.append(ValidationIssue("duplicate_label_or_alias", f"Label is already owned by {prior_owner}.", term_id))
            else:
                label_owners[key] = term_id

        for alias in term["aliases"]:
            key = _normalise_label(alias["value"])
            prior_owner = label_owners.get(key)
            if prior_owner is not None:
                issues.append(ValidationIssue("duplicate_label_or_alias", f"Alias is already owned by {prior_owner}.", term_id))
            else:
                label_owners[key] = term_id

        for tag in term["tag_refs"]:
            if catalog.get(tag) != "accepted":
                issues.append(ValidationIssue("noncanonical_tag", "Term tags must be present and accepted in tag_catalog.", term_id))

    for term_id, term in terms.items():
        successor = term["successor_term_id"]
        if successor is not None and successor not in terms:
            issues.append(ValidationIssue("unknown_successor", "A successor term must be present in this registry.", term_id))
        if successor == term_id:
            issues.append(ValidationIssue("self_successor", "A term cannot name itself as its successor.", term_id))
        for relation_ids in term["relationships"].values():
            for related_id in relation_ids:
                if related_id not in terms:
                    issues.append(ValidationIssue("unknown_related_term", "Term relationships must reference known terms.", term_id))
                elif related_id == term_id:
                    issues.append(ValidationIssue("self_relationship", "A term cannot relate to itself.", term_id))
    return issues


def validate(registry_path: str, inventory_path: str) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    registry_file, registry_path_issue = _safe_direct_json_path(registry_path, "--registry")
    inventory_file, inventory_path_issue = _safe_direct_json_path(inventory_path, "--inventory")
    issues.extend(issue for issue in (registry_path_issue, inventory_path_issue) if issue is not None)
    if issues:
        return {"status": "not_assessed", "issues": [issue.as_dict() for issue in issues]}

    registry, registry_issue = _load_json(registry_file)
    inventory, inventory_issue = _load_json(inventory_file)
    issues.extend(issue for issue in (registry_issue, inventory_issue) if issue is not None)
    if registry is None or inventory is None:
        return {"status": "invalid", "issues": [issue.as_dict() for issue in issues]}

    issues.extend(_schema_issues(registry, VOCABULARY_SCHEMA))
    issues.extend(_schema_issues(inventory, INVENTORY_SCHEMA))
    if not issues:
        issues.extend(_semantic_vocabulary_issues(registry))
        source_ids: set[str] = set()
        for source in inventory["source_records"]:
            source_id = source["source_id"]
            if source_id in source_ids:
                issues.append(ValidationIssue("duplicate_source_id", "Source identifiers must be unique.", source_id))
            source_ids.add(source_id)

    status = "structurally_valid" if not issues else "invalid"
    return {
        "status": status,
        "registry_id": registry.get("registry_id"),
        "inventory_id": inventory.get("inventory_id"),
        "checked_term_count": len(registry.get("terms", [])),
        "checked_source_count": len(inventory.get("source_records", [])),
        "issues": [issue.as_dict() for issue in issues],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, help="Absolute path to one caller-named vocabulary registry JSON file.")
    parser.add_argument("--inventory", required=True, help="Absolute path to one caller-named source-inventory JSON file.")
    args = parser.parse_args()
    result = validate(args.registry, args.inventory)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "structurally_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
