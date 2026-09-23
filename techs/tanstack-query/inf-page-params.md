---
title: "Derive infinite query page params from the server's response"
whenToRead: "Before planning, writing, changing, or reviewing a TanStack Query useInfiniteQuery, such as infinite scrolling, load-more buttons, or chat history."
impact: "MEDIUM"
impactDescription: "Guessing whether more pages exist from page size fetches an extra empty page or stops early."
tags: "tanstack-query, infinite-queries, pagination"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/inf-page-params.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule inf-page-params (MIT, notice retained in NOTICE.md): reframed from providing getNextPageParam, which TypeScript already requires, to deriving it from the server's response; restructured to the rule template."
---

## Derive infinite query page params from the server's response

Have `getNextPageParam` return the next cursor or page from what the server says, and return `undefined` or `null` when the server says there are no more pages.

### Implementation

- Prefer an API that returns a next cursor, or an explicit `hasMore` or total count.
- Return `undefined` or `null` from `getNextPageParam` when there is no next page; that sets `hasNextPage` to `false`.
- Avoid inferring the end from `lastPage.length < pageSize`; when the last page is exactly full, it fetches one extra empty page.
- Include filters in the query key, so changing them starts a new list instead of appending to the old one.
- Set `maxPages` for very long feeds to bound memory, and provide `getPreviousPageParam` when pages can be dropped from the start.
- Disable the load-more control while `isFetchingNextPage` is true.

### Rationale

The server knows whether more data exists; the client can only guess from page sizes.
A guess based on a full last page requests a page that turns out empty, and a guess that assumes short pages mean the end stops early when the server returns a short page for another reason.

### Examples

**Incorrect (counterexample):**

```tsx
useInfiniteQuery({
  queryKey: ['posts'],
  queryFn: ({ pageParam }) => fetchPosts({ page: pageParam, limit: 20 }),
  initialPageParam: 1,
  getNextPageParam: (lastPage, allPages) => (lastPage.length < 20 ? undefined : allPages.length + 1),
});
```

If there are exactly 40 posts, the query fetches a third, empty page before stopping.

**Correct:**

```tsx
useInfiniteQuery({
  queryKey: ['posts', { filter }],
  queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam, filter }),
  initialPageParam: null as string | null,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
});
```

The server's `nextCursor` is `null` when there are no more posts.

### Validation

Test with a result count that is an exact multiple of the page size and check that no empty page is requested.
Change a filter and check that the list restarts.

Page-size inference is not a violation when the API offers nothing better and an extra empty request is acceptable.
