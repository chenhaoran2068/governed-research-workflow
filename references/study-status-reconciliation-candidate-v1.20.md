# Study Status Reconciliation Candidate v1.20.0

## Candidate Status

This is a design-only candidate derived from the public `v1.19.1` tag. It
does not change an installed runtime, discover Studies, create or modify a
Study record, infer a scientific state, advance a Gate, grant access, or
publish material.

## Observed Problem

The v1.18 status-snapshot contract introduced a useful small declared view:
one of five operating statuses, an optional 01--11 lifecycle stage, current
focus, next action, next human decision, and named conditions. Two compatible
but distinct historical bootstrap surfaces now exist in real local use:

- an older empty-workspace scaffold that has no status snapshot;
- a newer scaffold that creates a structured status snapshot and state
  records.

The existing contract deliberately does not migrate older Studies. That
boundary remains correct. However, a real reconciled Study record also showed
that the fixed condition vocabulary and the single `current_stage` field do
not express a useful detailed work state without becoming structurally
invalid. The correction must preserve a small common contract while allowing
explicitly scoped detail.

## v1.20 Candidate Objective

Provide a read-only way to classify a caller-named Study-status record as one
of the following, without changing the Study:

1. valid under the v1.18 record shape;
2. valid under a proposed v1.20 record shape;
3. legacy with no snapshot;
4. present but structurally invalid, with an itemized mapping proposal;
5. unreadable or unavailable.

The output is a reconciliation preview. It is not a migration, approval,
transition, status decision, or evidence of any Study fact.

When an older record uses free text for `last_transition`, the preview reports
it as reconciliation context only. It must not synthesize a formal lifecycle
transition, transition reference, or human decision.

## Proposed Record Evolution

The outer record remains a single `study_status_snapshot` object. The five
operating statuses remain exactly:

```text
queued | active | paused | stopped | archived
```

The 01--11 stage catalogue remains the only lifecycle-stage catalogue. The
proposed v1.20 record keeps `current_stage` as either a catalogue stage object
or `null`; free prose must not occupy that field.

### Detailed Work State

Add an optional `work_state` object:

```json
{
  "code": "manuscript_completion_and_governance_reconciliation",
  "label": "Manuscript completion and governance reconciliation",
  "scope": "study_local",
  "description": "Optional declared detail beneath an active lifecycle stage."
}
```

Rules:

- `code` is lower-case ASCII words joined by hyphens or underscores, 3--128
  characters; it is an identifier, not a conclusion;
- `label` and `description` are explanatory text, not authority statements;
- `scope` is `study_local` unless a later released controlled catalogue names
  another scope;
- a `work_state` cannot replace `operating_status`, `current_stage`, a Gate,
  or a result-authority record.

### Conditions

Retain the existing six common condition types as the public core:

```text
StateRecordCurrent
ReadyForNextTransition
GateEvidenceCurrent
AuthorityResolved
RequirementsCurrent
ReconciliationComplete
```

Add an optional `declared_conditions` array for scoped detail. Each item must
contain:

```json
{
  "condition_id": "candidate_analysis_complete",
  "category": "analysis_readiness",
  "status": true,
  "message": "A declared candidate analysis package and QA record are present.",
  "evidence_references": ["07_analysis/05_runs/<run-id>/formal_run_manifest.json"],
  "scope": "study_local"
}
```

`category` is a small controlled list:

```text
analysis_readiness | manuscript_readiness | submission_readiness |
requirements | reconciliation | other_declared
```

`condition_id` is study-local unless a later release adds it to a controlled
catalogue. `message` and evidence references describe the declaration; they
do not independently establish that the declaration is true.

### Transition

Keep `last_transition` for changes to `operating_status` or the 01--11 stage.
Do not use it for a detailed work-state edit. Add an optional
`last_reconciliation` object for a human-confirmed conversion or correction:

```json
{
  "reconciliation_id": "<caller-assigned-id>",
  "recorded_at": "<RFC3339 timestamp>",
  "actor": "<accountable actor>",
  "source_shape": "v1_18_or_legacy",
  "human_decision_reference": "<project-relative reference>",
  "summary": "<what was mapped, preserved, or left unresolved>"
}
```

## Reconciliation Preview Interface

The proposed command accepts exactly one caller-named Study root. It resolves
only the fixed path `00_state/study_status_snapshot.json` beneath that root;
it must not enumerate the workspace, infer another Study root, or follow
references.

```text
python scripts/preview_study_status_reconciliation.py --study-root <path>
```

Expected output has one JSON object with:

- `result`: `v1_18_valid`, `v1_20_valid`, `legacy_no_snapshot`,
  `mapping_required`, `unreadable`, or `error`;
- `issues`: zero or more structural observations;
- `proposed_mapping`: zero or one non-applying mapping proposal;
- `write_performed`: always `false`.

When the fixed snapshot path is absent, the result is `legacy_no_snapshot`,
not an error or a request to create a record. Malformed JSON, an unavailable
Study root, absolute or parent-traversal evidence
references, and unsupported condition categories must produce distinct error
outcomes. No output may include source-data values, credentials, or directory
enumeration.

## Legacy Boundary

Existing Studies remain unchanged by installation or validation. A future
apply operation, if ever proposed, must require all of the following:

1. an explicit caller-named Study root;
2. a preview artifact that identifies the input snapshot and its hash;
3. a human-reviewed mapping with unresolved items retained explicitly;
4. an exact approval reference;
5. a new status-record revision and a receipt;
6. no overwrite of the prior record.

The v1.20 candidate does not include that apply operation.

## Compatibility and Tests Required Before Any Release

- Current v1.18 valid fixtures must remain valid without rewrite.
- A synthetic v1.20 detailed-work-state fixture must validate.
- A synthetic legacy-no-snapshot preview must be read-only.
- A synthetic mapping-required fixture must identify an invalid free-text
  stage and unrecognized condition types without changing input.
- Invalid references, malformed JSON, unsupported categories, and a missing
  path must fail explicitly.
- The bootstrap contract must have one declared status-record strategy across
  standalone and framework-integrated profiles. It must not silently migrate
  older scaffolds.

## Explicit Non-Goals

This candidate does not add a dashboard, discover or count Studies, alter the
Framework Program index, decide a Study's state, replace project-specific
records, or change data, analysis, manuscript, publication, or GitHub
authority.
