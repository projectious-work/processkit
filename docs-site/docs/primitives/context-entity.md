---
sidebar_position: 27
title: "Context"
---

# Context

A structured narrative document for long-lived ambient knowledge —
owner identity, working style, team relationships, grooming reports,
situational briefings. The value lives in the Markdown body.

| | |
|---|---|
| **ID prefix** | `CTX` (or custom, e.g. `OWNER`) |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `context-grooming` (Layer 4) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `description` | string | One-sentence summary of what this document holds |

### Optional

| Field | Type | Description |
|---|---|---|
| `purpose` | string | Why the document exists — when an agent should read it |
| `scope` | string | Where the context applies (`project`, `owner`, `team`, `sprint`) |
| `tags` | string[] | Freeform tags for retrieval |
| `sensitive` | boolean | `true` = body contains sensitive information (default: `false`) |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Context
metadata:
  id: OWNER-identity
  created: '2026-04-09T00:00:00Z'
spec:
  description: Owner identity, working style, and preferences for AI agents.
  purpose: |
    Read at session start to calibrate communication style and technical
    depth. Load before any substantive work begins.
  scope: owner
  sensitive: false
---

## Identity

Name: ...
Role: ...
Timezone: ...

## Working style

...
```

## Notes

- Context entities use the Markdown body (below the YAML frontmatter)
  for their primary content. The `spec` block is metadata only.
- Custom ID prefixes (e.g. `OWNER-identity`, `CTX-team-norms`) are
  idiomatic — the `CTX-` prefix is the default but not required.
- Sensitive context (`sensitive: true`) should live under
  `context/**/private/` to be excluded from git tracking and the
  docs-site build.
- Context grooming (`context-grooming` skill) prunes stale Context
  documents periodically — documents that have not been read or updated
  for a long time are candidates for archiving.
