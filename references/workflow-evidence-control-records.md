# Workflow And Evidence Control Records

Status: unreleased but accountable-human-admitted `v0.6.0` candidate guidance.
This reference describes a metadata-only structural-record contract only when
`GRW-CAP-060-01` is admitted in the selected version's ledger and that version
independently resolves to a matching public tag and GitHub Release. A local
candidate branch, admission alone, a template, a validator, a test result, or
this document does not itself make the capability publicly available.

## Purpose

The bundle records six different kinds of governance-relevant statements
without treating one as proof of another:

```text
assertion
  -> evidence reference
  -> declared assertion/evidence relation
  -> scoped verification event
  -> human decision when one is recorded
  -> visible revision and downstream-impact record when an object changes
```

It is intended to make representation, declared linkage, stale or unknown
states, and revision impact reviewable. It is not a scientific, legal,
clinical, ethics, DUA, journal, Gate, submission, release, or access-decision
system.

## Files And Record Roles

Use only these v0.6 contracts:

- `system/09_schemas_records_and_templates/workflow_evidence_control_bundle.schema.json`:
  one bundle containing exactly six allowed record types;
- `system/09_schemas_records_and_templates/workflow_evidence_control_baseline.schema.json`:
  an optional comparison manifest, not a seventh governance record;
- `assets/workflow-evidence-control-bundle.template.json` and
  `assets/workflow-evidence-control-baseline.template.json`: blank starting
  points only.

The allowed records are:

| Record | What it records | What it does not establish |
| --- | --- | --- |
| `assertion_record` | A bounded assertion, actor class, lifecycle, scope, and limitation. | Truth, support, or approval. |
| `evidence_reference_record` | A safe pointer, stated availability/currentness, exact locator when known, and limitation. | That the validator opened the source, that it is accessible, reliable, permitted, or sufficient. |
| `assertion_evidence_relation_record` | A declared relationship and its bounded assessment state. | Semantic entailment. |
| `verification_event_record` | The named structural check, inputs, result, and explicit non-claims. | Human review, human approval, Gate passage, compliance, scientific truth, or release readiness. |
| `human_decision_record` | A human-class decision record, stated basis, outcome, limitation, and review/expiry condition. | The human's identity, consent, or actual authorization merely because JSON says so. |
| `revision_and_impact_record` | A visible predecessor/new identity, reason, allowed-write scope, authorization state, and downstream reassessment state. | That a revision was justified, protected, or already rerun downstream. |

Unknown, missing, stale, conflicting, invalidated, pending, or expired states
remain visible. They are not positive authorization or satisfied prerequisites.

## Explicit Read-Only Validation

Invoke the validator only for an explicit, safe review root and explicit
relative JSON inputs:

```text
python scripts/validate_workflow_evidence_control_bundle.py \
  --root <review-root> \
  --bundle <relative-json-path> \
  [--baseline-manifest <relative-json-path>]
```

The validator reads only the supplied bundle and optional baseline below
`--root`. It rejects absolute paths, parent traversal, symbolic links, Windows
reparse points, non-regular files, malformed JSON, duplicate JSON keys, and
unapproved contract versions. It does not scan the review root, write any
file, create a baseline, follow a URL, open a pointer target, read data, or
contact a service.

Its output separates:

- `structural_status`: `valid`, `invalid`, or `not_assessed` for the named
  structural checks;
- `baseline_status`: `not_supplied`, `match`, `mismatch`, or `not_assessed`;
- declared stale, conflict, expiry, pending-authorization, and downstream
  reassessment findings; and
- the checks and non-claims that bound the result.

An overall `valid` result means only that the named JSON inputs matched the
v0.6 structural contract. It is never data-access, sharing, ethics, DUA,
compliance, Gate, submission, release, scientific, or human-approval evidence.

## Revision And Downstream Handling

Do not silently replace a prior authoritative representation. A revision record
must state either `initial_creation` or a predecessor, then state a reason,
allowed-write-scope reference, authorization state, and downstream impact.

When a declared downstream object needs reassessment, the bundle cannot also
represent that object as current, approved, or based on an unchanged upstream
input. The validator exposes this structural contradiction; it does not rerun
the downstream work or decide what the correction should be.

## Optional Baseline Comparison

The only admitted identity method is:

```text
workflow_evidence_control_canonical_json_sha256_v1
UTF-8 JSON, duplicate keys rejected, object keys sorted,
fixed comma/colon separators, SHA-256 of canonical bytes
```

A `match` says only that the supplied bundle equals the supplied baseline under
that method. A `mismatch` says only that they differ. Neither outcome proves
who changed a record, protects a baseline, prevents a process with equivalent
write access from changing both inputs, or makes the history tamper-proof.

## Compatibility And Safe Use

This contract is opt-in. It does not modify or migrate v0.4 single provenance
records, v0.5 provenance register sets, claim-register CSV files, project
records, or installed runtime material. Use only empty or synthetic examples
in public package tests and documentation.

For a real study, the relevant project authority, data-access evidence,
protocol, source-control, human decision, and release rules remain separate.
The bundle may record a declared relationship to those controls but cannot
replace them.
