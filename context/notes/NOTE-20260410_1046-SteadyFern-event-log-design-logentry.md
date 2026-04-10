---
apiVersion: processkit.projectious.work/v1
kind: Note
metadata:
  id: NOTE-20260410_1046-SteadyFern-event-log-design-logentry
  created: 2026-04-10
spec:
  title: "Event log design — LogEntry categories, JSONL sharding, query patterns"
  type: reference
  state: captured
  tags: [foundational, event-log, LogEntry, design, JSONL]
  review_due: 2026-05-10
  promotes_to: null
---

Provenance: Ingested from aibox/move-to-processkit/research/
event-log-design-2026-03.md on 2026-04-10.

# Event Log Design

**Date:** 2026-03-26
**Status:** Draft

---

## 1. Problem Statement

The context system has structured places for deliberate choices
(decisions), planned work (work items), session activity (standups),
and project tracking (scopes). What it lacks is a structured record
of **what happened** -- the chronological facts of project life.

Events like these currently have nowhere to go:

- "Deployed v1.2.3 to production"
- "Customer reported login failure on EU cluster"
- "Migrated database from RDS to Aurora"
- "Upgraded Node.js from 18 to 22 across all services"
- "SSL certificate renewed for api.example.com"
- "Hit 1,000 daily active users"

Some of these get mentioned in standup notes, but standups are
session-scoped and agent-scoped -- they capture what an agent worked
on, not what happened to the project. Some get captured as decisions,
but a deployment is not a decision; it is the consequence of one. The
result is institutional amnesia: three months later, nobody can answer
"when did we deploy v1.2.3?" or "what changed the week before the
outage started?" without digging through git logs and chat history.

An event log fills this gap: a lightweight, append-only, chronological
record of significant project events.

---

## 2. Event Format Design

### 2.1 Fields

| Field | Required | Description |
|-------|----------|-------------|
| **Timestamp** | yes | ISO 8601 date or datetime (`2026-03-26` or `2026-03-26T14:30Z`) |
| **Category** | yes | One of the defined categories (see below) |
| **Summary** | yes | One-line description of what happened |
| **Details** | no | Additional context, links, error messages, metrics |
| **Refs** | no | Related entity IDs |

### 2.2 Categories

| Category | When to use | Example |
|----------|-------------|---------|
| `deploy` | Code or config shipped to an environment | Deployed v1.2.3 to production |
| `release` | Version tagged and published | Released v2.0.0 to GHCR |
| `incident` | Something broke or degraded | API latency spike, p99 > 5s for 20 min |
| `milestone` | Notable achievement or threshold | Reached 1,000 DAU |
| `config` | Infrastructure or environment change | Increased worker pool from 4 to 8 |
| `dependency` | External dependency changed | Upgraded tokio from 1.36 to 1.40 |
| `security` | Security-relevant event | Rotated production API keys |
| `decision` | Pointer to a decision (lightweight cross-ref) | Adopted event log system |

The `decision` category exists solely as a cross-reference marker.
The full rationale belongs in the decision record; the event log
records the fact and timestamp.

### 2.3 File Structure: Single File

**Recommendation: `context/EVENTS.md` (single file).**

Rationale:

- Events are inherently chronological and flat. Unlike research
  reports or session notes, they do not benefit from individual files.
- A single file is greppable (`grep "deploy" context/EVENTS.md`).
- Agents and humans can scan the full timeline in one read.
- The file stays small for a long time -- even 5 events per week
  produces only ~260 entries per year, which is well under 1,000
  lines.
- If a project outgrows a single file (unlikely for most), archival
  by year is straightforward.

A directory (`context/events/`) would be warranted only for projects
generating dozens of events per day (e.g., a platform operations team
logging every deployment across 50 microservices). This is not the
common use case.

### 2.4 Ordering: Newest First

Newest-first (inverse chronological), matching the decisions file
convention. The most recent events are the most relevant during active
work. Agents and humans almost always want to know "what happened
recently?" not "what happened first?"

### 2.5 File Template

