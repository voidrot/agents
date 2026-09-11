# JVM Java

## Confirmed support and paths

Current Java docs confirm Sentry Structured Logs in the Java SDK 8.12.0+. Enable the documented `logs.enabled` option, initialize before application logging, and use `Sentry.logger()`; advanced calls use `SentryLogParameters` and typed `SentryAttributes`. The Java page documents a Logs `beforeSend` callback and scope attributes.

| Library/path | Structured Logs support | Current requirement/configuration boundary |
|---|---|---|
| Direct Java SDK | Confirmed, 8.12.0+ | `logs.enabled`; direct `Sentry.logger()` APIs. |
| Logback | Confirmed, 8.15.0+ | Configure the Sentry appender's Logs option/threshold exactly as its Logs page shows. MDC attributes require the documented `contextTags` support/configuration. |
| Log4j2 | Confirmed, 8.16.0+ | Enable Logs in SDK properties/init and set the Sentry appender `minimumLevel` as needed. |
| JUL (`java.util.logging`) | Confirmed, 8.16.0+ | Enable Logs in SDK properties/init and configure the Sentry handler/`minimumLevel`. |
| Spring Boot + Logback | Confirmed by a current dedicated page | Add the documented Logback module and let the Spring Boot starter auto-configure the appender, then enable/gate Logs as documented. |
| Spring Boot + Log4j2 | Confirmed by a current dedicated page | Use the documented Log4j2 module/appender and Logs threshold. |

The current Java Logs page names no other Structured Logs bridge. Do not treat an appender's breadcrumbs or error events as Logs, and avoid simultaneous direct/appender capture of the same record.

## Safe implementation and validation

- Inventory the actual backend selected at runtime; SLF4J alone does not identify whether Logback or Log4j2 is active.
- Initialize Sentry before the appender emits relevant records. Preserve local appenders unless the user explicitly asks otherwise.
- Configure Logs minimum level independently of breadcrumb/event thresholds. Use `contextTags` only for an allowlisted, non-sensitive MDC subset; MDC is often request/user-derived and may cross boundaries if mis-scoped.
- Use typed/stable fields and never include raw exceptions or payloads as attributes. Expect sensitive-data scrubbing through Sentry server-side rules; if the user explicitly requests client-side privacy scrubbing, a documented Logs callback is optional defense in depth.
- The Logs/appender pages do not establish a universal JVM shutdown/flush guarantee. Follow the active SDK/framework lifecycle docs and report abrupt-exit risk.
- With authorization, emit one controlled record through the chosen appender or direct logger and verify level, MDC allowlist, one Logs record, and no unintended error event.

## Canonical official docs

- [Java Logs](https://docs.sentry.io/platforms/java/logs/)
- [Logback Logs](https://docs.sentry.io/platforms/java/guides/logback/logs/)
- [Log4j2 Logs](https://docs.sentry.io/platforms/java/guides/log4j2/logs/)
- [JUL Logs](https://docs.sentry.io/platforms/java/guides/jul/logs/)
- [Spring Boot with Logback](https://docs.sentry.io/platforms/java/guides/spring-boot/logging-frameworks/logback/)
- [Spring Boot with Log4j2](https://docs.sentry.io/platforms/java/guides/spring-boot/logging-frameworks/log4j2/)
