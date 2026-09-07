# Python Crons

Source of truth: [Sentry Python Crons](https://docs.sentry.io/platforms/python/crons/). Recheck this page before relying on exact versions or signatures.

The current page requires Python SDK **1.17.0+** for recurring-job Crons. It documents `monitor` as a decorator and context manager, plus manual `capture_checkin` lifecycle. The page says `monitor` can annotate asynchronous functions from **1.44.1+**; use that version fact only after confirming the installed version and do not infer unlisted async exception behavior.

The page says `monitor_config` requires **1.45.0+** and can be supplied to the wrapper or manual `capture_checkin` path. It is a programmatic monitor create/update mechanism, therefore an explicit-authorization remote/product action. The documented configuration fields cover schedule, timezone, `checkin_margin`, `max_runtime`, `failure_issue_threshold`, `recovery_threshold`, and `owner`; verify exact types/defaults/semantics in the current page before editing. The page shows crontab and interval schedules, with interval values expressed as integers in its documented configuration.

For manual monitoring, follow the page's two-step lifecycle: retain the ID from `in_progress` and complete that same ID with `ok` or `error`. Do not port Node's `withMonitor` or Go APIs. Ensure a decorator/context manager surrounds the actual execution once; preserve the application’s exception, cancellation, and retry behavior rather than assuming undocumented wrapper behavior.

See [check-in lifecycle and monitor design](checkin-lifecycle-and-monitor-design.md) and [ownership, privacy, and lifecycle](ownership-privacy-and-lifecycle.md).
