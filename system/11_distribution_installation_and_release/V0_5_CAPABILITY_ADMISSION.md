# v0.5.0 Capability Admission Record

Status: candidate decision record. `GRW-CAP-050-01` is verified candidate
content with public claim forbidden. It is not admitted for a release, is not
C4 authorization, and does not create a tag, GitHub Release, installation
target, runtime claim, or public availability statement.

## Admission Rule

`GRW-CAP-050-01` may be admitted for one exact `v0.5.0` release only when:

1. its ledger record is `implementation_status: verified`;
2. its ledger record has current evidence and interface references for the
   exact candidate commit;
3. the final material, dependency, workflow, documentation, and CI review are
   complete for that same commit; and
4. an accountable human explicitly records admission or exclusion after seeing
   the exact capability scope and residual risks.

Admission makes the named capability eligible for final-release communication.
It does not create C4 authorization or any live release/install/runtime claim.
No passing test, green CI run, candidate branch, or AI statement substitutes
for accountable-human admission.

## Candidate Disposition

| Capability | Candidate state | Current public status |
| --- | --- | --- |
| `GRW-CAP-050-01` | verified candidate, pending exact-commit review | forbidden until an accountable human admits it for the named exact release and separately authorizes C4 |

## Contradiction Stop

If the ledger, README, roadmap, schema, validator, tests, candidate evidence,
or version identity conflict, do not admit or advertise the capability. Present
the evidence, unresolved items, and bounded alternatives to the accountable
human for decision.
