# Flutter

**Use for:** Flutter/Dart applications. Use [Android](android.md) only for an independent native Android app, not for a Flutter target.

1. Inspect `pubspec`, Flutter/Dart constraints, app startup, navigation, HTTP clients, platform targets, existing initialization, and obfuscation/symbol build settings. Follow the current Flutter guide for supported package/version and initialization details.
2. Initialize once around the documented app startup/error zone. Add navigation, network, tracing, replay, profiling, or ecosystem integrations only if currently supported and justified. Avoid duplicate error forwarding from Flutter and native layers.
3. If obfuscation or native artifacts apply, produce their symbols alongside the shipping build and preserve build/release identity. Authorized upload credentials remain outside source control.
4. Run Flutter analysis/tests/build. With authorization, validate a controlled event on the target platform and confirm stack readability when symbols apply.

Legacy material noted that capability varies by Flutter target and integrations; verify target support in the current guide. Docs: <https://docs.sentry.io/platforms/dart/guides/flutter/>.