"""Release-preparation controls for the versioned v1.1 future-Study source."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
ASSURANCE = ROOT / "system" / "10_assurance_evaluation_and_audit" / "V1_1_FUTURE_STUDY_EXECUTION_EVIDENCE.md"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V11ReleasePreparationTests(unittest.TestCase):
    def test_candidate_release_materials_are_present_and_preserve_release_identity_boundary(self) -> None:
        required = (
            "V1_1_CAPABILITY_ADMISSION.md",
            "V1_1_RELEASE_GATE.md",
            "V1_1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.1.0.md",
            "V1_1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V1_1_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v1.1.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE / name).is_file(), name)

        combined = "\n".join((RELEASE / name).read_text(encoding="utf-8").lower() for name in required)
        for marker in (
            "an exact commit",
            "github release",
            "does not state a current",
            "not asserted by this source record",
        ):
            self.assertIn(marker, combined)
        self.assertIn("admitted for the proposed", combined)
        self.assertNotIn("v1.1.0 is released", combined)
        self.assertNotIn("v1.1.0 is installed", combined)
        self.assertNotIn("not authorized and not established", combined)
        self.assertNotRegex(combined, r"\b\d+\s+(?:tests?\s+)?passed\b")
        self.assertNotRegex(combined, r"\b\d+\s+candidate files\b")

    def test_current_v11_source_surfaces_are_time_neutral(self) -> None:
        current_paths = (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            ROOT / "references" / "future-study-execution-and-reproducibility.md",
            ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json",
            ROOT / "system" / "00_manifest_and_profiles" / "v1_1_public_interface_manifest.json",
            ROOT / "system" / "00_manifest_and_profiles" / "v1_1_support_scope_matrix.json",
            RELEASE / "RELEASE_NOTES_v1.1.0.md",
        )
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_paths)
        self.assertIn("exact annotated", combined)
        self.assertIn("matching github release", combined)
        self.assertNotIn("unreleased v1.1.0", combined)
        self.assertNotIn("unpublished local candidate", combined)
        self.assertNotIn("unreleased_candidate", combined)
        self.assertNotIn("later github release", combined)

    def test_candidate_assurance_evidence_is_time_neutral_and_ledger_does_not_embed_run_counts(self) -> None:
        assurance = ASSURANCE.read_text(encoding="utf-8")
        self.assertIn("commit-neutral candidate source snapshot", assurance)
        self.assertIn("does not state a\ncurrent exact candidate commit", assurance)
        self.assertNotRegex(assurance, r"\b\d+\s+(?:tests?\s+)?passed\b")
        self.assertNotIn("remote CI, release preparation, C4, hosted Release", assurance)

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-111-01")
        source_snapshot = next(
            item for item in record["evidence"]["references"]
            if item["path"] == "system/10_assurance_evaluation_and_audit/V1_1_FUTURE_STUDY_EXECUTION_EVIDENCE.md"
        )
        self.assertEqual(source_snapshot["kind"], "run_record")
        self.assertEqual(source_snapshot["identifier"], "v1-1-candidate-evidence-source-snapshot")
        self.assertNotRegex(source_snapshot["identifier"], r"\b\d+-(?:pass|passed)\b")

    def test_release_control_is_valid_and_keeps_exact_identity_and_c4_unresolved(self) -> None:
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE / "V1_1_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_reviewed")
        self.assertEqual(record["record_revision"], 3)
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "remote_candidate_branch")
        self.assertEqual(record["capability_set"]["verified_candidate_capability_ids"], ["GRW-CAP-111-01"])
        self.assertEqual(record["capability_set"]["admitted_capability_ids"], ["GRW-CAP-111-01"])
        self.assertEqual(record["material_reviews"]["public_material_rights_review"], "pass")
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])


if __name__ == "__main__":
    unittest.main()
