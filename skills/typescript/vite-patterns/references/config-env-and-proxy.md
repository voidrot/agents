# Vite Config, Environment, and Proxy Recipes

## Basic Config

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': new URL('./src', import.meta.url).pathname },
  },
})
```

## Conditional Config

```typescript
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), ['VITE_'])

  return {
    plugins: [react()],
    server: command === 'serve' ? { port: 3000 } : undefined,
    define: {
      __API_URL__: JSON.stringify(env.VITE_API_URL),
    },
  }
})
```

## Environment Rules

- Vite loads mode-specific `.env` files and exposes only variables with the configured public prefix to client code.
- `import.meta.env` values are statically replaced in client bundles.
- Treat all client-exposed values as public.

```typescript
import.meta.env.VITE_API_URL
import.meta.env.MODE
import.meta.env.BASE_URL
import.meta.env.DEV
import.meta.env.PROD
import.meta.env.SSR
```

Avoid broad env loading unless the values stay server-side and are never inlined into browser code.

```typescript
// Avoid for client defines: loads unprefixed secrets too.
const unsafe = loadEnv(mode, process.cwd(), '')

// Prefer explicit public prefixes.
const env = loadEnv(mode, process.cwd(), ['VITE_', 'APP_'])
```

## Dev Server Proxy

```typescript
export default defineConfig({
  server: {
    proxy: {
      '/foo': 'http://localhost:4567',
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

Add `ws: true` for WebSocket proxy routes.

## Docker / Container Access

```typescript
export default defineConfig({
  server: {
    host: true,
    hmr: { clientPort: 3000 },
  },
})
```

Vite's dev server is local by default; containers and remote dev environments usually need an explicit host setting.

## Monorepo File Access

```typescript
export default defineConfig({
  server: {
    fs: {
      allow: ['..'],
    },
  },
})
```

Keep the allow list as narrow as practical.
