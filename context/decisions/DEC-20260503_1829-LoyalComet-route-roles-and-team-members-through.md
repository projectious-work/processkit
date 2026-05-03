---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260503_1829-LoyalComet-route-roles-and-team-members-through
  created: '2026-05-03T18:29:09+00:00'
spec:
  title: Route roles and team members through provider-neutral model profiles
  state: accepted
  decision: Role and TeamMember model assignments will bind to provider-neutral Artifact(kind=model-profile)
    artifacts by default. Concrete Artifact(kind=model-spec) artifacts remain provider/model-specific
    and may keep provider/model names in filenames. The resolver will expand profiles
    to concrete model-spec candidates after applying runtime/provider access gates.
    Direct Role/TeamMember to ModelSpec bindings are compatibility or explicit-pin
    cases only and should be flagged by pk-doctor unless marked accordingly.
  context: The v0.25.2 model-spec release moved concrete model descriptions into Artifact(kind=model-spec),
    but existing role and TeamMember bindings still target exact provider models.
    Cora and many role defaults therefore fail conceptually when the active harness/provider
    changes. The approved v0.25.3 plan adds a provider-neutral indirection layer without
    renaming concrete model-spec artifacts.
  rationale: Persistent identities and role definitions must survive switching harnesses
    between Codex, Claude Code, Gemini CLI, Aider, Continue, Cursor, Copilot, OpenCode,
    Hermes, and other provider surfaces. Binding identities directly to OpenAI, Anthropic,
    or other concrete models makes derived projects brittle when aibox.toml or runtime
    access changes. ModelSpec artifacts describe concrete provider models, while ModelProfile
    artifacts describe capability needs.
  alternatives:
  - option: Keep direct ModelSpec role bindings
    status: rejected
    reason: This preserves provider lock-in for identities and roles.
  - option: Rename concrete ModelSpec artifacts to opaque IDs
    status: rejected
    reason: The user clarified that concrete provider/model artifacts may and should
      encode provider/model in filenames.
  - option: Use hard-coded provider equivalence maps only
    status: rejected
    reason: Hard-coded equivalence is a tactical fallback, not a scalable routing
      contract.
  consequences: Schemas, default bindings, resolver logic, docs, pk-doctor checks,
    src/context mirrors, and tests must be updated. aibox remains responsible for
    exposing active harness/provider access and entitlement signals; processkit consumes
    those signals and falls back conservatively when unavailable.
  decided_at: '2026-05-03T18:29:09+00:00'
---
