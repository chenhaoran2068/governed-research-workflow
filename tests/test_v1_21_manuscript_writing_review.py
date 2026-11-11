"""Regression checks for the v1.21 generic manuscript-writing candidate."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = ROOT / "references" / "manuscript-writing-and-linked-review.md"
CHECKLIST = (
    ROOT
    / "assets"
    / "manuscript-writing-review"
    / "manuscript-writing-linked-review-checklist.template.md"
)
ASSEMBLY_TEMPLATE = (
    ROOT
    / "assets"
    / "manuscript-governance"
    / "manuscript-assembly-claim-display-review.template.md"
)
CONTROL = ROOT / "system" / "11_distribution_installation_and_release" / "V1_21_MANUSCRIPT_WRITING_REVIEW_CANDIDATE.md"
AUDIT = ROOT / "system" / "11_distribution_installation_and_release" / "V1_21_MANUSCRIPT_WRITING_REVIEW_AUDIT.md"
SKILL = ROOT / "SKILL.md"
PRIVATE_MARKERS = (
    r"(?i)[a-z]:\\",
    r"(?i)research[0-9]+",
    r"(?i)crs_dev",
    r"(?i)paco2",
    r"(?i)sepsis",
    r"(?i)99sai",
)


class V121ManuscriptWritingReviewTests(unittest.TestCase):
    @staticmethod
    def normalized(path: Path) -> str:
        return " ".join(path.read_text(encoding="utf-8").lower().split())

    def test_guidance_covers_all_eight_practices(self) -> None:
        text = self.normalized(GUIDANCE)
        expected = (
            "narrative weight",
            "structure results by result role",
            "put information where a reader needs it",
            "state limitations clearly",
            "describe cohort eligibility in two layers",
            "cohort flow as reconciled evidence",
            "review every material claim with its evidence",
            "reconcile the candidate before a human decision",
        )
        for item in expected:
            with self.subTest(item=item):
                self.assertIn(item, text)

    def test_guidance_preserves_reporting_and_authority_boundaries(self) -> None:
        text = self.normalized(GUIDANCE)
        for expected in (
            "not a journal instruction",
            "do not change a study",
            "not whether a p value",
            "does not permit hiding bias",
            "accountable-human",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_checklist_and_template_cover_linked_review_without_claiming_authority(self) -> None:
        checklist = self.normalized(CHECKLIST)
        assembly = self.normalized(ASSEMBLY_TEMPLATE)
        for expected in (
            "narrative weight",
            "information placement",
            "eligibility and flow",
            "claims, displays, and dependencies",
            "candidate reconciliation",
            "does not establish",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, checklist)
        for expected in ("narrative and information placement", "eligibility and flow"):
            self.assertIn(expected, assembly)

    def test_candidate_and_public_material_are_generic(self) -> None:
        content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (GUIDANCE, CHECKLIST, ASSEMBLY_TEMPLATE, CONTROL)
        )
        for pattern in PRIVATE_MARKERS:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, content), pattern)
        self.assertIn("candidate_local_not_released_not_adopted", CONTROL.read_text(encoding="utf-8"))

    def test_skill_extends_the_existing_manuscript_route_without_new_authority(self) -> None:
        text = self.normalized(SKILL)
        for expected in (
            "references/manuscript-writing-and-linked-review.md",
            "controlled enhancement of this existing manuscript route",
            "not a new task class or separate authority",
            "require the exact study root",
            "do not select a research/reporting profile",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_audit_records_verification_and_retains_owner_gates(self) -> None:
        text = self.normalized(AUDIT)
        for expected in (
            "no blocking implementation finding",
            "rr-2 promotion and route re-review",
            "full v1.21 regression suite after the route change: 449 tests passed; 3 tests skipped.",
            "release and runtime adoption remain pending",
            "does not authorise a tag, remote push, github release, publication, installation",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
