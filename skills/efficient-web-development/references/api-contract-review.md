# REST/API Contract Review

Read this only when the browser-facing change adds, changes, or diagnoses an HTTP API contract.

- Specify the operation's method, route, accepted headers/query/body, credential behavior, and validation ownership. Make the success status, headers, and response fields match what the browser uses.
- Give each expected failure a stable, user-safe status and body meaning. Separate correctable input, missing authentication, denied access, conflicts, missing resources, and unexpected server failures; never expose internals.
- Add pagination only when the collection's workload needs bounded retrieval, incremental loading, or navigation through more results. Define ordering, limit bounds, continuation or page semantics, and behavior while data changes. Do not paginate a small bounded result merely by convention.
- Decide repeated-request behavior from the operation's effects: safe reads must not mutate; retries or duplicate mutations need an established idempotency mechanism or an explicit conflict/outcome. Do not claim idempotence solely from a client-side disabled button.
- Preserve compatible consumers: retain documented fields, meanings, and error behavior unless a deliberate breaking change has an approved migration. Add envelope or API-versioning conventions only when the existing contract or a stated requirement calls for them.
- Keep security boundaries server-side: authenticate and authorize the specific resource/action, validate all input, apply existing CSRF/origin and rate controls where applicable, and avoid returning secrets or sensitive internals.

Repository API conventions and the requested behavior decide the result.
