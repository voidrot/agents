# PowerShell

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[PowerShell Capturing Errors](https://docs.sentry.io/platforms/powershell/usage/) is the current official general capture guide. It **confirms only the manual behavior shown on that page**. Use [PowerShell platform documentation](https://docs.sentry.io/platforms/powershell/) for current module/version setup. **Verify docs:** terminating versus non-terminating error handling, trap behavior, pipeline/runspace/jobs/remoting support, automatic unhandled capture, and shutdown/flush. Do not infer .NET SDK APIs or automatic behavior even though PowerShell runs on .NET.

## Decision and ordering

First classify the failure as a terminating exception, non-terminating error record, expected command outcome, or host termination. Preserve `$ErrorActionPreference`, trap/catch behavior, exit code, pipeline output, and host behavior. Manually capture only an unexpected actionable error at the boundary that consumes it. Do not change an error into terminating/non-terminating solely for telemetry, and do not stringify away exception/stack information.

If current docs do not establish a general automatic path, state that it is **unconfirmed** and use only documented manual capture. Avoid duplicate trap/catch/global host ownership. Logs, verbose/error streams, breadcrumbs, and messages are not captured exception events.

Use invocation/runspace-local bounded context. Never attach command lines containing secrets, environment dumps, credentials, remoting payloads, pipeline objects, script arguments, or raw error records.

## Lifecycle and validation

Short scripts, jobs, runspaces, remoting sessions, host stop, and forced exit may end before send completion. Follow current module guidance without sleeps or delivery claims. With authorization, use one caught synthetic exception in a test script. Confirm one event, exception/stack, unchanged stream and exit behavior, no duplicate, and safe context.
