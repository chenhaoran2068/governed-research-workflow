"""Tests for the v0.7 read-only lesson-promotion control validator."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate_lesson_promotion_control_bundle.py"
FIXTURE_PATH = REPOSITORY_ROOT / "tests" / "fixtures" / "lesson_promotion_control_bundle" / "valid" / "bundle.json"
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "lesson_promotion_control_bundle.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "lesson-promotion-control-bundle.template.json"

spec = importlib.util.spec_from_file_location("lesson_promotion_validator", VALIDATOR_PATH)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class LessonPromotionControlBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        # macOS commonly exposes temporary directories through /var, a system link to
        # /private/var. The validator rightly requires a physical review root.
        self.root = Path(self.temp_dir.name).resolve()
        self.bundle_path = self.root / "bundle.json"
        shutil.copyfile(FIXTURE_PATH, self.bundle_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _bundle(self) -> dict:
        return json.loads(self.bundle_path.read_text(encoding="utf-8"))

    def _write(self, bundle: dict) -> None:
        self.bundle_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    def test_valid_synthetic_bundle_passes_without_writing_or_enumerating_root(self) -> None:
        sentinel = self.root / "unrelated-private-looking-sentinel.txt"
        sentinel.write_text("must not be read or changed", encoding="utf-8")
        before = sentinel.read_bytes()
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "valid")
        self.assertEqual(result["checked_record_count"], 7)
        self.assertEqual(sentinel.read_bytes(), before)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["bundle.json", sentinel.name])

    def test_schema_and_blank_metadata_only_template_validate(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(template))
        self.assertEqual(errors, [])
        self.assertEqual(template["schema_version"], "1.1.0")
        self.assertTrue(template["metadata_only"])
        self.assertFalse(template["restricted_content_included"])
        self.assertFalse(template["promotion_control"]["automated_promotion"])

    def test_automatic_promotion_is_refused_by_schema(self) -> None:
        bundle = self._bundle()
        bundle["promotion_control"]["automated_promotion"] = True
        self._write(bundle)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

    def test_integrated_candidate_requires_matching_verified_integration_record(self) -> None:
        bundle = self._bundle()
        for record in bundle["records"]:
            if record["record_id"] == "IV-001":
                record["integration_status"] = "not_verified"
        self._write(bundle)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "integration_not_verified" for issue in result["issues"]))

    def test_supersession_requires_visible_change_event(self) -> None:
        bundle = self._bundle()
        bundle["records"] = [record for record in bundle["records"] if record["record_id"] != "CE-001"]
        self._write(bundle)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "missing_supersession_event" for issue in result["issues"]))

    def test_unlinked_or_mismatched_control_records_are_refused(self) -> None:
        bundle = self._bundle()
        for record in bundle["records"]:
            if record["record_id"] == "IV-001":
                record["human_decision_id"] = "HD-000"
        self._write(bundle)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "integration_decision_mismatch" for issue in result["issues"]))

    def test_v11_correction_requires_separate_linked_human_decision(self) -> None:
        bundle = self._bundle()
        bundle["schema_version"] = "1.1.0"
        for record in bundle["records"]:
            if record["record_id"] == "LC-001":
                record["decision_history_ids"] = ["HD-001", "HD-002"]
            elif record["record_id"] == "LC-000":
                record["decision_history_ids"] = ["HD-000"]
        bundle["records"].extend([
            {
                "record_id": "HD-002",
                "record_type": "human_decision",
                "candidate_id": "LC-001",
                "disposition": "confirm_correction",
                "accountable_human_reference": "synthetic://accountable-human/correction-review",
                "decision_basis_references": ["synthetic://review/correction-basis"],
                "decision_date": "2026-07-19",
                "representation": "recorded_accountable_human_decision_not_identity_verified"
            },
            {
                "record_id": "CE-002",
                "record_type": "change_event",
                "candidate_id": "LC-001",
                "human_decision_id": "HD-002",
                "change_type": "correction",
                "reason": "Synthetic correction with separate human review.",
                "successor_candidate_id": None,
                "event_date": "2026-07-19"
            }
        ])
        self._write(bundle)
        self.assertEqual(validator.validate_bundle(self.root, "bundle.json")["result"], "valid")

        missing_history = deepcopy(bundle)
        for record in missing_history["records"]:
            if record["record_id"] == "LC-001":
                record.pop("decision_history_ids")
        self._write(missing_history)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "missing_decision_history" for issue in result["issues"]))

        unlinked_correction = deepcopy(bundle)
        for record in unlinked_correction["records"]:
            if record["record_id"] == "LC-001":
                record["decision_history_ids"] = ["HD-001"]
        self._write(unlinked_correction)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "correction_decision_not_in_history" for issue in result["issues"]))

        missing_event_date = deepcopy(bundle)
        for record in missing_event_date["records"]:
            if record["record_id"] == "CE-002":
                record.pop("event_date")
        self._write(missing_event_date)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "missing_correction_event_date" for issue in result["issues"]))

        reused_original_decision = deepcopy(bundle)
        for record in reused_original_decision["records"]:
            if record["record_id"] == "CE-002":
                record["human_decision_id"] = "HD-001"
        self._write(reused_original_decision)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "correction_disposition_mismatch" for issue in result["issues"]))

        missing_correction_event = deepcopy(bundle)
        missing_correction_event["records"] = [record for record in missing_correction_event["records"] if record["record_id"] != "CE-002"]
        self._write(missing_correction_event)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "missing_correction_event_for_decision" for issue in result["issues"]))

    def test_v10_rejects_v11_only_correction_fields(self) -> None:
        bundle = self._bundle()

        decision_history = deepcopy(bundle)
        for record in decision_history["records"]:
            if record["record_id"] == "LC-001":
                record["decision_history_ids"] = ["HD-001"]
        self._write(decision_history)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

        correction_disposition = deepcopy(bundle)
        for record in correction_disposition["records"]:
            if record["record_id"] == "HD-001":
                record["disposition"] = "confirm_correction"
        self._write(correction_disposition)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

        event_date = deepcopy(bundle)
        for record in event_date["records"]:
            if record["record_id"] == "CE-001":
                record["event_date"] = "2026-07-19"
        self._write(event_date)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

    def test_root_with_symbolic_link_ancestor_is_refused_when_supported(self) -> None:
        actual_parent = self.root / "actual-parent"
        physical_root = actual_parent / "review-root"
        physical_root.mkdir(parents=True)
        shutil.copyfile(FIXTURE_PATH, physical_root / "bundle.json")
        linked_parent = self.root / "linked-parent"
        try:
            linked_parent.symlink_to(actual_parent, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic-link creation unavailable: {error}")
        try:
            result = validator.validate_bundle(linked_parent / "review-root", "bundle.json")
            self.assertEqual(result["result"], "invalid")
            self.assertTrue(any(issue["code"] == "unsafe_root_path" for issue in result["issues"]))
        finally:
            if linked_parent.exists() or linked_parent.is_symlink():
                linked_parent.unlink()

    def test_supersession_cycle_is_refused(self) -> None:
        bundle = self._bundle()
        for record in bundle["records"]:
            if record["record_id"] == "LC-001":
                record["lifecycle_status"] = "superseded"
                record["human_decision_id"] = "HD-002"
                record["integration_verification_id"] = None
                record["superseded_by_candidate_id"] = "LC-000"
            if record["record_id"] == "HD-001":
                record["disposition"] = "supersede"
        bundle["records"].extend([
            {
                "record_id": "HD-002",
                "record_type": "human_decision",
                "candidate_id": "LC-001",
                "disposition": "supersede",
                "accountable_human_reference": "synthetic://accountable-human/reference",
                "decision_basis_references": ["synthetic://review/basis"],
                "decision_date": "2026-07-19",
                "representation": "recorded_accountable_human_decision_not_identity_verified"
            },
            {
                "record_id": "CE-002",
                "record_type": "change_event",
                "candidate_id": "LC-001",
                "human_decision_id": "HD-002",
                "change_type": "supersession",
                "reason": "Synthetic cyclic replacement for refusal coverage.",
                "successor_candidate_id": "LC-000"
            }
        ])
        self._write(bundle)
        result = validator.validate_bundle(self.root, "bundle.json")
        self.assertEqual(result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "supersession_cycle" for issue in result["issues"]))

    def test_duplicate_json_keys_and_path_traversal_are_refused(self) -> None:
        self.bundle_path.write_text('{"schema_version":"1.0.0","schema_version":"1.0.0"}', encoding="utf-8")
        duplicate_result = validator.validate_bundle(self.root, "bundle.json")
        traversal_result = validator.validate_bundle(self.root, "../bundle.json")
        self.assertEqual(duplicate_result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "duplicate_json_key" for issue in duplicate_result["issues"]))
        self.assertEqual(traversal_result["result"], "invalid")
        self.assertTrue(any(issue["code"] == "unsafe_input_path" for issue in traversal_result["issues"]))

    def test_symbolic_link_input_is_refused_when_the_platform_permits_it(self) -> None:
        outside = Path(self.temp_dir.name).parent / f"lesson-promotion-outside-{os.getpid()}.json"
        outside.write_text(FIXTURE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        link = self.root / "linked.json"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"symbolic-link creation unavailable: {error}")
        try:
            result = validator.validate_bundle(self.root, "linked.json")
            self.assertEqual(result["result"], "invalid")
            self.assertTrue(any(issue["code"] == "unsafe_input_path" for issue in result["issues"]))
        finally:
            if link.exists() or link.is_symlink():
                link.unlink()
            if outside.exists():
                outside.unlink()

    def test_cli_returns_structured_valid_result(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--root", str(self.root), "--bundle", "bundle.json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["result"], "valid")


if __name__ == "__main__":
    unittest.main()
