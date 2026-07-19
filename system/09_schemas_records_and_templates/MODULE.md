# Schemas Module Boundary

Status: active blank-record baseline; the v0.4.0 release source adds one
formal generic capability-ledger schema for the `v0.4.0` target.

The active baseline is the set of blank human-reviewed records under `assets/`.
They are templates, not schemas and do not validate live project state. This
module may later hold versioned generic data contracts for reusable records
and their validation. A schema must document its version, required fields,
permitted values, compatibility expectation, ownership, and test fixture.

Do not store live project state, patient-derived data, private identifiers, or
facts that require study-specific approval in a public schema.

`capability_truth_ledger.schema.json` defines the structure of the
release-state-neutral capability truth source. It does not validate live project
state, create a capability, or grant approval.

`bounded_autonomy_authorization.schema.json` defines a synthetic, human-reviewed
task-boundary record. It does not enforce a model's behavior, create an
autonomous executor, grant tool access, or determine data permissions.

`data_provenance_register.schema.json` defines a metadata-only generic core
and optional restricted or clinical awareness extension. It does not read,
import, copy, hash, analyze, share, or authorize data content.

`../11_distribution_installation_and_release/release_control_record.schema.json`
defines a candidate-review and release-control record. It does not create a
Git tag or GitHub Release, grant C4 authorization, or certify security, rights,
or compliance sufficiency.

The admitted v0.6 release scope adds `workflow_evidence_control_bundle.schema.json`
and `workflow_evidence_control_baseline.schema.json`. They define an opt-in
metadata-only six-record bundle and a caller-supplied comparison manifest.
They do not read source content, prove truth or approval, protect a baseline,
or prevent a writer with equivalent access from changing both a bundle and its
comparison manifest.

The v0.8 pre-C4 release source adds `role_contract.schema.json` and
`controlled_helper_admission.schema.json`. The first describes a non-runnable
review-perspective boundary; the second describes a bounded generic helper
contract. Neither schema creates an agent runtime, grants a tool, authorizes a
task, authorizes data access, confirms a filesystem write, or approves a
Release. Their blank templates are synthetic records, not live state.
