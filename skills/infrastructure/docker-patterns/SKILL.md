---
name: docker-patterns
description: Use for Dockerfile, Compose, networking, volumes, security hardening, and local dev container workflows.
origin: ECC
---

# Docker Patterns

Activation and routing layer for Docker and Compose work.

## When to Activate

- Creating or reviewing Dockerfiles and multi-stage builds
- Setting up Docker Compose for local development or test dependencies
- Debugging container networking, ports, DNS, or volumes
- Hardening containers for least privilege and secret hygiene
- Splitting dev/prod container concerns without overbuilding orchestration

## Workflow

1. **Identify the target**: local dev, CI, test dependency, production image, or production orchestration.
2. **Choose build shape**: minimal runtime image, multi-stage build, pinned base image, reproducible package install.
3. **Model services**: Compose service names, networks, volumes, health checks, and startup dependencies.
4. **Harden defaults**: non-root user, no secrets in layers, minimal capabilities, read-only filesystem where practical.
5. **Verify behavior**: build, run, health-check, inspect logs, and document destructive cleanup commands.

## Safety Rules

- Do not bake secrets into images or committed Compose files.
- Pin image versions for reproducibility; avoid `latest` in durable workflows.
- Use named volumes for persistent service data; containers are disposable.
- Bind only required ports, preferably to `127.0.0.1` for local-only services.
- Treat `docker compose down -v` and prune commands as destructive.

## Reference Routing

- Dockerfile, Compose, override, and `.dockerignore` templates: [references/dockerfile-and-compose-templates.md](references/dockerfile-and-compose-templates.md)
- Networking, volumes, security, and secrets patterns: [references/networking-volumes-security.md](references/networking-volumes-security.md)
- Debugging and operational commands: [references/operations-debugging.md](references/operations-debugging.md)
- Imported general Docker workflow patterns: [references/imported-docker-patterns.md](references/imported-docker-patterns.md)
- Multi-stage Dockerfile structure and image-size optimization: [references/multi-stage-dockerfiles.md](references/multi-stage-dockerfiles.md)

## Expected Output

- Dockerfile/Compose changes or review notes
- Dev/prod boundary and startup dependency notes
- Security and secret-handling caveats
- Verification commands to run non-interactively
