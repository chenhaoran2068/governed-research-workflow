# Workflows Module Boundary

Status: active baseline.

The active baseline is implemented as focused route procedures under
`references/`, with matching blank records under `assets/`. It covers startup,
feasibility, manuscript work, citation control, submission routing, controlled
bootstrap, and retrospective learning. A workflow must identify its required
inputs, allowed outputs, human-controlled decisions, stop conditions, and
records.

Do not put a real study timeline, manuscript, result, protocol, or submission
package in this module. Future module-local workflows must not duplicate or
silently override active route references.

The v0.4.0 release source adds a route from an autonomy request to a structured
authorization record. Human-governed interactive work remains the default;
the route records boundaries and refusal conditions but executes nothing.

The unreleased v0.6 candidate adds a metadata-only record route for reviewing
declared assertion, evidence, relation, verification, human-decision, and
revision/downstream-impact states. It does not make a workflow decision,
advance a Gate, rerun downstream work, or replace project authority.
