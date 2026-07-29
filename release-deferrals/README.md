# Release deferrals

Phase-zero doctor warnings and actionable informational findings must be
resolved or explicitly deferred in a tracked file:

```text
release-deferrals/vX.Y.Z.md
```

Each entry must include the finding, rationale, owner, tracking issue, and
expiry or target release. A deferral does not override an error; errors always
block release publication.
