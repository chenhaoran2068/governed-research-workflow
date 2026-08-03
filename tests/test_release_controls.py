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
            "RELEASE_NOTES_v0.5.1.md",
            "V0_5_1_RELEASE_STATE_MAINTENANCE.md",
            "V0_6_RELEASE_GATE.md",
            "V0_6_RELEASE_EVIDENCE.md",
            "V0_6_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.6.0.md",
            "RELEASE_NOTES_v0.6.0.md",
            "V0_6_1_RELEASE_STATE_MAINTENANCE.md",
            "RELEASE_NOTES_v0.6.1.md",
            "V0_7_CAPABILITY_ADMISSION.md",
            "V0_7_RELEASE_GATE.md",
            "V0_7_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.7.0.md",
            "RELEASE_NOTES_v0.7.0.md",
            "V0_7_1_RELEASE_STATE_MAINTENANCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.7.1.md",
            "RELEASE_NOTES_v0.7.1.md",
            "V0_8_RELEASE_GATE.md",
            "V0_8_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.8.0.md",
            "V0_8_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_8_CAPABILITY_ADMISSION.md",
            "V0_8_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.8.0.md",
            "V0_9_CAPABILITY_ADMISSION.md",
            "V0_9_RELEASE_GATE.md",
            "V0_9_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.9.0.md",
            "V0_9_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_9_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.9.0.md",
            "V0_10_CAPABILITY_ADMISSION.md",
            "V0_10_RELEASE_GATE.md",
            "V0_10_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.0.md",
            "V0_10_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_10_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.10.0.md",
            "V0_10_1_CAPABILITY_ADMISSION.md",
            "V0_10_1_RELEASE_GATE.md",
            "V0_10_1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.1.md",
            "V0_10_1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_10_1_RELEASE_CONTROL_CANDIDATE.json",
            "RELEASE_NOTES_v0.10.1.md",
            "V0_10_2_HUMAN_MEDIATED_EXPERIENCE_CURATION_MAINTENANCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.2.md",
            "V0_10_2_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_10_2_RELEASE_EVIDENCE.md",
            "RELEASE_NOTES_v0.10.2.md",
            "V0_11_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.11.0.md",
            "V0_11_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_11_RELEASE_CONTROL_CANDIDATE.json",
            "V0_11_RELEASE_EVIDENCE.md",
            "V0_11_RELEASE_GATE.md",
            "RELEASE_NOTES_v0.11.0.md",
            "V0_12_SYNTHETIC_INTEGRATION_ASSURANCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.12.0.md",
            "V0_12_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_12_RELEASE_GATE.md",
            "V0_12_RELEASE_CONTROL_CANDIDATE.json",
            "V0_12_RELEASE_EVIDENCE.md",
            "RELEASE_NOTES_v0.12.0.md",
            "V0_13_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.13.0.md",
            "V0_13_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V0_13_RELEASE_GATE.md",
            "V0_13_RELEASE_CONTROL_CANDIDATE.json",
            "V0_13_RELEASE_EVIDENCE.md",
            "RELEASE_NOTES_v0.13.0.md",
            "V1_RELEASE_GATE.md",
            "V1_RELEASE_CONTROL_CANDIDATE.json",
            "V1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.0.0.md",
            "V1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "RELEASE_NOTES_v1.0.0.md",
            "RELEASE_NOTES_v1.5.2.md",
            "V1_5_2_RELEASE_GATE.md",
            "V1_5_2_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.5.2.md",
            "V1_5_2_RELEASE_CONTROL_CANDIDATE.json",
        )
        for record in required_records:
            self.assertTrue((RELEASE_ROOT / record).is_file(), f"Missing release record: {record}")

    def test_v050_historical_pre_c4_materials_preserve_boundaries(self) -> None:
        expected = {
            "V0_5_RELEASE_GATE.md": "historical pre-c3 candidate gate",
            "V0_5_RELEASE_EVIDENCE.md": "historical pre-c3 preparation evidence only",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.5.0.md": "historical pre-c3 preparation record",
            "V0_5_CAPABILITY_ADMISSION.md": "historical pre-c4 admission record",
            "RELEASE_NOTES_v0.5.0.md": "historical pre-c4 draft snapshot",
        }
        for name, boundary in expected.items():
            content = (RELEASE_ROOT / name).read_text(encoding="utf-8").lower()
            self.assertIn(boundary, content)
        current_status = (RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("Published v0.5.0 Baseline", current_status)

    def test_release_source_and_live_release_verification_are_distinct(self) -> None:
        manifest = (REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        current_status = (RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8")
        integrity_policy = (RELEASE_ROOT / "RELEASE_INTEGRITY_POLICY_v1.md").read_text(encoding="utf-8")
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "test-bootstrap.yml").read_text(encoding="utf-8")

        self.assertIn("system_version: 1.6.0", manifest)
        self.assertIn("jsonschema==4.26.0", manifest)
        self.assertIn('supported_framework_versions: "0.2.0"', manifest)
        self.assertIn("exact Framework v0.2.0 contract", manifest)
        self.assertIn("Status: v1.1.0 versioned source scope", readme)
        self.assertIn("does not itself prove the\nrelease or installation identity", readme)
        self.assertIn("## v0.5.1 (published release-state maintenance)", roadmap)
        self.assertIn("## v0.7.1 (release-state and control-hardening maintenance source)", roadmap)
        self.assertIn("## v0.7.0 (historical human-reviewed lesson-promotion release source)", roadmap)
        self.assertIn("## v0.5.0 (published metadata-only provenance register set)", roadmap)
        self.assertIn("## v0.4.0 (published governance-and-records baseline)", roadmap)
        self.assertIn("## v0.3.1 (released 2026-07-16)", roadmap)
        self.assertIn("## v0.3.2 (historical local release-state correction candidate)", roadmap)
        self.assertIn("Published v0.5.0 Baseline", current_status)
        self.assertIn("matching GitHub Release", current_status)
        self.assertIn("GitHub technical immutable releases are enabled", integrity_policy)
        self.assertIn("ref: 69c76f84a5b0913b26c17ea48f152dbc50b4bec6", workflow)
        self.assertIn("FRAMEWORK_RELEASE_TAG: v0.2.0", workflow)
        self.assertIn("FRAMEWORK_EXPECTED_COMMIT: 69c76f84a5b0913b26c17ea48f152dbc50b4bec6", workflow)
        self.assertNotIn("unreleased governance-and-records candidate version", readme)
        self.assertNotIn("current public baseline is `v0.3.1`", readme)
        self.assertNotIn("v0.3.1 (release-gated compatibility-maintenance source)", roadmap)
        self.assertNotIn("unreleased Workspace Framework candidate", manifest)

    def test_current_source_guidance_cannot_name_a_live_public_version(self) -> None:
        current_paths = (
            REPOSITORY_ROOT / "README.md",
            REPOSITORY_ROOT / "ROADMAP.md",
            REPOSITORY_ROOT / "SKILL.md",
            REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml",
            REPOSITORY_ROOT / "system" / "INDEX.md",
            RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md",
            RELEASE_ROOT / "RELEASE_CONTROL.md",
            RELEASE_ROOT / "MODULE.md",
            RELEASE_ROOT / "V0_6_1_RELEASE_STATE_MAINTENANCE.md",
            RELEASE_ROOT / "RELEASE_NOTES_v0.6.1.md",
            RELEASE_ROOT / "RELEASE_NOTES_v0.10.1.md",
            RELEASE_ROOT / "RELEASE_NOTES_v0.10.2.md",
        )
        current_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_paths)
        for prohibited in (
            "current published patch is",
            "current published version is",
            "current public baseline is",
            "current stable release is",
            "current release is",
            "currently published version is",
            "latest published tag is",
            "latest published version is",
            "latest release is",
        ):
            self.assertNotIn(prohibited, current_text)
        self.assertIn("does not declare a current published version", (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8"))
        control = (RELEASE_ROOT / "RELEASE_CONTROL.md").read_text(encoding="utf-8")
        self.assertIn("Current-State Assertion Control", control)
        self.assertIn("release-blocking documentation defect", control)
        self.assertIn("Candidate Snapshot Completeness", control)
        self.assertIn("git ls-files", control)

    def test_v101_candidate_records_are_time_neutral_and_boundary_limited(self) -> None:
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.10.1.md").read_text(encoding="utf-8").lower()
        gate = (RELEASE_ROOT / "V0_10_1_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        control = (RELEASE_ROOT / "V0_10_1_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8").lower()
        evidence = (RELEASE_ROOT / "V0_10_1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        status = (RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8").lower()
        self.assertIn("public-installation rule always requires", notes)
        self.assertNotIn("still required before", notes)
        self.assertIn("no public intake", gate)
        self.assertIn("all-zero exact_commit sentinel", control)
        self.assertIn("pre-c3-remote preparation evidence", evidence)
        self.assertIn("v0.10.1 synthetic exchange-pilot source scope", status)

    def test_v102_maintenance_records_do_not_invent_a_capability_or_intake_service(self) -> None:
        contract = (RELEASE_ROOT / "V0_10_2_HUMAN_MEDIATED_EXPERIENCE_CURATION_MAINTENANCE.md").read_text(encoding="utf-8").lower()
        rights = (RELEASE_ROOT / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.2.md").read_text(encoding="utf-8").lower()
        dependency = (RELEASE_ROOT / "V0_10_2_DEPENDENCY_AND_WORKFLOW_REVIEW.md").read_text(encoding="utf-8").lower()
        evidence = (RELEASE_ROOT / "V0_10_2_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.10.2.md").read_text(encoding="utf-8").lower()
        status = (RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8").lower()
        module = (RELEASE_ROOT / "MODULE.md").read_text(encoding="utf-8").lower()

        self.assertIn("zero-new-capability maintenance source", contract)
        self.assertIn("not used to invent a zero-capability admission", contract)
        self.assertIn("no contributor submission", rights)
        self.assertIn("new dependency or lockfile | none", dependency)
        self.assertIn("new admitted capability identifiers | none", evidence)
        self.assertIn("does not add external contributor support", notes)
        self.assertIn("does not create a user-facing intake", status)
        self.assertIn("bounded\nlocal pre-c3-remote maintenance-preparation records", module)
        for text in (contract, rights, dependency, evidence, notes):
            self.assertNotIn("hosted-release claim", text)

    def test_v011_release_preparation_records_preserve_scope_and_pending_gates(self) -> None:
        admission = (RELEASE_ROOT / "V0_11_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8").lower()
        rights = (RELEASE_ROOT / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.11.0.md").read_text(encoding="utf-8").lower()
        dependency = (RELEASE_ROOT / "V0_11_DEPENDENCY_AND_WORKFLOW_REVIEW.md").read_text(encoding="utf-8").lower()
        gate = (RELEASE_ROOT / "V0_11_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        evidence = (RELEASE_ROOT / "V0_11_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        notes = (RELEASE_ROOT / "RELEASE_NOTES_v0.11.0.md").read_text(encoding="utf-8").lower()
        control = (RELEASE_ROOT / "V0_11_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8").lower()

        self.assertIn("grw-cap-110-01", admission)
        self.assertIn("grw-cap-110-06", admission)
        self.assertIn("private project, source, or person identifier", admission)
        self.assertIn("accountable-human public-rights confirmation", gate)
        self.assertIn("remote ci pending", gate)
        self.assertIn("jsonschema==4.26.0", dependency)
        self.assertIn("backward-compatible ledger identifier-pattern extension", dependency)
        self.assertIn("dbbaea0a4aa335265c6e199971e6134892ba52d9", rights)
        self.assertIn("227 tests passed", evidence)
        self.assertIn("exact c3-remote candidate", evidence)
        self.assertIn("no exact c3-remote candidate has been authorized", control)
        self.assertIn("all-zero exact_commit sentinel", control)
        self.assertIn("no new schema artifact, validator, dependency, helper", notes)
        for text in (admission, rights, dependency, gate, evidence, control):
            self.assertIn("historical local pre-c3-remote snapshot", text)
        for text in (admission, rights, dependency, gate, evidence, notes, control):
            self.assertNotIn("v0.11.0 is released", text)

    def test_current_records_cannot_describe_the_published_v050_baseline_as_unreleased(self) -> None:
        current_paths = (
            REPOSITORY_ROOT / "README.md",
            REPOSITORY_ROOT / "ROADMAP.md",
            REPOSITORY_ROOT / "SECURITY.md",
            REPOSITORY_ROOT / "SKILL.md",
            REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml",
            REPOSITORY_ROOT / "system" / "INDEX.md",
            REPOSITORY_ROOT / "system" / "05_data_and_provenance" / "MODULE.md",
            REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json",
            RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md",
            RELEASE_ROOT / "MODULE.md",
            RELEASE_ROOT / "RELEASE_INTEGRITY_POLICY_v1.md",
        )
        current_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_paths)
        self.assertIn("published v0.5.0", current_text)
        self.assertIn("exact annotated tag", current_text)
        self.assertNotIn("no tag or github release exists", current_text)
        self.assertNotIn("v0.5.0 is release-source content, not a hosted release", current_text)

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
        self.assertIn("`v0.4.x`", security)
        self.assertIn("`v0.5.x`", security)
        self.assertIn("`v0.6.x`", security)
        self.assertIn("`v0.7.x`", security)
        self.assertIn("`v0.8.x`", security)
        self.assertIn("`v0.9.x`", security)
        self.assertIn("`v0.10.x`", security)
        self.assertIn("released bounded system baseline\nthrough `v0.4.0`", start_here)
        self.assertIn("`REL-008` was completed by the released `v0.3.0`", roadmap)
        self.assertNotIn("| REL-008 |", roadmap)
        self.assertIn("Historical v0.3.0 framework-integration evidence", integrity)
        self.assertIn("The published v0.3.1", integrity)
        self.assertIn("Historical v0.3.1 decision", integrity)
        self.assertIn("Secret Scanning and Secret Scanning Push Protection enabled", integrity)
        self.assertIn("Dependabot security updates and Dependabot alerts were", integrity)
        self.assertIn("Status: historical local maintenance candidate", candidate)
        self.assertIn("locally recorded current published patch\nbaseline remains `v0.3.1`", candidate)

    def test_v040_release_control_route_preserves_c4_and_post_release_stops(self) -> None:
        control = (RELEASE_ROOT / "RELEASE_CONTROL.md").read_text(encoding="utf-8")
        self.assertIn("Candidate-review acceptance is not C4 authorization", control)
        self.assertIn("C4 authorization is not\npost-release verification", control)
        self.assertIn("Before C4, retain `c4_release_authorization_reference` as `null`", control)


if __name__ == "__main__":
    unittest.main()
