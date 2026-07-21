"""Public-profile boundary tests retained by later release sources."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
ROLE_DIRECTORY = REPOSITORY_ROOT / "system" / "08_agent_contracts" / "role_contracts"
HELPER_RECORD_PATH = REPOSITORY_ROOT / "system" / "07_tools_and_integrations" / "bootstrap_empty_workspace_helper_admission.json"
REFERENCE_PATH = REPOSITORY_ROOT / "references" / "role-contracts.md"
README_PATH = REPOSITORY_ROOT / "README.md"
PRIVATE_PATH_PATTERN = r"(?i)(?:[a-z]:\\|/(?:home|users)/)"


class V08ProfileContractTests(unittest.TestCase):
    def test_manifest_retains_exactly_two_public_profiles_and_no_service(self) -> None:
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn("system_version: 0.10.1", manifest)
        self.assertEqual(re.findall(r"^  - ([a-z_]+)$", manifest, flags=re.MULTILINE), ["standalone", "framework_integrated"])
        self.assertIn("optional_shared_services: []", manifest)
        self.assertNotIn("private_lab_extended", manifest.lower())
        self.assertIsNone(re.search(PRIVATE_PATH_PATTERN, manifest))

    def test_role_and_helper_records_only_name_public_profiles(self) -> None:
        records = [json.loads(path.read_text(encoding="utf-8")) for path in ROLE_DIRECTORY.glob("*.json")]
        records.append(json.loads(HELPER_RECORD_PATH.read_text(encoding="utf-8")))
        for record in records:
            profiles = record["compatibility"]["supported_profiles"] if "compatibility" in record and "supported_profiles" in record["compatibility"] else record["supported_profiles"]
            self.assertEqual(set(profiles), {"standalone", "framework_integrated"})
            self.assertNotIn("private_lab_extended", profiles)

    def test_private_lab_extended_is_explicitly_excluded_from_public_support(self) -> None:
        reference = REFERENCE_PATH.read_text(encoding="utf-8").lower()
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("not a runnable agent", reference)
        self.assertIn("cannot replace", reference)
        self.assertIn("Private Lab Extended category is a private", readme)
        self.assertIn("not a v0.8 public profile", readme)


if __name__ == "__main__":
    unittest.main()
