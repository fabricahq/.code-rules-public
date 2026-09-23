---
title: "Run post-response work after the response"
whenToRead: "Before planning, writing, changing, or reviewing Next.js Route Handlers, Server Actions, or Server Components that do secondary work, such as logging, analytics, or notifications, before responding."
impact: "MEDIUM"
impactDescription: "Secondary work awaited before responding adds its latency to every request."
tags: "react, nextjs, server, latency"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-after-nonblocking.md
    description: "Adapted from the Vercel Agent Skills rule server-after-nonblocking: restructured to the rule template, added exceptions for work whose outcome the response reports."
---

## Run post-response work after the response

In Next.js, schedule work that the response does not depend on with `after()`, so it runs after the response is sent.

### Implementation

- Use `after()` for logging, analytics, audit records that may be written late, cache warming, and notifications that the caller does not wait for.
- Keep work in the request when the response reports its result, or when it must succeed before the caller proceeds.
- Handle errors inside the `after()` callback; the caller cannot see them.
- `after()` callbacks run even when the response fails or redirects; check the outcome inside the callback when that matters.

### Rationale

Every `await` before a response adds its latency to the request.
Work that the caller does not need delays it for no benefit.
`after()` lets the platform finish that work once the response is on its way.

### Examples

**Incorrect (counterexample):**

```ts
export async function POST(request: Request) {
  const result = await updateDatabase(request);
  await logUserAction({ action: 'update', userAgent: request.headers.get('user-agent') });
  return Response.json(result);
}
```

The client waits for the log write.

**Correct:**

```ts
import { after } from 'next/server';

export async function POST(request: Request) {
  const result = await updateDatabase(request);
  const userAgent = request.headers.get('user-agent');

  after(async () => {
    try {
      await logUserAction({ action: 'update', userAgent });
    } catch (error) {
      reportError(error);
    }
  });

  return Response.json(result);
}
```

### Validation

For each awaited call in a request path, ask whether the response needs its result or success.
If not, it belongs in `after()`.

Awaiting work whose result the response returns is not a violation.
