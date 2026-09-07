# Node.js, Bun, and Deno

**Use for:** server-side JavaScript/TypeScript without Next.js or Cloudflare. Use framework-specific official guidance when it exists.

1. Identify Node/Bun/Deno, ESM/CJS, true production start command, server framework, existing error middleware, startup/preload files, Sentry packages, and OTel. Current docs decide the runtime-specific package, import/preload order, and supported framework integration.
2. Load SDK instrumentation before modules/frameworks it must observe; initialize once. Place error middleware as documented without replacing application error responses. Do not assume Node instructions work in Bun or Deno.
3. Choose tracing/replay/profiling/logging only after checking runtime support and resolving competing OTel initialization. If a bundled server/client artifact has source maps, generate them in the shipping build and authorize any upload separately. Keep server-only credentials out of browser bundles.
4. Run the real start/build/test path. With authorization, create a controlled error and verify process lifecycle, trace linkage, and readable frames.

Legacy material warned that module system and preload order affect instrumentation; confirm the exact current startup pattern. Docs: <https://docs.sentry.io/platforms/javascript/guides/node/>; JavaScript overview: <https://docs.sentry.io/platforms/javascript/>.