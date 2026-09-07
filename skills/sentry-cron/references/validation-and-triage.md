# Validation and triage

## Safe local validation

Before any remote action, inspect code and configuration locally:

1. Confirm selected runtime, installed SDK version, and current official reference.
2. Map one logical job/environment to one stable slug and one actual execution owner.
3. Search for automatic helpers, wrappers, and manual check-ins that could double-report.
4. Review start, success, failure, timeout/cancellation where relevant, retry, overlap, and shutdown paths. Confirm a manual start ID is retained only by its execution and receives one intended terminal completion.
5. Confirm reporting errors cannot change job return/error, retry, or process lifecycle.
6. Check that no secrets, schedule internals, IDs, arguments, payloads, or raw telemetry will be logged or retained as evidence.

## Authorized controlled check-in process

Only after the user explicitly authorizes remote check-ins and any monitor create/update/configuration action, perform the smallest safe controlled process. Use a non-sensitive established or explicitly authorized monitor identity; do not create duplicate monitors. Verify in authorized Sentry views only:

- intended slug, environment, and configuration decision;
- one lifecycle's `in_progress` and same-ID terminal `ok` or `error` association; and
- expected duration/outcome without copying raw check-in data.

Do not promise delivery, flush, or deduplication. Do not configure alerts, notifications, dashboards, ownership/project settings, or other product administration.

Where authorized and safe, test failure, missed-run, or long-running behavior separately and only when it will not affect real work or create unwanted operational consequences. Heartbeat is relevant to missed-run detection; two-step check-ins are required to observe long runtime. Do not manufacture a failure or delay without explicit approval.

## Failure map

| Observation | Safe next action |
| --- | --- |
| Duplicate check-ins or monitors | Stop emissions; identify automatic/manual and scheduler/worker owners; retain one owner only. |
| Terminal state has wrong/missing ID | Stop; repair execution-local ID flow and ensure one completion path. |
| Job result/retry changed | Remove reporting influence from job control flow; preserve original error/return behavior. |
| Missing or late remote evidence | Do not assert delivery; check authorization, selected docs, SDK initialization/lifecycle, and scrubbed local path evidence. |
| Wrong environment/configuration | Stop remote changes; obtain authorization before correcting remote/product configuration. |
| Unsupported runtime/API | Do not port another SDK API; consult [unsupported or undocumented runtimes](unsupported-or-undocumented-runtimes.md). |

Official lifecycle behavior is platform-specific: [Go](https://docs.sentry.io/platforms/go/crons/), [Python](https://docs.sentry.io/platforms/python/crons/), [Node](https://docs.sentry.io/platforms/javascript/guides/node/crons/), [Next.js](https://docs.sentry.io/platforms/javascript/guides/nextjs/crons/), and [Cloudflare](https://docs.sentry.io/platforms/javascript/guides/cloudflare/crons/).
