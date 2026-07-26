# Future Study Execution And Reproducibility Contract

This reference defines a generic, metadata-only contract for a **future**
Study. It is a public template and boundary guide, not an analysis pipeline,
environment installer, research executor, result-approval mechanism, or
evidence of a real Study.

Use it only after an accountable human has selected the project-specific
workflow and authorized the relevant action. A generated empty workspace,
template field, structural validation result, or `approval_reference` field
does not itself prove that authorization exists.

## Generic Layout

The existing controlled bootstrap helper may create these empty child
directories for a new workspace:

```text
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
11_qa/
  analysis_runs/
```

This layout is a generic organization aid. It does not require Python, R, SQL,
or any specific workflow engine, filename, analysis stage, data model, or
scientific method. It does not migrate an existing Study.

## Five Record Types

| Record | Typical location | Purpose | Does not prove |
| --- | --- | --- | --- |
| `analysis_execution_contract` | `07_analysis/00_contract/` | Declares one future Study's selected formal execution path and environment/result policies. | Human approval, a runnable environment, or permission to execute. |
| `formal_run_manifest` | `07_analysis/05_runs/<run_id>/` | Identifies one non-overwriting formal run and its declared inputs and configuration evidence. | That a run occurred correctly or that its outputs are authoritative. |
| `result_manifest` | `08_results/runs/<run_id>/` | Identifies candidate output artifacts for one run. | That artifacts are valid, publishable, or approved. |
| `analysis_run_qa_record` | `11_qa/analysis_runs/<run_id>/` | Records bounded QA status and issues for a named run. | A human authority decision or scientific validity. |
| `current_result_authority` | `08_results/_manifests/` | Points to the run, result, QA, and human-decision records required before a result can be named authoritative. | That any pointer target exists, is true, or was approved. |

The package supplies blank templates under `assets/future-study-execution/`
and generic schemas under `system/09_schemas_records_and_templates/`.

## Required Boundaries

- Select exactly one formal execution path for the Study, but do not infer one
  from a template. The path may be Python, R, SQL, a workflow engine, a
  controlled runbook, or another explicitly declared method.
- Keep environment evidence, configuration, implementation, tests, run
  manifests, result manifests, and QA records separate. A formal run must not
  automatically install, upgrade, downgrade, or otherwise alter dependencies.
- Give every formal run a unique `run_id`; do not overwrite an existing run.
  A failed or superseded run remains a record, not a reason to rewrite history.
- Treat all outputs as candidates unless a `current_result_authority` record
  names the formal-run manifest, result manifest, QA record, and an
  accountable-human decision reference. Even all four shaped references do not
  prove their targets or the decision; they only make the required evidence
  explicit for human review.
- Treat `system_contract_reference` as a separately governed system-contract
  identity, not as a Study artifact path. The blank template deliberately uses
  `UNRESOLVED_SYSTEM_CONTRACT_REFERENCE`; an accountable human must replace it
  before a contract can be selected for use. An empty bootstrap does not copy
  this public guide into the Study.
- Keep Study artifact references project-relative and inside the declared Study
  layout. This applies to declared entrypoints, environment/configuration
  evidence, run manifests, result manifests, QA records, and artifact paths.
  Absolute paths, parent-directory traversal, data locators, credentials,
  network targets, and unlisted external files are outside this contract.

## Controlled Bootstrap Extension

`scripts/bootstrap_empty_workspace.py` still requires a no-write preview, its
exact `plan_id`, a nonempty accountable-human approval reference, safe paths,
and a non-existing destination. It creates only the reviewed empty directories
plus two blank records:

- `07_analysis/00_contract/analysis_execution_contract.json`
- `08_results/_manifests/current_result_authority.json`

It does not create a formal run, result manifest, QA decision, protocol,
analysis code, data object, manuscript, or authoritative result. It does not
read or copy source data, install dependencies, call a network service, or
advance a workflow Gate.

## Release And Installation Boundary

This is a versioned `v1.1.0` source reference. It does not establish a hosted
Release or an installed runtime. Verify a selected public version only when its
exact annotated tag and matching GitHub Release identify the reviewed source
commit. Public release identity, private source identity, installed runtime
identity, project result authority, and accountable-human project decisions
remain separate records.
