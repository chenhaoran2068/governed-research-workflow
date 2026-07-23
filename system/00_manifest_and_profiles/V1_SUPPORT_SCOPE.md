# V1 Support Scope

## Purpose

`v1_support_scope_matrix.json` is the sole machine-readable authority for the
module-level public V1 support posture of this package. It covers all thirteen
public modules and distinguishes a bounded supported surface from an external
boundary or a function excluded from V1.

The matrix does not replace the capability truth ledger. Use
`capability_truth_ledger.json` to determine whether one named capability has a
verified promise, non-promise, evidence, and admission state. Use the release
verification records to determine whether an exact tag has a matching GitHub
Release. Use a controlled installation receipt to determine what a local
runtime actually loads. Use project records and an accountable human for any
project, data, Gate, manuscript, compliance, or submission decision.

`matrix_status` describes frozen V1 contract maturity, not public-release
state. Its `interface_frozen` value means this source declares the v1 public
interface stable for review and release preparation. It does not state that a
v1 tag or GitHub Release already exists. Only selected-version release
verification records establish that public-release fact. A future modification
to this frozen contract requires separately reviewed evidence and a later
immutable release.

## Reading A Module Record

- `active_bounded` means only the named `bounded_surfaces` are public support
  candidates. It does not mean that every file or noun under a module is a
  supported capability.
- `external_boundaries` name functions that require a separate accountable
  human, project authority, current external source, or controlled process.
- `v1_exclusions` name functions that are not part of the public V1 contract.
- `known_limitations` and `refusal_statement` prevent a structural description
  from being read as truth, access, compatibility, release, or project approval.

When documentation conflicts with the matrix, do not choose a version by
convenience. Stop the affected support claim, identify the exact records and
unknowns, describe repair options and tradeoffs, and request accountable-human
resolution. The matrix itself does not decide that conflict.

## Profiles, Compatibility, And Migration

The only public profiles are `standalone` and `framework_integrated`. The
matrix introduces no profile, dependency, bootstrap behavior, validator
behavior, runtime route, data action, or migration executor. A v0.12 user need
not migrate a metadata bundle, project, or runtime merely to read this matrix.

Framework-integrated use remains subject to the exact framework contract and
its separately recorded validation. A public source tree does not prove that a
private workspace or installed runtime has been updated.

## Maintenance

The accountable maintainer owns changes to the matrix. A material revision to a
module posture, supported surface, boundary, capability reference, schema, or
claim surface requires affected-scope review under the package release controls
and M48. A correction after an immutable public Release requires a later
reviewed maintenance version; do not alter historical tags or Releases.

## What This Does Not Do

The matrix does not provide a data handler, source library, retrieval service,
agent runtime, coordinator, generic writer, installer, migration executor,
recovery executor, Release action, local-runtime replacement, or real-study
workflow executor. It is a structural support contract, not an execution or
approval mechanism.
