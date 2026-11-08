# 2. `processkit lock` resolves only from fetched data

Date: 2026-11-08

## Status

Accepted. Owner decision on #213, finding 3 (agent working conversation,
2026-11-08).

## Context

`security@v1` PK-SEC-005 allows only `processkit fetch` and the shared
server to use the network. But the baseline described `processkit lock` as
resolving upstream refs, which needs the remote repository. The two
requirements contradicted each other.

## Decision

Fetch, then lock.

- `processkit fetch` fetches every declared upstream into the local cache,
  including upstreams that are not locked yet.
- `processkit lock` resolves refs only from the local cache. If data is
  missing, `lock` fails as an environment failure and names the fix
  (`processkit fetch`).
- The network boundary of PK-SEC-005 is unchanged.

## Consequences

- One command owns network access, so it is easy to audit, sandbox, and run
  offline (`cli@v1` PK-CLI-005, PK-CLI-044).
- A first lock needs two commands: `processkit fetch`, then
  `processkit lock`.
- `cli@v1`, `inheritance@v1`, and `security@v1` cite this ADR.
