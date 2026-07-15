"""Synthetic installation test for the unreleased framework candidate.

This test is intentionally read-only outside a temporary directory. It proves
that the concrete public system can occupy the documented framework locations,
be registered with workspace-relative paths, and own one synthetic project
binding. It is not a system installer or a real research-project bootstrap.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
FRAMEWORK_ROOT_VALUE = os.environ.get("FRAMEWORK_REPOSITORY_ROOT")
FRAMEWORK_ROOT = Path(FRAMEWORK_ROOT_VALUE).resolve() if FRAMEWORK_ROOT_VALUE else None


class IntegrationContractError(ValueError):
    """Raised when a synthetic framework-integration record is inconsistent."""


def load_bootstrap_module(framework_root: Path):
    script_path = framework_root / "scripts" / "bootstrap_workspace.py"
    spec = importlib.util.spec_from_file_location("framework_bootstrap", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load framework bootstrap helper.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_workspace_relative_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise IntegrationContractError("Registered system path must be a safe workspace-relative path.")
    return candidate


def validate_candidate_records(
    workspace: dict[str, Any],
    system: dict[str, Any],
    binding: dict[str, Any],
) -> None:
    if workspace.get("workspace_profile") != "framework_integrated":
        raise IntegrationContractError("Framework-integrated system requires framework_integrated workspace profile.")
    if "framework_integrated" not in system.get("supported_profiles", []):
        raise IntegrationContractError("System manifest does not declare framework_integrated profile.")

    matching_records = [
        record
        for record in workspace.get("registered_systems", [])
        if record.get("system_id") == system.get("system_id")
    ]
    if len(matching_records) != 1:
        raise IntegrationContractError("Workspace must contain exactly one registration for this system.")
    registration = matching_records[0]
    validate_workspace_relative_path(str(registration.get("path", "")))
    if registration.get("system_version") != system.get("system_version"):
        raise IntegrationContractError("Registered system version does not match the system manifest.")
    if binding.get("primary_system") != system.get("system_id"):
        raise IntegrationContractError("Synthetic project binding names an unregistered primary system.")


@unittest.skipUnless(FRAMEWORK_ROOT_VALUE, "Set FRAMEWORK_REPOSITORY_ROOT to run cross-repository integration tests.")
class FrameworkCandidateIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert FRAMEWORK_ROOT is not None
        if not (FRAMEWORK_ROOT / "scripts" / "bootstrap_workspace.py").is_file():
            raise RuntimeError("FRAMEWORK_REPOSITORY_ROOT does not contain the expected framework candidate.")
        import yaml
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        cls.yaml = yaml
        cls.Draft202012Validator = Draft202012Validator
        cls.Registry = Registry
        cls.Resource = Resource
        cls.framework_root = FRAMEWORK_ROOT

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.parent = Path(self.temporary_directory.name) / "workspaces"
        self.parent.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def bootstrap_integrated_workspace(self) -> Path:
        script = self.framework_root / "scripts" / "bootstrap_workspace.py"
        base_command = [
            sys.executable,
            str(script),
            "--parent",
            str(self.parent),
            "--workspace-id",
            "synthetic-grw-integration",
            "--profile",
            "framework_integrated",
        ]
        preview = subprocess.run(base_command, text=True, capture_output=True, check=False)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        preview_payload = json.loads(preview.stdout)
        self.assertEqual(preview_payload["status"], "preview")
        self.assertFalse((self.parent / "synthetic-grw-integration").exists())

        confirmation = subprocess.run(
            [
                *base_command,
                "--confirm-create",
                "--plan-id",
                preview_payload["plan"]["plan_id"],
                "--approval-reference",
                "synthetic-ci-integration-validation",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(confirmation.returncode, 0, confirmation.stderr)
        self.assertEqual(json.loads(confirmation.stdout)["status"], "created")
        return self.parent / "synthetic-grw-integration"

    def copy_concrete_system_package(self, workspace: Path) -> Path:
        destination = workspace / "Systems" / "governed-research-workflow"
        ignored = shutil.ignore_patterns(".git", ".github", "__pycache__", "*.pyc")
        shutil.copytree(REPOSITORY_ROOT, destination, ignore=ignored)
        self.assertTrue((destination / "SYSTEM_MANIFEST.yaml").is_file())
        self.assertTrue((destination / "SKILL.md").is_file())
        return destination

    def load_yaml(self, path: Path) -> dict[str, Any]:
        loaded = self.yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIsInstance(loaded, dict)
        return loaded

    def validate_schemas(
        self,
        workspace: dict[str, Any],
        system: dict[str, Any],
        binding: dict[str, Any],
    ) -> None:
        schema_root = self.framework_root / "schemas"
        workspace_schema = json.loads((schema_root / "workspace_manifest.schema.json").read_text(encoding="utf-8"))
        system_schema = json.loads((schema_root / "system_manifest.schema.json").read_text(encoding="utf-8"))
        project_schema = json.loads((schema_root / "project_system_binding.schema.json").read_text(encoding="utf-8"))
        registry = self.Registry().with_resources(
            [
                (workspace_schema["$id"], self.Resource.from_contents(workspace_schema)),
                (system_schema["$id"], self.Resource.from_contents(system_schema)),
            ]
        )
        self.Draft202012Validator(workspace_schema, registry=registry).validate(workspace)
        self.Draft202012Validator(system_schema).validate(system)
        self.Draft202012Validator(project_schema).validate(binding)

    def test_concrete_system_installs_and_binds_in_an_empty_framework_workspace(self) -> None:
        workspace_root = self.bootstrap_integrated_workspace()
        system_root = self.copy_concrete_system_package(workspace_root)

        workspace_manifest_path = workspace_root / "WORKSPACE_MANIFEST.yaml"
        workspace = self.load_yaml(workspace_manifest_path)
        system = self.load_yaml(system_root / "SYSTEM_MANIFEST.yaml")
        workspace["registered_systems"] = [
            {
                "system_id": system["system_id"],
                "path": "Systems/governed-research-workflow",
                "system_version": system["system_version"],
            }
        ]
        workspace_manifest_path.write_text(
            self.yaml.safe_dump(workspace, sort_keys=False, allow_unicode=False), encoding="utf-8", newline="\n"
        )

        binding_path = workspace_root / "Instances" / "SyntheticStudy001" / "00_state" / "PROJECT_SYSTEM_BINDING.yaml"
        binding_path.parent.mkdir(parents=True)
        binding = {
            "binding_schema_version": 1,
            "project_id": "SyntheticStudy001",
            "primary_system": system["system_id"],
            "contributing_systems": [],
        }
        binding_path.write_text(
            self.yaml.safe_dump(binding, sort_keys=False, allow_unicode=False), encoding="utf-8", newline="\n"
        )

        self.validate_schemas(workspace, system, binding)
        validate_candidate_records(workspace, system, binding)
        registration = workspace["registered_systems"][0]
        self.assertEqual(workspace_root / validate_workspace_relative_path(registration["path"]), system_root)
        self.assertNotIn("E:\\", workspace_manifest_path.read_text(encoding="utf-8"))
        self.assertNotIn("C:\\Users", workspace_manifest_path.read_text(encoding="utf-8"))

    def test_rejects_nonintegrated_workspace_or_unsafe_registration(self) -> None:
        system = self.load_yaml(SYSTEM_MANIFEST_PATH)
        binding = {
            "binding_schema_version": 1,
            "project_id": "SyntheticStudy001",
            "primary_system": system["system_id"],
            "contributing_systems": [],
        }
        standalone_workspace = {
            "workspace_profile": "standalone",
            "registered_systems": [],
        }
        with self.assertRaisesRegex(IntegrationContractError, "framework_integrated workspace profile"):
            validate_candidate_records(standalone_workspace, system, binding)

        unsafe_registration_workspace = {
            "workspace_profile": "framework_integrated",
            "registered_systems": [
                {
                    "system_id": system["system_id"],
                    "path": "../outside-workspace",
                    "system_version": system["system_version"],
                }
            ],
        }
        with self.assertRaisesRegex(IntegrationContractError, "workspace-relative path"):
            validate_candidate_records(unsafe_registration_workspace, system, binding)

    def test_rejects_binding_to_an_unregistered_primary_system(self) -> None:
        system = self.load_yaml(SYSTEM_MANIFEST_PATH)
        workspace = {
            "workspace_profile": "framework_integrated",
            "registered_systems": [
                {
                    "system_id": system["system_id"],
                    "path": "Systems/governed-research-workflow",
                    "system_version": system["system_version"],
                }
            ],
        }
        binding = {
            "binding_schema_version": 1,
            "project_id": "SyntheticStudy001",
            "primary_system": "unregistered-system",
            "contributing_systems": [],
        }
        with self.assertRaisesRegex(IntegrationContractError, "unregistered primary system"):
            validate_candidate_records(workspace, system, binding)


if __name__ == "__main__":
    unittest.main()
