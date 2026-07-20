# v0.10.0 Dependency And Workflow Review

Status: local candidate review; no platform setting, hosted CI, or Release is
verified by this document.

- Runtime dependency remains exactly `jsonschema==4.26.0`; no dependency file
  change is introduced.
- The new validator uses standard-library path/JSON facilities plus the existing
  pinned JSON Schema dependency. It imports no network client, Git wrapper,
  subprocess executor, database client, or write helper.
- Existing CI remains the Windows/Ubuntu/macOS Python matrix. Exact candidate
  CI must be repeated after C3-remote push.
- Existing standalone and framework-integrated profile tests remain required;
  no framework dependency or profile expansion is added.
- The existing protected-main and immutable-release settings must be rechecked
  during final release preparation; this source review cannot prove them.
