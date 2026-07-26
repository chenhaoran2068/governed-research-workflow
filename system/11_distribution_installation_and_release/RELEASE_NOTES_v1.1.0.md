# V1.1.0 Candidate Release Notes

Status: local candidate release notes. They describe proposed scope only and
do not prove a tag, GitHub Release, public availability, installation target,
or runtime update.

## Proposed Addition

- A generic, metadata-only Future Study Execution And Reproducibility Contract
  (GRW-CAP-111-01) comprising five blank record templates and matching schemas:
  execution contract, formal-run manifest, result manifest, result-authority
  pointer, and analysis-run QA record.
- A reference guide describing a future Study layout, unique non-overwriting
  run records, separation of environment/configuration/implementation/tests,
  and the four references required before a result can be named authoritative.
- A bounded extension of the existing empty-workspace bootstrap that creates
  reviewed empty analysis/result/QA directories plus draft execution-contract
  and no-authoritative-result starters.
- Frozen-v1 preservation and regression coverage separating historical v1.0
  tests from the new v1.1 candidate ledger and manifests.

## Explicitly Not Added

No research executor, data access, data copy, dependency installation or
change, generic writer, result approver, human-decision verifier, agent
runtime, external-service action, Framework change, public experience intake,
release action, or runtime installation.

## Compatibility

Existing Study workspaces are not migrated. The public profiles remain
standalone and framework_integrated. Project-specific execution contracts
remain selected and approved by humans; a structural template or test result
does not establish real reproducibility, result authority, scientific truth,
data permission, or publication readiness.
