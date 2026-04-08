---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-webhook-integration
  name: webhook-integration
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Webhook design and consumption — payload format, HMAC signatures, idempotency, retries, dead-letter queues, security."
  category: api
  layer: null
  when_to_use: "Use when implementing a webhook consumer, designing an event-notification system, adding signature verification, or debugging duplicate or failed webhook deliveries."
---

# Webhook Integration

## Level 1 — Intro

Webhooks deliver at least once, in no particular order, over a
network that fails. A correct webhook integration verifies HMAC
signatures on the raw body, deduplicates by event ID, returns 2xx
immediately and processes asynchronously, and retries with
exponential backoff into a dead-letter queue.

## Level 2 — Overview

### Payload envelope

```json
{
  "id": "evt_a1b2c3d4",
  "type": "order.shipped",
  "created_at": "2026-03-22T10:30:00Z",
  "data": { "order_id": "ord_xyz789", "carrier": "ups" }
}
```

- A unique event `id` for idempotency.
- A dotted `type` of the form `resource.action`
  (`order.shipped`, `invoice.payment_failed`).
- ISO 8601 `created_at` for ordering and replay-window enforcement.
- Domain payload nested under `data` so the envelope stays stable as
  the domain model evolves.

### Signature verification (HMAC-SHA256)

Senders compute an HMAC over the **raw request body** using a shared
secret and send it in a header (e.g. `X-Webhook-Signature: sha256=<hex>`).
Consumers recompute and compare in constant time:

```python
expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
if not hmac.compare_digest(expected, received_signature):
    return 401
```

Three things matter:

1. **Sign the raw body**, not parsed JSON. Re-serializing reorders
   keys and breaks the signature.
2. **Constant-time comparison** (`hmac.compare_digest`) — never
   `==` — to avoid timing attacks.
3. **Replay protection.** Include a timestamp in the signed payload
   or as a separate signed header, and reject anything older than
   ~5 minutes.

Support multiple active secrets so you can rotate without downtime.

### Idempotency

Webhook delivery is at-least-once. Consumers must dedupe:

- Store processed event IDs in a database or cache with a unique
  constraint.
- Check before processing — `INSERT ... ON CONFLICT DO NOTHING` is
  the canonical pattern.
- TTL the idempotency store (e.g. 7 days) to bound storage. Senders
  should not retry beyond that window.

### Retry handling

**As a sender:** retry on transient failure with exponential backoff
(1 min, 5 min, 30 min, 2 hr, 8 hr, 24 hr is a typical schedule).
Treat 2xx as success, 5xx and timeouts as transient, and 4xx (except
429) as permanent failure. Include `X-Webhook-Retry-Count` so
consumers can log it.

**As a consumer:** verify the signature, enqueue the event for
asynchronous processing, and return 200/202 immediately. Never do
heavy work in the HTTP handler — the sender will time out and retry,
amplifying load.

### Dead-letter queues

Events that exhaust the retry schedule move to a DLQ with full
context: payload, headers, last error, attempt count. Provide
operator tooling to inspect and replay. Alert when the DLQ grows
unexpectedly. Retain DLQ entries for at least 30 days so you can
recover from outages discovered after the fact.

### Security

- TLS only. Never accept webhooks over plain HTTP.
- Always verify HMAC signatures, even if the source IP is
  allowlisted.
- Restrict by sender IP ranges when the source publishes them
  (Stripe, GitHub, etc.).
- Enforce a payload size limit (1 MB is typical) and rate-limit the
  consumer endpoint.
- Store secrets in a vault (AWS Secrets Manager, Vault, etc.), not
  in code or environment variables checked into source control.

## Level 3 — Full reference

### Ordering

Webhooks do **not** guarantee delivery order. A consumer that assumes
"shipped" must arrive after "created" will eventually be wrong. Two
options:

1. **Use `created_at`** to detect out-of-order events and ignore the
   stale one.
2. **Embed a monotonic version or sequence number** on stateful
   resources, then discard any event whose version is older than
   what's already applied.

Both work; pick the one that fits the resource model.

### Testing webhooks locally

- **Tunnels:** `ngrok` and `cloudflared tunnel` expose a local
  endpoint to a public URL so the sender can reach it.
- **Inspection:** `webhook.site` and `requestbin` capture raw
  requests for offline debugging when the sender doesn't expose a
  test mode.
- **Automated tests** must cover: invalid signature (reject), valid
  signature (accept), duplicate event ID (idempotent — process
  once), out-of-order events, malformed JSON, oversized payload,
  expired timestamp.

### Failure modes worth designing for

| Symptom                            | Likely cause                   |
|------------------------------------|--------------------------------|
| Events processed twice             | No idempotency check           |
| Sender reports timeouts            | Synchronous heavy processing   |
| Signature verification fails       | Parsed body re-serialized      |
| Random 401s after secret rotation  | Old secret no longer accepted  |
| State diverges from sender         | Out-of-order delivery ignored  |
| DLQ grows unexpectedly             | Downstream system degraded     |

The fix for the first two is the same on every platform: dedupe by
event ID with a unique constraint, and move processing to a
background queue so the HTTP handler returns in milliseconds.

### Webhook registration API (when designing your own)

If you're publishing webhooks rather than consuming them, expose a
simple registration API:

- `POST /webhooks` — register a `url`, an `events[]` filter, and
  receive a generated signing secret in the response (shown once).
- `GET /webhooks/{id}/deliveries` — recent delivery attempts with
  status, latency, and response body for debugging.
- `POST /webhooks/{id}/deliveries/{delivery_id}/replay` — manual
  replay for ops recovery.
- Admin dashboard with delivery success rate, latency percentiles,
  and DLQ depth per subscription.

### Anti-patterns to avoid

- **Synchronous processing in the HTTP handler.** Always enqueue and
  return immediately.
- **Verifying the signature against parsed JSON.** Sign and verify
  the raw bytes the sender produced.
- **`==` for signature comparison.** Use a constant-time function.
- **No idempotency store.** "It probably won't happen twice" is
  wrong on the day it matters.
- **Returning 200 from a handler that errored internally.** The
  sender will not retry. Return 500 so retry happens, after the
  signature has been verified.
- **No replay-window check.** A leaked recording can be replayed
  weeks later.
- **Single signing secret with no rotation path.** Plan rotation
  before you need it.
