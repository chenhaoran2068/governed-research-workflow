"""Read-only tests for the caller-named status reconciliation preview."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_PATH = ROOT / "scripts" / "preview_study_status_reconciliation.py"
FIXTURE = ROOT / "tests" / "fixtures" / "study_status_snapshot" / "valid" / "active-v1_1.json"


class StudyStatusReconciliationPreviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.study_root = Path(self.temporary_directory.name) / "synthetic-study"
        self.study_root.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_preview(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PREVIEW_PATH), "--study-root", str(self.study_root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_missing_snapshot_is_legacy_and_does_not_write(self) -> None:
        before = list(self.study_root.iterdir())
        result = self.run_preview()
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["result"], "legacy_no_snapshot")
        self.assertFalse(payload["write_performed"])
        self.assertEqual(before, list(self.study_root.iterdir()))

    def test_v1_1_snapshot_is_reported_without_write(self) -> None:
        state_root = self.study_root / "00_state"
        state_root.mkdir()
        snapshot = state_root / "study_status_snapshot.json"
        shutil.copyfile(FIXTURE, snapshot)
        before = snapshot.read_bytes()
        result = self.run_preview()
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["result"], "v1_20_valid")
        self.assertFalse(payload["write_performed"])
        self.assertEqual(before, snapshot.read_bytes())

    def test_nonconforming_snapshot_only_proposes_mapping(self) -> None:
        state_root = self.study_root / "00_state"
        state_root.mkdir()
        snapshot = state_root / "study_status_snapshot.json"
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["schema_version"] = "1.0.0"
        payload.pop("work_state")
        payload.pop("declared_conditions")
        payload.pop("last_reconciliation")
        payload["current_stage"] = "free-text-stage"
        payload["conditions"].append({"type": "CandidateAnalysisComplete"})
        payload["last_transition"] = "free-text-transition"
        snapshot.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        before = snapshot.read_bytes()
        result = self.run_preview()
        preview = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(preview["result"], "mapping_required")
        self.assertFalse(preview["proposed_mapping"]["apply_allowed"])
        sources = {item["source"] for item in preview["proposed_mapping"]["items"]}
        self.assertEqual(sources, {"current_stage", "conditions[2]", "last_transition"})
        self.assertEqual(before, snapshot.read_bytes())

    def test_missing_root_is_an_explicit_error(self) -> None:
        self.study_root.rmdir()
        result = self.run_preview()
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["result"], "error")

    def test_malformed_snapshot_is_unreadable_without_write(self) -> None:
        state_root = self.study_root / "00_state"
        state_root.mkdir()
        snapshot = state_root / "study_status_snapshot.json"
        snapshot.write_text("{", encoding="utf-8")
        before = snapshot.read_bytes()
        result = self.run_preview()
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["result"], "unreadable")
        self.assertFalse(payload["write_performed"])
        self.assertEqual(before, snapshot.read_bytes())

    def test_symbolic_link_ancestor_is_refused_when_supported(self) -> None:
        actual_parent = Path(self.temporary_directory.name) / "actual-parent"
        actual_study = actual_parent / "study"
        actual_study.mkdir(parents=True)
        linked_parent = Path(self.temporary_directory.name) / "linked-parent"
        try:
            linked_parent.symlink_to(actual_parent, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic-link creation unavailable: {error}")
        try:
            result = subprocess.run(
                [sys.executable, str(PREVIEW_PATH), "--study-root", str(linked_parent / "study")],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(payload["result"], "error")
        finally:
            if linked_parent.exists() or linked_parent.is_symlink():
                linked_parent.unlink()

    def test_root_level_system_alias_does_not_hide_a_caller_link(self) -> None:
        actual_parent = Path(self.temporary_directory.name) / "actual-parent"
        actual_study = actual_parent / "study"
        actual_study.mkdir(parents=True)
        linked_parent = Path(self.temporary_directory.name) / "linked-parent"
        try:
            linked_parent.symlink_to(actual_parent, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic-link creation unavailable: {error}")
        try:
            self.assertTrue(PREVIEW_PATH.is_file())
            result = subprocess.run(
                [sys.executable, str(PREVIEW_PATH), "--study-root", str(linked_parent / "study")],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)["result"], "error")
        finally:
            if linked_parent.exists() or linked_parent.is_symlink():
                linked_parent.unlink()

    def test_preview_source_has_no_write_operations(self) -> None:
        source = PREVIEW_PATH.read_text(encoding="utf-8")
        for write_operation in ("write_text(", "write_bytes(", "os.replace(", "unlink(", "mkdir("):
            self.assertNotIn(write_operation, source)


if __name__ == "__main__":
    unittest.main()
