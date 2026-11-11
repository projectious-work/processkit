# Inheritance across repositories — requirements

This specification defines how a processkit repository inherits governance
content from upstream governing repositories: declaring named upstreams,
fetching them only by explicit command, resolving them, including
transitive upstreams, from fetched data into a committed lock, resolving
one effective set of items with explicit overrides, final items and rules,
declared winners between upstreams, and provenance on every served item,
reviewing upstream changes, and the rule that upstream access rules grant
nothing downstream unless imported. It does not define the item envelope and
reference resolution (`ontology@v1`), the fields of each content kind
(`content-kinds@v1`), file locations and the local cache
(`repository-storage@v1`), command syntax, exit codes, and result envelopes
(`cli@v1`), context assembly and caching (`mcp-context-serving@v1`), or
authenticators, Roles, and Bindings (`access-control@v1`).

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Product goals

- **PK-PROD-009:** processkit shall enable a governing or project repository
  to inherit content from pinned upstream governing repositories, with
  explicit and reviewable overrides and recorded provenance for every served
  item.
- **PK-PROD-026:** processkit shall not create commits, branches, pull
  requests, pushes, or fetches as implicit side effects. Fetching a pinned
  upstream is an explicit command.

## Declaring upstreams

- **PK-INH-001:** A repository may declare any number of named upstreams in
  configuration, each with a Git source and a ref.
- **PK-INH-002:** When `processkit lock` runs, the processkit CLI shall
  resolve every ref, including the refs of transitive upstreams, to an exact
  commit and content digest from data that `processkit fetch` has already
  stored in the local cache, and shall write `processkit.lock`. processkit
  shall serve inherited content only from locked commits.
  <!-- changed by owner decision: #213 finding 3 (2026-11-08) — lock reads
       only the local cache; see cli@v1 PK-CLI-044 -->
- **PK-INH-003:** processkit shall fetch upstream content only through the
  explicit command `processkit fetch`. Serving and validation shall not
  access the network.
- **PK-INH-004:** If an upstream is missing, unreachable, or does not match
  its locked content digest, then `processkit fetch` shall fail and report
  the exact upstream and the reason. If the local cache lacks data that
  `processkit lock` needs, or the cached content does not match its locked
  content digest, then `processkit lock` shall fail and report the exact
  upstream and the reason. processkit shall not silently replace an
  upstream by another revision.
  <!-- changed by owner decision: #213 finding 3 (2026-11-08) — lock does
       not access the network, so only fetch meets an unreachable source -->

- **PK-INH-032:** processkit shall read upstream declarations from the
  `[[upstream]]` tables of `processkit.toml` in the shape of
  `schemas/inheritance-config.schema.json`. Each declaration shall have the
  keys `name`, `source`, and `ref`. Upstream names shall be unique in the
  file. The order of the tables shall have no effect. If a declaration
  violates the schema, then processkit shall report
  `cli.config-invalid-value` as a validation failure.
  <!-- agent proposal: OPEN-inheritance-01 -->
- **PK-INH-033:** processkit shall accept as `source` only an absolute
  local path, a `file://` URL, an `https://` URL, an `ssh://` URL, or an
  SCP-like address (`user@host:path`). If a `source` contains a password or
  token in its user information (`https://user:secret@host/...`), then
  processkit shall report `cli.config-forbidden-key` as a validation
  failure and shall not write or log the value.
  <!-- agent proposal: OPEN-inheritance-13 -->
- **PK-INH-034:** processkit shall not read, store, log, or pass a
  credential value for an upstream source. Where a source requires
  authentication, `processkit fetch` shall rely only on the Git credential
  mechanisms configured for the operating-system user who runs it, such as
  a Git credential helper or an SSH agent. A source that needs no
  authentication shall work without any credential configuration.
  <!-- agent proposal: OPEN-inheritance-13 -->
