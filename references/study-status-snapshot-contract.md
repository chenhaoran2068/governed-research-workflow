# Study Status Snapshot Contract

This candidate contract defines a short declared view of one Study: its broad
operating status, its current point in the shared 01-11 lifecycle, a current
focus, next action or human decision, and visible conditions that need
attention.

It is a query-facing sidecar. It does not replace a detailed project state
machine, a Gate record, result authority, QA, a submission route, or a human
decision record.

## Declared Fields

- `operating_status` is one of `queued`, `active`, `paused`, `stopped`, or
  `archived`. It is intentionally broad; a blocker, rework, or editorial
  outcome belongs in the next action, conditions, transitions, or a dedicated
  submission record.
- `current_stage` uses the stable pair from
  `assets/study-lifecycle-stage-catalog.v1.json`. It is absent while a Study is
  queued. An active record needs a stage, current focus, and a next action or
  human decision.
- `conditions` always include `StateRecordCurrent` and
  `ReadyForNextTransition`. Other condition types are added only when their
  stated scope applies.
- `study_profile: legacy_unreconciled` retains a visible unresolved
  reconciliation condition. Existing Studies are not automatically migrated.

The template, schema, and validator check structure and internal consistency
only. A valid result does not prove that a Study exists, a stage is correct, a
Gate passed, a requirement is current, a result is authoritative, or an
accountable human approved any action.

## Public Boundary

`scripts/validate_study_status_snapshot.py` reads exactly one caller-named
JSON snapshot plus its package-owned schema and stage catalogue. It does not
discover a Study, enumerate folders, follow or open a reference, read data,
write a record, update a status, create a Workbench index, decide a lifecycle
transition, or grant access.

This public candidate contains no Study, project-local path, data, result,
protocol, governance material, human-decision record, event log, Program-root
index, writer, migration helper, Workbench, release claim, or installed-runtime
claim. A private implementation may add controlled update and index behavior
only under separate review and authorization.
