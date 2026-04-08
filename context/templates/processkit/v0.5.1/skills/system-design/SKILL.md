---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-system-design
  name: system-design
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "System design methodology — requirements, capacity estimation, component design, trade-offs."
  category: architecture
  layer: null
  when_to_use: "Use when designing a new distributed system, evaluating an existing architecture for scalability or cost, performing back-of-envelope capacity estimation, or preparing for a system design review."
---

# System Design

## Level 1 — Intro

System design starts with requirements, not boxes. Estimate capacity
on the back of an envelope, draw a small high-level architecture,
then deep-dive only the components that are unique or risky. Make
trade-offs explicit — every design decision has a cost.

## Level 2 — Overview

### Gather requirements

Always start with requirements. Split them into functional and
non-functional.

**Functional:** what does the system do? Core use cases (2-4 most
important), user-facing vs internal features, data formats, and key
end-to-end workflows.

**Non-functional:** how well must it do it?

- **Scale** — DAU, peak QPS, data volume
- **Latency** — p50 and p99 targets
- **Availability** — 99.9%, 99.99%, or higher (and the downtime
  budget that implies)
- **Consistency** — strong or eventual, and which parts need which
- **Durability** — RPO/RTO targets, can we lose data
- **Security** — auth, encryption, compliance constraints
- **Cost** — budget, managed vs self-hosted preference

Do not over-specify. Focus on what differentiates this system from a
generic CRUD app.

### Capacity estimation

Numbers and formulas live in `references/estimation-cheatsheet.md`.

Back-of-envelope framework:

1. **Users** — DAU -> peak concurrent -> requests per second
2. **Storage** — data per record * records per day * retention
3. **Bandwidth** — request size * QPS in + response size * QPS out
4. **Compute** — QPS / requests-per-instance = instance count

State assumptions explicitly: read:write ratio (most systems are
10:1 to 100:1), peak-to-average ratio (typically 3x-10x), data
growth rate (linear or exponential), and cache hit rate (often
80-95% for read-heavy workloads).

### High-level design

Draw 5-10 major components. Start with the client and work inward.
For each core use case, trace the data flow with numbered arrows.
Place standard infrastructure where it belongs: load balancer, API
gateway, CDN, cache, database, queue. For each kind of data, choose
a store (relational, document, blob, cache, search index). Keep it
simple first; add complexity only when requirements demand it.

### Component deep dives

For each critical component, detail:

- **API design** — endpoints, request/response formats, pagination
- **Data model** — schema, indexing, partitioning/sharding key
- **Scaling strategy** — horizontal vs vertical, stateless vs
  stateful
- **Failure handling** — what happens when this component dies
- **Caching** — what is cached, where (client, CDN, app, DB), TTL,
  invalidation

Focus deep dives on components that are unique to this system or
most likely to be bottlenecks. Don't deep-dive a stock load
balancer.

### Trade-off analysis

Every decision has trade-offs. State the side you chose and why,
given the requirements:

- **Consistency vs availability** — CAP theorem; in a partition you
  pick C or A
- **Latency vs throughput** — batching raises throughput at the cost
  of latency
- **Simplicity vs scalability** — simpler designs are easier to
  operate but may not scale
- **Cost vs performance** — caching reduces latency but raises
  infrastructure cost
- **Flexibility vs optimization** — denormalization speeds reads but
  complicates writes

### Scalability patterns

- **Horizontal scaling** — stateless services behind a load balancer
- **Database sharding** — partition by user ID, tenant ID, or region
- **Read replicas** — offload reads, accept replication lag
- **Caching layers** — local cache -> distributed cache (Redis) ->
  CDN
- **Async processing** — push non-critical work onto background
  queues
- **Event-driven decoupling** — pub/sub between producers and
  consumers
- **Rate limiting** — token bucket, sliding window
- **Circuit breakers** — prevent cascade failures when downstream is
  unhealthy

### Example workflows

- **URL shortener:** create / redirect / analytics. 100M URLs/month,
  <100ms redirect, 99.99% availability. ~40 writes/s, ~4000 reads/s,
  ~10 TB over 5 years. Stateless API service -> Redis cache (hot
  URLs) -> sharded DB. Base62 encode a unique ID for short codes,
  CDN for redirect caching, async event stream for analytics.
- **Real-time chat:** 1:1 and group messaging, presence, history.
  50M DAU, <200ms delivery, eventual consistency for history. ~500K
  concurrent connections at peak, ~100K messages/s. WebSocket
  gateway sharded by user, message routing service, Cassandra
  (partitioned by chat_id) for storage, Redis for presence, push
  notifications for offline users.
- **Social news feed:** post creation, feed generation, follow
  relationships. 500M DAU, feed loads <500ms, eventual consistency
  acceptable. ~10K posts/s writes, ~500K feed reads/s. Fan-out on
  write for users with <10K followers (precompute feeds in Redis),
  fan-out on read for celebrities (merge at read time). Sharded
  post storage, feed cache in Redis sorted sets, media in object
  storage behind a CDN.

