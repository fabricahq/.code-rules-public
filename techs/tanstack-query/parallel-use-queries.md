---
title: "parallel-use-queries: Use useQueries for Dynamic Parallel Queries"
whenToRead: "Before fetching a dynamic collection of independent queries in parallel with TanStack Query."
impact: "MEDIUM"
impactDescription: "runs dynamic query sets concurrently without violating hook ordering"
tags: "tanstack-query, parallel-queries, use-queries, hooks, performance"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/parallel-use-queries.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/parallel-use-queries.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## parallel-use-queries: Use useQueries for Dynamic Parallel Queries

## Explanation

When you need to fetch multiple queries in parallel where the number or identity of queries is dynamic (e.g., fetching details for a list of IDs), use `useQueries`. It handles parallel execution and returns an array of query results.

## Bad Example

```tsx
// Sequential fetching with useEffect - waterfall
function UserProfiles({ userIds }: { userIds: string[] }) {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchAll() {
      const results = []
      for (const id of userIds) {
        const user = await fetchUser(id)  // Sequential!
        results.push(user)
      }
      setUsers(results)
      setLoading(false)
    }
    fetchAll()
  }, [userIds])

  // N requests run one after another
}

// Multiple useQuery calls - breaks rules of hooks
function UserProfiles({ userIds }: { userIds: string[] }) {
  // Can't call hooks in a loop!
  const queries = userIds.map(id => useQuery({
    queryKey: ['user', id],
    queryFn: () => fetchUser(id),
  }))
}
```

## Good Example

```tsx
import { useQueries } from '@tanstack/react-query'

function UserProfiles({ userIds }: { userIds: string[] }) {
  const userQueries = useQueries({
    queries: userIds.map(id => ({
      queryKey: ['users', id],
      queryFn: () => fetchUser(id),
      staleTime: 5 * 60 * 1000,
    })),
  })

  const isLoading = userQueries.some(q => q.isLoading)
  const isError = userQueries.some(q => q.isError)
  const users = userQueries.map(q => q.data).filter(Boolean)

  if (isLoading) return <Loading />
  if (isError) return <Error />

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

## Good Example: With Combine Option

```tsx
function UserProfiles({ userIds }: { userIds: string[] }) {
  const { data: users, isPending } = useQueries({
    queries: userIds.map(id => ({
      queryKey: ['users', id],
      queryFn: () => fetchUser(id),
    })),
    // Combine results into single value
    combine: (results) => ({
      data: results.map(r => r.data).filter(Boolean),
      isPending: results.some(r => r.isPending),
      isError: results.some(r => r.isError),
    }),
  })

  if (isPending) return <Loading />

  return <UserList users={users} />
}
```

## Good Example: Dependent Parallel Queries

```tsx
function PostsWithAuthors({ postIds }: { postIds: string[] }) {
  // First: fetch all posts in parallel
  const postQueries = useQueries({
    queries: postIds.map(id => ({
      queryKey: ['posts', id],
      queryFn: () => fetchPost(id),
    })),
  })

  const posts = postQueries.map(q => q.data).filter(Boolean)
  const authorIds = [...new Set(posts.map(p => p.authorId))]

  // Then: fetch all unique authors in parallel
  const authorQueries = useQueries({
    queries: authorIds.map(id => ({
      queryKey: ['users', id],
      queryFn: () => fetchUser(id),
      enabled: posts.length > 0,  // Wait for posts
    })),
  })

  // Combine data...
}
```

## Good Example: With Suspense

```tsx
import { useSuspenseQueries } from '@tanstack/react-query'

function UserProfiles({ userIds }: { userIds: string[] }) {
  const userQueries = useSuspenseQueries({
    queries: userIds.map(id => ({
      queryKey: ['users', id],
      queryFn: () => fetchUser(id),
    })),
  })

  // All data guaranteed - no loading states needed
  const users = userQueries.map(q => q.data)

  return <UserList users={users} />
}
```

## Context

- Queries run in parallel, not sequentially
- Each query is cached independently
- Use `combine` to transform results array into single value
- Empty queries array is valid (returns empty results)
- Pairs well with `useSuspenseQueries` for guaranteed data
- Individual query options (staleTime, etc.) apply per-query

Source: [TanStack Agent Skills - tanstack-query/parallel-use-queries.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/parallel-use-queries.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
