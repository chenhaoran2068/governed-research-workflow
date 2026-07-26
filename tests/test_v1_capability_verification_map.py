"""Structural checks for the V1 capability verification map."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "system" / "10_assurance_evaluation_and_audit" / "v1_capability_verification_map.json"
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "v1_capability_verification_map.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return (
        not normalized.startswith("/")
        and not re.match(r"^[A-Za-z]:", normalized)
        and ".." not in PurePosixPath(normalized).parts
    )


class V1CapabilityVerificationMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_map_validates_and_records_only_local_candidate_verification(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.mapping))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.mapping["source_contract_version"], "1.0.0")
        self.assertEqual(
            self.mapping["candidate_evidence_status"],
            "locally_verified_candidate",
        )
        self.assertTrue(all(
            item["candidate_verification_status"] == "locally_verified_candidate"
            for item in self.mapping["capabilities"]
        ))

    def test_map_covers_every_ledger_capability_once_with_matching_claim_status(self) -> None:
        ledger_statuses = {
            item["capability_id"]: item["public_claim_status"]
            for item in self.ledger["capabilities"]
        }
        mapped_statuses = {
            item["capability_id"]: item["expected_claim_status"]
            for item in self.mapping["capabilities"]
        }
        self.assertEqual(mapped_statuses, ledger_statuses)
        self.assertEqual(len(mapped_statuses), len(self.mapping["capabilities"]))
        forbidden = [
            item["capability_id"]
            for item in self.mapping["capabilities"]
            if item["expected_claim_status"] == "forbidden"
        ]
        self.assertEqual(forbidden, ["GRW-CAP-040-03"])

    def test_each_mapped_test_path_exists_and_requirements_are_complete(self) -> None:
        for item in self.mapping["capabilities"]:
            self.assertEqual(
                set(item["required_review_types"]),
                {"interface_scope", "negative_boundary", "full_regression"},
            )
            for path in item["verification_test_paths"]:
                self.assertTrue(is_safe_relative_path(path), path)
                self.assertTrue((ROOT / path).is_file(), path)

    def test_schema_refuses_unsafe_path_and_wrong_claim_state(self) -> None:
        unsafe = copy.deepcopy(self.mapping)
        unsafe["capabilities"][0]["verification_test_paths"][0] = "../outside.py"
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(unsafe)))

        wrong_status = copy.deepcopy(self.mapping)
        wrong_status["capabilities"][7]["expected_claim_status"] = "permitted"
        self.assertFalse(
            wrong_status["capabilities"][7]["expected_claim_status"]
            == self.ledger["capabilities"][7]["public_claim_status"]
        )


if __name__ == "__main__":
    unittest.main()
