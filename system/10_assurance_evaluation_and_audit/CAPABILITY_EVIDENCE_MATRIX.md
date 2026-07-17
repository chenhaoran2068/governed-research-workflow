# Capability Evidence Matrix

Status: local `v0.4.0` candidate assurance record. It is not a public release
record and does not admit a `v0.4.0` capability.

The canonical capability facts are in
`../00_manifest_and_profiles/capability_truth_ledger.json`. This matrix maps
those records to expected evidence; it is not a competing capability ledger.

| Capability ID | Target state | Minimum current evidence | Release limitation |
| --- | --- | --- | --- |
| `GRW-CAP-031-01` | Re-admission candidate | Existing routing boundary plus structural tests | Requires exact `v0.4.0` recheck and admission. |
| `GRW-CAP-031-02` | Re-admission candidate | Bootstrap positive and refusal tests | Requires exact `v0.4.0` recheck and admission. |
| `GRW-CAP-031-03` | Re-admission candidate | Exact framework-tag integration test | Does not imply universal compatibility. |
| `GRW-CAP-031-04` | Re-admission candidate | Existing route and structural test | Does not permit auto-promotion. |
| `GRW-CAP-040-00` | Implemented candidate | Ledger structure and refusal tests | The record itself grants no capability. |
| `GRW-CAP-040-01` | Verified candidate | Current/historical release-control tests plus accountable-human implementation review | Remains candidate-only and cannot create a Release or runtime-parity claim. |
| `GRW-CAP-040-02` | Verified candidate | Synthetic Schema, template, and refusal tests | No executor, tool grant, data authority, or public claim. |
| `GRW-CAP-040-03` | Verified excluded | Scope text and no-role-card/agent-runtime tests | Future role cards require a separately reviewed named-role design. |
| `GRW-CAP-040-04` | Verified candidate | Synthetic metadata schema, template, and refusal tests | No data-content handling, access authorization, or compliance claim. |
| `GRW-CAP-040-05` | Verified candidate | Synthetic release-control schema, template, hierarchy, and refusal tests | No tag, Release, hosted-control change, scan, signing, or certification claim. |
| `GRW-CAP-040-06` | Verified candidate | Synthetic cross-record, profile, identity, and refusal tests with a local run record | No runtime-parity, hosted-release, compliance, or publication claim. |

A passing test only verifies the named technical property. It does not approve
science, clinical work, compliance, rights, a project state, a release, or a
submission.
