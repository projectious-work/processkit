---
sidebar_position: 13
title: "Artifact"
---

# Artifact

A completed deliverable — document, dataset, build, diagram, URL,
runbook, slide deck, or any other produced output. A catalogue record,
not a work-tracking entity.

| | |
|---|---|
| **ID prefix** | `ART` |
| **State machine** | none |
| **MCP server** | `artifact-management` |
| **Skill** | `artifact-management` (Layer 2) |

## Two usage patterns

**Self-hosted** — the content lives in the entity file's Markdown body.
`location` is omitted or used as an optional secondary pointer.

**Pointer** — the content lives externally (Figma, Google Drive, S3, a
git path). `location` is required; the body may be empty or contain a
summary.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string | Human-readable name |
| `kind` | enum | `document` · `design` · `dataset` · `build` · `slides` · `video` · `spec` · `diagram` · `url` · `other` |

### Optional

| Field | Type | Description |
|---|---|---|
| `location` | string | Path, URL, repo ref, or storage identifier |
| `format` | string | File format or MIME type (`pdf`, `png`, `application/json`, …) |
| `version` | string | Version identifier |
| `checksum` | string | Hash for integrity verification |
| `owner` | `ACTOR-*` | Actor responsible for this artifact |
| `produced_by` | string | Entity that produced it (workitem, process, decision ID) |
| `produced_at` | datetime | When the artifact was produced |
| `tags` | string[] | Freeform tags for retrieval |

## Examples

### Self-hosted (document body in the file)

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260411_0903-BrightVale-deploy-runbook
  created: '2026-04-11T09:03:00Z'
spec:
  name: Deploy Runbook — v0.12.0
  kind: document
  tags: [runbook, deploy, v0.12.0]
  produced_at: '2026-04-11T09:03:00Z'
---

## Steps

1. Run smoke tests: `uv run scripts/smoke-test-servers.py`
2. Stamp provenance: `bash scripts/stamp-provenance.sh vX.Y.Z`
...
```

### Pointer (external file)

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260411_0904-NeatDawn-brand-design-system
  created: '2026-04-11T09:04:00Z'
spec:
  name: Brand Design System
  kind: design
  location: https://www.figma.com/file/abc123/brand-design-system
  format: figma
  owner: ACTOR-design-team
  tags: [brand, design-system]
---
```

## Notes

- Artifact has **no state machine** — it is a catalogue record, not a
  work-tracking entity. Use WorkItem to track the work that produces it.
- `query_artifacts` supports filtering by `kind`, `tags`, and title
  substring.
- For long-lived reference documents that agents should read, prefer
  the `context-management` skill; for point-in-time deliverables,
  use Artifact.
