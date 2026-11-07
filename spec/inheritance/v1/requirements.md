# Inheritance across repositories — requirements

This specification defines how a processkit repository inherits governance
content from upstream governing repositories: declaring named upstreams,
resolving them, including transitive upstreams, into a committed lock,
fetching locked commits only by explicit command, resolving one effective
set of items with explicit overrides, final items and rules, declared
winners between upstreams, and provenance on every served item, reviewing
upstream changes, and the rule that upstream access rules grant nothing
downstream unless imported. It does not define the item envelope and
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
  commit and content digest and shall write `processkit.lock`. processkit
  shall serve inherited content only from locked commits.
- **PK-INH-003:** processkit shall fetch upstream content only through the
  explicit command `processkit fetch`. Serving and validation shall not
  access the network.
- **PK-INH-004:** If an upstream is missing, unreachable, or does not match
  its locked content digest, then `processkit lock` or `processkit fetch`
  shall fail and report the exact upstream and the reason, and processkit
  shall not silently replace it by another revision.

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

## Upstream changes

- **PK-INH-020:** When `processkit lock --update [NAME]` runs, the processkit
  CLI shall show the items added, changed, removed, and newly conflicting
  before it writes the lock.
- **PK-INH-021:** processkit shall treat a lock change as an ordinary file
  change reviewed through Git, and shall not update the lock as a side
  effect of serving.

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
