# CLAUDE.md — processkit

This file exists because Claude Code auto-loads `CLAUDE.md` at startup.

The canonical agent instructions for this repo are **provider-neutral**
and live at **`AGENTS.md`** (at the repository root). Read that file
first. After AGENTS.md, the next deeper briefing is
`context/HANDOVER.md`.

## Why two files?

processkit aims to be consumable by any agent harness, not just Claude
Code. Following the [agents.md](https://agents.md/) ecosystem
convention, the authoritative agent instructions live in `AGENTS.md`.
Provider-specific files (`CLAUDE.md`, future `CODEX.md`, etc.) are thin
pointers that exist only because each harness auto-loads its own
filename. Add genuinely Claude-Code-specific content here only — slash
command bindings, settings.json guidance, Claude-Code-only skills under
`.claude/skills/`. Everything else belongs in `AGENTS.md`.

## Claude-Code-specific notes

(Currently none. This file is a pointer only.)
