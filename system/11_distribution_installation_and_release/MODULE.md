# Distribution, Installation, And Release

Status: active standalone package governance. Historical v0.3.0, v0.3.1, and
v0.4.0 release records are retained. The v0.5.0 provenance-register-set
release source is not an installation target; normal installation eligibility is
determined by the exact-tag and matching-Release rule in
`CURRENT_RELEASE_STATUS.md`.

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

`V0_5_RELEASE_GATE.md`, `V0_5_RELEASE_EVIDENCE.md`, and
`PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.5.0.md` are historical pre-C3 preparation
records. `V0_5_CAPABILITY_ADMISSION.md`, `RELEASE_NOTES_v0.5.0.md`, and
the current ledger describe the admitted v0.5.0 release-source scope. They
preserve separate exact-final-commit, C4, and post-release boundaries and do
not make a v0.5.0 public availability or installation claim.

`RELEASE_CONTROL.md` and `release_control_record.schema.json` define a
release-control record contract. Candidate-review acceptance, C4
authorization of an exact commit/tag/Release, and post-release verification are
separate records. The schema records conditions; it does not publish, scan,
sign, certify, or change hosted controls.
