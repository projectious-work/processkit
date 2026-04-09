# Draft: aibox issue — separate processkit config from aibox.toml

**Target repo:** projectious-work/aibox
**Kind:** architecture / enhancement

---

## Title

Remove processkit runtime settings from aibox.toml — introduce processkit.toml

## Summary

Several settings currently documented (and consumed by processkit's MCP
servers) inside `aibox.toml [context]` are processkit's responsibility,
not aibox's. This creates an unwanted tight coupling: a project that
installs processkit *without* aibox has no place to put them, and
processkit's lib reads from an aibox-named file.

processkit has introduced `processkit.toml` as its native config file
(shipped as `src/scaffolding/processkit.toml` starting in v0.8.0).
aibox should:

1. Stop writing processkit runtime settings into `aibox.toml [context]`.
2. Generate `processkit.toml` at `aibox init` / `aibox sync` time,
   populated from the owner's preferences gathered during first-time
   setup.
3. Leave `aibox.toml [context]` with only the two settings that are
   genuinely aibox-owned: `schema_version` and `packages`.

## Affected aibox.toml settings

### Move to processkit.toml (processkit-owned)

| Old key (in `[context]`) | New key (in processkit.toml) | Default |
|---|---|---|
| `id_format` | `[ids] format` | `"word"` |
| `id_slug` | `[ids] slug` | `false` |
| `[context.directories.<Kind>]` | `[directories] <Kind>` | per-kind defaults |
| `[context.sharding.<Kind>]` | `[sharding.<Kind>]` | none |
| `[context.index] path` | `[index] path` | `context/.cache/processkit/index.sqlite` |
| `[context.budget]` | `[context.budget]` (in processkit.toml) | none |
| `[context.grooming]` | `[grooming.rules]` (in processkit.toml) | none |

### Stay in aibox.toml (aibox-owned)

| Key | Reason |
|---|---|
| `[context] schema_version` | aibox installer manages this |
| `[context] packages` | aibox installer reads this to select skills |

## Project root marker

processkit's `paths.find_project_root()` previously looked for
`aibox.toml` as the project root marker. It now tries, in order:
`AGENTS.md`, `processkit.toml`, `aibox.toml`.

This means aibox-managed projects continue to work without any change.
Projects without aibox can use `AGENTS.md` or `processkit.toml` as the
marker. No action required from aibox on this point, but it is worth
knowing that `aibox.toml` is now a third-priority fallback.

## processkit.toml format (reference)

```toml
# processkit.toml — processkit runtime configuration

[ids]
format = "word"   # word | uuid
slug   = false    # append a content-derived slug from the entity title

# [directories]
# WorkItem       = "workitems"
# LogEntry       = "logs"
# DecisionRecord = "decisions"

# [sharding.LogEntry]
# scheme  = "date"
# pattern = "context/logs/{year}/{month}/"

# [index]
# path = "context/.cache/processkit/index.sqlite"
```

The full annotated template is at
`src/scaffolding/processkit.toml` in the processkit repo.

## What aibox needs to do

### aibox init

After gathering the owner's processkit preferences (ID format, slug,
directory overrides, sharding), generate `processkit.toml` at the
project root using the template from
`context/templates/processkit/<version>/scaffolding/processkit.toml`.

The AGENTS.md first-time-setup section (see `{{PROCESSKIT_PREFS}}`
placeholder) documents the questions to ask.

### aibox sync

If `processkit.toml` does not exist (upgrading from an older layout),
migrate the relevant keys from `aibox.toml [context]` into a newly
generated `processkit.toml` and remove them from `aibox.toml`.

### aibox.toml template cleanup

Remove the `id_format`, `id_slug`, `[context.directories]`,
`[context.sharding]`, `[context.index]`, `[context.budget]`, and
`[context.grooming]` documentation from the generated `aibox.toml`
comment block. Only `schema_version` and `packages` belong there.

## Migration path for existing projects

processkit's `config.load_config()` already implements the fallback:
it reads `processkit.toml` first, then falls back to `aibox.toml
[context]`. Existing projects continue to work without changes. The
fallback will remain for at least two minor versions of processkit
after this issue ships, to give aibox time to generate `processkit.toml`
on sync.

## Processkit version

These changes land in processkit **v0.8.0** (pending):
- `src/lib/processkit/config.py` — reads processkit.toml, aibox.toml
  fallback
- `src/lib/processkit/paths.py` — `find_project_root` tries AGENTS.md,
  processkit.toml, aibox.toml
- `src/scaffolding/processkit.toml` — new scaffolding template
- `src/scaffolding/AGENTS.md` — `{{PROCESSKIT_PREFS}}` placeholder
  added to first-time setup
