# V1 Public Interface Manifest

## Purpose

`v1_public_interface_manifest.json` is the single machine-readable inventory
of the public interfaces frozen for the v1 contract. It records public
profiles, paths, effect categories, linked capability identifiers, promises,
and non-promises.

`interface_frozen` means the listed public contract is frozen for review and
release preparation. It does not say a hosted v1 Release exists. Public
availability requires an exact annotated `v1.0.0` tag and matching GitHub
Release for the same reviewed commit. Installed-runtime identity requires a
separate controlled installation receipt and fresh-process validation.

## Effect Categories

- `guidance_only`: documentation, blank templates, or metadata contracts.
- `read_only`: an explicit validator reads only its named structural input and
  emits a bounded result.
- `controlled_empty_write`: the existing bootstrap helper may create only an
  empty workspace after its own preview and matching confirmation.

The manifest does not authorize invocation. No generic writer, installer,
transfer helper, intake service, or runtime updater is part of the v1 public
interface.

## Authority Separation

Use the capability ledger for individual capability claims. Use the V1
verification map for v1 freeze test requirements. Use exact Git tag and GitHub
Release evidence for hosted-release identity. Use an installation receipt for
local runtime identity. Use accountable humans and project records for project,
data, compliance, manuscript, and submission decisions.

On conflict, stop the affected claim, report the conflicting records and
unknowns, give repair options with tradeoffs, and request accountable-human
resolution. Do not select the convenient record.
