#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_paper_repository_candidate as builder
import validate_paper_repository_candidate as validator


def load_template(name: str) -> dict:
    return json.loads((ROOT / "assets" / "paper-repository" / name).read_text(encoding="utf-8"))


def valid_manifest() -> dict:
    manifest = load_template("paper-repository-release-manifest.template.json")
    manifest.update(
        {
            "study_id": "Research9999_synthetic",
            "research_output_id": "paper-001",
            "release_profile": "code_with_synthetic_demo",
            "updated_at": "2026-09-07T12:00:00+09:00",
        }
    )
    manifest["candidate"].update(
        {
            "candidate_id": "candidate-001",
            "destination_reference": "candidates/candidate-001",
        }
    )
    manifest["content"]["shortest_run_command"] = "python code/run.py"
    manifest["content"]["expected_output_reference"] = "expected/contract.md"
    manifest["repository"]["name"] = "critical-care-paco2-analysis"
    manifest["repository"]["naming"].update(
        {
            "subject_or_domain": "critical-care",
            "core_focus": "paco2",
            "output_type": "analysis",
            "selected_dimensions": ["domain", "exposure", "intended_use"],
            "rationale": "Stable public terms identifying the domain, focus, and output.",
            "human_confirmed": True,
        }
    )
    return manifest


class PaperRepositoryReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="paper-repository-release-test-"))
        self.source = self.temp / "source"
        self.source.mkdir()
        (self.source / "README.md").write_text("# Synthetic repository\n", encoding="utf-8")
        (self.source / "code").mkdir()
        (self.source / "code" / "run.py").write_text("print('synthetic')\n", encoding="utf-8")
        self.scope_path = self.temp / "scope.json"
        scope = {
            "record_type": "paper_repository_public_export_scope",
            "schema_version": "0.1.0",
            "study_id": "Research9999_synthetic",
            "candidate_id": "candidate-001",
            "source_root_reference": "source",
            "destination_reference": "candidate",
            "include": [
                {"source_reference": "README.md", "destination_reference": "README.md", "mode": "copy", "reason": "Synthetic test README"},
                {"source_reference": "code/run.py", "destination_reference": "code/run.py", "mode": "copy", "reason": "Synthetic test code"},
            ],
            "exclude_categories": [{"category": "restricted_data", "reason": "Never used in this synthetic test"}],
            "allowed_generated_derivatives": [],
            "review": {"owner": "synthetic tester", "rights_status": "pending", "privacy_status": "pending", "coauthor_status": "not_applicable"},
        }
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp, ignore_errors=True)

    def test_builder_copies_only_allowlisted_files_and_writes_inventory(self) -> None:
        destination = self.temp / "candidate"
        inventory = builder.build(self.scope_path, self.source, destination)
        self.assertEqual([item["path"] for item in inventory["files"]], ["README.md", "code/run.py"])
        self.assertTrue((destination / "PUBLIC_EXPORT_INVENTORY.json").is_file())
        self.assertFalse((destination / ".git").exists())

    def test_builder_refuses_existing_destination(self) -> None:
        destination = self.temp / "candidate"
        destination.mkdir()
        with self.assertRaises(FileExistsError):
            builder.build(self.scope_path, self.source, destination)

    def test_builder_refuses_parent_traversal(self) -> None:
        scope = json.loads(self.scope_path.read_text(encoding="utf-8"))
        scope["include"][0]["destination_reference"] = "../README.md"
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        with self.assertRaises(ValueError):
            builder.build(self.scope_path, self.source, self.temp / "candidate")

    def test_builder_refuses_case_insensitive_destination_collision(self) -> None:
        scope = json.loads(self.scope_path.read_text(encoding="utf-8"))
        scope["include"][1]["destination_reference"] = "readme.MD"
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        with self.assertRaises(ValueError):
            builder.build(self.scope_path, self.source, self.temp / "candidate")

    def test_builder_refuses_unimplemented_generated_derivative(self) -> None:
        scope = json.loads(self.scope_path.read_text(encoding="utf-8"))
        scope["allowed_generated_derivatives"] = [{"name": "synthetic-data"}]
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        with self.assertRaises(ValueError):
            builder.build(self.scope_path, self.source, self.temp / "candidate")

    def make_candidate(self) -> Path:
        candidate = self.temp / "review-candidate"
        (candidate / "expected").mkdir(parents=True)
        (candidate / "README.md").write_text("# Synthetic repository\n", encoding="utf-8")
        (candidate / "CITATION.cff").write_text("cff-version: 1.2.0\ntitle: Synthetic\n", encoding="utf-8")
        (candidate / "DATA_ACCESS.md").write_text("# Data access\nOnly generated synthetic data.\n", encoding="utf-8")
        (candidate / "expected" / "contract.md").write_text("# Expected outputs\n", encoding="utf-8")
        (candidate / "RELEASE_MANIFEST.json").write_text(json.dumps(valid_manifest()), encoding="utf-8")
        return candidate

    def test_private_preparation_candidate_is_structurally_valid(self) -> None:
        result = validator.validate(self.make_candidate())
        self.assertEqual(result, {"status": "valid", "errors": []})

    def test_candidate_detects_private_absolute_path(self) -> None:
        candidate = self.make_candidate()
        (candidate / "notes.md").write_text("Do not use E:\\Private\\real-data.csv\n", encoding="utf-8")
        result = validator.validate(candidate)
        self.assertIn("private_path", {item["code"] for item in result["errors"]})

    def test_release_candidate_requires_passed_gates_and_human_confirmation(self) -> None:
        candidate = self.make_candidate()
        manifest = valid_manifest()
        manifest["release_status"] = "release_candidate"
        (candidate / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = validator.validate(candidate)
        codes = [item["code"] for item in result["errors"]]
        self.assertIn("release_gate_not_passed", codes)
        self.assertIn("human_decision_missing", codes)

    def test_candidate_rejects_name_that_does_not_match_recorded_components(self) -> None:
        candidate = self.make_candidate()
        manifest = valid_manifest()
        manifest["repository"]["name"] = "unrelated-name"
        (candidate / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = validator.validate(candidate)
        self.assertIn("repository_name_mismatch", {item["code"] for item in result["errors"]})

    def test_release_candidate_requires_complete_confirmed_naming_record(self) -> None:
        candidate = self.make_candidate()
        manifest = valid_manifest()
        manifest["release_status"] = "release_candidate"
        manifest["repository"]["naming"]["human_confirmed"] = False
        manifest["repository"]["naming"]["selected_dimensions"] = []
        (candidate / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = validator.validate(candidate)
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("repository_name_unconfirmed", codes)
        self.assertIn("repository_naming_incomplete", codes)

    def test_unresolved_required_template_placeholder_is_rejected(self) -> None:
        candidate = self.make_candidate()
        (candidate / "notes.md").write_text("Study: <study-id>\n", encoding="utf-8")
        result = validator.validate(candidate)
        self.assertIn("unresolved_placeholder", {item["code"] for item in result["errors"]})

    def test_candidate_rejects_renv_library(self) -> None:
        candidate = self.make_candidate()
        library = candidate / "renv" / "library"
        library.mkdir(parents=True)
        (library / "package.txt").write_text("synthetic dependency cache\n", encoding="utf-8")
        result = validator.validate(candidate)
        self.assertIn("disallowed_path", {item["code"] for item in result["errors"]})


if __name__ == "__main__":
    unittest.main()
