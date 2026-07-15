"""Regression checks for release-control and maintenance-candidate records."""

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"


class ReleaseControlTests(unittest.TestCase):
    def test_required_release_and_maintenance_records_exist(self) -> None:
        required_records = (
            "V0_3_RELEASE_GATE.md",
            "INSTALL_UPDATE_ROLLBACK.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.0.md",
            "RELEASE_INTEGRITY_POLICY_v1.md",
            "RELEASE_NOTES_v0.3.0.md",
            "V0_3_RELEASE_EVIDENCE.md",
            "V0_3_1_COMPATIBILITY_MAINTENANCE_CANDIDATE.md",
        )
        for record in required_records:
            self.assertTrue((RELEASE_ROOT / record).is_file(), f"Missing release record: {record}")

    def test_maintenance_candidate_names_its_own_exact_framework_target(self) -> None:
        manifest = (REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "test-bootstrap.yml").read_text(encoding="utf-8")
        self.assertIn("system_version: 0.3.1", manifest)
        self.assertIn('supported_framework_versions: "0.1.0"', manifest)
        self.assertIn("unreleased `v0.3.1` compatibility-maintenance candidate", readme)
        self.assertIn("v0.3.1 (unreleased compatibility-maintenance candidate)", roadmap)
        self.assertIn("ref: v0.1.1", workflow)
        self.assertIn("FRAMEWORK_RELEASE_TAG: v0.1.1", workflow)
        self.assertNotIn("The unreleased `v0.3.0-system-foundation` candidate", readme)
        self.assertNotIn("unreleased Workspace Framework candidate", manifest)

    def test_release_gate_preserves_human_and_post_release_stops(self) -> None:
        gate = (RELEASE_ROOT / "V0_3_RELEASE_GATE.md").read_text(encoding="utf-8")
        evidence = (RELEASE_ROOT / "V0_3_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn("R30-G6", gate)
        self.assertIn("R30-G7", gate)
        self.assertIn("Status: pending.", evidence)
        self.assertIn("not applicable until a real release exists", evidence)


if __name__ == "__main__":
    unittest.main()
