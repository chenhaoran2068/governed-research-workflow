"""Structural and boundary checks for the generic Study-status snapshot candidate."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "study_status_snapshot.schema.json"
TEMPLATE_PATH = ROOT / "assets" / "study-status-snapshot.template.json"
CATALOG_PATH = ROOT / "assets" / "study-lifecycle-stage-catalog.v1.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_study_status_snapshot.py"
FIXTURES = ROOT / "tests" / "fixtures" / "study_status_snapshot"


def load_validator():
    specification = importlib.util.spec_from_file_location("study_status_snapshot_validator", VALIDATOR_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("Cannot load Study-status snapshot validator")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


class StudyStatusSnapshotTests(unittest.TestCase):
    def test_blank_template_is_schema_valid_and_queued(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(template)), [])
        self.assertEqual(VALIDATOR.validate_snapshot(TEMPLATE_PATH)["result"], "valid")
        self.assertEqual(template["operating_status"], "queued")
        self.assertIsNone(template["current_stage"])

    def test_valid_fixture_and_stage_catalogue_are_consistent(self) -> None:
        result = VALIDATOR.validate_snapshot(FIXTURES / "valid" / "active.json")
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        pairs = {(item["id"], item["code"]) for item in catalog["stages"]}
        self.assertEqual(result["result"], "valid")
        self.assertEqual(len(pairs), 11)
        self.assertIn(("03", "research_question"), pairs)

    def test_invalid_fixture_reports_active_and_reference_boundaries(self) -> None:
        result = VALIDATOR.validate_snapshot(FIXTURES / "invalid" / "unsafe_reference.json")
        codes = {issue["code"] for issue in result["issues"]}
        self.assertEqual(result["result"], "structurally_invalid")
        self.assertIn("active_next_step_missing", codes)
        self.assertIn("unsafe_reference", codes)

    def test_cli_reads_only_one_named_snapshot_and_writes_no_output(self) -> None:
        command = [sys.executable, str(VALIDATOR_PATH), "--snapshot", str(FIXTURES / "valid" / "active.json")]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["result"], "valid")
        validator_source = VALIDATOR_PATH.read_text(encoding="utf-8")
        for write_operation in ("write_text(", "write_bytes(", "os.replace(", "mkstemp(", "unlink(", "mkdir("):
            self.assertNotIn(write_operation, validator_source)

    def test_public_surface_does_not_contain_private_paths_or_a_writer(self) -> None:
        public_paths = (TEMPLATE_PATH, CATALOG_PATH, SCHEMA_PATH, VALIDATOR_PATH, ROOT / "references" / "study-status-snapshot-contract.md")
        content = "\n".join(path.read_text(encoding="utf-8") for path in public_paths)
        normalized = " ".join(content.lower().split())
        self.assertIsNone(re.search(r"(?i)[a-z]:\\", content))
        self.assertNotIn("study_status_index", normalized)
        self.assertNotIn("record_study_status", normalized)
        self.assertIn("does not discover", normalized)
        self.assertIn("write a record", normalized)


if __name__ == "__main__":
    unittest.main()
