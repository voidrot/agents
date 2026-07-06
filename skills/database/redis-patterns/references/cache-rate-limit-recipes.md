# Redis Cache and Rate-Limit Recipes

## Cache-Aside

Use for read-heavy data where slight staleness is acceptable.

```python
def get_product(product_id: int):
    key = f"product:{product_id}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    product = db.query("SELECT * FROM products WHERE id = %s", product_id)
    r.setex(key, 3600, json.dumps(product))
    return product
```

## Write-Through

Use when the cache must reflect writes immediately; still keep database write ordering explicit.

```python
def update_product(product_id: int, data: dict):
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)
    r.setex(f"product:{product_id}", 3600, json.dumps(data))
```

## Tag-Based Invalidation

```python
def cache_product(product_id: int, category_id: int, data: dict):
    key = f"product:{product_id}"
    tag = f"tag:category:{category_id}"
    pipe = r.pipeline(transaction=True)
    pipe.setex(key, 3600, json.dumps(data))
    pipe.sadd(tag, key)
    pipe.expire(tag, 3600)
    pipe.execute()

def invalidate_category(category_id: int):
    tag = f"tag:category:{category_id}"
    keys = r.smembers(tag)
    if keys:
        r.delete(*keys)
    r.delete(tag)
```

## Session Storage

```python
def create_session(user_id: int, ttl: int = 86400) -> str:
    session_id = str(uuid.uuid4())
    key = f"session:{session_id}"
    pipe = r.pipeline(transaction=True)
    pipe.hset(key, mapping={"user_id": user_id, "created_at": int(time.time())})
    pipe.expire(key, ttl)
    pipe.execute()
    return session_id
```

## Fixed Window Rate Limit

```python
def is_rate_limited(user_id: int, limit: int = 100, window: int = 60) -> bool:
    key = f"ratelimit:{user_id}:{int(time.time()) // window}"
    pipe = r.pipeline(transaction=True)
    pipe.incr(key)
    pipe.expire(key, window)
    count, _ = pipe.execute()
    return count > limit
```

## Cache Stampede Prevention

Use a process-local lock only for single-process deployments. In multi-process systems, use Redis-backed coordination or probabilistic early refresh.

```python
def get_with_lock(key: str, fetch_fn, ttl: int = 300):
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    with local_lock_for(key):
        cached = r.get(key)
        if cached:
            return json.loads(cached)
        value = fetch_fn()
        r.setex(key, ttl, json.dumps(value))
        return value
```