```markdown
# Event Log

Chronological record of significant project events. Newest first.
For deliberate choices with rationale, see decisions.

## Format

### YYYY-MM-DD -- category: Summary

Details (optional). Related: WI-xxx, DEC-xxx, PROJ-xxx.

---

<!-- Add events below, newest first -->
```

### 2.6 Example Entries

```markdown
### 2026-03-26 -- release: Published v0.13.2 to GHCR

All 10 image flavors built and pushed. Changelog includes HOME fix
and Dockerfile USER root fix.

### 2026-03-25 -- incident: devcontainer sync failure on Rust addon

Rust addon builder stage wrote cargo to /root/.cargo but runtime
COPY expected /home/user/.cargo. Users hitting build failures with
Rust addon enabled. Workaround documented in session notes.

### 2026-03-25 -- config: Switched addon from npm to native installer

Replaced `npm install -g` with the official curl-based installer.
Eliminates Node.js dependency for installation.

### 2026-03-23 -- decision: Adopted declarative config + minimal base images

Clean break from 10-image architecture to single base image with
composable add-ons and process packages.

### 2026-03-22 -- milestone: Reached 83 curated skills in library

Skills library expanded from 26 to 83 with reference file
scaffolding. 14 categories covering process, development,
infrastructure, data, security, and more.

### 2026-03-20 -- dependency: Upgraded base image to Debian Bookworm slim

Moved from ubuntu:22.04 to debian:bookworm-slim. Reduces base layer
by ~30 MB and aligns with devcontainer ecosystem conventions.

### 2026-03-18 -- security: Enabled cosign verification for published images

All GHCR images now signed with sigstore/cosign. Verification
command documented in installation guide.

### 2026-03-15 -- deploy: Deployed docs-site v2 to GitHub Pages

Docusaurus migration complete. New IA with addon, skill, and
customization sections.
```

---

## 3. Integration Options

### Option A: Pure Skill

A skill file teaches AI agents when and how to append entries to the
events file.

**How it works:**
- Skill lists trigger conditions: "After completing a deployment,
  release, incident resolution, significant config change, or
  milestone, append an event."
- Skill provides the exact format and category list.
- Agent reads the skill, recognizes a trigger, appends the entry.

**Pros:**
- Zero CLI changes. Works immediately with any process package.
- Agents can add rich detail and cross-references contextually.
- No toolchain dependency -- works even outside containers.

**Cons:**
- Agents may forget or skip the event (undertriggering -- a known
  issue per Anthropic research).
- Formatting may drift across sessions and agents.
- Not scriptable -- CI/CD pipelines cannot call a skill.
- No validation of categories or format.

**Effort:** ~1 hour (write the skill file).

### Option B: CLI Command

New subcommand: `processkit event add "summary" --category <cat>
[--details "..."] [--ref WI-xxx]`.

**How it works:**
- CLI parses arguments, validates category, generates timestamp.
- Reads events file, inserts new entry after the header (newest
  first).
- Writes the file back.

**Example usage:**
```bash
# Manual
processkit event add "Deployed v1.2.3 to production" \
    --category deploy

# With details and refs
processkit event add "API latency spike" --category incident \
  --details "p99 > 5s for 20 min, caused by connection pool \
  exhaustion" --ref WI-045

# From CI/CD pipeline
processkit event add "Released ${VERSION}" --category release

# List recent events
processkit event list --last 10
processkit event list --category deploy --since 2026-03-01
```

**Pros:**
- Consistent formatting -- no drift.
- Scriptable: CI/CD, git hooks, and shell aliases can all call it.
- Category validation prevents typos.
- Timestamp is always correct (no agent hallucination of dates).
- Future extensibility: filtering, search, statistics.

**Cons:**
- Requires CLI implementation (~200-400 lines of Rust).
- Only works inside a processkit environment (CLI must be available).
- Still requires agents or humans to remember to call it.

**Effort:** ~4-6 hours (Rust implementation, tests, docs).

### Option C: Hybrid (CLI Command + Skill)

Combine Option B's CLI command with Option A's skill. The skill
teaches agents to call the CLI command rather than editing the file
directly.

