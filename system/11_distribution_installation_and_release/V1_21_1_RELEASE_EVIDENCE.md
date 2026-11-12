# v1.21.1 Release Evidence

## Candidate Evidence

- Generic naming guidance: `references/study-root-naming.md`.
- Entrypoint boundary: `SKILL.md`.
- Structural and boundary checks: `tests/test_v1_21_1_study_root_naming.py`
  and `tests/test_v1_21_1_release_preparation.py`.

## Before C4

Record the reviewed main commit, passing local suite, passing GitHub Actions
matrix, public-material review, immutable-release setting, and accountable-
human release authorization. Create an annotated `v1.21.1` tag only after C4,
then create a matching GitHub Release and verify the generated source archive.

## Post-Release

Verify that the tag, Release, and source archive resolve to the reviewed main
commit. A runtime adoption receipt must separately record the selected tag,
resolved commit, installation location, and local validation result.
