---
title: "Fetch a dynamic set of queries with useQueries"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query code that fetches one query per item in a list whose length or contents change, such as details for a set of IDs."
impact: "MEDIUM"
impactDescription: "Fetching per-item data in a loop of awaits or Hooks either serializes requests or breaks the Rules of Hooks."
tags: "tanstack-query, useQueries, parallel"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/parallel-use-queries.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule parallel-use-queries (MIT, notice retained in NOTICE.md): restructured to the rule template, simplified the dependent example, and noted combine stability."
---

## Fetch a dynamic set of queries with useQueries

When the number of queries depends on data, such as one query per ID, use `useQueries`, or `useSuspenseQueries` with Suspense, instead of calling `useQuery` in a loop or fetching sequentially in an Effect.

### Implementation

- Map the items to query options, preferably from the entity's `queryOptions` factory, so each item shares the cache with other reads of the same entity.
- Use `combine` to turn the results into the shape the component needs, such as an array of data plus one pending flag.
  Define `combine` outside the component or memoize it when it does expensive work, because it re-runs when its reference changes.
- An empty list of queries is valid and returns an empty result.
- When the list of items comes from another query, build the second list from the first query's data; an empty list simply waits.
- When a single endpoint can return all items at once, one query for the batch may be better than many small requests.

### Rationale

Hooks cannot be called in a loop, and awaiting requests one by one in an Effect turns them into a waterfall.
`useQueries` runs all the queries in parallel, caches each one under its own key, and lets other components reuse those entries.

### Examples

**Incorrect (counterexample):**

```tsx
function UserProfiles({ userIds }: { userIds: ReadonlyArray<string> }) {
  const users = userIds.map((id) => useQuery({ queryKey: ['users', id], queryFn: () => fetchUser(id) }));
  // ...
}
```

The number of Hook calls changes with the list, which breaks the Rules of Hooks.

**Correct:**

```tsx
function UserProfiles({ userIds }: { userIds: ReadonlyArray<string> }) {
  const { users, isPending } = useQueries({
    queries: userIds.map((id) => userQueries.detail(id)),
    combine: (results) => ({
      users: results.flatMap((result) => (result.data ? [result.data] : [])),
      isPending: results.some((result) => result.isPending),
    }),
  });
  // ...
}
```

`userQueries.detail` is the user entity's query options factory.

### Validation

Check that per-item queries run in parallel in the network panel, and that no Hook is called inside a loop.

One query that fetches a whole batch from a batch endpoint is not a violation.
