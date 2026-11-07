# Retired processkit installation (2026-11-01)

This is the processkit installation that this repository used on itself, up to
installed version v0.28.8. It was retired when `aibox.toml` moved to
`[context] mode = "harness-only"`.

Nothing here is active. The harness directories were renamed so that no agent
harness discovers them. The product source in `/src` was not touched.

## Contents

| Path | Original location |
|------|-------------------|
| `context/` | `/context`: entities, logs, skills, schemas, templates |
| `harness/claude-skills/` | `/.claude/skills/pk-*` |
| `harness/claude-agents/` | `/.claude/agents/` (`cora`, `finn`) |
| `harness/agents-skills/` | `/.agents/skills/pk-*` |
| `harness/pk-doctor-allowlist.toml` | `/.pk-doctor-allowlist.toml` |
| `harness/pre-unwire/` | Pre-change copies of the files listed below |

Files in `harness/pre-unwire/`: `AGENTS.md`, `CLAUDE.md`, `aibox.lock`,
`.gitignore`, `claude-settings.json`, `claude-settings.local.json`, `mcp.json`,
`codex-hooks.json`, `codex-config.toml`.

`.gitignore` in this directory keeps the same files untracked that were
untracked before the move, including regenerable caches, template mirrors,
private entity files, and local harness configuration. Those files exist only
on the machine that made the archive, not in git.

## What was unwired

- `.mcp.json`, `.codex/config.toml`: removed the `processkit-gateway` server.
- `.claude/settings.json`: removed the skill-gate hooks, the gateway
  permission, and the managed keys. The aibox attention hooks stay.
- `.claude/settings.local.json`: removed the enabled server and the allow
  entries that named the root `context/` tree.
- `.codex/hooks.json`: removed the skill-gate calls. The aibox signals stay.
- `aibox.lock`: removed the `[processkit]` table.
- `.gitignore`: removed the root `context/` runtime rules.
- `AGENTS.md`, `CLAUDE.md`: replaced the compliance contract and the skill
  guards with neutral project instructions.

## Scripts that still expect a root `context/`

These stopped working, or lost part of their function, with this change. They
were left unchanged.

- `scripts/check-src-context-drift.sh`: compares root `context/` with
  `src/context/`.
- `scripts/generate-mcp-manifest.py`: writes the manifest to root `context/`
  and to `src/context/`.
- `scripts/processkit-diff.sh` and `scripts/test_processkit_diff.py`: review
  these before relying on them.

`CONTRIBUTING.md`, `README.md`, and `docs/harness-claude-code.md` also still
describe the root `context/` tree.

## Restoring

Reverse the moves in the table above and restore the files from
`harness/pre-unwire/`. Then set `[context] mode = "processkit"` in `aibox.toml`
and run `aibox apply`.
