"""Regression checks for current release guidance and historical records."""

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
            "V0_3_1_RELEASE_GATE.md",
            "V0_3_1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.1.md",
            "RELEASE_NOTES_v0.3.1.md",
            "V0_3_2_RELEASE_STATE_CORRECTION_CANDIDATE.md",
            "CURRENT_RELEASE_STATUS.md",
            "RELEASE_CONTROL.md",
            "release_control_record.schema.json",
        )
        for record in required_records:
            self.assertTrue((RELEASE_ROOT / record).is_file(), f"Missing release record: {record}")

    def test_current_candidate_and_published_baseline_are_distinct(self) -> None:
        manifest = (REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        current_status = (RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8")
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "test-bootstrap.yml").read_text(encoding="utf-8")

        self.assertIn("system_version: 0.4.0-candidate", manifest)
        self.assertIn('supported_framework_versions: "0.1.0"', manifest)
        self.assertIn("denotes the framework contract version", manifest)
        self.assertIn("local governance-and-records candidate version `0.4.0`", readme)
        self.assertIn("locally\nrecorded current public baseline is `v0.3.1`", readme)
        self.assertIn("## v0.4.0 (local governance-and-records candidate)", roadmap)
        self.assertIn("## v0.3.1 (released 2026-07-16)", roadmap)
        self.assertIn("## v0.3.2 (historical local release-state correction candidate)", roadmap)
        self.assertIn("Current public release: `v0.3.1`", current_status)
        self.assertIn("0a16e534fb11bc5254bcdd5c2780e09f46cf81d0", current_status)
        self.assertIn("Current local candidate: `v0.4.0`", current_status)
        self.assertIn("ref: b0e32d7710b70299e633df1316b6924cd87b647b", workflow)
        self.assertIn("FRAMEWORK_RELEASE_TAG: v0.1.1", workflow)
        self.assertIn("FRAMEWORK_EXPECTED_COMMIT: b0e32d7710b70299e633df1316b6924cd87b647b", workflow)
        self.assertNotIn("release-gated source version `0.3.1`", readme)
        self.assertNotIn("v0.3.1 (release-gated compatibility-maintenance source)", roadmap)
        self.assertNotIn("unreleased Workspace Framework candidate", manifest)

    def test_historical_v031_records_are_labeled_without_erasing_history(self) -> None:
        candidate = (RELEASE_ROOT / "V0_3_1_COMPATIBILITY_MAINTENANCE_CANDIDATE.md").read_text(encoding="utf-8")
        gate = (RELEASE_ROOT / "V0_3_1_RELEASE_GATE.md").read_text(encoding="utf-8")
        evidence = (RELEASE_ROOT / "V0_3_1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")
        rights = (RELEASE_ROOT / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.1.md").read_text(encoding="utf-8")
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.3.1.md").read_text(encoding="utf-8")

        self.assertIn("Status: historical pre-release candidate snapshot.", candidate)
        self.assertIn("Status: historical pre-release gate.", gate)
        self.assertIn("Status: historical pre-release evidence snapshot.", evidence)
        self.assertIn("Status: historical pre-release review snapshot", rights)
        self.assertIn("Status: historical release-note source", notes)
        self.assertIn("published\n`v0.3.1`", candidate)
        self.assertIn("published `v0.3.1`", gate)
        self.assertIn("published\n`v0.3.1`", evidence)
        self.assertIn("v0.1.1", candidate)
        self.assertIn("R31-G6", gate)
        self.assertIn("R31-G7", gate)

    def test_historical_v030_gate_retains_human_and_post_release_stops(self) -> None:
        gate = (RELEASE_ROOT / "V0_3_RELEASE_GATE.md").read_text(encoding="utf-8")
        evidence = (RELEASE_ROOT / "V0_3_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")

        self.assertIn("Status: historical pre-release gate.", gate)
        self.assertIn("Status: historical pre-release evidence snapshot.", evidence)
        self.assertIn("R30-G6", gate)
        self.assertIn("R30-G7", gate)
        self.assertIn("Status: pending.", evidence)
        self.assertIn("not applicable until a real release exists", evidence)

    def test_current_policy_and_candidate_separate_current_and_historical_states(self) -> None:
        security = (REPOSITORY_ROOT / "SECURITY.md").read_text(encoding="utf-8")
        start_here = (REPOSITORY_ROOT / "assets" / "START_HERE.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        integrity = (RELEASE_ROOT / "RELEASE_INTEGRITY_POLICY_v1.md").read_text(encoding="utf-8")
        candidate = (RELEASE_ROOT / "V0_3_2_RELEASE_STATE_CORRECTION_CANDIDATE.md").read_text(encoding="utf-8")

        self.assertIn("`v0.3.x`", security)
        self.assertIn("released bounded system\nfoundation introduced in `v0.3.0`", start_here)
        self.assertIn("`REL-008` was completed by the released `v0.3.0`", roadmap)
        self.assertNotIn("| REL-008 |", roadmap)
        self.assertIn("Historical v0.3.0\nframework-integration evidence", integrity)
        self.assertIn("published v0.3.1 patch", integrity)
        self.assertIn("Recorded v0.3.1 decision", integrity)
        self.assertIn("Status: historical local maintenance candidate", candidate)
        self.assertIn("locally recorded current published patch\nbaseline remains `v0.3.1`", candidate)

    def test_v040_release_control_route_preserves_c4_and_post_release_stops(self) -> None:
        control = (RELEASE_ROOT / "RELEASE_CONTROL.md").read_text(encoding="utf-8")
        self.assertIn("Candidate-review acceptance is not C4 authorization", control)
        self.assertIn("C4 authorization is not\npost-release verification", control)
        self.assertIn("Before C4, retain `c4_release_authorization_reference` as `null`", control)


if __name__ == "__main__":
    unittest.main()