**How it works:**
- CLI provides the event-add command with validation and formatting.
- Skill instructs agents: "Use `processkit event add` after
  deployments, incidents, milestones, and config changes. Here are
  the categories and when to use them."
- CI/CD pipelines call the same CLI command directly.

**Skill excerpt:**
```markdown
## When to log events

After completing any of these activities, run the event-add command:

- **deploy**: You deployed code or config to any environment
- **release**: You tagged and published a version
- **incident**: Something broke, degraded, or was reported broken
- **milestone**: A notable threshold was reached
- **config**: Infrastructure or environment configuration changed
- **dependency**: An external dependency was added, removed, or
  upgraded
- **security**: A security-relevant action was taken

## How

processkit event add "summary of what happened" \
    --category <category>

Add --details for context and --ref for cross-references:

processkit event add "Deployed v1.2.3" --category deploy \
    --ref WI-074
```

**Pros:**
- Best of both worlds: agents get guidance, CI/CD gets
  scriptability.
- Skill reduces undertriggering; CLI ensures format consistency.
- Format cannot drift because agents use the CLI, not raw file
  editing.
- Graceful degradation: if the CLI is unavailable, agents can still
  manually append following the skill's format spec.

**Cons:**
- Highest total implementation effort (CLI + skill).
- Two things to maintain.

**Effort:** ~5-7 hours (CLI + skill + docs).

### Option D: Git Hook (Auto-Logging)

Post-commit and post-tag hooks automatically append events.

**How it works:**
- `post-commit`: extracts commit subject, logs as event if it
  matches patterns (e.g., commits starting with `deploy:`, `fix:`,
  `feat:`).
- `post-tag`: logs `release: <tag>` events automatically.
- `post-merge`: logs merge events for significant branches.

**Pros:**
- Fully automatic for git-driven events.
- No human or agent action required.

**Cons:**
- Very noisy. Most commits are not events. Filtering heuristics are
  fragile.
- Cannot capture non-git events (incidents, config changes,
  milestones).
- Hooks are per-repo and not portable across environments.
- Conflates "code was committed" with "something significant
  happened."
- Git tags already serve as release markers; duplicating them adds
  no value.

**Effort:** ~2-3 hours (hook scripts, pattern matching).

### Comparison Matrix

| Criterion | A: Skill | B: CLI | C: Hybrid | D: Hook |
|-----------|----------|--------|-----------|---------|
| Format consistency | Low | High | High | Medium |
| Scriptable (CI/CD) | No | Yes | Yes | N/A |
| Agent-friendly | Medium | Medium | High | N/A |
| Non-git events | Yes | Yes | Yes | No |
| Implementation effort | Minimal | Medium | Medium+ | Low |
| Maintenance burden | Low | Medium | Medium | Low |
| Signal-to-noise | High | High | High | Low |

---

## 4. Relationship to Existing Context Files

### Events vs Decisions

| | Events | Decisions |
|---|--------|-----------|
| **Nature** | Facts: "X happened" | Choices: "We chose X because Y" |
| **Weight** | Lightweight, 1-3 lines | Heavyweight, rationale + alternatives |
| **Trigger** | Something occurred | A choice was made |
| **Example** | "Deployed v1.2.3 to prod" | "Chose PostgreSQL over DynamoDB for..." |
| **Frequency** | Several per week | A few per month |

An event can reference a decision: "Adopted event log system" is an
event that points to the full decision record. The event captures the
**when**; the decision captures the **why**.

### Events vs Standups

| | Events | Standups |
|---|--------|---------|
| **Scope** | Project-scoped | Session-scoped |
| **Author** | Anyone (agents, CI/CD, humans) | The agent or person who worked |
| **Content** | A single thing that happened | Summary of a work session |
| **Audience** | Future timeline reconstruction | Current coordination |
| **Example** | "Database migrated to Aurora" | "Done: worked on DB migration scripts" |

A standup might mention that migration work was done. The event
records that the migration actually happened. The standup is ephemeral
context; the event is permanent record.

