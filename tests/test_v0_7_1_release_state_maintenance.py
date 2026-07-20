"""Regression controls preserving v0.7.1 history in the v0.8 source."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"


class V071HistoricalMaintenanceTests(unittest.TestCase):
    def test_current_v08_source_retains_v071_history_without_reclassifying_v070(self) -> None:
        manifest = (REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        index = (REPOSITORY_ROOT / "system" / "INDEX.md").read_text(encoding="utf-8")

        self.assertIn("system_version: 0.8.1-dependency-lifecycle-maintenance-source", manifest)
        self.assertIn("Status: v0.8.1 maintenance source", readme)
        self.assertIn("## v0.8.0 (historical pre-C4 portability, role-contract, and helper-admission source)", roadmap)
        self.assertIn("## v0.7.1 (release-state and control-hardening maintenance source)", roadmap)
        self.assertIn("## v0.7.0 (historical human-reviewed lesson-promotion release source)", roadmap)
        self.assertIn("## Planned After v0.7 (not current capability)", roadmap)
        self.assertNotIn("v0.7.x: candidate", roadmap.lower())
        self.assertIn("Status: v0.8.1 maintenance source", index)

    def test_maintenance_keeps_the_v070_capability_identity_and_boundary(self) -> None:
        ledger_path = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-070-01")

        self.assertEqual(ledger["release_context"]["source_release_version"], "v0.8.1")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.8.1")
        self.assertIn("released historical scopes through v0.8.1", ledger["target_claim_scope"])
        self.assertEqual(record["version"]["introduced_version"], "v0.7.0")
        self.assertEqual(record["version"]["target_release"], "v0.7.0")
        self.assertEqual(record["version"]["last_verified_release"], "v0.7.0")
        limitations = record["limitations_and_next_action"].lower()
        self.assertIn("public availability", limitations)
        self.assertIn("exact immutable tag and matching github release", limitations)
        self.assertIn("separate controlled action", limitations)

    def test_maintenance_materials_are_present_and_do_not_claim_a_release(self) -> None:
        contract = RELEASE_ROOT / "V0_7_1_RELEASE_STATE_MAINTENANCE.md"
        rights = RELEASE_ROOT / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.7.1.md"
        notes = RELEASE_ROOT / "RELEASE_NOTES_v0.7.1.md"
        for path in (contract, rights, notes):
            self.assertTrue(path.is_file(), path)

        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in (contract, rights, notes))
        normalized = " ".join(combined.split())
        self.assertIn("does not itself prove", normalized)
        self.assertIn("historical pre-c3 review snapshot", normalized)
        self.assertIn("does not add a new capability category", normalized)
        self.assertIn("schema `1.0.0` readability", normalized)
        self.assertNotIn("e:\\", combined)
        self.assertNotIn("c:\\users", combined)


if __name__ == "__main__":
    unittest.main()
