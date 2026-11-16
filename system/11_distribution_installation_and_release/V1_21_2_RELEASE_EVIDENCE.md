# v1.21.2 Release Evidence

## Candidate Evidence

- Exact Framework contract: `SYSTEM_MANIFEST.yaml`.
- Cross-repository synthetic integration: `tests/test_framework_candidate_integration.py`.
- Compatibility boundary: `tests/test_v1_21_2_framework_v0_6_compatibility.py`.
- Release-control validation: `tests/test_v1_21_2_release_preparation.py`.

## Before C4

Record the reviewed main commit, passing local suite, passing GitHub Actions
matrix, Framework v0.6.0 tag/commit verification, public-material review,
immutable-release setting, and accountable-human release authorization. Create
an annotated `v1.21.2` tag only after C4, then create a matching GitHub Release
and verify the generated source archive.

## Post-Release

Verify that the tag, Release, and source archive resolve to the reviewed main
commit. A runtime adoption receipt must separately record the selected tag,
resolved commit, installation location, Framework v0.6.0 validation target,
and local validation result.
