"""Checks for the v1.1 candidate verification map and ledger alignment."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "system" / "10_assurance_evaluation_and_audit" / "v1_1_capability_verification_map.json"
SCHEMA_PATH = ROOT / "system" / "10_assurance_evaluation_and_audit" / "v1_1_capability_verification_map.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return not normalized.startswith("/") and not re.match(r"^[A-Za-z]:", normalized) and ".." not in PurePosixPath(normalized).parts


class V11CapabilityVerificationMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_locally_verified_candidate_map_validates_and_covers_current_ledger(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.mapping))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.mapping["source_contract_version"], "1.1.0")
        self.assertEqual(self.mapping["candidate_evidence_status"], "locally_verified_candidate")
        ledger_statuses = {item["capability_id"]: item["public_claim_status"] for item in self.ledger["capabilities"]}
        mapped_statuses = {item["capability_id"]: item["expected_claim_status"] for item in self.mapping["capabilities"]}
        self.assertEqual(mapped_statuses, ledger_statuses)
        self.assertEqual(len(mapped_statuses), 30)

    def test_new_capability_is_admitted_for_its_proposed_scope_but_not_released(self) -> None:
        record = next(item for item in self.mapping["capabilities"] if item["capability_id"] == "GRW-CAP-111-01")
        self.assertEqual(record["expected_claim_status"], "permitted")
        self.assertEqual(record["candidate_verification_status"], "locally_verified_candidate")
        self.assertEqual(set(record["required_review_types"]), {"interface_scope", "negative_boundary", "full_regression"})
        for item in self.mapping["capabilities"]:
            for path in item["verification_test_paths"]:
                self.assertTrue(is_safe_relative_path(path), path)
                self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
