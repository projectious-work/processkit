# Inheritance across repositories

Organizations govern in levels: a company sets rules, a business unit or team
refines them, and a project applies them and adds its own. In processkit
each level is a repository, and a repository inherits from the levels above.

```text
company-standards        (governing)
  └── platform-team      (governing; inherits company-standards)
        └── payments-api (project; inherits platform-team)
```

## Declaring upstreams

```toml
[[upstream]]
name = "company"
source = "https://git.example.com/company/standards.git"
ref = "v3.2.0"

[[upstream]]
name = "platform"
source = "https://git.example.com/platform/standards.git"
ref = "main"
```

- **PK-INH-001:** a repository MAY declare any number of named upstreams in
  configuration, each with a Git source and a ref.
- **PK-INH-002:** `processkit lock` MUST resolve every ref, including
  transitive upstreams, to an exact commit and content digest and write
  `processkit.lock`. Serving MUST use only locked commits.
- **PK-INH-003:** fetching MUST happen only through an explicit command,
  `processkit fetch`. Serving and validation MUST NOT access the network.
- **PK-INH-004:** a missing, unreachable, or digest-mismatched upstream MUST
  fail lock or fetch with the exact upstream and reason, and MUST NOT be
  replaced silently by another revision.

## Resolution

Resolution produces one effective set of items from the repository and its
locked upstreams.

- **PK-INH-010:** resolution MUST be deterministic for a given repository
  revision and lock.
- **PK-INH-011:** inherited items keep their upstream identity. A local item
  with the same kind and name as an inherited item is a conflict unless it
  declares an explicit override.
- **PK-INH-012:** an override MUST name the overridden upstream item and
  version and state a reason. An override MAY replace the item, add rules, or
  change a rule's level, as declared by the item's schema.
- **PK-INH-013:** an upstream MAY mark an item or rule `final`. A downstream
  override of a final item or rule MUST fail validation.
- **PK-INH-014:** when two upstreams provide the same item, the repository
  MUST declare which one wins. Upstream declaration order MUST NOT decide
  silently.
- **PK-INH-015:** every served item MUST carry its provenance: originating
  repository, commit, path, and every override applied on the way.
- **PK-INH-016:** an override that no longer matches the upstream version it
  names MUST be reported as stale by `processkit validate`.

## Upstream changes

- **PK-INH-020:** `processkit lock --update [NAME]` MUST show the items added,
  changed, removed, and newly conflicting before writing the lock.
- **PK-INH-021:** a lock change is an ordinary file change reviewed through
  Git. processkit MUST NOT update the lock as a side effect of serving.

## Inherited access

- **PK-INH-030:** access rules, Roles, and Bindings of an upstream MUST NOT
  grant access in a downstream repository unless the downstream configuration
  explicitly imports them.
- **PK-INH-031:** an upstream MAY mark items as restricted. A downstream
  shared server MUST NOT serve a restricted inherited item unless it imports
  the upstream's access rules, and then a caller sees the item only when both
  the upstream and the downstream rules allow it.
