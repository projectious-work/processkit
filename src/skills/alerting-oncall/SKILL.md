---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-alerting-oncall
  name: alerting-oncall
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Alert design and on-call practices — severity, runbooks, SLO burn-rate alerting, escalation."
  category: observability
  layer: null
  when_to_use: "Use when designing alerts, writing runbooks, reducing alert fatigue, setting up escalation policies, implementing SLO-based alerting, or improving on-call processes."
---

# Alerting & On-Call

## Level 1 — Intro

Good alerting wakes humans only when humans need to act. Severity tiers,
SLO burn-rate alerting, and runbooks turn noisy thresholds into a calm
on-call rotation. Alert fatigue is the number one quality problem — fix
it by tracking page volume and deleting low-value alerts.

## Level 2 — Overview

### Severity levels

Define clear tiers so responders know how urgently to act:

| Severity | Response Time | Action          | Example                                      |
|----------|---------------|-----------------|----------------------------------------------|
| **P1 / Critical** | Immediate (< 5 min) | Page on-call, wake people up | Total service outage, data loss, security breach |
| **P2 / High**     | Within 30 min        | Page during business hours   | Degraded service, error rate > SLO, partial outage |
| **P3 / Medium**   | Within 4 hours       | Ticket, fix today            | Elevated latency, disk 80% full, cert expiring in 7 days |
| **P4 / Low**      | Within 1 business day| Ticket, fix this sprint      | Deprecated API usage, non-critical background job failures |

Only P1 and P2 should page. P3 and P4 must create tickets and never
page. Every alert has exactly one severity; if you cannot decide, it is
P3.

### Page vs ticket

The single most important decision in alert design is whether the alert
pages a human or files a ticket. Page when users are currently
impacted, data is at risk, or the situation will get worse without
intervention. Ticket when the issue can wait hours or days, recovery is
likely automatic, or it is a warning about future risk. If the
responder's only action is "acknowledge and wait", it should be a
ticket. If you page more than twice a week for non-incidents, your
alerts need tuning.

### SLO-based (burn-rate) alerting

Threshold alerts like "error rate > 1%" are noisy. SLO alerting fires
only when you are consuming your error budget too fast.

1. Define the SLO (e.g. 99.9% availability over 30 days = 43 min budget)
2. Compute `burn_rate = actual_error_rate / (1 - SLO_target)`
3. Use multi-window alerts to suppress false positives:
   - **Page (P1)**: burn rate > 14.4 over both last 5 min AND last 1 hr
   - **Page (P2)**: burn rate > 6 over both last 30 min AND last 6 hr
   - **Ticket (P3)**: burn rate > 3 over both last 2 hr AND last 24 hr

This alerts early on severe burns and late on slow burns, matching
human response capabilities.

### Runbook minimum

Every alert that pages must have a runbook with: what the alert means
in one sentence, likely causes ranked by frequency, diagnosis steps
with dashboard and command links, mitigation (quick fix plus
escalation path), and the team and channel that owns it.

### Alert fatigue prevention

Track pages per week per person; target less than two pages per
on-call shift. Review every alert weekly — if it fired and no action
was taken, delete or downgrade it. Merge per-instance alerts into
per-service grouped alerts. Set thresholds from percentile baselines,
not guesses. Auto-resolve transient spikes within 5 minutes. Silence
known alerts proactively during deploys and planned maintenance.

## Level 3 — Full reference

### Runbook template

```
# Alert: <alert_name>
## What it means
One sentence explaining the condition and its user impact.

## Likely causes
- Cause 1 (most common)
- Cause 2
- Cause 3

## Diagnosis steps
1. Check <dashboard_link> for the current state
2. Run <command> to verify the symptom
3. Check recent deploys: <deploy_log_link>

## Mitigation
- Quick fix: <rollback command or toggle>
- If that doesn't work: <escalation path>

## Escalation
- Team: <team_name> (#slack-channel)
- Secondary: <person or team>
```

### Escalation policy

1. **Primary on-call** responds within the target time for severity
2. **Auto-escalate** to secondary if not acknowledged within 10 min
   (P1) or 30 min (P2)
3. **Escalate to engineering lead** if not resolved within 1 hour (P1)
   or 4 hours (P2)
4. **Declare an incident** if multiple P1 alerts fire simultaneously
   or the issue affects multiple services

### On-call handoff

Hand off at a consistent time (e.g. Monday 10:00 local). The outgoing
on-call writes a summary covering active incidents, flaky alerts,
known issues, and anything to watch. The incoming on-call reviews and
acknowledges. Shadow rotations pair new team members with experienced
on-call for 1-2 cycles before they take primary.

### Incident communication

During a P1/P2 incident: open an incident channel immediately, post an
initial summary (what is broken, who is affected, current severity),
update every 15-30 minutes even if the update is "still investigating",
post to a public status page if external users are affected, and after
resolution publish a timeline, root cause, and follow-up actions
within 48 hours.

### Anti-patterns

- Alerting on causes instead of symptoms (CPU > 80% rather than
  latency or error rate)
- Static thresholds that ignore traffic patterns or seasonality
- Alerts without runbooks — the responder has to invent the response
  while paged
- "Informational" pages — if no action is taken, the alert should not
  page
- Per-instance alerts in a fleet of N — group them
- Letting noisy alerts persist because "we'll fix it later"
