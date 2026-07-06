# Vite Plugins, HMR, Build, and Dependency Recipes

## Common Plugins

| npm package | Use when |
| --- | --- |
| @vitejs/plugin-react or @vitejs/plugin-react-swc | React applications |
| @vitejs/plugin-vue | Vue 3 SFC projects |
| vite-plugin-checker package | TypeScript/ESLint feedback during dev |
| vite-tsconfig-paths package | Reuse `tsconfig.json` path aliases |
| vite-plugin-dts package | Emit declaration files for libraries |
| vite-plugin-svgr | Import SVGs as React components |
| rollup-plugin-visualizer | Inspect bundle composition |

Vite does not type-check as part of ordinary transpilation. Run `tsc --noEmit` in CI or add an appropriate checker workflow.

## Minimal Custom Plugin

```typescript
import type { Plugin } from 'vite'

function myPlugin(): Plugin {
  return {
    name: 'my-plugin',
    enforce: 'pre',
    apply: 'build',
    transform(code, id) {
      if (!id.endsWith('.custom')) return null
      return { code: transformCustom(code), map: null }
    },
  }
}
```

Useful hooks include `transform`, `resolveId`, `load`, `transformIndexHtml`, `configureServer`, and the current HMR update hook documented by Vite for your version.

Virtual modules conventionally resolve to IDs prefixed with `\0` internally while user code imports a public `virtual:*` ID.

## Manual HMR

Framework plugins usually handle HMR. Use `import.meta.hot` directly for custom state stores or dev tools.

```typescript
if (import.meta.hot) {
  import.meta.hot.data.count = import.meta.hot.data.count ?? 0
  import.meta.hot.dispose((data) => clearInterval(data.intervalId))
  import.meta.hot.accept()
}
```

Mutate properties on `import.meta.hot.data`; do not replace the data object.

## Manual Chunks

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
        },
      },
    },
  },
})
```

Avoid splitting every package into its own chunk; excessive tiny chunks can hurt loading.

## Dependency Pre-Bundling

```typescript
export default defineConfig({
  optimizeDeps: {
    include: ['lodash-es', 'cjs-package'],
    exclude: ['local-esm-package'],
  },
})
```

Use `optimizeDeps` for known CJS/interop or deep-import issues. Clear `node_modules/.vite` when stale pre-bundle cache causes phantom errors.
