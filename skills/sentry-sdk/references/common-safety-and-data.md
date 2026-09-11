# Safety, data, and build association

## Authority boundary

Ask for explicit authorization before changing dependencies, sending a test event, uploading source maps/debug symbols, or running a build/deploy path that can contact Sentry. Do not create projects, releases, environments, alerts, or product settings. A DSN is a routing/configuration identifier, not a secret credential: use placeholders and avoid copying production DSNs into examples, logs, or user-visible evidence to minimize unnecessary configuration disclosure. Keep authentication/upload credentials in approved secret storage and out of logs.

## Minimize data before capture

- Capture only data needed to diagnose the stated problem. Avoid PII, credentials, authorization headers, request bodies, query values, and sensitive business payloads by default.
- Expect sensitive-data scrubbing through Sentry server-side rules. Confirming or configuring those rules may require authorized Sentry administrator action; report it if unavailable rather than silently adding client-side redaction. Only when the user explicitly requests client-side privacy scrubbing, use SDK filtering/before-send-style hooks after checking the current platform API, as optional defense in depth.
- Treat breadcrumbs, user context, replay, logs, and tracing attributes as data collection; enable each deliberately and document its purpose.
- Confirm or configure organization-side scrubbing only with authorization; it is the expected privacy-scrubbing control. SDK-side filtering, when explicitly requested, is optional defense in depth and not proof that product-side rules are configured.

Official data-scrubbing guidance: <https://docs.sentry.io/product/data-management-settings/data-scrubbing/>. Replay and profiling have additional privacy/performance implications; consult <https://docs.sentry.io/product/session-replay/> and <https://docs.sentry.io/product/profiling/> before enabling them.

## Sampling and context

Choose error, trace, replay, and profiling sampling based on traffic, diagnostic value, privacy, and cost. Do not rely on an assumed SDK default or copy rates between runtimes. Preserve distributed-trace propagation only to approved targets and avoid adding high-cardinality or sensitive span attributes.

Set `release`, `environment`, and distribution/build identifiers only from the actual shipped build and consistently across all applicable runtime processes. These fields make events, traces, and artifacts findable; they are not a request to administer releases or environments. Official concepts: <https://docs.sentry.io/product/releases/> and <https://docs.sentry.io/product/releases/environments/>.

## Source maps and native symbols

Generate artifacts in the same build that produces the deployed bundle/binary. Keep release, distribution, debug identifiers, artifact paths/URLs, and deploy ordering aligned byte-for-byte with that build. Do not upload credentials or artifacts without authorization. Verify with a **new** event; an upload does not retroactively repair unrelated old events. If frames remain unreadable, compare the matching keys and build inputs before retrying an upload.

For JavaScript source maps, use the current guide: <https://docs.sentry.io/platforms/javascript/sourcemaps/>. For Android, Flutter, React Native, and other native artifacts, use the selected platform guide before choosing the build integration.
