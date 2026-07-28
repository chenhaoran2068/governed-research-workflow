"""Focused tests for the generic controlled-vocabulary validator."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "controlled_experience_vocabulary"
SCRIPT = ROOT / "scripts" / "validate_controlled_experience_vocabulary.py"


def _load_validator() -> object:
    spec = importlib.util.spec_from_file_location("controlled_experience_vocabulary_validator", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load controlled vocabulary validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


def _inventory_payload(source_records: list[dict[str, str]] | None = None) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "record_type": "experience_source_inventory",
        "inventory_id": "XSI-900001",
        "metadata_only": True,
        "source_records": source_records or [],
    }


class ControlledExperienceVocabularyTests(unittest.TestCase):
    def _write_json(self, directory: Path, name: str, payload: object) -> Path:
        path = directory / name
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def _validate_fixture(self, fixture: Path) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            inventory = self._write_json(Path(temp_dir), "synthetic-inventory.json", _inventory_payload())
            return VALIDATOR.validate(str(fixture.resolve()), str(inventory.resolve()))

    def test_blank_and_synthetic_registries_validate_without_authority(self) -> None:
        for name in ("blank-vocabulary.json", "synthetic-vocabulary.json"):
            result = self._validate_fixture(FIXTURES / "valid" / name)
            self.assertEqual(result["status"], "structurally_valid", result)
            self.assertEqual(result["checked_source_count"], 0)

    def test_invalid_term_lifecycle_alias_and_tag_cases_are_refused(self) -> None:
        expected_codes = {
            "duplicate-alias.json": "duplicate_label_or_alias",
            "noncanonical-tag.json": "noncanonical_tag",
            "deprecated-canonical-label.json": "deprecated_canonical_label",
        }
        for name, expected_code in expected_codes.items():
            result = self._validate_fixture(FIXTURES / "invalid" / name)
            self.assertEqual(result["status"], "invalid", result)
            self.assertIn(expected_code, {issue["code"] for issue in result["issues"]})

    def test_duplicate_json_key_is_refused_and_no_sentinel_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            registry = directory / "duplicate-key.json"
            registry.write_text(
                '{"schema_version":"1.0.0","schema_version":"1.0.0"}',
                encoding="utf-8",
            )
            inventory = self._write_json(directory, "inventory.json", _inventory_payload())
            sentinel = directory / "sentinel.txt"
            sentinel.write_text("must-remain-unchanged", encoding="utf-8")
            result = VALIDATOR.validate(str(registry.resolve()), str(inventory.resolve()))
            self.assertEqual(result["status"], "invalid")
            self.assertIn("duplicate_json_key", {issue["code"] for issue in result["issues"]})
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "must-remain-unchanged")

    def test_symlink_input_is_refused_when_the_platform_supports_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            target = FIXTURES / "valid" / "blank-vocabulary.json"
            link = directory / "registry-link.json"
            try:
                os.symlink(target, link)
            except OSError as error:
                self.skipTest(f"symbolic links are unavailable: {error}")
            inventory = self._write_json(directory, "inventory.json", _inventory_payload())
            result = VALIDATOR.validate(str(link), str(inventory.resolve()))
            self.assertEqual(result["status"], "not_assessed", result)
            self.assertIn("unsafe_input_path", {issue["code"] for issue in result["issues"]})


if __name__ == "__main__":
    unittest.main()
