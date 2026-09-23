---
title: "Cross-Request LRU Caching"
whenToRead: "When planning, implementing, or reviewing server caches shared across requests in a React application."
impact: "HIGH"
impactDescription: "Repeated cross-request work can increase latency; unsafe cache keys can expose data between users."
tags: "react, performance, server, cache, lru, cross-request"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-cache-lru.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Cross-Request LRU Caching

`React.cache()` only works within one request. For safe, shared data across sequential requests (for example, the same public reference data needed by two actions), consider an LRU cache with bounded size and explicit invalidation. Never share user-specific data across requests without isolation in the cache key.

**Implementation:**

```typescript
import { LRUCache } from 'lru-cache'

type ReferenceItem = { id: string; label: string }

const cache = new LRUCache<string, ReferenceItem>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
})

export async function getPublicReferenceItem(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  // This helper reads data that is public and identical for every caller.
  const item = await loadPublicReferenceItem(id)
  if (item) cache.set(id, item)
  return item
}

// Request 1: source read, result cached in this process
// Request 2 on the same process: cache hit
```

Use when sequential requests need the same public, stable data. Invalidate the cache when that data changes; a TTL alone may be too stale for some contracts.

**With Vercel's [Fluid Compute](https://vercel.com/docs/fluid-compute):** LRU caching is especially effective because multiple concurrent requests can share the same function instance and cache. The in-memory cache may persist across requests served by the same instance; other instances do not share it.

**Across serverless instances:** Process memory is neither shared nor durable. Use an external cache such as Redis when requests need shared cache state.

Reference: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

Source: [Vercel Agent Skills - react-best-practices/server-cache-lru.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-cache-lru.md). Adapted with attribution.
