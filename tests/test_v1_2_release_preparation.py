"""Release-preparation checks for the v1.2.0 versioned source scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V12ReleasePreparationTests(unittest.TestCase):
    def test_versioned_release_preparation_chain_exists_and_control_record_validates(self) -> None:
        required = (
            "V1_2_CAPABILITY_ADMISSION.md",
            "V1_2_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V1_2_RELEASE_CONTROL_CANDIDATE.json",
            "V1_2_RELEASE_EVIDENCE.md",
            "V1_2_RELEASE_GATE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.2.0.md",
            "RELEASE_NOTES_v1.2.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE_DIR / name).is_file(), name)

        record = json.loads((RELEASE_DIR / "V1_2_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        schema = json.loads((RELEASE_DIR / "release_control_record.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["candidate_version"], "1.2.0")
        self.assertEqual(record["candidate_identity"]["intended_tag"], "v1.2.0")
        self.assertEqual(record["c4_release_authorization_reference"], None)
        self.assertEqual(record["post_release_verification_reference"], None)

    def test_current_facing_v12_surfaces_are_time_neutral_and_not_live_claims(self) -> None:
        paths = (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            ROOT / "system" / "06_memory_and_learning" / "MODULE.md",
            LEDGER_PATH,
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        lowered = text.lower()
        self.assertIn("v1.2.0 versioned source scope", lowered)
        self.assertNotIn("v1.2.0 candidate source", lowered)
        for forbidden in (
            "v1.2.0 is released",
            "v1.2.0 is current",
            "v1.2.0 is latest",
            "v1.2.0 is installed",
        ):
            self.assertNotIn(forbidden, lowered)

        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-120-01")
        self.assertIn("exact annotated tag and matching GitHub Release", record["limitations_and_next_action"])

    def test_versioned_records_stay_pre_c4_and_generic(self) -> None:
        names = (
            "V1_2_CAPABILITY_ADMISSION.md",
            "V1_2_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V1_2_RELEASE_EVIDENCE.md",
            "V1_2_RELEASE_GATE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.2.0.md",
            "RELEASE_NOTES_v1.2.0.md",
        )
        text = "\n".join((RELEASE_DIR / name).read_text(encoding="utf-8") for name in names)
        lowered = text.lower()
        self.assertIn("pre-c4", lowered)
        self.assertIn("not c4", lowered)
        self.assertIn("matching github release", lowered)
        self.assertNotIn("release has been created", lowered)
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\\\|/(?:home|users)/)", text))
        for prohibited in ("src-gm-", "src-lcr-", "src-pq-", "src-study-"):
            self.assertNotIn(prohibited, lowered)


if __name__ == "__main__":
    unittest.main()
