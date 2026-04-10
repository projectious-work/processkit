---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1840-AmberCliff-skill-finder-catalog-extension
  created: '2026-04-10T18:40:00+00:00'
spec:
  title: Extend skill-finder with user-facing catalog query mode
  state: backlog
  type: story
  priority: medium
  description: >
    skill-finder currently helps agents find the right skill to invoke. Extend
    it with a second mode — catalog — for user-facing skill discovery.


    **New catalog mode — capabilities:**

    - List all skills with configurable columns (name, category, description,
      tags, version, allowed-tools, …)
    - Filter by: category, tag, keyword in description/name
    - Sort by: name, category, version, or any frontmatter field
    - Output formats: Markdown table (default), JSON, YAML


    **Implementation approach:**

    1. Query processkit-index-management MCP (SQLite backend) using
       query_entities / search_entities for all entities of type skill.

    2. Map query results to requested columns from SKILL.md frontmatter fields.

    3. Format output inline — Markdown table for default, fenced JSON/YAML on
       request. No file artifact needed for simple queries.

    4. Add "Catalog queries" section to skill-finder SKILL.md with trigger
       phrases: "list skills", "what skills do we have", "show me all skills in X",
       "skills as JSON", etc.


    **Prerequisite:** BACK-20260410_1840-SteadyLeaf (skills directory
    reorganization) — catalog mode is most useful once category metadata is
    consistently populated in frontmatter.


    **No new MCP server required.** processkit-index-management already provides
    the query layer. This is a SKILL.md extension only.
---
