# v0.8.0 Capability Admission Record

Status: pre-C4 accountable-human release-scope admission record.
On 2026-07-19, the accountable human reviewed pull request #10 and accepted
the three-item v0.8.0 scope below. The resulting release-scope admission is
separate from C4 and does not establish a tag, GitHub Release, installation
target, or runtime identity.

## Admitted Exact Scope

| Capability | Admitted disposition | Bound public meaning |
| --- | --- | --- |
| `GRW-CAP-080-01` | admit | Structural evidence that only `standalone` and `framework_integrated` are public profiles, with bounded failure behavior and no private-service requirement. |
| `GRW-CAP-080-02` | admit | Two documentation-only, report-only, non-runnable role-contract records for supplied bounded review. |
| `GRW-CAP-080-03` | admit | A metadata admission record for the already released controlled empty-workspace bootstrap helper. |

No additional `GRW-CAP-080-*` capability is in the v0.8.0 release scope.

## Explicit Exclusions

v0.8.0 does not admit a runnable role card, agent runtime, coordinator,
external-evidence retrieval role, delegated authority, multi-agent
orchestration, hidden background work, generic writer, new helper, data action,
network action, credential use, release action, installation action, or public
Private Lab Extended profile.

## Historical C4 Boundary

This admission is recorded in the capability ledger and the v0.8 pre-C4
release-control record. It remains separate from C4: it cannot merge a pull
request, create an immutable tag, create a GitHub Release, or install any
local runtime. A later C4 review must name the exact final main commit, tag,
Release notes, material/rights evidence, CI evidence, and post-release plan.

If any proposed capability is excluded or changed, update the ledger, release
gate, release-control record, documentation, and affected tests before another
review. Do not silently substitute a broader capability.
