# v1.21.2 Release Gate

Release remains blocked until the exact main commit passes local and remote
validation, public-boundary review, protected-main review, exact-tag creation,
matching GitHub Release creation, and post-release verification.

The release scope is limited to exact Framework v0.6.0 compatibility. It must
not add an automatic audit route, workspace discovery, source-content read,
report write, cleanup, move, archive, deletion, repair, data access, external
action, or authority transfer.

Before tag creation, verify that the exact intended main commit has a passing
GitHub Actions matrix and that technical immutable-release protection remains
enabled. A merge, local test pass, or CI result alone is not a GitHub Release
or installed-runtime identity.
