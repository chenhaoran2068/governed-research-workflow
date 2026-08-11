"""Release-preparation controls for the v0.13 V1 support-scope matrix."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"


class V013ReleasePreparationTests(unittest.TestCase):
    def test_v013_records_are_complete_and_explicitly_pre_c3_remote(self) -> None:
        required = (
            "V0_13_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.13.0.md",
            "V0_13_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_13_RELEASE_GATE.md",
            "V0_13_RELEASE_CONTROL_CANDIDATE.json",
            "V0_13_RELEASE_EVIDENCE.md",
            "RELEASE_NOTES_v0.13.0.md",
        )
        contents = []
        for name in required:
            path = RELEASE_ROOT / name
            self.assertTrue(path.is_file(), name)
            contents.append(path.read_text(encoding="utf-8"))

        combined = "\n".join(contents).lower()
        self.assertIn("local pre-c3-remote", combined)
        self.assertIn("not c3-remote evidence", combined)
        self.assertIn("c4 authorization", combined)
        self.assertIn("does not prove exact candidate identity", combined)
        self.assertNotIn("v0.13.0 is published", combined)
        self.assertNotIn("v0.13.0 is installed", combined)

    def test_v013_release_control_is_valid_and_exact_identity_is_unresolved(self) -> None:
        schema = json.loads((RELEASE_ROOT / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE_ROOT / "V0_13_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["candidate_version"], "0.13.0")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertEqual(record["capability_set"]["verified_candidate_capability_ids"], ["GRW-CAP-130-01"])
        self.assertEqual(record["capability_set"]["admitted_capability_ids"], [])
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])

    def test_v013_admission_preserves_the_structural_and_operational_boundaries(self) -> None:
        admission = (RELEASE_ROOT / "V0_13_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8").lower()
        dependency = (RELEASE_ROOT / "V0_13_DEPENDENCY_AND_WORKFLOW_REVIEW.md").read_text(encoding="utf-8").lower()
        rights = (RELEASE_ROOT / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.13.0.md").read_text(encoding="utf-8").lower()

        self.assertIn("grw-cap-130-01", admission)
        self.assertIn("does not add data access", admission)
        self.assertIn("agent runtime", admission)
        self.assertIn("| new dependency, lockfile, or package | none |", dependency)
        self.assertIn("| new operational schema, validator, helper, or agent runtime | none |", dependency)
        self.assertIn("no new third-party source", rights)
        self.assertIn("apache-2.0", rights)

    def test_v013_current_source_and_historical_v012_baseline_are_separate(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.13.0.md").read_text(encoding="utf-8")

        self.assertIn("system_version: 1.13.0", manifest)
        self.assertEqual(ledger["release_context"]["source_release_version"], "v1.0.0")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.13.0")
        self.assertTrue(any(record["capability_id"] == "GRW-CAP-130-01" for record in ledger["capabilities"]))
        self.assertIn("Existing bootstrap behavior", notes)
        self.assertIn("unchanged", notes)


if __name__ == "__main__":
    unittest.main()
