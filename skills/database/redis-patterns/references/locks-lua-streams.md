# Redis Lua, Locks, Pub/Sub, and Streams

## Sliding Window Rate Limit With Lua

Lua keeps the multi-command sorted-set update atomic on a single Redis instance.

```lua
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)

if count < limit then
  local seq_key = key .. ':seq'
  local seq = redis.call('INCR', seq_key)
  redis.call('EXPIRE', seq_key, math.ceil(window / 1000))
  redis.call('ZADD', key, now, now .. '-' .. seq)
  redis.call('EXPIRE', key, math.ceil(window / 1000))
  return 1
end

return 0
```

```python
sliding_window = r.register_script(open('sliding_window.lua').read())

def allow_request(user_id: int) -> bool:
    now = int(time.time() * 1000)
    return bool(sliding_window(keys=[f"ratelimit:sliding:{user_id}"], args=[now, 60000, 100]))
```

## Single-Instance Lock

Use a unique token and release only when the token still matches.

```python
def acquire_lock(resource: str, ttl_ms: int = 5000) -> str | None:
    token = str(uuid.uuid4())
    ok = r.set(f"lock:{resource}", token, px=ttl_ms, nx=True)
    return token if ok else None

def release_lock(resource: str, token: str) -> bool:
    script = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
      return redis.call('del', KEYS[1])
    end
    return 0
    """
    return bool(r.eval(script, 1, f"lock:{resource}", token))
```

For multi-node locking, use a maintained library and validate the algorithm's failure model against your consistency requirements.

## Pub/Sub

Pub/Sub is fire-and-forget broadcast. Subscribers only receive messages while connected.

```python
def publish_event(channel: str, payload: dict):
    r.publish(channel, json.dumps(payload))

def subscribe_events(channel: str):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle(json.loads(message['data']))
```

## Redis Streams

Use Streams for durable event queues, replay, and consumer groups.

```python
def emit(stream: str, event: dict):
    r.xadd(stream, event, maxlen=10000, approximate=True)

try:
    r.xgroup_create('events:orders', 'processor', id='0', mkstream=True)
except Exception:
    pass

def consume(stream: str, group: str, consumer: str):
    messages = r.xreadgroup(group, consumer, {stream: '>'}, count=10, block=2000)
    for _, entries in (messages or []):
        for msg_id, data in entries:
            process(data)
            r.xack(stream, group, msg_id)
```

Handle pending entries and retries; acknowledging only after successful processing gives at-least-once behavior, not exactly-once behavior.
