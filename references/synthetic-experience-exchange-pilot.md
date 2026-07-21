# Self-Controlled Synthetic Experience-Exchange Pilot

## Purpose

This v0.10.1 protocol is a narrow, synthetic-only exercise for a maintainer
to check a declared private exchange path. It pairs one caller-named v0.10
metadata-only experience-package manifest with one caller-named
`synthetic_experience_exchange_pilot_receipt`.

It proves only that the named JSON records are structurally consistent at the
time they are checked. It does not establish a real transfer, identity,
authority, consent, rights, content safety, acceptance, promotion, deletion,
recall, independent Computer B, or external-contributor readiness.

## Preconditions

Use this protocol only when all of the following are true:

1. an accountable human has separately approved the bounded synthetic pilot;
2. the package contains only generic synthetic metadata and no attachment or
   real project, research, patient, manuscript, credential, personal, or
   copyrighted source material;
3. the repository is private, maintainer-controlled, and has no collaborator,
   Issue, Discussion, webhook, GitHub App, public visibility, or intake flow;
4. the caller has supplied the exact receipt path; and
5. the selected public workflow version has an exact immutable tag and a
   matching GitHub Release when this protocol is used as a normal installation
   feature.

If any item is unknown, stop the exchange activity. Planning that does not
read package content may continue.

## Receipt Contract

Create the receipt from
`assets/synthetic-experience-exchange-pilot-receipt.template.json`. It names:

- one package manifest relative to the receipt;
- package identity, revision, and deterministic package-tree SHA-256;
- a source commit that identifies the package source revision and a retrieval
  commit that identifies the exact later receipt revision;
- the synthetic private transfer profile and pre-transfer approval reference;
- a maintainer receipt state limited to structural review;
- an isolated-clean-clone or hosted-clean-runner retrieval profile;
- a represented correction/withdrawal state and future-governed-use state; and
- explicit non-claims.

The package-tree hash covers only `experience-package.json` and the five JSON
records named by that manifest. It is calculated as lexicographically sorted
portable relative path, NUL byte, raw file bytes, NUL byte. Unlisted files are
outside the validator's view and do not become checked merely because they are
near the package.

## Explicit Validation

Run only the named receipt:

```powershell
python scripts/validate_synthetic_experience_exchange_pilot.py `
  path\to\exchange-pilot-receipt.json
```

The validator reads only the named receipt, its named manifest, and the five
records named by the manifest. It rejects path escapes, link or reparse-point
indirection, dependency uncertainty, malformed JSON, identity/revision/hash
mismatch, and inconsistent correction/future-use representations. It does not
discover directories, write a result file, contact a service, clone a
repository, or perform a transfer.

`structurally_valid` means only that the checked representation is internally
consistent. It cannot approve a package or allow further use.

## B-Compatible Clean Retrieval Procedure

This is a same-host clean-environment simulation unless it is performed on a
separate physical computer. Do not call it Computer B evidence otherwise.

1. On Computer A, commit only the reviewed synthetic package and preserve the
   exact package-source commit in the receipt.
2. Commit the receipt as a later immutable Git commit without rewriting the
   source package history.
3. In a newly created isolated local directory, clone or fetch the exact
   receipt commit. Do not reuse a folder containing prior copies.
4. Invoke the explicit validator on the named receipt and retain only a
   bounded local execution record: exact retrieval commit, command outcome,
   validator version, and the declared non-claims.
5. For a synthetic correction or future-use stop, create later commits and a
   new matching receipt. Do not rewrite or erase earlier commits, and do not
   claim deletion, recall, or prevention of existing copies.

A hosted Windows, Ubuntu, or macOS runner may add clean-runner and platform
evidence. It does not establish a person, account, separate device, consent,
or real transfer.

## Stop And Escalate

Stop and request human review before any of these actions:

- adding a collaborator or making the private repository public;
- accepting a package from anyone else;
- using non-synthetic material;
- sharing an archive, issuing a token, creating a webhook, or adding an
  upload/download helper;
- treating structural validity as review, acceptance, promotion, or rights
  clearance; or
- performing a correction, deletion, or withdrawal action outside a new
  explicitly approved bounded task.

External contributor intake, consent/rights review, actual multi-computer
evidence, correction execution, withdrawal handling, and any public submission
channel remain deferred to v0.10.2 or a separately approved later release.
