"""Synthetic tests for the voluntary metadata-only experience package."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main, mock

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "voluntary_experience_package" / "valid"
SCHEMA = ROOT / "system" / "09_schemas_records_and_templates" / "voluntary_experience_package.schema.json"
TEMPLATE = ROOT / "assets" / "voluntary-experience-package.template.json"
GUIDANCE = ROOT / "references" / "voluntary-experience-package.md"
SCRIPT = ROOT / "scripts" / "validate_voluntary_experience_package.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_voluntary_experience_package", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module()


class VoluntaryExperiencePackageTests(TestCase):
    def copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        destination = Path(temporary_directory.name) / "package"
        shutil.copytree(FIXTURE, destination)
        return temporary_directory, destination

    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def assert_result(self, result: dict, expected: str, code: str | None = None) -> None:
        self.assertEqual(result["result"], expected)
        if code:
            self.assertIn(code, {issue["code"] for issue in result["issues"]})

    def test_schema_and_root_template_are_valid(self) -> None:
        schema = self.load_json(SCHEMA)
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema).iter_errors(self.load_json(TEMPLATE)))
        self.assertEqual(errors, [])

    def test_valid_synthetic_package_is_structurally_valid(self) -> None:
        result = VALIDATOR.validate_experience_package(FIXTURE / "experience-package.json")
        self.assertEqual(result, {"result": "structurally_valid", "checked_record_count": 5, "issues": []})

    def test_refuses_path_escape_and_indirection_before_out_of_scope_read(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        manifest_path = root / "experience-package.json"
        manifest = self.load_json(manifest_path)
        manifest["records"]["observation_record"] = "../outside.json"
        self.write_json(manifest_path, manifest)
        self.assert_result(VALIDATOR.validate_experience_package(manifest_path), "refused_boundary", "refused_boundary")

        manifest = self.load_json(manifest_path)
        manifest["records"]["observation_record"] = "records/observation.json"
        self.write_json(manifest_path, manifest)
        linked = root / "records" / "linked-observation.json"
        try:
            linked.symlink_to(root / "records" / "observation.json")
        except OSError:
            self.skipTest("symbolic-link creation is unavailable in this environment")
        manifest = self.load_json(manifest_path)
        manifest["records"]["observation_record"] = "records/linked-observation.json"
        self.write_json(manifest_path, manifest)
        self.assert_result(VALIDATOR.validate_experience_package(manifest_path), "refused_boundary", "refused_boundary")

    def test_rejects_duplicate_ids_and_invalid_review_or_withdrawal_states(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        observation_path = root / "records" / "observation.json"
        observation = self.load_json(observation_path)
        observation["record_id"] = "SYNTHETIC_SCOPE"
        self.write_json(observation_path, observation)
        self.assert_result(VALIDATOR.validate_experience_package(root / "experience-package.json"), "structurally_invalid", "duplicate_record_id")

        observation["record_id"] = "SYNTHETIC_OBSERVATION"
        self.write_json(observation_path, observation)
        review_path = root / "records" / "maintainer-review.json"
        review = self.load_json(review_path)
        review["review_state"] = "eligible_for_candidate_consideration"
        self.write_json(review_path, review)
        self.assert_result(VALIDATOR.validate_experience_package(root / "experience-package.json"), "structurally_invalid", "invalid_review_state")

        review["accountable_human_reference"] = "synthetic-human-decision"
        review["decision_basis_references"] = ["synthetic-basis"]
        self.write_json(review_path, review)
        withdrawal_path = root / "records" / "correction-or-withdrawal.json"
        withdrawal = self.load_json(withdrawal_path)
        withdrawal["request_state"] = "future_use_stopped"
        withdrawal["requested_action"] = "withdrawal"
        withdrawal["future_use_state"] = "stopped_after_human_decision"
        self.write_json(withdrawal_path, withdrawal)
        self.assert_result(VALIDATOR.validate_experience_package(root / "experience-package.json"), "structurally_invalid", "invalid_withdrawal_state")

    def test_unnamed_extra_file_is_not_discovered_or_claimed_as_checked(self) -> None:
        temporary_directory, root = self.copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        (root / "unlisted.txt").write_text("synthetic extra", encoding="utf-8")
        result = VALIDATOR.validate_experience_package(root / "experience-package.json")
        self.assert_result(result, "structurally_valid")
        guidance = GUIDANCE.read_text(encoding="utf-8").lower()
        self.assertIn("outside its view", guidance)
        self.assertNotIn("iterdir", SCRIPT.read_text(encoding="utf-8"))
        self.assertNotIn("rglob", SCRIPT.read_text(encoding="utf-8"))

    def test_validator_does_not_write_and_cli_is_machine_readable(self) -> None:
        before = {path.relative_to(FIXTURE).as_posix(): path.read_bytes() for path in FIXTURE.rglob("*") if path.is_file()}
        result = VALIDATOR.validate_experience_package(FIXTURE / "experience-package.json")
        after = {path.relative_to(FIXTURE).as_posix(): path.read_bytes() for path in FIXTURE.rglob("*") if path.is_file()}
        self.assertEqual(result["result"], "structurally_valid")
        self.assertEqual(before, after)

    def test_unpinned_dependency_is_not_assessed(self) -> None:
        with mock.patch.object(VALIDATOR, "_installed_jsonschema_version", return_value="0.0.0"):
            result = VALIDATOR.validate_experience_package(FIXTURE / "experience-package.json")
        self.assert_result(result, "not_assessed", "not_assessed_dependency")

    def test_same_host_clean_environment_simulation_copies_only_declared_synthetic_files(self) -> None:
        source_manifest = FIXTURE / "experience-package.json"
        source = self.load_json(source_manifest)
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        destination = Path(temporary_directory.name) / "received-package"
        destination.mkdir()
        shutil.copy2(source_manifest, destination / source_manifest.name)
        for relative_path in source["records"].values():
            source_path = FIXTURE / relative_path
            destination_path = destination / relative_path
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)
        received = VALIDATOR.validate_experience_package(destination / "experience-package.json")
        self.assert_result(received, "structurally_valid")
        files = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
        self.assertEqual(files, {"experience-package.json", *source["records"].values()})


if __name__ == "__main__":
    main()
