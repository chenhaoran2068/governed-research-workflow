"""Source-free structural and refusal checks for GRW-CAP-200-01."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
BRIDGE_PATH = ROOT / "references" / "research-ethics-preparation-bridge.md"
FIXTURE_ROOT = ROOT / "tests" / "fixtures"


class ResearchEthicsPreparationBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.bridge = BRIDGE_PATH.read_text(encoding="utf-8")
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_capability_is_explicit_metadata_only_routing(self) -> None:
        record = next(
            item
            for item in self.ledger["capabilities"]
            if item["capability_id"] == "GRW-CAP-200-01"
        )
        self.assertEqual("routing", record["capability_class"])
        self.assertEqual("v1.10.0", record["version"]["target_release"])
        self.assertIn("user-named compatible ethics-preparation module", record["promise"])
        self.assertIn("Does not", record["non_promise"])
        self.assertIn("no_data_access", record["data_and_external_boundary"])
        self.assertIn("no_external_service_action", record["data_and_external_boundary"])

    def test_bridge_requires_explicit_user_inputs_and_preserves_authority(self) -> None:
        for required in (
            "one compatible module and its caller-supplied public manifest",
            "one exact Study root",
            "actual_submission",
            "test_public",
            "exact protocol and compliance inputs",
            "Do not scan for modules or projects",
            "The current protocol remains authoritative in `03_protocol/`",
            "Do not let a module manifest, draft, template, field check, or generated Word",
        ):
            self.assertIn(required, self.bridge)

    def test_skill_does_not_automatically_invoke_the_optional_module(self) -> None:
        normalized = " ".join(self.skill.split())
        self.assertIn("GRW-CAP-200-01", normalized)
        self.assertIn("explicitly requests China Mainland ethics", normalized)
        self.assertIn("Do not discover a module or Study", normalized)
        self.assertIn("invoke a Skill automatically", normalized)

    def test_synthetic_valid_and_invalid_manifest_cases_are_separate(self) -> None:
        valid = (FIXTURE_ROOT / "research_ethics_module_manifest_valid.yaml").read_text(
            encoding="utf-8"
        )
        invalid = (FIXTURE_ROOT / "research_ethics_module_manifest_invalid.yaml").read_text(
            encoding="utf-8"
        )
        for expected in (
            "bridge_interface_version: 1.0.0",
            "source_discovery: forbidden",
            "automatic_invocation: forbidden",
        ):
            self.assertIn(expected, valid)
        for rejected in (
            "bridge_interface_version: 2.0.0",
            "source_discovery: allowed",
            "automatic_invocation: allowed",
        ):
            self.assertIn(rejected, invalid)
        for text in (valid, invalid):
            self.assertNotIn("E:" + "\\Chenhaoran", text)
            self.assertNotIn("project_id:", text)
            self.assertNotIn("\nstudy_root:", text)

    def test_out_of_scope_routes_remain_explicit_stops(self) -> None:
        for route in (
            "prospective\nresearcher-assigned",
            "randomized",
            "interventional",
            "product",
            "device",
            "IVD",
            "non-China",
        ):
            self.assertIn(route, self.bridge)
        self.assertIn("causal-design or target-trial-emulation review", self.bridge)


if __name__ == "__main__":
    unittest.main()
