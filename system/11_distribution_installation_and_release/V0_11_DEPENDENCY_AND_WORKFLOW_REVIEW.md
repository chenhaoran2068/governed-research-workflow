# v0.11.0 Dependency And Workflow Review

Status: local pre-C3-remote dependency and workflow review for v0.11 release
preparation. It records the reviewed source delta, not remote CI, a
protected-main identity, C4 authorization, a tag, GitHub Release, or runtime
installation evidence. Any later exact candidate requires affected evidence to
be refreshed under M48.

If a later C3-remote candidate or C4 release is approved, this record remains
a historical local pre-C3-remote snapshot. It does not establish the
dependency, workflow, or CI evidence for that later exact candidate or hosted
Release.

| Surface | Result |
| --- | --- |
| New runtime dependency, lockfile, or package | none |
| Existing direct runtime dependency | unchanged: `jsonschema==4.26.0` |
| New script, helper, validator, or agent runtime | none |
| GitHub Actions workflow or permission change | none |
| Public profiles | unchanged: `standalone` and `framework_integrated` only |
| Framework integration identity | unchanged: Workspace Framework `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |
| Capability-ledger schema change | backward-compatible ledger identifier-pattern extension for the six `110` records only |

The existing workflow remains a read-only Windows, Ubuntu, and macOS matrix on
Python 3.11 and 3.14. Its Action references remain full reviewed commit SHAs.
The v0.11 candidate must receive its own separately authorized three-platform
matrix run after an exact remote candidate exists; prior CI or local tests do
not substitute for that result.

The existing ledger-schema extension is intentionally disclosed here. It does
not add a new v0.11 data, workflow, or experience schema; it only lets the
already existing capability ledger represent the six admitted v0.11 IDs. The
existing ledger validation and complete regression suite remain required.
