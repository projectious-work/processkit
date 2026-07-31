---
title: "Rust Library API"
description: "Supported typed integration surface for the processkit executable."
weight: 12
---

The `processkit` crate exposes the versioned request envelope used by
`processkit execute --request`. The supported alpha surface is intentionally
small:

- `API_VERSION` identifies the machine protocol;
- `Operation` enumerates supported lifecycle operations; and
- `InstallerRequest` constructs and serializes typed request envelopes.

Build and test the API documentation with:

```sh
cargo test --doc --locked --manifest-path installer/Cargo.toml
cargo doc --locked --no-deps --manifest-path installer/Cargo.toml
```

Public items follow semantic versioning within the v1 release line. Modules
and functions not reachable from the crate root are internal implementation
details and may change between prereleases. Filesystem transactions, release
verification, and lifecycle execution remain behind the executable boundary;
the library does not offer an alternate mutation path.
