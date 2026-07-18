# Distribution, Installation, And Release

Status: active standalone package governance. Historical v0.3.0, v0.3.1,
v0.4.0, and pre-C4 v0.5.0 records are retained. The v0.5.0
provenance-register-set baseline and v0.5.1 maintenance patch are published;
normal installation eligibility for every selected version is determined by the
exact-tag and matching-Release rule in `CURRENT_RELEASE_STATUS.md`. Current
source materials must not declare a latest or current public version.

Released tags are immutable public contracts by policy. Candidate branches are
not releases. A correction requires a new release version rather than
rewriting a published tag.

The historical v0.3.0 release has evidence for a framework-integrated profile
against the exact released Workspace Framework `v0.1.0` tag. The published
v0.3.1 patch has its own exact `v0.1.1` synthetic validation. Public releases
must not
contain private paths, data, credentials, unpublished material, or project
audit records.

`V0_3_RELEASE_GATE.md` defines the historical contract, boundary,
installation, validation, integrity, human-approval, and post-release evidence
for public `v0.3.0`. The supporting records are `INSTALL_UPDATE_ROLLBACK.md`,
`PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.0.md`,
`RELEASE_INTEGRITY_POLICY_v1.md`, and `V0_3_RELEASE_EVIDENCE.md`.
`V0_3_1_COMPATIBILITY_MAINTENANCE_CANDIDATE.md` is retained as the historical
pre-release candidate record for the published patch.
`V0_3_2_RELEASE_STATE_CORRECTION_CANDIDATE.md` defines the bounded local
correction candidate and its required evidence. It is retained as a historical
input to the v0.4.0 candidate, not as the current package identity.

`V0_4_CAPABILITY_ADMISSION.md` is a historical pre-C4 control record. It
records verified evidence and accountable-human admission for the named
`v0.4.0` scope. It does not create a tag, GitHub Release, current public
capability claim, installation target, or C4 authorization.

`V0_4_RELEASE_GATE.md`, `V0_4_RELEASE_EVIDENCE.md`,
`PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.4.0.md`, and
`RELEASE_NOTES_v0.4.0.md` are historical pre-C3 release-preparation materials. They make
the candidate's proposed scope, evidence, public-material boundary, and future
release narrative reviewable before C3. They do not create an exact candidate
commit, tag, hosted Release, runtime installation, or C4 authorization.

`V0_5_RELEASE_GATE.md`, `V0_5_RELEASE_EVIDENCE.md`,
`PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.5.0.md`,
`V0_5_CAPABILITY_ADMISSION.md`, and `RELEASE_NOTES_v0.5.0.md` are historical
pre-C4 preparation or draft records. They preserve the evidence available at
their historical snapshot and do not override the published v0.5.0 tag/Release
or create an installation claim. `CURRENT_RELEASE_STATUS.md` is the current
source-side rule; the exact tag and matching hosted Release remain the live
release evidence.

`RELEASE_CONTROL.md` and `release_control_record.schema.json` define a
release-control record contract. Candidate-review acceptance, C4
authorization of an exact commit/tag/Release, and post-release verification are
separate records. The schema records conditions; it does not publish, scan,
sign, certify, or change hosted controls.

`V0_6_RELEASE_GATE.md`, `V0_6_RELEASE_EVIDENCE.md`,
`V0_6_CAPABILITY_ADMISSION.md`, `PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.6.0.md`,
and `RELEASE_NOTES_v0.6.0.md` are v0.6 release-source materials. They include
an accountable-human admission of `GRW-CAP-060-01` for the named v0.6.0 release
scope. That admission does not create a hosted public claim, installation
target, or remote action authority. Exact current identities, tag/Release
verification, and C4 remain separate evidence classes.

`V0_6_1_RELEASE_STATE_MAINTENANCE.md` and `RELEASE_NOTES_v0.6.1.md` define a
bounded maintenance source that removes a dynamic current-version assertion
from source guidance and adds the current-state assertion control. They do not
alter the v0.6 capability contract or historical immutable releases.
