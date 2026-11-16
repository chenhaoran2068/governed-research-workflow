"""Bounded System compatibility checks for Framework v0.6.0."""

from __future__ import annotations

import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK_TAG = "v0.6.0"
FRAMEWORK_COMMIT = "9793445a00764c4465a6292a928f50d29a71731b"


class V1212FrameworkCompatibilityTests(unittest.TestCase):
    def test_manifest_and_ci_pin_exact_framework_identity(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "test-bootstrap.yml").read_text(encoding="utf-8")
        self.assertIn("system_version: 1.21.2", manifest)
        self.assertIn('supported_framework_versions: "0.6.0"', manifest)
        self.assertIn("exact Framework v0.6.0 contract", manifest)
        self.assertIn(f"FRAMEWORK_RELEASE_TAG: {FRAMEWORK_TAG}", workflow)
        self.assertIn(f"FRAMEWORK_EXPECTED_COMMIT: {FRAMEWORK_COMMIT}", workflow)
        self.assertIn(f"ref: {FRAMEWORK_COMMIT}", workflow)

    def test_system_does_not_invoke_or_own_the_framework_audit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        release_notes = (
            ROOT / "system" / "11_distribution_installation_and_release" / "RELEASE_NOTES_v1.21.2.md"
        ).read_text(encoding="utf-8").lower()
        self.assertNotIn("audit_workspace_placement", skill)
        self.assertIn("does not invoke the framework audit", release_notes)
        self.assertIn("does not add a system capability", release_notes)

    def test_optional_framework_audit_assets_exist_only_in_caller_named_framework_checkout(self) -> None:
        framework_root = os.environ.get("FRAMEWORK_REPOSITORY_ROOT")
        framework_tag = os.environ.get("FRAMEWORK_RELEASE_TAG")
        framework_commit = os.environ.get("FRAMEWORK_EXPECTED_COMMIT")
        if not (framework_root and framework_tag and framework_commit):
            self.skipTest("Exact Framework integration environment is not configured.")
        root = Path(framework_root)
        self.assertEqual(framework_tag, FRAMEWORK_TAG)
        self.assertEqual(framework_commit, FRAMEWORK_COMMIT)
        self.assertTrue((root / "scripts" / "audit_workspace_placement.py").is_file())
        self.assertTrue((root / "docs" / "workspace_placement_integrity_audit_contract_v1.md").is_file())


if __name__ == "__main__":
    unittest.main()
