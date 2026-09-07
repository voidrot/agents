# React Native and Expo

**Use for:** React Native, Expo managed/bare, and Expo Router. It wins over React/browser. Check the current guide for Expo compatibility and native build requirements; do not infer them from legacy versions.

1. Inspect package manager, Expo vs bare RN, app config, native `android`/`ios` projects, navigation, Hermes/Metro, existing SDK/config plugin, and CI build/artifact path.
2. Use the current official Expo or React Native setup path. Initialize once in the documented application entry point and apply supported navigation/error integrations without duplicating native/JS capture.
3. Treat config-plugin/build changes as native build changes. Generate and, only when authorized, upload the matching JS source maps and native symbols from the same shipped build. Keep secrets out of app config and client bundles.
4. Run JS and native/Expo checks available locally. With authorization, validate a controlled event on device/simulator/test build and inspect JS/native frame resolution and navigation traces.

Legacy material noted Expo has a distinct path and that Hermes affects source-map handling; confirm current behavior in the official docs. Docs: <https://docs.sentry.io/platforms/react-native/>.