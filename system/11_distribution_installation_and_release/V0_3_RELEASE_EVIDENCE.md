# v0.3.0 Release Evidence Record

Status: pre-release candidate evidence. This record is not an authorization to
merge, tag, or publish. It must be refreshed against the final proposed
release commit before R30-G6.

## Release Identity Under Review

| Field | Candidate value |
| --- | --- |
| Package | governed-research-workflow |
| Intended version | v0.3.0 |
| Candidate branch | v0.3.0-system-foundation |
| Intended scope | bounded system foundation; not a complete research platform |
| Framework compatibility | exact released governed-research-workspace-framework v0.1.0 |
| Release assets | GitHub-generated source archives only; no binary, data, or research asset |

## Gate Status

### R30-G1: Scope And Contract Freeze

Status: candidate evidence prepared; final content review required before
R30-G6.

Evidence:

- README.md, ROADMAP.md, system/INDEX.md, and SYSTEM_MANIFEST.yaml identify
  the candidate as a bounded v0.3.0 system foundation.
- V0_3_RELEASE_GATE.md lists the public interface and explicitly excludes
  clinical-data processing, specialist agents, autonomous scientific judgment,
  submission authority, and automatic system installation.
- Module 05 and module 08 remain foundation-only and are excluded from the
  release claim.
- INSTALL_UPDATE_ROLLBACK.md identifies profile behavior and public package
  lifecycle boundaries.
- Candidate documentation audit completed at
  503e270ef1ad852512b524bb4a9345c02d5f27ad.

Next action: review the final release diff and use the same bounded language
in the GitHub Release notes.

### R30-G2: Public Material And Rights Boundary

Status: candidate technical review complete; maintainer rights confirmation is
required during R30-G6.

Evidence:

- PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.0.md records tracked-tree coverage,
  reviewed material classes, exceptions, scan results, and limits.
- .gitignore, CONTRIBUTING.md, SECURITY.md, and SKILL.md prohibit private,
  restricted, and real-project content.
- The current-tree and 16-commit reachable-history pattern scans reported zero
  credential and known-private-path matches at
  503e270ef1ad852512b524bb4a9345c02d5f27ad.

Next action: accountable maintainer confirms contribution authority and no
applicable institutional, DUA, privacy, employment, or confidentiality block.

### R30-G3: Installation And Profile Contract

Status: candidate evidence prepared; final command recheck required before
R30-G6.

Evidence:

- INSTALL_UPDATE_ROLLBACK.md documents manual standalone and
  framework-integrated installation, update, rollback, validation, and stop
  conditions.
- The document explicitly excludes automatic installation, migration, data
  import, and automatic repair.
- The root SYSTEM_MANIFEST.yaml is the expected framework system-manifest
  location and declares standalone plus framework_integrated against Framework
  0.1.0.
- An isolated lifecycle test cloned candidate
  503e270ef1ad852512b524bb4a9345c02d5f27ad, ran 23 tests successfully,
  rolled back to released v0.2.1 and ran 14 tests successfully, then restored
  the candidate and reran all 23 tests successfully.

Next action: execute the documented clean-install and rollback commands from
the final release candidate in a temporary directory.

### R30-G4: Behavioral And Compatibility Evidence

Status: candidate evidence available; rerun is required on the final intended
main commit.

Evidence:

- Local test suite: python -m unittest discover -s tests -v.
- Candidate GitHub Actions matrix: Windows, Ubuntu, and macOS on Python 3.11
  and 3.14.
- Exact-tag framework integration test checks out Framework v0.1.0, creates
  a synthetic empty framework workspace, installs synthetic public package
  material, validates manifests, and exercises unsafe-path, wrong-profile,
  version-mismatch, and unregistered-primary-system refusals.
- Candidate GitHub Actions run 29396558104 completed successfully for all six
  matrix cells on commit 503e270ef1ad852512b524bb4a9345c02d5f27ad:
  Windows, Ubuntu, and macOS on Python 3.11 and 3.14.

Limit: the tests prove only the listed technical behavior. They do not prove
scientific quality, compliance, data access, real project safety, or every
agent/runtime compatibility.

Next action: record the final main CI URL and local command result.

### R30-G5: Release Integrity And Security Review

Status: candidate policy and review record prepared; final clean-tree and
security-alert check required before R30-G6.

Evidence:

- RELEASE_INTEGRITY_POLICY_v1.md records action pinning, dependency scope,
  secret-review limits, release identity rules, and the immutable-release
  decision for v0.3.0.
- GitHub Actions uses SHA-pinned official checkout and setup-python actions
  with read-only contents permission.
- The release will include no assets beyond GitHub source archives.
- GitHub alert APIs were checked with maintainer credentials during candidate
  review. Dependabot returned 403, code scanning returned 404, and secret
  scanning was unavailable to the current credential; therefore no claim is
  made that hosted scanning is enabled or clear.

Next action: run the final history/tree scan, inspect accessible GitHub alerts,
verify clean status, and approve or reject the candidate integrity evidence.

### R30-G6: Human Release Decision

Status: pending. No AI, script, test, or candidate document can satisfy this
gate.

Required decision: named accountable maintainer authorizes the exact merge
commit, v0.3.0 annotated tag, and GitHub Release only after G1-G5 are
refreshed and accepted.

### R30-G7: Post-Release Verification

Status: not applicable until a real release exists.

Required evidence: the release tag resolves to the intended tested main
commit; the GitHub Release and source archive reference that tag; and the
candidate branch retention or deletion decision is recorded.
