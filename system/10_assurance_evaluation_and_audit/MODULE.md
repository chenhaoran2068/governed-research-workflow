# Assurance, Evaluation, And Audit

Status: active regression baseline; broader assurance is foundation only.

`tests/` protects the controlled bootstrap helper, module inventory,
and a synthetic cross-repository framework integration. Passing tests prove
only the tested technical behavior. They do not approve scientific quality,
compliance, data access, manuscript claims, or a submission package.

Future assurance additions require synthetic fixtures, explicit expected
behavior, failure cases, and a statement of what the test does not establish.

The v0.4.0 release source adds a deterministic capability-ledger test and an
evidence matrix for the `v0.4.0` target. They verify record completeness,
refusal conditions, and safe references. They do not create a release or
establish scientific, clinical, compliance, or publication truth; capability
admission remains a separate accountable-human ledger decision.

Release-control tests validate only synthetic record structure and refusal
paths. They do not scan a repository, verify GitHub settings, create a tag, or
replace the C4 and post-release checks required for an actual publication.

`tests/test_v0_4_synthetic_assurance.py` combines release-source records,
the release-verification rule, synthetic templates, profile identity, and
refusal paths. Its run record is source-level evidence, not an installed
runtime, hosted Release, or release-readiness claim.

The unreleased v0.6 candidate adds
`V0_6_CANDIDATE_EVIDENCE_MAP.md` and
`tests/test_v0_6_candidate_assurance.py`. They keep candidate implementation
evidence separate from the canonical capability ledger until an accountable
human reviews one exact candidate commit. They do not admit a capability,
authorize C4, or make a public-release or runtime claim.
