#!/usr/bin/env python3
"""Read-only structural validation for controlled experience-descriptor profiles."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import validate_experience_reference_index as common


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates"
VOCABULARY_SCHEMA = SCHEMAS / "controlled_experience_vocabulary.schema.json"
CATALOGUE_SCHEMA = SCHEMAS / "controlled_experience_descriptor_catalogue.schema.json"
DECISION_SCHEMA = SCHEMAS / "experience_descriptor_decision_register.schema.json"
INDEX_SCHEMA = SCHEMAS / "experience_descriptor_index.schema.json"
DIMENSIONS = ("domain", "record_kind", "task_trigger", "target_object", "scope")
PROFILE_FIELDS = {
    "domain": "domain_ids",
    "record_kind": "record_kind_id",
    "task_trigger": "task_trigger_ids",
    "target_object": "target_object_ids",
    "scope": "scope_id",
}
FORBIDDEN_PAYLOAD_KEYS = {
    "body",
    "content",
    "copied_text",
    "quote",
    "source_path",
    "path",
    "locator",
    "anchor",
    "attachment",
    "credential",
    "token",
    "approval",
    "approval_reference",
    "evidence",
    "evidence_pointers",
    "currentness",
    "maturity",
    "reuse_status",
    "promotion",
    "owner",
    "action_authority",
}


def _contains_forbidden_payload(value: Any, location: str, issues: list[common.ValidationIssue]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_PAYLOAD_KEYS:
                issues.append(common.ValidationIssue("forbidden_payload_field", f"{location}.{key} is not allowed."))
            _contains_forbidden_payload(nested, f"{location}.{key}", issues)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _contains_forbidden_payload(nested, f"{location}[{index}]", issues)


def _load_inputs(paths: dict[str, str]) -> tuple[dict[str, dict[str, Any]], list[common.ValidationIssue]]:
    loaded: dict[str, dict[str, Any]] = {}
    issues: list[common.ValidationIssue] = []
    for option, raw_path in paths.items():
        path, issue = common._safe_direct_json_path(raw_path, option)
        if issue is not None or path is None:
            issues.append(issue or common.ValidationIssue("not_assessed_input", f"{option} could not be read."))
            continue
        value, issue = common._load_json(path)
        if issue is not None or value is None:
            issues.append(issue or common.ValidationIssue("not_assessed_input", f"{option} could not be parsed."))
            continue
        loaded[option] = value
    return loaded, issues


def _catalogue_values(catalogue: dict[str, Any], issues: list[common.ValidationIssue]) -> tuple[dict[str, set[str]], dict[str, tuple[int, int]]]:
    if catalogue.get("catalogue_state") not in {"active_empty", "active"}:
        issues.append(common.ValidationIssue("catalogue_state", "Catalogue state is invalid."))
    dimensions = catalogue.get("dimensions")
    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        issues.append(common.ValidationIssue("catalogue_dimensions", "Catalogue must define exactly the five descriptor dimensions."))
        return {}, {}

    values_by_dimension: dict[str, set[str]] = {}
    cardinality: dict[str, tuple[int, int]] = {}
    all_ids: set[str] = set()
    has_values = False
    for dimension in DIMENSIONS:
        definition = dimensions[dimension]
        if not isinstance(definition, dict):
            issues.append(common.ValidationIssue("catalogue_dimension", f"{dimension} must be an object."))
            continue
        minimum = definition.get("minimum_count")
        maximum = definition.get("maximum_count")
        values = definition.get("values")
        if not isinstance(minimum, int) or not isinstance(maximum, int) or minimum > maximum:
            issues.append(common.ValidationIssue("catalogue_cardinality", f"{dimension} has invalid cardinality."))
            continue
        if not isinstance(values, list):
            issues.append(common.ValidationIssue("catalogue_values", f"{dimension} values must be an array."))
            continue
        ids = [value.get("descriptor_value_id") for value in values if isinstance(value, dict)]
        if len(ids) != len(values) or len(ids) != len(set(ids)):
            issues.append(common.ValidationIssue("duplicate_descriptor_value", f"{dimension} contains duplicate or malformed descriptor values."))
        duplicate_across_dimensions = set(ids).intersection(all_ids)
        if duplicate_across_dimensions:
            issues.append(common.ValidationIssue("duplicate_descriptor_value", f"Descriptor values may not occur in more than one dimension: {sorted(duplicate_across_dimensions)}."))
        all_ids.update(value for value in ids if isinstance(value, str))
        accepted = {
            value["descriptor_value_id"]
            for value in values
            if isinstance(value, dict) and value.get("lifecycle_status") == "accepted"
        }
        values_by_dimension[dimension] = accepted
        cardinality[dimension] = (minimum, maximum)
        has_values = has_values or bool(values)
    if catalogue.get("catalogue_state") == "active_empty" and has_values:
        issues.append(common.ValidationIssue("active_empty_catalogue_has_values", "An active_empty catalogue must contain no descriptor values."))
    if catalogue.get("catalogue_state") == "active" and not has_values:
        issues.append(common.ValidationIssue("active_catalogue_missing_values", "An active catalogue must contain at least one descriptor value."))
    return values_by_dimension, cardinality


def _validate_profile(profile: Any, values_by_dimension: dict[str, set[str]], cardinality: dict[str, tuple[int, int]], issues: list[common.ValidationIssue], decision_id: str) -> None:
    if not isinstance(profile, dict) or set(profile) != set(PROFILE_FIELDS.values()):
        issues.append(common.ValidationIssue("invalid_descriptor_profile", "A described decision must contain exactly the five descriptor profile fields.", decision_id))
        return
    for dimension, field in PROFILE_FIELDS.items():
        selected = profile[field]
        lower, upper = cardinality.get(dimension, (0, -1))
        selected_ids = selected if isinstance(selected, list) else [selected]
        if not isinstance(selected_ids, list) or len(selected_ids) < lower or len(selected_ids) > upper or len(selected_ids) != len(set(selected_ids)):
            issues.append(common.ValidationIssue("descriptor_cardinality", f"{dimension} violates the catalogue cardinality.", decision_id))
            continue
        unknown = set(selected_ids).difference(values_by_dimension.get(dimension, set()))
        if unknown:
            issues.append(common.ValidationIssue("unknown_descriptor_value", f"{dimension} uses unaccepted descriptor values: {sorted(unknown)}.", decision_id))


def _validate_decisions(
    vocabulary: dict[str, Any],
    catalogue: dict[str, Any],
    register: dict[str, Any],
    issues: list[common.ValidationIssue],
) -> dict[str, dict[str, Any]]:
    if register.get("catalogue_id") != catalogue.get("catalogue_id"):
        issues.append(common.ValidationIssue("catalogue_identity_mismatch", "Decision register must name the supplied descriptor catalogue."))
    values_by_dimension, cardinality = _catalogue_values(catalogue, issues)
    known_terms = {
        term["canonical_term_id"]
        for term in vocabulary.get("terms", [])
        if isinstance(term, dict) and term.get("lifecycle_status") == "accepted"
    }
    decisions = register.get("decisions", [])
    result: dict[str, dict[str, Any]] = {}
    source_ids: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            issues.append(common.ValidationIssue("invalid_decision", "A decision must be an object."))
            continue
        decision_id = decision["decision_id"]
        source_id = decision["source_id"]
        _contains_forbidden_payload(decision, f"decision:{decision_id}", issues)
        if decision_id in result:
            issues.append(common.ValidationIssue("duplicate_descriptor_decision", "Descriptor decision IDs must be unique.", decision_id))
        else:
            result[decision_id] = decision
        if source_id in source_ids:
            issues.append(common.ValidationIssue("duplicate_descriptor_source", "Each source may have only one final descriptor decision per register.", source_id))
        source_ids.add(source_id)
        outcome = decision["final_disposition"]
        profile = decision["descriptor_profile"]
        topic_terms = decision["topic_term_ids"]
        if outcome == "described":
            _validate_profile(profile, values_by_dimension, cardinality, issues, decision_id)
            unknown_terms = set(topic_terms).difference(known_terms)
            if unknown_terms:
                issues.append(common.ValidationIssue("unknown_topic_term", f"Topic terms must be accepted in the supplied vocabulary: {sorted(unknown_terms)}.", decision_id))
        elif profile is not None or topic_terms:
            issues.append(common.ValidationIssue("non_described_payload", "Deferred or blocked decisions must not carry a descriptor profile or topic terms.", decision_id))
    return result


def _validate_index(register: dict[str, Any], index: dict[str, Any], decisions: dict[str, dict[str, Any]], issues: list[common.ValidationIssue]) -> None:
    if index.get("catalogue_id") != register.get("catalogue_id"):
        issues.append(common.ValidationIssue("catalogue_identity_mismatch", "Descriptor index must name the decision register catalogue."))
    reference = index.get("decision_register_reference", {})
    if reference.get("register_id") != register.get("register_id") or reference.get("schema_version") != register.get("schema_version"):
        issues.append(common.ValidationIssue("decision_register_identity_mismatch", "Descriptor index must name the supplied decision register."))
    seen_sources: set[str] = set()
    for entry in index.get("entries", []):
        if not isinstance(entry, dict):
            issues.append(common.ValidationIssue("invalid_descriptor_index_entry", "Descriptor index entries must be objects."))
            continue
        source_id = entry["source_id"]
        decision_id = entry["decision_id"]
        _contains_forbidden_payload(entry, f"index:{source_id}", issues)
        if source_id in seen_sources:
            issues.append(common.ValidationIssue("duplicate_descriptor_index_source", "Descriptor index source IDs must be unique.", source_id))
        seen_sources.add(source_id)
        decision = decisions.get(decision_id)
        if decision is None:
            issues.append(common.ValidationIssue("missing_descriptor_decision", "Each index entry must name a decision in the supplied register.", decision_id))
            continue
        if decision["final_disposition"] != "described":
            issues.append(common.ValidationIssue("non_described_index_entry", "Only a described decision may support a descriptor index entry.", decision_id))
        if decision["source_id"] != source_id:
            issues.append(common.ValidationIssue("descriptor_source_mismatch", "Index source ID must match its decision.", decision_id))
        if entry["decision_sha256"] != common._canonical_sha256(decision):
            issues.append(common.ValidationIssue("descriptor_decision_digest_mismatch", "Index decision digest must match the supplied decision metadata.", decision_id))
        if entry["descriptor_profile"] != decision["descriptor_profile"]:
            issues.append(common.ValidationIssue("descriptor_profile_mismatch", "Index profile must match its decision.", decision_id))
        if entry["topic_term_ids"] != decision["topic_term_ids"]:
            issues.append(common.ValidationIssue("descriptor_topic_mismatch", "Index topic terms must match its decision.", decision_id))


def validate(vocabulary_path: str, catalogue_path: str, decision_register_path: str, descriptor_index_path: str) -> dict[str, Any]:
    loaded, issues = _load_inputs({
        "--vocabulary": vocabulary_path,
        "--catalogue": catalogue_path,
        "--decision-register": decision_register_path,
        "--descriptor-index": descriptor_index_path,
    })
    if issues:
        return {"status": "not_assessed", "issues": [issue.as_dict() for issue in issues]}

    vocabulary = loaded["--vocabulary"]
    catalogue = loaded["--catalogue"]
    register = loaded["--decision-register"]
    index = loaded["--descriptor-index"]
    for instance, schema in (
        (vocabulary, VOCABULARY_SCHEMA),
        (catalogue, CATALOGUE_SCHEMA),
        (register, DECISION_SCHEMA),
        (index, INDEX_SCHEMA),
    ):
        issues.extend(common._schema_issues(instance, schema))
    if issues:
        return {"status": "structurally_invalid", "issues": [issue.as_dict() for issue in issues]}

    decisions = _validate_decisions(vocabulary, catalogue, register, issues)
    _validate_index(register, index, decisions, issues)
    return {
        "status": "structurally_valid" if not issues else "structurally_invalid",
        "catalogue_id": catalogue.get("catalogue_id"),
        "checked_decision_count": len(decisions),
        "checked_index_entry_count": len(index.get("entries", [])),
        "issues": [issue.as_dict() for issue in issues],
        "boundary": "Reads only four caller-named UTF-8 JSON metadata inputs and four bundled schemas. It does not read inventory, source bodies, pointers, locators, paths, hashes, external services, or write any output.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocabulary", required=True, help="Absolute path to one caller-named controlled vocabulary registry JSON file.")
    parser.add_argument("--catalogue", required=True, help="Absolute path to one caller-named descriptor catalogue JSON file.")
    parser.add_argument("--decision-register", required=True, help="Absolute path to one caller-named descriptor decision-register JSON file.")
    parser.add_argument("--descriptor-index", required=True, help="Absolute path to one caller-named descriptor index JSON file.")
    args = parser.parse_args()
    result = validate(args.vocabulary, args.catalogue, args.decision_register, args.descriptor_index)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "structurally_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
