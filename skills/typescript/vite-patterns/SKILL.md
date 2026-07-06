---
name: vite-patterns
description: Use when configuring or debugging Vite projects, including config files, plugins, env, HMR, dev proxy, SSR, library mode, dependency optimization, and builds.
origin: ECC
---

# Vite Patterns

Activation and routing layer for Vite-based projects.

## When to Activate

- Editing `vite.config.ts` / `vite.config.js`
- Configuring env variables, dev server, proxy, HMR, aliases, or Docker access
- Choosing or authoring Vite plugins
- Debugging dependency pre-bundling, CJS/ESM interop, slow dev server, or build output
- Publishing libraries with Vite library mode
- Handling SSR externals or framework integration issues

## Workflow

1. **Identify mode**: dev server, production build, preview smoke test, SSR, or library build.
2. **Keep config typed**: use `defineConfig` and framework plugins before custom hooks.
3. **Protect secrets**: only public values should use the client-exposed env prefix.
4. **Verify production path**: `vite build` then `vite preview` for a local smoke test; deploy with a real static host/server.
5. **Add type checking separately**: Vite transpiles; run `tsc --noEmit` or a checker plugin in CI/dev.

## Safety Rules

- Do not expose secrets through `VITE_` env vars, `envPrefix: ''`, or broad `loadEnv(..., '')` usage.
- Do not assume dev behavior matches build; test the built output.
- Do not ship source maps publicly unless your release process uploads and protects them appropriately.
- Do not hand-write many aliases that duplicate `tsconfig` paths; prefer a maintained paths plugin.
- For containers, set the dev server host explicitly so it is reachable outside the container.

## Reference Routing

- Config structure, env variables, security, dev proxy, Docker, and monorepo access: [references/config-env-and-proxy.md](references/config-env-and-proxy.md)
- Plugin choices, custom plugin shape, HMR, build chunks, and dependency optimization: [references/plugins-hmr-and-build.md](references/plugins-hmr-and-build.md)
- Library mode, SSR externals, performance tuning, and deployment pitfalls: [references/library-ssr-and-performance.md](references/library-ssr-and-performance.md)

## Expected Output

- Minimal Vite config change or recipe
- Dev/build/SSR mode caveats
- Security implications for env and source maps
- Verification commands, especially build and type-check checks
