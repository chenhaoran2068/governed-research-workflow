"""Release-preparation controls for v0.12 synthetic integration assurance."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"
FORBIDDEN_MARKERS = (
    "E:" + chr(92) + "Chen" + "haoran",
    "C:" + chr(92) + "Us" + "ers",
    "99" + "sai",
    "research1",
    "research2",
    "sepsis",
    "paco2",
    "gh" + "p_",
    "github" + "_pat_",
    "BEGIN" + " PRIVATE" + " KEY",
)


class V012ReleasePreparationTests(unittest.TestCase):
    def test_v012_records_are_complete_and_keep_no_new_interface_scope(self) -> None:
        required = (
            "V0_12_SYNTHETIC_INTEGRATION_ASSURANCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.12.0.md",
            "V0_12_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_12_RELEASE_GATE.md",
            "V0_12_RELEASE_CONTROL_CANDIDATE.json",
            "V0_12_RELEASE_EVIDENCE.md",
            "RELEASE_NOTES_v0.12.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE_ROOT / name).is_file(), name)

        combined = "\n".join((RELEASE_ROOT / name).read_text(encoding="utf-8").lower() for name in required)
        for required_phrase in (
            "no-new-interface",
            "synthetic",
            "does not",
            "c4",
            "not a hosted release",
        ):
            self.assertIn(required_phrase, combined)
        self.assertNotIn("v0.12.0 is published", combined)
        self.assertNotIn("v0.12.0 is installed", combined)

    def test_v012_release_control_is_valid_and_exact_identity_is_unresolved(self) -> None:
        schema = json.loads((RELEASE_ROOT / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE_ROOT / "V0_12_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_reviewed")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertEqual(record["capability_set"]["candidate_outcome"], "verified_candidate_or_explicitly_excluded_only")
        self.assertEqual(record["capability_set"]["admitted_capability_ids"], [])
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])

    def test_v012_history_remains_distinct_from_later_v013_admission(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        self.assertEqual(ledger["release_context"]["source_release_version"], "v1.0.0")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.13.0")
        self.assertFalse(any(item["capability_id"].startswith("GRW-CAP-120-") for item in ledger["capabilities"]))
        self.assertFalse(any(item["version"]["target_release"] == "v0.12.0" for item in ledger["capabilities"]))
        self.assertTrue(any(item["capability_id"] == "GRW-CAP-130-01" for item in ledger["capabilities"]))

    def test_v012_public_preparation_surface_has_no_local_or_project_marker(self) -> None:
        paths = (
            ROOT / "assets" / "integration-assurance" / "v0_12_synthetic_integration_scenario.md",
            ROOT / "references" / "v0-12-synthetic-integration-assurance.md",
            ROOT / "system" / "10_assurance_evaluation_and_audit" / "V0_12_SYNTHETIC_INTEGRATION_ASSURANCE.md",
            *(RELEASE_ROOT / name for name in (
                "V0_12_SYNTHETIC_INTEGRATION_ASSURANCE.md",
                "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.12.0.md",
                "V0_12_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
                "V0_12_RELEASE_GATE.md",
                "V0_12_RELEASE_EVIDENCE.md",
                "RELEASE_NOTES_v0.12.0.md",
            )),
        )
        for path in paths:
            content = path.read_text(encoding="utf-8")
            for marker in FORBIDDEN_MARKERS:
                self.assertNotIn(marker, content, f"{path} contains {marker!r}")


if __name__ == "__main__":
    unittest.main()
