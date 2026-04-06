# primitives/schemas/

One YAML file per primitive kind. Each schema is itself a processkit entity
(`kind: Schema`) and validates the `spec` field of entities of the target kind.

Schema files use **JSON Schema (draft 2020-12) expressed in YAML** for the
`spec_schema` field. This is the format consumed by the `index-management`
MCP server (Phase 3).

## Shape

```yaml
apiVersion: processkit.projectious.work/v1
kind: Schema
metadata:
  id: SCHEMA-<kind>
  target_kind: <Kind>            # which primitive kind this schema validates
  version: "1.0.0"
spec:
  description: "One-line summary of the primitive."
  id_prefix: <PREFIX>             # the ID prefix entities of this kind use
  state_machine: <name>           # optional — references state-machines/<name>.yaml
  spec_schema:                    # JSON Schema for the entity's spec field
    type: object
    required: [...]
    properties:
      ...
```

## Phase 1 schemas (v0.1.0)

- `workitem.yaml` — WorkItem (BACK prefix, workitem state machine)
- `logentry.yaml` — LogEntry (LOG prefix, immutable)
- `decisionrecord.yaml` — DecisionRecord (DEC prefix, decision state machine)

Phase 2 adds the remaining 15 primitive schemas.
