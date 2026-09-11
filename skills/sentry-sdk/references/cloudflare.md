# Cloudflare

**Use for:** Cloudflare Workers or Pages, including worker handlers and supported Cloudflare bindings. It wins over Node/browser. For a framework deployed to Cloudflare, first verify whether its official framework guide supersedes this route.

1. Inspect Wrangler configuration, Worker vs Pages entry point, compatibility settings, bindings, existing SDK, and build output. Consult the current Cloudflare guide for the official package and wrapper/init route.
2. Apply the documented wrapper/instrumentation at the actual request/handler boundary, once. Preserve platform error semantics; add tracing or binding-specific instrumentation only if currently documented and needed.
3. DSNs are routing/configuration identifiers, not secret credentials; use placeholders and avoid copying production DSNs into examples, logs, or user-visible evidence. Treat tokens and other Worker environment credentials as secret and do not expose them in source or output. If source maps are produced, associate them with the exact deployed build and use authorized credential handling.
4. Run local Worker/Pages checks where the repository provides them. With authorization, send a controlled event through the deployed test path and verify runtime, trace, and frames.

Legacy claims about automatic binding instrumentation are version-dependent; confirm them in the current guide instead of assuming them. Docs: <https://docs.sentry.io/platforms/javascript/guides/cloudflare/>.