#!/usr/bin/env python3
"""Validate one explicit manuscript-style-profile JSON record without discovery or writes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "manuscript_style_profile.schema.json"
REFERENCE_FIELDS = {"profile_reference", "human_decision_reference", "requirement_reference"}
REFERENCE_LIST_FIELDS = {"guidance_references"}


class DuplicateJsonKeyError(ValueError):
    """Raised when the one named JSON input repeats an object key."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_json_object(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".json" or not path.is_file():
        raise ValueError(f"Expected one explicit readable JSON file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def is_safe_project_reference(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if value.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", value):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return False
    return ".." not in re.split(r"[\\/]", value)


def iter_references(payload: Any, path: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            item_path = f"{path}.{key}" if path else key
            if key in REFERENCE_FIELDS and value is not None:
                yield item_path, value
            elif key in REFERENCE_LIST_FIELDS and isinstance(value, list):
                for index, reference in enumerate(value):
                    yield f"{item_path}[{index}]", reference
            yield from iter_references(value, item_path)
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            yield from iter_references(value, f"{path}[{index}]")


def validate_cross_fields(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    profile = payload.get("active_profile", {})
    reporting = payload.get("reporting_guidance", {})
    journal = payload.get("target_journal", {})
    selection_status = profile.get("selection_status")

    if selection_status == "not_declared":
        forbidden = ("profile_id", "profile_reference", "human_decision_reference")
        if (
            profile.get("application_mode") != "not_declared"
            or profile.get("source_boundary_status") != "not_declared"
            or any(profile.get(field) is not None for field in forbidden)
        ):
            issues.append(_issue("invalid_profile_state", "active_profile", "a not-declared profile must not name a profile, reference, decision, application mode, or source status"))
    elif selection_status == "selected":
        if not isinstance(profile.get("profile_id"), str) or not profile["profile_id"].strip():
            issues.append(_issue("invalid_profile_state", "active_profile.profile_id", "a selected profile needs a profile identifier"))
        if profile.get("application_mode") not in {"local_default", "human_selected"}:
            issues.append(_issue("invalid_profile_state", "active_profile.application_mode", "a selected profile needs local_default or human_selected application mode"))
        if not is_safe_project_reference(profile.get("profile_reference")):
            issues.append(_issue("missing_profile_reference", "active_profile.profile_reference", "a selected profile needs a safe profile reference"))
        if profile.get("application_mode") == "human_selected" and not is_safe_project_reference(profile.get("human_decision_reference")):
            issues.append(_issue("missing_human_decision_reference", "active_profile.human_decision_reference", "a human-selected profile needs a safe accountable-human decision reference"))
        if profile.get("application_mode") == "local_default" and profile.get("human_decision_reference") is not None:
            issues.append(_issue("invalid_profile_state", "active_profile.human_decision_reference", "a local-default profile must not present a Study-specific human-selection reference"))
        if profile.get("source_boundary_status") in {"not_declared", "not_applicable"}:
            issues.append(_issue("invalid_profile_state", "active_profile.source_boundary_status", "a selected profile needs a declared source boundary status"))
    elif selection_status == "not_applicable":
        if (
            profile.get("profile_id") is not None
            or profile.get("profile_reference") is not None
            or profile.get("human_decision_reference") is not None
            or profile.get("application_mode") != "not_applicable"
            or profile.get("source_boundary_status") != "not_applicable"
        ):
            issues.append(_issue("invalid_profile_state", "active_profile", "a not-applicable profile must not declare a profile or decision reference"))

    if payload.get("record_status") == "current" and selection_status != "selected":
        issues.append(_issue("invalid_current_record", "record_status", "a current record requires a selected active profile"))
    if payload.get("discipline_scope") == "medical_health" and selection_status == "not_applicable":
        issues.append(_issue("invalid_profile_state", "active_profile", "a medical-health record must select a profile or remain not_declared"))

    guidance_status = reporting.get("status")
    guidance_references = reporting.get("guidance_references", [])
    if guidance_status in {"applicable", "candidate"} and not guidance_references:
        issues.append(_issue("missing_reporting_guidance_reference", "reporting_guidance.guidance_references", "candidate or applicable reporting guidance needs at least one safe reference"))
    if guidance_status in {"not_declared", "not_applicable", "pending", "specialist_review_required"} and guidance_references:
        issues.append(_issue("invalid_reporting_guidance_state", "reporting_guidance.guidance_references", "this reporting-guidance status must not declare guidance references"))

    if journal.get("selection_status") == "no_target_selected":
        if journal.get("journal_name") is not None or journal.get("requirement_reference") is not None or journal.get("requirement_status") != "not_required":
            issues.append(_issue("invalid_journal_state", "target_journal", "a no-target record must not name a journal, requirement reference, or active journal requirement status"))
    elif journal.get("selection_status") == "target_selected":
        if not isinstance(journal.get("journal_name"), str) or not journal["journal_name"].strip():
            issues.append(_issue("invalid_journal_state", "target_journal.journal_name", "a selected target journal needs a journal name"))
        if journal.get("requirement_status") == "current_snapshot_available" and not is_safe_project_reference(journal.get("requirement_reference")):
            issues.append(_issue("missing_journal_requirement_reference", "target_journal.requirement_reference", "a current journal requirement snapshot needs a safe project reference"))
        if journal.get("requirement_status") in {"pending", "stale_or_unknown", "conflict"} and journal.get("requirement_reference") is not None:
            issues.append(_issue("invalid_journal_state", "target_journal.requirement_reference", "unconfirmed journal requirements must not be represented as a current requirement reference"))

    for index, conflict in enumerate(payload.get("conflicts", [])):
        if not isinstance(conflict, dict):
            continue
        if conflict.get("status") == "resolved" and not is_safe_project_reference(conflict.get("human_decision_reference")):
            issues.append(_issue("missing_human_decision_reference", f"conflicts[{index}].human_decision_reference", "a resolved conflict needs a safe accountable-human decision reference"))
        if conflict.get("status") in {"open", "deferred"} and conflict.get("human_decision_reference") is not None:
            issues.append(_issue("invalid_conflict_state", f"conflicts[{index}].human_decision_reference", "an open or deferred conflict must not claim a resolution decision reference"))

    for reference_path, reference in iter_references(payload):
        if not is_safe_project_reference(reference):
            issues.append(_issue("unsafe_project_reference", reference_path, "references must be nonempty project-relative strings without absolute, URI, or parent traversal syntax"))
    return issues


def validate_profile(profile_path: Path) -> dict[str, Any]:
    payload = load_json_object(profile_path)
    schema = load_json_object(SCHEMA_PATH)
    try:
        schema_issues = [
            _issue("schema_validation", "/".join(str(part) for part in error.absolute_path) or "<root>", error.message)
            for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: list(item.absolute_path))
        ]
    except SchemaError as error:
        schema_issues = [_issue("schema_validation", "<schema>", error.message)]
    issues = schema_issues + validate_cross_fields(payload)
    return {"result": "valid" if not issues else "structurally_invalid", "issues": issues}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one explicit manuscript-style-profile JSON record.")
    parser.add_argument("--profile", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        result = validate_profile(parse_args(argv).profile)
    except DuplicateJsonKeyError as error:
        result = {"result": "structurally_invalid", "issues": [_issue("duplicate_json_key", "<root>", str(error))]}
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {"result": "structurally_invalid", "issues": [_issue("schema_validation", "<input>", str(error))]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["result"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
