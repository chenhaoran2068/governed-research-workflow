"""Tests for the v0.9 metadata-only integrity-audit bundle validator."""

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
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate_integrity_audit_bundle.py"
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "system"
    / "09_schemas_records_and_templates"
    / "integrity_audit_bundle.schema.json"
)
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "integrity-audit-bundle.template.json"
FIXTURE_PATH = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "integrity_audit_bundle"
    / "valid"
    / "bundle.json"
)

spec = importlib.util.spec_from_file_location("integrity_audit_validator", VALIDATOR_PATH)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class IntegrityAuditBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        self.bundle_path = self.root / "bundle.json"
        shutil.copyfile(FIXTURE_PATH, self.bundle_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _bundle(self) -> dict:
        return json.loads(self.bundle_path.read_text(encoding="utf-8"))

    def _write(self, bundle: dict) -> None:
        self.bundle_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    def _result(self) -> dict:
        return validator.validate_bundle_path(self.bundle_path)

    def _closed_link(self, bundle: dict) -> dict:
        bundle["audit_findings"][0]["status"] = "closed"
        bundle["correction_reassessment_links"] = [
            {
                "link_id": "CORRECTION_LINK",
                "prior_finding_id": "FINDING_LIMITATION",
                "prior_affected_identity": "synthetic declared identity set",
                "human_disposition_reference": "synthetic-human-disposition-reference",
                "later_changed_identity": "synthetic corrected identity",
                "allowed_write_scope_reference": "synthetic allowed write scope",
                "direct_downstream_references": ["synthetic downstream review"],
                "prior_evidence_limited": True,
                "required_reruns": ["synthetic structural re-review"],
                "skipped_checks": [],
                "residual_risks": ["No hosted or human verification is established."],
                "latest_rereview_outcome": "reviewed"
            }
        ]
        return bundle

    def test_valid_synthetic_bundle_passes_without_reading_or_writing_sibling(self) -> None:
        sentinel = self.root / "unlisted-sentinel.txt"
        sentinel.write_text("must remain unchanged", encoding="utf-8")
        before = sentinel.read_bytes()

        result = self._result()

        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["bundle_id"], "SYNTHETIC_AUDIT_BUNDLE")
        self.assertEqual(result["issues"], [])
        self.assertEqual(sentinel.read_bytes(), before)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["bundle.json", sentinel.name])

    def test_schema_and_template_are_structurally_valid(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(template))
        self.assertEqual(errors, [])
        self.assertTrue(template["metadata_only"])
        self.assertFalse(template["restricted_content_included"])
        self.assertEqual(len(template["explicit_non_claims"]), 7)
        self.assertEqual(template["audit_harness"]["evaluation_variability"], "deterministic")
        self.assertEqual(template["audit_harness"]["attempt_budget"]["status"], "not_applicable")

    def test_incomplete_root_non_claims_are_refused(self) -> None:
        bundle = self._bundle()
        bundle["explicit_non_claims"].pop()
        self._write(bundle)

        result = self._result()

        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

    def test_identifier_reuse_across_record_classes_is_refused(self) -> None:
        bundle = self._bundle()
        bundle["audit_findings"][0]["finding_id"] = "OBS_RELEASE"
        self._write(bundle)

        result = self._result()

        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "duplicate_record_id" for issue in result["issues"]))

    def test_declared_input_set_must_match_observations_and_harness(self) -> None:
        bundle = self._bundle()
        bundle["audit_scope"]["declared_input_record_ids"] = ["OBS_RELEASE", "HARNESS_AUDIT"]
        self._write(bundle)

        result = self._result()

        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "declared_input_mismatch" for issue in result["issues"]))

    def test_stop_required_label_requires_stop(self) -> None:
        bundle = self._bundle()
        bundle["audit_findings"][0]["finding_class"] = "stop_required"
        bundle["audit_findings"][0]["stop_required"] = False
        self._write(bundle)

        result = self._result()

        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "inconsistent_stop_requirement" for issue in result["issues"]))

    def test_harness_identity_validity_and_variable_budget_are_bound(self) -> None:
        checker_mismatch = self._bundle()
        checker_mismatch["audit_harness"]["checker_version"] = "2.0.0"
        self._write(checker_mismatch)
        mismatch = self._result()
        self.assertEqual(mismatch["status"], "invalid")
        self.assertTrue(any(issue["code"] == "checker_identity_mismatch" for issue in mismatch["issues"]))

        invalid_pass = self._bundle()
        invalid_pass["audit_harness"]["validity_status"] = "not_assessed"
        self._write(invalid_pass)
        invalid_result = self._result()
        self.assertEqual(invalid_result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "unreliable_passed_harness" for issue in invalid_result["issues"]))

        unbounded_variable = self._bundle()
        unbounded_variable["audit_harness"]["evaluation_variability"] = "variable"
        unbounded_variable["audit_harness"]["attempt_budget"] = {
            "status": "not_applicable",
            "maximum_attempts": None,
        }
        self._write(unbounded_variable)
        budget_result = self._result()
        self.assertEqual(budget_result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in budget_result["issues"]))

    def test_closed_finding_needs_linked_reassessment_and_matching_identity(self) -> None:
        closed_without_link = self._bundle()
        closed_without_link["audit_findings"][0]["status"] = "closed"
        self._write(closed_without_link)
        missing_link = self._result()
        self.assertEqual(missing_link["status"], "invalid")
        self.assertTrue(any(issue["code"] == "closed_finding_without_rereview" for issue in missing_link["issues"]))

        valid_closure = self._closed_link(self._bundle())
        self._write(valid_closure)
        self.assertEqual(self._result()["status"], "valid")

        mismatched_identity = deepcopy(valid_closure)
        mismatched_identity["correction_reassessment_links"][0]["prior_affected_identity"] = "other identity"
        self._write(mismatched_identity)
        mismatch = self._result()
        self.assertEqual(mismatch["status"], "invalid")
        self.assertTrue(any(issue["code"] == "affected_identity_mismatch" for issue in mismatch["issues"]))

    def test_unsafe_worktree_preflight_dispositions_are_refused(self) -> None:
        active_with_maintenance = self._bundle()
        active_with_maintenance["operational_integrity_records"][1]["recovery_disposition"] = "preflight_only"
        self._write(active_with_maintenance)
        active_result = self._result()
        self.assertEqual(active_result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "unsafe_worktree_recovery_disposition" for issue in active_result["issues"]))

        prunable_but_present = self._bundle()
        record = prunable_but_present["operational_integrity_records"][1]
        record["worktree_listed_state"] = "prunable"
        record["recovery_disposition"] = "separately_authorized_maintenance"
        record["physical_worktree_state"] = "present"
        self._write(prunable_but_present)
        prunable_result = self._result()
        self.assertEqual(prunable_result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "incomplete_worktree_preflight" for issue in prunable_result["issues"]))

    def test_operational_records_cannot_omit_receipt_or_worktree_preflight_limits(self) -> None:
        bundle = self._bundle()
        bundle["operational_integrity_records"][0]["does_not_establish_later_installation"] = False
        self._write(bundle)
        result = self._result()
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

        missing_worktree_context = self._bundle()
        missing_worktree_context["operational_integrity_records"][1].pop("worktree_changes_state")
        self._write(missing_worktree_context)
        result = self._result()
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(issue["code"] == "schema_validation" for issue in result["issues"]))

    def test_duplicate_json_keys_and_relative_path_are_refused(self) -> None:
        self.bundle_path.write_text(
            '{"schema_version":"1.0.0","schema_version":"1.0.0"}',
            encoding="utf-8",
        )
        duplicate_result = self._result()
        relative_result = validator.validate_bundle_path(Path("bundle.json"))

        self.assertEqual(duplicate_result["status"], "not_assessed")
        self.assertTrue(any(issue["code"] == "duplicate_json_key" for issue in duplicate_result["issues"]))
        self.assertEqual(relative_result["status"], "not_assessed")
        self.assertTrue(any(issue["code"] == "unsafe_bundle_path" for issue in relative_result["issues"]))

    def test_symbolic_link_input_is_refused_when_supported(self) -> None:
        outside = self.root.parent / f"integrity-audit-outside-{os.getpid()}.json"
        shutil.copyfile(FIXTURE_PATH, outside)
        linked = self.root / "linked.json"
        try:
            linked.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"symbolic-link creation unavailable: {error}")
        try:
            result = validator.validate_bundle_path(linked)
            self.assertEqual(result["status"], "not_assessed")
            self.assertTrue(any(issue["code"] == "unsafe_bundle_path" for issue in result["issues"]))
        finally:
            if linked.exists() or linked.is_symlink():
                linked.unlink()
            if outside.exists():
                outside.unlink()

    def test_cli_reports_only_structured_result(self) -> None:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--bundle", str(self.bundle_path)],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "valid")
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
