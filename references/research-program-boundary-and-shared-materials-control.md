# Research Program Boundary And Shared-Materials Control

## Purpose

This runtime reference guides a human-reviewed grouping of independent Studies
into an optional Research Program. It prevents both errors of ignoring a real
research lineage and treating a common topic, tool, dataset, or contributor
group as permission to merge material or authority.

## Default Isolation

Member Studies remain isolated by default. Their sources, definitions, design
choices, analyses, results, drafts, submission material, exceptions, and human
decisions do not become reusable merely through Program membership. Do not load
sibling Studies or a whole Program history by default.

## Research Program Index

For a Framework v0.5.0-compatible instance with an internal registry, a
human-reviewed index may be located at:

```text
<instance-root>/Registry/Research_Programs/<research-program-id>/
  research_program_index.json
```

The index is metadata about named Study membership. It is not a parent
directory, migration mechanism, access grant, or replacement for Study-local
lifecycle records. It uses instance-relative references and must not contain
absolute local paths, copied Study content, data, or credentials.

`project_id` and `project_manifest` remain Study-level compatibility terms.
Research Program is the distinct upper-level grouping term.

## Human-Reviewed Membership

The caller supplies the exact candidate registry location and exact Study roots
to consider. This guidance does not scan a workspace or discover Studies.
Before a Program is proposed or confirmed, record:

1. its upper-level purpose;
2. its bounded question family, stable shared backbone, or documented lineage;
3. how each named Study relates to the Program; and
4. any proposed narrow reference to stable material.

An accountable human reviews this basis before confirmation. Common title,
author group, schedule, target venue, dataset, or tool alone is insufficient.

## Shared Material Boundary

Program membership does not merge Studies, transfer ethics, governance, data,
result, manuscript, submission, release, or other authority, or grant access.
By default the shared-material list is empty.

Any proposed shared reference must identify the exact source artifact, owner,
reference mode, receiving scope, source version or date, sharing status, and
human-review reference. A pointer, adopted copy, or scoped derivative does not
authorize reading a full sibling workspace or inheriting a decision.
