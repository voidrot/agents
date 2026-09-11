# Ruby

## Confirmed support and paths

Current Ruby documentation confirms the direct `Sentry.logger` route for Structured Logs after SDK initialization. It also documents the standard-library Ruby Logger `:logger` patch as sending Structured Logs. Standard-library Logger does not expose structured fields through that route; use the direct logger when intentional structured attributes are required.

No logging library other than standard-library Ruby Logger is named by the cited Logs and logging-integration docs. Do not infer support for other Ruby gems.

Logs are standalone searchable records, not breadcrumbs or error events. Preserve explicit exception capture for errors that need issue grouping or stack traces, and validate the configured output independently.

## Lifecycle, privacy, and validation

- Initialize before records are emitted and avoid overlapping direct and patched-Logger capture of the same call.
- Avoid intentionally logging secrets, PII, headers, bodies, and user-controlled data; use stable messages and low-cardinality attributes. Expect sensitive-data scrubbing through Sentry server-side rules. Use a current documented client-side filtering hook for privacy only when the user explicitly requests it, as optional defense in depth; do not invent one.
- Follow only current Ruby SDK lifecycle guidance; shutdown, crash, or abrupt termination can prevent buffered telemetry from arriving, and no flush is a delivery guarantee.
- With authorization, emit one non-sensitive record through the chosen route and verify one Structured Logs record rather than only a breadcrumb or event.

## Canonical official docs

- [Ruby Logs](https://docs.sentry.io/platforms/ruby/logs/)
- [Ruby Logger integration](https://docs.sentry.io/platforms/ruby/integrations/logging/)
