---
title: "Dependency-Based Parallelization"
whenToRead: "When planning, implementing, or reviewing asynchronous tasks that have partial dependencies."
impact: "CRITICAL"
impactDescription: "Unnecessary waits lengthen completion time for partly independent operations."
tags: "react, performance, async, parallelization, dependencies, better-all"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-dependencies.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Dependency-Based Parallelization

For operations with partial dependencies, consider `better-all` when it is available in the project. Model dependencies so independent work can start without waiting for unrelated tasks.

**Incorrect (profile waits for config unnecessarily):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Correct (config and profile run in parallel):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**Alternative without extra dependencies:**

We can also create all the promises first, and do `Promise.all()` at the end.

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

Reference: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)

Source: [Vercel Agent Skills - react-best-practices/async-dependencies.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-dependencies.md). Adapted with attribution.
