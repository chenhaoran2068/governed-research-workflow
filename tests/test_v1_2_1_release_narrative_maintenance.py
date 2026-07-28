"""Regression tests for v1.2.1 release-narrative maintenance."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V121ReleaseNarrativeMaintenanceTests(unittest.TestCase):
    def test_maintenance_records_exist_and_control_record_validates(self) -> None:
        required = (
            "RELEASE_NOTES_v1.2.1.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.2.1.md",
            "V1_2_1_MAINTENANCE_SCOPE.md",
            "V1_2_1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V1_2_1_RELEASE_CONTROL_CANDIDATE.json",
            "V1_2_1_RELEASE_GATE.md",
            "V1_2_1_RELEASE_EVIDENCE.md",
        )
        for name in required:
            self.assertTrue((RELEASE_DIR / name).is_file(), name)

        record = json.loads(
            (RELEASE_DIR / "V1_2_1_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8")
        )
        schema = json.loads((RELEASE_DIR / "release_control_record.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["candidate_version"], "1.2.1")
        self.assertEqual(record["candidate_identity"]["intended_tag"], "v1.2.1")
        self.assertEqual(record["c4_release_authorization_reference"], None)
        self.assertEqual(record["post_release_verification_reference"], None)

    def test_release_notes_are_user_facing_and_time_neutral(self) -> None:
        text = (RELEASE_DIR / "RELEASE_NOTES_v1.2.1.md").read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertIn("release narration", lowered)
        self.assertIn("does not add, remove, or change", lowered)
        for forbidden in (
            "later matching github release",
            "future release source",
            "candidate",
            "pending",
            "not yet published",
            "installed runtime",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_current_records_preserve_v120_verification_without_live_v121_claim(self) -> None:
        current_paths = (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            RELEASE_DIR / "CURRENT_RELEASE_STATUS.md",
            LEDGER_PATH,
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in current_paths)
        lowered = text.lower()
        self.assertIn("v1.2.0", lowered)
        self.assertIn("v1.2.1", lowered)
        for forbidden in ("v1.2.1 is released", "v1.2.1 is current", "v1.2.1 is latest", "v1.2.1 is installed"):
            self.assertNotIn(forbidden, lowered)

        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-120-01")
        self.assertEqual(record["version"]["introduced_version"], "v1.2.0")
        self.assertEqual(record["version"]["last_verified_release"], "v1.2.0")
        self.assertEqual(record["version"]["target_release"], "v1.2.0")
        self.assertIn({"release_version": "v1.2.0", "public_claim_status": "permitted"}, record["prior_release_history"])
        self.assertIn("exact annotated tag and matching github release", record["limitations_and_next_action"].lower())

    def test_v120_historical_release_notes_are_retained_unchanged(self) -> None:
        historical_notes = RELEASE_DIR / "RELEASE_NOTES_v1.2.0.md"
        text = historical_notes.read_text(encoding="utf-8")
        self.assertIn("# V1.2.0 Release Notes Source", text)
        self.assertIn("later matching GitHub Release", text)


if __name__ == "__main__":
    unittest.main()
