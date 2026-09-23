---
title: "qk-factory-pattern: Use Query Key Factories for Complex Applications"
whenToRead: "Before organizing many TanStack Query keys shared across features, cache updates, or invalidation calls."
impact: "MEDIUM"
impactDescription: "centralizes query-key construction so cache access stays consistent as the app grows"
tags: "tanstack-query, query-keys, factories, type-safety, cache"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-factory-pattern.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/qk-factory-pattern.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## qk-factory-pattern: Use Query Key Factories for Complex Applications

## Explanation

For applications with many queries, centralize query key definitions in factory functions. This ensures consistency, enables autocomplete, prevents typos, and makes refactoring safer. Query key factories are the recommended pattern for production applications.

## Bad Example

```tsx
// Scattered, inconsistent key definitions across files
// file: components/TodoList.tsx
const { data } = useQuery({
  queryKey: ['todos', 'list'],
  queryFn: fetchTodos,
})

// file: components/TodoDetail.tsx
const { data } = useQuery({
  queryKey: ['todo', id],  // Inconsistent: 'todo' vs 'todos'
  queryFn: () => fetchTodo(id),
})

// file: components/TodoComments.tsx
const { data } = useQuery({
  queryKey: ['todoComments', todoId],  // Different naming convention
  queryFn: () => fetchComments(todoId),
})

// Invalidation is error-prone
queryClient.invalidateQueries({ queryKey: ['todos'] })  // Misses 'todo' and 'todoComments'
```

## Good Example

```tsx
// file: lib/query-keys.ts
export const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filters: TodoFilters) => [...todoKeys.lists(), filters] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: number) => [...todoKeys.details(), id] as const,
  comments: (id: number) => [...todoKeys.detail(id), 'comments'] as const,
}

export const userKeys = {
  all: ['users'] as const,
  detail: (id: string) => [...userKeys.all, id] as const,
  posts: (id: string) => [...userKeys.detail(id), 'posts'] as const,
}

// file: components/TodoList.tsx
import { todoKeys } from '@/lib/query-keys'

const { data } = useQuery({
  queryKey: todoKeys.list({ status: 'active' }),
  queryFn: () => fetchTodos({ status: 'active' }),
})

// file: components/TodoDetail.tsx
const { data } = useQuery({
  queryKey: todoKeys.detail(id),
  queryFn: () => fetchTodo(id),
})

// Invalidation is type-safe and predictable
queryClient.invalidateQueries({ queryKey: todoKeys.all })  // Invalidates everything
queryClient.invalidateQueries({ queryKey: todoKeys.detail(5) })  // Specific todo + comments
```

## Query Options Factory Pattern

```tsx
// Even better: combine with queryOptions for full type safety
import { queryOptions } from '@tanstack/react-query'

export const todoQueries = {
  all: () => queryOptions({
    queryKey: todoKeys.all,
    queryFn: fetchAllTodos,
  }),
  detail: (id: number) => queryOptions({
    queryKey: todoKeys.detail(id),
    queryFn: () => fetchTodo(id),
    staleTime: 5 * 60 * 1000,
  }),
}

// Usage
const { data } = useQuery(todoQueries.detail(5))
await queryClient.prefetchQuery(todoQueries.detail(5))
```

## Context

- Essential for applications with 10+ different query types
- Enables IDE autocomplete and typo prevention
- Makes invalidation patterns discoverable
- Pairs well with `queryOptions` for full type inference
- Consider the `@lukemorales/query-key-factory` package for standardized implementation

Source: [TanStack Agent Skills - tanstack-query/qk-factory-pattern.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-factory-pattern.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
