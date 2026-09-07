# Validation checklist

Do not send telemetry, deploy, or change Sentry/cloud settings without explicit authorization. Never report raw payloads, DSNs, credentials, headers, bodies, cookies, PII, or copied telemetry.

## Local checks

- Review the minimal diff against the existing initializer and configuration ownership. Confirm it merges rather than replaces and does not add another client/provider.
- Confirm current platform docs for all changed option names, integration behavior, middleware order, defaults, and lifecycle calls.
- Run applicable format, lint, type, unit, build, and startup checks without transmission where possible.
- Verify config resolution in test and production modes without printing sensitive values. Confirm a missing/invalid telemetry setting fails open and preserves normal application/error control flow.
- Exercise configured filters/redactors with synthetic non-sensitive values. Confirm no sensitive/high-cardinality fields are added by explicit scope enrichment.
- Exercise concurrent requests/jobs/tasks where relevant and verify scope isolation and cleanup.
- Inspect integration overlap: one owner per signal, no duplicate middleware/auto instrumentation, and no unintended startup/runtime overhead.
- Review error-event versus trace-sampling ownership and OTel coexistence; verify lifecycle coverage for worker/serverless/short-lived paths.

## Authorized controlled runtime check

Only after explicit authorization, use one uniquely marked, non-sensitive controlled event or request in an approved environment. Do not force a crash or use production/user data. Check the expected integration effect, intended tags/context only, filter/drop behavior, scope isolation, sampling decision, lack of duplicates, and documented lifecycle/draining attempt. Remove temporary diagnostics immediately.

A received event or successful flush is evidence of an attempt/result in that test, not a universal delivery guarantee.

## Report

Summarize: SDK/version and official pages read; changed locations; initializer/order; integration/default review; allowed data and filters; sampling/OTel/lifecycle decisions; local commands and outcomes; authorized remote test window/result without raw data; duplicates/overhead findings; skipped actions and authorization status; remaining uncertainty and rollback path.
