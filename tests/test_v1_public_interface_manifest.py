"""Structural checks for the frozen V1 public interface manifest."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_public_interface_manifest.json"
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "v1_public_interface_manifest.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"

EXPECTED_MODULE_IDS = {f"{index:02d}" for index in range(13)}
EXPECTED_INTERFACES = {
    "profile_contract",
    "task_routing",
    "empty_workspace_bootstrap",
    "workflow_guidance",
    "evidence_guidance",
    "provenance_records",
    "learning_records",
    "helper_admission_boundary",
    "role_contracts",
    "schemas_and_templates",
    "assurance_and_audit",
    "distribution_and_release_controls",
    "synthetic_examples",
}


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return (
        not normalized.startswith("/")
        and not re.match(r"^[A-Za-z]:", normalized)
        and ".." not in PurePosixPath(normalized).parts
    )


class V1PublicInterfaceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_manifest_validates_and_uses_time_neutral_identity(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.manifest))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.manifest["contract_version"], "1.0.0")
        self.assertEqual(self.manifest["contract_status"], "interface_frozen")
        self.assertEqual(self.manifest["source_identity"]["source_version"], "1.0.0")
        self.assertEqual(self.manifest["source_identity"]["historical_public_baseline"], "v0.13.0")
        rule = self.manifest["source_identity"]["public_release_identity_rule"]
        self.assertIn("exact annotated", rule)
        self.assertIn("matching GitHub Release", rule)
        self.assertIn("does not itself prove", rule)

    def test_interface_inventory_is_complete_and_resolves_to_existing_files(self) -> None:
        interfaces = self.manifest["interfaces"]
        self.assertEqual({item["interface_id"] for item in interfaces}, EXPECTED_INTERFACES)
        self.assertEqual(len(interfaces), len({item["interface_id"] for item in interfaces}))
        self.assertEqual(
            {module_id for item in interfaces for module_id in item["module_ids"]},
            EXPECTED_MODULE_IDS,
        )
        ledger_ids = {record["capability_id"] for record in self.ledger["capabilities"]}
        for item in interfaces:
            for path in item["paths"]:
                self.assertTrue(is_safe_relative_path(path), path)
                self.assertTrue((ROOT / path).is_file(), path)
            self.assertTrue(set(item["capability_ids"]).issubset(ledger_ids))
            self.assertTrue(item["promise"])
            self.assertTrue(item["non_promise"])

    def test_effect_boundary_has_exactly_one_controlled_write_interface(self) -> None:
        writers = [
            item for item in self.manifest["interfaces"]
            if item["effect"] == "controlled_empty_write"
        ]
        self.assertEqual([item["interface_id"] for item in writers], ["empty_workspace_bootstrap"])
        self.assertEqual(
            writers[0]["paths"][0],
            "scripts/bootstrap_empty_workspace.py",
        )
        self.assertFalse(any(
            item["effect"] == "controlled_empty_write"
            for item in self.manifest["interfaces"]
            if item["interface_id"] != "empty_workspace_bootstrap"
        ))

    def test_global_non_promises_retain_execution_and_authority_boundaries(self) -> None:
        text = "\n".join(self.manifest["global_non_promises"]).lower()
        for phrase in (
            "real-data handling",
            "agent runtime",
            "multi-agent orchestration",
            "generic writer",
            "installed-runtime",
            "project-decision",
        ):
            self.assertIn(phrase, text)

    def test_schema_refuses_unsafe_path_and_extra_interface(self) -> None:
        unsafe = copy.deepcopy(self.manifest)
        unsafe["interfaces"][0]["paths"][0] = "../outside.md"
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(unsafe)))

        extra = copy.deepcopy(self.manifest)
        extra["interfaces"].append(copy.deepcopy(extra["interfaces"][0]))
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(extra)))


if __name__ == "__main__":
    unittest.main()
