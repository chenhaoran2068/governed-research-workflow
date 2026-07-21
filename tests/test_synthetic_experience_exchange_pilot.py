"""Synthetic tests for the self-controlled exchange-pilot receipt validator."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "synthetic_experience_exchange_pilot" / "valid"
SCHEMA = ROOT / "system" / "09_schemas_records_and_templates" / "synthetic_experience_exchange_pilot_receipt.schema.json"
TEMPLATE = ROOT / "assets" / "synthetic-experience-exchange-pilot-receipt.template.json"
SCRIPT = ROOT / "scripts" / "validate_synthetic_experience_exchange_pilot.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_synthetic_experience_exchange_pilot", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module()


class SyntheticExperienceExchangePilotTests(TestCase):
    def copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        destination = Path(temporary_directory.name) / "pilot"
        shutil.copytree(FIXTURE, destination)
        return temporary_directory, destination

    @staticmethod
    def load_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def write_json(path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def receipt_path(root: Path) -> Path:
        return root / "exchange-pilot-receipt.json"

    def assert_result(self, result: dict, expected: str, code: str | None = None) -> None:
        self.assertEqual(result["result"], expected)
        if code:
            self.assertIn(code, {issue["code"] for issue in result["issues"]})

    def refresh_receipt_hash(self, root: Path) -> None:
        receipt_path = self.receipt_path(root)
        receipt = self.load_json(receipt_path)
        manifest_path = root / receipt["package_manifest_path"]
        manifest = self.load_json(manifest_path)
        paths, issue = VALIDATOR._package_paths(manifest_path, manifest)
        self.assertIsNone(issue)
        assert paths is not None
        receipt["package_tree_sha256"] = VALIDATOR._package_tree_hash(paths)
        self.write_json(receipt_path, receipt)

    def test_schema_and_template_are_valid(self) -> None:
        schema = self.load_json(SCHEMA)
        Draft202012Validator.check_schema(schema)
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(self.load_json(TEMPLATE))), [])

    def test_valid_synthetic_pilot_is_structurally_valid(self) -> None:
        result = VALIDATOR.validate_exchange_pilot(self.receipt_path(FIXTURE))
        self.assert_result(result, "structurally_valid")
        self.assertEqual(result["checked_record_count"], 6)
        self.assertEqual(result["package_tree_sha256"], "228e8d73a57e08ca0350f63cc67e01af8e7534e585174cec4cf4820de692fce0")

    def test_refuses_receipt_path_escape_and_linked_root(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        receipt_path = self.receipt_path(root)
        receipt = self.load_json(receipt_path)
        receipt["package_manifest_path"] = "../outside.json"
        self.write_json(receipt_path, receipt)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "refused_boundary", "refused_boundary")
        receipt["package_manifest_path"] = "experience-package.json"
        self.write_json(receipt_path, receipt)
        linked = root.parent / "linked-pilot"
        try:
            linked.symlink_to(root, target_is_directory=True)
        except OSError:
            self.skipTest("symbolic-link creation is unavailable in this environment")
        self.assert_result(VALIDATOR.validate_exchange_pilot(linked / "exchange-pilot-receipt.json"), "refused_boundary", "refused_boundary")

    def test_rejects_identity_revision_and_hash_mismatches(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        receipt_path = self.receipt_path(root)
        receipt = self.load_json(receipt_path)
        receipt["package_id"] = "OTHER_PACKAGE"
        self.write_json(receipt_path, receipt)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_invalid", "package_identity_mismatch")
        receipt["package_id"] = "SYNTHETIC_EXPERIENCE_PACKAGE"
        receipt["package_revision"] = 2
        self.write_json(receipt_path, receipt)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_invalid", "package_revision_mismatch")
        receipt["package_revision"] = 1
        receipt["package_tree_sha256"] = "0" * 64
        self.write_json(receipt_path, receipt)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_invalid", "package_hash_mismatch")

    def test_correction_and_future_use_links_must_remain_consistent(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        correction_path = root / "records" / "correction-or-withdrawal.json"
        correction = self.load_json(correction_path)
        correction.update(
            {
                "request_state": "human_disposition_recorded",
                "requested_action": "correction",
                "accountable_human_decision_reference": "SYNTHETIC_HUMAN_DECISION",
                "future_use_state": "not_requested",
            }
        )
        self.write_json(correction_path, correction)
        receipt_path = self.receipt_path(root)
        receipt = self.load_json(receipt_path)
        receipt.update(
            {
                "declared_correction_or_withdrawal_state": "human_disposition_recorded",
                "future_governed_use_state": "not_requested",
            }
        )
        self.write_json(receipt_path, receipt)
        self.refresh_receipt_hash(root)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_valid")

        receipt = self.load_json(receipt_path)
        receipt["future_governed_use_state"] = "stopped_after_human_decision"
        self.write_json(receipt_path, receipt)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_invalid", "future_use_state_mismatch")

        correction.update(
            {
                "request_state": "future_use_stopped",
                "requested_action": "withdrawal",
                "future_use_state": "stopped_after_human_decision",
            }
        )
        self.write_json(correction_path, correction)
        receipt = self.load_json(receipt_path)
        receipt.update(
            {
                "declared_correction_or_withdrawal_state": "future_use_stopped",
                "future_governed_use_state": "stopped_after_human_decision",
            }
        )
        self.write_json(receipt_path, receipt)
        self.refresh_receipt_hash(root)
        self.assert_result(VALIDATOR.validate_exchange_pilot(receipt_path), "structurally_valid")

    def test_unlisted_content_is_not_discovered_or_hashed_and_no_write_occurs(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        baseline = VALIDATOR.validate_exchange_pilot(self.receipt_path(root))
        before = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}
        (root / "unlisted.txt").write_text("synthetic unlisted content", encoding="utf-8")
        result = VALIDATOR.validate_exchange_pilot(self.receipt_path(root))
        after = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file() and path.name != "unlisted.txt"}
        self.assert_result(result, "structurally_valid")
        self.assertEqual(result["package_tree_sha256"], baseline["package_tree_sha256"])
        self.assertEqual(before, after)
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("iterdir", source)
        self.assertNotIn("rglob", source)

    def test_crlf_checkout_does_not_change_the_declared_json_hash(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        baseline = VALIDATOR.validate_exchange_pilot(self.receipt_path(root))
        for path in root.rglob("*.json"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        result = VALIDATOR.validate_exchange_pilot(self.receipt_path(root))
        self.assert_result(result, "structurally_valid")
        self.assertEqual(result["package_tree_sha256"], baseline["package_tree_sha256"])

    def test_dependency_failure_is_not_misreported_as_invalid(self) -> None:
        issue = VALIDATOR.ValidationIssue("not_assessed_dependency", "Synthetic dependency absence.")
        self.assertEqual(VALIDATOR._schema_issue_status([issue]), "not_assessed")


if __name__ == "__main__":
    main()
