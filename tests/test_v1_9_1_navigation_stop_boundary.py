"""Regression checks for the v1.9.1 possible-new-Study stop boundary."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V191NavigationStopBoundaryTests(unittest.TestCase):
    def test_first_response_has_one_human_confirmable_route_contract(self) -> None:
        guidance = (ROOT / "references" / "new-study-navigator-and-route-recommendation.md").read_text(encoding="utf-8")
        for expected in (
            "Return exactly one of:",
            "The first substantive response must contain exactly these six parts:",
            "the user's choices to accept, revise, defer, or reject.",
            "For `insufficient_information`, ask\nno more than two focused questions",
        ):
            self.assertIn(expected, guidance)

    def test_causal_and_randomized_requests_stop_before_methods_or_sources(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        guidance = (ROOT / "references" / "new-study-navigator-and-route-recommendation.md").read_text(encoding="utf-8")
        for expected in (
            "return only\n`v1_8_with_specialist_review`",
            "Do not give\nestimators, models, weighting methods, eligibility rules, or external sources",
            "return only `specialist_module_required`",
        ):
            self.assertIn(expected, skill)
        for expected in (
            "target-trial-emulation review, and stop.",
            "name the specialist trial route, and stop.",
            "it also does not provide an estimator,\nmodel, weighting method, target-trial specification, analysis procedure,\nexternal source, citation, link, or data-access suggestion.",
        ):
            self.assertIn(expected, guidance)

    def test_public_surfaces_preserve_the_same_priority_boundary(self) -> None:
        surfaces = (
            ROOT / "assets" / "START_HERE.md",
            ROOT / "references" / "startup-and-routing.md",
            ROOT / "system" / "03_workflows" / "NEW_STUDY_NAVIGATOR_AND_ROUTE_RECOMMENDATION.md",
            ROOT / "PUBLIC_BOUNDARY.md",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in surfaces)
        self.assertIn("before methods", text)
        self.assertIn("project creation", text)
        self.assertNotIn("E:" + "\\Chenhaoran", text)


if __name__ == "__main__":
    unittest.main()
