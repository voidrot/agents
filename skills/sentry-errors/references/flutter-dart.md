# Flutter and Dart

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

- [Flutter Capturing Errors](https://docs.sentry.io/platforms/dart/guides/flutter/usage/) **confirms** current manual capture for Flutter.
- [Dart Capturing Errors](https://docs.sentry.io/platforms/dart/usage/) is the base Dart guide.
- Read [Flutter platform setup](https://docs.sentry.io/platforms/dart/guides/flutter/) for the installed SDK's framework handlers and native integration behavior.

**Verify docs:** current `FlutterError`, platform-dispatcher/zone, isolate, silent framework error, Android/iOS native crash, and scope-sync behavior. Do not infer all Dart isolate or web/native failures are automatic.

## Layer and boundary decisions

Map Flutter framework errors, uncaught async Dart errors, spawned isolates, Android native/JVM/NDK faults, iOS native faults, desktop, and web separately. Preserve the framework's prior error callback/delegation and UI behavior. Manually capture a handled Dart exception with its original stack only if no installed handler owns it. Do not report manually and then pass the same exception to an automatic framework handler.

Initialize through the current documented Flutter wrapper/startup ordering. For custom framework callbacks, retain existing callbacks after/before Sentry exactly as docs require. Use event-local or isolate-local context; do not attach widget trees, state objects, route arguments, form input, HTTP bodies, or platform-channel payloads.

An error event is distinct from Logs and breadcrumbs. A textual message loses exception/stack semantics and is not a substitute.

## Lifecycle and validation

Native mobile crashes, Dart async work, isolates, desktop shutdown, web unload, and offline caching have different completion paths. Follow only platform-confirmed behavior; no flush guarantees delivery. With authorization, use one handled synthetic Dart exception with its captured stack. Test a secondary isolate or native crash only when in scope and separately authorized. Confirm one event, correct layer, stack/cause, scope isolation, unchanged Flutter error UI/propagation, and readable frames. Dart obfuscation/native symbols may be prerequisites; upload is outside scope.
