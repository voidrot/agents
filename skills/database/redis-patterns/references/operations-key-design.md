# Redis Key Design and Operations

## Data Structure Cheat Sheet

| Use case | Structure | Example key |
| --- | --- | --- |
| Simple cache | String | `product:123` |
| User session | Hash | `session:abc` |
| Leaderboard | Sorted set | `scores:weekly` |
| Unique visitors | Set | `visitors:2026-07-06` |
| Activity feed | List | `feed:user:456` |
| Durable events | Stream | `events:orders` |
| Counters/rate limits | String + `INCR` | `ratelimit:user:123` |
| Approximate cardinality | HyperLogLog | `hll:pageviews` |

## Naming

```text
resource:id:field        user:123:profile
namespace:resource:id    myapp:session:abc123
time-bound key           stats:pageviews:2026-07-06
```

For Redis Cluster, use hash tags intentionally when multi-key operations must target the same slot, for example `cart:{user123}:items` and `cart:{user123}:total`.

## TTL Guidance

| Data | Typical TTL decision |
| --- | --- |
| Sessions | Match authentication/session policy |
| API response cache | Minutes, with explicit invalidation for writes |
| Rate-limit keys | Match or slightly exceed the window |
| Short-lived tokens | Minutes |
| Leaderboards | Based on recomputation cost and freshness |
| Static reference data | Longer TTL plus explicit versioning/invalidation |

## Eviction Policies

| Policy | Behavior | Fit |
| --- | --- | --- |
| `noeviction` | Writes fail when memory is full | Queues/critical data where loss is worse than errors |
| `allkeys-lru` | Evicts least-recently-used keys | General cache-only instances |
| `volatile-lru` | LRU among keys with TTL | Mixed instances where only expiring keys are disposable |
| `allkeys-lfu` | Evicts least-frequently-used keys | Skewed cache workloads |
| `volatile-ttl` | Evicts keys nearest expiry | TTL-heavy workloads |

Avoid mixing critical queues and disposable caches in one memory policy when possible.

## Connection Management

```python
from redis import ConnectionPool, Redis

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=20,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)
r = Redis(connection_pool=pool)
```

Size pools by process count and Redis connection limits, not only per-service traffic.

## Production Anti-Patterns

| Anti-pattern | Problem | Safer approach |
| --- | --- | --- |
| `KEYS *` | Blocks server on large keyspaces | `SCAN` with cursor |
| No TTL on cache keys | Unbounded memory growth | TTL plus invalidation |
| Huge values | Serialization and network pressure | Store object reference or shard value |
| One Redis for everything | Failure and eviction coupling | Separate instances/DBs by criticality |
| Blind `FLUSHALL` | Global data loss | Scoped deletes and backups |
