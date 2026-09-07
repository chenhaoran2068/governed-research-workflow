# Governed Research Workflow v1.18.0

v1.18.0 derives from immutable v1.16.0 and contains two additions.

## Study Status

`GRW-CAP-250-01` absorbs the accepted but unpublished v1.17 Study-status
candidate. It provides a blank snapshot, 11-stage catalogue, structural
schema, read-only validator, and synthetic fixtures. No v1.17 Git tag or
GitHub Release was published.

## Paper Repository Governance

`GRW-CAP-260-01` adds:

- Paper Repository Standard v0.1;
- four release profiles;
- blank README, data-access, citation, release-manifest, export-scope, review,
  and ignore templates;
- release-manifest and export-scope schemas;
- an explicit file-only allowlist builder that writes to a new directory and
  refuses overwrite;
- a read-only candidate validator and synthetic regression tests.

## Boundaries

This release does not inspect or modify a real Study, determine Study status,
grant data access, decide privacy or rights, create a GitHub repository,
initialize Git, commit, push, tag another repository, publish a paper package,
archive a release, or approve publication. A structural or automated check is
not proof of scientific correctness, privacy, rights, authorship, or human
authorization.
