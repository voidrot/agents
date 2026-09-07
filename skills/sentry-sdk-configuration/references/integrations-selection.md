# Integration selection

Integrations extend SDK behavior for common runtimes and libraries. Before implementation, read the current integration page for the installed SDK/version; an integration's availability, auto-detection, defaults, configuration, ordering, and data effects are platform-specific.

1. Detect the framework/library from manifests and actual runtime startup, then name the single capability needed.
2. Check whether the SDK already enables or auto-detects it. Review default and manual integrations before adding anything.
3. Select only the needed integration and the smallest documented compatible configuration. Do not add speculative integrations or a broad bundle.
4. Inspect integration arrays/callbacks carefully: they may merge with, transform, or replace defaults depending on the SDK. Preserve intended defaults explicitly only as current docs direct; never assume array behavior.
5. Review overlap with existing middleware/instrumentation, duplicate event/breadcrumb/span paths, startup/runtime overhead, and new data collection. Reject or narrow unsafe overlap.
6. For framework middleware, use the exact order from the selected platform/framework documentation. Do not generalize order from another framework or version.
7. Validate what changes: startup success, integration activation, changed signal/data behavior, duplication, overhead, filtering, and isolated request behavior. Do not use a remote event without authorization.

## Confirmed Go-specific behavior

For the current Go SDK documentation only, `ClientOptions.Integrations` receives the default integration list and can add to it or filter integrations by name. Supplying an empty list disables defaults. This is **not** an API pattern to apply to Python, JavaScript, or any other SDK; read their current documentation instead.

## Sources

- [Go integrations](https://docs.sentry.io/platforms/go/integrations/)
- [Python integrations](https://docs.sentry.io/platforms/python/integrations/)
- [JavaScript integrations](https://docs.sentry.io/platforms/javascript/configuration/integrations/)
