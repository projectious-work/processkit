# Verification, compatibility, and release

> **Non-normative documentation** (moved from `spec/doc/v1/` in #206).
> The normative contract is the specifications under
> [`spec/`](../../spec/); see [the v1 overview](README.md). Requirements
> that moved into a specification are listed here by ID only.

## Verification

- **PK-TEST-001:** every schema MUST have valid and invalid fixtures, and
  every published template MUST validate against its schema.
- **PK-TEST-002:** the ontology registry MUST be checked for full inventory
  coverage, classification, and consistency with schemas and documentation.
- **PK-TEST-003:** resolution tests MUST cover multi-level inheritance,
  overrides, final items, conflicting upstreams, stale overrides, and
  digest mismatch.
- **PK-TEST-004:** assembly tests MUST prove byte-identical results for equal
  inputs, stable ordering, cache invalidation on every input change, and
  briefing budget behavior.
- **PK-TEST-005:** CLI and MCP MUST be tested for equivalent results, and MCP
  discovery MUST match the published tool schemas.
- **PK-TEST-006:** access tests MUST include negative cases for every
  authenticator (expired, not-yet-valid, wrong-audience, and wrong-issuer
  tokens; untrusted, expired, and revoked certificates; spoofed proxy
  headers; disabled anonymous access) and MUST prove that forbidden items do
  not appear through list, get, context, briefing, references, counts,
  errors, or timing beyond a documented bound.
- **PK-TEST-007:** security tests MUST cover path traversal, symlink escape,
  oversized and malformed input, instructions embedded in content, and
  credential patterns in catalog entries.
- **PK-TEST-008:** tests MUST use synthetic data, temporary repositories, and
  no ambient credentials or user configuration.

## Acceptance journeys

Each release candidate MUST pass these journeys from its exact artifacts:

1. Install a verified release and initialize an empty governing repository.
2. Create a standard, a skill, and an MCP server entry from templates and
   validate them.
3. Describe a ticket-handling process in natural language, let an agent
   produce a ProcessSpecification with the ontology, validate it, and serve
   it per state.
4. Initialize a project repository that inherits from two governing levels,
   lock, fetch, override one rule, and explain the provenance of the result.
5. Connect a harness over stdio with no instruction or skill files and show
   that the briefing and `get_context` deliver the applicable rules, process,
   and skills.
6. Run the shared server with OIDC and x509 authenticators and show that two
   principals with different Bindings receive different, correctly filtered
   context.
7. Repeat a request and show a cache hit with byte-identical output; change
   one input and show invalidation.

## Performance

- `PK-PERF-001`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PERF-002`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PERF-003`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).

## Compatibility

- `PK-COMPAT-001`: normative in
  [`v0-migration@v1`](../../spec/v0-migration/v1/requirements.md).
- `PK-COMPAT-002`: normative in
  [`v0-migration@v1`](../../spec/v0-migration/v1/requirements.md).
- `PK-COMPAT-003`: normative in
  [`v0-migration@v1`](../../spec/v0-migration/v1/requirements.md).

## Migration from v0

- `PK-MIG-001`: normative in
  [`v0-migration@v1`](../../spec/v0-migration/v1/requirements.md).
- `PK-MIG-002`: normative in
  [`v0-migration@v1`](../../spec/v0-migration/v1/requirements.md).

## Release

- **PK-REL-001:** releases MUST be built from a clean worktree and an exact
  annotated tag, with wheel, source distribution, checksums, signatures, and
  a software bill of materials.
- **PK-REL-002:** release candidates MUST be installed and tested from the
  candidate artifacts, not the source tree.
- **PK-REL-003:** tags and published artifacts are immutable; corrections use
  a new version.
