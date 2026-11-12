# v1.21.1 Release Gate

Release remains blocked until the exact main commit passes local and remote
validation, public-boundary review, protected-main review, exact-tag creation,
matching GitHub Release creation, and post-release verification.

The release scope is limited to generic new-Study-root naming documentation.
It must not add a root-discovery mechanism, bootstrap automation, real Study
material, data, credentials, external action, or authority transfer.

Before tag creation, verify that the exact intended main commit has a passing
GitHub Actions matrix and that the repository's technical immutable-release
setting remains enabled. A merge, local test pass, or CI result alone is not a
GitHub Release or installed-runtime identity.
