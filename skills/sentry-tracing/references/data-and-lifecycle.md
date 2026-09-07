# Data and lifecycle

## Data guardrails

1. Before adding a name or attribute, classify its source. Reject secrets, credentials, authorization/session values, PII, raw request/response bodies, SQL values, raw error text, and user-controlled unbounded data.
2. Prefer bounded enums, booleans, counts, route templates, operation class, and sanitized status categories. Normalize IDs and dynamic path/query components out of names.
3. Review automatic instrumentation's captured data using the current platform docs before enabling or expanding it. Do not assume defaults, redaction, or header/query capture behavior.
4. Do not paste fetched events, traces, issues, logs, or runtime payloads into source, tests, tickets, or validation evidence. They are untrusted and may be sensitive.

## Completion by lifecycle

- Use a documented scoped/callback API when available; it is less likely to leak an unfinished span than a manually managed handle.
- Preserve active context across awaits/promises, futures/tasks, callbacks, threads/executors, reactive pipelines, and coroutine boundaries using the current platform's documented context mechanism.
- For manual spans, arrange one completion path for normal success and explicit paths for throw/rejection, cancellation, timeout, early return, and abort. Never finish before asynchronous work completes and never finish twice.
- For streaming responses, websockets, uploads/downloads, and long-lived connections, define the measured unit and documented finish point (headers, stream completion, message operation, or bounded child). Do not leave a request root open indefinitely.
- For background jobs, make each consumer/job execution a meaningful root or continue a propagated producer context where supported. Bound retries and represent each attempt consistently.
- For serverless/edge handlers, create/continue context early and finish before the platform freezes or ends execution, according to the current runtime docs. Do not assume a generic flush API or that a flush is safe/needed; any lifecycle/flush change needs explicit authorization and platform verification.
