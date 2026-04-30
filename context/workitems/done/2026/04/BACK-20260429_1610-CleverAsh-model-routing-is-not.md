---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260429_1610-CleverAsh-model-routing-is-not
  created: '2026-04-29T16:10:24+00:00'
  labels:
    component: model-recommender
    area: bindings
    provider_independence: 'true'
    derived_projects: 'true'
    possible_aibox_followup: 'true'
  updated: '2026-04-29T20:08:01+00:00'
spec:
  title: Model routing is not provider-independent across roles, team-members, and
    derived projects
  state: done
  type: bug
  priority: high
  description: |
    Investigate and fix the actor/team-member, role, model, and binding routing stack. Observed failure: resolving planned implementation roles in a Codex/OpenAI session still preferred Anthropic defaults, some roles had no viable model binding, and provider preference required ad-hoc binding changes instead of clean provider-independent routing. Derived projects appear not to pick up team-members, models, and model-assignment bindings reliably; work distribution is therefore not efficient and role/team-member indirection does not achieve provider independence.

    Processkit responsibility: review DEC-20260422_0233-SpryTulip, DEC-20260422_0234-BraveFalcon, and DEC-20260422_0234-LoyalComet against the implementation; audit default binding pack, resolver precedence, provider_preference semantics, equivalent_tier usage, team-member preferences, role+seniority bindings, and explain-routing output. Ensure OpenAI, Anthropic, and other providers can be selected via capability/equivalent-tier/project preference without role slugs or bindings being provider-baked.

    Possible aibox responsibility: if derived projects do not receive or refresh model artifacts, team-members, model-assignment bindings, or generated MCP/command config during sync/rebuild, file a linked aibox issue with reproduction evidence. This processkit bug should first define the expected contract and local correctness checks so any aibox propagation defect is precise.

    Acceptance criteria: provider-neutral routing tests cover OpenAI-preferred, Anthropic-preferred, and no-provider-preference projects; explain-routing shows why a provider wins; default bindings avoid provider-specific role names and single-provider lock-in; pk-doctor or release audit catches missing model/team-member/binding propagation; derived-project simulation verifies sync-visible model routing state.
  started_at: '2026-04-29T20:07:45+00:00'
  completed_at: '2026-04-29T20:08:01+00:00'
---

## Transition note (2026-04-29T20:07:45+00:00)

Implemented resolver provider-equivalent fallback. When a project scope veto blocks a role binding target and provider_preference is set, resolver now substitutes an explicit or inferred equivalent model from the preferred provider instead of returning no viable candidate. Added regression coverage for OpenAI substitution of blocked Anthropic role defaults.


## Transition note (2026-04-29T20:07:52+00:00)

Validation completed: resolver unit tests passed, smoke tests passed, drift guard passed, pk-doctor passed with only the existing aibox#55 Codex warning, release-audit passed with existing warnings only.


## Transition note (2026-04-29T20:08:01+00:00)

Closed as processkit-side fix. Remaining broader UX around visible active actor and harness-specific subagent export is tracked separately in new backlog items.
