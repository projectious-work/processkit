# Command: team-rebalance

Apply a `team-review` recommendation. Targeted re-tiering of one or
more roles without full team recreation. Requires `--confirm` to
prevent accidental writes.

## Syntax

```
team-rebalance
  --roles <list|"all">    # comma-separated role names, or "all"
  --confirm               # required; prevents accidental writes
  --reason <string>       # recorded in the DecisionRecord amendment
  [--landscape <artifact-id>]   # default: latest landscape-summary
  [--weight-overrides <json>]   # override stored weights for this run
```

## Process (sequential)

### Step 1 — Load governing DecisionRecord

```
decision-record.get_decision(<governing-DEC-id>)
```

Read `spec.inputs_snapshot` to retrieve:
- Stored formula weights (used unless `--weight-overrides` supplied)
- `governance_floor`
- `parallelism_cap`
- The landscape artifact ID from the prior run

If `--roles all` is specified, re-run the full `team-create` logic
(steps 1–8 of `team-create`) and write a new DecisionRecord instead
of amending. The remainder of this document covers the non-`all`
path.

### Step 2 — Resolve landscape snapshot

Same resolution logic as `team-create` Step 1. If `--landscape` is
not supplied, use the latest `landscape-summary` artifact. Warn if
older than 90 days; do not block.

### Step 3 — Re-score targeted roles

For each role in `--roles`:

1. Query accessible models scoped to that role's pinned tier:
   ```
   model-recommender.query_models(
     G_floor=<governance_floor>,
     apply_user_filter=true
   )
   ```
2. Apply the tiering formula with stored (or override) weights.
3. Select best-scoring candidate for this role's tier.
4. If the best candidate is the same model as the current assignment:
   report "no change needed" for this role; skip writes.

### Step 4 — End old Bindings

For each role where a model change is needed:

```
binding-management.end_binding(
  id=<current-BIND-id>,
  reason="superseded by team-rebalance: <--reason> (<ISO-timestamp>)"
)
```

### Step 5 — Create or reuse Actor entities

For each role being reassigned:
- If the incoming model ID matches an existing Actor entity in
  `context/actors/` (active or inactive): reactivate it (set
  `active: true` via `actor-profile.update_actor`). Do not create
  a duplicate.
- If no matching Actor exists:
  ```
  actor-profile.create_actor(
    type="ai-agent",
    name=<model-display-name>,
    active=true
  )
  ```

### Step 6 — Create new Bindings

```
binding-management.create_binding(
  type="role-assignment",
  subject=<ACTOR-id>,
  target=<ROLE-id>,
  valid_from=<today>,
  description="<model-id> fills <role-name> — rebalanced <date>"
)
```

### Step 7 — Update roster.md in-place

Rewrite the affected rows in `context/team/roster.md`'s routing table.
Update the "Last rebalanced" timestamp and append the reason to the
history section.

### Step 8 — Amend governing DecisionRecord

Append to the governing DecisionRecord's `progress_notes`:

```
Rebalanced on <ISO-timestamp> by <actor>:
  Roles changed: <list>
  Reason: <--reason>
  New assignments: <role> → <model-id> (score: <score>)
  Weights used: C=<C> K=<K> L=<L> G=<G>
  Landscape: <artifact-id> (<date>)
```

A new DecisionRecord is NOT written unless `--roles all` is used.

## The `--roles all` shortcut

`team-rebalance --roles all --confirm --reason "<reason>"` is
equivalent to running `team-create` with the stored weights and
subscription, except:
- A new DecisionRecord IS written (superseding the current one).
- The deactivation sequence from `team-create` Step 5 applies in full.

Use this when the landscape has shifted so broadly that targeted
rebalancing would touch every role anyway.

## State side-effects

Ends N old Bindings. Creates (or reactivates) N Actors. Creates N new
Bindings. Amends roster.md in-place. Appends to the governing
DecisionRecord's `progress_notes`. Does NOT write a new DecisionRecord
(unless `--roles all`).

## Safety

- `--confirm` is always required. The command prints the plan and
  exits if `--confirm` is absent.
- Dry-run preview is printed before writing, even with `--confirm`:
  show the plan and ask for explicit "proceed" confirmation in
  interactive mode; in non-interactive mode proceed immediately after
  showing the plan.
