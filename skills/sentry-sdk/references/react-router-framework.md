# React Router Framework mode

**Use for:** React Router Framework mode with its framework entry/server model. It wins over generic React. Non-framework/data/declarative React Router should use [React](react.md).

1. Confirm framework mode from its config/entry structure and inspect client/server entry points, server startup, Vite/build config, existing SDK, and source-map output. Consult the current React Router Sentry guide before selecting package and setup steps.
2. Apply the current documented client and server initialization/error/tracing hooks at the framework boundaries. Preserve thrown responses and framework error behavior; avoid adding generic React/Node instrumentation that duplicates coverage.
3. Decide browser replay and server tracing separately, with deliberate sampling/data filtering. Create source maps in the matching build and keep upload authority/credentials separate from client output.
4. Run framework build/tests. With authorization, validate a controlled client error and server request error, then check route/trace association and readable frames.

Legacy material described this SDK as pre-release; confirm current support and compatibility instead of repeating that status. Docs: <https://docs.sentry.io/platforms/javascript/guides/react-router/>.