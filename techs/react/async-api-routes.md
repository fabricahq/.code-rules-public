---
title: "Prevent Waterfall Chains in API Routes"
whenToRead: "Before implementing or reviewing Next.js API routes or Server Actions with multiple asynchronous operations."
impact: "CRITICAL"
impactDescription: "Sequential independent operations add their latencies to API response time."
tags: "react, performance, api-routes, server-actions, waterfalls, parallelization"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-api-routes.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Prevent Waterfall Chains in API Routes

In API routes and Server Actions, start independent operations immediately, even if you don't await them yet.

**Incorrect (config waits for auth, data waits for both):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**Correct (auth and config start immediately):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

For more complex dependency chains, identify which tasks can start before others complete. A dependency-aware concurrency helper can express that ordering when one is already part of the project.

Source: [Vercel Agent Skills - react-best-practices/async-api-routes.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-api-routes.md). Adapted with attribution.
