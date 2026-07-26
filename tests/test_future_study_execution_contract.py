"""Structural and refusal checks for the generic future-Study record set."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "system" / "09_schemas_records_and_templates"
ASSET_ROOT = ROOT / "assets" / "future-study-execution"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "future_study_execution_contract"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_empty_workspace.py"
GUIDANCE = ROOT / "references" / "future-study-execution-and-reproducibility.md"

RECORDS = {
    "analysis_execution_contract": "analysis-execution-contract",
    "formal_run_manifest": "formal-run-manifest",
    "result_manifest": "result-manifest",
    "current_result_authority": "current-result-authority",
    "analysis_run_qa_record": "analysis-run-qa-record",
}


class FutureStudyExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            record_type: json.loads(
                (SCHEMA_ROOT / f"{record_type}.schema.json").read_text(encoding="utf-8")
            )
            for record_type in RECORDS
        }
        cls.templates = {
            record_type: json.loads(
                (ASSET_ROOT / f"{asset_name}.template.json").read_text(encoding="utf-8")
            )
            for record_type, asset_name in RECORDS.items()
        }

    def test_all_blank_templates_validate_without_claiming_approval_or_authority(self) -> None:
        for record_type, template in self.templates.items():
            errors = list(Draft202012Validator(self.schemas[record_type]).iter_errors(template))
            self.assertEqual(errors, [], record_type + ": " + "; ".join(error.message for error in errors))

        execution = self.templates["analysis_execution_contract"]
        self.assertEqual(execution["contract_status"], "draft")
        self.assertIsNone(execution["approval_reference"])
        self.assertEqual(
            execution["system_contract_reference"],
            "UNRESOLVED_SYSTEM_CONTRACT_REFERENCE",
        )
        self.assertEqual(execution["formal_execution_path"]["kind"], "unselected")
        authority = self.templates["current_result_authority"]
        self.assertEqual(authority["authority_status"], "no_authoritative_result")
        self.assertIsNone(authority["human_authority_decision_reference"])

        guidance = " ".join(GUIDANCE.read_text(encoding="utf-8").split())
        self.assertIn(
            "system-contract identity, not as a Study artifact path",
            guidance,
        )
        self.assertIn("Keep Study artifact references project-relative", guidance)

    def test_authoritative_status_requires_all_four_shaped_references(self) -> None:
        valid = json.loads(
            (FIXTURE_ROOT / "valid" / "current-result-authority.json").read_text(encoding="utf-8")
        )
        invalid = json.loads(
            (FIXTURE_ROOT / "invalid" / "authoritative-without-human-decision.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(self.schemas["current_result_authority"])
        self.assertEqual(list(validator.iter_errors(valid)), [])
        self.assertTrue(list(validator.iter_errors(invalid)))

    def test_unsafe_or_wrong_layout_references_are_refused(self) -> None:
        formal = copy.deepcopy(self.templates["formal_run_manifest"])
        formal["execution_contract_reference"] = "../outside.json"
        self.assertTrue(list(Draft202012Validator(self.schemas["formal_run_manifest"]).iter_errors(formal)))

        result = copy.deepcopy(self.templates["result_manifest"])
        result["formal_run_manifest_reference"] = "07_analysis/05_runs/run-001/not-a-manifest.json"
        self.assertTrue(list(Draft202012Validator(self.schemas["result_manifest"]).iter_errors(result)))

    def test_bootstrap_creates_only_reviewed_empty_record_starters(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace_root = Path(temporary_directory) / "workspaces"
            workspace_root.mkdir()
            command = [
                sys.executable,
                str(BOOTSTRAP),
                "--workspace-root",
                str(workspace_root),
                "--title",
                "Synthetic Study",
                "--workspace-id",
                "synthetic-study",
            ]
            preview = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            plan = json.loads(preview.stdout)["plan"]
            confirmed = subprocess.run(
                command
                + [
                    "--confirm-create",
                    "--plan-id",
                    plan["plan_id"],
                    "--approval-reference",
                    "synthetic-test-approval",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(confirmed.returncode, 0, confirmed.stderr)
            workspace = workspace_root / "synthetic-study"
            execution = json.loads(
                (workspace / "07_analysis" / "00_contract" / "analysis_execution_contract.json").read_text(encoding="utf-8")
            )
            authority = json.loads(
                (workspace / "08_results" / "_manifests" / "current_result_authority.json").read_text(encoding="utf-8")
            )
            self.assertEqual(execution["project_id"], "synthetic-study")
            self.assertEqual(execution["contract_status"], "draft")
            self.assertEqual(
                execution["system_contract_reference"],
                "UNRESOLVED_SYSTEM_CONTRACT_REFERENCE",
            )
            self.assertFalse((workspace / "references").exists())
            self.assertEqual(authority["authority_status"], "no_authoritative_result")
            self.assertIsNone(authority["human_authority_decision_reference"])


if __name__ == "__main__":
    unittest.main()
