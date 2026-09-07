# Browser JavaScript

**Use for:** browser JavaScript/TypeScript without a more-specific framework route. Next.js, React, React Router Framework mode, TanStack Start, React Native/Expo, and Cloudflare take precedence.

1. Inspect the bundler, existing browser SDK/init, router, error handling, service-worker/CSP constraints, and source-map build output. Use the current JavaScript guide to choose the official browser SDK and current install/init API.
2. Initialize once before application rendering; add supported error, navigation, fetch/XHR, replay, or profiling instrumentation only for an agreed need. Deliberately configure sampling, propagation targets, and sensitive-data filtering.
3. Generate source maps in the deployed build and keep artifact paths, release/environment/dist/debug IDs aligned. Upload requires authorization; never put upload credentials in client code.
4. Run the app/build locally and verify no duplicate errors. With authorization, create one controlled non-sensitive event and confirm a new event has readable frames.

Legacy guidance favored framework SDKs over a raw browser SDK and warned that source maps must match the shipped build; current docs determine all API/tooling details. Docs: <https://docs.sentry.io/platforms/javascript/>; source maps: <https://docs.sentry.io/platforms/javascript/sourcemaps/>.