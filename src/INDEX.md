# src/

**The content processkit ships to consumers.** Treat this like source code: it
is the canonical material that gets installed into a project by `aibox init`
(or any future consumer) when pinned to a processkit tag.

## Layout

```
src/
├── primitives/      ← 18 process primitives (schemas, state machines, format spec)
├── skills/          ← multi-artifact skill packages
├── processes/       ← process definitions (code-review, release, ...)
└── packages/        ← package tier definitions (minimal, managed, ...)
```

## Rule

Anything in `src/` is shipped. Anything outside `src/` is about *this repo*
(its dev environment, its own context, its own docs). Do not mix the two.

- `.devcontainer/`, `aibox.toml`, `CLAUDE.md` → repo infrastructure
- `context/` → this repo's own project-management artifacts
- `.claude/skills/` → skills the agent uses ON this repo
- `docs-site/` → processkit's user-facing documentation
- `src/` → **the content shipped to consumers**

When a consumer runs `aibox init` with `processkit_version = "v0.2.0"`, the
files under `src/` (filtered by selected packages) are what get installed.
