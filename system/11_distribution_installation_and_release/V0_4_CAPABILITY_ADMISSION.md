# v0.4.0 Capability Admission Record

Status: current unreleased-candidate admission record. No `v0.4.0` tag or GitHub Release
exists. The named capability scope is admitted for a future
exact release, but this is not C4 authorization or a current public-release
claim.

The canonical record is
`../00_manifest_and_profiles/capability_truth_ledger.json`. This file records
the release-control decision boundary, not a second capability truth source.

## Admission Rule

An entry may be admitted for the named `v0.4.0` release scope only when all of
the following are true:

1. its ledger record has `implementation_status: verified`;
2. its ledger record has `release_disposition: admitted`;
3. its ledger record has `public_claim_status: permitted`;
4. its evidence references and claimed interfaces are current for the exact
   candidate commit;
5. its accountable-human approval reference identifies the admission decision.

Admission makes a capability eligible for final-release communication. It does
not create a tag, GitHub Release, normal installation target, runtime claim,
or C4 authorization. Before any public release claim, the final release gate
must separately accept the exact commit, tag, notes, and GitHub Release action.

No passing test, green CI run, branch, candidate record, or AI statement may
substitute for accountable-human admission or final release approval.

## Current Candidate Disposition

On 2026-07-17, the accountable human accepted Option A as the `v0.4.0`
capability-set admission decision. The decision applies to the named scope,
not to a mutable branch identity; final exact-commit evidence and C4 remain
separate requirements. The current ledger state is:

| Record set | Current state | v0.4.0 public status |
| --- | --- | --- |
| `GRW-CAP-031-01` to `GRW-CAP-031-04` | verified and admitted for the named v0.4.0 scope | eligible only for final-release communication after final exact-commit evidence and C4 |
| `GRW-CAP-040-00`, `040-01`, `040-02`, `040-04`, `040-05`, `040-06` | verified and admitted for the named v0.4.0 scope | eligible only for final-release communication after final exact-commit evidence and C4 |
| `GRW-CAP-040-03` | verified explicit exclusion | role cards and agent runtime are not v0.4.0 scope |

The accountable-human implementation reviews for R40-00 through R40-06 prove
that the candidate work packages were reviewed. The subsequent Option A
decision chooses the named capability scope. Neither implementation review nor
capability admission grants C4 authority.

Before C4, refresh exact-commit material, source, dependency, test, profile,
and documentation evidence. The existing `v0.3.1` capabilities remain
historical released baselines, not automatic `v0.4.0` admissions.

## Contradiction Stop

If a current public surface, historical snapshot, ledger field, interface,
evidence reference, or version identity conflicts, do not admit or advertise
the affected capability. Prepare the required bounded decision brief and wait
for the accountable-human choice.
