# TanStack Start

**Use for:** TanStack Start React applications. It wins over generic React/browser because it has client and server integration points.

1. Confirm TanStack Start, inspect client/router/server entry points, Vite config, production startup, existing SDK, and artifact build. Read the current TanStack Start guide before choosing the official package, plugin, or server instrumentation pattern.
2. Configure current documented client and server paths once each as applicable. Preserve framework middleware/error behavior; do not stack generic React or Node setup unless current docs explicitly support it.
3. Configure tracing, replay, logs, and sampling only for a stated use case and documented support. Build source maps from the deployment build; any upload uses explicitly authorized secret-backed credentials.
4. Run local build/tests and exercise client/server failure paths. With authorization, verify a new controlled event, request trace, release/environment association, and resolved frames.

Legacy material's Start-specific plugin/startup claims are version-sensitive; use the current guide rather than its exact names. Docs: <https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/>.