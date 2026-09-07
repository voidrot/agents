# Configuration workflow

Read the matching current platform pages in [platform documentation](platform-documentation.md) before changing configuration. Exact option names, default behavior, initialization APIs, and framework order are version-sensitive.

## Implementation checklist

1. Inspect the repository for the installed SDK/version, package lock/manifest, every runtime entry point, and all `init`/provider calls. Include workers, serverless handlers, native/mobile startup, SSR, and test bootstrap where applicable.
2. Map configuration sources: checked-in defaults, environment/runtime injection, build-time variables, secret manager, deployment manifests, and test fixtures. Identify which layer wins per environment.
3. Record active defaults, auto-detected integrations, manual integrations, callbacks, filters, scopes, sampling, OTel providers, and shutdown/draining. Do not assume an omitted option means the same thing across versions.
4. Name explicit ownership for each setting: one existing initializer and one configuration source. Separate test and production values and state who may change each.
5. Write a minimal proposed diff before mutation: file/location, old behavior, intended behavior, affected runtime, data effect, defaults preserved, tests, and rollback. Redact all values that could identify, authenticate, or transmit data.
6. Merge into the existing initialization object/function. Do not replace it, add a second initialization path, or replace an integration collection unless the exact docs establish the semantics and the diff preserves intended defaults.
7. Keep DSNs and credentials out of source, logs, fixtures, and build output. Respect runtime-vs-build boundaries: a browser/mobile value may be a public routing identifier but must still not be printed or copied; auth, upload, and deployment credentials remain secret and are outside this skill.
8. Ensure an absent, invalid, or failed configuration leaves normal error handling and app control flow intact. Do not add exits, retries, response changes, or error swallowing for telemetry.

## Authorization boundary

Read-only inspection and planning are allowed. Ask before changing a package or config, transmitting a controlled test event, deploying, or changing any Sentry/cloud setting. State the exact action, affected runtime/environment, data category, and secret location without revealing the secret.

## Sources

- [Go options](https://docs.sentry.io/platforms/go/configuration/options/)
- [Python options](https://docs.sentry.io/platforms/python/configuration/options/)
- [JavaScript options](https://docs.sentry.io/platforms/javascript/configuration/options/)
