# Project Workspace And Bootstrap

Status: active empty-workspace bootstrap; framework integration foundation only.

The explicit helper in `scripts/bootstrap_empty_workspace.py` creates a generic
empty project scaffold only after preview and matching human approval. Its
current contract is documented in `references/controlled-bootstrap.md`.

It does not create a protocol, copy data, import sources, infer compliance,
advance a Gate, or authorize research execution. A future framework-integrated
bootstrap must use a reviewed workspace/system manifest contract and retain the
same preview, confirmation, no-overwrite, and path-safety boundaries.
