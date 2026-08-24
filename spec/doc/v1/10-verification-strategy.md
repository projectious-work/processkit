# Verification strategy

## Principles

Default checks are offline, deterministic, credential-free, parallel-safe,
locale-independent, and isolated from real home directories and repositories.
Tests assert observable contracts and failure behavior, not only code paths.

## Layers

| Layer | Required evidence |
|---|---|
| Unit | Domain invariants, merge decisions, lifecycle guards, parsing, rendering, redaction. |
| Component | Repository transactions, indexes, package resolution, configuration, migration, MCP dispatch. |
| Contract | Schemas, positive/negative fixtures, CLI/MCP envelopes, generated-reference drift. |
| Black box | Installed CLI and MCP workflows in temporary repositories. |
| Integration | Supported Python, OS, filesystem, terminal, uv, Git, and harness adapters. |
| Disposable end to end | Signed artifact install, first workflow, update conflict, recovery, removal, and published-artifact verification. |

## Required suites

- **PK-TEST-001:** schema metaschema tests and positive/negative fixtures MUST
  cover every public contract and format assertion.
- **PK-TEST-002:** every EntityType MUST test create, read, valid transition,
  invalid transition, unknown field, malformed reference, concurrency conflict,
  emitted event, and terminal behavior as applicable.
- **PK-TEST-003:** mutation tests MUST inject failures before and after each
  durability boundary and assert canonical files, journals, indexes, and
  reported recovery state.
- **PK-TEST-004:** install/update tests MUST cover clean install, idempotence,
  unchanged update, local modification, compatible merge, conflict, stale plan,
  interruption, recovery, downgrade refusal, and conservative uninstall.
- **PK-TEST-005:** MCP tests MUST compare runtime discovery with published
  schemas and execute requests over stdio and the authenticated daemon/proxy
  path, including concurrency, cancellation, bounds, malformed input,
  authentication refusal, catalog refresh, root isolation, and shutdown.
- **PK-TEST-015:** every application operation exposed through both CLI and
  MCP MUST have adapter-equivalence tests for successful, refused, stale,
  invalid, interrupted, and recovery-required outcomes.
- **PK-TEST-006:** query tests MUST compare indexed results with a canonical
  scan across randomized create/update/archive sequences.
- **PK-TEST-014:** semantic and hybrid retrieval tests MUST cover deterministic
  fixture embeddings or a controlled fake adapter, source attribution,
  sensitivity filters, stale projections, model changes, complete rebuild,
  bounded context assembly, and operation with semantic indexing disabled.
- **PK-TEST-007:** security suites MUST exercise every threat-driven case in
  the security chapter and verify refusal plus redaction.
- **PK-TEST-008:** documentation examples and generated references MUST be
  executed or schema-validated and checked for drift.
- **PK-TEST-009:** confirmed defects MUST gain permanent regression coverage at
  the narrowest useful layer and at a public boundary when user-visible.
- **PK-TEST-013:** applicable signed-release, interrupted-installation, and
  recovery cases from prior implementations MUST be adapted to the Python
  artifacts and the new ownership contract. Passing an old implementation's
  test unchanged is not evidence when its asserted contract differs from v1.
- **PK-TEST-016:** multi-participant tests MUST use independent clones or
  worktrees with separate indexes, integrate canonical changes through Git,
  and prove that no local lock, cache, or database is mistaken for
  cross-working-copy authority.
- **PK-TEST-017:** each supported harness adapter MUST project one canonical
  fixture skill, MCP capability, and safety constraint; tests MUST verify
  provenance, conflict preservation, idempotence, support-matrix reporting,
  and equivalence across all generated harness forms.
- **PK-TEST-018:** MCP tests MUST prove stable capability snapshots, manifest
  provenance, namespace collision refusal, tool-description immutability, and
  explicit refresh or restart after package changes.
- **PK-TEST-019:** adversarial agent-interface tests MUST inject instructions
  through skills, entities, external references, search results, logs, and
  handoffs and prove that untrusted data cannot alter tools, authority, next
  actions, or server policy.
- **PK-TEST-023:** retry and session-loss tests MUST prove replay-resistant
  mutation identity, no duplicate canonical effect, and recovery through both
  CLI and a newly authorized MCP client.

## Property and fuzz testing

- **PK-TEST-010:** property tests SHOULD cover serialization round trips, path
  containment, three-way reconciliation invariants, state-machine
  reachability, relation inverse rules, deterministic plans, and index
  equivalence. Fuzz smoke tests cover structured parsers, frontmatter
  boundaries, archives, machine envelopes, and MCP requests with bounded
  resource use.

## Platform matrix

Every supported Python minor and release operating system is represented in
pre-release evidence. Filesystem-sensitive behavior is tested on case-sensitive
and case-insensitive filesystems where supported. Windows path, locking,
replacement, signal, and terminal differences receive explicit black-box
tests rather than being inferred from Linux success.

## Gates

- **Local fast:** formatting, lint, type check, unit/component subset,
  contract fixtures, affected docs.
- **Change risk:** local fast plus selected migration, concurrency, fuzz,
  security, compatibility, performance, and platform checks.
- **Pre-release:** complete matrix, dependency/license/vulnerability/secret
  review, generated drift, docs, packages, clean-room extension conformance.
- **Release candidate:** exact wheel/source/archive verification and installed
  black-box journeys.
- **Published release:** download, integrity/authenticity verification,
  isolated installation, `version`, `help`, MCP startup, and first workflow.

- **PK-TEST-020:** unexplained skips fail required gates.
- **PK-TEST-021:** flaky tests are defects; quarantine requires owner, issue,
  scope, and expiry.
- **PK-TEST-022:** coverage is reviewed by risk and MUST NOT be substituted for
  behavioral evidence or set as a context-free universal percentage.
