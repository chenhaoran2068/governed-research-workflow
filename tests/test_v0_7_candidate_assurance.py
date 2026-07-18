"""Candidate-scope assurance for v0.7 lesson-promotion controls."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tests.test_v0_4_synthetic_assurance import source_snapshot_sha256


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
ADMISSION_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_7_CAPABILITY_ADMISSION.md"
GATE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_7_RELEASE_GATE.md"
EVIDENCE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_7_RELEASE_EVIDENCE.md"
RIGHTS_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.7.0.md"
NOTES_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "RELEASE_NOTES_v0.7.0.md"
ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_7_SYNTHETIC_ASSURANCE.md"
ASSURANCE_RELATIVE_PATH = ASSURANCE_PATH.relative_to(REPOSITORY_ROOT).as_posix().encode("utf-8")


class V07CandidateAssuranceTests(unittest.TestCase):
    def test_candidate_scope_is_admitted_but_not_released_or_installed(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-070-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertIsNone(record["version"]["last_verified_release"])
        self.assertIn("not c4 publication authorization", ADMISSION_PATH.read_text(encoding="utf-8").lower())

    def test_candidate_interface_is_complete_and_has_no_private_path_claim(self) -> None:
        expected = (
            "system/09_schemas_records_and_templates/lesson_promotion_control_bundle.schema.json",
            "assets/lesson-promotion-control-bundle.template.json",
            "scripts/validate_lesson_promotion_control_bundle.py",
            "references/lesson-promotion-control-records.md",
            "tests/test_lesson_promotion_control_bundle.py",
        )
        for relative_path in expected:
            self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)
        source = "\n".join((REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8") for relative_path in expected if relative_path.endswith((".md", ".py", ".json")))
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\\\|/(?:home|users)/)", source))
        self.assertIn("metadata-only", source.lower())
        self.assertIn("does not", source.lower())

    def test_candidate_release_materials_keep_c4_and_runtime_boundaries(self) -> None:
        for path in (GATE_PATH, EVIDENCE_PATH, RIGHTS_PATH, NOTES_PATH):
            self.assertTrue(path.is_file(), path)
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in (GATE_PATH, EVIDENCE_PATH, RIGHTS_PATH, NOTES_PATH))
        self.assertIn("c4", combined)
        self.assertIn("not a public release", combined)
        self.assertIn("runtime", combined)
        self.assertNotIn("e:\\", combined)
        self.assertNotIn("c:\\users", combined)

    def test_staged_candidate_assurance_snapshot_matches_all_other_tracked_source(self) -> None:
        assurance = ASSURANCE_PATH.read_text(encoding="utf-8")
        match = re.search(r"source snapshot SHA-256: `([0-9a-f]{64})`", assurance)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), source_snapshot_sha256(ASSURANCE_RELATIVE_PATH))
        self.assertIn("excludes this file only", assurance)


if __name__ == "__main__":
    unittest.main()
