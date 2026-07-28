---

---

The installer treats an archive, descriptor, manifest, catalog, adapter, and
target filesystem as untrusted until validated. It must reject absolute or
parent-traversal paths, archive links and path escapes, duplicate normalized
destinations, unsupported operations, unverified assets, and target symlink
escapes. It must not execute release-supplied code.

Before beta, tests must cover archive size/count limits, TOCTOU and symlink
races, interrupted application/recovery, malformed provenance, downgrade
policy, MCP command-array injection, and secret redaction in plans and state.
