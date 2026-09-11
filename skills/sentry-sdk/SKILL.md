---
name: sentry-sdk
description: Configure, instrument, upgrade, debug setup, or validate official Sentry SDKs in Android, browser JavaScript, Cloudflare, Flutter, Go, Next.js, Node/Bun/Deno, Python, React, React Native, React Router Framework mode, TanStack Start, and SDK-relevant OpenTelemetry interoperability. Not for Sentry product administration or generic OpenTelemetry work.
---

# Sentry SDK

Use this skill for application-side official SDK work only. Do **not** use it for alert creation, issue triage/remediation, release or product administration, billing, arbitrary custom Sentry integrations, or a generic OpenTelemetry project. Metadata is in scope only when it makes SDK events readable and correctly associated.

## Safety prerequisites

1. Inspect the repository and its existing telemetry before proposing changes. Preserve its package manager, runtime entry points, and deployment model.
2. DSNs are routing/configuration identifiers, not secret credentials. Use placeholders such as `<SENTRY_DSN>` and avoid copying production DSNs into examples, logs, or user-visible evidence to minimize unnecessary configuration disclosure. Never print, commit, or put auth tokens, source-map/debug-symbol credentials, or PII in examples, output, logs, or test fixtures.
3. Installation, source-map/debug-symbol upload, deployment, test-event sending, and any remote Sentry action require explicit user authorization. Do not create projects or change Sentry settings.
4. Read [common safety and data](references/common-safety-and-data.md) before initialization; read [common verification](references/common-verification.md) before claiming success.
5. Current official docs and the installed SDK version control. Look up the selected platform page before writing version-sensitive commands, package names, configuration keys, or APIs.

## Select the runtime reference

Specific framework routes always win:

| Detect/request | Read |
|---|---|
| Next.js | [Next.js](references/nextjs.md), not browser or Node |
| Cloudflare Workers/Pages | [Cloudflare](references/cloudflare.md), not Node or browser |
| React Native or Expo | [React Native](references/react-native.md), not React or browser |
| React Router **Framework mode** | [React Router Framework](references/react-router-framework.md), not React |
| TanStack Start | [TanStack Start](references/tanstack-start.md), not React or browser |
| Other React SPA/non-framework routing | [React](references/react.md) |
| Browser JavaScript without a more-specific framework SDK | [Browser](references/browser.md) |
| Node.js, Bun, or Deno server runtime without a more-specific framework SDK | [Node/Bun/Deno](references/node-bun-deno.md) |
| Android native | [Android](references/android.md) |
| Flutter/Dart | [Flutter](references/flutter.md) |
| Go | [Go](references/go.md) |
| Python | [Python](references/python.md) |
| Existing OpenTelemetry that must coexist with Sentry SDK tracing | [OpenTelemetry](references/opentelemetry.md) |
| Any SDK upgrade | [Upgrades](references/upgrades.md) plus the selected platform |

For an unlisted framework, stop rather than substituting a generic SDK; use its current official Sentry platform guide.

## Ordered workflow

1. **Inventory.** Identify runtime/framework, SDK and version, package manager, initialization and startup order, existing error middleware/boundaries, tracing provider, build pipeline, and artifact output. Do not duplicate initialization or providers.
2. **Choose coverage.** Start with error capture. Add tracing, replay, profiling, logging, metrics, crons, user feedback, or framework integrations only for a stated need and after checking the current platform docs. Set sampling deliberately; do not assume defaults.
3. **Obtain authority.** Before a package change, remote test event, upload, or deployment, state the exact action, data involved, credentials location, and ask for authorization if it was not already granted.
4. **Install and initialize.** Use the platform's current official installation and initialization path. Initialize at the earliest documented runtime entry point, once per runtime, before code to be observed. Load the DSN from the configuration source appropriate to the project and runtime; it is not a secret credential, but avoid committing or copying a production DSN into source, examples, logs, or user-visible evidence.
5. **Instrument the application.** Add official framework middleware, error boundaries, route/navigation hooks, or supported integrations only where the platform reference and current docs call for them. Preserve error propagation and avoid capturing the same exception twice.
6. **Make events usable.** Set release/environment/dist or equivalent only from the deployed build identity; keep artifact identifiers and paths aligned with that build. Avoid intentionally attaching sensitive data and expect scrubbing through Sentry server-side rules; confirming or configuring rules may require authorized Sentry administrator action, and report it if unavailable. Configure client-side privacy filtering or scrubbers only when the user explicitly requests them, as optional defense in depth. See [safety/data](references/common-safety-and-data.md).
7. **Build artifacts when relevant.** Generate source maps or native symbols in the producing build. Upload only with explicit authorization and approved secret handling; never claim stack traces will resolve until matching is verified.
8. **Validate.** Run local static/build/test checks first. Send one controlled test event only when authorized, then verify event, trace, and artifact association according to [verification](references/common-verification.md). Remove temporary diagnostics.
9. **Report evidence.** State selected SDK/runtime, installed version, initialization locations, enabled signals and sampling, sensitive-data controls, release/environment/artifact matching, local checks, authorized remote checks, and unresolved risks.

## Documentation-first decisions

Treat these as version-sensitive and look them up at implementation time: installation command, SDK/package choice, initialization API/options, startup/preload behavior, framework wrappers, sampling option names/defaults, integrations, source-map/debug-symbol tooling, and upgrade migrations. Do not copy old snippets merely because they compile.

## Completion evidence

Do not call setup complete without: one initialization per applicable runtime; configuration sourced safely; error path covered; no competing tracing provider; build/tests passing; and, if authorized, a newly generated controlled event with the intended release/environment and readable frames where artifacts apply. Record remote checks that were skipped because authorization was absent.