### Events vs Work Items

| | Events | Work Items |
|---|--------|--------|
| **Tense** | Past: "what happened" | Future: "what should happen" |
| **Lifecycle** | Append-only, never modified | Items move through statuses |
| **Cross-ref** | Events can cite work item IDs | Work items don't cite events |

When a work item is resolved and deployed, its status changes to
`done` and an event records the completion fact.

### Cross-Referencing Convention

Events reference other context IDs using the `Related:` suffix:

```
Related: WI-074, DEC-016, PROJ-001
```

This creates a lightweight, greppable link without introducing a
formal relational system. To find all events related to a work item:

```bash
grep "WI-074" context/EVENTS.md
```

---

## 5. Process Package Integration

### Which packages should include event logging?

| Package | Purpose | Event logging? |
|---------|---------|----------------|
| core | Agent management | No |
| backlog | Task tracking | No |
| decisions | Architectural decision records | No |
| standups | Session coordination | No |
| projects | Project registry | No |
| release | Release process | **Yes** |
| code-review | Review workflow | No |
| bug-fix | Bug resolution workflow | No |
| feature-dev | Feature development workflow | No |
| operations | Deployment, infra, incidents | **Yes** |
| research | Research documentation | No |
| retrospective | Team retrospectives | No |
| event-log | **Dedicated package** | **Yes** |

**Recommendation: Create a dedicated `event-log` package.**

Rationale:
- Event logging is orthogonal to other packages. A project might want
  event logging without operations (e.g., a library that publishes
  releases but has no infrastructure). A project might want operations
  without event logging (e.g., a team that already uses PagerDuty's
  timeline).
- Keeping it separate follows the composability principle.
- The package contains: `EVENTS.md` template + event-logging skill.

**Convenience preset inclusion:**

| Preset | Includes event-log? |
|--------|---------------------|
| minimal | No |
| managed | No |
| research | No |
| product | Yes |

The `product` preset targets production software projects where
deployment and incident tracking matters. Teams using `managed` can
add `event-log` explicitly if they want it. This avoids adding
process overhead to simpler setups.

---

## 6. Recommendation

### Implement Option C (Hybrid) in two phases.

**Phase 1 -- Immediate (skill-only, ~1 hour):**

1. Create `event-log` process package containing `EVENTS.md`
   template.
2. Create `event-logging` skill that teaches agents when and how to
   manually append events to the events file following the defined
   format.
3. Add `event-log` to the `product` convenience preset.

This delivers value immediately with zero CLI changes. Agents can
start logging events in the next session.

**Phase 2 -- Next release (~4-6 hours):**

1. Implement the `event add` CLI command with category validation,
   timestamp generation, and file insertion.
2. Implement `event list` with optional filters (`--category`,
   `--since`, `--last`).
3. Update the skill to reference the CLI command instead of manual
   editing.
4. Document CI/CD integration patterns in docs-site.

### Concrete file format (final)

**`context/EVENTS.md`:**

```markdown
# Event Log

Chronological record of significant project events. Newest first.
For deliberate choices with rationale, see decisions.

## Categories

deploy, release, incident, milestone, config, dependency, security,
decision

---

<!-- Add events below, newest first -->

### 2026-03-26 -- release: Published v0.13.2 to GHCR

All image flavors built and pushed. Includes HOME fix and Dockerfile
USER root fix.

### 2026-03-25 -- incident: devcontainer build failure on Rust addon

Builder stage wrote cargo to /root/.cargo but runtime COPY expected
/home/user/.cargo.
```

**Entry format (formal spec):**

```
### <ISO-8601-date> -- <category>: <summary>

<optional details paragraph>
<optional "Related: ID, ID, ID." line>
```

Rules:
- Date is mandatory. Time is optional (include for incidents).
- Category must be one of the eight defined values.
- Summary is a single line, sentence case, no trailing period.
- Details are plain prose, 1-3 lines. Keep it brief -- this is a
  log, not a report.
- Related IDs use the `Related:` prefix on a separate line.
- Blank line between entries (the `###` heading provides visual
  separation).
