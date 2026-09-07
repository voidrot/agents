# Go Crons

Source of truth: [Sentry Go Crons](https://docs.sentry.io/platforms/go/crons/). Recheck this page before relying on version-sensitive APIs.

The current page requires Go SDK **0.23.0+** for recurring-job Crons. It documents manual check-ins: send `in_progress`, retain the returned check-in ID, then send `ok` or `error` with that same ID. It also documents heartbeat as a single check-in for missed-job detection; it does not detect a job exceeding maximum runtime.

The page documents `MonitorConfig` as the programmatic monitor create/update path. This is a remote/product action and requires explicit authorization. Its documented `MonitorConfig` fields are `Schedule`, `MaxRuntime`, `CheckInMargin`, and `FailureIssueThreshold`; inspect exact current types and semantics before editing. The documented schedule constructors are `CrontabSchedule` and `IntervalSchedule`; the latter documents minute, hour, day, week, month, and year units. Do not infer a wrapper, cancellation behavior, flush behavior, or delivery guarantee: this page establishes no such general guarantee.

Use manual lifecycle when it is the documented fit for the actual execution boundary. Preserve Go error and defer/control-flow semantics: reporting failure must not suppress or replace the job outcome. Do not port Python or JavaScript wrapper APIs to Go.

See [check-in lifecycle and monitor design](checkin-lifecycle-and-monitor-design.md) and [ownership, privacy, and lifecycle](ownership-privacy-and-lifecycle.md).
