"""Regression checks for v0.4.0 historical pre-release boundaries."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V04ReleasePreparationTests(unittest.TestCase):
    def test_historical_pre_release_documents_remain_non_release_material(self) -> None:
        expected = {
            "V0_4_CAPABILITY_ADMISSION.md": "historical pre-c4 admission record",
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

    def test_release_source_ledger_records_exact_option_a_admission_without_a_release(self) -> None:
        capabilities = json.loads(LEDGER.read_text(encoding="utf-8"))["capabilities"]
        admitted_ids = {
            "GRW-CAP-031-01",
            "GRW-CAP-031-02",
            "GRW-CAP-031-03",
            "GRW-CAP-031-04",
            "GRW-CAP-040-00",
            "GRW-CAP-040-01",
            "GRW-CAP-040-02",
            "GRW-CAP-040-04",
            "GRW-CAP-040-05",
            "GRW-CAP-040-06",
            "GRW-CAP-050-01",
        }
        for capability in capabilities:
            if capability["capability_id"] == "GRW-CAP-040-03":
                self.assertEqual(capability["release_disposition"], "excluded")
                self.assertEqual(capability["public_claim_status"], "forbidden")
            else:
                self.assertIn(capability["capability_id"], admitted_ids)
                self.assertEqual(capability["release_disposition"], "admitted")
                self.assertEqual(capability["public_claim_status"], "permitted")


if __name__ == "__main__":
    unittest.main()
