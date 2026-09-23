---
title: "Keep request data out of shared module state"
whenToRead: "Before planning, writing, changing, or reviewing server-rendered React code, Server Components, or server functions that store data in module-level variables."
impact: "HIGH"
impactDescription: "Concurrent requests share module state, so request data stored there can leak one user's data into another user's response."
tags: "react, server-components, ssr, concurrency, security"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-no-shared-module-state.md
    description: "Adapted from the Vercel Agent Skills rule server-no-shared-module-state: restructured to the rule template with a rationale and validation."
---

## Keep request data out of shared module state

Do not store request- or user-specific data in mutable module-level variables on the server.
Pass it through props, function arguments, or a request-scoped API such as `React.cache`.

### Implementation

- Treat server module scope as memory shared by every request the process handles.
- Pass request data, such as the current user, down the component tree as props, or read it through a request-scoped function.
- Module-level values are fine when they are immutable and identical for every request, such as static configuration or assets loaded once.
- A shared cache is fine when it is designed for cross-request reuse and its keys include everything that makes an entry request-specific.

### Rationale

A server can render several requests concurrently in one process, interleaving their asynchronous work.
If one render writes a module-level variable and another render overwrites it before the first reads it, the first request renders the second request's data.
The result is a race condition that can expose one user's data to another.

### Examples

**Incorrect (counterexample):**

```tsx
let currentUser: User | null = null;

export default async function Page() {
  currentUser = await auth();
  return <Dashboard />;
}

async function Dashboard() {
  return <div>{currentUser?.name}</div>;
}
```

If two requests overlap, request B can overwrite `currentUser` before request A renders `Dashboard`, so user A sees user B's name.

**Correct:**

```tsx
export default async function Page() {
  const user = await auth();
  return <Dashboard user={user} />;
}

function Dashboard({ user }: { user: User | null }) {
  return <div>{user?.name}</div>;
}
```

### Validation

Search server modules for top-level `let` declarations and for module-level objects or collections that are mutated inside request handlers or components.
Each one should hold only request-independent data or be a cache keyed by all request-specific inputs.

Immutable configuration, assets loaded once, and correctly keyed caches are not violations.
