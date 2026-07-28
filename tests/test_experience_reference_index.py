"""Focused tests for the generic experience-reference-index validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / "tests" / "fixtures" / "controlled_experience_vocabulary" / "valid" / "synthetic-vocabulary.json"
FIXTURES = ROOT / "tests" / "fixtures" / "experience_reference_index"
SCRIPT = ROOT / "scripts" / "validate_experience_reference_index.py"


def _load_validator() -> object:
    spec = importlib.util.spec_from_file_location("experience_reference_index_validator", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load experience reference index validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


def _inventory_payload(inventory_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "record_type": "experience_source_inventory",
        "inventory_id": inventory_id,
        "metadata_only": True,
        "source_records": [
            {
                "source_id": "SRC-SYN-001",
                "source_kind": "shared_candidate",
                "owner_scope": "cross_project_shared",
                "review_state": "metadata_reviewed",
                "descriptor": "Synthetic source descriptor only; no pointer or content is present."
            }
        ]
    }


class ExperienceReferenceIndexTests(unittest.TestCase):
    def _write_json(self, directory: Path, name: str, payload: object) -> Path:
        path = directory / name
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def _read_fixture(self, *parts: str) -> dict[str, object]:
        return json.loads((FIXTURES.joinpath(*parts)).read_text(encoding="utf-8"))

    def _validate(self, index_payload: dict[str, object], decisions: list[dict[str, object]]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            inventory = self._write_json(directory, "inventory.json", _inventory_payload(index_payload["inventory_id"]))
            index = self._write_json(directory, "index.json", index_payload)
            decision_paths = [
                str(self._write_json(directory, f"decision-{position}.json", decision).resolve())
                for position, decision in enumerate(decisions)
            ]
            return VALIDATOR.validate(str(VOCABULARY.resolve()), str(inventory.resolve()), str(index.resolve()), decision_paths)

    def test_active_empty_index_and_single_synthetic_mapping_validate(self) -> None:
        empty = self._read_fixture("valid", "active-empty-index.json")
        self.assertEqual(self._validate(empty, [])["status"], "structurally_valid")

        index = self._read_fixture("valid", "single-mapping-index.json")
        decision = self._read_fixture("valid", "synthetic-mapping-decision.json")
        result = self._validate(index, [decision])
        self.assertEqual(result["status"], "structurally_valid", result)
        self.assertEqual(result["checked_entry_count"], 1)

    def test_missing_held_and_duplicate_mapping_states_are_refused(self) -> None:
        missing = self._validate(self._read_fixture("invalid", "missing-decision-reference.json"), [])
        self.assertIn("missing_decision_reference", {issue["code"] for issue in missing["issues"]})

        held_decision = self._read_fixture("valid", "synthetic-mapping-decision.json")
        held_decision["decision_id"] = "XMD-900002"
        held_decision["decision_state"] = "hold"
        held = self._validate(self._read_fixture("invalid", "held-decision-mapping.json"), [held_decision])
        self.assertIn("non_mapping_decision", {issue["code"] for issue in held["issues"]})

        decision = self._read_fixture("valid", "synthetic-mapping-decision.json")
        duplicate = self._validate(self._read_fixture("invalid", "duplicate-mapping.json"), [decision])
        self.assertIn("duplicate_mapping", {issue["code"] for issue in duplicate["issues"]})

    def test_unknown_term_and_active_empty_decision_input_are_refused(self) -> None:
        index = self._read_fixture("valid", "single-mapping-index.json")
        index["entries"][0]["term_ids"] = ["XVT-999999"]
        decision = self._read_fixture("valid", "synthetic-mapping-decision.json")
        decision["term_ids"] = ["XVT-999999"]
        result = self._validate(index, [decision])
        self.assertIn("unknown_term_id", {issue["code"] for issue in result["issues"]})

        empty = self._read_fixture("valid", "active-empty-index.json")
        result = self._validate(empty, [self._read_fixture("valid", "synthetic-mapping-decision.json")])
        self.assertIn("active_empty_has_decision_input", {issue["code"] for issue in result["issues"]})

    def test_validation_does_not_resolve_source_content_or_write_a_sentinel(self) -> None:
        index = self._read_fixture("valid", "active-empty-index.json")
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            inventory = self._write_json(directory, "inventory.json", _inventory_payload(index["inventory_id"]))
            index_path = self._write_json(directory, "index.json", index)
            sentinel = directory / "source-content.txt"
            sentinel.write_text("validator must not open or change this", encoding="utf-8")
            result = VALIDATOR.validate(str(VOCABULARY.resolve()), str(inventory.resolve()), str(index_path.resolve()), [])
            self.assertEqual(result["status"], "structurally_valid", result)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "validator must not open or change this")


if __name__ == "__main__":
    unittest.main()
