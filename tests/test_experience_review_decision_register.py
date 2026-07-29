"""Focused tests for the generic proportionate L1 decision-register contract."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "experience_review_decision_register"
SCHEMA = ROOT / "system" / "09_schemas_records_and_templates" / "experience_review_decision_register.schema.json"
REGISTRY = ROOT / "tests" / "fixtures" / "controlled_experience_vocabulary" / "valid" / "synthetic-vocabulary.json"


def _load_validator() -> object:
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("experience_review_decision_register_validator", SCRIPTS / "validate_experience_review_decision_register.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load experience review decision-register validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


class ExperienceReviewDecisionRegisterTests(unittest.TestCase):
    def _fixture(self, name: str) -> dict[str, object]:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def _schema_errors(self, payload: dict[str, object]) -> list[object]:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        return list(Draft202012Validator(schema).iter_errors(payload))

    def _validate_fixture(self, name: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temporary:
            register_path = Path(temporary) / "register.json"
            register_path.write_text(json.dumps(self._fixture(name)), encoding="utf-8")
            return VALIDATOR.validate(str(REGISTRY.resolve()), str(register_path.resolve()), str(SCHEMA.resolve()))

    def test_template_and_four_final_dispositions_validate(self) -> None:
        template = json.loads((ROOT / "assets" / "experience-vocabulary" / "experience-review-decision-register.template.json").read_text(encoding="utf-8"))
        self.assertEqual([], self._schema_errors(template))
        for name in (
            "valid-empty-register.json",
            "valid-mapped-decision.json",
            "valid-not-mapped-decision.json",
            "valid-deferred-decision.json",
            "valid-blocked-decision.json",
        ):
            with self.subTest(name=name):
                self.assertEqual([], self._schema_errors(self._fixture(name)))
                self.assertEqual("structurally_valid", self._validate_fixture(name)["status"])

    def test_schema_rejects_non_mapped_terms_and_prohibited_authority(self) -> None:
        for name in ("invalid-non-mapped-terms.json", "invalid-prohibited-authority-field.json"):
            with self.subTest(name=name):
                self.assertNotEqual([], self._schema_errors(self._fixture(name)))

    def test_validator_rejects_real_twenty_one_entry_synthetic_fixture(self) -> None:
        fixture = self._fixture("invalid-batch-over-twenty.json")
        self.assertEqual(21, len(fixture["decisions"]))
        self.assertEqual(21, len({item["decision_id"] for item in fixture["decisions"]}))
        result = self._validate_fixture("invalid-batch-over-twenty.json")
        self.assertEqual("structurally_invalid", result["status"])
        self.assertIn("l1_batch_over_twenty", {issue["code"] for issue in result["issues"]})

    def test_validator_reads_only_caller_named_json_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            register_path = root / "register.json"
            register_path.write_text(json.dumps(self._fixture("valid-mapped-decision.json")), encoding="utf-8")
            sentinel = root / "source-body.txt"
            sentinel.write_text("must not be opened or changed", encoding="utf-8")
            result = VALIDATOR.validate(str(REGISTRY.resolve()), str(register_path.resolve()), str(SCHEMA.resolve()))
            self.assertEqual("structurally_valid", result["status"])
            self.assertEqual("must not be opened or changed", sentinel.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
