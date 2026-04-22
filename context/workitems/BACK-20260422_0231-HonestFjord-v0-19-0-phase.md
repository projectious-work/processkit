---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_0231-HonestFjord-v0-19-0-phase
  created: '2026-04-22T02:31:58+00:00'
  updated: '2026-04-22T06:07:15+00:00'
spec:
  title: v0.19.0 Phase 4 — Role catalog (51 curated) + pure-ordinal seniority + T-shirt
    tiers + efforts
  state: done
  type: task
  priority: high
  assignee: ACTOR-sr-architect
  description: 'Expanded, de-seniority''d role catalog.


    **Roles (51 curated, user-approved list)**

    software-engineer, embedded-engineer, devops-engineer, site-reliability-engineer,
    cloud-engineer, database-engineer, observability-engineer, data-scientist, machine-learning-engineer,
    ai-research-scientist, research-scientist, security-operations-engineer, security-architect,
    qa-engineer, solutions-architect, enterprise-architect, cloud-architect, data-architect,
    technical-writer, community-manager, product-manager, product-owner, program-manager,
    scrum-master, chief-of-staff, product-designer, ux-designer, product-marketing-manager,
    seo-specialist, brand-manager, pr-manager, content-marketer, account-executive,
    sales-engineer, customer-success-manager, recruiter, learning-development-manager,
    financial-analyst, controller, treasury-analyst, general-counsel, compliance-officer,
    data-protection-officer, business-operations-analyst, coo, ceo, cto, cpo, cfo,
    cmo, assistant.


    **Conventions**

    - No seniority baked into role slugs (no jr-/sr-/senior-/junior- prefixes on role
    files).

    - Seniority is a pure ordinal tag; ladder: `junior → specialist → expert → senior
    → principal`.

    - Roles are descriptive labels (for routing + human team management), not restrictive.


    **Model capacity tiers** (in model.yaml `equivalent_tier`, and referenced by bindings)

    - `xs` / `s` / `m` / `l` / `xl` / `xxl`

    - Extensible both directions by convention (xxxs, xxxl, …).


    **Efforts** `[none, low, medium, high, extra-high, max]`

    - Alias `extra-high → xhigh` at the Anthropic provider adapter boundary.

    - `max` = provider-maximum thinking budget (per model artifact).


    **Done when**

    - 51 role files created under context/roles/; old 8 removed in Phase 6.

    - Ladder and tier/effort enums defined in schemas (Phase 1).

    - docs-site and team roster reference new taxonomies.'
  started_at: '2026-04-22T05:35:31+00:00'
  completed_at: '2026-04-22T06:07:15+00:00'
---

## Transition note (2026-04-22T05:35:31+00:00)

Starting Phase 4: 51 role files under context/roles/ with function_group attribute and seniority ladder accepted via schema v2.


## Transition note (2026-04-22T06:07:11+00:00)

51 role files created under context/roles/ + src/context/roles/, dual-tree clean for new files, all parse as valid Role entities with v2 schema attributes (default_seniority, function_group). 7 legacy files remain for Phase 6 cleanup.
