# v0.8.0 Capability Admission Proposal

Status: accountable-human scope acceptance recorded on 2026-07-19. The
accountable human accepted the three-item proposed v0.8.0 scope below. Exact
release-scope admission remains pending until a separate C3 record names a
clean candidate commit and its refreshed evidence and exact-tree review exist.
This document does not create an exact candidate commit, pull request, tag,
GitHub Release, installation target, or runtime identity.

## Proposed Exact Scope

| Capability | Proposed disposition | Bound public meaning |
| --- | --- | --- |
| `GRW-CAP-080-01` | admit | Structural evidence that only `standalone` and `framework_integrated` are public profiles, with bounded failure behavior and no private-service requirement. |
| `GRW-CAP-080-02` | admit | Two documentation-only, report-only, non-runnable role-contract records for supplied bounded review. |
| `GRW-CAP-080-03` | admit | A metadata admission record for the already released controlled empty-workspace bootstrap helper. |

No additional `GRW-CAP-080-*` capability is proposed for v0.8.0.

## Explicit Exclusions

v0.8.0 does not admit a runnable role card, agent runtime, coordinator,
external-evidence retrieval role, delegated authority, multi-agent
orchestration, hidden background work, generic writer, new helper, data action,
network action, credential use, release action, installation action, or public
Private Lab Extended profile.

## Decision Boundary

The accountable human has accepted this proposed scope, but the capability
ledger and release-control record must not yet show a named v0.8.0
release-scope admission. They may be updated only after the candidate evidence
named by the separate C3 record is reviewed. That later admission remains
separate from C4: it cannot merge a pull request, create an immutable tag,
create a GitHub Release, or install any local runtime.

If any proposed capability is excluded or changed, update the ledger, release
gate, release-control record, documentation, and affected tests before another
review. Do not silently substitute a broader capability.
