#!/usr/bin/env python3

"""Create one empty governed-research workspace after explicit confirmation.

The helper is intentionally narrow. It creates a generic, empty directory
layout and provenance receipt. It never imports research material, calls a
network service, advances a workflow state, or makes a scientific or
compliance determination.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import unicodedata
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TOOL_VERSION = "0.2.0-dev"
PLAN_SCHEMA_VERSION = "1.0.0"
STATE_SCHEMA_VERSION = "1.0.0"
MIN_PYTHON = (3, 11)
SAFE_WORKSPACE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parent.parent
ASSET_ROOT = SKILL_ROOT / "assets" / "bootstrap"

WORKSPACE_DIRS = [
    "00_state",
    "01_intake",
    "02_registry",
    "03_protocol",
    "04_knowledge",
    "05_memory",
    "05_memory/retrospective",
    "06_data",
    "07_analysis",
    "08_results",
    "09_manuscript",
    "10_submission",
    "11_qa",
    "12_archive",
]

PLANNED_FILES = [
    "README.md",
    "00_state/workspace_state.json",
    "00_state/bootstrap_receipt.json",
]


class BootstrapRefusal(ValueError):
    """Raised when a requested operation violates the helper contract."""


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(payload: dict[str, Any], stream: Any = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def require_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        current = ".".join(str(part) for part in sys.version_info[:3])
        minimum = ".".join(str(part) for part in MIN_PYTHON)
        raise BootstrapRefusal(
            "Python %s or later is required; current interpreter is %s. "
            "Install or select a supported Python interpreter, then rerun."
            % (minimum, current)
        )


def safe_workspace_id(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    candidate = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return candidate or "research-workspace"


def is_link_or_reparse_point(path: Path) -> bool:
    """Identify symlinks on every platform and Windows directory junctions."""
    if path.is_symlink():
        return True
    if os.name != "nt":
        return False
    try:
        attributes = os.lstat(path).st_file_attributes
    except FileNotFoundError:
        return False
    reparse_attribute = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(attributes & reparse_attribute)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or create one empty governed-research workspace."
    )
    parser.add_argument(
        "--workspace-root",
        required=True,
        help="Existing directory in which one new workspace directory may be created.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Human-readable title stored only in the generated local workspace.",
    )
    parser.add_argument(
        "--workspace-id",
        help="Optional lowercase ASCII directory name; defaults to a title-derived ID.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Emit a no-write preview. Preview is also the default without confirmation.",
    )
    parser.add_argument(
        "--confirm-create",
        action="store_true",
        help="Create only after a reviewed plan is matched and an approval reference is supplied.",
    )
    parser.add_argument(
        "--plan-id",
        help="Exact plan ID returned by the reviewed no-write preview.",
    )
    parser.add_argument(
        "--approval-reference",
        help="Nonempty accountable-human approval reference for the reviewed plan.",
    )
    return parser.parse_args(argv)


def validate_title(title: str) -> str:
    normalized = title.strip()
    if not normalized:
        raise BootstrapRefusal("Title must contain non-whitespace text.")
    if len(normalized) > 200:
        raise BootstrapRefusal("Title must be at most 200 characters.")
    return normalized


def validate_workspace_root(raw_root: str) -> Path:
    candidate = Path(raw_root).expanduser()
    if not candidate.exists() or not candidate.is_dir():
        raise BootstrapRefusal("Workspace root must already exist as a directory: %s" % candidate)
    if is_link_or_reparse_point(candidate):
        raise BootstrapRefusal("Workspace root must not be a symbolic link or reparse point: %s" % candidate)
    resolved = candidate.resolve(strict=True)
    if resolved == SKILL_ROOT or SKILL_ROOT in resolved.parents:
        raise BootstrapRefusal(
            "Workspace root must be outside the skill package so generated research "
            "material cannot enter the public repository."
        )
    return resolved


def build_identity(args: argparse.Namespace, workspace_root: Path) -> tuple[str, Path]:
    workspace_id = args.workspace_id or safe_workspace_id(args.title)
    if not SAFE_WORKSPACE_ID.fullmatch(workspace_id):
        raise BootstrapRefusal(
            "Workspace ID must use lowercase ASCII letters, digits, and hyphens, "
            "start with an alphanumeric character, and be at most 64 characters."
        )
    requested_root = workspace_root / workspace_id
    if requested_root.exists() or is_link_or_reparse_point(requested_root):
        raise BootstrapRefusal("Refusing to create or overwrite existing workspace: %s" % requested_root)
    final_root = requested_root.resolve(strict=False)
    if final_root.parent != workspace_root:
        raise BootstrapRefusal("Final workspace must be a direct child of the selected workspace root.")
    if final_root.exists() or is_link_or_reparse_point(final_root):
        raise BootstrapRefusal("Refusing to create or overwrite existing workspace: %s" % final_root)
    return workspace_id, final_root


def asset_inventory() -> list[dict[str, str]]:
    assets = [
        SCRIPT_PATH,
        ASSET_ROOT / "workspace-readme.template.md",
        ASSET_ROOT / "workspace-state.template.json",
    ]
    for asset in assets:
        if not asset.is_file():
            raise BootstrapRefusal("Required public bootstrap asset is missing: %s" % asset)
    return [
        {
            "relative_path": asset.relative_to(SKILL_ROOT).as_posix(),
            "sha256": sha256_file(asset),
        }
        for asset in assets
    ]


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    title = validate_title(args.title)
    workspace_root = validate_workspace_root(args.workspace_root)
    workspace_id, final_root = build_identity(args, workspace_root)
    payload = {
        "plan_schema_version": PLAN_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "minimum_python": ".".join(str(part) for part in MIN_PYTHON),
        "workspace_root": workspace_root.as_posix(),
        "workspace_id": workspace_id,
        "workspace_title": title,
        "final_workspace_root": final_root.as_posix(),
        "planned_directories": WORKSPACE_DIRS,
        "planned_files": PLANNED_FILES,
        "asset_inventory": asset_inventory(),
        "scope": {
            "creates_empty_scaffold_only": True,
            "copies_source_data": False,
            "reads_source_data": False,
            "calls_network_services": False,
            "advances_workflow_or_gate": False,
            "asserts_scientific_or_compliance_status": False,
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["plan_id"] = "grw-plan-" + sha256_bytes(encoded)[:24]
    return payload


def render_workspace_readme(plan: dict[str, Any]) -> str:
    template = (ASSET_ROOT / "workspace-readme.template.md").read_text(encoding="utf-8")
    return (
        template.replace("{{WORKSPACE_ID}}", plan["workspace_id"])
        .replace("{{WORKSPACE_TITLE}}", plan["workspace_title"])
    )


def render_workspace_state(plan: dict[str, Any], created_at: str) -> str:
    template_path = ASSET_ROOT / "workspace-state.template.json"
    state = json.loads(template_path.read_text(encoding="utf-8"))
    state["workspace_id"] = plan["workspace_id"]
    state["workspace_title"] = plan["workspace_title"]
    state["created_at"] = created_at
    state["workspace_root"] = plan["final_workspace_root"]
    return json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def collect_hashed_files(root: Path, excluded: set[str] | None = None) -> list[dict[str, str]]:
    excluded = excluded or set()
    records = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative_path = path.relative_to(root).as_posix()
        if relative_path in excluded:
            continue
        records.append({"relative_path": relative_path, "sha256": sha256_file(path)})
    return records


def validate_staged_tree(staging_root: Path) -> None:
    actual_directories = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_dir()
    }
    actual_files = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_file()
    }
    if actual_directories != set(WORKSPACE_DIRS):
        raise RuntimeError("Staging directory set differs from the allowlisted scaffold.")
    if actual_files != set(PLANNED_FILES):
        raise RuntimeError("Staging file set differs from the allowlisted scaffold.")


def create_workspace(plan: dict[str, Any], approval_reference: str) -> dict[str, Any]:
    workspace_root = Path(plan["workspace_root"])
    final_root = Path(plan["final_workspace_root"])
    if final_root.parent != workspace_root:
        raise BootstrapRefusal("Final workspace no longer has the approved direct-child location.")
    if final_root.exists() or is_link_or_reparse_point(final_root):
        raise BootstrapRefusal("Refusing to create or overwrite existing workspace: %s" % final_root)

    staging_root = workspace_root / (".grw-bootstrap-" + plan["workspace_id"] + "-" + uuid.uuid4().hex)
    created_at = now_utc()
    try:
        staging_root.mkdir()
        for directory in WORKSPACE_DIRS:
            (staging_root / directory).mkdir(parents=True, exist_ok=False)

        write_text(staging_root / "README.md", render_workspace_readme(plan))
        write_text(
            staging_root / "00_state" / "workspace_state.json",
            render_workspace_state(plan, created_at),
        )

        file_hashes = collect_hashed_files(
            staging_root, excluded={"00_state/bootstrap_receipt.json"}
        )
        receipt = {
            "receipt_schema_version": "1.0.0",
            "created_at": created_at,
            "tool_version": TOOL_VERSION,
            "plan": plan,
            "approval_reference": approval_reference,
            "created_file_hashes": file_hashes,
            "receipt_file_not_self_hashed": True,
            "scope": plan["scope"],
        }
        write_text(
            staging_root / "00_state" / "bootstrap_receipt.json",
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        validate_staged_tree(staging_root)
        if final_root.exists() or is_link_or_reparse_point(final_root):
            raise BootstrapRefusal("Refusing to create or overwrite existing workspace: %s" % final_root)
        staging_root.rename(final_root)
    except Exception:
        if staging_root.exists():
            shutil.rmtree(staging_root)
        raise

    return {
        "status": "created",
        "workspace_root": final_root.as_posix(),
        "plan_id": plan["plan_id"],
        "approval_reference": approval_reference,
        "receipt_path": (final_root / "00_state" / "bootstrap_receipt.json").as_posix(),
        "next_required_action": "Select a collaboration mode before consequential research work.",
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.plan and args.confirm_create:
        raise BootstrapRefusal("Use either preview or confirmation, not both in one invocation.")
    plan = build_plan(args)
    if not args.confirm_create:
        return {
            "status": "preview",
            "plan": plan,
            "next_required_action": (
                "Review the no-write plan. A human must explicitly approve it before "
                "rerunning with --confirm-create, matching --plan-id, and a nonempty "
                "--approval-reference."
            ),
        }
    if args.plan_id != plan["plan_id"]:
        raise BootstrapRefusal("Provided plan ID does not match the current no-write preview.")
    approval_reference = (args.approval_reference or "").strip()
    if not approval_reference:
        raise BootstrapRefusal("Confirmation requires a nonempty --approval-reference.")
    return create_workspace(plan, approval_reference)


def main(argv: list[str] | None = None) -> int:
    try:
        require_supported_python()
        result = run(parse_args(argv))
        emit(result)
        return 0
    except BootstrapRefusal as error:
        emit({"status": "refused", "reason": str(error)}, stream=sys.stderr)
        return 2
    except Exception as error:
        emit({"status": "failed", "reason": str(error)}, stream=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
