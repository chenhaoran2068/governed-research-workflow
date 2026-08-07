"""Synthetic structural tests for GRW-CAP-180-01."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "system" / "09_schemas_records_and_templates"
ASSET_ROOT = ROOT / "assets" / "future-study-lifecycle"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "future_study_lifecycle_contract"
SCRIPT_PATH = ROOT / "scripts" / "validate_future_study_lifecycle_records.py"

SPEC = importlib.util.spec_from_file_location("future_study_lifecycle_validator", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class FutureStudyLifecycleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            "design": json.loads((SCHEMA_ROOT / "study_design_and_classification_record.schema.json").read_text(encoding="utf-8")),
            "governance": json.loads((SCHEMA_ROOT / "governance_readiness_record.schema.json").read_text(encoding="utf-8")),
            "analysis_state": json.loads((SCHEMA_ROOT / "analysis_state_and_freeze_decision.schema.json").read_text(encoding="utf-8")),
            "execution_contract": json.loads((SCHEMA_ROOT / "analysis_execution_contract.schema.json").read_text(encoding="utf-8")),
        }
        cls.valid_bundle = json.loads((FIXTURE_ROOT / "valid" / "in-scope-observational-record-set.json").read_text(encoding="utf-8"))

    def assert_invalid(self, schema_name: str, payload: dict) -> None:
        self.assertTrue(list(Draft202012Validator(self.schemas[schema_name]).iter_errors(payload)))

    def test_blank_templates_validate_without_claiming_facts(self) -> None:
        names = {
            "design": "study-design-and-classification-record.template.json",
            "governance": "governance-readiness-record.template.json",
            "analysis_state": "analysis-state-and-freeze-decision.template.json",
        }
        for schema_name, file_name in names.items():
            payload = json.loads((ASSET_ROOT / file_name).read_text(encoding="utf-8"))
            self.assertEqual(list(Draft202012Validator(self.schemas[schema_name]).iter_errors(payload)), [])
        self.assertEqual(json.loads((ASSET_ROOT / names["design"]).read_text(encoding="utf-8"))["scope_route"], "not_declared")

    def test_valid_declared_metadata_bundle_is_accepted(self) -> None:
        self.assertEqual(VALIDATOR.validate_bundle(self.valid_bundle), [])

    def test_legacy_v1_execution_contract_remains_schema_compatible(self) -> None:
        legacy = json.loads((FIXTURE_ROOT / "valid" / "legacy-v1-execution-contract.json").read_text(encoding="utf-8"))
        self.assertEqual(list(Draft202012Validator(self.schemas["execution_contract"]).iter_errors(legacy)), [])

    def test_out_of_scope_design_requires_additional_charter_route(self) -> None:
        payload = copy.deepcopy(self.valid_bundle["design"])
        payload["classification"]["primary_research_purpose"] = "causal"
        self.assert_invalid("design", payload)

    def test_recorded_governance_requires_safe_evidence_pointers(self) -> None:
        payload = copy.deepcopy(self.valid_bundle["governance"])
        payload["governance_domains"][0]["compliance_index_reference"] = None
        self.assert_invalid("governance", payload)

    def test_current_freeze_requires_human_decision_reference(self) -> None:
        payload = copy.deepcopy(self.valid_bundle["analysis_state"])
        payload["human_decision_reference"] = None
        self.assert_invalid("analysis_state", payload)

    def test_approved_v2_contract_requires_safe_lifecycle_references(self) -> None:
        payload = copy.deepcopy(self.valid_bundle["execution_contract"])
        payload["contract_status"] = "approved_for_use"
        payload["approval_reference"] = "00_state/lifecycle/approval.md"
        payload["design_and_classification_record_reference"] = None
        self.assert_invalid("execution_contract", payload)

    def test_absolute_and_parent_references_are_refused(self) -> None:
        payload = copy.deepcopy(self.valid_bundle["execution_contract"])
        payload["governance_readiness_record_reference"] = "../outside.json"
        self.assert_invalid("execution_contract", payload)
        payload["governance_readiness_record_reference"] = "C:\\outside.json"
        self.assert_invalid("execution_contract", payload)

    def test_explicit_validator_reads_only_caller_supplied_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            paths = {}
            for key, payload in self.valid_bundle.items():
                path = folder / f"{key}.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                paths[key] = path
            result = VALIDATOR.validate_explicit_paths(
                paths["design"], paths["governance"], paths["analysis_state"], paths["execution_contract"]
            )
            self.assertEqual(result, {"status": "valid", "errors": []})
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for forbidden in ("rglob(", ".glob(", "subprocess", "requests", "urlopen", "write_text("):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
