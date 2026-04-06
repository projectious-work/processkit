# primitives/state-machines/

Default state machine definitions for primitives that have lifecycle states
(WorkItem, DecisionRecord, Scope, Discussion). Each is a YAML file describing
states, allowed transitions, and optional transition guards.

Projects may override these defaults by providing their own state machines
with the same name in their `context/state-machines/` directory.

## Shape

```yaml
apiVersion: processkit.projectious.work/v1
kind: StateMachine
metadata:
  id: SM-<name>
  name: <name>
spec:
  initial: <state>
  terminal: [<state>, ...]
  states:
    <state>:
      description: "What this state means."
      transitions:
        - to: <other-state>
          guard: "optional condition for the transition"
```

## Phase 1 state machines

- `workitem.yaml` — WorkItem: backlog → in-progress → review → done (+ blocked, cancelled)
- `decisionrecord.yaml` — DecisionRecord: proposed → accepted → (superseded)
