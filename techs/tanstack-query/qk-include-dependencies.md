---
title: "qk-include-dependencies: Include All Variables the Query Depends On"
whenToRead: "Before defining a TanStack Query key for a query function that depends on IDs, filters, search terms, or other changing inputs."
impact: "HIGH"
impactDescription: "prevents stale data and cache collisions when query functions depend on changing values"
tags: "tanstack-query, query-keys, dependencies, cache, stale-data"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-include-dependencies.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/qk-include-dependencies.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## qk-include-dependencies: Include All Variables the Query Depends On

## Explanation

If your query function depends on a variable, that variable must be included in the query key. This ensures independent caching per variable combination and automatic refetching when dependencies change. Missing dependencies cause stale data bugs and cache collisions.

## Bad Example

```tsx
function UserPosts({ userId }: { userId: string }) {
  // Missing userId in query key - all users share the same cache!
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetchPostsByUser(userId),
  })

  return <PostList posts={data} />
}

function FilteredTodos({ status, page }: { status: string; page: number }) {
  // Missing filter parameters - won't refetch when filters change
  const { data } = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetchTodos({ status, page }),
  })

  return <TodoList todos={data} />
}
```

## Good Example

```tsx
function UserPosts({ userId }: { userId: string }) {
  // userId included - each user has their own cache entry
  const { data } = useQuery({
    queryKey: ['posts', userId],
    queryFn: () => fetchPostsByUser(userId),
  })

  return <PostList posts={data} />
}

function FilteredTodos({ status, page }: { status: string; page: number }) {
  // All dependencies included - refetches when any change
  const { data } = useQuery({
    queryKey: ['todos', { status, page }],
    queryFn: () => fetchTodos({ status, page }),
  })

  return <TodoList todos={data} />
}
```

## Context

- This is arguably the most important query key rule
- Applies whenever query function uses external variables
- Prevents subtle bugs where different contexts share cached data
- Works in conjunction with staleTime - even with long staleTime, changing keys triggers new fetches

Source: [TanStack Agent Skills - tanstack-query/qk-include-dependencies.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-include-dependencies.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
