# Dependency Provenance

The v0.5 candidate adds one direct runtime dependency for the explicitly
invoked, metadata-only register-set validator:

- package: `jsonschema`;
- required version: `4.26.0` exactly, declared in `requirements.txt`;
- purpose: validate supplied metadata JSON against the package's released
  Draft 2020-12 schemas;
- supported Python baseline: `3.11+`; GitHub CI covers Python `3.11` and
  `3.14` on Windows, Ubuntu, and macOS;
- package source and verification: official documentation and PyPI project
  metadata reviewed on `2026-07-18`;
- license expression reported by PyPI: `MIT`;
- excluded uses: downloader, network client, credential handler, data reader,
  data processor, compliance decision engine, or tool grant.

The dependency's transitive packages are resolved by the package installer for
the selected platform. The v0.5 release review must record the exact resolved
environment used for local and CI validation. A dependency version change,
range expansion, lockfile, extra, or new runtime use requires a separately
reviewed candidate change and M48 revalidation.
