"""Release-facing boundary checks for the v1.15 joint-review profile source."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "system" / "11_distribution_installation_and_release"
PUBLIC_PATHS = (
    "README.md",
    "ROADMAP.md",
    "SKILL.md",
    "SYSTEM_MANIFEST.yaml",
    "PUBLIC_BOUNDARY.md",
    "references/joint-review-profiles-and-dependency-order.md",
    "assets/joint-review-plan.template.json",
    "assets/joint-review-plan.template.md",
    "system/09_schemas_records_and_templates/joint_review_plan.schema.json",
    "scripts/validate_joint_review_plan.py",
)
RELEASE_RECORDS = (
    "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.15.0.md",
    "RELEASE_NOTES_v1.15.0.md",
    "V1_15_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
    "V1_15_RELEASE_CONTROL_CANDIDATE.json",
    "V1_15_RELEASE_EVIDENCE.md",
    "V1_15_RELEASE_GATE.md",
)
PRIVATE_MARKERS = (
    r"(?i)[a-z]:\\",
    r"(?i)researchx_",
    r"(?i)src-[a-z0-9]",
    r"(?i)xvt-[0-9]",
)


class V115JointReviewProfileTests(unittest.TestCase):
    def test_manifest_and_ledger_admit_the_named_generic_capability(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        ledger = json.loads((ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json").read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-230-01")
        self.assertIn("system_version: 1.18.0", manifest)
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["version"]["target_release"], "v1.15.0")

    def test_public_paths_and_release_records_exist(self) -> None:
        for relative in PUBLIC_PATHS:
            self.assertTrue((ROOT / relative).is_file(), relative)
        for name in RELEASE_RECORDS:
            self.assertTrue((RELEASE_ROOT / name).is_file(), name)

    def test_public_guidance_keeps_default_and_specialist_routes_distinct(self) -> None:
        guidance = (ROOT / "references" / "joint-review-profiles-and-dependency-order.md").read_text(encoding="utf-8")
        self.assertIn("observational_empirical_original_research_v1", guidance)
        self.assertIn("additional_review_profile_required", guidance)
        self.assertIn("Do not force", guidance)
        self.assertIn("R0 - profile and reporting context", guidance)
        self.assertIn("R10 - reconciliation, revision, and archive", guidance)

    def test_public_surface_is_generic_and_does_not_claim_project_or_release_authority(self) -> None:
        content = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in PUBLIC_PATHS)
        normalized = " ".join(content.lower().split())
        for pattern in PRIVATE_MARKERS:
            self.assertIsNone(re.search(pattern, content), pattern)
        self.assertIn("does not select a profile", normalized)
        self.assertIn("does not resolve references", normalized)
        self.assertIn("scientific, governance, submission, or release", normalized)

    def test_release_records_keep_later_gates_pending(self) -> None:
        control = json.loads((RELEASE_ROOT / "V1_15_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        gate = (RELEASE_ROOT / "V1_15_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        evidence = (RELEASE_ROOT / "V1_15_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        self.assertEqual(control["status"], "source_prepared_not_released")
        self.assertEqual(control["capability_ids"], ["GRW-CAP-230-01"])
        self.assertIn("release remains blocked", gate)
        self.assertIn("not evidence", evidence)


if __name__ == "__main__":
    unittest.main()
