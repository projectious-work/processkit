# src/

**The content processkit ships to consumers.** Treat this like source code: it
is the canonical material that gets installed into a project by `aibox init`
(or any future consumer) when pinned to a processkit tag.

## Layout

```
src/
├── PROVENANCE.toml  ← (v0.4.0+) maps every shipped file to the version it last changed
├── primitives/      ← 19 process primitives (schemas, state machines, format spec)
├── skills/          ← multi-artifact skill packages
├── processes/       ← process definitions (code-review, release, ...)
├── packages/        ← package tier definitions (minimal, managed, ...)
├── lib/             ← shared Python library used by MCP servers (NOT a primitive — internal infra)
└── scaffolding/     ← project-init templates (AGENTS.md, etc.) installed at consumer's project root
```

## Rules

**Rule 1 — `src/` vs everything else.** Anything in `src/` is shipped.
Anything outside `src/` is about *this repo* (its dev environment, its
own context, its own docs). Do not mix the two.

- `.devcontainer/`, `aibox.toml`, `CLAUDE.md`, `AGENTS.md` → THIS repo's
  infrastructure (the AGENTS.md at the repo root is processkit's own;
  the shipped template lives at `src/scaffolding/AGENTS.md`)
- `context/` → this repo's own project-management artifacts
- `.claude/skills/` → skills the agent uses ON this repo
- `docs-site/` → processkit's user-facing documentation
- `scripts/` → developer-facing scripts (release, smoke test, diff)
- `src/` → **the content shipped to consumers**

**Rule 2 — provider-neutral and aibox-neutral.** Content under `src/`
must work for a consumer who never installs aibox and who uses a
non-Claude agent harness. Reference processkit's own internals (MCP
servers, the index, the lib, primitives) freely; do not reference
`aibox.toml`, `aibox sync`, `CLAUDE.md`, or any provider-specific path.

When a consumer installs processkit (e.g. by running `aibox init` with
`processkit_version = "v0.4.0"`, or by manually copying files from a
tagged release), the content under `src/` is what gets installed.

## PROVENANCE.toml

`src/PROVENANCE.toml` (added in v0.4.0) is a single file that maps every
shipped file to the git tag in which its content last changed. It is the
input to `scripts/processkit-diff.sh` and to aibox's migration generator.

The release process regenerates it via `scripts/stamp-provenance.sh
<next-version>` before tagging. Do not edit by hand. Forks regenerate
against their own git history; the `[source]` block identifies which
project the provenance map belongs to.

## Privacy convention for files installed into a project's `context/`

Per `primitives/FORMAT.md`, every entity has an optional `privacy:` field
with three tiers: `public`, `project-private` (default), `user-private`.

**Filesystem rule (enforced by `aibox lint`):** entities with
`privacy: user-private` MUST live under a directory named `private/`
somewhere within `context/`. The default `.gitignore` shipped by aibox
includes:

```
context/**/private/
```

This pattern matches `private/` directories at any depth under `context/`,
including directly under `context/` itself, because `**` matches zero or
more path components. So all of these are excluded from git:

- `context/private/...`
- `context/owner/private/team-and-relationships.md`
- `context/foo/bar/private/...`

But NOT directories named `private/` outside `context/` (e.g.
`cli/src/private/` would NOT be ignored by this rule).

The `owner-profiling` skill uses this convention for
`context/owner/private/team-and-relationships.md`. Other user-private
entities follow the same rule.
