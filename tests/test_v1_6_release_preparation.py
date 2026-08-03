"""Release-preparation checks for the v1.6 public derivative source scope."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V16ReleasePreparationTests(unittest.TestCase):
    def test_release_control_is_local_candidate_only(self) -> None:
        record = json.loads(
            (ROOT / "system" / "11_distribution_installation_and_release" / "V1_6_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["candidate_release_version"], "v1.6.0")
        self.assertEqual(record["status"], "local_candidate_only")
        self.assertEqual(record["capability_ids"], ["GRW-CAP-160-01"])
        self.assertEqual(record["public_baseline"]["annotated_tag"], "v1.5.2")
        self.assertEqual(record["public_baseline"]["commit"], "4f73a2fca5b998c9e37d811827f13d83418f6cba")
        self.assertIn("separate exact-main C4 authorization", record["required_gates"])
        self.assertIn("installed runtime", record["prohibited_claims"])

    def test_public_admission_and_boundary_do_not_make_release_or_authority_claims(self) -> None:
        admission = (ROOT / "system" / "11_distribution_installation_and_release" / "GRW_CAP_160_01_PUBLIC_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8").lower()
        boundary = (ROOT / "PUBLIC_BOUNDARY.md").read_text(encoding="utf-8").lower()
        for text in (admission, boundary):
            self.assertIn("does not", text)
        self.assertIn("does not grant access", admission)
        self.assertIn("does not automatically load", boundary)
        self.assertIn("does not itself prove", admission)

    def test_legacy_entrypoint_and_current_reference_are_aligned(self) -> None:
        legacy = (ROOT / "system" / "06_memory_and_learning" / "knowledge_governance_experience_collection" / "README.md").read_text(encoding="utf-8")
        reference = (ROOT / "references" / "knowledge-governance-experience-collection.md").read_text(encoding="utf-8")
        self.assertIn("Historical KGE Public Collection Entry Point", legacy)
        self.assertIn("public-safe-shared-experience-derivatives.md", legacy)
        self.assertIn("public-safe-shared-experience-derivatives.md", reference)
        self.assertIn("historical public identifiers", reference.lower())


if __name__ == "__main__":
    unittest.main()
