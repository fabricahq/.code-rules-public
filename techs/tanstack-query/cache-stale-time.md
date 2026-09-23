---
title: "Set staleTime from how fast data changes"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query client defaults or per-query staleTime or gcTime, or diagnosing refetches on every mount, focus, or navigation."
impact: "MEDIUM"
impactDescription: "The default staleTime of zero refetches data on every mount and window focus, while an overly long staleTime shows outdated data."
tags: "tanstack-query, cache, staleTime, gcTime"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/tree/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules
    description: "Adapted from two rules in Deckard Gerritsen's TanStack Agent Skills (cache-stale-time and cache-gc-time; MIT, notice retained in NOTICE.md): merged the gcTime rule, restructured to the rule template, and labeled suggested durations as starting points."
---

## Set staleTime from how fast data changes

Set a client-wide default `staleTime` above zero, and override it per query based on how quickly that data changes and how much outdated data would matter.
Leave `gcTime` at its default unless you have a specific reason to change it.

### Implementation

- Set `defaultOptions.queries.staleTime` on the `QueryClient`, such as one minute, rather than relying on the default of zero.
- Give slowly changing data, such as reference lists or configuration, a longer `staleTime`, up to `Infinity` with explicit invalidation.
- Give fast-changing data a short `staleTime`, or refetch on an interval when users need it live.
- Put per-query values in the query's `queryOptions` factory so every use gets the same freshness.
- `gcTime` controls how long unused data stays in memory, five minutes by default in the browser.
  Raise it when users often return to the same data after longer gaps, or when persisting the cache.
  Lower it for large results viewed once.
  Avoid `gcTime: 0` for queries rendered on the server.
- Treat suggested durations as starting points; the right value depends on how stale data can be before users are misled.

### Rationale

Data is fresh for `staleTime` after it is fetched, and TanStack Query does not refetch fresh data when a component mounts or the window regains focus.
With the default of zero, every new observer and every focus triggers a request, which multiplies load for data that rarely changes.
`gcTime` is independent: it decides when data no longer used by any component is removed from the cache.

### Examples

**Incorrect (counterexample):**

```tsx
const queryClient = new QueryClient();

useQuery({ queryKey: ['categories'], queryFn: fetchCategories });
```

Categories rarely change, but they are refetched every time a component using them mounts and every time the window regains focus.

**Correct:**

```tsx
const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 60 * 1000 } },
});

export const categoryQueries = {
  all: () =>
    queryOptions({
      queryKey: ['categories'],
      queryFn: fetchCategories,
      staleTime: 30 * 60 * 1000,
    }),
};
```

### Validation

Watch the network panel while navigating between screens and refocusing the window, and check that slowly changing data is not refetched each time.
Check that the `QueryClient` sets a default `staleTime`.

A `staleTime` of zero is not a violation for data that must always be refetched when shown.
