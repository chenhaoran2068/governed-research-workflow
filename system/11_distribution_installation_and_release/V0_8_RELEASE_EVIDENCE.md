# v0.8.0 Release Evidence: Active Candidate Preparation Record

Status: active candidate-preparation record. It preserves evidence collected
for the v0.8 implementation candidate and identifies what must be repeated for
the later exact release candidate. It is not C4 authorization, a tag, a GitHub
Release, a normal installation target, or an installed-runtime statement.

## Current Preparation Context

| Field | Value at preparation review |
| --- | --- |
| Intended version | `v0.8.0` |
| Public baseline | `v0.7.1`, commit `39d88408c2059d4c736303a1ae9aa509797c3ad4` |
| Implementation candidate commit | `49102f9da068b290e311f63437351d1e1ce220e7` |
| Candidate branch | `v0.8.0-portability-role-helper-admission-candidate` |
| Intended framework identity | `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |
| Intended capability set | `GRW-CAP-080-01`, `GRW-CAP-080-02`, and `GRW-CAP-080-03` only |
| Exact C3 candidate identity | deliberately recorded outside this source tree by a separate C3 record; source files cannot truthfully self-identify a future Git commit |

## Evidence Collected For The Implementation Candidate

- The complete local suite passed with `162` tests after the source-identity
  repair, including framework-integrated tests.
- GitHub Actions run `29680656435` passed the six required contexts: Windows,
  Ubuntu, and macOS, each with Python 3.11 and 3.14.
- The controlled-helper admission repair changed no helper behavior. It binds
  source text with `sha256_utf8_lf_v1`; the canonical helper hash at the
  implementation commit is
  `603aed58d0aed8ea1d76f23082b5d819d7c4f200906253e60766cf5572f42f63`.
- The candidate-to-baseline implementation diff contains generic Markdown,
  JSON, JSON Schema, and Python test material only. It contains no dependency
  manifest or CI workflow change, submodule, Git LFS object, symlink, or
  binary artifact.

## Required Refresh Before C4

The following cannot be inherited from the implementation commit when
release-preparation materials are added or changed:

1. a separate C3 record naming the clean exact-candidate identity, staged
   tracked-source snapshot, and candidate-to-baseline diff;
2. complete local test result on that exact source;
3. six-context CI result for that exact source;
4. public-material, rights, privacy, secret, dependency, workflow, and
   protected-main review for that exact source;
5. accountable-human capability admission or explicit exclusion; and
6. C4 approval naming the post-merge commit, tag, notes, and Release action.

The separate release-control record at
`V0_8_RELEASE_CONTROL_CANDIDATE.json` is intentionally incomplete until those
items are resolved. A passing implementation CI run is not a release claim.
