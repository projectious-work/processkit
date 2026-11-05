# Retired processkit installation (2026-11-01, v1.x line)

This is the processkit installation that the `v1.x-dev` line used on itself,
up to installed version v0.28.4. It was retired when `aibox.toml` moved to
`[context] mode = "harness-only"`, matching the same change on
`v0.x-release` (#200).

Nothing here is active. The harness directories were renamed so that no agent
harness discovers them. The product source in `/src` and the installer in
`/installer` were not touched.

## Contents

| Path | Original location |
|------|-------------------|
| `context/` | `/context`: entities, logs, skills, schemas, templates |
| `harness/claude-skills/` | `/.claude/skills/pk-*` |
| `harness/claude-agents/` | `/.claude/agents/` (`cora`, `finn`) |
| `harness/agents-skills/` | `/.agents/skills/pk-*` |
| `harness/pre-unwire/` | Pre-change copies of the files listed below |

Files in `harness/pre-unwire/`: `AGENTS.md`, `CLAUDE.md`, `aibox.lock`,
`.gitignore`, `claude-settings.json`, `codex-hooks.json`. Local, untracked
harness files (`.mcp.json`, `.codex/config.toml`,
`.claude/settings.local.json`) are not part of this branch; their pre-unwire
copies are archived on `v0.x-release`.

`.gitignore` in this directory keeps the same files untracked that were
untracked before the move, including regenerable caches, template mirrors,
and private entity files.

## What was unwired

- `aibox.toml`: `[context] mode = "harness-only"`; removed the `[skills]`
  catalog, `[ai.mcp.gateway]`, `[processkit]`, and `[processkit.context]`.
- `aibox.lock`: removed the `[processkit]` table.
- `.claude/settings.json`: removed the skill-gate hooks, the gateway
  server, its permissions, and the managed keys. It now carries only the
  aibox attention hooks, as generated on `v0.x-release`.
- `.codex/hooks.json`: removed the skill-gate calls. It now carries only the
  aibox signals.
- `.gitignore`: removed the root `context/` runtime rules.
- `AGENTS.md`, `CLAUDE.md`: replaced the compliance contract, skill guards,
  team and MCP-manifest sections with neutral project instructions.

## Scripts that used the root `context/`

These were repointed after the retirement (2026-11-05):

- `scripts/build-release-tarball.sh`: runs the release audit from
  `src/context/` (the same script, byte-identical to the archived copy).
- `scripts/maintain.sh`: the release `doctors` and `audit` gates run the
  release audit from `src/context/` with `--tree=src-context`. `pk-doctor`
  is no longer run, because there is no live install to check.
- `scripts/check-src-context-drift.sh`: `--release-deliverable` works without
  a root `context/`; the default drift mode explains that the tree is retired.
- `scripts/generate-mcp-manifest.py` and `scripts/generate-mcp-preauth.py`:
  write only to `src/context/` while no root `context/` exists.
- `scripts/bench-aggregate-mcp-coldstart.py`: falls back to `src/context/`.

`scripts/processkit-diff.sh` and `scripts/test_processkit_diff.py` were not
changed; review them before relying on them. `CONTRIBUTING.md`, `README.md`,
and `docs/harness-claude-code.md` still describe the root `context/` tree.

## Restoring

Reverse the moves in the table above and restore the files from
`harness/pre-unwire/`. Restore the removed `aibox.toml` sections from git
history, set `[context] mode = "processkit"`, and run `aibox apply`.
