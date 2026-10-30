# Architecture and language

## Language

processkit is a content, schema, and protocol product. Its work is parsing,
validating, resolving, and serving files; performance needs are modest and
IO-bound. Python fits this best: strong JSON Schema and MCP tooling, fast
iteration on contracts, and reproducible installation with `uv tool install`.
A native executable is not a requirement.

- **PK-ARCH-001:** the reference implementation MUST use Python 3.12 or later
  as its only required language.
- **PK-ARCH-002:** v1 is a new implementation. Code from processkit v0 or the
  v1 alpha MUST NOT be copied merely to preserve it; retained behavior MUST
  first become a requirement or a black-box fixture.

## Components

```text
CLI adapter          MCP adapter (stdio, shared server)
        \               /
       application core
  validate · resolve · assemble · authorize · explain
               |
            ports
  repository · upstream cache · clock · identity · log
               |
         local adapters
  filesystem · Git (read-only) · Git fetch · authenticators
```

- **PK-ARCH-010:** CLI and MCP MUST be thin adapters over one application
  core. Domain and application code MUST NOT depend on MCP SDK types,
  transport sessions, or a model vendor.
- **PK-ARCH-011:** the core MUST access the filesystem, Git, clock, network,
  and identity only through ports so tests can control them.
- **PK-ARCH-012:** public behavior MUST be defined by schemas and conformance
  fixtures, not by module layout.
- **PK-ARCH-013:** schemas, the ontology registry, tool definitions, and
  reference documentation MUST be generated from one source of truth and
  checked for drift.
- **PK-ARCH-014:** no database is required. Caches MAY use files or SQLite
  under `.processkit/` and MUST be disposable.
- **PK-ARCH-015:** processkit MUST remain usable without aibox or any other
  projectious.work product.
