# JavaScript: Node and Next.js Crons

Use only the current official pages: [Node Crons](https://docs.sentry.io/platforms/javascript/guides/node/crons/), [Node troubleshooting](https://docs.sentry.io/platforms/javascript/guides/node/crons/troubleshooting/), [Next.js Crons](https://docs.sentry.io/platforms/javascript/guides/nextjs/crons/), and [Next.js troubleshooting](https://docs.sentry.io/platforms/javascript/guides/nextjs/crons/troubleshooting/). Do not claim parity between Node, Next.js, browser, Bun, Deno, or Cloudflare; use the dedicated [Cloudflare Crons](cloudflare.md) reference for Cloudflare.

## Node

The current Node page requires SDK **7.51.1+** for Crons and documents `Sentry.withMonitor()` from **7.76.0+**. It documents manual `Sentry.captureCheckIn()` for lifecycle control. Verify installed version and current signature before editing.

The documented monitor configuration path used with `withMonitor` or `captureCheckIn` can create/update a monitor remotely, so it requires explicit authorization. The page documents schedule (crontab or interval), `checkinMargin`, `maxRuntime`, `timezone`, `failureIssueThreshold`, and `recoveryThreshold`; the threshold fields currently state an SDK **8.7.0+** requirement. Recheck exact field support/type and avoid invented defaults.

The Node page documents scheduler helpers only for the listed libraries. Use a helper only when the actual scheduler matches current documentation and it produces the one intended owner/check-in path. Do not substitute or wrap it with a second manual path. `withMonitor` does not create a trace; that fact does not authorize generic tracing work.

## Next.js

The current Next.js page states Crons support only in **Server and Edge runtimes**. It documents `withMonitor` and manual lifecycle with the same version gates noted above, subject to the selected installed SDK and page confirmation.

Automatic check-ins are **Vercel-only**. The documented `automaticVercelMonitors` option applies to cron jobs determined at runtime from the `crons` field of `vercel.json`; the page's automatic monitoring scope is Vercel **Pages**. Do not enable or alter it without authorization, do not infer support for other hosts/runtimes, and do not combine it with another emitter for the same execution.

Neither section establishes a universal delivery, flush, cancellation, or deduplication guarantee. Preserve handler response/error and scheduler semantics. See [check-in lifecycle and monitor design](checkin-lifecycle-and-monitor-design.md).
