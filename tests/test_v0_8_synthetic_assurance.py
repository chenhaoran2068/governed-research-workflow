"""Cross-control assurance for the v0.8 candidate source only."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
ROLE_REFERENCE_PATH = REPOSITORY_ROOT / "references" / "role-contracts.md"
HELPER_REFERENCE_PATH = REPOSITORY_ROOT / "references" / "controlled-helper-admission.md"


class V08SyntheticAssuranceTests(unittest.TestCase):
    def test_candidate_capabilities_are_present_but_not_publicly_claimable(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        records = {record["capability_id"]: record for record in ledger["capabilities"]}
        self.assertEqual(
            set(records).intersection({"GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"}),
            {"GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"},
        )
        for capability_id in ("GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"):
            record = records[capability_id]
            self.assertEqual(record["implementation_status"], "implemented")
            self.assertEqual(record["release_disposition"], "candidate")
            self.assertEqual(record["public_claim_status"], "forbidden")
            self.assertEqual(record["evidence"]["status"], "unverified")
            self.assertEqual(record["version"]["target_release"], "v0.8.0")
            self.assertIn("C2", record["approval_reference"])
            self.assertIn("C4 remain pending", record["approval_reference"])

    def test_role_m53_helper_and_per_run_controls_remain_non_substitutable(self) -> None:
        combined = (ROLE_REFERENCE_PATH.read_text(encoding="utf-8") + "\n" + HELPER_REFERENCE_PATH.read_text(encoding="utf-8")).lower()
        for required in ("role contract", "m53", "helper admission", "per-run write confirmation", "data/share evidence"):
            self.assertIn(required, combined)
        self.assertIn("cannot replace", combined)
        self.assertIn("not m53", combined)

    def test_candidate_source_retains_no_runtime_or_generic_writer_claim(self) -> None:
        module = (REPOSITORY_ROOT / "system" / "08_agent_contracts" / "MODULE.md").read_text(encoding="utf-8").lower()
        helper_reference = HELPER_REFERENCE_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("no role card", module)
        self.assertIn("no runnable", module)
        self.assertIn("no generic writer", helper_reference)
        self.assertFalse((REPOSITORY_ROOT / "system" / "08_agent_contracts" / "runtime").exists())
        self.assertFalse((REPOSITORY_ROOT / "agent_runtime").exists())


if __name__ == "__main__":
    unittest.main()
