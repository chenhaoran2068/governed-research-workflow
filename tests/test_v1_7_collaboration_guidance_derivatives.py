"""Regression checks for the v1.7 public collaboration-guidance scope."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "public-experience-derivatives"
VOCABULARY = ASSETS / "public_experience_vocabulary.json"
CATALOGUE = ASSETS / "public_experience_catalogue.json"
CARDS = ASSETS / "cards"


class V17CollaborationGuidanceDerivativesTests(unittest.TestCase):
    def test_new_topics_and_cards_are_present_with_no_fabricated_kge_origin(self) -> None:
        vocabulary = json.loads(VOCABULARY.read_text(encoding="utf-8"))
        catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        terms = {term["public_topic_id"]: term for term in vocabulary["terms"]}
        cards = {card["public_experience_id"]: card for card in catalogue["cards"]}

        self.assertEqual(vocabulary["vocabulary_version"], "v1.7.0")
        self.assertEqual(catalogue["catalogue_version"], "v1.7.0")
        self.assertEqual(
            {term_id: terms[term_id]["canonical_term"] for term_id in ("GRW-TOP-016", "GRW-TOP-017", "GRW-TOP-018")},
            {
                "GRW-TOP-016": "substantive-reader-facing-delivery",
                "GRW-TOP-017": "plan-state-visibility-and-change-control",
                "GRW-TOP-018": "governed-task-initiation",
            },
        )
        for number in range(1, 39):
            card = cards[f"GRW-EXP-{number:03d}"]
            self.assertEqual(card["legacy_public_identifier"], f"KGE-{number:03d}")
        for number in range(39, 42):
            card = cards[f"GRW-EXP-{number:03d}"]
            self.assertIsNone(card["legacy_public_identifier"])
            self.assertTrue((CARDS / f"GRW-EXP-{number:03d}.md").is_file())

    def test_guidance_is_selective_and_non_authoritative(self) -> None:
        content = (ROOT / "system" / "03_workflows" / "SUBSTANTIVE_CONTENT_BEFORE_SUPPORTING_MATERIAL_REFERENCE.md").read_text(encoding="utf-8").lower()
        plan = (ROOT / "system" / "03_workflows" / "PLAN_STATE_VISIBILITY_AND_CONTROLLED_CHANGE.md").read_text(encoding="utf-8").lower()
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("does not", content)
        self.assertIn("does not", plan)
        self.assertIn("visible plan is not authorization", plan)
        self.assertIn("selective public", skill)
        self.assertIn("guidance, not a retrieval", skill)

    def test_release_materials_name_only_the_new_public_capability(self) -> None:
        admission = (ROOT / "system" / "11_distribution_installation_and_release" / "GRW_CAP_170_01_PUBLIC_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8")
        control = json.loads((ROOT / "system" / "11_distribution_installation_and_release" / "V1_7_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        self.assertIn("GRW-CAP-170-01", admission)
        self.assertEqual(control["candidate_release_version"], "v1.7.0")
        self.assertEqual(control["capability_ids"], ["GRW-CAP-170-01"])
        self.assertEqual(control["public_baseline"]["annotated_tag"], "v1.6.0")


if __name__ == "__main__":
    unittest.main()
