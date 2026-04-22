---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_0231-TallWillow-v0-19-0-phase
  created: '2026-04-22T02:31:38+00:00'
  updated: '2026-04-22T06:07:14+00:00'
spec:
  title: v0.19.0 Phase 2 — Team-manager skill (replaces actor-profile)
  state: done
  type: task
  priority: high
  assignee: ACTOR-developer
  description: 'Replace `actor-profile` skill with `team-manager`. Clean break (no
    backward-compat per user directive).


    **Skill location**: `context/skills/processkit/team-manager/`


    **MCP tools**

    - Lifecycle: create_team_member, get_team_member, list_team_members, update_team_member,
    deactivate_team_member, reactivate_team_member

    - Name pool: reserve_name, release_name, list_available_names, suggest_name

    - Memory tree scaffolding: init_memory_tree(slug) — creates knowledge/, journal/,
    skills/, relations/, lessons/, private/ with .gitkeep and frontmatter templates

    - Export/import: export_team_member(slug) → tarball (A2A-signed card); import_team_member(tarball)
    with signature validation; respects export_policy (default-excludes journal/ and
    project-scoped)

    - Consistency: check_consistency(slug), check_all_consistency() — returns 10 check
    categories (see Phase 6 for pk-doctor wiring)


    **Name pool**: `data/name-pool.yaml` shipped with ~60 curated international English
    names (Alice, Aria, Ava, Cora, Emma, Eva, Hazel, Iris, Ivy, Kira, Lara, Lena,
    Lily, Luna, Maya, Mia, Nina, Nora, Ruby, Sara, Sophie, Zoe; Adam, Alex, Cole,
    Dean, Eli, Ethan, Felix, Finn, Henry, Ivan, Jack, Leo, Liam, Luke, Mark, Max,
    Milo, Noah, Oscar, Owen, Theo, Tim; Avery, Blake, Casey, Dana, Jamie, Jordan,
    Kai, Morgan, Quinn, Rae, Riley, Robin, Sage, Sam, Taylor). One-shot reservation.


    **Done when**

    - Skill validates; MCP tools callable.

    - `actor-profile/` skill removed.

    - Name pool enforced on `create_team_member` for type=ai-agent.

    - A2A Agent Card schema wired; signature verification available.

    - Export/import tested with a scratch team-member.'
  started_at: '2026-04-22T05:31:42+00:00'
  completed_at: '2026-04-22T06:07:14+00:00'
---

## Transition note (2026-04-22T05:31:42+00:00)

Starting Phase 2: build team-manager skill (replaces actor-profile) with MCP server, name pool, memory-tree scaffolding, A2A card export/import, and 10 consistency checks.


## Transition note (2026-04-22T06:07:06+00:00)

team-manager skill complete: 14 files, 17 MCP tools, 49 pytest tests passing, dual-tree mirror clean. processkit lib extended with TeamMember kind. 59 names in pool. 10 consistency checks implemented.
