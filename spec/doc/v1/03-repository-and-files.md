# Repository layout and files

## Layout

A processkit repository is any Git repository with a processkit
configuration. Content lives under one configured directory, `context/` by
default:

```text
processkit.toml                 project configuration
processkit.lock                 resolved upstream pins
context/
  standards/<name>.json
  processes/<name>.json
  skills/<name>/SKILL.md        skill body plus skill.json metadata
  mcp-servers/<name>.json
  decisions/<name>.md
  documents/...                 or other declared document sources
  ontology/                     containers, roles, bindings, extensions
.processkit/                    local cache; never committed
```

- **PK-STORE-001:** the repository root and content directory MUST resolve to
  exactly one Git working copy. Nested repositories and submodules are
  independent roots and MUST NOT be absorbed.
- **PK-STORE-002:** every kind MUST have one declared location. processkit
  MUST NOT discover content by scanning undeclared paths.
- **PK-STORE-003:** `.processkit/` holds only caches and fetched upstream
  copies. Deleting it MUST lose nothing; every cache MUST be rebuildable from
  committed files and the lock.
- **PK-STORE-004:** processkit MUST NOT require committing caches, locks used
  only for concurrency, credentials, or machine-specific paths.

## File formats

One file holds one item. Content that people mainly review as prose uses
Markdown with a structured header; all other content is JSON.

| Format | Used for |
|---|---|
| JSON | standards, process specifications, MCP server entries, containers, roles, bindings, extensions, skill metadata |
| Markdown with JSON or YAML front matter | decision records, documents, skill bodies |

- **PK-STORE-010:** text MUST be UTF-8 with LF line endings. Serialization
  written by processkit MUST be deterministic: sorted object keys where the
  schema does not define an order, two-space indentation, and a trailing
  newline.
- **PK-STORE-011:** Markdown files MUST keep all structured fields in the
  front matter or a declared structured region. Prose MUST NOT carry
  structural semantics.
- **PK-STORE-012:** front matter MUST be located by an exact delimiter
  contract, and YAML MUST be limited to a declared safe subset.
- **PK-STORE-013:** paths derived from names or input MUST be normalized,
  checked for containment, and rejected on traversal, symlink escape, special
  files, or case-normalization collision.

## Writing

processkit writes rarely: when initializing a repository, creating an item
from a template, formatting, or updating the lock. Authors and agents change
content with ordinary file edits.

- **PK-STORE-020:** each file write MUST use a temporary file in the
  destination directory and an atomic replace where the platform supports it.
- **PK-STORE-021:** a command that writes several files MUST state its plan
  before writing and MUST report exactly which files it changed. It MUST NOT
  claim atomicity across files; Git is the recovery mechanism.
- **PK-STORE-022:** processkit MUST NOT overwrite a file it did not create in
  the same command unless the user confirmed the plan.

## Release-owned files

Schemas, templates, and the ontology registry ship with processkit. A
repository uses them from the installed release and does not copy them,
except when it pins a release in configuration.

- **PK-STORE-030:** processkit MUST NOT copy release-owned schemas or
  templates into a repository by default. A repository MAY vendor them
  explicitly; vendored copies MUST carry the release version and digest and
  MUST fail verification when modified.
- **PK-STORE-031:** content MUST declare the `apiVersion` it was written for,
  and validation MUST use the schema of that version.

## Git boundary

- **PK-STORE-040:** processkit MAY read Git root, revision, tracked state, and
  cleanliness to report provenance. It MUST NOT commit, branch, merge,
  rebase, push, switch branches, or change Git configuration.
- **PK-STORE-041:** every served result MUST be attributable to a working-copy
  revision, and results MUST mark content that differs from that revision as
  uncommitted.
