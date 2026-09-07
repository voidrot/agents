# Platform documentation index

This index is not a capability matrix. Before implementation, identify the runtime, framework, and **installed SDK version**, then read the matching current official page(s). A framework-specific guide wins over a base-language page. If this index lacks the exact runtime/framework page, find its current official `docs.sentry.io` guide before modifying configuration.

| Runtime | Read before configuration work |
|---|---|
| Go | [integrations](https://docs.sentry.io/platforms/go/integrations/), [options](https://docs.sentry.io/platforms/go/configuration/options/), [scopes](https://docs.sentry.io/platforms/go/enriching-events/scopes/), [draining](https://docs.sentry.io/platforms/go/configuration/draining/) |
| Python | [integrations](https://docs.sentry.io/platforms/python/integrations/), [options](https://docs.sentry.io/platforms/python/configuration/options/), [sensitive data](https://docs.sentry.io/platforms/python/data-management/sensitive-data/) |
| JavaScript browser | [integrations](https://docs.sentry.io/platforms/javascript/configuration/integrations/), [options](https://docs.sentry.io/platforms/javascript/configuration/options/), [enriching events](https://docs.sentry.io/platforms/javascript/enriching-events/) |
| Node.js | [Node guide](https://docs.sentry.io/platforms/javascript/guides/node/), then applicable JavaScript integrations/options/enrichment pages |
| Next.js | [Next.js guide](https://docs.sentry.io/platforms/javascript/guides/nextjs/), then applicable framework-specific configuration pages |
| Android | [Android platform guide](https://docs.sentry.io/platforms/android/) and the current platform's scope guidance. The [versioned v7 scope page](https://docs.sentry.io/platforms/android/enriching-events/scopes__v7.x) is historical only; use it only when the installed version is v7. |
| Flutter/Dart | [Flutter guide](https://docs.sentry.io/platforms/dart/guides/flutter/) |
| React Native | [React Native guide](https://docs.sentry.io/platforms/react-native/) |
| Apple | [Apple platform guide](https://docs.sentry.io/platforms/apple/) |
| .NET | [.NET platform guide](https://docs.sentry.io/platforms/dotnet/) |

For privacy/sampling/lifecycle, follow links from the selected guide to that SDK's current options, data-management, tracing/OTel, and draining/shutdown pages; exact behavior remains version-specific.
