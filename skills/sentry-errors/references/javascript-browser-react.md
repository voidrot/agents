# Browser JavaScript and React

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status and sources

- [JavaScript Capturing Errors](https://docs.sentry.io/platforms/javascript/usage/) — **confirmed:** manual exception and message capture; pass an `Error` object for useful stack information; breadcrumbs are recorded with an event rather than creating one.
- [React Capturing Errors](https://docs.sentry.io/platforms/javascript/guides/react/usage/) — **confirmed:** React uses JavaScript capture APIs and documents React-specific error capture.
- [React error boundaries](https://docs.sentry.io/platforms/javascript/guides/react/features/error-boundary/) — consult for the installed React/Sentry versions and exact boundary API.
- The seeded Browser URL `/platforms/javascript/guides/browser/usage/` returned 404 during authoring; use the current [JavaScript platform guide](https://docs.sentry.io/platforms/javascript/) rather than preserving that stale path.

## Capture decision

The current JavaScript usage guide confirms intentional manual capture and that breadcrumbs are distinct from events. **Verify docs:** the exact default global-handler set and option names for the installed Browser SDK before claiming uncaught exceptions or promise rejections are automatic.

For React, place a framework-supported reporting boundary around the subtree that needs fallback behavior and keep any outer browser handler as the last-resort owner. React boundaries do not catch every event-handler or asynchronous error; route those failures through normal promise/event handling, then capture only if intentionally consumed. **Verify docs:** React 18 versus 19 root hooks, hydration/recoverable behavior, and whether a selected Sentry boundary already reports before adding a manual call.

Capture the original `Error`, not its text. A message is for a genuinely non-exceptional actionable condition. Console/Logs and breadcrumbs are not exception events.

## Ordering and duplicates

Initialize at the earliest current documented browser entry point before observed application code. Mount framework boundaries in the render tree where fallback ownership belongs. Do not manually report inside a boundary callback if that Sentry boundary/root hook already reports. Development render/replay can look duplicated; validate a production-like build before changing ownership.

Use event-local context for component/route-template/operation class. Do not attach props, state, form values, URLs with query strings, DOM dumps, headers, or user-entered text.

## Lifecycle and validation

Browser unload, tab termination, offline state, and abrupt crashes can lose buffered events; do not add unload blocking or promise delivery. With authorization, trigger one handled synthetic `Error` in a test build and one local-only boundary behavior test. Confirm one error event, useful JS/component frames when available, preserved fallback/control flow, and no sensitive context. Source maps may be required for readable minified frames; uploading them is outside this skill.
