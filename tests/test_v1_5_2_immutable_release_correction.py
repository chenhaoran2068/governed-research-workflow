"""Contract checks for the v1.5.2 immutable-release correction scope."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "system" / "11_distribution_installation_and_release"
HISTORICAL_FRAMEWORK_TAG = "v0.2.0"
HISTORICAL_FRAMEWORK_COMMIT = "69c76f84a5b0913b26c17ea48f152dbc50b4bec6"
CURRENT_FRAMEWORK_TAG = "v0.4.0"
CURRENT_FRAMEWORK_COMMIT = "30ba0f4032a90723612b6d213bd54faa7cce5aee"


class V152ImmutableReleaseCorrectionTests(unittest.TestCase):
    def test_manifest_and_ci_retain_only_the_exact_framework_identity(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "test-bootstrap.yml").read_text(encoding="utf-8")

        self.assertIn("system_version: 1.18.1", manifest)
        self.assertIn('supported_framework_versions: "0.4.0"', manifest)
        self.assertNotIn('supported_framework_versions: "0.1.0"', manifest)
        self.assertIn(f"FRAMEWORK_RELEASE_TAG: {CURRENT_FRAMEWORK_TAG}", workflow)
        self.assertIn(f"FRAMEWORK_EXPECTED_COMMIT: {CURRENT_FRAMEWORK_COMMIT}", workflow)
        self.assertIn(f"ref: {CURRENT_FRAMEWORK_COMMIT}", workflow)

    def test_public_materials_preserve_the_compatibility_only_boundary(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        integration_plan = (ROOT / "system" / "00_manifest_and_profiles" / "FRAMEWORK_INTEGRATION_PLAN.md").read_text(encoding="utf-8")
        current_material = "\n".join(
            (
                readme.split("## Capability Truth", maxsplit=1)[0],
                roadmap.split("## v1.5.0", maxsplit=1)[0],
                integration_plan.split("## Historical Validation Evidence", maxsplit=1)[0],
            )
        ).lower()

        self.assertIn("## v1.5.2", roadmap)
        self.assertIn(CURRENT_FRAMEWORK_COMMIT, current_material)
        self.assertIn("does not create a `papers/` root", current_material)
        self.assertIn("no new capability", current_material)
        self.assertIn("this roadmap does not state that v1.5.2 is released", current_material)
        self.assertIn("does not itself prove the release\nor installation identity", current_material)

    def test_pre_c4_release_records_are_complete_and_require_draft_first(self) -> None:
        required = (
            "RELEASE_NOTES_v1.5.2.md",
            "V1_5_2_RELEASE_GATE.md",
            "V1_5_2_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.5.2.md",
            "V1_5_2_RELEASE_CONTROL_CANDIDATE.json",
        )
        for name in required:
            self.assertTrue((RELEASE_ROOT / name).is_file(), name)

        gate = (RELEASE_ROOT / "V1_5_2_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        self.assertIn("annotated tag", gate)
        self.assertIn("draft github release", gate)
        self.assertIn("separate accountable-human c4-publish approval", gate)

        schema = json.loads((RELEASE_ROOT / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE_ROOT / "V1_5_2_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["candidate_version"], "1.5.2")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertEqual(record["dependency_and_source_authority"]["framework_tag"], HISTORICAL_FRAMEWORK_TAG)
        self.assertEqual(record["dependency_and_source_authority"]["framework_commit"], HISTORICAL_FRAMEWORK_COMMIT)
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])


if __name__ == "__main__":
    unittest.main()
