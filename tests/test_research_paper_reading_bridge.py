"""Source-free structural and refusal checks for GRW-CAP-210-01."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
BRIDGE_PATH = ROOT / "references" / "research-paper-reading-bridge.md"
NAVIGATOR_PATH = ROOT / "references" / "new-study-navigator-and-route-recommendation.md"


class ResearchPaperReadingBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.bridge = BRIDGE_PATH.read_text(encoding="utf-8")
        cls.navigator = NAVIGATOR_PATH.read_text(encoding="utf-8")
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_capability_is_explicit_and_source_free(self) -> None:
        record = next(item for item in self.ledger["capabilities"] if item["capability_id"] == "GRW-CAP-210-01")
        self.assertEqual("routing", record["capability_class"])
        self.assertEqual("v1.11.0", record["version"]["target_release"])
        self.assertIn("paper-reading", record["promise"])
        self.assertIn("Does not", record["non_promise"])
        self.assertIn("no_data_access", record["data_and_external_boundary"])
        self.assertIn("no_external_service_action", record["data_and_external_boundary"])

    def test_specific_paper_reading_is_not_a_new_study_by_default(self) -> None:
        normalized_navigator = " ".join(self.navigator.split()).lower()
        normalized_skill = " ".join(self.skill.split()).lower()
        for text in (normalized_navigator, normalized_skill):
            self.assertIn("specific scholarly paper", text)
            self.assertIn("unless the same request clearly asks", text)
        self.assertIn("not a possible new study request", normalized_navigator)
        self.assertIn("not a possible new study merely", normalized_skill)
        self.assertIn("do not begin with `Route:`", self.skill)

    def test_bridge_does_not_invoke_or_operate_the_reading_skill(self) -> None:
        for required in (
            "research-paper-reading",
            "does not discover, invoke, install, configure, or verify",
            "Do not read, download, copy, parse, quote, summarize, index, classify, or",
            "Do not create a reading dossier",
            "not a source-verification service",
        ):
            self.assertIn(required, self.bridge)
        for text in (self.bridge, self.navigator, self.skill):
            self.assertNotIn("E:" + "\\\\Chenhaoran", text)


if __name__ == "__main__":
    unittest.main()
