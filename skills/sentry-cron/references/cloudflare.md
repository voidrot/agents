# Cloudflare Crons

Use the current official [Cloudflare Crons documentation](https://docs.sentry.io/platforms/javascript/guides/cloudflare/crons/) as the authority for `@sentry/cloudflare` Crons. The documented SDK support starts at **7.51.1+**; `withMonitor` is documented at **7.76.0+**.

The page documents two-step manual lifecycle reporting with `captureCheckIn`: start an execution, retain its returned check-in ID for that execution, and complete that same ID exactly once with the terminal outcome. A heartbeat is also documented; use it only when missed-start detection is sufficient, since it does not establish long-runtime completion. The documented `MonitorConfig` create/update fields include `schedule`, `checkinMargin`, `maxRuntime`, and `timezone`; `failureIssueThreshold` and `recoveryThreshold` require **8.7.0+**.

Choose one execution owner and one stable monitor identity per logical job/environment. Authorize monitor configuration and emitted check-ins before making remote changes. Keep metadata private and low-cardinality; never expose secrets, payloads, arguments, or raw check-ins. Do not assume cancellation, deduplication, delivery, or flush guarantees.

For Workers and Pages, follow the current Cloudflare documentation for execution and lifetime behavior. Do not port Node process-shutdown, blocking-flush, or other lifecycle assumptions to Cloudflare runtimes. Preserve job idempotency, retry behavior, and native result/error semantics independently of reporting.
