---
name: roadmap
description: Maintain a product roadmap in roadmap.yaml with item/phase statuses (idea, planned, in_progress, done, shipped, cancelled) and development notes. Use when creating or changing a roadmap, starting or finishing a roadmap phase or feature, changing an item's status, or preparing a release.
---

# Roadmap

## Source of truth

- The roadmap is machine-readable YAML in `roadmap.yaml` at the repository
  root, or at a path the README documents.
- Rendered pages (website, Markdown) are generated from it and checked for
  drift. They never become a second source of truth.
- The roadmap states user outcomes and commitment, not an implementation
  inventory. Tickets hold the tasks; roadmap items link to them.

Schema and example: `references/roadmap-yaml.md`.

## Statuses

| Status | Meaning | Entry condition |
|---|---|---|
| `idea` | exploratory, non-committal | none |
| `planned` | intended and sequenced, not started | outcome and rough scope agreed |
| `in_progress` | active work | visible owner and evidence (baseline, branch, PR) |
| `done` | implemented, integrated into the development branch, validated | completion evidence (see below); release may be pending |
| `shipped` | available in a named published release | `done` evidence + release gates + `release` field |
| `cancelled` | intentionally not pursued | rationale or decision reference |

Normal progression: `planned` → `in_progress` → `done` → `shipped`. Status is
observed state, never a wish. Never upgrade a status because code exists or a
PR merged. Reopen an item as `in_progress` when its completion evidence no
longer holds.

## Becoming `done`

All of these agree before the status changes:

1. accepted scope implemented and integrated into the development branch;
2. required verification passes and the conformance matrix is accepted;
3. version-appropriate documentation describes the behavior;
4. a development note exists for non-trivial items (`devNote` field).

## Becoming `shipped`

`done` evidence plus the applicable release gates, publication, and release
evidence; the `release` field names the published release. Several `done`
items may ship together in one release. Public roadmaps show unreleased
`done` items as **Done — awaiting release**.

## With the spec-driven development cycle

| Cycle event | Roadmap status |
|---|---|
| baseline and plan approved (§5) | `planned` (if it was `idea`) |
| implementation waves start (§6) | `in_progress` |
| PR merged | stays `in_progress` |
| phase complete (§10) | `done` |
| released with release evidence | `shipped` |

## Development notes

Non-trivial items and architectural changes keep a note in
`dev-notes/<roadmap-id>-<slug>.md`, updated during the work. It records:
scope and status; implemented behavior and boundaries; decisions,
alternatives, and deviations; tests and manual validation including gaps;
security, compatibility, migration, and operational consequences; docs
changed; and follow-up work with ticket links. It explains why and what was
proven. It does not narrate commits or replace user documentation.

## Validation

Validate `roadmap.yaml` against its schema on every change. Reject duplicate
IDs, unknown statuses, `shipped` without `release`, non-trivial `done` or
`shipped` without `devNote`, broken `dependencies`, and references to missing
notes.
