# Project Workspace And Bootstrap

Status: active empty-workspace bootstrap; candidate framework integration
validation only.

The explicit helper in `scripts/bootstrap_empty_workspace.py` creates a generic
empty project scaffold only after preview and matching human approval. Its
current contract is documented in `references/controlled-bootstrap.md`.

It does not create a protocol, copy data, import sources, infer compliance,
advance a Gate, or authorize research execution. The candidate framework
integration test begins only after the framework's separate bootstrap has
created an empty workspace. It does not add an automatic system installer.
Any future installation helper must use a reviewed workspace/system manifest
contract and retain explicit confirmation, no-overwrite, and path-safety
boundaries.
