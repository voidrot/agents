# React Native

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[React Native Capturing Errors](https://docs.sentry.io/platforms/react-native/usage/) **confirms** current manual exception/message capture. [React Native platform documentation](https://docs.sentry.io/platforms/react-native/) is authoritative for the installed SDK's JS handler, React boundary, Expo, Android, and Apple native integration behavior. **Verify docs:** exact automatic JS rejection/error handling, top-level wrapper/boundary APIs, Hermes behavior, native crash persistence, ANR/app-hang support, and JS-to-native scope sync.

## Layer and owner decisions

Map JavaScript/Hermes errors, React render boundaries, Android Java/Kotlin/NDK crashes, and Apple native crashes separately. Prefer each layer's documented automatic owner for unhandled failures. Manually capture the original JS `Error` only when intentionally consumed. Do not catch a native fatal crash or duplicate it from JS. A React fallback boundary does not cover every event-handler/async error; handle those where they occur and capture only if consumed.

Initialize and wrap the app in the current documented order, preserving framework fallback and native crash-handler behavior. Nested boundaries, root wrappers, global JS handlers, and native bridges can overlap; validate one event per fault and do not use fingerprinting to conceal duplicates.

Use event-local/JS execution context with stable feature/screen template values. Never attach Redux/state snapshots, navigation parameters, form values, network bodies/headers, device identifiers, or raw native payloads. Logs and breadcrumbs are not exception events.

## Lifecycle and validation

JS reloads, app suspension/termination, native crash persistence, offline queues, and next-launch transmission differ by platform. No flush/ready callback guarantees delivery. Prefer one authorized handled synthetic JS error. Native hard-crash or ANR/app-hang tests require separate authorization and a safe device/build. Confirm event layer/mechanism, one event, cause/stack, safe cross-layer context, preserved fallback/termination behavior, and readable frames. JS source maps and Android/iOS debug symbols may be prerequisites; upload is outside scope.
