# Schemas Module Boundary

The V1 Support Scope Matrix is the machine-readable authority for this
module's support posture; this boundary record does not enlarge that scope.

Status: active blank-record baseline; the v0.4.0 release source adds one
formal generic capability-ledger schema for the `v0.4.0` target.

The active baseline is the set of blank human-reviewed records under `assets/`.
They are templates, not schemas and do not validate live project state. This
module may later hold versioned generic data contracts for reusable records
and their validation. A schema must document its version, required fields,
permitted values, compatibility expectation, ownership, and test fixture.

Do not store live project state, patient-derived data, private identifiers, or
facts that require study-specific approval in a public schema.

`synthetic_experience_exchange_pilot_receipt.schema.json` defines a synthetic,
metadata-only representation of named package identity, hash, receipt,
retrieval, correction, and future-use state. It does not validate a network
transfer, contributor identity, consent, rights, physical device, acceptance,
promotion, deletion, or recall.

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

The historical v0.8.0 pre-C4 source record adds `role_contract.schema.json` and
`controlled_helper_admission.schema.json`. The first describes a non-runnable
review-perspective boundary; the second describes a bounded generic helper
contract. Neither schema creates an agent runtime, grants a tool, authorizes a
task, authorizes data access, confirms a filesystem write, or approves a
Release. Their blank templates are synthetic records, not live state.

The v0.9 integrity-audit source adds `integrity_audit_bundle.schema.json`. It
defines an opt-in finite metadata record containing audit scope, observations,
findings, harness identity, correction/reassessment links, and operational
preflight descriptions. It validates no live repository, receipt, runtime,
hosted Release, source content, data content, authorization, or scientific
fact; it cannot make history append-only or tamper-proof.

The v0.10 release source adds `voluntary_experience_package.schema.json` and five
blank generic record templates. They model only represented scope,
redaction/rights, human review, and correction/withdrawal metadata. They do
not verify identity, consent, rights, privacy, content safety, acceptance,
cross-machine receipt, deletion, or recall.

The v0.11 source adds five Markdown templates under
`assets/manuscript-governance/`. They are blank human-review aids, not new data
schemas or validators. They do not validate manuscript, reviewer, declaration,
route, package, author, policy, or submission facts.

The v1.1 candidate adds five generic future-Study record schemas and matching
blank JSON templates: an execution contract, formal-run manifest, result
manifest, result-authority pointer, and analysis-run QA record. They organize
declared metadata and safe relative references only. They do not execute code,
install dependencies, read data, validate scientific results, prove the
existence or truth of referenced artifacts, or prove that a human approved a
result.

The v1.8 source adds three generic future-Study declared-metadata schemas for
design/classification, governance readiness, and analysis state/freeze. Their
matching templates and explicit validator organize only caller-supplied
records. They do not determine a design, prove governance, authorize access,
approve a freeze, execute analysis, or make a result authoritative.

The v1.15 source adds `joint_review_plan.schema.json` and matching blank JSON
and Markdown templates. They represent only a human-selected review-profile
placeholder, package order, Results work-unit assembly state, and reopen
metadata. They do not select a profile, follow references, inspect a Study or
result, verify a review or decision, rerun work, or make a scientific,
governance, submission, or release determination.
