"""Regression checks for v0.8 candidate release-preparation material."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"
RECORD_PATH = RELEASE_ROOT / "V0_8_RELEASE_CONTROL_CANDIDATE.json"
SCHEMA_PATH = RELEASE_ROOT / "release_control_record.schema.json"


class V08ReleasePreparationTests(unittest.TestCase):
    def test_required_candidate_materials_exist_and_remain_pre_c4(self) -> None:
        required = (
            "V0_8_RELEASE_GATE.md",
            "V0_8_CAPABILITY_ADMISSION.md",
            "V0_8_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.8.0.md",
            "V0_8_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_8_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.8.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE_ROOT / name).is_file(), f"Missing v0.8 release-preparation material: {name}")

        gate = (RELEASE_ROOT / "V0_8_RELEASE_GATE.md").read_text(encoding="utf-8")
        admission = (RELEASE_ROOT / "V0_8_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8")
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.8.0.md").read_text(encoding="utf-8")
        self.assertIn("does not admit a capability", gate)
        self.assertIn("scope acceptance recorded", admission)
        self.assertIn("Exact\nrelease-scope admission remains pending", admission)
        self.assertIn("does not itself establish publication", notes)

    def test_candidate_record_validates_and_cannot_stand_in_for_c4(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

        self.assertEqual(record["status"], "candidate_evidence_incomplete")
        self.assertEqual(record["candidate_identity"]["branch_state"], "remote_candidate_branch")
        self.assertEqual(record["capability_set"]["admitted_capability_ids"], [])
        self.assertIsNone(record["candidate_review_acceptance_reference"])
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])
        self.assertEqual(record["release_integrity_posture"]["technical_immutable_release_status"], "unknown")

    def test_public_documents_link_to_preparation_without_claiming_release(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        security = (REPOSITORY_ROOT / "SECURITY.md").read_text(encoding="utf-8")
        module = (RELEASE_ROOT / "MODULE.md").read_text(encoding="utf-8")

        self.assertIn("V0_8_RELEASE_GATE.md", readme)
        self.assertIn("candidate release gate", roadmap)
        self.assertIn("`v0.8.x`", security)
        self.assertIn("active v0.8 candidate release-preparation", module)
        self.assertNotIn("v0.8.0 is the current release", (readme + roadmap + module).lower())


if __name__ == "__main__":
    unittest.main()
