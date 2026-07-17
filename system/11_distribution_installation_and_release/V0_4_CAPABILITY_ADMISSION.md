# v0.4.0 Capability Admission Record

Status: local candidate control record. No `v0.4.0` tag or GitHub Release
exists, and no `v0.4.0` capability is admitted by this file.

The canonical record is
`../00_manifest_and_profiles/capability_truth_ledger.json`. This file records
the release-control decision boundary, not a second capability truth source.

## Admission Rule

An entry may be admitted for the exact `v0.4.0` release only when all of the
following are true:

1. its ledger record has `implementation_status: verified`;
2. its ledger record has `release_disposition: admitted`;
3. its ledger record has `public_claim_status: permitted`;
4. its evidence references and claimed interfaces are current for the exact
   candidate commit;
5. its accountable-human approval reference identifies the admission decision;
   and
6. the final release gate accepts the exact commit, tag, notes, and GitHub
   Release action.

No passing test, green CI run, branch, candidate record, or AI statement may
substitute for accountable-human admission or final release approval.

## Current Candidate Disposition

All entries currently have `public_claim_status: forbidden`. The exact current
ledger state is:

| Record set | Current state | v0.4.0 public status |
| --- | --- | --- |
| `GRW-CAP-031-01` to `GRW-CAP-031-04` | verified re-admission candidates | not automatically re-admitted from `v0.3.1` |
| `GRW-CAP-040-00`, `040-01`, `040-02`, `040-04`, `040-05`, `040-06` | verified local candidates | not admitted and cannot yet be publicly claimed |
| `GRW-CAP-040-03` | verified explicit exclusion | role cards and agent runtime are not v0.4.0 scope |

The accountable-human implementation reviews for R40-00 through R40-06 prove
only that the local candidate work packages were reviewed. They do not choose
the final public capability set, convert `candidate` to `admitted`, or grant
C4 authority.

The candidate-admission decision occurs only after an exact candidate commit
exists and the release gate's current material, source, dependency, test,
profile, and documentation evidence has been refreshed. The decision must name
each admitted ID, retain each excluded ID, and record the accountable-human
admission reference in the canonical ledger. The existing `v0.3.1`
capabilities remain historical released baselines, not automatic `v0.4.0`
admissions.

## Contradiction Stop

If a current public surface, historical snapshot, ledger field, interface,
evidence reference, or version identity conflicts, do not admit or advertise
the affected capability. Prepare the required bounded decision brief and wait
for the accountable-human choice.
