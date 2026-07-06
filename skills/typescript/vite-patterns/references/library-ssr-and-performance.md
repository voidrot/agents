# Vite Library, SSR, Performance, and Deployment Notes

## Library Mode

```typescript
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.ts',
      formats: ['es', 'cjs'],
      fileName: (format) => `my-lib.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom', 'react/jsx-runtime'],
    },
  },
})
```

- Emit types separately with `tsc --emitDeclarationOnly` or a declaration plugin.
- Externalize peer dependencies to avoid bundling duplicate runtimes into consumers.

## SSR Externals

Most app teams should prefer a framework with documented Vite SSR integration. When tuning raw Vite SSR or framework escape hatches, use externals deliberately.

```typescript
export default defineConfig({
  ssr: {
    external: ['node-native-package'],
    noExternal: ['esm-only-package'],
    target: 'node',
  },
})
```

## Dev Server Performance

- Avoid broad barrel imports in hot paths; direct imports reduce module fan-out.
- Prefer maintained plugins over custom transform pipelines.
- Keep aliases and extension resolution minimal.
- Use Vite's profiling/debug guidance for the installed version when dev server startup or HMR is slow.

```typescript
export default defineConfig({
  server: {
    warmup: {
      clientFiles: ['./src/main.tsx', './src/routes/**/*.tsx'],
    },
  },
})
```

## Deployment Pitfalls

- `vite preview` is a local smoke-test server, not a production server.
- New builds create new hashed chunks; keep old assets available during rolling deploys or handle dynamic-import failures with a reload path.
- Disable public source maps unless your release process uploads them to an error tracker and prevents public exposure.
- Verify production behavior with build output, not only the dev server.

```bash
npm run build
npm run preview -- --host 127.0.0.1
npm run typecheck
```
