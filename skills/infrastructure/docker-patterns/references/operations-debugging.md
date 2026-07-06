# Docker Operations and Debugging

## Common Commands

```bash
docker compose up --build
docker compose up -d --build
docker compose logs -f app
docker compose logs --tail=50 db
docker compose ps
docker compose top
docker stats
docker compose build --no-cache app
```

## Running Commands in Containers

```bash
docker compose exec app sh
docker compose exec db psql -U postgres
```

In non-interactive automation, avoid TTY flags and pass the exact command.

```bash
docker compose exec -T db psql -U postgres -c 'select 1'
```

## Networking Checks

```bash
docker compose exec -T app getent hosts db
docker compose exec -T app wget -qO- http://api:3000/health
docker network ls
docker network inspect <project>_default
```

## Cleanup

```bash
docker compose down
docker compose down -v
docker system prune -f
```

`down -v` removes named and anonymous volumes declared by the project and can delete local databases. Use only when data loss is acceptable.

## Anti-Patterns

| Anti-pattern | Risk | Better approach |
| --- | --- | --- |
| `latest` tags | Non-reproducible builds | Pin versions |
| Root runtime user | Larger blast radius | Create and use non-root user |
| Secrets in Dockerfile | Stored in layers/history | Runtime env or secrets manager |
| Data in container FS | Lost on recreate | Named volumes or external storage |
| One giant container | Hard scaling/debugging | One process/service per container |
