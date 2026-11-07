---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260515_1232-GentleLantern-keep-processkit-host-orchestrator-neutral
  created: '2026-05-15T12:32:11+00:00'
spec:
  title: Keep processkit host-orchestrator neutral
  state: accepted
  decision: processkit skills, commands, MCP tools, and doctor findings must not invoke
    or require aibox host commands from inside derived project containers. aibox and
    other host installers may consume and reference processkit, but processkit remediation
    surfaces stay generic and host-orchestrator neutral.
  context: The owner established a one-directionality principle while separating pk-doctor
    from host-side aibox diagnostics. pk-doctor is the in-container processkit health
    surface; host installer diagnostics and repair commands belong to the owner outside
    the container.
  rationale: This keeps processkit provider-neutral and usable outside aibox-managed
    projects while still allowing derived projects to report external host-action
    evidence when a host installer must repair generated config, runtime state, or
    container orchestration.
  consequences: Active processkit skill/MCP/command surfaces should phrase host repair
    as generic owner-operated host installer/runtime-manager actions. processkit MCP
    tools should not execute aibox host commands. pk-doctor now includes a doctor_boundary
    guard to catch forbidden host-command remediation bindings.
  decided_at: '2026-05-15T12:32:11+00:00'
---
