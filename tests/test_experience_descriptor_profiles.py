"""Focused tests for generic controlled experience-descriptor profiles."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "system" / "09_schemas_records_and_templates"
ASSETS = ROOT / "assets" / "experience-descriptor-profiles"
FIXTURES = ROOT / "tests" / "fixtures" / "experience_descriptor_profiles"
VOCABULARY = ROOT / "tests" / "fixtures" / "controlled_experience_vocabulary" / "valid" / "synthetic-vocabulary.json"
SCRIPT = ROOT / "scripts" / "validate_experience_descriptor_profiles.py"


def _load_validator() -> object:
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("experience_descriptor_profiles_validator", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load descriptor-profile validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


class ExperienceDescriptorProfilesTests(unittest.TestCase):
    def _fixture(self, directory: str, name: str) -> dict[str, object]:
        return json.loads((FIXTURES / directory / name).read_text(encoding="utf-8"))

    def _schemas_validate(self, payload: dict[str, object], schema_name: str) -> None:
        schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(payload))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def _validate(self, catalogue: dict[str, object], decisions: dict[str, object], index: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            paths = {}
            for name, payload in (("catalogue", catalogue), ("decisions", decisions), ("index", index)):
                path = directory / f"{name}.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                paths[name] = path
            return VALIDATOR.validate(
                str(VOCABULARY.resolve()),
                str(paths["catalogue"].resolve()),
                str(paths["decisions"].resolve()),
                str(paths["index"].resolve()),
            )

    def test_blank_templates_are_valid_and_carry_no_decision(self) -> None:
        catalogue = json.loads((ASSETS / "controlled-experience-descriptor-catalogue.template.json").read_text(encoding="utf-8"))
        decisions = json.loads((ASSETS / "experience-descriptor-decision-register.template.json").read_text(encoding="utf-8"))
        index = json.loads((ASSETS / "experience-descriptor-index.template.json").read_text(encoding="utf-8"))
        self._schemas_validate(catalogue, "controlled_experience_descriptor_catalogue.schema.json")
        self._schemas_validate(decisions, "experience_descriptor_decision_register.schema.json")
        self._schemas_validate(index, "experience_descriptor_index.schema.json")
        result = self._validate(catalogue, decisions, index)
        self.assertEqual("structurally_valid", result["status"], result)
        self.assertEqual(0, result["checked_decision_count"])
        self.assertEqual(0, result["checked_index_entry_count"])

    def test_synthetic_described_profile_and_index_validate(self) -> None:
        result = self._validate(
            self._fixture("valid", "synthetic-descriptor-catalogue.json"),
            self._fixture("valid", "synthetic-descriptor-decision-register.json"),
            self._fixture("valid", "synthetic-descriptor-index.json"),
        )
        self.assertEqual("structurally_valid", result["status"], result)
        self.assertEqual(1, result["checked_decision_count"])
        self.assertEqual(1, result["checked_index_entry_count"])

    def test_unknown_value_and_digest_mismatch_are_refused(self) -> None:
        catalogue = self._fixture("valid", "synthetic-descriptor-catalogue.json")
        index = self._fixture("valid", "synthetic-descriptor-index.json")
        unknown_result = self._validate(catalogue, self._fixture("invalid", "unknown-descriptor-value.json"), index)
        self.assertEqual("structurally_invalid", unknown_result["status"], unknown_result)
        self.assertIn("unknown_descriptor_value", {issue["code"] for issue in unknown_result["issues"]})

        invalid_index = self._fixture("valid", "synthetic-descriptor-index.json")
        invalid_index["entries"][0]["decision_sha256"] = "0" * 64
        digest_result = self._validate(catalogue, self._fixture("valid", "synthetic-descriptor-decision-register.json"), invalid_index)
        self.assertEqual("structurally_invalid", digest_result["status"], digest_result)
        self.assertIn("descriptor_decision_digest_mismatch", {issue["code"] for issue in digest_result["issues"]})

    def test_validator_does_not_open_an_unnamed_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            sentinel = directory / "source-body.txt"
            sentinel.write_text("must remain unread and unchanged", encoding="utf-8")
            result = self._validate(
                self._fixture("valid", "synthetic-descriptor-catalogue.json"),
                self._fixture("valid", "synthetic-descriptor-decision-register.json"),
                self._fixture("valid", "synthetic-descriptor-index.json"),
            )
            self.assertEqual("structurally_valid", result["status"], result)
            self.assertEqual("must remain unread and unchanged", sentinel.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
