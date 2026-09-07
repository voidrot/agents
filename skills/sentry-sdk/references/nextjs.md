# Next.js

**Use for:** Next.js. It wins over generic browser and Node because browser, server, and Edge paths may all need coverage.

1. Inspect Next version, App vs Pages Router, `next.config`, instrumentation/client/server/edge files, error boundaries, build mode, and existing SDK. Merge with existing instrumentation rather than replacing it. Follow the current Next.js guide for package, wizard/manual setup, and runtime files.
2. Initialize/configure each required runtime through the documented route, once per runtime. Preserve App/Pages error boundaries and server behavior. Do not apply a raw Node preload or browser init unless the current Next guide directs it.
3. Decide tracing, replay, profiling, logging, and cron instrumentation individually; check present framework/version support. Build source maps in the deploy build; upload only with authority and server-side credentials, keeping release/build identity aligned.
4. Run Next lint/type/test/build. With authorization, test client, server, and Edge paths that the app uses; verify the resulting event runtime, release/environment, trace continuity, and frames.

Legacy material's three-runtime warning remains useful, but file names/options and build tooling are version-sensitive. Docs: <https://docs.sentry.io/platforms/javascript/guides/nextjs/>.