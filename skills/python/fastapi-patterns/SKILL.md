---
name: fastapi-patterns
description: Build and review FastAPI apps with dependencies, Pydantic models, lifespan, OpenAPI, tests, and production boundaries.
origin: community
---

# FastAPI Patterns

## When to use

- implementing or reviewing FastAPI routes, dependencies, request/response models, middleware, or lifespan code
- organizing FastAPI services around async I/O, validation, OpenAPI, and tests
- checking FastAPI/Starlette/Pydantic behavior before changing API contracts

## Workflow

1. Identify FastAPI, Starlette, Pydantic, and ASGI server versions.
2. Keep route handlers thin: validate/authorize/coordinate, then delegate domain work.
3. Model request and response schemas explicitly and preserve documented API contracts.
4. Use dependency injection for request-scoped resources and lifespan for app-scoped resources.
5. Verify with focused API tests and generated OpenAPI expectations when contracts change.

## Constraints

- Do not block the event loop with sync I/O inside async routes.
- Do not leak internal exceptions or data models through response schemas.
- Move long examples for dependencies, lifespan, CORS, and tests to references.

## References

- [moved FastAPI patterns and examples](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
