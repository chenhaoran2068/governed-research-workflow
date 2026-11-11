# v1.20.0 State Reconciliation Candidate Control

## Scope

This candidate proposes a narrow System evolution from `v1.19.1`:

- reconcile the declared Study-status record shape with real, caller-named
  status records;
- preserve the five operating statuses and the 01--11 lifecycle catalogue;
- introduce a bounded way to express detailed local work state and scoped
  declared conditions;
- define read-only legacy classification and mapping preview.

## Non-Goals

The candidate does not modify Framework `v0.5.0`, move a Study, migrate a
legacy Study, update the active local runtime, make a research decision,
create a repository, push, tag, publish, or change a GitHub Release.

## Affected Public Surfaces

If implemented after design review, the affected surfaces would be limited to:

- `study_status_snapshot.schema.json` and its template;
- the status-snapshot contract reference;
- the caller-named status validator and a new read-only preview tool;
- synthetic fixtures and tests;
- bootstrap documentation and contract tests.

No Framework schema change is proposed in this candidate. The Framework owns
workspace and Program-location conventions; the System owns the internal
shape and validation of a Study state record.

## Owner Gates

Before implementation, an accountable human must approve:

1. the `work_state` field and its identifier rules;
2. the bounded `declared_conditions` category vocabulary;
3. whether any real Study should receive a separately reviewed reconciliation
   candidate;
4. the exact bootstrap compatibility behavior;
5. release, installation, and restart gates after independent verification.

## Accepted Design Direction

The accountable owner accepted the design direction for the optional
`work_state`, bounded `declared_conditions`, and caller-named read-only
legacy reconciliation preview on 2026-11-10. The preview accepts a Study root
and inspects only its fixed `00_state/study_status_snapshot.json` location.
This acceptance permits implementation planning only. It does not authorize
schema or code changes, modification of an existing Study, runtime adoption,
publication, or release.

## Candidate Evidence

The candidate is based on two observed classes of local records:

- legacy scaffolds that intentionally predate status snapshots;
- newer status records that need detailed local work-state and readiness
  descriptions not representable by the v1.18 fixed condition vocabulary.

These observations justify interface design review only. They do not prove the
correct status, approval, scientific quality, or publication readiness of any
Study.

## Exit Criteria for Design Phase

The design phase is complete only when the owner accepts, revises, defers, or
rejects the proposed record evolution. No code, schema, existing Study record,
or runtime changes are authorized by this document.
