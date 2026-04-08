---
name: actor-profile
description: |
  Create and maintain Actor entities — humans and AI agents that participate in the project. Use when adding a new collaborator (human or agent) to the project, updating their preferences/expertise, or querying who does what.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-actor-profile
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 1
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Actor]
      mcp_tools:
        - create_actor
        - get_actor
        - update_actor
        - deactivate_actor
        - list_actors
      templates: [actor-human, actor-agent]
---

# Actor Profile Management

## Intro

Actors are the entities that do things in the project — humans, AI agents, and
services. This skill creates and maintains their profiles: name, type, contact,
expertise, preferences, working style.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### When to create an Actor

Create an Actor entity the first time a person or agent participates in a
way the project needs to remember:
- Someone gets assigned a WorkItem → create their Actor if missing.
- An agent starts making decisions → create its Actor.
- A service account performs automated actions → create its Actor.

Do **not** promote every mention of a person into an Actor. Actors are for
collaborators with ongoing involvement, not for every name that appears in a
commit message.

### Actor types

| type         | Example                                     |
|--------------|---------------------------------------------|
| `human`      | Project members, reviewers, stakeholders    |
| `ai-agent`   | Claude, Copilot, Aider, Cursor, custom MCP  |
| `service`    | GitHub Actions, CI bots, deploy pipelines   |

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-alice
  created: 2026-04-06T00:00:00Z
spec:
  type: human
  name: "Alice Chen"
  email: alice@example.com
  expertise: [backend, databases, rust]
  preferences:
    commit_style: conventional
    timezone: Europe/Berlin
  active: true
---

Optional Markdown body — bio, context, working-style notes.
```

### Workflow

1. Pick an ID: `ACTOR-<short-name>` where short-name is memorable and unique.
2. Set `type` (human / ai-agent / service).
3. Fill in `name` + contact (email for humans; nothing for agents; service
   account identifier for services).
4. Record `expertise` as a tag list — used by assignment skills.
5. Write the Actor file to `context/actors/`.
6. Log a `LogEntry` with `event_type: actor.created`.

## Full reference

### Fields

| Field           | Type              | Notes                                                     |
|-----------------|-------------------|-----------------------------------------------------------|
| `type`          | enum              | `human` / `ai-agent` / `service`                          |
| `name`          | string            | Display name. For agents: model name + version.           |
| `email`         | string            | Optional. Human actors only.                              |
| `handle`        | string            | Optional. GitHub handle, Slack user, etc.                 |
| `expertise`     | list[string]      | Tags used by assignment suggestions.                      |
| `roles`         | list[string]      | Role IDs. For scoped roles prefer a Binding over this.    |
| `preferences`   | map               | Free-form. See conventional keys below.                   |
| `active`        | bool              | `false` = profile preserved but no new work assigned.     |
| `joined_at`     | datetime          | When they became part of the project.                     |
| `left_at`       | datetime          | When they stopped (sets `active: false`).                  |

### Conventional preference keys

- `commit_style`: `conventional` / `freeform`
- `timezone`: IANA name
- `review_style`: `strict` / `pragmatic` / `light`
- `communication`: `async` / `sync` / `mixed`
- `languages`: human languages for communication

These are conventions, not enforced. Projects may add any preferences they like.

### Scoped roles: use a Binding, not the `roles` field

`spec.roles` is a shortcut for "Alice is a developer" when that's true
everywhere in the project. If "Alice is the tech lead for Project X but a
regular developer everywhere else", use a Binding entity instead:

```yaml
kind: Binding
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-tech-lead
  scope: SCOPE-project-x
```

See `skills/binding-management` for details.

### Deactivation, not deletion

When an actor leaves the project, set `active: false` and `left_at`. Do not
delete the file — historical LogEntries and Bindings reference it. Queries
for "current team" should filter by `active: true`.

### Privacy considerations

Actor files are checked into git and visible to everyone with repo access.
Do not put sensitive contact info (phone, home address) in Actor files.
Keep email optional — agents and services do not need one.
