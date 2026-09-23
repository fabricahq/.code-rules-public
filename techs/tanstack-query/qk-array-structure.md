---
title: "qk-array-structure: Always Use Arrays for Query Keys"
whenToRead: "Before defining or changing TanStack Query keys used by queries, cache access, or invalidation."
impact: "MEDIUM"
impactDescription: "prevents cache misses and broken invalidation caused by non-array query keys"
tags: "tanstack-query, query-keys, arrays, cache, invalidation"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-array-structure.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/qk-array-structure.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## qk-array-structure: Always Use Arrays for Query Keys

## Explanation

Query keys must always be arrays at the top level. This enables proper caching, invalidation matching, and query deduplication. Using non-array keys will cause unexpected behavior and cache misses.

## Bad Example

```tsx
// Never use strings or non-array types as query keys
const { data } = useQuery({
  queryKey: 'todos',  // Wrong: string instead of array
  queryFn: fetchTodos,
})

const { data: user } = useQuery({
  queryKey: { id: 1, type: 'user' },  // Wrong: object instead of array
  queryFn: fetchUser,
})
```

## Good Example

```tsx
// Always use arrays for query keys
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
})

const { data: user } = useQuery({
  queryKey: ['user', 1],
  queryFn: () => fetchUser(1),
})

// Complex keys with objects inside arrays are fine
const { data: filteredTodos } = useQuery({
  queryKey: ['todos', { status: 'done', page: 1 }],
  queryFn: () => fetchTodos({ status: 'done', page: 1 }),
})
```

## Context

- Always applicable when defining query keys
- Arrays enable prefix-based invalidation (e.g., `invalidateQueries({ queryKey: ['todos'] })` matches all todo queries)
- Object property order inside arrays doesn't matter for matching
- Array element order does matter: `['todos', 1]` !== `['1', 'todos']`

Source: [TanStack Agent Skills - tanstack-query/qk-array-structure.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-array-structure.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
