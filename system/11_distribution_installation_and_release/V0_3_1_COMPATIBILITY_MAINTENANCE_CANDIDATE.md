# v0.3.1 Compatibility Maintenance Candidate

Status: release-gated public source on `main`. It is not a public release, tag,
or normal installation target until an exact annotated `v0.3.1` tag and a
matching GitHub Release exist. It is no longer a branch that is separate from
`main`, and its merge into `main` did not itself authorize a release or any
change to a real research project.

## Purpose

Prepare a narrowly scoped patch release after the published v0.3.0
source-branch documentation was found to retain stale wording that described
the already released system foundation as an unreleased candidate. The
release-gated source also replaces its prospective framework-integrated claim
with a new test against the exact released Governed Research Workspace
Framework v0.1.1 tag.

Historical v0.3.0 evidence remains evidence only for v0.3.0 and framework
v0.1.0. It must not be reused as evidence for this candidate.

## Intended Scope

- Correct current-branch release-status wording without rewriting the published
  v0.3.0 tag.
- Set SYSTEM_MANIFEST.yaml to release-gated version 0.3.1 while preserving its
  workspace framework-contract version at 0.1.0. Record framework release tag
  v0.1.1 and commit b0e32d7710b70299e633df1316b6924cd87b647b as the exact
  test subject in the compatibility evidence.
- Retest the synthetic framework-integrated profile against tag v0.1.1 and its
  resolved commit.
- Preserve the existing standalone profile, thin entry, controlled empty
  bootstrap boundary, human approvals, no-data-access boundary, and historical
  release records.

This candidate does not add an agent runtime, data-processing helper,
scientific-analysis capability, compliance determination, project migration,
automatic release, or submission capability.

## Required Evidence Before A Patch Release Decision

1. The full local regression suite passes with the exact framework v0.1.1
   checkout and the integration environment variables set.
2. The cross-platform GitHub Actions matrix passes for the exact candidate
   commit, including the exact v0.1.1 checkout.
3. README, roadmap, system manifest, module index, CI configuration, tests,
   intended tag, release notes, and compatibility statement are reviewed for a
   consistent version and framework claim.
4. A fresh tracked-tree and reachable-history public-material, rights, and
   secret review is completed for the final candidate commit.
5. An accountable human maintainer reviews the exact final diff and decides
   whether to create a new annotated tag and GitHub Release.

Until all five items are complete, the current public installation target is
the latest published tag. This source must not be presented as released or as
support for framework v0.1.1 outside the stated synthetic validation boundary.
