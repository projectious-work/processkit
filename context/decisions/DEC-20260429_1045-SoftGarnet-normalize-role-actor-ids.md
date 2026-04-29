---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260429_1045-SoftGarnet-normalize-role-actor-ids
  created: '2026-04-29T10:45:32+00:00'
spec:
  title: Normalize role actor IDs and preauth diagnostics
  state: accepted
  decision: Move the actor role allowlist from the nonstandard top-level x-allowed-role-ids
    key into Schema spec.role_actor_ids, rename the vendor-specific pm-claude role
    actor slug to product-manager, and extend processkit's preauth diagnostic surface
    to include Codex config as well as Claude settings.
  context: User reported derived-project evidence showing x-allowed-role-ids as an
    upstream standard deviation and pm-claude as a baked-in vendor name despite model
    routing now being provider-neutral. The same report identified harness preauthorization
    prompts in Claude Code and Codex after container rebuilds.
  rationale: The role actor allowlist is still useful because role-class Actor IDs
    intentionally bypass the full identity-class datetime format, but it should be
    modeled as normal Schema metadata rather than an x-* extension. Product-manager
    is a role concept; claude is a provider/model family and belongs only in Model
    records or bindings. Processkit owns the declarative preauth spec and diagnostics,
    while aibox owns merging those specs into generated harness configs.
  alternatives:
  - option: Keep x-allowed-role-ids and pm-claude
    reason: Lowest compatibility risk, but preserves nonstandard schema metadata and
      a vendor-specific role slug.
  - option: Remove role actor IDs entirely
    reason: Eliminates allowlist maintenance, but would permit any short ACTOR-* slug
      and weaken pk-doctor's data hygiene check.
  - option: Fix only aibox merge behavior
    reason: Necessary for derived-project prompting, but would leave processkit's
      own standard and diagnostics inconsistent.
  consequences: Derived projects should migrate future role actor references to ACTOR-product-manager.
    Existing ACTOR-pm-claude data will require local reconciliation if present. aibox
    still needs to consume the updated preauth metadata and prune stale generated
    skills/commands during sync.
  decided_at: '2026-04-29T10:45:32+00:00'
---
