# React

**Use for:** React browser apps and non-framework routing. React Router **Framework mode**, TanStack Start, Next.js, and React Native/Expo use their specific references instead.

1. Inspect React/router/build-tool versions, existing SDK, root rendering, error boundaries, navigation, and source-map output. Confirm this is not a framework-mode route before selecting the current official React SDK instructions.
2. Initialize once before rendering. Use current documented error boundary/error-handler and router instrumentation patterns; preserve fallback UI and normal error propagation. Add replay, profiling, logs, or state integrations only when needed and supported.
3. Configure tracing/replay sampling and data masking deliberately. Generate source maps from the shipping build, with matching release/environment/dist/debug IDs; authorized upload credentials must never reach client code.
4. Run type/build/test checks and manually exercise an error boundary. With authorization, validate one controlled event and navigation trace, then verify readable frames.

Legacy material correctly routes framework mode away from generic React; React-version-specific error handling is version-sensitive. Docs: <https://docs.sentry.io/platforms/javascript/guides/react/>; source maps: <https://docs.sentry.io/platforms/javascript/sourcemaps/>.