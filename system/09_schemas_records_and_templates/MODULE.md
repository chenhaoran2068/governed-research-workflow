# Schemas Module Boundary

Status: active blank-record baseline; the unreleased candidate branch adds one
formal generic capability-ledger schema for the `v0.4.0` target.

The active baseline is the set of blank human-reviewed records under `assets/`.
They are templates, not schemas and do not validate live project state. This
module may later hold versioned generic data contracts for reusable records
and their validation. A schema must document its version, required fields,
permitted values, compatibility expectation, ownership, and test fixture.

Do not store live project state, patient-derived data, private identifiers, or
facts that require study-specific approval in a public schema.

`capability_truth_ledger.schema.json` defines the structure of the unreleased
candidate's single capability truth source. It does not validate live project
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
