# Your First Entity

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

Create the first WorkItem through processkit's MCP tools. Do not hand-edit
canonical entity files: the management tool validates the schema, applies the
storage policy, and writes the audit event as one governed operation.

## Prerequisites

- Complete the [v1 alpha tutorial](./v1-alpha-tutorial/).
- Start a new harness session after the installer writes its managed MCP
  projection.
- Confirm the `processkit-gateway` tools are visible.

## Create a WorkItem

Ask your MCP-capable agent:

> Create a medium-priority task WorkItem titled "Evaluate processkit v1
> alpha" with acceptance criteria to verify installation, record one
> decision, and test an update plan.

The agent should route the request and call `create_workitem`. A successful
response includes an ID and canonical path, for example:

```text
BACK-curious-quail
context/workitems/2026/07/BACK-curious-quail.md
```

## Read and transition it

Ask:

> Read BACK-curious-quail through processkit, then transition it from backlog
> to in-progress.

The transition tool checks the WorkItem state machine and records its event.
An invalid transition is rejected rather than silently changing the file.

## Record and query a decision

Ask:

> Record the accepted decision that this project will evaluate
> v1.0.0-alpha.4 in an isolated branch, link it to BACK-curious-quail, and
> query both entities back.

This exercises the core v1 user journey: governed write, relationship, audit
event, and indexed read over visible project files.

## Inspect the result

The files remain readable in Git:

```sh
git status --short
processkit verify --root .
```

`processkit verify` checks installer-managed content. Domain MCP tools and
`pk-doctor` check project entities; a native `processkit doctor` command is
planned but is not part of alpha.4.

## Next

- Review [MCP server operation](../mcp-servers/).
- Learn the [entity model](../primitives/).
- Read the [alpha.4 limitations](../development/v1-version/issue-135-status/).
