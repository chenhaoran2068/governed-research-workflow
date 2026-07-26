# Controlled Empty-Workspace Bootstrap

Use `scripts/bootstrap_empty_workspace.py` only when the user explicitly asks
to create a new empty workspace and has selected an existing destination
directory outside the skill package.

The helper requires Python 3.11 or later and uses only the Python standard
library. It is designed to avoid platform-specific behavior. Public support is
claimed only for platforms that have passed the repository test matrix.

## Required Interaction

1. Identify the workspace root, title, and safe workspace ID. Do not search
   drives or choose a location for the user. Supply an explicit ID when a
   human-readable directory name matters; a non-ASCII-only title otherwise
   receives a stable hash-suffixed fallback ID.
2. Run a no-write preview. Running without `--confirm-create` is a preview.
3. Explain the plan and wait for an accountable human to approve that exact
   plan.
4. Rerun only with `--confirm-create`, the exact previewed `--plan-id`, and a
   nonempty `--approval-reference`.
5. Read the resulting receipt and report that a scaffold exists. Do not treat
   the receipt as a passed workflow Gate or permission for consequential work.

Example preview on Windows:

```powershell
python scripts/bootstrap_empty_workspace.py `
  --workspace-root C:\ResearchWorkspaces `
  --title "Example Study" `
  --workspace-id example-study
```

Example preview on Linux or macOS:

```bash
python3 scripts/bootstrap_empty_workspace.py \
  --workspace-root ~/research-workspaces \
  --title "Example Study" \
  --workspace-id example-study
```

The output contains `plan.plan_id`. After human approval, use the same inputs:

```bash
python3 scripts/bootstrap_empty_workspace.py \
  --workspace-root ~/research-workspaces \
  --title "Example Study" \
  --workspace-id example-study \
  --confirm-create \
  --plan-id <previewed-plan-id> \
  --approval-reference <accountable-approval-reference>
```

The reviewed plan also binds the filesystem identity of the selected workspace
root. Replacing that directory, even with another ordinary directory at the
same path, changes the plan and requires a new preview and approval.

## Output Boundary

The helper creates only this generic empty layout:

```text
<workspace-root>/<workspace-id>/
  00_state/
  01_intake/
  02_registry/
  03_protocol/
  04_knowledge/
  05_memory/retrospective/
  06_data/
  07_analysis/
    00_contract/
    01_environment/
    02_configuration/
    03_implementation/
    04_tests/
    05_runs/
    06_development/
  08_results/
    _manifests/
    runs/
  09_manuscript/
  10_submission/
  11_qa/
    analysis_runs/
  12_archive/
```

It also creates a root README, an initial `00_state/workspace_state.json`,
`07_analysis/00_contract/analysis_execution_contract.json`,
`08_results/_manifests/current_result_authority.json`, and
`00_state/bootstrap_receipt.json`. The two analysis/result records are blank
metadata templates: they declare no selected execution path and no
authoritative result. The receipt hashes the generated files other than itself.

It never copies or reads source data, imports papers, contacts a network
service, discovers credentials, creates analysis or manuscript content,
installs or changes dependencies, makes an ethics/compliance assertion,
advances a workflow Gate, or creates a submission route.

## Refusal And Failure Behavior

The helper refuses an invalid Python version, non-existent or linked workspace
root (including a Windows reparse point), a root whose identity changed after
preview, a destination inside the skill package, invalid workspace ID, an
existing workspace, a changed plan, missing approval reference, path escape,
overwrite, or resume request.

It builds the scaffold in a same-parent staging directory. If construction
fails, it removes only the staging directory it created and does not leave a
final workspace root. If the staging path itself becomes a link or reparse
point, it refuses recursive cleanup rather than risk traversing it.
