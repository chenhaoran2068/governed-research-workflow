"""Synthetic-only cross-module and lifecycle assurance for v0.12."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
FIXTURES_ROOT = REPOSITORY_ROOT / "tests" / "fixtures"
SCENARIO_PATH = REPOSITORY_ROOT / "assets" / "integration-assurance" / "v0_12_synthetic_integration_scenario.md"
REFERENCE_PATH = REPOSITORY_ROOT / "references" / "v0-12-synthetic-integration-assurance.md"
ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "V0_12_SYNTHETIC_INTEGRATION_ASSURANCE.md"
MANUSCRIPT_TEMPLATE_ROOT = REPOSITORY_ROOT / "assets" / "manuscript-governance"


def load_module(filename: str):
    path = SCRIPTS_ROOT / filename
    module_name = f"v012_{path.stem}"
    specification = importlib.util.spec_from_file_location(module_name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


def tracked_paths(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        text=False,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    deleted = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--deleted", "-z"],
        text=False,
        capture_output=True,
        check=False,
    )
    if deleted.returncode != 0:
        raise RuntimeError(deleted.stderr.decode("utf-8", errors="replace"))
    deleted_paths = {item.decode("utf-8") for item in deleted.stdout.split(b"\0") if item}
    paths = [item.decode("utf-8") for item in completed.stdout.split(b"\0") if item]
    return sorted((path for path in paths if path not in deleted_paths), key=lambda item: item.encode("utf-8"))


def snapshot_digest(root: Path, relative_paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative_path in sorted(relative_paths, key=lambda item: item.encode("utf-8")):
        path = root / relative_path
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"snapshot path must be one regular file: {relative_path}")
        payload = path.read_bytes()
        encoded_name = relative_path.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(8, "big"))
        digest.update(encoded_name)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def copy_declared_tree(source: Path, destination: Path, relative_paths: list[str]) -> None:
    for relative_path in relative_paths:
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative_path, target)


class V012RuntimeHardeningAndIntegratedValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.provenance_validator = load_module("validate_data_provenance_register_set.py")
        cls.workflow_validator = load_module("validate_workflow_evidence_control_bundle.py")
        cls.lesson_validator = load_module("validate_lesson_promotion_control_bundle.py")

    def test_synthetic_chain_uses_existing_bounded_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            workspace_root = temporary_root / "workspaces"
            workspace_root.mkdir()
            target_workspace = workspace_root / "synthetic-v012"
            command = [
                sys.executable,
                str(SCRIPTS_ROOT / "bootstrap_empty_workspace.py"),
                "--workspace-root",
                str(workspace_root),
                "--title",
                "Synthetic v0.12 Integration Assurance",
                "--workspace-id",
                "synthetic-v012",
            ]
            environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            preview = subprocess.run(command, text=True, capture_output=True, check=False, env=environment)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            preview_payload = json.loads(preview.stdout)
            self.assertEqual(preview_payload["status"], "preview")
            self.assertFalse(target_workspace.exists())

            confirmed = subprocess.run(
                [
                    *command,
                    "--confirm-create",
                    "--plan-id",
                    preview_payload["plan"]["plan_id"],
                    "--approval-reference",
                    "synthetic-v012-integration-assurance",
                ],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(confirmed.returncode, 0, confirmed.stderr)
            self.assertEqual(json.loads(confirmed.stdout)["status"], "created")
            self.assertTrue(target_workspace.is_dir())

            provenance = self.provenance_validator.validate_register_set(
                FIXTURES_ROOT / "data_provenance_register_set" / "valid" / "register-index.json"
            )
            self.assertEqual(provenance, {"result": "valid", "checked_entry_count": 2, "issues": []})

            workflow = self.workflow_validator.validate_bundle(
                FIXTURES_ROOT / "workflow_evidence_control_bundle" / "valid",
                "bundle.json",
                "baseline.json",
            )
            self.assertEqual(workflow["result"], "valid")
            self.assertEqual(workflow["structural_status"], "valid")
            self.assertEqual(workflow["baseline_status"], "match")
            self.assertEqual(workflow["checked_record_count"], 6)

            lesson = self.lesson_validator.validate_bundle(
                FIXTURES_ROOT / "lesson_promotion_control_bundle" / "valid",
                "bundle.json",
            )
            self.assertEqual(lesson["result"], "valid")
            self.assertEqual(lesson["checked_record_count"], 7)

            for template_path in MANUSCRIPT_TEMPLATE_ROOT.glob("*.template.md"):
                template = template_path.read_text(encoding="utf-8").lower()
                self.assertIn("blank generic template", template)
                self.assertIn("accountable human", template)
                self.assertIn("does not", template)

    def test_invalid_record_is_not_an_approval(self) -> None:
        result = self.provenance_validator.validate_register_set(
            FIXTURES_ROOT / "data_provenance_register_set" / "invalid_duplicate_id" / "register-index.json"
        )
        self.assertEqual(result["result"], "invalid")
        self.assertIn("duplicate_record_id", {issue["code"] for issue in result["issues"]})
        self.assertNotIn("approved", json.dumps(result).lower())

    def test_tracked_snapshot_is_binary_stable_and_ignores_untracked_support(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            tracked = ["text.txt", "binary.bin"]
            (root / "text.txt").write_bytes(b"line-one\r\nline-two\r\n")
            binary_payload = b"\x00binary\r\npayload\xff"
            (root / "binary.bin").write_bytes(binary_payload)
            before = snapshot_digest(root, tracked)
            (root / "_framework_release").mkdir()
            (root / "_framework_release" / "ci-support.txt").write_text("untracked", encoding="utf-8")
            self.assertEqual(snapshot_digest(root, tracked), before)
            self.assertEqual((root / "binary.bin").read_bytes(), binary_payload)

    def test_temporary_update_and_rollback_is_not_a_runtime_installation(self) -> None:
        source_paths = tracked_paths(REPOSITORY_ROOT)
        self.assertNotIn("__pycache__", "\n".join(source_paths))
        self.assertFalse(any(path.endswith(".pyc") for path in source_paths))
        source_digest = snapshot_digest(REPOSITORY_ROOT, source_paths)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            prior_runtime = root / "prior-runtime"
            prior_runtime.mkdir()
            (prior_runtime / "synthetic-prior-runtime-marker.txt").write_text("prior", encoding="utf-8")
            staging = root / "candidate-staging"
            active = root / "simulated-active-runtime"
            rollback = root / "rollback-copy"

            copy_declared_tree(REPOSITORY_ROOT, staging, source_paths)
            self.assertEqual(snapshot_digest(staging, source_paths), source_digest)
            shutil.copytree(prior_runtime, active)
            shutil.move(str(active), str(rollback))
            shutil.move(str(staging), str(active))
            self.assertFalse(staging.exists())
            self.assertEqual(snapshot_digest(active, source_paths), source_digest)
            shutil.rmtree(active)
            shutil.copytree(rollback, active)
            self.assertEqual((active / "synthetic-prior-runtime-marker.txt").read_text(encoding="utf-8"), "prior")
            self.assertEqual(snapshot_digest(REPOSITORY_ROOT, source_paths), source_digest)

    def test_public_explanations_keep_the_synthetic_and_non_installation_boundaries(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (SCENARIO_PATH, REFERENCE_PATH, ASSURANCE_PATH)
        )
        for required in ("synthetic", "not a", "does not", "runtime", "temporary"):
            self.assertIn(required, combined)
        for forbidden in ("e:\\chenhaoran", "c:\\users", "99sai", "research1", "research2", "sepsis", "paco2"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
