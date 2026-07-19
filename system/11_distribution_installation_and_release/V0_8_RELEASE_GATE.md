# v0.8.0 Portability, Role-Contract, And Helper-Admission Release Gate

Status: pre-C4 release-gate record. It records the evidence and
scope reviewed before a later C4 decision. It does not identify the final
release commit, authorize C4, create a tag or GitHub Release, or establish a
local installation or runtime identity.

## Intended Scope

The release-scope-admitted v0.8.0 scope contains exactly these three bounded
capabilities:

- `GRW-CAP-080-01`: profile-scoped portability and failure-boundary evidence
  for the public `standalone` and `framework_integrated` profiles only;
- `GRW-CAP-080-02`: two non-runnable, report-only role-contract records,
  `record_validation_reviewer` and `audit_boundary_reviewer`; and
- `GRW-CAP-080-03`: a bounded admission record for the existing
  `bootstrap_empty_workspace.py` helper.

It does not add a helper, modify the bootstrap helper, grant a role authority,
provide a role card or agent runtime, coordinate agents, delegate work, access
data, contact an external service, use credentials, or update a local runtime.
`Private Lab Extended` remains outside the public profile contract.

## Required Gates

### P80-G1: Exact Source And Compatibility Identity

- Historical implementation evidence refers to candidate commit
  `49102f9da068b290e311f63437351d1e1ce220e7`, based on public `v0.7.1`
  commit `39d88408c2059d4c736303a1ae9aa509797c3ad4`.
- The protected-main review later passed for
  `d896a3f455b37e8c8d757db3687b8b6f13e84d4e`. A later C4 record must name
  the exact final release identity after any subsequent corrective source
  change; package source files do not self-identify that future commit.
- Published v0.4 through v0.7 records, schemas, templates, and released
  capability meanings remain readable without migration or rewrite.

### P80-G2: Capability Admission And Claim Truth

- The accountable human admitted `GRW-CAP-080-01` through `GRW-CAP-080-03`
  for the named v0.8.0 release scope after reviewing pull request #10.
- This release-scope admission is recorded in the capability ledger and does
  not establish a hosted Release or installed runtime.
- Admission is distinct from C4 authorization, an exact tag, a GitHub Release,
  installation eligibility, and runtime identity.

### P80-G3: Public Material, Rights, Privacy, And Boundary Review

- Review the exact tracked tree, newly reachable history, Git LFS objects,
  submodules, generated archives, and planned Release assets.
- Stop if any credential, key, private absolute path, real project material,
  restricted data, unpublished manuscript, personal record, or unreviewed
  third-party payload appears.
- The accountable human must confirm Apache-2.0 publication authority for the
  exact generic tree. A test, GitHub setting, or AI statement cannot supply
  that authority.

### P80-G4: Contract And Helper-Boundary Integrity

- Role contracts must remain documentation-only, report-only, and
  non-runnable. They cannot substitute for M53 authorization, data/share
  evidence, helper admission, or per-run write confirmation.
- The helper-admission record must identify only the existing bootstrap helper,
  keep its supported public profiles exact, preserve its refusal and recovery
  boundaries, and bind source text through the declared canonical hash
  algorithm.
- Positive and negative tests must reject unsupported profiles, role-runtime
  claims, role-as-approval claims, generic-writer claims, unsafe helper source
  identities, invalid UTF-8 source text, and CRLF/LF identity drift.

### P80-G5: Technical, Dependency, And Cross-Repository Evidence

- Re-run the complete local suite after the final release source is staged.
- Re-run the exact final release source through GitHub CI on Windows, Ubuntu, and
  macOS with Python 3.11 and 3.14.
- Any framework-integrated claim must remain bound to Workspace Framework
  `v0.1.2` at commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.
- Review the fixed runtime dependency, SHA-pinned GitHub Actions, dependency
  alert availability, and repository protection evidence. Disabled or
  unavailable security checks remain visible residual risks, not passes.

### P80-G6: Protected Main, C4, And Post-Release Verification

- `main` must be reached through its protected pull-request route with all six
  required CI contexts and resolved conversations.
- A later C4 package must name the exact post-merge commit, `v0.8.0` tag,
  reviewed Release notes, capability admission, release-control record,
  material/rights review, CI evidence, residual risks, and post-release plan.
- Only a separately recorded accountable-human C4 decision can authorize an
  immutable tag and matching GitHub Release.
- Afterwards independently verify the hosted tag, Release, notes, archive,
  source identity, and protected-main result. Local runtime adoption remains a
  separate controlled task.
