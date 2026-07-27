# v0 to v1 compatibility inspection

The v1 installer identifies legacy processkit evidence without consulting
aibox, harness, devcontainer, or MCP configuration files.

```sh
processkit inspect-compatibility \
  --root /path/to/legacy-tree \
  --distribution /path/to/processkit-v1-release \
  --json
```

An `exact-release` result requires every immutable anchor in a shipped
compatibility manifest to match. The beta manifests cover v0.27.1 and
v0.28.4 release trees. A partial installed project may be classified only as
`legacy-project-candidate`; its exact version is never guessed.

Beta compatibility is read-only and evidence-only. Detection does not mutate
the inspected tree and does not authorize an in-place install. For an exact
release or candidate:

1. copy the project
2. run the v0-to-v1 corpus migration planner
3. review source hashes, field-loss reports, unsupported kinds, and immutable
   LogEntry evidence
4. validate the migrated copy
5. install v1 into a fresh or disposable target

Automatic in-place migration remains unsupported until historical installed
project fixtures prove mapping, rollback, and user-modification behavior.
This boundary prevents a structural lookalike or a downstream manager's lock
file from being mistaken for processkit provenance.
