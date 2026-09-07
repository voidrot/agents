# Cloudflare Workers and Pages

## Confirmed support and paths

The current Cloudflare guide covers both Cloudflare Workers and Cloudflare Pages, and its Logs page confirms the JavaScript Structured Logs API for the Cloudflare SDK. JavaScript Logs are supported from SDK 9.41.0+, enabled by default from 10.71.0+, and require `enableLogs: true` on older supported versions. Initialize through the documented Cloudflare wrapper for the actual Worker/Pages request handler, then use `Sentry.logger` with structured attributes or `Sentry.logger.fmt`.

Current Cloudflare Logs documentation names exactly these bridges:

| Path/library | Structured Logs status |
|---|---|
| Direct `Sentry.logger` | Confirmed |
| Console via `consoleLoggingIntegration` | Confirmed; select levels explicitly. Multiple-argument parsing requires SDK 10.13.0+. |
| Consola via `createConsolaReporter` | Confirmed; requires SDK 10.12.0+. |

No Pino, Winston, Bunyan, or other logging-library bridge is named on the current Cloudflare Logs page. Do not infer Node or Next.js integrations into Workers/Pages. Ordinary `console.*` behavior is not proof of Sentry Logs without the documented Logs forwarding integration.

## Initialization and lifecycle

- Inspect whether the deployment is a Worker, Pages Function, or both and find every exported request handler. Apply the current Cloudflare wrapper/setup only to the in-scope handler.
- Keep request attributes on the request/current scope; never mutate process/global scope with tenant, user, authorization, or request data in a reused isolate.
- Broad Console capture can forward platform/framework messages. Restrict levels and use `beforeSendLog` with a key allowlist.
- The Cloudflare Logs page does not document a universal flush call for request completion. Do not import Node shutdown patterns, extend request lifetime speculatively, or promise delivery; follow only current Cloudflare lifecycle guidance verified for the installed SDK.

## Safe validation

After explicit authorization, invoke one safe non-production Worker/Pages route that emits a controlled `info` log after Sentry initialization. Use a synthetic correlation value and bounded `runtime="cloudflare_worker"` or `"cloudflare_pages"` attribute. Verify one record, expected origin/level, and no direct-plus-console duplicate. Never log request headers, cookies, URL query strings, bodies, environment bindings, or secrets.

## Canonical official docs

- [Cloudflare Logs](https://docs.sentry.io/platforms/javascript/guides/cloudflare/logs/)
- [Cloudflare Workers and Pages setup](https://docs.sentry.io/platforms/javascript/guides/cloudflare/)
