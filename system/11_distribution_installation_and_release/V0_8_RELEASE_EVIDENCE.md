# v0.8.0 Release Evidence: Pre-C4 Review Record

Status: pre-C4 review record. It preserves historical implementation and
protected-main evidence, records release-scope admission, and identifies what
must be repeated for the later exact C4 release object. It is not C4
authorization, a tag, a GitHub Release, a normal installation target, or an
installed-runtime statement.

## Current Preparation Context

| Field | Recorded pre-C4 value |
| --- | --- |
| Intended version | `v0.8.0` |
| Public baseline | `v0.7.1`, commit `39d88408c2059d4c736303a1ae9aa509797c3ad4` |
| Historical implementation commit | `49102f9da068b290e311f63437351d1e1ce220e7` |
| Reviewed protected-main commit | `d896a3f455b37e8c8d757db3687b8b6f13e84d4e` |
| Intended framework identity | `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |
| Intended capability set | `GRW-CAP-080-01`, `GRW-CAP-080-02`, and `GRW-CAP-080-03` only |
| Exact C4 release identity | deliberately recorded outside this source tree by a separate C4 record; source files cannot truthfully self-identify a future Git commit |

## Historical Implementation And Protected-Main Evidence

- The complete local suite passed with `162` tests after the source-identity
  repair, including framework-integrated tests.
- GitHub Actions run `29680656435` passed the six required contexts: Windows,
  Ubuntu, and macOS, each with Python 3.11 and 3.14.
- The controlled-helper admission repair changed no helper behavior. It binds
  source text with `sha256_utf8_lf_v1`; the canonical helper hash at the
  implementation commit is
  `603aed58d0aed8ea1d76f23082b5d819d7c4f200906253e60766cf5572f42f63`.
- The historical implementation diff contains generic Markdown,
  JSON, JSON Schema, and Python test material only. It contains no dependency
  manifest or CI workflow change, submodule, Git LFS object, symlink, or
  binary artifact.

## Required Refresh Before C4

The following cannot be inherited from a prior reviewed commit when this source
or its release-preparation materials are added or changed:

1. a separate C3 record naming the clean exact corrective-source identity,
   staged tracked-source snapshot, and reviewed diff;
2. complete local test result on that exact source;
3. six-context CI result for that exact source;
4. public-material, rights, privacy, secret, dependency, workflow, and
   protected-main review for that exact source;
5. verification that the recorded accountable-human capability admission still
   matches the exact final scope; and
6. C4 approval naming the post-merge commit, tag, notes, and Release action.

The separate release-control record at
`V0_8_RELEASE_CONTROL_CANDIDATE.json` is intentionally pre-C4 until those
items are resolved. A passing local or hosted CI run is not a Release claim.
