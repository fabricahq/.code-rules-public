---
title: "Define hierarchical query keys and options in factories"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query keys that several components, prefetches, or invalidations share, or when adding queries for a new entity."
impact: "MEDIUM"
impactDescription: "Keys written by hand in many places drift apart, so invalidation and prefetching miss entries that were meant to match."
tags: "tanstack-query, query-keys, queryOptions, invalidation"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-factory-pattern.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule qk-factory-pattern (MIT, notice retained in NOTICE.md): merged the hierarchical-organization rule, restructured to the rule template, and made queryOptions factories the primary pattern."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-hierarchical-organization.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule qk-hierarchical-organization (MIT, notice retained in NOTICE.md): merged the hierarchical-organization rule, restructured to the rule template, and made queryOptions factories the primary pattern."
---

## Define hierarchical query keys and options in factories

Build each entity's query keys from general to specific, such as entity, then kind, then ID or filters, and define them, together with their query functions, in one factory per entity.
Use the factory everywhere the query is read, prefetched, updated, or invalidated.

### Implementation

- Start every key for an entity with the same prefix, such as `['todos']`, then add a kind such as `'list'` or `'detail'`, then the ID or filters.
- Define factory functions that return `queryOptions({ queryKey, queryFn, ... })`, so the key, query function, and per-query options stay together and types flow to `useQuery`, `prefetchQuery`, and `getQueryData`.
- Expose prefix helpers, such as `todoQueries.all()` or `todoKeys.lists()`, for invalidation at each level.
- A small app with a handful of queries can inline keys; add a factory when the same key is written in more than one place.

### Rationale

TanStack Query matches keys by prefix for invalidation and cache filters.
A consistent hierarchy lets one call target exactly the right level, such as every list of todos or one todo and its sub-resources.
Keys typed by hand in many files drift, such as `'todo'` in one place and `'todos'` in another, and the mismatch silently skips cache entries.

### Examples

**Incorrect (counterexample):**

```tsx
useQuery({ queryKey: ['todos', 'list', filters], queryFn: () => fetchTodos(filters) });
useQuery({ queryKey: ['todo', id], queryFn: () => fetchTodo(id) });

queryClient.invalidateQueries({ queryKey: ['todos'] });
```

The detail query uses `'todo'`, so invalidating `['todos']` misses it.

**Correct:**

```tsx
export const todoQueries = {
  all: () => ['todos'] as const,
  lists: () => [...todoQueries.all(), 'list'] as const,
  list: (filters: TodoFilters) =>
    queryOptions({
      queryKey: [...todoQueries.lists(), filters] as const,
      queryFn: () => fetchTodos(filters),
    }),
  detail: (id: number) =>
    queryOptions({
      queryKey: [...todoQueries.all(), 'detail', id] as const,
      queryFn: () => fetchTodo(id),
      staleTime: 5 * 60 * 1000,
    }),
};

useQuery(todoQueries.detail(id));
await queryClient.prefetchQuery(todoQueries.list({ status: 'active' }));
queryClient.invalidateQueries({ queryKey: todoQueries.lists() });
queryClient.invalidateQueries({ queryKey: todoQueries.all() });
```

### Validation

Search for query keys written as literals outside the factory, and check that each entity's keys share one prefix.

Inline keys in a small app where each key appears once are not a violation.
