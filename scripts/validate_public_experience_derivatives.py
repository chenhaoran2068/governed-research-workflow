"""Read-only validation for the public experience derivative library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "public-experience-derivatives"
VOCABULARY_SCHEMA_PATH = ASSET_ROOT / "schemas" / "public_experience_vocabulary.schema.json"
CATALOGUE_SCHEMA_PATH = ASSET_ROOT / "schemas" / "public_experience_catalogue.schema.json"
CARD_SCHEMA_PATH = ASSET_ROOT / "schemas" / "public_experience_card.schema.json"
REQUIRED_SECTIONS = (
    "## Applicable Context",
    "## Generic Experience",
    "## Recommended Behavior",
    "## Exclusions And Stop Conditions",
)
EXPECTED_TOPICS = {
    "GRW-TOP-001": "knowledge-governance",
    "GRW-TOP-002": "source-admission",
    "GRW-TOP-003": "source-ownership-and-rights",
    "GRW-TOP-004": "metadata-boundary",
    "GRW-TOP-005": "source-currentness",
    "GRW-TOP-006": "derivative-boundary",
    "GRW-TOP-007": "accountable-human-review",
    "GRW-TOP-008": "bounded-retrieval",
    "GRW-TOP-009": "controlled-pilot",
    "GRW-TOP-010": "scope-expansion",
    "GRW-TOP-011": "reproducibility-boundary",
    "GRW-TOP-012": "revision-impact",
    "GRW-TOP-013": "lifecycle-maintenance",
    "GRW-TOP-014": "capability-stabilization",
    "GRW-TOP-015": "public-material-boundary",
    "GRW-TOP-016": "substantive-reader-facing-delivery",
    "GRW-TOP-017": "plan-state-visibility-and-change-control",
    "GRW-TOP-018": "governed-task-initiation",
}
LEGACY_EXPERIENCE_IDS = {f"GRW-EXP-{number:03d}" for number in range(1, 39)}
NEW_DERIVATIVE_EXPERIENCE_IDS = {f"GRW-EXP-{number:03d}" for number in range(39, 42)}
EXPECTED_EXPERIENCE_IDS = LEGACY_EXPERIENCE_IDS | NEW_DERIVATIVE_EXPERIENCE_IDS
PRIVATE_MARKERS = (
    re.compile(r"\b(?:SRC|EDR|XVT|XVD)-[A-Za-z0-9-]+\b"),
    re.compile(r"(?:[A-Za-z]:[\\/]|\\\\|/Users/|/home/)", re.IGNORECASE),
    re.compile(r"\b(?:sha(?:-?256)?|receipt|chenhaoran2068|99sai)\b", re.IGNORECASE),
)
PROHIBITED_CLAIMS = (
    "automatically load",
    "automatically update",
    "grants access",
    "approves an action",
    "proves external currentness",
    "replaces a human decision",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_errors(schema_path: Path, value: Any) -> list[str]:
    schema = _load_json(schema_path)
    return [error.message for error in Draft202012Validator(schema).iter_errors(value)]


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "true", "false"} or value.startswith("[") or value.startswith("{") or value.startswith('"'):
        return json.loads(value)
    return value


def parse_card(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("card must begin with front matter delimiter")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("card front matter closing delimiter is missing") from error

    front_matter: dict[str, Any] = {}
    for line in lines[1:closing_index]:
        if not line or ":" not in line:
            raise ValueError("front matter line must contain a key and value")
        key, raw_value = line.split(":", 1)
        if not re.fullmatch(r"[a-z_]+", key):
            raise ValueError(f"invalid front matter key: {key}")
        if key in front_matter:
            raise ValueError(f"duplicate front matter key: {key}")
        front_matter[key] = _parse_scalar(raw_value)
    return front_matter, text


def _validate_card_content(card: dict[str, Any], text: str) -> list[str]:
    errors = _schema_errors(CARD_SCHEMA_PATH, card)
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required card section: {section}")
    for marker in PRIVATE_MARKERS:
        if marker.search(text):
            errors.append("card contains a prohibited private marker")
            break
    lowered = text.lower()
    for claim in PROHIBITED_CLAIMS:
        if claim in lowered:
            errors.append(f"card contains prohibited automation or authority claim: {claim}")
    public_id = card.get("public_experience_id")
    legacy_id = card.get("legacy_public_identifier")
    if public_id in LEGACY_EXPERIENCE_IDS:
        expected_legacy_id = f"KGE-{public_id.removeprefix('GRW-EXP-')}"
        if legacy_id != expected_legacy_id:
            errors.append("legacy card must retain its matching KGE identifier")
    elif public_id in NEW_DERIVATIVE_EXPERIENCE_IDS:
        if legacy_id is not None:
            errors.append("new public derivative must not claim a KGE identifier")
    return errors


def validate_card_file(path: Path, known_topics: set[str] | None = None) -> list[str]:
    try:
        card, text = parse_card(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]
    errors = _validate_card_content(card, text)
    if known_topics is not None:
        primary = card.get("primary_public_topic")
        secondary = card.get("optional_secondary_topics", [])
        if primary not in known_topics:
            errors.append("card primary topic is not in vocabulary")
        if isinstance(secondary, list):
            for topic in secondary:
                if topic not in known_topics:
                    errors.append("card secondary topic is not in vocabulary")
    return errors


def _acyclic_hierarchy(terms: dict[str, dict[str, Any]]) -> bool:
    for identifier in terms:
        visited: set[str] = set()
        current = identifier
        while True:
            parent = terms[current]["broader_topic_id"]
            if parent is None:
                break
            if parent not in terms or parent in visited:
                return False
            visited.add(parent)
            current = parent
    return True


def validate_package(vocabulary_path: Path, catalogue_path: Path, cards_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        vocabulary = _load_json(vocabulary_path)
        catalogue = _load_json(catalogue_path)
    except (OSError, json.JSONDecodeError) as error:
        return [str(error)]

    errors.extend(_schema_errors(VOCABULARY_SCHEMA_PATH, vocabulary))
    errors.extend(_schema_errors(CATALOGUE_SCHEMA_PATH, catalogue))
    if errors:
        return errors

    terms = vocabulary["terms"]
    term_ids = [term["public_topic_id"] for term in terms]
    term_map = {term["public_topic_id"]: term for term in terms}
    if len(term_ids) != len(term_map):
        errors.append("vocabulary contains duplicate public topic identifiers")
    if set(term_map) != set(EXPECTED_TOPICS):
        errors.append("v1.6 vocabulary must contain exactly the accepted 15 public topics")
    for identifier, canonical_term in EXPECTED_TOPICS.items():
        if term_map.get(identifier, {}).get("canonical_term") != canonical_term:
            errors.append(f"unexpected canonical term for {identifier}")
    if not _acyclic_hierarchy(term_map):
        errors.append("topic hierarchy is unresolved or cyclic")

    cards = catalogue["cards"]
    experience_ids = [card["public_experience_id"] for card in cards]
    legacy_ids = [card["legacy_public_identifier"] for card in cards if card["legacy_public_identifier"] is not None]
    if len(experience_ids) != len(set(experience_ids)):
        errors.append("catalogue contains duplicate public experience identifiers")
    if len(legacy_ids) != len(set(legacy_ids)):
        errors.append("catalogue contains duplicate legacy public identifiers")
    expected_experience_ids = EXPECTED_EXPERIENCE_IDS
    expected_legacy_ids = {f"KGE-{number:03d}" for number in range(1, 39)}
    if set(experience_ids) != expected_experience_ids:
        errors.append("catalogue must contain exactly GRW-EXP-001 through GRW-EXP-041")
    if set(legacy_ids) != expected_legacy_ids:
        errors.append("catalogue must contain exactly KGE-001 through KGE-038")

    catalogue_by_id = {card["public_experience_id"]: card for card in cards}
    for public_id, entry in catalogue_by_id.items():
        legacy_id = entry["legacy_public_identifier"]
        if public_id in LEGACY_EXPERIENCE_IDS:
            expected_legacy_id = f"KGE-{public_id.removeprefix('GRW-EXP-')}"
            if legacy_id != expected_legacy_id:
                errors.append(f"catalogue legacy identifier mismatch for {public_id}")
        elif public_id in NEW_DERIVATIVE_EXPERIENCE_IDS and legacy_id is not None:
            errors.append(f"catalogue new derivative must not claim a legacy identifier for {public_id}")
        if entry["primary_public_topic"] not in term_map:
            errors.append(f"catalogue primary topic is unresolved for {public_id}")
        if entry["primary_public_topic"] in entry["optional_secondary_topics"]:
            errors.append(f"catalogue repeats its primary topic for {public_id}")
        if any(topic not in term_map for topic in entry["optional_secondary_topics"]):
            errors.append(f"catalogue secondary topic is unresolved for {public_id}")
        expected_path = f"assets/public-experience-derivatives/cards/{public_id}.md"
        if entry["card_path"] != expected_path:
            errors.append(f"catalogue card path is not canonical for {public_id}")

    if not cards_root.is_dir():
        errors.append("explicit cards root is missing")
        return errors
    actual_paths = {path.name for path in cards_root.glob("GRW-EXP-*.md")}
    expected_paths = {f"{public_id}.md" for public_id in expected_experience_ids}
    if actual_paths != expected_paths:
        errors.append("explicit cards root does not contain exactly the declared card files")

    for public_id, entry in catalogue_by_id.items():
        path = cards_root / f"{public_id}.md"
        card_errors = validate_card_file(path, set(term_map))
        errors.extend(f"{public_id}: {error}" for error in card_errors)
        if card_errors:
            continue
        card, _ = parse_card(path)
        for key in ("public_experience_id", "legacy_public_identifier", "primary_public_topic", "optional_secondary_topics", "status"):
            if card[key] != entry[key]:
                errors.append(f"{public_id}: card and catalogue differ for {key}")
        expected_package_version = "v1.6.0" if public_id in LEGACY_EXPERIENCE_IDS else "v1.7.0"
        if card["public_package_version"] != expected_package_version:
            errors.append(f"{public_id}: unexpected public package version")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocabulary", type=Path)
    parser.add_argument("--catalogue", type=Path)
    parser.add_argument("--cards-root", type=Path)
    parser.add_argument("--card-only", type=Path)
    arguments = parser.parse_args()

    if arguments.card_only is not None:
        errors = validate_card_file(arguments.card_only)
    elif arguments.vocabulary and arguments.catalogue and arguments.cards_root:
        errors = validate_package(arguments.vocabulary, arguments.catalogue, arguments.cards_root)
    else:
        parser.error("provide --card-only or all of --vocabulary, --catalogue, and --cards-root")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("structurally_valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
