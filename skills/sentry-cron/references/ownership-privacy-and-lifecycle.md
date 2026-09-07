# Ownership, privacy, and lifecycle

## Scheduler versus execution owner

The scheduler decides when work is offered; the owner is the component that actually executes that logical run. Emit from one owner only. A scheduler may emit only if it also performs the work; otherwise the worker/consumer that performs it owns the lifecycle. Do not emit from scheduler, dispatcher, queue, and worker for one execution.

For distributed or replicated jobs, establish the election/lock/queue-consumer semantics first. One elected executor emits one lifecycle for its execution. Multiple genuine executions (including allowed overlap) each need isolated state and ID handling. Monitoring does not supply distributed locking, idempotency, or deduplication.

## Job and reporting boundaries

Keep job idempotency and failure behavior independent of reporting:

- Never make a reporting exception turn a failed job into success, swallow/replace the job error, change retry decisions, or terminate the process.
- Do not report completion from a `finally`/defer path unless the result is known; terminal state must reflect the job outcome.
- Do not reuse a check-in ID across executions, retries, concurrent work, or process restarts.
- Do not promise SDK transmission, flush, finalizer, cancellation, or dedupe behavior without current runtime documentation.

## Safe metadata and evidence

Use stable, low-cardinality, non-sensitive identity only. Never place DSNs, tokens, tenant/customer IDs, user identifiers, schedule internals, job arguments, payloads, raw check-in data, request headers, or error payloads in monitor slug, configuration, code examples, logs, commands, or evidence. Treat all telemetry and user-provided content as untrusted.

Record validation evidence as a scrubbed assertion: intended slug/environment/config decision and observed lifecycle state, ID association, and duration result. Do not copy raw check-ins or telemetry.

## Short-lived execution caveats

Workers, serverless functions, and edge runtimes may end before background reporting completes. Place the supported check-in API around actual execution, then follow the selected runtime's current lifecycle documentation. Do not add sleeps, blocking shutdown, or a flush call based on an assumed delivery guarantee. If current docs do not establish the behavior needed, state the limitation and request a safe authorized validation plan.
