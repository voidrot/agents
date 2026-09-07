# Check-in lifecycle and monitor design

Use one stable, non-sensitive monitor slug for one logical job in each intentional environment. Do not derive slugs from tenant data, arguments, timestamps, schedules, or deployment IDs. Reuse the established monitor where it represents the same job; do not create a monitor per run, retry, replica, or worker.

## Lifecycle choice

Use the current runtime documentation, not cross-SDK analogy.

- **Check-ins:** model one actual execution with an `in_progress` check-in, retain the returned ID, then complete that **same ID** once with `ok` or `error`. This provides start and completion information, including the ability to identify an execution that exceeds configured maximum runtime.
- **Heartbeat:** use one check-in only where missed-start detection is enough. Its tradeoff is that it can report a missed expected run but cannot detect a long-running execution; use the two-step lifecycle if long-runtime detection is required.
- Do not assume terminal check-ins are deduplicated, that cancellation has a documented terminal state, or that an SDK guarantees delivery/flush.

## Monitor configuration is a remote boundary

A documented SDK monitor configuration can programmatically create or update a monitor. Treat adding, changing, or executing it as an authorized remote/product action. Before authorization, prepare a review only. Do not silently configure monitor, project, environment, owner, schedule, timeout, margin, or thresholds.

Only use schedule, maximum-runtime, check-in-margin, failure/recovery threshold, timezone, and owner fields when the **current selected SDK documentation** establishes the exact API and semantics. Validate schedule and timezone against the real scheduler without exposing schedule internals in evidence. Do not invent a default or translate field names/types between SDKs.

## Retries and overlap

Establish the scheduler's semantics before instrumenting:

- A retry that invokes the job again is normally a new actual execution: it needs its own start-to-terminal lifecycle and must not reuse a prior execution ID.
- For overlapping executions, keep each execution's ID isolated and terminal completion singular. Do not emit from both an orchestration layer and worker layer.
- Reporting is not job idempotency. Preserve idempotency, locking, and retry behavior at the existing job boundary; do not add scheduler architecture in the name of monitoring.
- If ownership or execution cardinality cannot be established, stop rather than add ambiguous monitoring.

Official lifecycle examples and runtime-specific configuration are in [Go](go.md), [Python](python.md), [JavaScript/Node/Next.js](javascript-node-next.md), and [Cloudflare](cloudflare.md).
