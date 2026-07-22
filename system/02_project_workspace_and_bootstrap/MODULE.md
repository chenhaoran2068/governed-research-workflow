# Project Workspace And Bootstrap

The v0.13 V1 Support Scope Matrix is the machine-readable authority for this
module's support posture; this boundary record does not enlarge that scope.

Status: active empty-workspace bootstrap; framework integration validation
only.

The explicit helper in `scripts/bootstrap_empty_workspace.py` creates a generic
empty project scaffold only after preview and matching human approval. Its
current contract is documented in `references/controlled-bootstrap.md`.

It does not create a protocol, copy data, import sources, infer compliance,
advance a Gate, or authorize research execution. The framework
integration test begins only after the framework's separate bootstrap has
created an empty workspace. It does not add an automatic system installer.
Any future installation helper must use a reviewed workspace/system manifest
contract and retain explicit confirmation, no-overwrite, and path-safety
boundaries.