- **PK-INH-035:** processkit shall resolve a `ref` in this order: a value
  of 40 or 64 lowercase hexadecimal digits is a commit ID; a value that
  starts with `refs/` is a full reference name; otherwise
  `refs/tags/<ref>`, then `refs/heads/<ref>`. processkit shall resolve an
  annotated tag to the commit it points to. If no step yields a commit,
  then the ref is missing.
  <!-- agent proposal: OPEN-inheritance-01 -->

## Fetching

- **PK-INH-036:** When `processkit fetch` runs, processkit shall resolve
  the ref of every declared upstream at its source, shall store the
  resulting commit and the resolution in the local cache, and shall store
  every locked commit in the local cache. For every commit it stored for a
  declared upstream, `processkit fetch` shall also read the
  `processkit.lock` of that commit and shall store every commit that this
  lock names. A declared upstream that is not yet locked shall therefore
  be fetched, so that a first `processkit lock` is possible.
  <!-- owner decision: #213 finding 3 (2026-11-08) — fetch, then lock -->
- **PK-INH-037:** When `processkit fetch` stores a commit for which a lock
  names a content digest, processkit shall compute the content digest of
  the commit and compare it with that digest. If they differ, then
  processkit shall report `inheritance.digest-mismatch` and shall not keep
  that commit in the local cache. processkit shall use a cached commit
  only for a lock entry whose digest equals the digest computed when the
  commit was stored.
  <!-- agent proposal: OPEN-inheritance-02 -->
- **PK-INH-038:** processkit shall compute the content digest of a commit
  as `interfaces.yaml` states (`content_digest`): SHA-256 over a manifest
  of every file and symbolic link in the commit's tree, sorted by path.
  The digest shall not depend on the Git object format or on file
  modification times.
  <!-- agent proposal: OPEN-inheritance-02 -->
- **PK-INH-039:** If `processkit fetch` fails for one upstream, then it
  shall still try every other upstream, shall report one diagnostic for
  each failure, and shall keep in the local cache every commit that it
  fetched and verified. `processkit fetch` shall report what it resolved
  and fetched in `data` in the shape of `schemas/fetch-result.schema.json`.
  `processkit fetch` shall not change a repository file.
  <!-- agent proposal: OPEN-inheritance-05 -->

## Locking

- **PK-INH-040:** processkit shall write `processkit.lock` as JSON in the
  shape of `schemas/lock.schema.json`, with the serialization of
  `repository-storage@v1` PK-STORE-049. The lock shall have one entry for
  every declared upstream and one entry for every transitive upstream,
  sorted by entry name. The entry name of a declared upstream shall be its
  `name`. The entry name of a transitive upstream shall be the entry name
  of the upstream whose lock introduced it, a `/`, and its entry name in
  that lock.
  <!-- agent proposal: OPEN-inheritance-01 -->
- **PK-INH-041:** processkit shall take the transitive entries of a
  declared upstream from the `processkit.lock` at that upstream's locked
  commit, and shall not resolve their refs again. If an upstream declares
  upstreams and its lock is absent, has an unsupported `apiVersion`, fails
  `schemas/lock.schema.json`, or does not match its own declarations, then
  processkit shall report `inheritance.upstream-lock-invalid` as a
  validation failure for that upstream.
  <!-- agent proposal: OPEN-inheritance-10 -->
- **PK-INH-042:** When `processkit lock` runs without `--update`,
  processkit shall keep every entry whose declared upstream still has the
  same `source` and `ref`. processkit shall resolve a new declaration, or
  one whose `source` or `ref` changed, to the commit that the latest
  `processkit fetch` stored for that `source` and `ref`. processkit shall
  remove the entries of upstreams that are no longer declared.
  <!-- agent proposal: OPEN-inheritance-05 -->
