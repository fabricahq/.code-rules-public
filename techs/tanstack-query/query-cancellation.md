---
title: "Pass the query's AbortSignal to the request"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query query functions that make network requests or long-running work, especially search-as-you-type, fast navigation, or optimistic updates."
impact: "MEDIUM"
impactDescription: "Requests that ignore the query's AbortSignal keep running after they become obsolete, wasting bandwidth and server work."
tags: "tanstack-query, cancellation, AbortSignal"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/query-cancellation.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule query-cancellation (MIT, notice retained in NOTICE.md): restructured to the rule template and corrected when queries are cancelled: only when the query function consumes the signal."
---

## Pass the query's AbortSignal to the request

Pass the `signal` that TanStack Query gives the query function to the underlying request, such as `fetch` or an HTTP client, so obsolete requests are aborted.

### Implementation

- Destructure `signal` from the query function's context and pass it to `fetch`, your HTTP client, or any cancellable work.
- For custom work, such as a web worker, stop the work when the signal fires.
- Encode user input in URLs, such as with `URLSearchParams`, rather than interpolating it raw.
- Before an optimistic update, await `queryClient.cancelQueries` for the affected keys.
- Debounce search-as-you-type input as well; cancellation stops obsolete responses but does not prevent the requests from starting.

### Rationale

By default, TanStack Query does not cancel a query when its component unmounts or its key changes; the request finishes and its data is cached.
When the query function consumes the signal, TanStack Query aborts the request in those cases, and the query reverts to its previous state.
Aborting obsolete requests saves bandwidth and server work, and keeps a slow old response from arriving after a newer one.

### Examples

**Incorrect (counterexample):**

```tsx
const { data } = useQuery({
  queryKey: ['search', term],
  queryFn: async () => {
    const response = await fetch(`/api/search?q=${term}`);
    return response.json();
  },
});
```

Typing "abc" leaves the requests for "a" and "ab" running to completion, and the raw term breaks on characters such as `&`.

**Correct:**

```tsx
const { data } = useQuery({
  queryKey: ['search', term],
  queryFn: async ({ signal }) => {
    const response = await fetch(`/api/search?${new URLSearchParams({ q: term })}`, { signal });
    return response.json();
  },
});
```

When the key changes, the previous request is aborted.

### Validation

Type quickly into a search field backed by the query and check in the network panel that superseded requests show as cancelled.
Check that query functions making requests pass `signal` through.

A query function for instant, local work does not need to use the signal.
