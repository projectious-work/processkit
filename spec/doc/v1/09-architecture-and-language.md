# Architecture and language assessment

## Decision drivers

The implementation language is evaluated against the product defined here,
not against prior sunk cost. Highest-weight drivers are:

1. correctness of schema, file, lifecycle, and reconciliation behavior;
2. speed of evolving process contracts before v1 stability;
3. MCP and AI-tooling ecosystem fit;
4. cross-platform installation and isolated dependency management;
5. testability of filesystems, failures, and protocol boundaries;
6. maintainer accessibility and extension authoring;
7. startup and memory efficiency; and
8. supply-chain surface and release complexity.

## Assessment

| Driver | Python | Go | Rust |
|---|---|---|---|
| Contract iteration and schema tooling | Strong | Good | Adequate |
| MCP and agent ecosystem integration | Strong | Good | Developing |
| Safe high-level YAML/Markdown processing | Strong | Good | Good but costly |
| Single native executable | Weak | Strong | Strong |
| Transactional filesystem implementation | Good with disciplined design | Strong | Strong |
| Extension and contributor accessibility | Strong | Good | Adequate |
| Cross-platform packaging | Strong with uv/PyPI | Strong | Strong |
| Runtime performance | Adequate | Strong | Strongest |
| Implementation complexity for this product | Lowest | Medium | Highest |

Python wins because processkit is primarily a contract, content, filesystem,
and integration product whose model will continue to evolve through v1
prereleases. Its performance requirements are modest and IO-bound. `uv tool
install` provides an isolated, reproducible application installation path, so
the absence of one native executable is not decisive.

Go would be preferred if the dominant product requirement were a native,
dependency-free executable or a long-running high-concurrency service. Rust
would be preferred for a smaller security-critical native installer with
strict resource or embedded constraints. Neither is the primary v1 product.

The earlier Rust CLI plus Python MCP split is not an implementation baseline.
No module, architecture boundary, API, or behavior is inherited merely because
it exists in that implementation. It may supply adversarial fixtures and
evidence for transaction, archive, trust, migration, and recovery requirements
only after those fixtures are reviewed against this specification. v1 uses a
new one-language implementation unless measured evidence later justifies a
narrow native component.

## Reference architecture

- **PK-ARCH-001:** the reference implementation MUST use Python 3.12 or later
  as its sole required application language.
- **PK-ARCH-002:** the CLI, MCP server, validation, reconciliation, indexing,
  migration, and generation surfaces MUST share one application core.
- **PK-ARCH-003:** public behavior MUST be defined by versioned schemas and
  conformance fixtures, not Python module layout or implementation classes.
- **PK-ARCH-004:** the core MUST use explicit ports for filesystem, clock,
  process, network, terminal, and index dependencies so tests can control them.
- **PK-ARCH-005:** a future native component requires measured need, a narrow
  versioned boundary, independent fixtures, failure isolation, and an accepted
  architecture decision.
- **PK-ARCH-006:** implementation MUST begin from the accepted specification
  and conformance fixtures, not by porting or adapting modules from the prior
  Rust v1 implementation. Reuse requires an explicit file-level review proving
  conformance and must not import prior architecture by default.
- **PK-ARCH-007:** the Rust installer MUST be replaced. Its adversarial
  transaction, interruption, archive, and recovery cases SHOULD be extracted
  as implementation-independent fixtures before replacement where they remain
  applicable to the accepted contracts.
- **PK-ARCH-008:** the reference runtime is an on-demand CLI or MCP process,
  or an optional long-lived local MCP daemon, bound to one repository working
  copy. A sidecar, shared database, remote daemon, or hosted processkit service
  MUST NOT be required for v1.
- **PK-ARCH-009:** the Python application MUST remain useful without Aibox,
  Airunner, Tau, Kaits, or a Git forge. Those products may launch or consume
  it through the documented CLI, MCP, file, and handoff contracts.

## Component boundaries

```text
CLI / MCP adapters
        ↓
application services
        ↓
domain model and policies
        ↓
ports: repository, lexical index, semantic index, package, clock, process,
       network, rendering
        ↓
local adapters: filesystem, SQLite/FTS, embedding/vector index,
                uv/Python packaging, MCP stdio and loopback HTTP
```

Each running application instance binds the repository port to one working
copy and the index ports to disposable state derived from that copy. Separate
agents normally have separate clones and index generations; Git review and
merge, not shared index state, reconcile their accepted work.

- **PK-ARCH-010:** domain behavior MUST not depend on CLI parsing, MCP SDK
  objects, SQLite rows, or ambient process globals.
- **PK-ARCH-011:** canonical repository mutation MUST have one implementation
  path shared by CLI, MCP, migration, and reconciliation.
- **PK-ARCH-012:** SQLite with FTS is the default derived query adapter; a
  different adapter MAY be added without changing canonical storage semantics.
- **PK-ARCH-015:** embedding generation and vector search MUST be behind
  replaceable local ports. Their model, dimensions, chunking, distance metric,
  and projection version are adapter metadata and MUST NOT enter canonical
  entity semantics.
- **PK-ARCH-013:** Pydantic or equivalent typed boundary models MAY be used,
  but published JSON Schemas and fixtures remain the interoperability contract.
- **PK-ARCH-014:** network release resolution and external connectors are
  optional adapters and MUST not enter the local domain core.
- **PK-ARCH-016:** Git and forge automation MAY be implemented later as
  explicit adapters over proposed changes and handoff bundles. It MUST NOT be
  embedded in entity application services or make GitHub-specific concepts
  part of the ontology.

## Dependency posture

- **PK-ARCH-020:** the initial implementation SHOULD prefer maintained focused
  libraries for CLI, MCP, YAML, JSON Schema, models, and platform directories.
- **PK-ARCH-021:** it SHOULD use the standard library for hashing, archives
  where safely sufficient, atomic file operations, subprocess control,
  logging foundations, and SQLite. Dependency selection is finalized during
  implementation planning with locked versions and contract tests; this
  specification does not bless a library by name.
