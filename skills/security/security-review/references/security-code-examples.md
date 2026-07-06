# Security code examples

Examples are illustrative. Match exact APIs and mitigations to the framework in use.

## Secrets

```typescript
const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) {
  throw new Error('OPENAI_API_KEY is not configured')
}
```

Avoid hardcoded values such as `const apiKey = "sk-..."` or committing `.env` files.

## Input validation

```typescript
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
})

export async function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input)
  return db.users.create({ data: validated })
}
```

## SQL injection prevention

```typescript
await db.query('SELECT * FROM users WHERE email = $1', [userEmail])
```

Avoid:

```typescript
await db.query(`SELECT * FROM users WHERE email = '${userEmail}'`)
```

## Authorization check before mutation

```typescript
export async function deleteUser(userId: string, requesterId: string) {
  const requester = await db.users.findUnique({ where: { id: requesterId } })
  if (!requester || requester.role !== 'admin') {
    return { status: 403, error: 'Forbidden' }
  }
  await db.users.delete({ where: { id: userId } })
}
```

## XSS and CSP

```typescript
import DOMPurify from 'isomorphic-dompurify'

const clean = DOMPurify.sanitize(userHtml, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
  ALLOWED_ATTR: [],
})
```

Start CSP strict and loosen only with a documented reason:

```text
default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; script-src 'self'
```

## Logging

```typescript
logger.info('payment_authorized', { userId, paymentId, last4 })
```

Avoid logging passwords, tokens, full card numbers, CVV, private keys, session cookies, and raw authorization headers.

## Negative security tests

```typescript
test('rejects unauthenticated access', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

test('rejects invalid input', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' }),
  })
  expect(response.status).toBe(400)
})
```
