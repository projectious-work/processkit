# Project storage and ownership

## Canonical layout

- **PK-STORE-000:** the processkit root is the selected repository root. The
  default context directory is `<repository>/context/`. A project MAY
  configure another contained context directory before installation. Both the
  repository identity and contained context path are recorded in processkit
  state and cannot change implicitly.

```text
context/
  entities/<entity-type>/...
  schemas/...
  state-machines/...
  processes/...
  skills/...
  packages/...
  policy/...
  generated/...
  .processkit/...
```

Exact sharding beneath an EntityType is declared by its storage contract.
Index databases, journals, locks, ownership manifests, and installed-release
metadata live below `.processkit/` and are not domain entities.

- **PK-STORE-000A:** root discovery MUST resolve exactly one repository and
  one contained context directory. It MUST reject ambiguous nested roots,
  context paths outside the selected repository, and attempts to combine
  several repositories into one invocation.
- **PK-STORE-000B:** each clone or worktree MAY maintain its own runtime locks
  and disposable indexes. Those derived stores do not coordinate Git branches
  and MUST never be treated as shared authority between working copies.

## Sources of truth

- **PK-STORE-006:** v1 MUST preserve the product principle of Git-backed,
  human-readable canonical entities while defining their formats anew from
  this specification. Existing file shapes are migration inputs, not v1
  format authority.
- **PK-STORE-001:** canonical entities, accepted project policy, and local
  extensions MUST be ordinary files suitable for Git review.
- **PK-STORE-002:** SQLite databases, full-text indexes, embedding/vector
  indexes and entries, caches, rendered indexes, and harness projections MUST
  be rebuildable derived state. None may become the only copy of project
  context or memory.
- **PK-STORE-007:** SQLite with FTS MUST remain the default derived index
  adapter, reimplemented behind the repository query port. Existing index
  schemas and code are evidence only and MUST NOT constrain canonical storage
  or public query semantics.
- **PK-STORE-008:** embedding text, vectors, chunk metadata, and similarity
  indexes MUST identify the canonical source ID, source revision or digest,
  projection version, embedding model contract, and generation. Stale or
  untraceable entries MUST NOT contribute to a complete or verified result.
- **PK-STORE-009:** deleting every derived database and embedding entry MUST
  lose no canonical information; `rebuild` MUST reproduce functionally
  equivalent indexes from Git-backed files and declared local configuration.
- **PK-STORE-039:** the default SQLite derived index MUST project canonical
  entity nodes and typed relation edges with indexes suitable for bounded
  directional traversal. It MAY use recursive queries without becoming the
  canonical relation store.
- **PK-STORE-040:** lexical, semantic/vector, and graph projections MUST share
  canonical source identity and generation metadata so hybrid retrieval can
  detect and report incompatible or stale generations.
- **PK-STORE-041:** graph indexing MUST be exposed behind a replaceable local
  index port. v1 MUST NOT require a dedicated graph database, network service,
  or shared graph authority.
- **PK-STORE-042:** another graph adapter requires benchmark evidence that the
  default indexed SQLite projection cannot meet an accepted query, scale, or
  graph-analysis requirement. Adapter choice MUST NOT alter public relation
  semantics or canonical ownership.
- **PK-STORE-003:** generated schemas MAY be committed for review, but their
  generator inputs and generation metadata MUST identify the authoritative
  source and support a drift check.
- **PK-STORE-004:** release payload content and consuming-project state MUST
  have distinct ownership; dogfood project entities MUST NOT enter a release.
- **PK-STORE-005:** processkit MUST NOT require users to commit caches, locks
  used only for concurrency, or machine-specific paths.

## File contract

- **PK-STORE-010:** text contracts MUST use UTF-8, LF on serialization, and a
  deterministic documented serialization policy.
- **PK-STORE-011:** entity bodies MAY use Markdown, but structural semantics
  MUST remain in validated frontmatter or another declared structured region.
- **PK-STORE-012:** parsers MUST support the complete declared YAML subset and
  MUST NOT locate frontmatter with ambiguous delimiter heuristics.
- **PK-STORE-013:** paths derived from IDs or user input MUST be normalized,
  checked for containment, and rejected on traversal, symlink escape, special
  files, or normalization collision.
- **PK-STORE-014:** writes MUST use temporary files in the destination
  filesystem, flush as required by the durability profile, and replace
  atomically where the platform supports it.
- **PK-STORE-015:** multi-file operations MUST use a journal and publish their
  achieved guarantees; processkit MUST NOT label a sequence atomic when a
  crash can expose an intermediate state.

## Ownership classes

Every managed path is classified as one of:

- `release-owned`: exact bytes supplied by a pinned package;
- `mergeable`: upstream baseline with supported project customization;
- `project-owned`: created and controlled by the consuming project;
- `generated`: reproducible from declared inputs; or
- `runtime`: local cache, lock, journal, or index.

- **PK-STORE-020:** installation manifests MUST record path, ownership class,
  source package, source digest, installed digest, and applicable merge rule.
- **PK-STORE-021:** update MUST use recorded base, incoming release, and local
  content for three-way reconciliation of mergeable files.
- **PK-STORE-022:** an unresolved semantic or textual conflict MUST stop before
  canonical mutation and appear in both human and machine plans.
- **PK-STORE-023:** uninstall MUST remove only paths whose ownership and
  unchanged state processkit can prove; modified or project-owned paths remain.
- **PK-STORE-024:** processkit MUST NOT silently overwrite an unknown existing
  path, adopt it as owned, or delete an untracked path.

## Concurrency and recovery

- **PK-STORE-030:** mutating commands MUST acquire a root-scoped operation lock
  with owner, process, start time, and safe stale-lock diagnostics.
- **PK-STORE-031:** concurrent reads MAY proceed from canonical files; index
  readers MUST detect generation changes or use a consistent snapshot.
- **PK-STORE-032:** interruption MUST preserve a recovery journal until the
  operation is completed, rolled back, or explicitly abandoned.
- **PK-STORE-033:** recovery MUST revalidate source hashes and current paths;
  it MUST NOT replay stale operations onto changed content.
- **PK-STORE-034:** `verify` and `doctor` MUST distinguish invalid canonical
  state, stale derived state, interrupted mutation, and benign local changes.
- **PK-STORE-035:** processkit MAY inspect Git root, tracked state, ignore
  rules, and cleanliness for safety evidence but MUST NOT commit, merge,
  rebase, push, fetch, switch branches, or modify Git configuration as an
  implicit side effect of a lifecycle or entity operation.
- **PK-STORE-038:** processkit MUST report the selected repository identity,
  working-copy revision, context path, and relevant worktree state in plans
  and machine results whenever they affect reproducibility or mutation safety.
- **PK-STORE-036:** a command requiring a clean worktree MUST report the exact
  relevant dirty paths and allow no blanket assumption that unrelated changes
  belong to processkit.
- **PK-STORE-037:** generated ignore-file updates are planned, bounded to a
  marked processkit block, idempotent, and preserve surrounding project-owned
  content.
