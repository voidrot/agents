# Common error-capture policy

Apply this policy before runtime-specific implementation. Exact SDK APIs and defaults come from the current platform guide, not this document.

## Event ownership

1. Draw the path from throw/fault to the framework/runtime terminus.
2. Mark every catcher: local `catch`/rescue, UI boundary, framework middleware, task runner, global handler, native crash handler.
3. Assign exactly one Sentry **error-event owner**:
   - use a documented automatic integration for an error that remains unhandled;
   - manually capture an unexpected actionable exception only where application code intentionally handles/consumes it;
   - if manually captured and rethrown, disable/narrow another owner or remove the manual call after confirming automatic coverage.
4. Preserve the application's pre-existing response, fallback, retry, propagation, and termination semantics. Telemetry failure must fail open.

Automatic capture is integration- and version-specific; it is not implied merely by SDK initialization. A caught exception is not necessarily invisible and a rethrown one is not necessarily captured—verify the exact framework boundary.

## Exceptions, causes, and messages

- Capture the original exception/error/throwable so stack and mechanism survive. Preserve native language cause/chaining/wrapping; do not replace it with a formatted string.
- Capture a message only for an actionable condition that genuinely has no exception. Messages often have weaker stacks/grouping.
- Logs and breadcrumbs are separate telemetry. `logger.error`, console output, and a breadcrumb do not create a captured exception event.
- An event is one occurrence sent to Sentry; an Issue is server-side grouping of similar events. This skill creates/reviews events, not Issue triage.

Official concepts: [breadcrumbs](https://docs.sentry.io/product/issues/issue-details/breadcrumbs/) and the [SDK platform/usage overview](https://docs.sentry.io/platforms/).

## Expected versus actionable errors

Do not report routine input validation, cancellation, expected authorization denial, not-found, health checks, polling misses, retries, circuit-breaker control flow, or expected business outcomes by default. First decide whether the condition represents an actionable defect. Filter at the narrowest semantic boundary, not by a broad fragile substring. Keep a documented allow/drop rationale and test that real unexpected failures still pass.

Use [filtering](https://docs.sentry.io/platforms/javascript/configuration/filtering/) only as a concept example; open the exact platform's filtering/configuration page before implementing option names or callback behavior.

## Scope lifetime and isolation

Choose the narrowest lifetime:

- **Event-local:** preferred for one handled exception.
- **Request/job/task/isolate-local:** identity and operation context shared by events in one unit of work.
- **Process/global:** immutable deployment-wide values only. Never place request or user values here in concurrent software.

Confirm that framework integrations isolate concurrent requests and that context crosses only intended async/thread/goroutine/isolate boundaries. Clear user context on logout/end of identity. A scope must not leak between tenants, requests, jobs, sessions, JS/native layers, or pooled workers.

Official scope concepts: [scopes](https://docs.sentry.io/platforms/javascript/enriching-events/scopes/) and the selected platform's **Enriching Events** section.

## Context, tags, extras, and breadcrumbs

- **Tags:** small, stable, low-cardinality dimensions such as component or operation class.
- **Contexts/extras:** bounded structured diagnostic values not intended as indexed dimensions.
- **Breadcrumbs:** a short scrubbed sequence leading to the event, not an event and not an audit log.
- **User:** only an approved pseudonymous identifier if policy permits; omit email, IP, names, and raw account data by default.

Use an allowlist. Never attach request/response bodies, authorization/cookie headers, credentials, tokens, query strings, raw framework objects, arbitrary exceptions' custom fields, or raw telemetry. Avoid high-cardinality IDs and attacker-controlled values. Prefer counts, enums, route templates, feature names, and bounded outcomes.

## PII and filtering

Prevent sensitive collection at the source. Review automatic request/user/device integrations and local before-send/event-processor/breadcrumb filters for the exact SDK. Product-side scrubbing is defense in depth, not permission to send data. A filter must itself avoid logging the discarded payload. Treat every captured value and exception message as untrusted.

Current official starting points: [data management](https://docs.sentry.io/security-legal-pii/scrubbing/), [SDK data handling](https://docs.sentry.io/platforms/javascript/data-management/), and the exact platform's configuration/filtering pages.

## Duplicate avoidance

Common duplicate paths include manual capture plus rethrow; nested UI boundaries; framework callback plus global handler; worker wrapper plus task handler; server and client reporting the same serialized failure; native and managed bridges; overlapping integrations; and development-mode double invocation. Compare event mechanism, exception identity, stack, timestamp, and boundary—not raw payloads in evidence. Fix ownership rather than adding a fingerprint to hide duplicates.

## Grouping and fingerprints

Start with default grouping. Before overriding it, write the intended invariant: which events must merge or split and why that aids actionability. Use stable bounded domain components; never use user IDs, request IDs, timestamps, full URLs, or raw messages. Prefer retaining the default fingerprint component when the exact SDK documents it. Validate at least two same-family and two different-family examples. Fingerprinting can permanently fragment or merge Issues; it does not fix duplicate capture.

Current official docs: [grouping](https://docs.sentry.io/concepts/data-management/event-grouping/) and [custom fingerprints](https://docs.sentry.io/platforms/javascript/usage/sdk-fingerprinting/). Treat the JavaScript API syntax as JavaScript-only; locate the exact platform page for implementation.
