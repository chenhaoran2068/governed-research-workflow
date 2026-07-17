"""Regression checks for v0.4.0 historical pre-C3 preparation boundaries."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V04ReleasePreparationTests(unittest.TestCase):
    def test_historical_pre_c3_documents_remain_non_release_material(self) -> None:
        expected = {
            "V0_4_CAPABILITY_ADMISSION.md": "no `v0.4.0` tag or github release",
            "V0_4_RELEASE_GATE.md": "historical pre-c3 gate snapshot",
            "V0_4_RELEASE_EVIDENCE.md": "historical pre-c3 preparation evidence only",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.4.0.md": "historical pre-c3 preparation record",
            "RELEASE_NOTES_v0.4.0.md": "historical pre-c3 draft snapshot",
        }
        for name, boundary in expected.items():
            content = (DIST / name).read_text(encoding="utf-8")
            self.assertIn(boundary, content.lower())
            self.assertNotIn("v0.4.0 has been released", content.lower())

    def test_gate_preserves_exact_commit_and_human_release_boundaries(self) -> None:
        content = (DIST / "V0_4_RELEASE_GATE.md").read_text(encoding="utf-8")
        for gate in range(1, 8):
            self.assertIn(f"R40-G{gate}", content)
        self.assertIn("C3 and C4 remain distinct", content)
        self.assertIn("exact candidate commit", content)

    def test_candidate_ledger_is_not_admitted_or_publicly_claimable(self) -> None:
        capabilities = json.loads(LEDGER.read_text(encoding="utf-8"))["capabilities"]
        for capability in capabilities:
            self.assertEqual(capability["public_claim_status"], "forbidden")
            if capability["capability_id"] == "GRW-CAP-040-03":
                self.assertEqual(capability["release_disposition"], "excluded")
            else:
                self.assertEqual(capability["release_disposition"], "candidate")


if __name__ == "__main__":
    unittest.main()
