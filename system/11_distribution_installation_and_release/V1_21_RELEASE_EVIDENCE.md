# v1.21.0 Release Evidence

Status: source-prepared local evidence before remote CI and release identity.

## Local Evidence

- The v1.21 targeted writing-and-route suite passed 6 tests.
- The full package suite passed 449 tests with 3 expected skips before the
  release-source identity update.
- The Shared candidate register passed structural validation and its local
  regression suite passed 4 tests; those private local records are not part of
  the public package.
- Candidate whitespace checks passed.
- Public-boundary review found no real Study path, data, credential, secret,
  manuscript, result, or private local record in the changed public source.

## Remaining Evidence

Before Release, rerun the full suite on the final source commit with the exact
Framework v0.5.0 environment, record the final main commit, verify the remote
matrix, create an annotated `v1.21.0` tag only after C4, create the matching
GitHub Release, and verify tag, Release, source archive, and runtime receipt.

This file does not establish those remote, tag, Release, or installation facts
in advance.
