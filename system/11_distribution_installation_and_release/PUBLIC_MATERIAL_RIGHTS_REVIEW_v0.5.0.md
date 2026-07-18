# Public Material And Rights Review: v0.5.0 Pre-C3 Candidate

Status: historical pre-C3 preparation record. It defines the required
exact-commit review and does not clear any uncommitted or future candidate tree
for publication, C4 authorization, or a hosted Release. It is not the current
D50 publication-authority decision; that bounded accountable-human decision is
recorded in `V0_5_CAPABILITY_ADMISSION.md` and remains subject to final
exact-commit re-review before C4.

## Public Boundary

The intended public package may include generic documentation, blank templates,
schemas, synthetic JSON fixtures, tests, an explicitly invoked read-only
validator, CI configuration, dependency declaration, and Apache-2.0 license
text. It must not include real research workspaces, patient or restricted data,
unpublished manuscripts, reviewer material, private audit trails, private
prompts, credentials, personal memory, local absolute paths, or third-party
content without a verified redistribution right.

`GRW-CAP-050-01` operates on metadata JSON supplied by the user. Its bundled
fixtures must remain synthetic and must not identify a real dataset, project,
participant, institution, account, URL, credential, or access basis.

## Exact-Commit Review Method

For the selected exact candidate commit, review:

1. tracked and untracked file inventory, candidate-to-baseline diff, size, and
   generated or binary artifacts;
2. credentials, private keys, tokens, connection strings, local paths, and
   unexpected personal identifiers;
3. real-project, patient, restricted-data, unpublished-material, and
   third-party redistribution risks;
4. Git LFS, submodules, Actions/workflow references, direct/transitive
   dependencies, generated source archives, and planned Release assets; and
5. license, author/contributor, institution/employer, confidentiality, and
   publication-authority questions requiring accountable-human confirmation.

Pattern scans reduce risk but cannot prove legal ownership, rights clearance,
or absence of every sensitive fact. Generic references to data, ethics, DUA,
or restricted material are allowed only as boundary guidance or synthetic
refusal tests.

## Required Accountable-Human Decision

Before C4, an accountable human must confirm authority to publish the exact
reviewed tree under Apache-2.0, including the author identity and any
institutional, employer, contributor, confidentiality, or third-party rights
constraints. Uncertainty blocks publication; it is not cured by an AI
disclaimer or inference.

## Stop Rule

Stop candidate progression if a rights, ownership, private-material,
institutional, employer, contributor, license, credential, or confidentiality
question remains unresolved. Preserve evidence and create a corrective
candidate if needed; never publish first and silently repair later.
