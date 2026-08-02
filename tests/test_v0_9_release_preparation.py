"""Release-preparation controls for the v0.9 integrity-audit source."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "system" / "11_distribution_installation_and_release"


class V09ReleasePreparationTests(unittest.TestCase):
    def test_v09_history_is_retained_while_current_source_moves_forward(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        index = (ROOT / "system" / "INDEX.md").read_text(encoding="utf-8")

        self.assertIn("system_version: 1.5.2", manifest)
        self.assertIn("Status: v1.1.0 versioned source scope", readme)
        self.assertIn("does not itself prove the\nrelease or installation identity", readme)
        self.assertIn("## v0.9.0 (integrity-audit source)", roadmap)
        self.assertIn("Status: v1.5.2 compatibility-maintenance source retaining the frozen public-", index)
        combined = "\n".join((manifest, readme, roadmap, index)).lower()
        self.assertNotIn("v0.9.0 is published", combined)
        self.assertNotIn("v0.9.0 is installed", combined)

    def test_admitted_scope_and_release_materials_are_complete_but_pre_c4(self) -> None:
        required = (
            "V0_9_CAPABILITY_ADMISSION.md",
            "V0_9_RELEASE_GATE.md",
            "V0_9_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.9.0.md",
            "V0_9_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_9_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.9.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE_ROOT / name).is_file(), name)

        combined = "\n".join(
            (RELEASE_ROOT / name).read_text(encoding="utf-8").lower() for name in required
        )
        self.assertIn("grw-cap-090-01", combined)
        self.assertIn("grw-cap-090-02", combined)
        self.assertIn("grw-cap-090-03", combined)
        self.assertIn("does not authorize", combined)
        self.assertNotIn("v0.9.0 is published", combined)
        self.assertNotIn("v0.9.0 is installed", combined)

    def test_release_control_record_is_valid_and_keeps_exact_identity_unresolved(self) -> None:
        schema = json.loads((RELEASE_ROOT / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE_ROOT / "V0_9_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_reviewed")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])


if __name__ == "__main__":
    unittest.main()
