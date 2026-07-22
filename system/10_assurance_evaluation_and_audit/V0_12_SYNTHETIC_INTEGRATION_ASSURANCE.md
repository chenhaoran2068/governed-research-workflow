# v0.12 Synthetic Integration Assurance

Status: source-scope assurance record. It does not establish a hosted Release,
installed runtime, or real-world installation result.

## What Is Checked

- the existing bootstrap has a preview followed by matching confirmation;
- existing valid provenance, workflow/evidence, and lesson-promotion fixtures
  remain structurally valid;
- existing manuscript-governance templates remain blank and human-governed;
- a test-owned source snapshot is based on declared tracked paths rather than
  accidental cache, staging, or CI-support files; and
- a temporary copy can be staged, made active, and restored to a prior
  test-owned state without modifying the source tree.

## What Is Not Checked

- real source, data, manuscript, reviewer/editorial, declaration, submission,
  credential, URL, external service, or project material;
- factual truth, citation support, authorization, access, compliance, ethics,
  publication readiness, or submission readiness; and
- private source/runtime identity or a real update/rollback operation.

## Evidence Boundary

The test is one integration-oriented complement to existing module-specific
tests. It does not replace them. A candidate test pass requires full regression
and the existing Windows/Ubuntu/macOS x Python 3.11/3.14 CI matrix before a
later public Release can be considered.
