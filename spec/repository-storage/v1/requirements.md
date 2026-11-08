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
- **PK-STORE-042:** processkit shall read the content directory from the
  key `directory` in the table `[content]` of `processkit.toml`. If the key
  is absent, then the content directory shall be `context`. The value shall
  be a relative path with `/` as separator, resolved against the repository
  root. If the value is empty, is absolute, contains a `..` segment, names
  the repository root, or resolves into `.git/` or `.processkit/`, then
  processkit shall fail with `storage.invalid-content-directory`.
<!-- agent proposal: OPEN-repository-storage-01 -->
- **PK-STORE-043:** processkit shall require the repository root to be the
  top level of a Git working copy. If the repository root is not inside a
  Git working copy, or is a subdirectory of one, then processkit shall fail
  with `storage.not-a-working-copy`.
<!-- agent proposal: OPEN-repository-storage-09 -->
- **PK-STORE-044:** If the content directory, or a directory between the
  repository root and the content directory, is the top level of a nested
  repository or submodule, then processkit shall fail with
  `storage.invalid-content-directory`. A directory is such a top level when
  it contains an entry named `.git`. processkit shall not read files below
  a nested repository or submodule inside a declared location, and shall
  not report them.
<!-- agent proposal: OPEN-repository-storage-09 -->
- **PK-STORE-045:** processkit shall use fixed per-kind locations relative
  to the content directory, as listed in `interfaces.yaml`
  (`kind_locations`). Configuration shall not change these locations. The
  locations of Documents shall be the files that the declared document
  sources match (`content-kinds@v1` PK-DOC-001).
<!-- agent proposal: OPEN-repository-storage-01 -->
- **PK-STORE-046:** processkit shall require the file name stem of an
  item, and the directory name of a Skill, to equal the item's
  `metadata.name`. This rule does not apply to Documents. processkit shall
  require the `kind` of an item to be the kind of the location that holds
  it. If either condition fails, then
  processkit shall report `storage.location-mismatch` and shall not serve
  the item.
<!-- agent proposal: OPEN-repository-storage-12 -->
- **PK-STORE-047:** If a command receives a path argument that is outside
  every declared location, then processkit shall report
  `storage.undeclared-path` as a usage error and shall not read the file as
  content.
<!-- agent proposal: OPEN-repository-storage-01 -->

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
- **PK-STORE-048:** processkit shall reject a text file that is not valid
  UTF-8 or that starts with a byte order mark, with
  `storage.invalid-encoding`. processkit shall reject a text file that
  contains a carriage return (U+000D), with `storage.invalid-line-ending`.
  Both are validation failures.
<!-- agent proposal: OPEN-repository-storage-10 -->
- **PK-STORE-049:** When processkit serializes JSON, processkit shall apply
  the serialization rules in `interfaces.yaml`
  (`serialization_written_by_processkit`). In v1, no schema defines a key
  order, so processkit shall sort the keys of every object. If a JSON
  object or a YAML mapping contains the same key twice, then processkit
  shall reject the file with `storage.duplicate-key`.
<!-- agent proposal: OPEN-repository-storage-10 -->
- **PK-STORE-050:** When `processkit format` runs, processkit shall
  first replace every CRLF and every lone CR with LF. processkit shall then
  rewrite JSON item files and JSON front matter in deterministic
  serialization. processkit shall keep YAML front matter and the Markdown
  body byte for byte, except that the file shall end with exactly one LF.
  processkit shall not rewrite a file that it cannot parse; it shall report
  the file instead. If a file is already in deterministic serialization,
  then `processkit format` shall not include it in the plan.
<!-- agent proposal: OPEN-repository-storage-10 -->
- **PK-STORE-051:** processkit shall locate front matter only by these
  delimiters. The first line of the file shall be exactly `---` for YAML
  front matter or exactly `---json` for JSON front matter. The front matter
  shall end at the next line that is exactly `---`. The front matter shall
  be one object or mapping. If a file starts with an opening delimiter and
  has no closing delimiter, then processkit shall report
  `storage.front-matter-delimiter`.
<!-- agent proposal: OPEN-repository-storage-03 -->
- **PK-STORE-052:** processkit shall parse YAML front matter with the safe
  subset in `interfaces.yaml` (`formats.markdown-front-matter.yaml_subset`).
  If front matter uses a construct outside the subset, then processkit shall
  report `storage.unsafe-yaml` and shall not expand or execute the
  construct.
<!-- agent proposal: OPEN-repository-storage-03 -->
- **PK-STORE-053:** In v1, front matter shall be the only structured region
  of a Markdown file. processkit shall not read structured fields from a
  Markdown body.
