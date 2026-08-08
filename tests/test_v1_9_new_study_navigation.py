"""Release-facing checks for GRW-CAP-190-01 new-Study navigation."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V19NewStudyNavigationTests(unittest.TestCase):
    def test_public_navigator_is_generic_and_human_confirmable(self) -> None:
        guidance = (ROOT / "references" / "new-study-navigator-and-route-recommendation.md").read_text(encoding="utf-8")
        for expected in (
            "v1_8_primary_route_candidate",
            "v1_8_with_specialist_review",
            "specialist_module_required",
            "insufficient_information",
            "the user's choices to accept, revise, defer, or reject.",
            "does not create a Study",
        ):
            self.assertIn(expected, guidance)
        self.assertNotIn("E:" + "\\Chenhaoran", guidance)

    def test_public_capability_paths_and_boundaries_exist(self) -> None:
        required = (
            "references/new-study-navigator-and-route-recommendation.md",
            "system/03_workflows/NEW_STUDY_NAVIGATOR_AND_ROUTE_RECOMMENDATION.md",
            "system/11_distribution_installation_and_release/GRW_CAP_190_01_PUBLIC_CAPABILITY_ADMISSION.md",
            "system/11_distribution_installation_and_release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.9.0.md",
            "system/11_distribution_installation_and_release/RELEASE_NOTES_v1.9.0.md",
            "system/11_distribution_installation_and_release/V1_9_RELEASE_CONTROL_CANDIDATE.json",
            "system/11_distribution_installation_and_release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.9.1.md",
            "system/11_distribution_installation_and_release/RELEASE_NOTES_v1.9.1.md",
            "system/11_distribution_installation_and_release/V1_9_1_RELEASE_CONTROL_CANDIDATE.json",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

        boundary = (ROOT / "PUBLIC_BOUNDARY.md").read_text(encoding="utf-8")
        self.assertIn("New-Study Navigation Material", boundary)
        self.assertIn("does not read material", boundary)

    def test_skill_automatically_navigates_only_possible_new_study_intent(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        self.assertIn("When ordinary language indicates a possible new Study", normalized)
        self.assertIn("the navigator is the first substantive response", normalized)
        self.assertIn("does not create a Study", normalized)
        self.assertIn("user confirms the navigator's lifecycle route", normalized)
        self.assertIn("the navigator is the first substantive response", normalized)


if __name__ == "__main__":
    unittest.main()
