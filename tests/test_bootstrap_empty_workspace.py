"""End-to-end and failure-path tests for the public empty-workspace helper."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "bootstrap_empty_workspace.py"


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location("public_bootstrap", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load bootstrap helper for test.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BootstrapEmptyWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.temporary_directory.name) / "workspaces"
        self.workspace_root.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def command(self, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT_PATH),
            "--workspace-root",
            str(self.workspace_root),
            "--title",
            "Example Study",
            "--workspace-id",
            "example-study",
            *extra,
        ]

    def run_command(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(self.command(*extra), text=True, capture_output=True, check=False)

    def preview(self) -> dict[str, object]:
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "preview")
        return payload

    def test_preview_makes_no_write(self) -> None:
        payload = self.preview()
        self.assertFalse((self.workspace_root / "example-study").exists())
        self.assertEqual(payload["plan"]["workspace_id"], "example-study")
        self.assertIn("workspace_root_identity", payload["plan"])

    def test_non_ascii_titles_receive_distinct_stable_workspace_ids(self) -> None:
        module = load_bootstrap_module()
        first = module.safe_workspace_id("血气研究")
        second = module.safe_workspace_id("氧合研究")
        self.assertRegex(first, r"^research-workspace-[0-9a-f]{10}$")
        self.assertRegex(second, r"^research-workspace-[0-9a-f]{10}$")
        self.assertNotEqual(first, second)
        self.assertEqual(first, module.safe_workspace_id("血气研究"))

    def test_confirmation_requires_matching_plan_and_approval_reference(self) -> None:
        self.preview()
        missing_plan = self.run_command("--confirm-create", "--approval-reference", "approval-001")
        self.assertEqual(missing_plan.returncode, 2)
        self.assertIn("does not match", missing_plan.stderr)

        wrong_plan = self.run_command(
            "--confirm-create",
            "--plan-id",
            "grw-plan-wrong",
            "--approval-reference",
            "approval-001",
        )
        self.assertEqual(wrong_plan.returncode, 2)
        self.assertFalse((self.workspace_root / "example-study").exists())

    def test_confirmed_create_makes_only_allowlisted_scaffold_and_valid_receipt(self) -> None:
        plan = self.preview()["plan"]
        result = self.run_command(
            "--confirm-create",
            "--plan-id",
            plan["plan_id"],
            "--approval-reference",
            "approval-001",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "created")

        workspace = self.workspace_root / "example-study"
        module = load_bootstrap_module()
        actual_directories = {
            path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_dir()
        }
        actual_files = {
            path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file()
        }
        self.assertEqual(actual_directories, set(module.WORKSPACE_DIRS))
        self.assertEqual(actual_files, set(module.PLANNED_FILES))

        receipt_path = workspace / "00_state" / "bootstrap_receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["approval_reference"], "approval-001")
        self.assertEqual(receipt["tool_version"], "0.3.0")
        self.assertTrue(receipt["scope"]["creates_empty_scaffold_only"])
        self.assertFalse(receipt["scope"]["copies_source_data"])
        state = json.loads((workspace / "00_state" / "workspace_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["authorization_status"], "not_authorized")
        self.assertEqual(state["state"], "scaffolded")
        execution_contract = json.loads(
            (workspace / "07_analysis" / "00_contract" / "analysis_execution_contract.json").read_text(encoding="utf-8")
        )
        result_authority = json.loads(
            (workspace / "08_results" / "_manifests" / "current_result_authority.json").read_text(encoding="utf-8")
        )
        self.assertEqual(execution_contract["contract_status"], "draft")
        self.assertEqual(execution_contract["formal_execution_path"]["kind"], "unselected")
        self.assertEqual(result_authority["authority_status"], "no_authoritative_result")
        self.assertIsNone(result_authority["human_authority_decision_reference"])
        for record in receipt["created_file_hashes"]:
            self.assertEqual(module.sha256_file(workspace / record["relative_path"]), record["sha256"])

    def test_existing_workspace_is_not_overwritten(self) -> None:
        existing = self.workspace_root / "example-study"
        existing.mkdir()
        marker = existing / "marker.txt"
        marker.write_text("do not overwrite\n", encoding="utf-8")

        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_text(encoding="utf-8"), "do not overwrite\n")

    def test_replaced_workspace_root_invalidates_the_reviewed_plan(self) -> None:
        plan = self.preview()["plan"]
        parked_root = self.workspace_root.parent / "original-workspaces"
        self.workspace_root.rename(parked_root)
        self.workspace_root.mkdir()

        result = self.run_command(
            "--confirm-create",
            "--plan-id",
            plan["plan_id"],
            "--approval-reference",
            "approval-001",
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("does not match", result.stderr)
        self.assertEqual(list(self.workspace_root.iterdir()), [])
        self.assertEqual(list(parked_root.iterdir()), [])

    def test_invalid_workspace_id_cannot_escape_selected_root(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--workspace-root",
                str(self.workspace_root),
                "--title",
                "Example Study",
                "--workspace-id",
                "../outside",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.workspace_root.parent / "outside").exists())

    def test_linked_workspace_name_is_refused_when_supported_by_the_platform(self) -> None:
        linked_name = self.workspace_root / "example-study"
        linked_target = self.workspace_root / "linked-target"
        try:
            linked_name.symlink_to(linked_target, target_is_directory=True)
        except OSError as error:
            self.skipTest("Symbolic links are unavailable in this test environment: %s" % error)

        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertTrue(linked_name.is_symlink())
        self.assertFalse(linked_target.exists())

    def test_linked_workspace_root_is_refused_when_supported_by_the_platform(self) -> None:
        actual_root = Path(self.temporary_directory.name) / "actual-workspaces"
        actual_root.mkdir()
        linked_root = Path(self.temporary_directory.name) / "linked-workspaces"
        try:
            linked_root.symlink_to(actual_root, target_is_directory=True)
        except OSError as error:
            self.skipTest("Symbolic links are unavailable in this test environment: %s" % error)

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--workspace-root",
                str(linked_root),
                "--title",
                "Example Study",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("symbolic link or reparse point", result.stderr)
        self.assertEqual(list(actual_root.iterdir()), [])

    @unittest.skipUnless(sys.platform == "win32", "Windows junction test")
    def test_windows_junction_workspace_root_is_refused(self) -> None:
        actual_root = Path(self.temporary_directory.name) / "junction-target"
        actual_root.mkdir()
        junction_root = Path(self.temporary_directory.name) / "junction-workspaces"
        def powershell_literal(path: Path) -> str:
            return "'{}'".format(str(path).replace("'", "''"))

        create_command = (
            "New-Item -ItemType Junction -Path {} -Target {} -ErrorAction Stop | Out-Null"
        ).format(powershell_literal(junction_root), powershell_literal(actual_root))
        created = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", create_command],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        module = load_bootstrap_module()
        self.assertTrue(module.is_link_or_reparse_point(junction_root))
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--workspace-root",
                    str(junction_root),
                    "--title",
                    "Example Study",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("symbolic link or reparse point", result.stderr)
            self.assertEqual(list(actual_root.iterdir()), [])
        finally:
            if junction_root.exists() or junction_root.is_symlink():
                remove_command = "Remove-Item -LiteralPath {} -Force -ErrorAction Stop".format(
                    powershell_literal(junction_root)
                )
                removed = subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", remove_command],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
        self.assertFalse(junction_root.exists())
        self.assertTrue(actual_root.exists())

    def test_injected_write_failure_cleans_owned_staging_directory(self) -> None:
        module = load_bootstrap_module()
        args = module.parse_args(
            [
                "--workspace-root",
                str(self.workspace_root),
                "--title",
                "Example Study",
                "--workspace-id",
                "example-study",
            ]
        )
        plan = module.build_plan(args)
        original_write_text = module.write_text
        write_count = 0

        def failing_write_text(path: Path, content: str) -> None:
            nonlocal write_count
            write_count += 1
            if write_count == 2:
                raise OSError("injected write failure")
            original_write_text(path, content)

        module.write_text = failing_write_text
        try:
            with self.assertRaises(OSError):
                module.create_workspace(plan, "approval-001")
        finally:
            module.write_text = original_write_text

        self.assertFalse((self.workspace_root / "example-study").exists())
        self.assertEqual(list(self.workspace_root.iterdir()), [])

    def test_helper_has_no_source_data_or_network_input(self) -> None:
        module = load_bootstrap_module()
        parser = module.parse_args
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser(["--workspace-root", str(self.workspace_root), "--title", "Example", "--data-source", "x"])

        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for forbidden_import in ("import urllib", "import socket", "import requests"):
            self.assertNotIn(forbidden_import, source)

    def test_unsupported_python_is_refused_without_environment_mutation(self) -> None:
        module = load_bootstrap_module()
        with mock.patch.object(module.sys, "version_info", (3, 10, 99)):
            with self.assertRaises(module.BootstrapRefusal) as raised:
                module.require_supported_python()
        self.assertIn("Python 3.11 or later", str(raised.exception))

    def test_workspace_root_inside_skill_package_is_refused(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--workspace-root",
                str(REPOSITORY_ROOT),
                "--title",
                "Example Study",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the skill package", result.stderr)


if __name__ == "__main__":
    unittest.main()
