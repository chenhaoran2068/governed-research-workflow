# V1.1.0 Release Evidence

Status: local release-preparation evidence for a candidate tree. It is
intentionally commit-neutral; a separate controlled C3 receipt binds the exact
local candidate identity. It is not an exact C3 remote candidate, remote CI
result, protected-main identity, C4 authorization, tag, GitHub Release, or
runtime-installation statement.

| Field | Current value |
| --- | --- |
| Intended version | v1.1.0 |
| Public baseline | immutable v1.0.0 commit 476a70d90eea2e9cab6cf1bea08b0b915695f745 |
| Local branch | v1.1.0-future-study-execution-candidate |
| Exact local candidate | bound only by the separately controlled local C3 receipt; this source record deliberately remains commit-neutral |
| Candidate capability | GRW-CAP-111-01, locally verified and admitted for the proposed v1.1.0 scope, but not released |
| Frozen historical contract | v1_capability_truth_ledger.json preserved and covered by dedicated test |
| Local regression | release-preparation targeted run: 39 passed; refreshed full run: 274 passed, 3 existing skips, 0 failures, bytecode cache count 0 |
| Static review | 57 candidate files in scope; no private path, credential pattern, reparse point, malformed JSON, trailing whitespace, or positive v1.1 release/install misclaim finding |
| Dependencies and Framework | no new dependency; no Framework change; existing exact Framework binding retained |
| Remote CI / C4 / Release / runtime | not authorized and not established |

Any later candidate change invalidates affected local evidence under M48. The
receipt-bound exact commit must be rechecked after later candidate changes,
remote CI, and protected-main merge; neither a green local suite nor this table
creates a public Release or installation identity.
