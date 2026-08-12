"""Structural, refusal, and CLI checks for one explicit joint-review plan."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "joint_review_plan.schema.json"
TEMPLATE_PATH = ROOT / "assets" / "joint-review-plan.template.json"
MARKDOWN_TEMPLATE_PATH = ROOT / "assets" / "joint-review-plan.template.md"
VALIDATOR_PATH = ROOT / "scripts" / "validate_joint_review_plan.py"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "joint_review_plan"


def load_validator_module():
    specification = importlib.util.spec_from_file_location("joint_review_plan_validator", VALIDATOR_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load joint-review-plan validator")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


VALIDATOR = load_validator_module()


class JointReviewPlanTests(unittest.TestCase):
    def validate_fixture(self, group: str, name: str) -> dict[str, object]:
        return VALIDATOR.validate_plan(FIXTURE_ROOT / group / name)

    def test_schema_and_blank_template_are_valid_without_declaring_a_route(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(template))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        result = VALIDATOR.validate_plan(TEMPLATE_PATH)
        self.assertEqual(result["result"], "valid")
        self.assertEqual(template["profile"]["route_status"], "not_declared")
        self.assertEqual(template["review_packages"], [])
        self.assertIn("explanatory only", MARKDOWN_TEMPLATE_PATH.read_text(encoding="utf-8"))

    def test_valid_default_profile_preserves_exact_dependency_order_and_all_results_modes(self) -> None:
        result = self.validate_fixture("valid", "default_observational_draft.json")
        self.assertEqual(result["result"], "valid")
        payload = json.loads((FIXTURE_ROOT / "valid" / "default_observational_draft.json").read_text(encoding="utf-8"))
        self.assertEqual([item["package_id"] for item in payload["review_packages"]], [f"R{index}" for index in range(11)])
        units = payload["review_packages"][4]["results_work_units"]
        self.assertEqual({item["assembly_mode"] for item in units}, {"display_first", "parallel", "text_provisional"})

    def test_valid_reopen_preserves_historical_provisional_mode_after_reconciliation(self) -> None:
        result = self.validate_fixture("valid", "default_observational_reopen.json")
        self.assertEqual(result["result"], "valid")
        payload = json.loads((FIXTURE_ROOT / "valid" / "default_observational_reopen.json").read_text(encoding="utf-8"))
        provisional = payload["review_packages"][4]["results_work_units"][2]
        self.assertEqual(provisional["assembly_mode"], "text_provisional")
        self.assertEqual(provisional["display_reconciliation_status"], "completed")
        self.assertEqual(len(payload["reopen_events"]), 1)

    def test_specialist_placeholder_does_not_appear_as_an_observational_review_plan(self) -> None:
        result = self.validate_fixture("valid", "specialist_route_placeholder.json")
        self.assertEqual(result["result"], "valid")
        payload = json.loads((FIXTURE_ROOT / "valid" / "specialist_route_placeholder.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["profile"]["route"], "additional_review_profile_required")
        self.assertEqual(payload["review_packages"], [])

    def test_invalid_fixtures_report_their_required_boundary_code(self) -> None:
        expected_codes = {
            "default_order_for_specialist_route.json": "invalid_default_package_order",
            "accepted_package_without_human_reference.json": "missing_human_decision_reference",
            "results_unit_without_assembly_mode.json": "invalid_results_assembly_mode",
            "reopen_without_affected_package.json": "invalid_reopen_event",
            "absolute_or_parent_reference.json": "unsafe_project_reference",
        }
        for name, expected_code in expected_codes.items():
            with self.subTest(name=name):
                result = self.validate_fixture("invalid", name)
                self.assertEqual(result["result"], "structurally_invalid")
                codes = {issue["code"] for issue in result["issues"]}
                self.assertIn(expected_code, codes)

    def test_duplicate_keys_are_rejected_without_a_second_file_or_write(self) -> None:
        with self.assertRaises(VALIDATOR.DuplicateJsonKeyError):
            VALIDATOR._reject_duplicate_keys([("route", "one"), ("route", "two")])

    def test_results_unit_and_provisional_reconciliation_boundaries_are_enforced_without_writes(self) -> None:
        payload = json.loads((FIXTURE_ROOT / "valid" / "default_observational_reopen.json").read_text(encoding="utf-8"))
        results_units = payload["review_packages"][4].pop("results_work_units")
        payload["review_packages"][3]["results_work_units"] = results_units
        codes = {issue["code"] for issue in VALIDATOR.validate_cross_fields(payload)}
        self.assertIn("invalid_results_assembly_mode", codes)

        payload = json.loads((FIXTURE_ROOT / "valid" / "default_observational_reopen.json").read_text(encoding="utf-8"))
        provisional = payload["review_packages"][4]["results_work_units"][2]
        provisional["display_reconciliation_status"] = "pending"
        codes = {issue["code"] for issue in VALIDATOR.validate_cross_fields(payload)}
        self.assertIn("provisional_results_unit_not_reconciled", codes)

    def test_reference_guard_rejects_absolute_uri_and_parent_forms(self) -> None:
        for unsafe_reference in ("C:\\private\\record.json", "/private/record.json", "https://example.invalid/record", "03_protocol/../record.json"):
            with self.subTest(unsafe_reference=unsafe_reference):
                self.assertFalse(VALIDATOR.is_safe_project_reference(unsafe_reference))
        self.assertTrue(VALIDATOR.is_safe_project_reference("00_state/lifecycle/decision.json#r4"))

    def test_cli_reads_only_the_named_plan_and_returns_structured_output(self) -> None:
        plan = FIXTURE_ROOT / "valid" / "default_observational_draft.json"
        original = plan.read_bytes()
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR_PATH), "--plan", str(plan)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["result"], "valid")
        self.assertEqual(plan.read_bytes(), original)

    def test_validator_has_no_discovery_network_or_writer_route(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        for forbidden in ("os.walk", "rglob", "glob(", "requests", "urllib", "http.client", "subprocess", "write_text", "write_bytes", "mkdir", "unlink", "replace("):
            self.assertNotIn(forbidden, source)
        self.assertIn("one explicit", source)
        guidance = " ".join((ROOT / "references" / "joint-review-profiles-and-dependency-order.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("does not resolve references", guidance)


if __name__ == "__main__":
    unittest.main()
