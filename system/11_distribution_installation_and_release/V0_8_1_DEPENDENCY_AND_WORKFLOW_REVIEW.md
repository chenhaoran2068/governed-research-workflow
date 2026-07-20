# v0.8.1 Dependency And Workflow Review

Status: candidate-only technical-review source. It does not certify a hosted
release, dependency security, C4 authorization, or publication.

## Declared Surface

- the only declared runtime dependency remains `jsonschema==4.26.0`;
- no dependency version, lockfile, Python import, validator behavior, helper,
  schema, template, profile, Framework contract, or CI workflow may change;
- explicitly invoked structural validators require that direct dependency only;
  they do not require the Workspace Framework, optional shared service, or a
  private environment; and
- a later exact candidate must retain SHA-pinned workflow actions and repeat
  the existing Windows, Ubuntu, and macOS CI matrix after separate authorization.

## Required Rechecks

Before C4, compare the exact candidate with immutable `v0.8.0`, inspect every
dependency and workflow path, run focused and full local tests, and obtain
exact-candidate cross-platform CI. Any dependency, workflow, or Framework
contract drift stops this maintenance scope for revised human review.
