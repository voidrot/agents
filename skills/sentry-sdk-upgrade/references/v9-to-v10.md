# Sentry JavaScript SDK: v9 to v10 Migration Reference

v10 has been released. For authoritative migration steps, consult the official [v10 migration guide](https://docs.sentry.io/platforms/javascript/migration/v9-to-v10/); this reference has not yet been populated with its full detail.

## Current Status

As of this writing, v10 is the latest major version of the Sentry JavaScript SDK (`@sentry/node` is at 10.x on npm). The deprecation table below lists the v9 deprecations that were slated for removal in v10; verify against the official guide.

## Known v9 Deprecations (Likely Removed in v10)

These were deprecated in v9 and will likely be removed in v10:

| Deprecated | Replacement |
|---|---|
| `logger` export from `@sentry/core` (internal SDK logger) | `debug` export (`debug.log`, `debug.warn`, `debug.error`) |
| `@sentry/types` package | `@sentry/core` (all types available there) |

```diff
- import { logger } from '@sentry/core';
- logger.info('message');
+ import { debug } from '@sentry/core';
+ debug.log('message');
```

## Preparation

To prepare for v10:
1. Upgrade to latest v9
2. Fix all deprecation warnings
3. Replace `@sentry/types` imports with `@sentry/core`
4. Replace internal `logger` usage with `debug`

## When This Reference Is Expanded

Populate this file from the official guide with:
1. Version support changes
2. Removed APIs (from v9 deprecations)
3. Behavioral changes
4. Package changes
5. Migration grep patterns
