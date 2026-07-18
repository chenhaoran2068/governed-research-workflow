"""Synthetic assurance tests for the metadata-only provenance register set."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main, mock

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPOSITORY_ROOT / "tests" / "fixtures" / "data_provenance_register_set"
VALID_FIXTURE = FIXTURE_ROOT / "valid"
INVALID_DUPLICATE_ID_FIXTURE = FIXTURE_ROOT / "invalid_duplicate_id" / "register-index.json"
INDEX_SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "data_provenance_register_set_index.schema.json"
ENTRY_SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "data_provenance_register.schema.json"
INDEX_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "data-provenance-register-set-index.template.json"
GUIDANCE_PATH = REPOSITORY_ROOT / "references" / "data-provenance-register-set.md"
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "validate_data_provenance_register_set.py"
REQUIREMENTS_PATH = REPOSITORY_ROOT / "requirements.txt"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_data_provenance_register_set", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR_MODULE = _load_validator_module()


class DataProvenanceRegisterSetTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index_schema = json.loads(INDEX_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.entry_schema = json.loads(ENTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.index_schema)
        Draft202012Validator.check_schema(cls.entry_schema)
        cls.index_validator = Draft202012Validator(cls.index_schema, format_checker=FormatChecker())

    def copy_valid_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        destination = Path(temporary_directory.name) / "register"
        shutil.copytree(VALID_FIXTURE, destination)
        return temporary_directory, destination

    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, content: dict) -> None:
        path.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")

    def assert_issue(self, result: dict, expected_code: str) -> None:
        self.assertEqual(result["result"], "invalid")
        self.assertIn(expected_code, {issue["code"] for issue in result["issues"]})

    def test_blank_index_template_matches_the_index_schema(self) -> None:
        template = self.load_json(INDEX_TEMPLATE_PATH)
        self.assertEqual(list(self.index_validator.iter_errors(template)), [])
        self.assertTrue(template["metadata_only"])
        self.assertEqual(template["entries"], [])

    def test_valid_fixture_has_reciprocal_relationships(self) -> None:
        result = VALIDATOR_MODULE.validate_register_set(VALID_FIXTURE / "register-index.json")
        self.assertEqual(result, {"result": "valid", "checked_entry_count": 2, "issues": []})

    def test_static_invalid_fixture_is_rejected_for_duplicate_identity(self) -> None:
        result = VALIDATOR_MODULE.validate_register_set(INVALID_DUPLICATE_ID_FIXTURE)
        self.assert_issue(result, "duplicate_record_id")

    def test_rejects_duplicate_path_and_record_id_mismatch(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        index_path = root / "register-index.json"
        index = self.load_json(index_path)
        index["entries"].append({"record_id": "THIRD_META", "entry_path": "entries/DATASET_META.json"})
        self.write_json(index_path, index)
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(index_path), "duplicate_entry_path")

        index = self.load_json(index_path)
        index["entries"] = index["entries"][:2]
        index["entries"][0]["record_id"] = "WRONG_ID"
        self.write_json(index_path, index)
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(index_path), "record_id_mismatch")

    def test_rejects_unsafe_and_missing_entry_paths(self) -> None:
        for unsafe_path, expected_code in [
            ("../outside.json", "unsafe_entry_path"),
            ("C:/outside.json", "unsafe_entry_path"),
            ("/outside.json", "unsafe_entry_path"),
            ("entries\\SOURCE_META.json", "unsafe_entry_path"),
            ("entries/missing.json", "missing_or_outside_entry"),
        ]:
            with self.subTest(unsafe_path=unsafe_path):
                temporary_directory, root = self.copy_valid_fixture()
                self.addCleanup(temporary_directory.cleanup)
                index_path = root / "register-index.json"
                index = self.load_json(index_path)
                index["entries"][0]["entry_path"] = unsafe_path
                self.write_json(index_path, index)
                self.assert_issue(VALIDATOR_MODULE.validate_register_set(index_path), expected_code)

    def test_rejects_self_and_asymmetric_relationships(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        source_path = root / "entries" / "SOURCE_META.json"
        source = self.load_json(source_path)
        source["lineage"]["upstream_record_ids"] = ["SOURCE_META"]
        self.write_json(source_path, source)
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(root / "register-index.json"), "self_relation")

        source = self.load_json(source_path)
        source["lineage"]["upstream_record_ids"] = []
        source["lineage"]["downstream_record_ids"] = ["DATASET_META"]
        self.write_json(source_path, source)
        dataset_path = root / "entries" / "DATASET_META.json"
        dataset = self.load_json(dataset_path)
        dataset["lineage"]["upstream_record_ids"] = []
        self.write_json(dataset_path, dataset)
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(root / "register-index.json"), "asymmetric_relation")

    def test_unknown_status_remains_metadata_only_and_not_access_approval(self) -> None:
        result = VALIDATOR_MODULE.validate_register_set(VALID_FIXTURE / "register-index.json")
        self.assertEqual(result["result"], "valid")
        self.assertNotIn("access", json.dumps(result).lower())
        source = self.load_json(VALID_FIXTURE / "entries" / "SOURCE_META.json")
        self.assertEqual(source["access_and_sharing"]["access_status"], "unknown")
        self.assertTrue(source["access_and_sharing"]["verification_hypothesis"]["not_an_authorization"])

    def test_marks_an_unpinned_jsonschema_runtime_as_not_assessed(self) -> None:
        with mock.patch.object(VALIDATOR_MODULE, "_installed_jsonschema_version", return_value="4.25.0"):
            result = VALIDATOR_MODULE.validate_register_set(VALID_FIXTURE / "register-index.json")
        self.assertEqual(result["result"], "not_assessed")
        self.assertEqual(result["checked_entry_count"], 0)
        self.assertEqual(result["issues"][0]["code"], "not_assessed_dependency")

    def test_does_not_open_unlisted_sentinel_or_create_output(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        sentinel = root / "real-data-sentinel.bin"
        sentinel.write_bytes(b"\x00must-not-be-read\x01")
        before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        original_read_text = Path.read_text
        reads: list[Path] = []

        def guarded_read_text(path: Path, *args, **kwargs):
            resolved = path.resolve()
            reads.append(resolved)
            if resolved == sentinel.resolve():
                raise AssertionError("validator attempted to read the unlisted sentinel")
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", guarded_read_text):
            result = VALIDATOR_MODULE.validate_register_set(root / "register-index.json")
        after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        self.assertEqual(result["result"], "valid")
        self.assertNotIn(sentinel.resolve(), reads)
        self.assertEqual(before, after)

    def test_rejects_symbolic_link_or_reparse_escape_when_supported(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        outside = Path(temporary_directory.name) / "outside.json"
        shutil.copyfile(root / "entries" / "SOURCE_META.json", outside)
        linked_entry = root / "entries" / "linked.json"
        try:
            os.symlink(outside, linked_entry)
        except OSError as error:
            self.skipTest(f"symbolic link creation is unavailable in this test environment: {error}")
        index_path = root / "register-index.json"
        index = self.load_json(index_path)
        index["entries"][0]["entry_path"] = "entries/linked.json"
        self.write_json(index_path, index)
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(index_path), "unsafe_entry_path")

    def test_allows_a_canonicalized_index_parent_but_refuses_a_linked_index_file(self) -> None:
        temporary_directory, root = self.copy_valid_fixture()
        self.addCleanup(temporary_directory.cleanup)
        linked_parent = Path(temporary_directory.name) / "linked-register-parent"
        linked_index = Path(temporary_directory.name) / "linked-index.json"
        try:
            os.symlink(root, linked_parent, target_is_directory=True)
            os.symlink(root / "register-index.json", linked_index)
        except OSError as error:
            self.skipTest(f"symbolic link creation is unavailable in this test environment: {error}")
        self.assertEqual(
            VALIDATOR_MODULE.validate_register_set(linked_parent / "register-index.json")["result"],
            "valid",
        )
        self.assert_issue(VALIDATOR_MODULE.validate_register_set(linked_index), "unsafe_index_path")

    def test_cli_emits_machine_readable_result_and_expected_exit_status(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(VALID_FIXTURE / "register-index.json")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["result"], "valid")

    def test_dependency_and_guidance_truthfully_state_runtime_scope(self) -> None:
        self.assertEqual(REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines()[-1], "jsonschema==4.26.0")
        guidance = GUIDANCE_PATH.read_text(encoding="utf-8")
        script = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("Python 3.11+", guidance)
        self.assertIn('REQUIRED_JSONSCHEMA_VERSION = "4.26.0"', script)
        self.assertIn("does not open, locate, download, inspect", guidance)
        self.assertNotIn("urllib", script)
        self.assertNotIn("requests", script)


if __name__ == "__main__":
    main()
