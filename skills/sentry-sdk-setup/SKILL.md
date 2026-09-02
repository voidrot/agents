---
name: sentry-sdk-setup
description: Select and set up the appropriate Sentry SDK for a project. Use when asked to add Sentry, install an SDK, or configure error monitoring.
license: Apache-2.0
metadata:
  role: router
---
# Sentry SDK Setup

## Choose the SDK

1. Inspect project files and state the detected platform. Confirm before editing when multiple choices fit.
2. Prefer the most specific available local skill:

| Project | Skill |
|---|---|
| Android | `sentry-android-sdk` |
| Browser JavaScript | `sentry-browser-sdk` |
| Cloudflare Workers/Pages | `sentry-cloudflare-sdk` |
| Flutter | `sentry-flutter-sdk` |
| Go | `sentry-go-sdk` |
| Next.js | `sentry-nextjs-sdk` |
| Node.js, Bun, or Deno | `sentry-node-sdk` |
| Python | `sentry-python-sdk` |
| React Native/Expo | `sentry-react-native-sdk` |
| React Router framework | `sentry-react-router-framework-sdk` |
| React | `sentry-react-sdk` |
| TanStack Start | `sentry-tanstack-start-sdk` |

Use framework-specific skills over their general runtime skill. For an unavailable platform, consult current official Sentry documentation rather than assuming a sibling skill exists.

## Set up safely

1. Ask for approval before installing packages, creating a remote project, or sending telemetry.
2. Follow the chosen skill's documented initialization, using the project's approved configuration and secret handling.
3. Start with error capture; enable extra signals only when requested or justified.
4. Verify with a controlled local test when possible. A remote event, deployment, or account action needs explicit authorization.

If an authenticated Sentry MCP capability is available, capability-check its tools and schema first; it is optional and not required for local setup.
