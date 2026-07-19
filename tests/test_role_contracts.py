"""Structural and boundary tests for v0.8 non-runnable role contracts."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "role_contract.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "role_contract.template.json"
ROLE_DIRECTORY = REPOSITORY_ROOT / "system" / "08_agent_contracts" / "role_contracts"
REFERENCE_PATH = REPOSITORY_ROOT / "references" / "role-contracts.md"
M53_SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "bounded_autonomy_authorization.schema.json"


class RoleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.records = {
            path.stem: json.loads(path.read_text(encoding="utf-8"))
            for path in ROLE_DIRECTORY.glob("*.json")
        }

    def assert_valid(self, record: dict[str, object]) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def test_schema_template_and_exact_two_contracts_are_valid(self) -> None:
        self.assertEqual(self.schema["$id"], "https://github.com/chenhaoran2068/governed-research-workflow/schemas/role_contract.schema.json")
        self.assert_valid(self.template)
        self.assertEqual(set(self.records), {"record_validation_reviewer", "audit_boundary_reviewer"})
        for record in self.records.values():
            self.assert_valid(record)
            self.assertEqual(record["contract_status"], "reviewed")
            self.assertFalse(record["authoritative_inputs"]["automatic_discovery_permitted"])
            self.assertEqual(record["authoritative_inputs"]["unlisted_or_undisclosed_input_policy"], "stop_and_escalate")
            self.assertFalse(record["allowed_outputs"]["may_mutate"])
            self.assertFalse(record["allowed_outputs"]["may_issue_action_command"])
            self.assertTrue(record["audit_record_requirements"]["must_be_recorded"])

    def test_initial_contracts_are_read_only_and_non_runnable(self) -> None:
        for record in self.records.values():
            for action, allowed in record["tool_and_action_boundary"].items():
                self.assertFalse(allowed, action)
            non_claims = " ".join(record["explicit_non_claims"]).lower()
            for required in ("not an agent runtime", "not delegated authority", "not a tool grant", "m53", "not data-access authority", "not a compliance determination", "not a release authority"):
                self.assertIn(required, non_claims)

        validation = self.records["record_validation_reviewer"]
        self.assertEqual(validation["allowed_outputs"]["output_classes"], ["structural_validation_report"])
        audit = self.records["audit_boundary_reviewer"]
        self.assertEqual(audit["allowed_outputs"]["output_classes"], ["bounded_finding_list"])
        self.assertIn("network retrieval", " ".join(audit["stop_and_escalation_conditions"]).lower())

    def test_schema_rejects_missing_boundary_and_privileged_permission(self) -> None:
        missing_stop = copy.deepcopy(self.records["record_validation_reviewer"])
        del missing_stop["stop_and_escalation_conditions"]
        self.assertNotEqual(list(self.validator.iter_errors(missing_stop)), [])

        privileged = copy.deepcopy(self.records["record_validation_reviewer"])
        privileged["tool_and_action_boundary"]["file_write"] = True
        self.assertNotEqual(list(self.validator.iter_errors(privileged)), [])

        unsupported_input = copy.deepcopy(self.records["record_validation_reviewer"])
        unsupported_input["authoritative_inputs"]["allowed_input_classes"] = ["automatic_workspace_discovery"]
        self.assertNotEqual(list(self.validator.iter_errors(unsupported_input)), [])

    def test_role_contract_cannot_substitute_for_m53_or_helper_controls(self) -> None:
        m53_schema = M53_SCHEMA_PATH.read_text(encoding="utf-8")
        reference = REFERENCE_PATH.read_text(encoding="utf-8").lower()
        self.assertNotIn('"role_contract"', m53_schema)
        for required in ("m53", "helper admission", "per-run write confirmation", "data/share evidence"):
            self.assertIn(required, reference)


if __name__ == "__main__":
    unittest.main()
