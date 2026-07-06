# Docker Networking, Volumes, and Security

## Service Discovery

Compose services on the same network resolve each other by service name.

```text
postgres://postgres:postgres@db:5432/app_dev
redis://redis:6379/0
```

`ports` publish container ports to the host. Services do not need published ports to talk to each other inside the Compose network.

## Custom Networks

```yaml
services:
  frontend:
    networks: [frontend-net]
  api:
    networks: [frontend-net, backend-net]
  db:
    networks: [backend-net]

networks:
  frontend-net:
  backend-net:
```

## Volume Patterns

```yaml
services:
  app:
    volumes:
      - .:/app
      - /app/node_modules
      - /app/.next

  db:
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro

volumes:
  pgdata:
```

- Named volumes persist across container recreation.
- Bind mounts are useful for local development and hot reload.
- Anonymous volumes can protect container-generated directories from a broad bind mount.

## Dockerfile Hardening

```dockerfile
FROM node:22.12-alpine3.20
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
USER app
```

Use specific tags, run as non-root, keep runtime images small, and keep secrets out of layers.

## Compose Security Options

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /app/.cache
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

Add capabilities back only when the process actually needs them.

## Secrets

```yaml
services:
  app:
    env_file:
      - .env
    environment:
      API_KEY: ${API_KEY}
```

For Swarm or platforms that support secret mounts, prefer file-mounted secrets. For plain local Compose, keep `.env` gitignored and avoid committing secret values.
