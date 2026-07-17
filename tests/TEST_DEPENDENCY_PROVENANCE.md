# Test Dependency Provenance

The public package has no runtime Python dependency for its routing documents.
The candidate test suite uses `jsonschema` only to validate public JSON Schema
fixtures and records.

- observed local test environment: Python `3.13.14`, `jsonschema` `4.26.0`;
- accepted test-time compatibility range: `jsonschema >=4.23,<5`;
- purpose: structural validation of synthetic records only;
- not a package runtime requirement, downloader, network client, or credential
  dependency.

Any new dependency, range expansion, lockfile, or runtime use requires a
separate reviewed change.
