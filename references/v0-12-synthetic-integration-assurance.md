# v0.12 Synthetic Integration Assurance

v0.12 adds no runtime interface. It is an assurance-maintenance release that
composes already released bounded controls with existing synthetic fixtures.

The regression path validates only documented structure and test-owned file
lifecycle behavior. It uses the existing controlled empty-workspace bootstrap,
metadata-only provenance-register-set validator, workflow/evidence-control
validator, lesson-promotion-control validator, and blank manuscript-governance
templates. Each component retains its own limits.

The test-owned update/rollback simulation is deliberately not a runtime
installer. A public source tree, private canonical source, installed runtime,
installation receipt, and rollback backup remain different identities. Actual
adoption requires a separately approved controlled installation, content hash,
receipt, backup, and fresh-process validation.

The scenario rejects missing bootstrap confirmation and keeps invalid or
unknown structural records from becoming an access, compliance, Gate, Release,
or submission approval. A successful result remains synthetic evidence only.
