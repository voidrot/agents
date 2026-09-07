# Android

**Use for:** native Android/Kotlin/Java. Use [Flutter](flutter.md) or [React Native](react-native.md) when Android is only a target of those SDKs.

1. Inspect Gradle modules, application class/startup path, existing Sentry dependency/config, R8/ProGuard, native code, and CI artifact build. Consult the current Android setup before selecting the official dependency/plugin and initialization model.
2. Initialize once at the documented earliest application lifecycle point. Add supported integrations for unhandled exceptions, ANRs, performance, or HTTP only when required; do not add manual captures that duplicate automatic capture.
3. For obfuscated Java/Kotlin or native frames, generate the matching mapping/native symbols in the shipping build. Upload only with authorization and approved credentials; match the deployed release/build identity.
4. Run Gradle checks/build locally. With authorization, verify one controlled event from the built app, including symbolicated frames and intended release/environment.

Legacy material mentioned Gradle/build integration and R8 mappings; use the current guide for their exact behavior and options. Official docs: <https://docs.sentry.io/platforms/android/>.