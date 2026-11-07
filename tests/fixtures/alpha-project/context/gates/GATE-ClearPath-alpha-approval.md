---
apiVersion: processkit.projectious.work/v2
kind: Gate
metadata:
  id: GATE-ClearPath-alpha-approval
  created: "2026-07-19T00:01:00Z"
spec:
  name: alpha-approval
  description: Confirms that the alpha fixture passes its contract tests.
  kind: automated
  validator: Run the schema-generation contract test suite.
  validator_command: uv run pytest tests/schema_generation -q
  required_roles: []
  blocking: true
  evidence_required: true
---

Approval gate for the v1 alpha foundation.
