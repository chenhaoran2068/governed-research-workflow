"""Release-preparation checks for the local V1 interface-freeze candidate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"


class V1ReleasePreparationTests(unittest.TestCase):
    def test_required_v1_records_exist_and_do_not_claim_c4_or_release(self) -> None:
        names = (
            "V1_RELEASE_GATE.md",
            "V1_RELEASE_CONTROL_CANDIDATE.json",
            "V1_RELEASE_EVIDENCE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.0.0.md",
            "V1_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "RELEASE_NOTES_v1.0.0.md",
        )
        content = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in names)
        for name in names:
            self.assertTrue((RELEASE / name).is_file(), name)
        lowered = content.lower()
        self.assertIn("local c3", lowered)
        self.assertIn("commit-neutral", lowered)
        self.assertIn("does not", lowered)
        self.assertNotIn("v1.0.0 is published", lowered)
        self.assertNotIn("v1.0.0 is installed", lowered)
        self.assertNotIn("uncommitted candidate", lowered)

    def test_release_control_is_valid_and_keeps_exact_identity_and_c4_unresolved(self) -> None:
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE / "V1_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_reviewed")
        self.assertEqual(record["candidate_identity"]["candidate_version"], "1.0.0")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])
        self.assertEqual(record["material_reviews"]["public_material_rights_review"], "pass")
        self.assertEqual(record["material_reviews"]["private_material_secret_review"], "pass")
        self.assertEqual(record["dependency_and_source_authority"]["source_authority_review"], "pass")

    def test_v1_candidate_contract_has_no_new_operational_scope(self) -> None:
        gate = (RELEASE / "V1_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        notes = (RELEASE / "RELEASE_NOTES_v1.0.0.md").read_text(encoding="utf-8").lower()
        evidence = (RELEASE / "V1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        for phrase in (
            "no new research operation",
            "no data-content operation",
            "agent/runtime",
            "c4 authorization",
            "260 tests passed",
        ):
            self.assertIn(phrase, gate + "\n" + notes + "\n" + evidence)


if __name__ == "__main__":
    unittest.main()
