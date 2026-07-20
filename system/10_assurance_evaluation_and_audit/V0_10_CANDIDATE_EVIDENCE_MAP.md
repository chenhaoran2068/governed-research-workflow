# v0.10.0 Candidate Evidence Map

Status: local candidate evidence map. It describes required evidence and does
not prove a remote candidate, protected-main commit, C4 authorization, hosted
Release, or installed runtime.

| Claim | Evidence | Limit |
| --- | --- | --- |
| Finite metadata-only manifest | `tests/test_voluntary_experience_package.py` valid/schema tests | Does not inspect real content. |
| Boundary refusal | Unsafe-path/link/no-discovery tests | Does not prove an unnamed file is safe. |
| Manual-review and withdrawal semantics | State-combination/non-substitution tests | Does not prove a decision, consent, or recall. |
| No validator write | Byte-for-byte fixture comparison | Does not prove another process did not write. |
| Same-host receive simulation | Explicit-copy test of named synthetic records | Not Computer B, cross-device, upload, or external-user evidence. |
| Public capability boundary | Ledger, admission record, reference, README, ROADMAP tests | Does not create a Release or local installation. |

Before remote C3, repeat affected local tests on an exact candidate commit.
Before C4, repeat local and cross-platform CI evidence, public-material,
rights/privacy, dependency, release-control, and exact-final-identity reviews.

## Local Verification Snapshot

| Field | Value |
| --- | --- |
| Reviewed implementation commit | `c3095d0bab9da8ddf3ae8c86dc93b9cc28fa2d5c` |
| Command | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_*.py` |
| Result | `203` passed; `3` existing environment-dependent skips; no failures |
| Hygiene | No `__pycache__`, `.pyc`, or `.pyo` artifact after the run; `git diff --check HEAD^ HEAD` passed. |
| Static boundary review | New public surface contained no local identity/credential marker; new validator contained no network, recursive discovery, or write executor. |
| Limitation | This is local evidence for `c3095d0...`, not remote CI, protected-main, C4, hosted Release, installed runtime, Computer B, or real contribution evidence. |
