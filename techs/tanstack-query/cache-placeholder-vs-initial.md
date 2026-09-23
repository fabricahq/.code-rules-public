---
title: "Use initialData only for complete data"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query code that shows data before a fetch completes, such as previews from a list, server-provided data, or the previous page while the next loads."
impact: "MEDIUM"
impactDescription: "Partial data passed as initialData is cached as if it were a real response, so other components see incomplete data and it may never be refetched."
tags: "tanstack-query, placeholderData, initialData, cache"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/cache-placeholder-vs-initial.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule cache-placeholder-vs-initial (MIT, notice retained in NOTICE.md): restructured to the rule template and removed an example that combined options in a way TanStack Query ignores."
---

## Use initialData only for complete data

Pass `initialData` only when you have the complete, authoritative value for a query.
Use `placeholderData` for anything partial or temporary, such as a preview from a list or the previous page while the next one loads.

### Implementation

- Use `placeholderData` for previews and previous results; it is shown while the query fetches and is never written to the cache.
- Use `placeholderData: keepPreviousData` to keep showing the previous page or filter results while the next ones load.
- Check `isPlaceholderData` to mark or disable UI that shows placeholder content.
- Use `initialData` only for complete data, and pass `initialDataUpdatedAt` so `staleTime` is measured from when that data was actually fetched.
- For server rendering, prefer prefetching and hydrating the cache over passing `initialData` through props.

### Rationale

`initialData` is written to the cache as if a fetch returned it.
Other components reading the same key receive it, and if it looks fresh under `staleTime`, no fetch replaces it.
Partial data in `initialData` therefore spreads incomplete data through the app.
`placeholderData` exists only for the observer that uses it and disappears once real data arrives.

### Examples

#### Application: A preview from a list

**Incorrect (counterexample):**

```tsx
const { data } = useQuery({
  queryKey: ['posts', postId],
  queryFn: () => fetchPost(postId),
  initialData: postSummaryFromList,
});
```

The summary lacks the post body, but it is cached as the full post for every component that reads `['posts', postId]`.

**Correct:**

```tsx
const { data, isPlaceholderData } = useQuery({
  queryKey: ['posts', postId],
  queryFn: () => fetchPost(postId),
  placeholderData: postSummaryFromList,
});
```

#### Application: Paginated results

**Correct:**

```tsx
const { data, isPlaceholderData } = useQuery({
  queryKey: ['products', { page }],
  queryFn: () => fetchProducts(page),
  placeholderData: keepPreviousData,
});
```

The previous page stays visible, marked by `isPlaceholderData`, until the next page arrives.

### Validation

For each `initialData`, check that the value is complete for the query and that `initialDataUpdatedAt` is set when the data came from an earlier fetch.

`initialData` holding a complete, authoritative value is not a violation.
