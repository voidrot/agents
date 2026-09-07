# Ruby

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Ruby Capturing Errors](https://docs.sentry.io/platforms/ruby/usage/) **confirms** manual exception/message capture. Use [Ruby integrations](https://docs.sentry.io/platforms/ruby/integrations/) for Rails, Rack, Sidekiq, background jobs, and other automatic capture. Automatic behavior is not established for an integration until its current page confirms it.

## Decision and ordering

Prefer documented middleware/job integration capture for unhandled exceptions. Manually capture the original exception only where rescue code intentionally consumes an unexpected actionable failure. Preserve `cause` and backtrace; do not capture only the message. Avoid rescue/capture/re-raise into an automatic Rack/Rails/job boundary.

Follow the exact integration's initializer and middleware order, keeping custom exception rendering and job retry/dead-letter behavior unchanged. **Verify docs:** Rails exception app behavior, Rack insertion order, Sidekiq retry ownership, async/fiber context, forking servers, and logging integration event behavior.

Use request/job/fiber-local scope and reset it in pooled workers. Never attach params, session, cookies, headers, ActiveRecord objects, job arguments, or arbitrary exception instance data. Logs and breadcrumbs are context, not captured exceptions.

## Lifecycle and validation

Forks, preloading, worker shutdown, short scripts, signals, and abrupt exit can lose buffered events. Follow current worker/server lifecycle docs and do not promise delivery. With authorization, use one rescued synthetic exception with a cause in a safe environment; confirm one event, backtrace/cause, scope isolation, unchanged response/retry/re-raise behavior, and expected-error filtering. Native extension symbols are a separate readability prerequisite.
