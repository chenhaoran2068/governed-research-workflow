# Research-Program Boundary And Shared-Materials Control

## Purpose

This optional guidance prevents two opposite errors: treating related research
work units as unrelated when a small stable shared context is useful, and
treating a broad topic or common tool as permission to merge facts, materials,
or authority.

## Default Isolation

Each research work unit remains isolated by default. Its sources, definitions,
analysis choices, results, drafts, submission-facing artifacts, temporary
notes, exceptions, and human decisions do not become reusable merely because
another work unit has a related topic, method, contributor group, dataset, or
target venue.

Do not load sibling work units or a whole research-program history by default.

## Human-Reviewed Grouping

A proposed research-program grouping needs accountable-human review and a
stated upper-level purpose, bounded question family, and meaningful shared
backbone or documented lineage. Broad subject, common dataset, method family,
author group, schedule, or similar title alone is insufficient.

Grouping does not merge work units, change their authority, or grant access to
their materials.

## Research Program Index

For a Framework v0.5.0-compatible instance that already declares an internal
registry, a human-reviewed grouping may be recorded in the optional
instance-local location:

```text
<instance-root>/Registry/Research_Programs/<research-program-id>/
  research_program_index.json
```

The index is a metadata record of named Study membership. It is not a parent
directory for member Studies, a migration mechanism, or a replacement for
their individual lifecycle records. It must use instance-relative references;
it must not contain absolute local paths, copied Study content, data,
credentials, or a claim that membership grants material access.

The Framework's `project_id` and older local `project_manifest` vocabulary
remain Study-level compatibility terms. In this guidance, **Research Program**
is the distinct upper-level grouping of independent Studies.

## Preparing Or Revising An Index

The caller supplies the exact candidate registry location and the exact Study
roots to be considered. This guidance does not scan a workspace or discover
related Studies. Before recording a proposed or confirmed membership, state:

1. the Program's upper-level purpose;
2. the bounded question family, stable shared backbone, or documented lineage;
3. how each named Study relates to the Program; and
4. whether any specific stable material is proposed for narrow reference.

Every index declares that membership does not merge Studies, does not transfer
ethics, governance, data, result, manuscript, submission, release, or other
authority, and does not grant access. By default `shared_material_references`
is empty. Any later
reference names its exact source artifact, owner, reference mode, receiving
scope, source version or date, sharing state, and human-review reference; it
does not authorize reading a full sibling workspace or inheriting a prior
decision.

The accountable human reviews the membership basis and record scope before a
Program is marked `confirmed`. The record is a grouping statement, not proof
of scientific relatedness, data permission, a common protocol, or permission
to advance a member Study.

## Limited Stable Shared Material

Material can be considered for a shared role only when it is stable, compact,
useful to more than one work unit, provenance-clear, and safe to reuse without
silently changing a local question, definition, claim, result, or authority.

Unsettled reasoning, local results and displays, live drafts, review responses,
submission-facing packages, one-off exception logic, and unconfirmed facts
remain local unless a separate human decision provides a stricter basis.

## Narrow Explicit References

When a relationship is allowed, state the named source artifact, reference
mode, receiving purpose and scope, available version or date, and responsible
human or record. The allowed modes are narrow:

- a pointer to one named stable artifact;
- a local adopted copy with source identity and an adoption record; or
- a scoped local derivative with origin and adaptation recorded.

A reference is never permission to read a full source workspace, copy a live
draft, reuse a result, inherit a decision, or treat another work unit's
approval as local approval.

## Human Review Boundary

Repeated reuse may justify a later human-reviewed proposal for a shared rule,
template, checklist, or index. It does not automatically promote material,
change authority, create a sharing mechanism, or authorize access, copying,
merging, publication, or submission.
