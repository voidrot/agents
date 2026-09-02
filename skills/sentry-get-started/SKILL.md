---
name: sentry-get-started
description: Orient a project to Sentry and safely start an error-monitoring setup. Use when a user is new to Sentry or asks how to begin monitoring an application.
license: Apache-2.0
---
# Get Started with Sentry

First determine whether the project needs a new integration, an additional signal, issue investigation, readable stack traces, or release tracking. Do not create remote resources, install packages, or send telemetry without approval.

## Workflow

1. Inspect local manifests and existing Sentry configuration. Briefly report the detected platform and whether Sentry appears configured.
2. Ask the user to select the goal when it is not explicit:
   - Set up error monitoring: use `sentry-sdk-setup` or `sentry-instrument`.
   - Add tracing, logging, replay, profiling, metrics, cron, feedback, or AI telemetry: use `sentry-instrument`.
   - Investigate a known issue: use `sentry-debug-issue`.
   - Fix unreadable frames: use `sentry-fix-stack-traces`.
   - Track releases and deploys: use `sentry-setup-releases`.
3. For a new integration, confirm the SDK choice, package changes, DSN source, privacy requirements, and desired signals before editing. Start with error capture and add optional telemetry only when requested.
4. Use Sentry MCP only if it is available, authenticated, and its advertised tools authorize the intended action. It is optional; never assume authentication or perform a remote read/write without the user's authorization.
5. Complete the selected local workflow and report what was configured, how to verify it, required secrets, and any action the user must perform in Sentry or CI.
