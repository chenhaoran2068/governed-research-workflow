#!/usr/bin/env python3
"""Read-only structural validation for proportionate L1 review decisions."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import validate_experience_reference_index as common


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VOCABULARY_SCHEMA = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "controlled_experience_vocabulary.schema.json"


def validate(registry_path: str, register_path: str, register_schema_path: str) -> dict[str, Any]:
    """Validate only caller-named JSON metadata; never resolve a source."""
    issues: list[common.ValidationIssue] = []
    checked = [
        ("--registry", *common._safe_direct_json_path(registry_path, "--registry")),
        ("--register", *common._safe_direct_json_path(register_path, "--register")),
        ("--register-schema", *common._safe_direct_json_path(register_schema_path, "--register-schema")),
    ]
    issues.extend(issue for _, _, issue in checked if issue is not None)
    if issues:
        return {"status": "not_assessed", "issues": [issue.as_dict() for issue in issues]}

    registry_path_safe = checked[0][1]
    register_path_safe = checked[1][1]
    schema_path_safe = checked[2][1]
    assert registry_path_safe is not None and register_path_safe is not None and schema_path_safe is not None

    registry, registry_issue = common._load_json(registry_path_safe)
    register, register_issue = common._load_json(register_path_safe)
    if registry_issue is not None:
        issues.append(registry_issue)
    if register_issue is not None:
        issues.append(register_issue)
    if issues or registry is None or register is None:
        return {"status": "structurally_invalid", "issues": [issue.as_dict() for issue in issues]}

    issues.extend(common._schema_issues(registry, VOCABULARY_SCHEMA))
    issues.extend(common._schema_issues(register, schema_path_safe))
    if issues:
        return {"status": "structurally_invalid", "issues": [issue.as_dict() for issue in issues]}

    known_terms = {term["canonical_term_id"] for term in registry["terms"]}
    decisions = register["decisions"]
    decision_ids = [decision["decision_id"] for decision in decisions]
    source_ids = [decision["source_id"] for decision in decisions]
    for decision_id, count in Counter(decision_ids).items():
        if count > 1:
            issues.append(common.ValidationIssue("duplicate_decision_id", "Decision IDs must be unique.", decision_id))
    for source_id, count in Counter(source_ids).items():
        if count > 1:
            issues.append(common.ValidationIssue("duplicate_source_decision", "Each source may have only one final decision in one register version.", source_id))
    for batch_id, count in Counter(decision["review_batch_id"] for decision in decisions).items():
        if count > 20:
            issues.append(common.ValidationIssue("l1_batch_over_twenty", "An L1 review batch may contain no more than twenty decisions.", batch_id))
    for decision in decisions:
        for term_id in decision["term_ids"]:
            if term_id not in known_terms:
                issues.append(common.ValidationIssue("unknown_term_id", "Decision terms must exist in the supplied vocabulary registry.", term_id))

    return {
        "status": "structurally_valid" if not issues else "structurally_invalid",
        "register_id": register.get("register_id"),
        "checked_decision_count": len(decisions),
        "issues": [issue.as_dict() for issue in issues],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, help="Absolute path to one caller-named vocabulary registry JSON file.")
    parser.add_argument("--register", required=True, help="Absolute path to one caller-named L1 decision-register JSON file.")
    parser.add_argument("--register-schema", required=True, help="Absolute path to one caller-named decision-register schema JSON file.")
    args = parser.parse_args()
    result = validate(args.registry, args.register, args.register_schema)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "structurally_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
