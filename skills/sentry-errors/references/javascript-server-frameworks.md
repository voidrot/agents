# JavaScript servers and full-stack frameworks

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

Do not treat these as one runtime API. Select the exact row and read it before editing.

| Target | Current official source | Confirmed / documentation-first boundary |
|---|---|---|
| Node.js | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/node/usage/) | Manual exception/message capture confirmed. Verify early initialization, automatic uncaught behavior, and the exact framework error-handler order in the selected integration docs. |
| Bun | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/bun/usage/) | Manual usage confirmed on its own page. **Verify docs** for Bun startup, integrations, and termination; do not copy Node preload or shutdown APIs. |
| Deno | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/deno/usage/) | Manual usage confirmed on its own page. **Verify docs** for Deno permissions, startup, runtime handlers, and termination; do not copy Node APIs. |
| Next.js | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/nextjs/capturing-errors/) | Framework error boundaries and manually captured caught Server Action/API failures are documented. Use the current App/Pages Router instructions and SDK-version prerequisites. |
| Cloudflare | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/cloudflare/usage/) | Manual capture is confirmed. **Verify docs** for current Worker/Pages/Queue/Durable Object wrappers, request isolation, and lifecycle; never substitute Node APIs. |
| React Router Framework mode | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/react-router/usage/) | Manual usage is confirmed. Read its [framework setup](https://docs.sentry.io/platforms/javascript/guides/react-router/) for current client/server request and error-handler ordering. Do not use this route for a plain React SPA. |
| TanStack Start | [Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/usage/) | Manual usage is confirmed. Read its [platform setup](https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/) for current SSR, global request/function middleware, and server-entry ordering. |

## Common decision

Capture an actual `Error` at one owner. A message is only for an actionable non-exception; Logs, `logger.error`, console, and breadcrumbs do not substitute for an error event. For caught and converted failures, manual capture may be needed, but first prove no framework hook/wrapper reports it. A manual capture followed by rethrow into an automatic owner is a likely duplicate.

## Framework ordering

- **Node frameworks:** initialization must precede instrumented imports where the current guide requires it. Error middleware order differs among Express/Fastify/Koa/Hapi/Connect/Nest and versions; use the exact integration page and do not preserve legacy order tables without re-verification.
- **Next.js:** treat browser, Node server, and edge runtime as separate capture layers. Follow the current `capturing-errors` page for App Router/Pages Router boundaries and request-error hooks. Caught Server Action or API failures need a deliberate owner. An error boundary may report an error also seen by a server hook, so validate duplicates rather than adding capture everywhere.
- **Cloudflare:** put official wrappers/plugins at the documented exported-handler or middleware boundary so platform lifecycle context remains available. Do not manually flush with Node APIs.
- **React Router Framework mode:** preserve its documented client hydration and server request/error handler exports/order. Custom handlers that replace defaults must deliberately retain capture and original logging/response behavior.
- **TanStack Start:** SSR/server errors and global request/function middleware have distinct boundaries. Preserve documented middleware array and server-entry wrapper order; do not infer React Router or Next.js behavior.

## Context and isolation

Use request/job/invocation-local context, stable route templates, and bounded operation/outcome tags. Never process-global request/user values. Do not attach bodies, headers, cookies, tokens, complete URLs/query strings, queue payloads, Server Action arguments, or raw errors as extras.

## Lifecycle and validation

Short-lived CLIs, workers, queues, serverless invocations, streams, and abrupt exits may finish before asynchronous transport. Follow only the selected page's current wait/flush/lifecycle method; `process.exit`-style abrupt termination can bypass normal cleanup. No method guarantees delivery.

With authorization, use one synthetic handled exception in the exact runtime. Verify one exception event, cause/stack, request isolation, unchanged HTTP/action/worker behavior, filtering, and no client/server duplicate. Source maps may be required for readable frames; upload is outside scope.
