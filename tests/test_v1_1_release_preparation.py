"""Release-preparation controls for the v1.1 future-Study candidate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"


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
