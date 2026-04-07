---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-api-design
  name: api-design
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "REST API design — resource naming, HTTP methods, status codes, pagination, versioning, OpenAPI."
  category: api
  layer: null
  when_to_use: "Use when designing a new REST API, reviewing API contracts, writing OpenAPI/Swagger documentation, or choosing pagination, versioning, or error-format strategies."
---

# API Design

## Level 1 — Intro

REST APIs follow well-established conventions: plural-noun resources,
HTTP methods that match their semantics, correct status codes, cursor
pagination, URI versioning, and a consistent error envelope. Document
the contract in OpenAPI 3.1 with reusable components.

## Level 2 — Overview

### Resource naming

Use plural nouns for collections (`/users`, `/orders`). Nest
sub-resources to express ownership (`/users/{id}/orders`) but cap
nesting at three levels — go flat once the relationship is clear.
Avoid verbs in URIs; the HTTP method is the verb. Use kebab-case for
multi-word segments (`/line-items`), lowercase only, no trailing
slash, no file extensions.

When CRUD doesn't fit, model the action as a sub-resource POST:
`POST /v1/orders/{id}/cancel`, `POST /v1/users/{id}/verify-email`.

### HTTP methods and status codes

Map operations to methods consistently and return the right success
code:

| Operation | Method | Success | Notes                  |
|-----------|--------|---------|------------------------|
| List      | GET    | 200     | Collection endpoint    |
| Read      | GET    | 200     | Single resource        |
| Create    | POST   | 201     | Return Location header |
| Replace   | PUT    | 200     | Full replacement       |
| Patch     | PATCH  | 200     | Partial update         |
| Delete    | DELETE | 204     | No body                |

GET is safe and idempotent. PUT and DELETE are idempotent. Never
return 200 with an error payload — use the right 4xx/5xx code.

### Pagination

Default to **cursor-based** pagination. It is correct under concurrent
writes, scales to large datasets, and is what every serious API uses.
Reserve offset-based pagination for small, stable datasets where users
need to jump to page N.

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "abc123",
    "has_more": true
  }
}
```

Cursors are opaque (base64-encoded). Clients must not parse them.

### Filtering, sorting, versioning

- Filter via query params: `GET /orders?status=shipped&created_after=2025-01-01`.
- Sort with `sort=`, prefix with `-` for descending: `?sort=-created_at,name`.
- Version in the URI path for public APIs (`/v1/users`). Use the
  `Accept` header for internal APIs that need URL stability.
- Within a version, only additive changes — never break clients.

### Error responses

Use one error envelope across every endpoint:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required.",
    "details": [
      { "field": "email", "reason": "required" }
    ],
    "request_id": "req_abc123"
  }
}
```

`code` is machine-readable; `message` is human-readable; `details`
holds per-field errors; `request_id` makes support tickets debuggable.

### Rate limiting

Return rate-limit headers on every response, not just 429s:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1672531200
```

Return 429 Too Many Requests when the limit is exceeded.

### OpenAPI 3.1

Document the API in OpenAPI 3.1. Extract shared schemas, parameters,
and responses into `components/` and `$ref` them everywhere. Define
security schemes globally with per-endpoint overrides for public
routes. See `references/openapi-patterns.md` for the full skeleton
including reusable parameters, responses, and security schemes.

## Level 3 — Full reference

### Status code reference

| Code | Name                  | When to use                              |
|------|-----------------------|------------------------------------------|
| 200  | OK                    | GET / PUT / PATCH with response body     |
| 201  | Created               | POST that creates a resource (+Location) |
| 202  | Accepted              | Async operation started                  |
| 204  | No Content            | DELETE success or empty PUT/PATCH        |
| 400  | Bad Request           | Malformed syntax, invalid JSON           |
| 401  | Unauthorized          | Missing/invalid auth                     |
| 403  | Forbidden             | Authenticated but lacks permission       |
| 404  | Not Found             | Resource does not exist                  |
| 405  | Method Not Allowed    | Method not supported for this endpoint   |
| 409  | Conflict              | Duplicate or version conflict            |
| 422  | Unprocessable Entity  | Valid syntax, semantic validation failed |
| 429  | Too Many Requests     | Rate limit exceeded                      |
| 500  | Internal Server Error | Unhandled exception                      |
| 502  | Bad Gateway           | Upstream returned bad response           |
| 503  | Service Unavailable   | Overloaded or in maintenance             |
| 504  | Gateway Timeout       | Upstream timed out                       |

The full method-semantics table (idempotency, safety, body usage) is
in `references/rest-conventions.md`.

### Standard error codes

Pair the HTTP status with a stable string code so clients can match
without parsing prose:

| Code                  | HTTP        | Description                |
|-----------------------|-------------|----------------------------|
| VALIDATION_ERROR      | 400 / 422   | Field validation failed    |
| AUTHENTICATION_ERROR  | 401         | Invalid or missing creds   |
| AUTHORIZATION_ERROR   | 403         | Insufficient permissions   |
| NOT_FOUND             | 404         | Resource does not exist    |
| CONFLICT              | 409         | Resource state conflict    |
| RATE_LIMITED          | 429         | Too many requests          |
| INTERNAL_ERROR        | 500         | Unexpected server error    |

### Cursor vs offset pagination

Cursor pagination is preferred because it survives concurrent writes:
inserting a row at the start of an offset-paginated list shifts every
subsequent page and causes drift (duplicates and skips). The cursor
encodes the position in the index, so new rows do not affect pages
already fetched. Use offset only when the dataset is small, stable,
and users genuinely need to jump to "page 47."

### HATEOAS (when to bother)

For genuinely discoverable APIs, embed action links in responses:

```json
{
  "id": "order-123",
  "status": "shipped",
  "_links": {
    "self":   { "href": "/v1/orders/order-123" },
    "cancel": { "href": "/v1/orders/order-123/cancel", "method": "POST" }
  }
}
```

In practice, most internal and partner APIs skip HATEOAS because
clients are written against an OpenAPI spec, not a discoverable graph.
Add it when the API is genuinely browsable (public, long-lived, many
unknown clients) or you're following a strict HAL/JSON:API standard.

### OpenAPI component patterns

Define `components/schemas` for every entity, plus `UserCreate`-style
input variants that omit `readOnly` fields. Define
`components/parameters` for shared query/path params (cursor, limit,
path id) and `components/responses` for shared error responses
(`Unauthorized`, `ValidationError`, `NotFound`). List endpoints use
`allOf` to compose `PaginatedResponse` with the entity type. See
`references/openapi-patterns.md` for full YAML examples and security
scheme definitions (Bearer JWT, API key, OAuth2).

### Review checklist

When reviewing an API design, verify:

1. Plural-noun resources, no verbs in paths.
2. HTTP methods match semantics (GET safe, PUT idempotent).
3. Status codes are correct (201 + Location on create, 204 on delete).
4. Errors use the standard envelope with machine-readable codes.
5. Every list endpoint paginates (cursor preferred).
6. Versioning strategy is explicit and consistent.
7. Rate-limit headers on every response.
8. OpenAPI 3.1 spec compiles, schemas are `$ref`-ed, no copy-paste.

### Anti-patterns to avoid

- Verbs in URIs (`/getUsers`, `/createOrder`).
- Singular collections (`/user` instead of `/users`).
- Deep nesting beyond three levels.
- 200 responses carrying error payloads.
- Inconsistent error formats between endpoints.
- Unpaginated list endpoints ("we'll add pagination later").
- Breaking changes inside a stable version — bump the version.
- Inline-duplicated schemas in OpenAPI instead of `$ref`.
