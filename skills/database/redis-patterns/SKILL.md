---
name: redis-patterns
description: Use for Redis cache, session, rate-limit, lock, Pub/Sub, Streams, TTL, eviction, and key-design decisions.
origin: ECC
---

# Redis Patterns

Activation and routing layer for Redis-backed application state.

## When to Activate

- Adding or reviewing caching, session storage, counters, or rate limiting
- Designing keys, TTLs, eviction behavior, or memory isolation
- Implementing distributed locks or atomic multi-step operations
- Choosing Pub/Sub vs Redis Streams
- Configuring connection pools, Sentinel, Cluster, persistence, or production operations

## Decision Workflow

1. **Classify the state**: cache, coordination, queue/stream, session, counter, or durable source of truth.
2. **Pick the data structure**: string/hash/set/sorted set/list/stream/HyperLogLog based on access pattern.
3. **Define lifecycle**: TTL, invalidation, maxmemory policy, persistence needs, and ownership.
4. **Make atomicity explicit**: single command, pipeline/transaction, Lua script, or external lock.
5. **Verify operational fit**: memory bounds, connection pool sizing, failure mode, and observability.

## Safety Rules

- Do not use `KEYS *` in production; use cursor-based `SCAN` patterns.
- Always decide whether keys need TTLs; unbounded key growth is a production risk.
- Use `SET key token NX PX ttl` plus token-checked release for single-instance locks.
- Prefer Streams over Pub/Sub when messages need replay, consumer groups, or at-least-once processing.
- Treat Redis Cluster multi-key operations carefully; keys must hash to compatible slots.

## Reference Routing

- Cache-aside, invalidation, sessions, rate limits, and stampede prevention: [references/cache-rate-limit-recipes.md](references/cache-rate-limit-recipes.md)
- Lua scripts, locks, Pub/Sub, and Streams examples: [references/locks-lua-streams.md](references/locks-lua-streams.md)
- Key naming, TTLs, eviction, connection management, and operations: [references/operations-key-design.md](references/operations-key-design.md)

## Expected Output

- Recommended Redis data structure and key shape
- TTL/invalidation and memory policy notes
- Atomicity/failure-mode plan
- Minimal code or command recipe from the relevant reference
