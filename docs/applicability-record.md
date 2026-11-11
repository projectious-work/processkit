# Applicability record

Record required by the company application-profiles standard
(`.standards/application-profiles.md`, "Applicability record"). Review it
when the product boundary or distribution model changes.

## Profiles and components

| Component | Profile |
| --- | --- |
| `processkit` CLI (`installer/`) | CLI application |
| MCP servers (`src/context/skills/*/mcp/`), local over stdio | MCP server, CLI stream rules |
| Shared server (v1 roadmap, access-controlled) | MCP server, remote, so also Service or worker |
| Schemas, ontology, templates (`src/context/`, `spec/`) | Schema, protocol, or process package |
| Documentation site (`docs-site/`) | Documentation website, so also the user-interface design standard |
| Shipped skills (`src/context/skills/`) and `AGENTS.md` | AI agent |

## Platforms and distribution

- Release targets: x86_64 and arm64 Linux, x86_64 and arm64 macOS (#165).
  v1 prereleases currently ship the native Linux ARM64 GNU target only.
- Distribution: signed GitHub Release assets, consumed by exact version.
  Documentation is published to `gh-pages` by the local publish script.
- MCP runtime: Python 3.10+ and `uv`, as intentional dependencies.

## Verification and release gates

`scripts/maintain.sh release` runs the candidate gates (`state`, `doctors`,
`audit`, `test`, `docs`, `build`) on `release/vX.Y.Z`, then `publish` and
`verify` on the target line. See `CONTRIBUTING.md`, "Releasing". The host-gated
release overlay applies: signing and native host builds run outside the dev
container.

## Twelve-Factor deviations beyond the company list

The company position table already covers III (CLI config), V (local
release), X (dev containers), and XI (CLI logs). processkit adds:

| Factor | Component | Deviation and rationale |
| --- | --- | --- |
| II Dependencies | Local MCP servers | Each server's PEP 723 header declares version ranges (`mcp[cli]>=1.0,<2.0`), which `uv` resolves on first run when a server is started on its own. The release pins them: `installer/python-runtime.in` is compiled with hashes into the release-owned runtime lock. |

No further deviation is identified for the local stdio servers. The shared
server does not exist yet. Its Twelve-Factor review is due when the
shared-server roadmap phase starts.

## Obligations added by standards v2.2.0

| Obligation | Status |
| --- | --- |
| CLI command style recorded in an ADR (`command-line-interface-design.md`) | Met. Style B (kubectl), ADR `docs/adr/0001-cli-command-style.md`, accepted 2026-11-11 (#212). |
| AI agent profile: each shipped skill and `AGENTS.md` states job, persona, instructions, tools, model, and evaluation (`agent-building.md`) | Open (#217). Plan: extend the v1 skill metadata in `content-kinds@v1` with persona (by reference to the company default), model class, and evaluation cases. |
| Documentation site follows `user-interface-design.md` | Open (#218). Review `docs-site/` against the standard, then fix each finding or record it as a deviation here. |
| stdio MCP servers log to stderr | Met. The local servers write only protocol messages to stdout. |
| No configuration layer contains a secret | Met for v0. v1 is specified in `cli@v1` and `security@v1`. |

## Deviations from the specification lifecycle

| Rule (`specification-layout-and-lifecycle.md`, `git-branching-and-releases.md`) | Deviation and rationale |
| --- | --- |
| One freeze per slug: branch `spec/<slug>-v<N>`, squash title `docs(spec): freeze <slug>@v<N>` | The nine v1 specifications are frozen together in #212 on branch `spec/206-layout-cut-v1`, squash title `docs(spec): freeze the v1 specifications`, with one freeze commit and one tag `spec/<slug>/v1` per slug on the squash commit. They cite each other's requirements, so no single slug passes validation on `main` alone, and a slug frozen first could cite text that a later review changes. Owner decision 2026-11-11 (#212). One-time; later versions follow the rule. |

## Non-applicable or deferred requirements

- User-interface application profile: does not apply (no GUI).
- Infrastructure or template product profile: does not apply.
