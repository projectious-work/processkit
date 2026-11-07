# Repository storage — requirements

This specification defines how processkit stores governance content: the
repository and content-directory layout, the local cache, file formats and
deterministic serialization, how processkit writes files, how release-owned
schemas and templates relate to a repository, and the boundary between
processkit and Git. It also fixes the product-level rules that canonical
content is human-readable files in Git and that processkit stores no
instances such as events, logs, work items, transcripts, or memories.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Canonical content

- **PK-PROD-001:** processkit shall keep canonical governance content as
  human-readable files in Git repositories. processkit shall remain usable
  for that content without a hosted processkit service.
- **PK-PROD-020:** processkit shall not act as agent or project memory.
  processkit shall not store an event log, LogEntry records, work-item
  instances, session transcripts, or agent memories.

## Layout

A processkit repository is any Git repository with a processkit
configuration (`processkit.toml` at the repository root). Content lives under
one configured content directory, `context/` by default. The local cache is
`.processkit/` and is never committed.

- **PK-STORE-001:** processkit shall resolve the repository root and the
  content directory to exactly one Git working copy. processkit shall treat
  nested repositories and submodules as independent roots and shall not
  absorb them.
- **PK-STORE-002:** processkit shall use exactly one declared location for
  every content kind. processkit shall not discover content by scanning
  undeclared paths.
- **PK-STORE-003:** processkit shall hold only caches and fetched upstream
  copies in `.processkit/`. If `.processkit/` is deleted, then nothing shall
  be lost, and every cache shall be rebuildable from committed files and the
  lock.
- **PK-STORE-004:** processkit shall not require committing caches, locks
  used only for concurrency, credentials, or machine-specific paths.

## File formats

One file holds one item. Content that people mainly review as prose
(decision records, documents, skill bodies) is Markdown with JSON or YAML
front matter; all other content (standards, process specifications, MCP
server entries, containers, roles, bindings, extensions, skill metadata) is
JSON.

- **PK-STORE-010:** Text content shall be UTF-8 with LF line endings. When
  processkit writes serialized content, processkit shall produce
  deterministic serialization: sorted object keys where the schema does not
  define an order, two-space indentation, and a trailing newline.
- **PK-STORE-011:** processkit shall require Markdown files to keep all
  structured fields in the front matter or in a declared structured region.
  Prose shall not carry structural semantics.
- **PK-STORE-012:** processkit shall locate front matter by an exact
  delimiter contract. processkit shall limit YAML to a declared safe subset.
- **PK-STORE-013:** processkit shall normalize every path derived from names
  or input and check it for containment. If such a path traverses outside
  its root, escapes through a symlink, names a special file, or collides
  with another path after case normalization, then processkit shall reject
  it.

## Writing

processkit writes rarely: when initializing a repository, creating an item
from a template, formatting, or updating the lock. Authors and agents change
content with ordinary file edits.

- **PK-STORE-020:** When processkit writes a file, processkit shall write a
  temporary file in the destination directory and, where the platform
  supports it, atomically replace the destination with it.
- **PK-STORE-021:** When a command writes several files, the command shall
  state its plan before writing and shall report exactly which files it
  changed. The command shall not claim atomicity across files; Git is the
  recovery mechanism.
- **PK-STORE-022:** processkit shall not overwrite a file it did not create
  in the same command unless the user confirmed the plan.

## Release-owned files

Schemas, templates, and the ontology registry ship with processkit. A
repository uses them from the installed release and does not copy them,
except when it pins a release in configuration.

- **PK-STORE-030:** processkit shall not copy release-owned schemas or
  templates into a repository by default. Where a repository vendors them
  explicitly, the vendored copies shall carry the release version and digest,
  and if a vendored copy is modified, then processkit shall fail its
  verification.
- **PK-STORE-031:** processkit shall require content to declare the
  `apiVersion` it was written for. When processkit validates content,
  processkit shall use the schema of that declared `apiVersion`.

## Git boundary

- **PK-STORE-040:** processkit may read the Git root, revision, tracked
  state, and cleanliness to report provenance. processkit shall not commit,
  branch, merge, rebase, push, switch branches, or change Git configuration.
- **PK-STORE-041:** processkit shall attribute every served result to a
  working-copy revision. When served content differs from that revision,
  processkit shall mark that content as uncommitted.
