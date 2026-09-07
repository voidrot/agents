# Apple/iOS Application Metrics

Use this reference only for the current official [iOS Application Metrics page](https://docs.sentry.io/platforms/apple/guides/ios/metrics/). It states that metrics are supported in Sentry Cocoa SDK **9.12.0+** (previously experimental from 9.4.0), are enabled by default, and are manually recorded through the `SentrySDK.metrics` namespace.

## Language and API boundary

The page documents Swift and says **Objective-C support for metrics is not currently available**. Do not infer an Objective-C implementation from a Swift API or another platform.

The documented namespace has `count`, `gauge`, and `distribution`:

- `count`: discrete event/request/error occurrence counts; values are typically non-negative integers.
- `gauge`: point-in-time values such as current queue depth or resource use.
- `distribution`: value observations such as duration or size.

Use the page's current Swift examples and types for the exact method signatures and `SentryUnit` representation. Do not port JavaScript unit strings or Dart option names.

## Enablement, filtering, attributes, and trace boundary

The page documents `options.enableMetrics = false` to disable metrics. Its `beforeSendMetric` callback can modify a `SentryMetric` or return `nil` to drop it. The documented metric exposes name, value, unit, attributes, timestamp, and `traceId`; use that callback to enforce an allowlist/drop policy, never to manufacture attributes from untrusted values.

A `traceId` in the iOS callback is runtime-specific correlation information. It is not a requirement to configure tracing for application metrics and does not establish behavior for another SDK. For trace-owned data, use tracing/span metrics instead.

## Delivery and validation

The page documents `SentrySDK.metrics.flush` as a blocking call that waits for pending data or its timeout. Use it only after authorization and at a documented lifecycle boundary; it does not guarantee delivery. First test metric contract and once-only placement locally. With separate authorization for remote traffic, send one low-volume, non-sensitive metric and verify only safe aggregate fields. Do not include a DSN, credentials, raw payload, or user data in source or evidence.