<!-- agent proposal: OPEN-repository-storage-03 -->
- **PK-STORE-054:** processkit shall read every structured field of a Skill
  from `skill.json` beside `SKILL.md`. processkit shall not interpret the
  front matter of `SKILL.md`, except that a `name` in it shall equal the
  Skill's `metadata.name`. If it does not, then processkit shall report
  `storage.location-mismatch`.
<!-- agent proposal: OPEN-repository-storage-11 -->
- **PK-STORE-055:** processkit shall normalize a path by splitting it at
  `/`, removing `.` segments, and resolving `..` segments lexically, and
  then shall check that the result is inside its root. processkit shall
  treat two paths as colliding when they are equal after Unicode NFC
  normalization followed by Unicode full case folding. processkit shall
  report each rejection with the code that `interfaces.yaml` lists for it
  (`paths.rejected`).
<!-- agent proposal: OPEN-repository-storage-02 -->

## Writing

processkit writes rarely: when initializing a repository, creating an item
from a template, formatting, or updating the lock. Authors and agents change
content with ordinary file edits. processkit replaces or deletes only
committed files, so Git is always able to restore them.

- **PK-STORE-020:** When processkit writes a file, processkit shall write a
  temporary file in the destination directory and, where the platform
  supports it, atomically replace the destination with it.
- **PK-STORE-021:** When a command writes several files, the command shall
  state its plan before writing and shall report exactly which files it
  changed. The command shall not claim atomicity across files; Git is the
  recovery mechanism.
- **PK-STORE-022:** processkit shall not overwrite a file it did not create
  in the same command unless the user confirmed the plan.
- **PK-STORE-056:** Before a command writes a repository file, processkit
  shall check that every plan target that exists is tracked by Git and has
  no staged or unstaged change relative to `HEAD`. If a target fails this
  check, then processkit shall report `storage.target-not-committed` for
  each failing target and shall write no file. Changes to files that are
  not plan targets shall not affect this check. No option shall bypass
  this check, and processkit shall not create a backup instead.
<!-- owner decision: #213 finding 4 (2026-11-08), decision C1 -->
- **PK-STORE-057:** A plan and a change report shall list file changes in
  the shape of `schemas/file-change.schema.json`, sorted by path. A plan
  shall not list a file whose content would not change. When a write fails
  part way, processkit shall stop, report `storage.write-failed` for the
  failing file, and report the files it already changed.
<!-- agent proposal: OPEN-repository-storage-06 -->
- **PK-STORE-058:** processkit shall name a temporary file
  `.<file name>.processkit-tmp-<random>` and shall create it exclusively.
  processkit should flush the temporary file to stable storage before it
  replaces the destination. When processkit replaces an existing file, it
  shall keep the file's permission bits. processkit shall remove the
  temporary file when the command ends, also on failure.
<!-- agent proposal: OPEN-repository-storage-13 -->
- **PK-STORE-059:** If the atomic replace fails, then processkit shall not
  fall back to a non-atomic write. processkit shall leave the destination
  unchanged and shall report `storage.atomic-replace-failed` as an
  environment failure.
<!-- agent proposal: OPEN-repository-storage-13 -->
- **PK-STORE-060:** When `processkit init` runs, processkit shall plan
  `processkit.toml` and shall create the content directory. processkit
  shall not create item files, schemas, or templates during `init`.
<!-- agent proposal: OPEN-repository-storage-01 -->

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
- **PK-STORE-061:** If an item declares an `apiVersion` that the installed
  release does not support, then processkit shall report
  `storage.unsupported-api-version` as a validation failure and shall not
  serve the item. The supported values shall be those that
  `processkit version` reports.
<!-- agent proposal: OPEN-repository-storage-08 -->

## Git boundary

- **PK-STORE-040:** processkit may read the Git root, revision, tracked
  state, and cleanliness to report provenance. processkit shall not commit,
  branch, merge, rebase, push, switch branches, or change Git configuration.
- **PK-STORE-041:** processkit shall attribute every served result to a
  working-copy revision. When served content differs from that revision,
  processkit shall mark that content as uncommitted.
- **PK-STORE-062:** processkit shall report the working-copy revision as
  the object in `schemas/revision.schema.json`. processkit shall mark an
  item as uncommitted when any of its source files is untracked, or has a
  staged or unstaged change relative to `HEAD`. processkit shall mark the
  result as uncommitted when any served item is uncommitted, or when
  `processkit.toml` or `processkit.lock` has such a change.
<!-- agent proposal: OPEN-repository-storage-04 -->
