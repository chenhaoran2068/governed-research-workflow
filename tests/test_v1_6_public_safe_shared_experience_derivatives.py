"""Regression checks for the v1.6 public-safe shared-experience library."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPOSITORY_ROOT / "assets" / "public-experience-derivatives"
VOCABULARY_PATH = ASSET_ROOT / "public_experience_vocabulary.json"
CATALOGUE_PATH = ASSET_ROOT / "public_experience_catalogue.json"
CARDS_ROOT = ASSET_ROOT / "cards"
VOCABULARY_SCHEMA = ASSET_ROOT / "schemas" / "public_experience_vocabulary.schema.json"
CATALOGUE_SCHEMA = ASSET_ROOT / "schemas" / "public_experience_catalogue.schema.json"
CARD_SCHEMA = ASSET_ROOT / "schemas" / "public_experience_card.schema.json"
VALID_ROOT = ASSET_ROOT / "fixtures" / "valid"
INVALID_ROOT = ASSET_ROOT / "fixtures" / "invalid"

SPEC = importlib.util.spec_from_file_location(
    "validate_public_experience_derivatives",
    REPOSITORY_ROOT / "scripts" / "validate_public_experience_derivatives.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not import v1.6 public validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class V16PublicSafeSharedExperienceDerivativesTests(unittest.TestCase):
    def test_complete_public_package_is_structurally_valid(self) -> None:
        self.assertEqual(VALIDATOR.validate_package(VOCABULARY_PATH, CATALOGUE_PATH, CARDS_ROOT), [])

    def test_exact_public_vocabulary_and_catalogue_contract(self) -> None:
        vocabulary = json.loads(VOCABULARY_PATH.read_text(encoding="utf-8"))
        catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(vocabulary["schema_version"], "1.0.0")
        self.assertEqual(vocabulary["vocabulary_version"], "v1.6.0")
        self.assertEqual(vocabulary["status"], "current_public")
        self.assertEqual(len(vocabulary["terms"]), 15)
        self.assertEqual(
            {term["public_topic_id"] for term in vocabulary["terms"]},
            {f"GRW-TOP-{number:03d}" for number in range(1, 16)},
        )
        self.assertEqual(len(catalogue["cards"]), 38)
        self.assertEqual(
            {card["public_experience_id"] for card in catalogue["cards"]},
            {f"GRW-EXP-{number:03d}" for number in range(1, 39)},
        )
        self.assertEqual(
            {card["legacy_public_identifier"] for card in catalogue["cards"]},
            {f"KGE-{number:03d}" for number in range(1, 39)},
        )

    def test_public_cards_preserve_public_kind_and_boundary(self) -> None:
        cards = [VALIDATOR.parse_card(path)[0] for path in sorted(CARDS_ROOT.glob("GRW-EXP-*.md"))]
        self.assertEqual(len(cards), 38)
        self.assertEqual(sum(card["content_kind"] == "adapted_public_experience_rule" for card in cards), 14)
        self.assertEqual(sum(card["content_kind"] == "redacted_historical_experience_note" for card in cards), 24)
        for card in cards:
            self.assertEqual(card["public_package_version"], "v1.6.0")
            self.assertEqual(card["status"], "current_public_guidance")
            self.assertTrue(card["exclusions_and_stop_conditions"])
            self.assertEqual(VALIDATOR.validate_card_file(CARDS_ROOT / f"{card['public_experience_id']}.md"), [])

    def test_synthetic_schema_fixtures_validate(self) -> None:
        vocabulary = json.loads((VALID_ROOT / "public_experience_vocabulary.json").read_text(encoding="utf-8"))
        catalogue = json.loads((VALID_ROOT / "public_experience_catalogue.json").read_text(encoding="utf-8"))
        vocabulary_schema = json.loads(VOCABULARY_SCHEMA.read_text(encoding="utf-8"))
        catalogue_schema = json.loads(CATALOGUE_SCHEMA.read_text(encoding="utf-8"))
        card_schema = json.loads(CARD_SCHEMA.read_text(encoding="utf-8"))
        card, _ = VALIDATOR.parse_card(VALID_ROOT / "cards" / "GRW-EXP-001.md")
        self.assertEqual(list(Draft202012Validator(vocabulary_schema).iter_errors(vocabulary)), [])
        self.assertEqual(list(Draft202012Validator(catalogue_schema).iter_errors(catalogue)), [])
        self.assertEqual(list(Draft202012Validator(card_schema).iter_errors(card)), [])
        self.assertEqual(VALIDATOR.validate_card_file(VALID_ROOT / "cards" / "GRW-EXP-001.md"), [])

    def test_synthetic_negative_cards_are_rejected(self) -> None:
        for name in (
            "private_identifier_in_card.md",
            "private_path_in_card.md",
            "legacy_identifier_mismatch_card.md",
            "missing_stop_boundary_card.md",
        ):
            self.assertTrue(VALIDATOR.validate_card_file(INVALID_ROOT / name), name)

    def test_unresolved_catalogue_is_rejected(self) -> None:
        errors = VALIDATOR.validate_package(
            VOCABULARY_PATH,
            INVALID_ROOT / "unresolved_primary_topic_catalogue.json",
            CARDS_ROOT,
        )
        self.assertTrue(errors)
        self.assertTrue(any("unresolved" in error or "exactly" in error for error in errors))

    def test_public_route_is_selective_and_non_authoritative(self) -> None:
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        reference = (REPOSITORY_ROOT / "references" / "public-safe-shared-experience-derivatives.md").read_text(encoding="utf-8").lower()
        boundary = (REPOSITORY_ROOT / "PUBLIC_BOUNDARY.md").read_text(encoding="utf-8").lower()
        for text in (skill, reference, boundary):
            self.assertIn("not", text)
        self.assertIn("do not load all cards", skill)
        self.assertIn("selectively read", boundary)
        self.assertIn("does not grant access", boundary)
        self.assertIn("does not discover a workspace", reference)


if __name__ == "__main__":
    unittest.main()
