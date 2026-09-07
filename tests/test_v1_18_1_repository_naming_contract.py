import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"


class V1181RepositoryNamingContractTests(unittest.TestCase):
    def test_current_source_and_patch_records_are_present(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        ledger = json.loads(
            (ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json").read_text(encoding="utf-8")
        )
        self.assertIn("system_version: 1.18.1", manifest)
        self.assertEqual(ledger["release_context"]["source_release_version"], "v1.18.1")
        for name in (
            "RELEASE_NOTES_v1.18.1.md",
            "V1_18_1_RELEASE_CONTROL_CANDIDATE.json",
            "V1_18_1_RELEASE_GATE.md",
            "V1_18_1_RELEASE_EVIDENCE.md",
            "V1_18_1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.18.1.md",
        ):
            self.assertTrue((RELEASE / name).is_file(), name)

    def test_standard_separates_name_identity_and_worktree_promotion(self) -> None:
        standard = (ROOT / "references" / "paper-repository-standard.md").read_text(encoding="utf-8")
        readme = (ROOT / "assets" / "paper-repository" / "paper-repository-README.template.md").read_text(encoding="utf-8")
        self.assertIn("`<subject-or-domain>-<core-focus>-<output-type>`", standard)
        self.assertIn("rather than forcing every\noutput into PICOS", standard)
        self.assertIn("`Github/<repository-name>/`", standard)
        self.assertIn("Do not copy the complete\nStudy", standard)
        self.assertIn("Research Identity And Repository Name", readme)

    def test_manifest_template_records_naming_decision(self) -> None:
        template = json.loads(
            (ROOT / "assets" / "paper-repository" / "paper-repository-release-manifest.template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(template["schema_version"], "0.1.1")
        naming = template["repository"]["naming"]
        self.assertEqual(naming["strategy"], "subject-focus-output-type")
        self.assertFalse(naming["human_confirmed"])


if __name__ == "__main__":
    unittest.main()
