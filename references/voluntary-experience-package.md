# Voluntary Metadata-Only Experience Package

## Purpose

This package format helps a person prepare a finite, generic description of an
experience for later **human** review. It is a local format and preflight only.
It is not an upload channel, contributor portal, identity system, consent
system, anonymization tool, or public submission process.

## Before Creating A Package

Do not put any personal information, patient/research data, credentials,
unpublished material, real project identifier, raw transcript, proprietary
text, copyrighted source content, restricted fact, attachment, or URL requiring
access into the package. The validator cannot detect every prohibited item.
When unsure, stop and keep the material private for human review.

Use the root template and the five record templates under
`assets/experience-package/`. Keep every path relative and use forward slashes.
The validator only reads the manifest and exactly the five records it names.
An extra file is outside its view and is not checked, approved, or included in
the structural result.

## Structural States

`not_reviewed` means no maintainer decision is recorded. A schema pass does not
turn it into approval. `eligible_for_candidate_consideration` means only that
an accountable human may separately consider a v0.7 lesson-promotion
candidate. It does not make a shared rule, template, skill change, or public
contribution.

A correction or withdrawal request is not deletion. `future_use_stopped` can
be represented only after an accountable-human decision reference and means no
future governed use after that decision. It cannot recall copies, forks,
backups, exports, or already published material.

## Validate Explicitly

Run the validator only against a path you deliberately selected:

```powershell
python scripts/validate_voluntary_experience_package.py path/to/experience-package.json
```

It prints `structurally_valid`, `structurally_invalid`, or `refused_boundary`.
It performs no upload, network request, package discovery, report-file write,
hashing of attachments, Git action, promotion, or correction.

`structurally_valid` means only that the named metadata records matched the
published structural contract. It does not prove the experience is true, safe,
rights-cleared, consented, accepted, suitable for sharing, or ready for a
multi-machine transfer.

## Trial And Deferred Work

The included test package is synthetic and can be obtained with the public
source/Release. It supports a same-host clean-environment receive simulation
only: copy the declared synthetic records into a fresh temporary directory and
validate the named manifest. This is not a Computer B test or a real
contribution upload/download exercise.

Private intake, real external contributors, true cross-device transfer,
identity/authentication, telemetry, actual remote correction/withdrawal, and
automatic redaction/review/promotion are intentionally deferred to v0.10.1 or
later and need a new reviewed Charter.
