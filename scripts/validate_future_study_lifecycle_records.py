#!/usr/bin/env python3
"""Validate four explicit lifecycle records without discovery or writes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {
    "design": ROOT / "system" / "09_schemas_records_and_templates" / "study_design_and_classification_record.schema.json",
    "governance": ROOT / "system" / "09_schemas_records_and_templates" / "governance_readiness_record.schema.json",
    "analysis_state": ROOT / "system" / "09_schemas_records_and_templates" / "analysis_state_and_freeze_decision.schema.json",
    "execution_contract": ROOT / "system" / "09_schemas_records_and_templates" / "analysis_execution_contract.schema.json",
}
EXPECTED_V2_REFERENCES = {
    "design_and_classification_record_reference": "03_protocol/study_design_and_classification_record.json",
    "governance_readiness_record_reference": "02_registry/compliance/governance_readiness_record.json",
    "analysis_state_and_freeze_decision_reference": "00_state/lifecycle/analysis_state_and_freeze_decision.json",
}


def load_json(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".json" or not path.is_file():
        raise ValueError(f"Expected an explicit readable JSON file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def validate_payload(name: str, payload: dict[str, Any]) -> list[str]:
    try:
        schema = load_json(SCHEMAS[name])
        validator = Draft202012Validator(schema)
    except SchemaError as error:
        return [f"{name} schema error: {error.message}"]
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
    ]


def validate_bundle(payloads: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for name, payload in payloads.items():
        errors.extend(f"{name}: {error}" for error in validate_payload(name, payload))
    project_ids = {payload.get("project_id") for payload in payloads.values()}
    if len(project_ids) != 1 or None in project_ids:
        errors.append("all four explicit lifecycle records must use one non-null project_id")
    contract = payloads["execution_contract"]
    if contract.get("contract_version") == "2.0.0":
        for field, expected in EXPECTED_V2_REFERENCES.items():
            if contract.get(field) != expected:
                errors.append(f"execution_contract: {field} must equal {expected} for the v2 profile")
    return errors


def validate_explicit_paths(design: Path, governance: Path, analysis_state: Path, execution_contract: Path) -> dict[str, Any]:
    payloads = {
        "design": load_json(design),
        "governance": load_json(governance),
        "analysis_state": load_json(analysis_state),
        "execution_contract": load_json(execution_contract),
    }
    errors = validate_bundle(payloads)
    return {"status": "valid" if not errors else "invalid", "errors": errors}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate four explicit future-Study lifecycle JSON records.")
    parser.add_argument("--design", required=True, type=Path)
    parser.add_argument("--governance", required=True, type=Path)
    parser.add_argument("--analysis-state", required=True, type=Path)
    parser.add_argument("--execution-contract", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        result = validate_explicit_paths(args.design, args.governance, args.analysis_state, args.execution_contract)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "invalid", "errors": [str(error)]}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
