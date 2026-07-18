"""Cross-record assurance for the v0.5 provenance-register release source."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
README_PATH = REPOSITORY_ROOT / "README.md"
ROADMAP_PATH = REPOSITORY_ROOT / "ROADMAP.md"
SECURITY_PATH = REPOSITORY_ROOT / "SECURITY.md"
CURRENT_RELEASE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "CURRENT_RELEASE_STATUS.md"
DEPENDENCY_PATH = REPOSITORY_ROOT / "requirements.txt"


class V05ReleaseSourceAssuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.records = {record["capability_id"]: record for record in cls.ledger["capabilities"]}

    def test_release_source_identity_and_public_baseline_are_separate(self) -> None:
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        release_status = CURRENT_RELEASE_PATH.read_text(encoding="utf-8")
        self.assertIn("system_version: 0.5.0-release-source", manifest)
        self.assertIn("release-source `v0.5.0` content", readme)
        self.assertIn("historical public baseline", readme)
        self.assertIn("`v0.5.0` release-source", release_status)
        self.assertNotIn("v0.5.0 is released", "\n".join((manifest, readme, release_status)).lower())

    def test_release_source_capability_is_verified_admitted_but_not_released(self) -> None:
        record = self.records["GRW-CAP-050-01"]
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["version"]["target_release"], "v0.5.0")
        self.assertIn("Exact final-commit review", record["limitations_and_next_action"])

    def test_candidate_has_only_metadata_safe_interfaces(self) -> None:
        record = self.records["GRW-CAP-050-01"]
        for relative_path in record["interface"]["paths"]:
            self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)
        combined = "\n".join(
            (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")
            for relative_path in record["interface"]["paths"]
            if relative_path.endswith((".md", ".json", ".py"))
        )
        self.assertIn("metadata-only", combined.lower())
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\|/(?:home|users)/)", combined))
        self.assertIsNone(re.search(r"(?i)(password\s*[=:]|api[_-]?key\s*[=:]|authorization:\s*bearer)", combined))

    def test_roadmap_and_security_materials_describe_the_same_next_version(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
        security = SECURITY_PATH.read_text(encoding="utf-8")
        self.assertIn("`v0.5.0`: metadata-only provenance register set", readme)
        self.assertIn("`v0.6.0`: reviewable workflow and evidence controls", readme)
        self.assertIn("## v0.5.0 (release-source metadata-only provenance register set)", roadmap)
        self.assertIn("`v0.6.0`: reviewable workflow and evidence controls", roadmap)
        self.assertIn("`v0.4.x`", security)
        self.assertIn("v0.5.0 release-source tree", security)

    def test_direct_dependency_is_declared_and_not_claimed_as_locked_supply_chain(self) -> None:
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        requirements = DEPENDENCY_PATH.read_text(encoding="utf-8")
        self.assertIn("jsonschema==4.26.0", manifest)
        self.assertIn("jsonschema==4.26.0", requirements)
        policy = (REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "RELEASE_INTEGRITY_POLICY_v1.md").read_text(encoding="utf-8")
        self.assertIn("not hash-locked", policy)
        self.assertIn("M48 revalidation", policy)


if __name__ == "__main__":
    unittest.main()
