#!/usr/bin/env python3
"""Classify one caller-named Study status record without applying a change."""

from __future__ import annotations

import argparse
import json
import os
import stat
from pathlib import Path
from typing import Any

from validate_study_status_snapshot import DuplicateJsonKeyError, load_json_object, validate_snapshot


SNAPSHOT_RELATIVE_PATH = Path("00_state") / "study_status_snapshot.json"
CORE_CONDITION_TYPES = {
    "StateRecordCurrent",
    "ReadyForNextTransition",
    "GateEvidenceCurrent",
    "AuthorityResolved",
    "RequirementsCurrent",
    "ReconciliationComplete",
}


def is_link_or_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    if os.name != "nt":
        return False
    try:
        attributes = os.lstat(path).st_file_attributes
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400))


def has_link_or_reparse_ancestor(path: Path) -> bool:
    current = path.absolute()
    while True:
        if is_link_or_reparse_point(current):
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def proposed_mapping(payload: dict[str, Any]) -> dict[str, Any]:
    mapping: dict[str, Any] = {"apply_allowed": False, "items": []}
    stage = payload.get("current_stage")
    if isinstance(stage, str) and stage.strip():
        mapping["items"].append(
            {
                "source": "current_stage",
                "proposal": "preserve text as a candidate work_state label and select an 01--11 lifecycle stage through human review",
            }
        )
    for index, condition in enumerate(payload.get("conditions", [])):
        if isinstance(condition, dict) and condition.get("type") not in CORE_CONDITION_TYPES:
            mapping["items"].append(
                {
                    "source": f"conditions[{index}]",
                    "proposal": "review for a bounded declared_conditions entry; do not transfer status or evidence automatically",
                }
            )
    transition = payload.get("last_transition")
    if transition is not None and not isinstance(transition, dict):
        mapping["items"].append(
            {
                "source": "last_transition",
                "proposal": "preserve text only as reconciliation context; record any lifecycle transition separately through human review",
            }
        )
    return mapping


def preview(study_root: Path) -> dict[str, Any]:
    if not study_root.exists() or not study_root.is_dir():
        return {"result": "error", "issues": [issue("study_root", "<input>", "expected one existing Study root directory")], "proposed_mapping": None, "write_performed": False}
    if has_link_or_reparse_ancestor(study_root):
        return {"result": "error", "issues": [issue("study_root", "<input>", "Study root and its ancestors must not be symbolic links or reparse points")], "proposed_mapping": None, "write_performed": False}

    snapshot_path = study_root / SNAPSHOT_RELATIVE_PATH
    if not snapshot_path.exists():
        return {"result": "legacy_no_snapshot", "issues": [issue("missing_snapshot", SNAPSHOT_RELATIVE_PATH.as_posix(), "no status snapshot is present; no record was created")], "proposed_mapping": None, "write_performed": False}
    if has_link_or_reparse_ancestor(snapshot_path):
        return {"result": "error", "issues": [issue("snapshot", SNAPSHOT_RELATIVE_PATH.as_posix(), "snapshot and its ancestors must not be symbolic links or reparse points")], "proposed_mapping": None, "write_performed": False}

    try:
        payload = load_json_object(snapshot_path)
        validation = validate_snapshot(snapshot_path)
    except (DuplicateJsonKeyError, OSError, ValueError, json.JSONDecodeError) as error:
        return {"result": "unreadable", "issues": [issue("snapshot", SNAPSHOT_RELATIVE_PATH.as_posix(), str(error))], "proposed_mapping": None, "write_performed": False}

    if validation["result"] == "valid":
        version = payload.get("schema_version")
        result = "v1_20_valid" if version == "1.1.0" else "v1_18_valid"
        return {"result": result, "issues": [], "proposed_mapping": None, "write_performed": False}
    return {"result": "mapping_required", "issues": validation["issues"], "proposed_mapping": proposed_mapping(payload), "write_performed": False}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview one caller-named Study-status reconciliation without writes.")
    parser.add_argument("--study-root", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    result = preview(parse_args(argv).study_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["result"] != "error" else 2


if __name__ == "__main__":
    raise SystemExit(main())
