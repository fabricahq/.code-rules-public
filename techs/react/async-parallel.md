---
title: "Promise.all() for Independent Operations"
whenToRead: "Before implementing or reviewing multiple independent asynchronous operations in a React application."
impact: "CRITICAL"
impactDescription: "Sequential independent awaits increase response or render latency."
tags: "react, performance, async, parallelization, promises, waterfalls"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-parallel.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Promise.all() for Independent Operations

When async operations have no interdependencies, execute them concurrently using `Promise.all()`.

**Incorrect (sequential execution, 3 round trips):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct (parallel execution, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

Source: [Vercel Agent Skills - react-best-practices/async-parallel.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-parallel.md). Adapted with attribution.
