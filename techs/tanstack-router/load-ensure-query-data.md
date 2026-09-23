---
title: "With TanStack Query, load route data into the Query cache"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router loaders or route components in an app that also uses TanStack Query, or router options that control preload caching."
impact: "HIGH"
impactDescription: "Returning data from loaders alongside Query hooks creates two caches that disagree, and misusing prefetchQuery lets routes render before their data is ready."
tags: "tanstack-router, tanstack-query, loaders, ensureQueryData, cache"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/tree/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills
    description: "Adapted from three rules in Deckard Gerritsen's TanStack Agent Skills (flow-loader-query-pattern, load-ensure-query-data, and cache-single-source; MIT, notice retained in NOTICE.md): merged three overlapping rules on loader and Query integration, restructured to the rule template, and corrected ensureQueryData, which returns cached data even when stale."
---

## With TanStack Query, load route data into the Query cache

When an app uses TanStack Query, make it the only cache for server data: loaders call `queryClient.ensureQueryData` with the same query options the component reads, and components read with `useSuspenseQuery`.
Set `defaultPreloadStaleTime: 0` so the router always runs loaders and Query decides whether to fetch.

### Implementation

- Define query options once, such as in a `queryOptions` factory, and use them in both the loader and the component.
- In the loader, await `ensureQueryData` for data the route cannot render without, and start them together with `Promise.all`.
- Start non-critical data with `prefetchQuery` without awaiting it, and read it with `useQuery` so the component can show a loading state for that part.
- In the component, read critical data with `useSuspenseQuery`; it finds the data the loader cached.
- `ensureQueryData` returns cached data even when it is stale.
  Pass `revalidateIfStale: true` to also refetch stale data in the background, or rely on the component's query to refetch according to `staleTime`.
- `prefetchQuery` never throws and returns nothing; use it only when the route can render without the result.
- Set `defaultPreloadStaleTime: 0` on the router, so preloads and navigations always call the loader and TanStack Query's `staleTime` controls freshness.
- Do not also return the fetched data from the loader for the component to read; read it from Query.

### Rationale

TanStack Router has its own loader cache, and TanStack Query has another.
If loaders return fetched data while components also query it, the two copies go stale on different schedules and mutations update only one.
Loading into Query's cache keeps one source of truth, while the loader still starts the fetch early and on preload.

### Examples

#### Application: Two caches

**Incorrect (counterexample):**

```tsx
export const Route = createFileRoute('/posts')({
  loader: () => fetchPosts(),
  component: PostsPage,
});

function PostsPage() {
  const { data } = useQuery({ queryKey: ['posts'], queryFn: fetchPosts });
  // ...
}
```

The loader's copy lives in the router cache and the component's copy in Query, so they are fetched twice and can disagree.

**Correct:**

```tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params, context: { queryClient } }) => {
    void queryClient.prefetchQuery(commentQueries.forPost(params.postId));
    await queryClient.ensureQueryData(postQueries.detail(params.postId));
  },
  component: PostPage,
});

function PostPage() {
  const { postId } = Route.useParams();
  const { data: post } = useSuspenseQuery(postQueries.detail(postId));
  const comments = useQuery(commentQueries.forPost(postId));
  // ...
}
```

`postQueries` and `commentQueries` are query options factories.
The post is required before render, while comments load in parallel and show their own loading state.

#### Application: Router preload caching

**Correct:**

```tsx
const router = createRouter({
  routeTree,
  context: { queryClient },
  defaultPreload: 'intent',
  defaultPreloadStaleTime: 0,
});
```

### Validation

Check that loaders call `ensureQueryData` or `prefetchQuery` with the same query options their components read, and that loaders return no server data for components to read directly.
Check that the router sets `defaultPreloadStaleTime: 0`.

Returning route-only values that are not server data, such as a computed page title, is not a violation.
