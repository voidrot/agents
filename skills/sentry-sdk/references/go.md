# Go

**Use for:** Go services, CLIs, HTTP/gRPC servers, and workers. Do not assume a framework integration merely from a dependency; check the current Go guide.

1. Inspect `go.mod`, Go version, process entry points, HTTP/gRPC framework, panic/recovery middleware, logging, existing Sentry, and OpenTelemetry. Use the current guide to select supported modules and initialization lifecycle.
2. Initialize once early; ensure buffered events can flush during bounded graceful shutdown. Add documented HTTP/gRPC/framework integrations at the correct middleware position while preserving existing recovery/error responses.
3. Add tracing and sampling only after resolving any existing OTel provider through [OpenTelemetry](opentelemetry.md). Add release/environment from build metadata, not hand-maintained values. Go normally has no browser source-map step; if the delivery process creates native/debug artifacts, use the current platform documentation and preserve build identity.
4. Run `go test` and repository build/lint. With authorization, send a controlled error and confirm shutdown does not discard it and traces/artifacts behave as intended.

Legacy material stressed middleware selection and shutdown flushing; exact APIs and support are version-sensitive. Docs: <https://docs.sentry.io/platforms/go/>.