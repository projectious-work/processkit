---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-error-handling
  name: error-handling
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Error handling across languages — Result types, exceptions, retries, circuit breakers, and structured error responses."
  category: meta
  layer: null
  when_to_use: "Use when designing error handling for a module or service, choosing between Result types and exceptions, building error hierarchies, implementing retries or circuit breakers, or reviewing code for missing or poor error handling."
---

# Error Handling

## Level 1 — Intro

Errors are part of the type system, not an afterthought. Make
failure paths explicit, separate user-facing messages from internal
diagnostics, and reach for retries and circuit breakers only when
the failure is genuinely transient.

## Level 2 — Overview

### Result types vs exceptions

Use algebraic types where the language supports them — they make
error paths explicit in the signature.

- **Rust:** `Result<T, E>` for recoverable errors, `Option<T>` for
  missing values. Propagate with `?`. Define domain error enums
  with `thiserror`.
- **TypeScript:** discriminated unions or a `Result<T, E>` library.
  Avoid `throw` for expected failures (validation, not-found).
  Reserve exceptions for truly unexpected conditions.
- **Python:** exceptions are idiomatic, but consider returning
  `None` or a result tuple in tight loops where try/except overhead
  matters.
- **Java:** checked exceptions for recoverable conditions the
  caller must handle, unchecked (`RuntimeException`) for
  programming errors. Prefer specific types over `Exception`.

### Error hierarchies

Design errors in layers:

1. **Domain errors** — business rule violations
   (`InsufficientFunds`, `ItemOutOfStock`).
2. **Application errors** — workflow failures (`OrderNotFound`,
   `Unauthorized`).
3. **Infrastructure errors** — external system failures
   (`DatabaseUnavailable`, `TimeoutError`).

Each layer exposes only errors meaningful at that level.
Infrastructure errors are mapped to application errors before
reaching the domain.

### User-facing vs internal

Never leak stack traces, SQL, or file paths to end users.

- **Internal errors:** full context for debugging — stack trace,
  request ID, input values.
- **User-facing errors:** human-readable message, error code,
  optional field-level details.
- Map at the boundary (HTTP handler, CLI output). Log the internal
  error with a correlation ID; return the ID to the user for
  support.

### Error codes and structured responses

Use namespaced, stable error codes (`PAYMENT.DECLINED`,
`AUTH.TOKEN_EXPIRED`, `VALIDATION.FIELD_REQUIRED`). Document them
in a central registry. Never reuse or rename codes once shipped.

For APIs, return a consistent error shape:

```json
{
  "error": {
    "code": "VALIDATION.FIELD_REQUIRED",
    "message": "The 'email' field is required.",
    "details": [
      { "field": "email", "reason": "required" }
    ],
    "request_id": "req-abc123"
  }
}
```

### Retries and circuit breakers

Retry only transient failures (network timeouts, 503s, lock
contention). Use exponential backoff with jitter: base delay
100–500ms, multiply by 2 each attempt, add random jitter (0–100% of
delay) to prevent thundering herd. Cap retries (3–5) and total
timeout. **Never retry** 4xx client errors (except 429), validation
failures, or auth errors.

Circuit breakers prevent cascading failures when a downstream
service is unhealthy:

- **Closed** (normal): requests flow through; track failure rate.
- **Open** (tripped): requests fail immediately; return a fallback.
- **Half-open** (probing): allow one request after a timeout. On
  success, close. On failure, reopen.

Configure failure threshold (e.g. 5 failures in 30s), open duration
(e.g. 60s), and half-open probe count.

## Level 3 — Full reference

### Error reporting

- Log with structured fields: `level`, `error_code`, `message`,
  `stack`, `request_id`, `user_id`.
- Send unhandled exceptions to an error tracker (Sentry, Datadog,
  Honeybadger).
- Alert on error rate spikes, not individual errors.
- Group errors by root cause, not by message string.

### Domain error enum (Rust)

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PaymentError {
    #[error("insufficient funds: required {required}, available {available}")]
    InsufficientFunds { required: u64, available: u64 },

    #[error("card declined: {reason}")]
    CardDeclined { reason: String },

    #[error("payment provider unavailable")]
    ProviderUnavailable(#[source] reqwest::Error),
}

pub fn charge(amount: u64, balance: u64) -> Result<Receipt, PaymentError> {
    if amount > balance {
        return Err(PaymentError::InsufficientFunds {
            required: amount,
            available: balance,
        });
    }
    Ok(Receipt { amount })
}
```

### Retry with backoff (Python)

```python
import time
import random
import httpx

def fetch_with_retry(url: str, max_retries: int = 4) -> httpx.Response:
    base_delay = 0.3
    for attempt in range(max_retries + 1):
        try:
            resp = httpx.get(url, timeout=5.0)
            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", base_delay))
                time.sleep(retry_after + random.uniform(0, 0.5))
                continue
            resp.raise_for_status()
            return resp
        except httpx.TransportError:
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, base_delay)
            time.sleep(delay)
    raise httpx.HTTPError(f"Failed after {max_retries} retries")
```

### Structured API error response (TypeScript)

```typescript
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500,
    public details?: { field: string; reason: string }[],
  ) {
    super(message);
  }
}

// In route handler
app.post("/orders", async (req, res) => {
  try {
    const order = await createOrder(req.body);
    res.status(201).json(order);
  } catch (err) {
    if (err instanceof AppError) {
      res.status(err.statusCode).json({
        error: {
          code: err.code,
          message: err.message,
          details: err.details,
          request_id: req.id,
        },
      });
    } else {
      console.error("Unhandled error", { request_id: req.id, err });
      res.status(500).json({
        error: {
          code: "INTERNAL.UNEXPECTED",
          message: "An unexpected error occurred.",
          request_id: req.id,
        },
      });
    }
  }
});
```

### Anti-patterns

- Catching `Exception` (or bare `except:`) and swallowing it
- Returning sentinel values (`-1`, empty string) instead of an
  explicit error
- Leaking SQL, stack traces, or filesystem paths in HTTP responses
- Retrying non-idempotent operations without a deduplication key
- Retrying 4xx errors as if they were transient
- Renaming or reusing error codes after shipping them
- Alerting on every individual error instead of rate spikes
