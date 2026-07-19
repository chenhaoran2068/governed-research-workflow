"""Synthetic assurance for the metadata-only v0.6 workflow/evidence bundle."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPOSITORY_ROOT / "tests" / "fixtures" / "workflow_evidence_control_bundle"
VALID_FIXTURE = FIXTURE_ROOT / "valid"
BUNDLE_SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "workflow_evidence_control_bundle.schema.json"
BASELINE_SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "workflow_evidence_control_baseline.schema.json"
BUNDLE_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "workflow-evidence-control-bundle.template.json"
BASELINE_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "workflow-evidence-control-baseline.template.json"
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "validate_workflow_evidence_control_bundle.py"
REQUIREMENTS_PATH = REPOSITORY_ROOT / "requirements.txt"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_workflow_evidence_control_bundle", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR_MODULE = _load_validator_module()


class WorkflowEvidenceControlBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle_schema = json.loads(BUNDLE_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.baseline_schema = json.loads(BASELINE_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.bundle_schema)
        Draft202012Validator.check_schema(cls.baseline_schema)
        cls.bundle_validator = Draft202012Validator(cls.bundle_schema, format_checker=FormatChecker())
        cls.baseline_validator = Draft202012Validator(cls.baseline_schema, format_checker=FormatChecker())

    def copy_valid_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        root = Path(temporary_directory.name).resolve() / "workflow-evidence"
        shutil.copytree(VALID_FIXTURE, root)
        return temporary_directory, root

    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, content: dict) -> None:
        path.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")

    def validate(self, root: Path, baseline: bool = False) -> dict:
        return VALIDATOR_MODULE.validate_bundle(root, "bundle.json", "baseline.json" if baseline else None)

    def assert_issue(self, result: dict, expected_code: str) -> None:
        self.assertEqual(result["result"], "invalid", result)
        self.assertIn(expected_code, {issue["code"] for issue in result["issues"]})

    def test_schemas_and_blank_templates_are_valid(self) -> None:
        bundle_template = self.load_json(BUNDLE_TEMPLATE_PATH)
        baseline_template = self.load_json(BASELINE_TEMPLATE_PATH)
        self.assertEqual(list(self.bundle_validator.iter_errors(bundle_template)), [])
        self.assertEqual(list(self.baseline_validator.iter_errors(baseline_template)), [])
        self.assertTrue(bundle_template["metadata_only"])
        self.assertEqual(bundle_template["records"], [])
        self.assertEqual(len(bundle_template["record_contract"]["allowed_record_types"]), 6)

    def test_valid_six_record_bundle_matches_its_explicit_baseline(self) -> None:
        result = VALIDATOR_MODULE.validate_bundle(VALID_FIXTURE, "bundle.json", "baseline.json")
        self.assertEqual(result["result"], "valid")
        self.assertEqual(result["structural_status"], "valid")
        self.assertEqual(result["baseline_status"], "match")
        self.assertEqual(result["checked_record_count"], 6)
        self.assertEqual(result["issues"], [])

    def test_rejects_duplicate_ids_missing_references_self_references_and_cycles(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        duplicate = copy.deepcopy(bundle["records"][0])
        bundle["records"].append(duplicate)
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "duplicate_record_id")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][2]["assertion_id"] = "MISSING_ASSERTION"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "missing_record_reference")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][3]["target_record_ids"] = ["VERIFY_001"]
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "self_record_reference")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][4]["target_record_ids"] = ["REVISION_001"]
        bundle["records"][5]["affected_downstream_object_ids"] = ["DECISION_001"]
        bundle["records"][5]["downstream_impact_state"] = "downstream_reassessment_required"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "circular_record_reference")

    def test_rejects_missing_exact_locator_and_machine_claim_overreach(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][1]["exact_locator"] = None
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "missing_exact_locator")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][3]["positive_scope"] = "Citation entailment was established."
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "forbidden_machine_claim")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][3]["explicit_non_claims"].remove("human_approval")
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "incomplete_verification_non_claims")

    def test_rejects_ai_human_decision_and_problem_evidence_as_satisfied_prerequisite(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][4]["decision_maker_actor_class"] = "ai"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "schema_validation")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][1]["availability_currentness"] = "unknown"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "unsatisfied_evidence_prerequisite")

    def test_rejects_incomplete_revision_and_downstream_reassessment_misrepresentation(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        revision = bundle["records"][5]
        revision["creation_mode"] = "revision"
        revision["predecessor_reference"] = None
        revision["prior_version_or_safe_identity"] = None
        revision["change_type"] = "correction"
        revision["reason"] = "synthetic correction"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "schema_validation")

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        revision = bundle["records"][5]
        revision["affected_downstream_object_ids"] = ["DECISION_001"]
        revision["downstream_impact_state"] = "downstream_reassessment_required"
        self.write_json(bundle_path, bundle)
        self.assert_issue(self.validate(root), "downstream_reassessment_not_complete")

    def test_pending_revision_authorization_is_visible_but_not_represented_as_approved(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        revision = bundle["records"][5]
        revision["authorization"] = {"state": "pending", "reference": "SYNTHETIC-PENDING-001"}
        self.write_json(bundle_path, bundle)
        result = self.validate(root)
        self.assertEqual(result["result"], "valid")
        self.assertIn("REVISION_001", result["declared_findings"]["pending_or_unknown_revision_authorization_record_ids"])

    def test_canonical_identity_is_stable_and_duplicate_json_keys_are_refused(self) -> None:
        bundle = self.load_json(VALID_FIXTURE / "bundle.json")
        reordered = dict(reversed(list(bundle.items())))
        self.assertEqual(
            VALIDATOR_MODULE.canonical_json_sha256(bundle),
            VALIDATOR_MODULE.canonical_json_sha256(reordered),
        )

        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        duplicate_path = root / "duplicate.json"
        duplicate_path.write_text('{"schema_version":"1.0.0","schema_version":"1.0.0"}\n', encoding="utf-8")
        result = VALIDATOR_MODULE.validate_bundle(root, "duplicate.json")
        self.assert_issue(result, "duplicate_json_key")

    def test_baseline_mismatch_is_not_a_successful_identity_check(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        bundle_path = root / "bundle.json"
        bundle = self.load_json(bundle_path)
        bundle["records"][0]["assertion_summary"] = "Synthetic bundle changed after its baseline was produced."
        self.write_json(bundle_path, bundle)
        result = self.validate(root, baseline=True)
        self.assertEqual(result["structural_status"], "valid")
        self.assertEqual(result["baseline_status"], "mismatch")
        self.assert_issue(result, "baseline_mismatch")

    def test_refuses_root_escape_and_linked_bundle_or_baseline_when_supported(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        result = VALIDATOR_MODULE.validate_bundle(root, "../outside.json")
        self.assert_issue(result, "unsafe_input_path")

        outside = Path(temporary_directory.name) / "outside.json"
        shutil.copyfile(root / "bundle.json", outside)
        linked_bundle = root / "linked-bundle.json"
        linked_baseline = root / "linked-baseline.json"
        try:
            os.symlink(outside, linked_bundle)
            os.symlink(root / "baseline.json", linked_baseline)
        except OSError as error:
            self.skipTest(f"symbolic link creation is unavailable in this test environment: {error}")
        self.assert_issue(VALIDATOR_MODULE.validate_bundle(root, "linked-bundle.json"), "unsafe_input_path")
        self.assert_issue(VALIDATOR_MODULE.validate_bundle(root, "bundle.json", "linked-baseline.json"), "unsafe_input_path")

    def test_refuses_root_with_symbolic_link_ancestor_when_supported(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        physical_temporary_root = Path(temporary_directory.name).resolve()
        actual_parent = physical_temporary_root / "actual-parent"
        physical_root = actual_parent / "review-root"
        shutil.copytree(VALID_FIXTURE, physical_root)
        linked_parent = physical_temporary_root / "linked-parent"
        try:
            os.symlink(actual_parent, linked_parent, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic link creation is unavailable in this test environment: {error}")
        result = VALIDATOR_MODULE.validate_bundle(linked_parent / "review-root", "bundle.json", "baseline.json")
        self.assertEqual(result["structural_status"], "invalid")
        self.assertIn("unsafe_root_path", {issue["code"] for issue in result["issues"]})

    def test_does_not_read_unlisted_sentinel_enumerate_root_or_create_output(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        sentinel = root / "unlisted-data-sentinel.bin"
        sentinel.write_bytes(b"\x00must-not-be-read\x01")
        before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        original_read_text = Path.read_text
        original_iterdir = Path.iterdir
        reads: list[Path] = []

        def guarded_read_text(path: Path, *args, **kwargs):
            resolved = path.resolve()
            reads.append(resolved)
            if resolved == sentinel.resolve():
                raise AssertionError("validator attempted to read an unlisted sentinel")
            return original_read_text(path, *args, **kwargs)

        def guarded_iterdir(path: Path):
            if path.resolve() == root.resolve():
                raise AssertionError("validator attempted to enumerate the review root")
            return original_iterdir(path)

        with mock.patch.object(Path, "read_text", guarded_read_text), mock.patch.object(Path, "iterdir", guarded_iterdir):
            result = self.validate(root, baseline=True)
        after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        self.assertEqual(result["result"], "valid")
        self.assertNotIn(sentinel.resolve(), reads)
        self.assertEqual(before, after)

    def test_cli_output_and_existing_v0_5_contract_boundary(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(VALID_FIXTURE),
                "--bundle",
                "bundle.json",
                "--baseline-manifest",
                "baseline.json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["result"], "valid")
        self.assertIn("jsonschema==4.26.0", REQUIREMENTS_PATH.read_text(encoding="utf-8"))

        prior_schema = json.loads(
            (REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "data_provenance_register.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(prior_schema["properties"]["schema_version"]["const"], "1.0.0")
        self.assertNotIn("data_provenance", SCRIPT_PATH.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
