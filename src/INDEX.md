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

## AGENTS.md placeholder contract (scaffolding)

`src/scaffolding/AGENTS.md` is rendered into a consumer project's root by
the installer at install time. It uses `{{TOKEN}}`-style placeholders that
fall into three classes. The contract is **one-directional**: installers
substitute the Class A names they recognize and leave every other token
literal, so processkit can introduce Class B/C names freely without
breaking any installer, and an installer can add new Class A names
without breaking processkit's template.

### Class A — installer-rendered (coordination contract)

Names that the project's installer substitutes from its own configuration
at render time. Adding a name to Class A is a coordination step with each
installer that implements the contract — currently `aibox` is the only
known one (see the aibox docs for the authoritative Class A list and the
source for each value).

Class A names processkit's `src/scaffolding/AGENTS.md` currently uses:

- `{{PROJECT_NAME}}` — the project name
- `{{PROCESSKIT_SOURCE}}` — processkit upstream URL
- `{{PROCESSKIT_VERSION}}` — pinned processkit version tag
- `{{CONTEXT_PACKAGES}}` — processkit package tier(s) in use
- `{{AI_PROVIDERS}}` — AI providers configured for the project
- `{{INSTALL_DATE}}` — render-time date (`YYYY-MM-DD`)

processkit deliberately avoids Class A names that embed installer-specific
vocabulary (e.g. `{{AIBOX_VERSION}}`, `{{AIBOX_BASE}}`, `{{ADDONS}}`),
even when the installer offers them, to keep the template
installer-neutral. Other installers can implement the same names later
without coordination on processkit's side.

### Class B — owner-supplied (processkit's vocabulary)

Information only the project owner knows. The agent fills these by
interviewing the owner during the first-time-setup protocol that the
template's `## ⚠ First-time setup` section walks through. processkit owns
this vocabulary and can grow it freely; installers pass these tokens
through unchanged.

Class B names currently used:

- `{{PROJECT_DESCRIPTION}}` — one-paragraph description of the project
- `{{PROJECT_PURPOSE}}` — the problem the project exists to solve
- `{{CODE_STYLE_NOTES}}` — non-linter conventions
- `{{PR_CONVENTIONS}}` — PR review and merge process
- `{{NONOBVIOUS_GOTCHAS}}` — things not visible from the code
- `{{PROCESSKIT_PREFS}}` — processkit runtime preferences (ID format,
  directory overrides, sharding). Agent edits per-skill config files
  under `context/skills/<name>/config/settings.toml` and summarises
  choices here.

### Class C — discoverable + owner-confirmable (processkit's vocabulary)

Information the agent can extract from the codebase and propose for owner
confirmation. processkit owns this vocabulary too.

Class C names currently used:

- `{{BUILD_COMMAND}}` — install + build command
- `{{TEST_COMMAND}}` — test runner command
- `{{LINT_COMMAND}}` — linter / formatter check command

### Markup

Each non-Class-A placeholder is preceded by an HTML comment of the form:

```
<!-- PLACEHOLDER:NAME class=B|C
     Free-text description for the agent explaining what the value is
     and where to find it. -->
```

Both the comment and the placeholder are deleted by the agent when the
value is written in. Placeholders without an annotation default to
**Class B** (interview the owner). Class A placeholders typically appear
without per-occurrence annotation — their meaning is self-evident in
context, and if any are still literal after install the agent falls back
to reading the installer's config file directly.
