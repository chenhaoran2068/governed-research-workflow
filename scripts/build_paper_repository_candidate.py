#!/usr/bin/env python3
"""Build one clean candidate from an explicit file-only JSON allowlist."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from paper_repository_release_common import (
    SCHEMA_ROOT, has_linked_parent, is_reparse_or_symlink, load_json,
    relative_posix, safe_relative, sha256,
)


def build(scope_path: Path, source_root: Path, destination: Path) -> dict:
    scope = load_json(scope_path)
    schema = load_json(SCHEMA_ROOT / "paper_repository_public_export_scope.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(scope), key=lambda item: list(item.absolute_path))
    if errors:
        raise ValueError("invalid export scope: " + "; ".join(error.message for error in errors))
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    if not source_root.is_dir() or is_reparse_or_symlink(source_root):
        raise ValueError("source root must be an existing non-link directory")
    source_root = source_root.resolve()
    if scope["allowed_generated_derivatives"]:
        raise ValueError("this builder supports copy-only allowlists; generated derivatives require a separately reviewed builder")

    planned: list[tuple[Path, Path]] = []
    destinations: set[str] = set()
    for item in scope["include"]:
        source_ref = item["source_reference"]
        destination_ref = item["destination_reference"]
        if not safe_relative(source_ref) or not safe_relative(destination_ref):
            raise ValueError("include references must be safe relative paths")
        destination_key = destination_ref.replace("\\", "/").casefold()
        if destination_key in destinations:
            raise ValueError(f"duplicate destination: {destination_ref}")
        destinations.add(destination_key)
        source = source_root / Path(source_ref)
        target = destination / Path(destination_ref)
        if not source.is_file() or is_reparse_or_symlink(source) or has_linked_parent(source, source_root):
            raise ValueError(f"allowlisted source must be a regular file: {source_ref}")
        if not source.resolve().is_relative_to(source_root):
            raise ValueError(f"allowlisted source resolves outside source root: {source_ref}")
        planned.append((source, target))

    destination.mkdir(parents=True, exist_ok=False)
    try:
        for source, target in planned:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        inventory = {
            "record_type": "paper_repository_candidate_inventory",
            "schema_version": "0.1.0",
            "candidate_id": scope["candidate_id"],
            "built_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {"path": relative_posix(target, destination), "size": target.stat().st_size, "sha256": sha256(target)}
                for _, target in sorted(planned, key=lambda pair: relative_posix(pair[1], destination))
            ],
        }
        (destination / "PUBLIC_EXPORT_INVENTORY.json").write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise
    return inventory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.scope.resolve(), args.source_root.resolve(), args.destination.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "built", "file_count": len(result["files"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
