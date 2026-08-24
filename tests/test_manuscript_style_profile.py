"""Structural, refusal, and CLI checks for one explicit manuscript-style-profile record."""

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
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "manuscript_style_profile.schema.json"
TEMPLATE_PATH = ROOT / "assets" / "manuscript-style-profile.template.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_manuscript_style_profile.py"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "manuscript_style_profile"


def load_validator_module():
    specification = importlib.util.spec_from_file_location("manuscript_style_profile_validator", VALIDATOR_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load manuscript-style-profile validator")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


VALIDATOR = load_validator_module()


class ManuscriptStyleProfileTests(unittest.TestCase):
    def validate_fixture(self, group: str, name: str) -> dict[str, object]:
        return VALIDATOR.validate_profile(FIXTURE_ROOT / group / name)

    def test_schema_and_blank_template_are_valid_without_declaring_a_profile(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(template)), [])
        self.assertEqual(VALIDATOR.validate_profile(TEMPLATE_PATH)["result"], "valid")

    def test_medical_local_default_keeps_manual_verification_limit_visible(self) -> None:
        result = self.validate_fixture("valid", "medical_local_default.json")
        self.assertEqual(result["result"], "valid")
        payload = json.loads((FIXTURE_ROOT / "valid" / "medical_local_default.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["active_profile"]["profile_id"], "ama_11_default")
        self.assertEqual(payload["active_profile"]["source_boundary_status"], "manual_verification_required")
        self.assertEqual(payload["target_journal"]["precedence_rule"], "journal_overrides_style_profile")

    def test_invalid_fixtures_report_boundary_codes(self) -> None:
        expected = {
            "medical_not_applicable.json": "invalid_profile_state",
            "journal_snapshot_without_reference.json": "missing_journal_requirement_reference",
        }
        for name, code in expected.items():
            with self.subTest(name=name):
                result = self.validate_fixture("invalid", name)
                self.assertEqual(result["result"], "structurally_invalid")
                self.assertIn(code, {issue["code"] for issue in result["issues"]})

    def test_default_and_human_selected_profiles_have_distinct_decision_rules(self) -> None:
        payload = json.loads((FIXTURE_ROOT / "valid" / "medical_local_default.json").read_text(encoding="utf-8"))

        default_with_human_selection = json.loads(json.dumps(payload))
        default_with_human_selection["active_profile"]["human_decision_reference"] = "00_state/lifecycle/style-selection.json"
        default_result = VALIDATOR.validate_cross_fields(default_with_human_selection)
        self.assertIn("invalid_profile_state", {issue["code"] for issue in default_result})

        human_selected_without_decision = json.loads(json.dumps(payload))
        human_selected_without_decision["active_profile"]["application_mode"] = "human_selected"
        human_result = VALIDATOR.validate_cross_fields(human_selected_without_decision)
        self.assertIn("missing_human_decision_reference", {issue["code"] for issue in human_result})

    def test_reference_guard_rejects_absolute_uri_and_parent_forms(self) -> None:
        for unsafe_reference in ("C:\\private\\record.json", "/private/record.json", "https://example.invalid/record", "09_manuscript/../record.json"):
            with self.subTest(unsafe_reference=unsafe_reference):
                self.assertFalse(VALIDATOR.is_safe_project_reference(unsafe_reference))
        self.assertTrue(VALIDATOR.is_safe_project_reference("09_manuscript/drafting_requirement_stack.yaml#active_style_profile"))

    def test_cli_reads_only_the_named_profile_and_returns_structured_output(self) -> None:
        profile = FIXTURE_ROOT / "valid" / "medical_local_default.json"
        original = profile.read_bytes()
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR_PATH), "--profile", str(profile)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["result"], "valid")
        self.assertEqual(profile.read_bytes(), original)

    def test_validator_has_no_discovery_network_or_writer_route(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        for forbidden in ("os.walk", "rglob", "glob(", "requests", "urllib", "http.client", "subprocess", "write_text", "write_bytes", "mkdir", "unlink", "replace("):
            self.assertNotIn(forbidden, source)
        guidance = " ".join((ROOT / "references" / "manuscript-style-profile-contract.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("does not automatically select", guidance)
        self.assertIn("journal controls", guidance)


if __name__ == "__main__":
    unittest.main()
