#!/usr/bin/env python3
"""Validate one explicit joint-review-plan JSON record without discovery or writes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "joint_review_plan.schema.json"
DEFAULT_PACKAGE_ORDER = tuple(f"R{index}" for index in range(11))
ACCEPTED_STATUSES = {"accepted", "accepted_with_conditions"}
RESULTS_ASSEMBLY_MODES = {"display_first", "parallel", "text_provisional"}
REFERENCE_FIELDS = {
    "profile_selection_human_decision_reference",
    "human_decision_reference",
    "replacement_reference",
}
REFERENCE_LIST_FIELDS = {"authority_references", "display_references", "claim_references"}


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
            if key in REFERENCE_FIELDS:
                if value is not None:
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
    profile = payload.get("profile", {})
    route_status = profile.get("route_status")
    route = profile.get("route")
    decision_reference = profile.get("profile_selection_human_decision_reference")
    packages = payload.get("review_packages", [])
    reopen_events = payload.get("reopen_events", [])

    if route_status == "not_declared":
        if (
            route is not None
            or decision_reference is not None
            or profile.get("specialist_profile_need") is not None
            or packages
            or reopen_events
        ):
            issues.append(_issue("schema_validation", "profile", "a not_declared route must not declare a selected route, decision reference, packages, or reopen events"))
    elif route_status == "selected":
        if route not in {"observational_empirical_original_research_v1", "additional_review_profile_required"}:
            issues.append(_issue("schema_validation", "profile.route", "a selected route must use a supported route identifier"))
        if not is_safe_project_reference(decision_reference):
            issues.append(_issue("missing_human_decision_reference", "profile.profile_selection_human_decision_reference", "a selected route requires a safe accountable-human decision reference"))

    if payload.get("plan_status") == "current" and route_status != "selected":
        issues.append(_issue("schema_validation", "plan_status", "a current plan requires a selected review route"))

    if route == "observational_empirical_original_research_v1":
        if profile.get("specialist_profile_need") is not None:
            issues.append(_issue("schema_validation", "profile.specialist_profile_need", "the default route must not claim a specialist profile need"))
        package_ids = [package.get("package_id") for package in packages if isinstance(package, dict)]
        if package_ids != list(DEFAULT_PACKAGE_ORDER):
            issues.append(_issue("invalid_default_package_order", "review_packages", "the default route requires exactly R0 through R10 in dependency order"))
    elif route == "additional_review_profile_required":
        if not isinstance(profile.get("specialist_profile_need"), str) or not profile["specialist_profile_need"].strip():
            issues.append(_issue("schema_validation", "profile.specialist_profile_need", "a specialist-route placeholder requires a stated specialist profile need"))
        if packages or reopen_events:
            issues.append(_issue("invalid_default_package_order", "review_packages", "a specialist-route placeholder must not declare default review packages or reopen events"))

    seen_unit_ids: set[str] = set()
    for package_index, package in enumerate(packages):
        if not isinstance(package, dict):
            continue
        package_path = f"review_packages[{package_index}]"
        package_status = package.get("status")
        package_decision_reference = package.get("human_decision_reference")
        if package_status in ACCEPTED_STATUSES and not is_safe_project_reference(package_decision_reference):
            issues.append(_issue("missing_human_decision_reference", f"{package_path}.human_decision_reference", "an accepted package requires a safe accountable-human decision reference"))

        has_units = "results_work_units" in package
        if package.get("package_id") != "R4" and has_units:
            issues.append(_issue("invalid_results_assembly_mode", f"{package_path}.results_work_units", "only R4 may declare Results work units"))
        for unit_index, unit in enumerate(package.get("results_work_units", [])):
            if not isinstance(unit, dict):
                continue
            unit_path = f"{package_path}.results_work_units[{unit_index}]"
            unit_id = unit.get("unit_id")
            if isinstance(unit_id, str):
                if unit_id in seen_unit_ids:
                    issues.append(_issue("invalid_results_assembly_mode", f"{unit_path}.unit_id", "Results work-unit identifiers must be unique"))
                seen_unit_ids.add(unit_id)
            assembly_mode = unit.get("assembly_mode")
            if assembly_mode not in RESULTS_ASSEMBLY_MODES:
                issues.append(_issue("invalid_results_assembly_mode", f"{unit_path}.assembly_mode", "use display_first, parallel, or text_provisional"))
            if (
                assembly_mode == "text_provisional"
                and unit.get("status") in ACCEPTED_STATUSES
                and unit.get("display_reconciliation_status") != "completed"
            ):
                issues.append(_issue("provisional_results_unit_not_reconciled", unit_path, "accepted provisional text requires completed display reconciliation"))

    for event_index, event in enumerate(reopen_events):
        if not isinstance(event, dict):
            continue
        event_path = f"reopen_events[{event_index}]"
        required = ("event_id", "trigger_class", "affected_package_ids", "downstream_effect", "qa_or_rerun_status", "human_decision_reference")
        if (
            any(not event.get(field) for field in required if field not in {"qa_or_rerun_status"})
            or event.get("qa_or_rerun_status") not in {"not_assessed", "not_required", "required"}
            or not is_safe_project_reference(event.get("human_decision_reference"))
        ):
            issues.append(_issue("invalid_reopen_event", event_path, "a reopen event needs its trigger, affected packages, downstream effect, QA or rerun status, and safe human decision reference"))

    for reference_path, reference in iter_references(payload):
        if not is_safe_project_reference(reference):
            issues.append(_issue("unsafe_project_reference", reference_path, "references must be nonempty project-relative strings without absolute, URI, or parent traversal syntax"))

    return issues


def validate_plan(plan_path: Path) -> dict[str, Any]:
    payload = load_json_object(plan_path)
    schema = load_json_object(SCHEMA_PATH)
    try:
        schema_issues = [
            _issue(
                "schema_validation",
                "/".join(str(part) for part in error.absolute_path) or "<root>",
                error.message,
            )
            for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: list(item.absolute_path))
        ]
    except SchemaError as error:
        schema_issues = [_issue("schema_validation", "<schema>", error.message)]
    issues = schema_issues + validate_cross_fields(payload)
    return {"result": "valid" if not issues else "structurally_invalid", "issues": issues}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one explicit joint-review-plan JSON record.")
    parser.add_argument("--plan", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        result = validate_plan(parse_args(argv).plan)
    except DuplicateJsonKeyError as error:
        result = {"result": "structurally_invalid", "issues": [_issue("duplicate_json_key", "<root>", str(error))]}
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {"result": "structurally_invalid", "issues": [_issue("schema_validation", "<input>", str(error))]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["result"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
