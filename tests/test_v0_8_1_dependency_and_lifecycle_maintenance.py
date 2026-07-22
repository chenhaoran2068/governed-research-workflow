"""Regression controls for the v0.8.1 dependency and lifecycle maintenance source."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"
MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
RECORD_PATH = RELEASE_ROOT / "V0_8_1_RELEASE_CONTROL_CANDIDATE.json"
SCHEMA_PATH = RELEASE_ROOT / "release_control_record.schema.json"


class V081DependencyAndLifecycleMaintenanceTests(unittest.TestCase):
    def test_historical_v080_scope_remains_separate_from_later_source_identity(self) -> None:
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("## v0.8.1 (dependency and lifecycle maintenance source)", roadmap)
        self.assertIn("## v0.8.0 (historical pre-C4 portability, role-contract, and helper-admission source)", roadmap)
        self.assertIn("historical v0.8.0 pre-C4 release materials", (RELEASE_ROOT / "MODULE.md").read_text(encoding="utf-8"))

    def test_ledger_preserves_v081_capabilities_while_adding_admitted_v09_scope(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        self.assertEqual(ledger["ledger_status"], "release_source_prepared")
        self.assertEqual(ledger["release_context"]["source_release_version"], "v0.11.0")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.10.2")
        self.assertIn("released historical scopes through v0.10.2", ledger["target_claim_scope"])
        records = {record["capability_id"]: record for record in ledger["capabilities"]}
        self.assertEqual(
            set(records).intersection({"GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"}),
            {"GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"},
        )
        for capability_id in ("GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"):
            self.assertEqual(records[capability_id]["version"]["target_release"], "v0.8.0")
            self.assertEqual(records[capability_id]["version"]["last_verified_release"], "v0.8.0")
            self.assertIn("subsequent C4 publication completed", records[capability_id]["approval_reference"])
            self.assertNotIn("v0.8.1", records[capability_id]["approval_reference"])

        for capability_id in ("GRW-CAP-090-01", "GRW-CAP-090-02", "GRW-CAP-090-03"):
            self.assertEqual(records[capability_id]["implementation_status"], "verified")
            self.assertEqual(records[capability_id]["release_disposition"], "admitted")
            self.assertEqual(records[capability_id]["public_claim_status"], "permitted")
            self.assertIsNone(records[capability_id]["version"]["last_verified_release"])

    def test_installation_records_declared_system_version_without_literal_tag_equality(self) -> None:
        install = (RELEASE_ROOT / "INSTALL_UPDATE_ROLLBACK.md").read_text(encoding="utf-8")
        self.assertIn("Record the `system_version` declared by that exact selected Release", install)
        self.assertIn("need not be textually identical to the Git tag", install)
        self.assertIn("exact tag and matching GitHub Release remain independently required", install)
        self.assertNotIn("system_version is the exact selected release version", install)

    def test_current_module_guidance_does_not_reuse_a_pre_c4_source_identity(self) -> None:
        current_modules = (
            REPOSITORY_ROOT / "system" / "INDEX.md",
            REPOSITORY_ROOT / "system" / "07_tools_and_integrations" / "MODULE.md",
            REPOSITORY_ROOT / "system" / "08_agent_contracts" / "MODULE.md",
            REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "MODULE.md",
            REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "MODULE.md",
            REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "MODULE.md",
        )
        combined = "\n".join(path.read_text(encoding="utf-8") for path in current_modules)
        self.assertNotIn("v0.8 pre-C4 release source", combined)
        self.assertIn("v0.9.0 integrity-audit source", combined)
        self.assertIn("historical v0.8.0 pre-C4", combined)

    def test_candidate_records_are_complete_but_do_not_claim_release_or_runtime(self) -> None:
        required = (
            "V0_8_1_RELEASE_GATE.md",
            "V0_8_1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.8.1.md",
            "V0_8_1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_8_1_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.8.1.md",
        )
        for name in required:
            self.assertTrue((RELEASE_ROOT / name).is_file(), name)

        combined = "\n".join((RELEASE_ROOT / name).read_text(encoding="utf-8").lower() for name in required)
        self.assertIn("candidate-only", combined)
        self.assertIn("does not establish publication", combined)
        self.assertNotIn("v0.8.1 is published", combined)
        self.assertNotIn("v0.8.1 is installed", combined)

    def test_release_control_record_uses_an_explicit_unknown_commit_sentinel(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_evidence_incomplete")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertIn("unresolved", record["candidate_identity"]["intended_github_release"].lower())
        self.assertIsNone(record["candidate_review_acceptance_reference"])
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])


if __name__ == "__main__":
    unittest.main()
