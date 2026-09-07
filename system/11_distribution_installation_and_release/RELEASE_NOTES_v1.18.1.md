# Governed Research Workflow v1.18.1

v1.18.1 is a zero-new-capability maintenance patch derived from v1.18.0.

It refines the paper-repository standard by:

- defining a short, research-type-aware repository naming pattern;
- keeping complete research identity in the README and study summary rather
  than forcing every PICOS-like field into the repository name;
- recording the selected naming dimensions, rationale, and human confirmation
  in the release manifest;
- validating the confirmed repository name before release-candidate status;
- keeping release evidence in the Study while promoting only an accepted clean
  candidate to `Github/<repository-name>/`; and
- forbidding whole-Study copies and automatic bidirectional synchronization.

It does not create or publish a repository, inspect a private Study, decide
rights or privacy, or perform Git/GitHub actions.
