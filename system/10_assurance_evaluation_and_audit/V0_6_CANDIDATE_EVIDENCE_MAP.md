# V0.6 Release-Source Evidence Map

Status: v0.6 release-source evidence map. It is not the canonical capability
truth ledger, C4 authorization, a hosted Release, or an installed-runtime
record. The accountable-human admission is recorded separately in the
canonical ledger and `V0_6_CAPABILITY_ADMISSION.md`.

## Admitted Capability Scope

| Capability | Scope status | Interfaces | Evidence boundary |
| --- | --- | --- | --- |
| `GRW-CAP-060-01` Reviewable Workflow And Evidence Control Records | Verified and admitted for the named v0.6.0 release scope | Bundle schema, baseline schema, blank templates, read-only validator, synthetic fixtures, reference guide, and regression tests | Exact-source review, local regression, synthetic positive/refusal/path-safety/revision-impact checks, framework `v0.1.2` integration, public-material and dependency review, remote CI, and a separate C4 decision are distinct release evidence. |

## Scope Boundary

The bundle can assess only explicitly supplied JSON record structure
and declared relationships under a caller-provided review root. A pass does not
prove source truth, citation entailment, human identity, actual authorization,
data availability, compliance, Gate passage, submission readiness, release
readiness, or tamper-proof history.

The map must be updated or superseded if the admitted scope or its source-level
evidence changes. The existing admission applies only to the named v0.6.0
release scope. Neither this map nor any source file establishes public
availability: users must resolve a selected version through its exact tag and
matching GitHub Release before treating it as an installation target.
