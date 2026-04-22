---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260422_0234-BraveFalcon-curated-51-role-catalog
  created: '2026-04-22T02:34:05+00:00'
spec:
  title: Curated 51-role catalog with pure-ordinal seniority ladder (junior → specialist
    → expert → senior → principal)
  state: accepted
  decision: 'Expand the role catalog from 8 to 51 curated roles, grouped loosely by
    function (engineering, data/ML, security, architecture, product/program, design,
    marketing, sales, HR, finance, legal, operations, executive, plus generic `assistant`).
    Strip seniority from role slugs entirely — no jr-/sr- prefixes. Treat seniority
    as a pure ordinal attribute with a named ladder: `junior → specialist → expert
    → senior → principal`. Bindings (not role schemas) define what each seniority
    means in terms of model capability, effort, context budget, and tool scope. Ship
    a default binding pack with sensible starter mappings; projects override via their
    own bindings. Roles remain descriptive routing labels (not restrictive access
    control): their primary job is to cluster tasks by archetype so (role, seniority)
    can bind to (model, effort).'
  context: 'The current 8-role catalog (assistant, developer, jr-architect, jr-developer,
    jr-researcher, pm-claude, sr-architect, sr-researcher) has two problems: (1) too
    narrow — no coverage for data/ML, security, design, business/exec functions; (2)
    seniority is baked into slugs (jr-/sr-), creating duplicate role entities for
    the same responsibility set. Research on role taxonomies (SFIA v9 for IT, O*NET
    for cross-function, ESCO for EU mapping) confirms ~50-70 roles is the normal catalog
    size for a modern tech org. For AI agents, roles serve as logical/organizational
    labels rather than knowledge boundaries — any LLM can research domain knowledge
    on demand — so role granularity should serve routing and human management, not
    gatekeeping. Seniority attached as attribute rather than slug allows one role
    to span the capability ladder without duplication.'
  rationale: '(1) User curated a 51-role list from a ~65-role research catalog, targeting
    actual project needs over combinatorial completeness. (2) Pure-ordinal seniority
    decouples the label from its meaning: different projects/teams can legitimately
    map `senior` to different (model, effort) combinations (fast-prototype vs safety-critical).
    (3) Future-proof: new model tiers or effort levels are absorbed by binding updates,
    not ladder changes. (4) Ladder ordering `junior → specialist → expert → senior
    → principal` captures a progression from entry → niche-deep → broad-mastery →
    multi-domain-judgment → strategic/top, matching common (if non-unanimous) industry
    intent. (5) Simpler mental model: seniority is just a label; bindings decide what
    it means. (6) Mitigation for "no baked-in defaults" concern: shipped default binding
    pack gives any new processkit project sensible out-of-box mappings.'
  alternatives:
  - option: Ship the full ~65 researched roles
    rejected_because: File bloat for roles this project doesn't use; better to curate
      and extend on demand.
  - option: Keep seniority baked into slugs (jr-developer, sr-developer)
    rejected_because: Creates duplicate role entities and couples ladder changes to
      role-catalog changes.
  - option: Seniority with baked-in capability/effort defaults in the seniority definition
    rejected_because: Couples 'what senior means' to the ladder itself; bindings give
      per-project override without changing the ladder.
  - option: Numeric seniority (L1..L6) instead of named
    rejected_because: Less human-readable; the named ladder aligns with common industry
      language.
  - option: Alternative ordering expert→specialist (swap)
    rejected_because: 'User preference: specialist (narrow-deep) precedes expert (broad-mastery);
      captured in the final ladder.'
  consequences: Breaking change to role.yaml schema (seniority enum added; model_profiles[]
    removed — moved to bindings). Existing 8 roles are superseded and deleted in Phase
    6. docs-site, team roster, routing heuristics all need updates to reference new
    taxonomy. `jr-` and `sr-` slug prefixes disallowed by pk-doctor going forward.
    51 role YAML files to create. Team-manager consistency check enforces ladder enum
    membership on any team-member's `default_seniority` field.
  deciders:
  - ACTOR-20260421_0144-ThriftyOtter-owner
  related_workitems:
  - BACK-20260422_0231-WildSeal-v0-19-0-phase
  - BACK-20260422_0231-HonestFjord-v0-19-0-phase
  - BACK-20260422_0232-ShinyIvy-v0-19-0-phase
  - BACK-20260422_0232-CuriousOwl-v0-19-0-phase
  decided_at: '2026-04-22T02:34:05+00:00'
---
