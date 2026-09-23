---
title: "Build Index Maps for Repeated Lookups"
whenToRead: "Before doing repeated key-based searches over the same collection in React code."
impact: "LOW-MEDIUM"
impactDescription: "Repeated linear searches become costly as the number of items and lookups grows."
tags: "react, performance, javascript, map, indexing, optimization"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-index-maps.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Build Index Maps for Repeated Lookups

Multiple `.find()` calls by the same key should use a Map.

**Incorrect (O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Correct (O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Build map once (O(n)), then all lookups are O(1).
For 1000 orders and 1000 users, repeated linear searches can examine up to roughly 1M entries; building one map and then looking up each order takes roughly 2K collection operations.

Source: [Vercel Agent Skills - react-best-practices/js-index-maps.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-index-maps.md). Adapted with attribution.
