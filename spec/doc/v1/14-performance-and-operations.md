# Performance and operations

processkit is local tooling, not a high-throughput distributed database.
Performance requirements protect interactive agent use and bound resource
exhaustion without allowing caches to redefine correctness.

## Scale profile

The v1 reference profile is one repository containing up to:

- 100,000 canonical entities;
- 1,000,000 LogEntries;
- 10,000 relations returned by an explicitly bounded traversal;
- 1 GiB total structured context excluding externally referenced artifacts;
- 500 installed skills and ProcessDefinitions; and
- 16 concurrent read requests with one serialized root mutation.

- **PK-PERF-000:** larger repositories MAY work but are outside the v1
  performance guarantee.

## Interactive budgets

- **PK-PERF-001:** after warm startup and with a verified index, single-entity
  lookup and bounded metadata listing SHOULD complete within 100 ms at the
  reference scale on the published reference machine.
- **PK-PERF-002:** bounded full-text search SHOULD return its first page within
  500 ms at the reference scale.
- **PK-PERF-003:** ordinary single-entity validation and mutation excluding
  lock wait SHOULD complete within 500 ms and MUST not rebuild the full index.
- **PK-PERF-004:** CLI help and version SHOULD complete within 300 ms warm and
  one second cold on the reference machine.
- **PK-PERF-005:** MCP stdio startup SHOULD advertise capabilities within two
  seconds with installed dependencies and no network access.

These are release objectives, not semantic timeouts. A slower correct result
must report measurement and remain cancellable; it must not bypass validation.

## Bounds and degradation

- **PK-PERF-010:** list, search, event, and traversal operations MUST require or
  apply documented result limits and stable pagination.
- **PK-PERF-011:** relation traversal MUST bound depth, visited nodes, returned
  edges, and execution time and report truncation explicitly.
- **PK-PERF-012:** index rebuild MUST stream or batch input and MUST NOT require
  all entity bodies in memory simultaneously.
- **PK-PERF-013:** when an index is absent or stale, processkit MAY fall back to
  bounded canonical scans but MUST identify degraded completeness or latency.
- **PK-PERF-014:** corrupted indexes are quarantined and rebuilt; they MUST NOT
  cause canonical entity deletion or mutation.
- **PK-PERF-015:** request and parser limits are configurable only within
  system/user authority bounds; project policy cannot disable protection.

## Operational behavior

- **PK-OPS-001:** `doctor` reports runtime, contract support, root identity,
  lock and journal state, canonical validation, ownership drift, projection
  drift, index generation, package consistency, and configured MCP readiness.
- **PK-OPS-002:** health output MUST distinguish `healthy`, `degraded`,
  `blocked`, and `recovery_required`; unavailable optional checks are not
  successes.
- **PK-OPS-003:** every finding has a stable code, severity, scope, evidence,
  next action, and optional registered reconciler.
- **PK-OPS-004:** diagnostic collection MUST be available as a sanitized local
  bundle with an explicit manifest and exclusion report.
- **PK-OPS-005:** processkit MUST expose its effective resource limits and
  current derived-state generations in machine-readable diagnostics.

## Benchmarks

Pre-release evidence records reference hardware, operating system, Python
version, filesystem, corpus generator seed and digest, cold/warm state, sample
count, percentiles, and variance. Performance regression thresholds compare
like-for-like profiles and require review rather than silently updating a
golden number.
