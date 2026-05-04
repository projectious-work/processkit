---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_0929-BoldBird-active-interlocutor-uses-capability-negotiated-runtime
  created: '2026-05-04T09:29:21+00:00'
spec:
  title: Active interlocutor uses capability-negotiated runtime binding
  state: accepted
  decision: 'Active TeamMember interlocutors will be bound through capability negotiation:
    prefer harness-native primary-agent support when available, otherwise launch-time
    model/effort conformance, otherwise identity-only fallback. Session start must
    surface the active identity, resolved runtime, observed runtime when detectable,
    and any mismatch. Subagent MCP usage remains unsupported for this implementation
    until gateway lifecycle stability is proven.'
  context: 'The user approved a plan after noting that setting Cora as interlocutor
    does not change the already-running harness model. Current harnesses vary: Claude
    Code supports primary agents and model/effort settings; Codex currently behaves
    primarily as a launch/config-selected parent model with no stable project TeamMember
    primary-agent equivalent. Subagents currently crash or leave MCP servers running,
    so implementation must avoid subagent MCP dependence.'
  rationale: This preserves provider-neutral TeamMember identity and memory while
    recognizing that the harness owns the actual model runtime. Capability negotiation
    lets processkit use stronger integrations when available without making identity
    setup brittle. Explicit mismatch reporting avoids misleading users when identity
    and runtime differ.
  alternatives:
  - option: Make set_active_interlocutor force the current harness model
    reason_rejected: The running parent harness generally owns model selection and
      cannot reliably be hot-swapped from processkit MCP tools.
  - option: Keep identity-only forever
    reason_rejected: Misses available Claude Code and ACP-style integration paths
      and hides model/runtime mismatches.
  - option: Use subagents for all TeamMember execution
    reason_rejected: Current subagent MCP lifecycle is unstable and can crash or leave
      servers running.
  consequences: Processkit will carry explicit binding state and mismatch reporting.
    aibox/harness launchers remain responsible for actually applying model/effort
    before a session starts. Subagent-based team workflows must remain guarded until
    gateway lifecycle tests pass.
  deciders:
  - TEAMMEMBER-cora
  related_workitems:
  - BACK-20260504_0929-HonestSea-active-interlocutor-runtime-binding
  decided_at: '2026-05-04T09:29:21+00:00'
---
