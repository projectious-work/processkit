# Product roadmap and development evidence standard

## Purpose and scope

This standard defines how projectious.work software projects express future
direction and connect completed and shipped outcomes to implementation evidence.
It applies once a project discusses future work beyond the current release.

The canonical roadmap MUST be machine-readable YAML in `roadmap.yaml`, or at a
documented project-specific path. A rendered website or Markdown roadmap MAY be
generated from it, but MUST NOT become a competing source of truth.

## Principles

- Roadmaps communicate outcomes and commitment, not implementation inventory.
- Status is observed state. It is not a substitute for evidence.
- Dates are optional and appear only when the project will maintain them.
- Stable identifiers survive title, grouping, and sequencing changes.
- Planned behavior is never presented as shipped documentation.

## Required model

The roadmap schema MUST be versioned. It MUST support groups containing ordered
items or phases with these fields:

| Field | Requirement |
|---|---|
| `id` | Stable and unique within the project. |
| `title` | Short, outcome-oriented name. |
| `summary` | User or operator outcome, not only a component name. |
| `status` | One of `idea`, `planned`, `in_progress`, `done`, `shipped`, or `cancelled`. |
| `target` | Optional release, milestone, or date. |
| `dependencies` | Optional stable IDs whose outcomes are prerequisites. |
| `issues` | Optional external tracking references. |
| `decisions` | Optional governing decision references. |
| `devNote` | Required when a non-trivial item becomes `done`; retained when shipped. |
| `release` | Required for `shipped`; names a published release containing the outcome. |

Projects MAY extend this model with product-specific fields. Extensions MUST
not redefine the standard fields or statuses.

## Status semantics

- `idea`: exploratory and non-committal.
- `planned`: intended and sequenced, but implementation has not started.
- `in_progress`: active implementation has visible ownership and evidence.
- `done`: agreed scope is implemented, integrated into the applicable development
  branch, and validated; required documentation and development evidence are
  complete. Publication and release-wide gates may still be pending.
- `shipped`: available in the named published release and supported by conformance
  evidence, documentation, and a development note when required.
- `cancelled`: intentionally not proceeding; rationale or a decision reference
  is present.

The normal progression is `planned` → `in_progress` → `done` → `shipped`.
Changing an item to `done` requires agreement between its accepted scope, code,
tests, specification where present, version-appropriate documentation, and
development evidence. Merging code alone is insufficient. Incomplete item-level
acceptance remains `in_progress`; a pending release alone does not.

Changing an item to `shipped` additionally requires the applicable release gates,
publication, and release evidence. Several dependent items MAY become `done`
before a shared release gate and become `shipped` together in one named release.
An internal foundation MAY remain `done` when no separate release claim applies.

Implementation dependencies MAY be satisfied by `done` or `shipped` outcomes.
A dependency requiring released availability MUST explicitly require `shipped`
in the consuming item's acceptance criteria or a documented schema extension.
`target` expresses intent and MUST NOT substitute for actual release evidence.

Public roadmaps MUST distinguish completion from availability. Display unreleased
`done` outcomes as **Done — awaiting release**; internal-only foundations MAY use
**Done — internal foundation** when that scope is explicit. Neither label grants
a released support claim. Reopen an item as `in_progress` if its completion
evidence no longer supports the agreed scope.

## Development notes

Non-trivial roadmap phases and material architectural changes maintain a note
under `dev-notes/`, named with the roadmap ID and a descriptive slug. The note
evolves during implementation and records:

- roadmap item, scope, status, and intended reader;
- implemented behavior and important boundaries;
- decisions, alternatives, and deviations;
- tests and manual validation, including known gaps;
- security, compatibility, migration, and operational consequences;
- documentation and examples changed; and
- unresolved follow-up work linked to owned tracking items.

Development notes explain why and what was proven. They do not narrate commits
or replace stable user documentation.

## Validation

Projects MUST validate roadmap YAML against the declared schema. Validation
MUST reject duplicate IDs, unknown statuses, missing done or shipped evidence,
broken internal references, and references to absent development notes. Generated
roadmap pages MUST be reproducible locally and checked for drift.

Schema status enums, evidence conditions, validators, and renderers MUST support
`done` together. Adoption MUST NOT bulk-promote existing items: reconcile each
status against implementation and release evidence.

## Agent skill

Agents apply this standard through the
[`roadmap` agent skill](agent-skills/roadmap/SKILL.md).

## Agent briefing

> Treat `roadmap.yaml` as the roadmap source of truth. Do not upgrade status
> based on code presence alone. A done item has accepted implementation evidence;
> a shipped item additionally names its published release and release evidence;
> an idea remains explicitly non-committal.