- **PK-INH-043:** When `processkit lock --update` runs without UPSTREAM,
  processkit shall resolve every declared upstream again as PK-INH-042
  resolves a new declaration. When UPSTREAM operands are given, processkit
  shall resolve only those declared upstreams again, and their transitive
  entries, and shall treat every other upstream as PK-INH-042 states. If
  an UPSTREAM is not the name of a declared upstream, then processkit
  shall report `inheritance.unknown-upstream` as a usage error and shall
  not write the lock.
  <!-- agent proposal: OPEN-inheritance-05; changed by owner decision:
       2026-11-11 (#212), CLI style B -->
- **PK-INH-044:** `processkit lock` shall write the lock only through the
  plan and confirmation rules of `cli@v1` (PK-CLI-004, PK-CLI-014) and the
  write precondition of `repository-storage@v1` (PK-STORE-056).
  processkit shall not ask for any additional confirmation. If the lock
  would not change, then the plan shall be empty and processkit shall not
  write the file.
  <!-- agent proposal: OPEN-inheritance-05 -->
- **PK-INH-045:** If `processkit.lock` fails `schemas/lock.schema.json` or
  has an unsupported `apiVersion`, then processkit shall report
  `inheritance.lock-invalid` as a validation failure and shall serve no
  inherited item. If upstreams are declared and the lock is absent, or the
  lock does not have exactly one entry with the same `source` and `ref`
  for every declared upstream and no other direct entry, then
  `processkit validate` shall report `inheritance.lock-outdated` as a
  validation failure, and the other commands shall report it as a warning
  and serve inherited items from the lock as it is.
  <!-- agent proposal: OPEN-inheritance-07 -->

## Resolution

- **PK-INH-010:** processkit shall resolve the repository and its locked
  upstreams into one effective set of items, and the resolution shall be
  deterministic for a given repository revision and lock.
- **PK-INH-011:** processkit shall keep the upstream identity of every
  inherited item. If a local item has the same kind and name as an
  inherited item and does not declare an explicit override, then processkit
  shall treat it as a conflict.
- **PK-INH-012:** processkit shall require an override to name the
  overridden upstream item and its version and to state a reason. Where the
  item's schema declares it, an override may replace the item, add rules, or
  change a rule's level.
- **PK-INH-013:** An upstream may mark an item or a rule `final`. If a
  downstream override overrides a final item or a final rule, then
  validation shall fail.
- **PK-INH-014:** If two upstreams provide the same item, then processkit
  shall require the repository to declare which upstream wins.
  processkit shall not let upstream declaration order decide silently.
- **PK-INH-015:** processkit shall attach to every served item its
  provenance: the originating repository, commit, and path, and every
  override applied on the way.
- **PK-INH-016:** If an override no longer matches the upstream version it
  names, then `processkit validate` shall report the override as stale.

- **PK-INH-046:** processkit shall build the effective item set of a
  repository from its local items and, for every declared upstream, the
  effective item set of that upstream at its locked commit. processkit
  shall resolve an upstream's effective item set with that upstream's own
  `processkit.toml` and the lock entries below its entry name, by the same
  rules. The identity of an item shall be its kind, namespace, and name.
  An upstream "provides" every item of its effective item set.
  <!-- agent proposal: OPEN-inheritance-10 -->
- **PK-INH-047:** If two declared upstreams provide an item with the same
  identity, the same `provenance.origin`, and the same
  `provenance.overrides`, then processkit shall treat them as one item and
  shall not report a conflict. Every other pair of candidates with the
  same identity from two declared upstreams shall need a declared winner
  (PK-INH-014). This shall also apply when two paths reach the same
  repository at different commits.
  <!-- agent proposal: OPEN-inheritance-10 -->
- **PK-INH-048:** If resolving an upstream's effective item set yields a
  diagnostic of severity `error` with an `inheritance.` code, then
  processkit shall report `inheritance.upstream-invalid` as a validation
  failure for that upstream, with the upstream diagnostic's code in
  `evidence`, and shall not serve the items that the upstream diagnostic
  concerns.
  <!-- agent proposal: OPEN-inheritance-07 -->
- **PK-INH-049:** A repository shall declare a winner in a `[[winner]]`
  table of `processkit.toml` with the keys `item` (a typed name
  `<kind>/<name>` or `<kind>/<namespace>/<name>`) and `upstream` (the name
  of a declared upstream), in the shape of
  `schemas/inheritance-config.schema.json`. A winner shall apply to
  exactly one item. If a winner names an undeclared upstream, or an
  upstream that does not provide the item, or if two winners name the same
  item, then processkit shall report `inheritance.winner-invalid` as a
  validation failure. If a winner names an item that fewer than two
  declared upstreams provide, then processkit shall report
  `inheritance.winner-unused` as a warning.
  <!-- agent proposal: OPEN-inheritance-03 -->
- **PK-INH-050:** processkit shall allow an override and the `final` marks
  only for kinds whose schema defines `spec.overrides` and `spec.final`
  (`content-kinds@v1`). A local item of a kind without `spec.overrides`
  that has the identity of an inherited item shall be a conflict
  (PK-INH-011). An override shall have the identity of the item it
  overrides. `spec.overrides.upstream` shall name the declared upstream
  that provides the inherited item after winners apply. If
  `spec.overrides.name` is not the overriding item's own name, then
  processkit shall report `inheritance.override-name-mismatch`. If the
  named upstream does not provide the item after winners apply, then
  processkit shall report `inheritance.override-target-not-found`. Both
  are validation failures.
  <!-- agent proposal: OPEN-inheritance-04 -->
- **PK-INH-051:** processkit shall apply an override by its
  `spec.overrides.effect` (`content-kinds@v1` `standard.schema.json`).
  With `replace`, processkit shall serve the overriding item in place of
  the inherited item. With `amend`, processkit shall serve the inherited
  item with the level of every rule in `spec.overrides.ruleLevels` set as
  given and the rules of `spec.overrides.addRules` appended in order; every
  other member shall be the inherited item's. processkit shall identify a
  rule by its `id`. The effects allowed for each kind are those that
  `content-kinds@v1` declares in the kind's schema.
  <!-- agent proposal: OPEN-inheritance-04 -->
- **PK-INH-052:** A rule of a `replace` override is unchanged when it
  equals the upstream rule with the same `id` as a JSON value, where an
  absent `final` equals `false`. A `replace` override changes a final rule
  when it has no rule with that rule's `id` or the rule is not unchanged.
  An `amend` override changes a final rule when its `ruleLevels` names
  that rule. processkit shall report an override of a final item as
  `inheritance.override-final-item` and an override that changes a final
  rule as `inheritance.override-final-rule`, both as validation failures
  that name the item or the rule.
  <!-- agent proposal: OPEN-inheritance-04 -->
- **PK-INH-053:** An override shall be stale when its
  `spec.overrides.version` differs from the `spec.version` of the item it
  overrides. processkit shall report a stale override as
  `inheritance.override-stale`, a validation failure, and shall still apply
  the override.
  <!-- agent proposal: OPEN-inheritance-11 -->
- **PK-INH-054:** processkit shall report every inheritance condition with
  the diagnostic code, category, and scope that `interfaces.yaml` lists
  (`errors`), in the diagnostic shape of `cli@v1`.
  <!-- agent proposal: OPEN-inheritance-07 -->

## Provenance

- **PK-INH-055:** processkit shall report the provenance of an item as
  `status.provenance` (`ontology@v1` `schemas/status.schema.json`) in the
  shape of `schemas/provenance.schema.json`: `origin`, the location of the
  item in the repository that first provides it, `overrides`, every
  override applied on the way in the order applied, and `restricted` with
  `restrictedBy`.
  A location shall name the lock entry name and `source` of the
  repository (both `null` for the serving repository), the commit, and the
  path. Where a result carries `status.references[].origin`, it shall be
  the `provenance.origin` of the reference target.
  <!-- agent proposal: OPEN-inheritance-06 -->
- **PK-INH-056:** Where processkit maps provenance to W3C PROV, it should
  use the mapping in `interfaces.yaml` (`prov_mapping`). processkit shall
  not emit a PROV serialization in v1.
  <!-- agent proposal: OPEN-inheritance-06 -->

## Upstream changes

- **PK-INH-020:** When `processkit lock --update [UPSTREAM...]` runs, the
  processkit CLI shall show the items added, changed, removed, and newly
  conflicting before it writes the lock.
  <!-- changed by owner decision: 2026-11-11 (#212), CLI style B -->
- **PK-INH-021:** processkit shall treat a lock change as an ordinary file
  change reviewed through Git, and shall not update the lock as a side
  effect of serving.

- **PK-INH-057:** Every run of `processkit lock` shall report a change
  summary in `data` in the shape of `schemas/lock-result.schema.json`,
  also with `--dry-run`, and shall print it with the plan before it asks
  for confirmation or writes. processkit shall compare the inherited items
  (the items that declared upstreams provide, after winners and before
  local items apply) of the current lock with those of the new lock. Where
  no winner selects one candidate, the inherited item is the set of all
  candidates. An item is added when only the new lock provides it, removed
  when only the current lock provides it, and changed when both provide it
  and its `provenance.origin` source or path, its `provenance.overrides`,
  or the bytes of any of its source files differ. An item is newly
  conflicting when the resolution with the new lock reports
  `inheritance.conflict` or `inheritance.winner-missing` for it and the
  resolution with the current lock does not.
  <!-- agent proposal: OPEN-inheritance-12 -->
- **PK-INH-058:** If a commit of the current lock is not in the local
  cache, then `processkit lock` shall treat the items of that entry as
  absent in the current lock and shall report
  `inheritance.previous-lock-unavailable` as a warning.
  <!-- agent proposal: OPEN-inheritance-12 -->

## Inherited access

- **PK-INH-030:** processkit shall not let access rules, Roles, or Bindings
  of an upstream grant access in a downstream repository unless the
  downstream configuration explicitly imports them.
- **PK-INH-031:** An upstream may mark items as restricted. If the
  downstream configuration does not import the upstream's access rules, then
  a downstream shared server shall not serve a restricted inherited item.
  Where the upstream's access rules are imported, the shared server shall
  serve a restricted inherited item to a caller only when both the upstream
  rules and the downstream rules allow it.
- **PK-INH-059:** processkit shall import access rules only through the
  operator configuration key `inheritance.import-access-rules`, a list of
  lock entry names. Project configuration and repository content shall not
  import access rules. If an entry name in the list is not in the lock,
  then processkit shall report `inheritance.import-unknown-upstream` as a
  warning and shall import nothing for it.
  <!-- agent proposal: OPEN-inheritance-09 -->
- **PK-INH-060:** When the access rules of an upstream are imported, the
  Roles and Bindings that this upstream declares itself (its local items)
  shall grant access in the downstream repository in addition to the
  downstream's own rules, as `access-control@v1` evaluates them. In
  PK-INH-031, "the downstream rules" shall mean the Roles and Bindings that
  the downstream repository declares itself.
  <!-- agent proposal: OPEN-inheritance-09 -->
- **PK-INH-061:** A repository shall mark its own items as restricted in
  the list `restricted` of the `[downstream]` table of `processkit.toml`,
  as typed names (`schemas/inheritance-config.schema.json`). An item shall
  stay restricted in every downstream repository, and only the import of
  the access rules of the repository that marked it shall satisfy
  PK-INH-031. If a typed name in the list names no local item, then
  processkit shall report `inheritance.restricted-unknown-item` as a
  warning.
  <!-- agent proposal: OPEN-inheritance-08 -->
- **PK-INH-062:** While processkit serves over stdio or runs a CLI command,
  processkit shall serve restricted inherited items to the local principal
  like every other item (`access-control@v1` PK-ACC-001) and shall report
  `provenance.restricted` as `true`.
  <!-- agent proposal: OPEN-inheritance-08 -->
