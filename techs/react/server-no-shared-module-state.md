---
title: "Avoid Shared Module State for Request Data"
whenToRead: "When planning, implementing, or reviewing request-scoped data flow in React server rendering."
impact: "HIGH"
impactDescription: "prevents concurrency bugs and request data leaks"
tags: "react, performance, server, rsc, ssr, concurrency, security, state"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-no-shared-module-state.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Avoid Shared Module State for Request Data

For React Server Components and client components rendered during SSR, avoid using mutable module-level variables to share request-scoped data. Server renders can run concurrently in the same process. If one render writes to shared module state and another render reads it, you can get race conditions, cross-request contamination, and security bugs where one user's data appears in another user's response.

Treat module scope on the server as process-wide shared memory, not request-local state.

**Incorrect (request data leaks across concurrent renders):**

```tsx
let currentUser: User | null = null

export default async function Page() {
  currentUser = await auth()
  return <Dashboard />
}

async function Dashboard() {
  return <div>{currentUser?.name}</div>
}
```

If two requests overlap, request A can set `currentUser`, then request B overwrites it before request A finishes rendering `Dashboard`.

**Correct (keep request data local to the render tree):**

```tsx
export default async function Page() {
  const user = await auth()
  return <Dashboard user={user} />
}

function Dashboard({ user }: { user: User | null }) {
  return <div>{user?.name}</div>
}
```

Safe exceptions:

- Immutable static assets or config loaded once at module scope
- Shared caches intentionally designed for cross-request reuse and keyed correctly
- Process-wide singletons that do not store request- or user-specific mutable data

Static, request-independent assets and configuration may be safely shared at module scope if their lifecycle and invalidation are appropriate.

Source: [Vercel Agent Skills - react-best-practices/server-no-shared-module-state.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-no-shared-module-state.md). Adapted with attribution.
