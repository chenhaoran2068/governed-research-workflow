#!/usr/bin/env python3
"""Validate one explicit Study-status snapshot without discovery or writes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "study_status_snapshot.schema.json"
CATALOG_PATH = ROOT / "assets" / "study-lifecycle-stage-catalog.v1.json"
REQUIRED_CONDITIONS = {"StateRecordCurrent", "ReadyForNextTransition"}


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


def is_safe_relative_reference(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", normalized):
        return False
    return all(part not in {"", ".", ".."} for part in normalized.split("#", 1)[0].split("/"))


def _stage_pairs() -> set[tuple[str, str]]:
    catalog = load_json_object(CATALOG_PATH)
    return {(item["id"], item["code"]) for item in catalog["stages"]}


def _references(payload: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    for key in ("last_transition_reference", "project_manifest_reference"):
        yield key, payload.get(key)
    for index, value in enumerate(payload.get("related_record_references", [])):
        yield f"related_record_references[{index}]", value
    for index, condition in enumerate(payload.get("conditions", [])):
        for reference_index, value in enumerate(condition.get("evidence_references", [])):
            yield f"conditions[{index}].evidence_references[{reference_index}]", value
    transition = payload.get("last_transition")
    if isinstance(transition, dict):
        yield "last_transition.human_decision_reference", transition.get("human_decision_reference")


def validate_snapshot(snapshot_path: Path) -> dict[str, Any]:
    payload = load_json_object(snapshot_path)
    schema = load_json_object(SCHEMA_PATH)
    try:
        schema_issues = [
            _issue("schema_validation", "/".join(str(part) for part in error.absolute_path) or "<root>", error.message)
            for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: list(error.absolute_path))
        ]
    except SchemaError as error:
        schema_issues = [_issue("schema_validation", "<schema>", error.message)]
    if schema_issues:
        return {"result": "structurally_invalid", "issues": schema_issues}

    issues: list[dict[str, str]] = []
    stage = payload["current_stage"]
    if stage is not None and (stage["id"], stage["code"]) not in _stage_pairs():
        issues.append(_issue("invalid_stage_pair", "current_stage", "stage id and code do not match the package-owned catalogue"))

    conditions: dict[str, dict[str, Any]] = {}
    for index, condition in enumerate(payload["conditions"]):
        condition_type = condition["type"]
        if condition_type in conditions:
            issues.append(_issue("duplicate_condition_type", f"conditions[{index}].type", "condition types must be unique"))
        conditions[condition_type] = condition
    for required in REQUIRED_CONDITIONS:
        if required not in conditions:
            issues.append(_issue("missing_required_condition", "conditions", f"{required} is required"))

    if payload["study_profile"] == "legacy_unreconciled":
        reconciliation = conditions.get("ReconciliationComplete")
        if reconciliation is None or reconciliation["status"] is True:
            issues.append(_issue("legacy_reconciliation_invalid", "conditions", "legacy_unreconciled must retain an unresolved reconciliation condition"))
    if payload["operating_status"] == "active":
        if stage is None:
            issues.append(_issue("active_stage_missing", "current_stage", "active requires a current stage"))
        if payload["current_focus"] is None:
            issues.append(_issue("active_focus_missing", "current_focus", "active requires a current focus"))
        if payload["next_action_summary"] is None and payload["next_human_decision"] is None:
            issues.append(_issue("active_next_step_missing", "<root>", "active requires a next action or next human decision"))
    if payload["operating_status"] == "queued" and stage is not None:
        issues.append(_issue("queued_stage_present", "current_stage", "queued must not declare a current stage"))
    if payload["operating_status"] in {"paused", "stopped", "archived"} and payload["status_note"] is None:
        issues.append(_issue("status_note_missing", "status_note", "paused, stopped, or archived requires an explanatory status note"))

    transition = payload["last_transition"]
    transition_reference = payload["last_transition_reference"]
    if (transition is None) != (transition_reference is None):
        issues.append(_issue("transition_pair_mismatch", "last_transition", "transition and transition reference must both be present or both be null"))
    if isinstance(transition, dict):
        if transition["to_operating_status"] != payload["operating_status"]:
            issues.append(_issue("transition_status_mismatch", "last_transition.to_operating_status", "transition target must equal operating status"))
        stage_id = stage["id"] if stage else None
        if transition["to_stage_id"] != stage_id:
            issues.append(_issue("transition_stage_mismatch", "last_transition.to_stage_id", "transition target must equal current stage"))
        expected = "status/study_status_transitions.jsonl#" + transition["transition_id"]
        if transition_reference != expected:
            issues.append(_issue("transition_reference_mismatch", "last_transition_reference", "must reference the declared transition id"))
    for path, value in _references(payload):
        if value is not None and not is_safe_relative_reference(value):
            issues.append(_issue("unsafe_reference", path, "references must be nonempty, relative, and free of parent traversal"))
    return {"result": "valid" if not issues else "structurally_invalid", "issues": issues}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one explicit Study-status snapshot JSON record.")
    parser.add_argument("--snapshot", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        result = validate_snapshot(parse_args(argv).snapshot)
    except DuplicateJsonKeyError as error:
        result = {"result": "structurally_invalid", "issues": [_issue("duplicate_json_key", "<root>", str(error))]}
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {"result": "structurally_invalid", "issues": [_issue("input", "<input>", str(error))]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["result"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
