"""Structural checks for the v1.1 future-Study candidate interface manifest."""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_1_public_interface_manifest.json"
SCHEMA_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_1_public_interface_manifest.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
V1_LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return not normalized.startswith("/") and not re.match(r"^[A-Za-z]:", normalized) and ".." not in PurePosixPath(normalized).parts


class V11PublicInterfaceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_candidate_manifest_validates_and_is_not_a_release_claim(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.manifest))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.manifest["contract_version"], "1.1.0")
        self.assertEqual(self.manifest["contract_status"], "unreleased_candidate")
        rule = self.manifest["source_identity"]["public_release_identity_rule"]
        self.assertIn("unreleased", rule)
        self.assertIn("exact annotated", rule)
        self.assertIn("matching GitHub Release", rule)

    def test_inventory_contains_one_new_interface_and_one_writer(self) -> None:
        interfaces = self.manifest["interfaces"]
        identifiers = {item["interface_id"] for item in interfaces}
        self.assertEqual(len(interfaces), 14)
        self.assertIn("future_study_execution_contract", identifiers)
        self.assertEqual({module for item in interfaces for module in item["module_ids"]}, {f"{index:02d}" for index in range(13)})
        ledger_ids = {item["capability_id"] for item in self.ledger["capabilities"]}
        for interface in interfaces:
            self.assertTrue(set(interface["capability_ids"]).issubset(ledger_ids))
            for path in interface["paths"]:
                self.assertTrue(is_safe_relative_path(path), path)
                self.assertTrue((ROOT / path).is_file(), path)
        writers = [item["interface_id"] for item in interfaces if item["effect"] == "controlled_empty_write"]
        self.assertEqual(writers, ["empty_workspace_bootstrap"])

    def test_frozen_v1_ledger_is_byte_identical_to_the_immutable_tag(self) -> None:
        expected = subprocess.run(
            ["git", "show", "v1.0.0:system/00_manifest_and_profiles/capability_truth_ledger.json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected.returncode, 0, expected.stderr)
        snapshot = V1_LEDGER_PATH.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        self.assertEqual(snapshot, expected.stdout.encode("utf-8"))
        self.assertNotIn("GRW-CAP-111-01", V1_LEDGER_PATH.read_text(encoding="utf-8"))
        self.assertIn("GRW-CAP-111-01", LEDGER_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
