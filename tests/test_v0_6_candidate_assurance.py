"""Assurance checks for the local-only v0.6 workflow/evidence candidate."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tests.test_v0_4_synthetic_assurance import source_snapshot_sha256


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
README_PATH = REPOSITORY_ROOT / "README.md"
ROADMAP_PATH = REPOSITORY_ROOT / "ROADMAP.md"
SKILL_PATH = REPOSITORY_ROOT / "SKILL.md"
FRAMEWORK_PLAN_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "FRAMEWORK_INTEGRATION_PLAN.md"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "test-bootstrap.yml"
EVIDENCE_MAP_PATH = REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "V0_6_CANDIDATE_EVIDENCE_MAP.md"
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"
SYNTHETIC_ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_6_SYNTHETIC_ASSURANCE.md"
SYNTHETIC_ASSURANCE_RELATIVE_PATH = SYNTHETIC_ASSURANCE_PATH.relative_to(REPOSITORY_ROOT).as_posix().encode("utf-8")


class V06CandidateAssuranceTests(unittest.TestCase):
    def test_candidate_identity_is_distinct_from_the_published_v051_base(self) -> None:
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
        self.assertIn("system_version: 0.6.0-workflow-evidence-controls-candidate", manifest)
        self.assertIn("local unreleased `v0.6.0` candidate", readme)
        self.assertIn("`v0.5.1` is its published release-state-maintenance", readme)
        self.assertIn("## v0.6.0 (unreleased workflow/evidence-control candidate)", roadmap)
        self.assertIn("## v0.5.1 (published release-state maintenance)", roadmap)

    def test_candidate_is_not_admitted_in_the_canonical_capability_ledger(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        capability_ids = {record["capability_id"] for record in ledger["capabilities"]}
        self.assertNotIn("GRW-CAP-060-01", capability_ids)
        evidence_map = EVIDENCE_MAP_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("not admitted", evidence_map)
        self.assertIn("not publicly claimable", evidence_map)
        self.assertIn("not the canonical\ncapability truth ledger", EVIDENCE_MAP_PATH.read_text(encoding="utf-8"))

    def test_candidate_interfaces_are_present_and_metadata_only(self) -> None:
        required_paths = (
            "system/09_schemas_records_and_templates/workflow_evidence_control_bundle.schema.json",
            "system/09_schemas_records_and_templates/workflow_evidence_control_baseline.schema.json",
            "assets/workflow-evidence-control-bundle.template.json",
            "assets/workflow-evidence-control-baseline.template.json",
            "scripts/validate_workflow_evidence_control_bundle.py",
            "references/workflow-evidence-control-records.md",
            "tests/test_workflow_evidence_control_bundle.py",
            "system/12_synthetic_examples/V0_6_SYNTHETIC_ASSURANCE.md",
        )
        for relative_path in required_paths:
            self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)
        reference = (REPOSITORY_ROOT / "references" / "workflow-evidence-control-records.md").read_text(encoding="utf-8").lower()
        self.assertIn("metadata-only", reference)
        self.assertIn("does not", reference)

    def test_release_and_runtime_boundaries_remain_pending(self) -> None:
        candidate_records = (
            "V0_6_RELEASE_GATE.md",
            "V0_6_RELEASE_EVIDENCE.md",
            "V0_6_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.6.0.md",
            "RELEASE_NOTES_v0.6.0.md",
        )
        candidate_text = "\n".join((RELEASE_ROOT / name).read_text(encoding="utf-8") for name in candidate_records).lower()
        self.assertIn("not published", candidate_text)
        self.assertIn("not a capability\nadmission", candidate_text)
        self.assertIn("not authorize", candidate_text)
        self.assertIn("runtime-installation", candidate_text)

    def test_current_framework_validation_target_is_v012_and_historical_v04_evidence_is_not_rewritten(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        plan = FRAMEWORK_PLAN_PATH.read_text(encoding="utf-8")
        historical_v04 = (REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_4_SYNTHETIC_ASSURANCE.md").read_text(encoding="utf-8")
        self.assertIn("FRAMEWORK_RELEASE_TAG: v0.1.2", workflow)
        self.assertIn("FRAMEWORK_EXPECTED_COMMIT: 97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8", workflow)
        self.assertIn("Workspace Framework `v0.1.2`", plan)
        self.assertIn("framework tag: `v0.1.1`", historical_v04)

    def test_v06_candidate_assurance_uses_the_existing_tracked_source_snapshot_method(self) -> None:
        assurance = SYNTHETIC_ASSURANCE_PATH.read_text(encoding="utf-8")
        match = re.search(r"candidate source snapshot SHA-256: `([0-9a-f]{64})`", assurance)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), source_snapshot_sha256(SYNTHETIC_ASSURANCE_RELATIVE_PATH))
        self.assertIn("This assurance file\n  is excluded from its own digest", assurance)

    def test_candidate_surfaces_have_no_private_path_or_release_claim(self) -> None:
        candidate_paths = (
            README_PATH,
            ROADMAP_PATH,
            SKILL_PATH,
            EVIDENCE_MAP_PATH,
            REPOSITORY_ROOT / "references" / "workflow-evidence-control-records.md",
            REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_6_SYNTHETIC_ASSURANCE.md",
        )
        candidate_text = "\n".join(path.read_text(encoding="utf-8") for path in candidate_paths)
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\|/(?:home|users)/)", candidate_text))
        self.assertNotIn("v0.6.0 is published", candidate_text.lower())
        self.assertNotIn("v0.6.0 provides an agent runtime", candidate_text.lower())


if __name__ == "__main__":
    unittest.main()