## Level 3 — Full reference

### Powers of 2

| Power | Value | Approx | Common usage |
|-------|-------|--------|--------------|
| 2^10  | 1,024 | 1 Thousand | 1 KB |
| 2^20  | 1,048,576 | 1 Million | 1 MB |
| 2^30  | 1,073,741,824 | 1 Billion | 1 GB |
| 2^40  | ~1.1 Trillion | 1 Trillion | 1 TB |

Useful shortcuts: 1 million seconds ~ 12 days. 1 billion seconds ~
32 years.

### Latency numbers every engineer should know

| Operation | Time |
|-----------|------|
| L1 cache reference | 1 ns |
| L2 cache reference | 4 ns |
| Main memory reference | 100 ns |
| Mutex lock/unlock | 17 ns |
| SSD random read | 16 us |
| Read 1 MB from memory | 3 us |
| Read 1 MB sequentially from SSD | 50 us |
| Read 1 MB sequentially from HDD | 825 us |
| HDD random read | 2 ms |
| Round trip within same datacenter | 500 us |
| Round trip CA to Netherlands | 150 ms |

Key takeaways: memory is ~100x faster than SSD for random access,
SSD ~100x faster than HDD, intra-DC network ~0.5 ms,
cross-continent ~150 ms.

### DAU to QPS conversion

Formula: `QPS = DAU * actions_per_user_per_day / 86400`

| DAU  | Actions/User/Day | QPS (avg) | QPS (peak, 3x) |
|------|------------------|-----------|----------------|
| 1M   | 10               | ~115      | ~350           |
| 10M  | 10               | ~1,150    | ~3,500         |
| 100M | 10               | ~11,500   | ~35,000        |
| 1B   | 10               | ~115,000  | ~350,000       |

Rule of thumb: 1M DAU * 10 actions/day ~ 100 QPS average, 300-500
QPS peak.

### Storage estimation

| Data type | Typical size |
|-----------|--------------|
| User profile (text) | 1-5 KB |
| Tweet / short post | 250 B - 1 KB |
| Chat message | 100-500 B |
| Photo (compressed) | 200 KB - 2 MB |
| Video (1 min, compressed) | 5-50 MB |
| Log entry | 200-500 B |
| DB row (typical) | 500 B - 2 KB |

Formula: `total = records_per_day * avg_size * retention_days`.
Example: 10M messages/day * 500 bytes * 365 days * 5 years ~ 9 TB.

### Bandwidth

Formula: `bandwidth = QPS * avg_size`. Example: 10K QPS * 5 KB
average response = 50 MB/s = 400 Mbps outbound.

### Common capacity patterns

- **1M DAU social app:** ~100 QPS avg, ~500 QPS peak. ~10 GB/day
  new data. ~5 TB over 2 years. 2-5 app servers, 1-2 DB servers,
  Redis cache.
- **100M DAU messaging app:** ~50K QPS avg, ~200K QPS peak. ~500
  GB/day messages. ~500 TB over 3 years. Sharded DB cluster,
  dedicated cache layer, WebSocket gateway fleet.
- **1B DAU read-heavy platform:** ~500K QPS avg, ~2M QPS peak.
  Multi-region CDN mandatory. Read replicas plus 95%+ cache hit
  rate. Terabytes of bandwidth per day.

### Server capacity rules of thumb

| Resource | Typical limit |
|----------|---------------|
| Single web server (simple API) | 1K-10K QPS |
| Single Redis instance | 100K+ ops/s |
| Single PostgreSQL (tuned) | 5K-20K QPS |
| Single Kafka broker | 100K+ messages/s |
| Single machine network | 1-10 Gbps |
| Single machine connections | 10K-100K concurrent |

### Quick estimation framework

1. Start with DAU and read:write ratio.
2. Compute average and peak QPS.
3. Estimate storage per year.
4. Estimate bandwidth (QPS * size).
5. Divide QPS by per-server capacity to get instance count.
6. Add 2-3x headroom for growth and spikes.
7. Consider geographic distribution needs.

### Anti-patterns

- **Drawing boxes before requirements** — leads to designs that
  solve the wrong problem.
- **Skipping estimation** — "we'll scale when we get there" usually
  means the design cannot.
- **Picking strong consistency by default** — most systems can
  tolerate eventual consistency for most operations, and the cost
  of strong consistency is high.
- **Single point of failure hidden in plain sight** — usually the
  database, the load balancer, or a "smart" orchestrator.
- **Caching without invalidation strategy** — stale reads outlive
  the bug that introduced them.
- **Premature sharding** — shard when you have to, not before. The
  operational cost is real.
- **Synchronous chains of more than 2-3 services** — latency
  multiplies and any one failure takes the chain down.
