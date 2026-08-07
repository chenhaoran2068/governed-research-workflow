"""Release-facing checks for the v1.8 future-Study lifecycle guidance."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V18FutureStudyLifecycleTests(unittest.TestCase):
    def test_public_material_is_generic_and_bounded(self) -> None:
        guidance = (ROOT / "references" / "future-study-lifecycle-design-governance-and-analysis-state.md").read_text(encoding="utf-8")
        self.assertIn("eleven stages", guidance.lower())
        self.assertIn("does not discover", guidance)
        self.assertIn("separately governed", guidance)
        self.assertNotIn("E:" + "\\Chenhaoran", guidance)

    def test_capability_and_public_paths_exist(self) -> None:
        required = [
            "assets/future-study-lifecycle/study-design-and-classification-record.template.json",
            "assets/future-study-lifecycle/governance-readiness-record.template.json",
            "assets/future-study-lifecycle/analysis-state-and-freeze-decision.template.json",
            "scripts/validate_future_study_lifecycle_records.py",
            "system/03_workflows/FUTURE_STUDY_LIFECYCLE_DESIGN_GOVERNANCE_AND_ANALYSIS_STATE.md",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
