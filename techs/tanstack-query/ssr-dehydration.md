---
title: "Prefetch on the server and hydrate the query cache"
whenToRead: "Before planning, writing, changing, or reviewing server rendering or route loaders in an app that reads data with TanStack Query, such as Next.js pages, TanStack Start routes, or a custom SSR setup."
impact: "MEDIUM-HIGH"
impactDescription: "Passing server data around the query cache causes duplicate client fetches and loading flashes, and a shared server QueryClient can leak one user's data to another."
tags: "tanstack-query, ssr, hydration, dehydrate"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/ssr-dehydration.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule ssr-dehydration (MIT, notice retained in NOTICE.md): restructured to the rule template, added the client staleTime requirement, and described safe serialization."
---

## Prefetch on the server and hydrate the query cache

When a page is server-rendered, prefetch its queries into a `QueryClient` created for that request, dehydrate the cache, and hydrate it on the client, so components read the same cached data with no second fetch.

### Implementation

- Create a new `QueryClient` for each request on the server; never share one across requests.
- Prefetch with the same query options factories that client components use, so the keys match.
- Pass `dehydrate(queryClient)` to `HydrationBoundary`, or to your framework's equivalent, around the components that read the data.
- Set a default `staleTime` above zero on the client `QueryClient`, so hydrated data is not refetched immediately.
- When serializing dehydrated state into HTML yourself, use a serializer that escapes it for a script tag; plain `JSON.stringify` output can break out of the tag.
- Only successful queries are dehydrated by default; configure `shouldDehydrateQuery` when you need others.
- In a router with loaders, such as TanStack Start, call `ensureQueryData` in the loader and read with `useSuspenseQuery` in the component.

### Rationale

Data fetched on the server outside the query cache, such as through props, is invisible to TanStack Query, so the client fetches it again and components juggle two sources.
Dehydrating puts the server's results into the client cache under the same keys.
A server `QueryClient` shared across requests keeps one user's data in memory where another request can read it.

### Examples

**Incorrect (counterexample):**

```tsx
export async function getServerSideProps() {
  return { props: { posts: await fetchPosts() } };
}

function PostsPage({ posts }: { posts: Array<Post> }) {
  const { data } = useQuery({ queryKey: ['posts'], queryFn: fetchPosts });
  return <PostList posts={data ?? posts} />;
}
```

The client fetches the posts again, and the component has to choose between two sources.

**Correct (Next.js App Router):**

```tsx
export default async function PostsPage() {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery(postQueries.list());

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList />
    </HydrationBoundary>
  );
}
```

```tsx
'use client';

export function PostList() {
  const { data: posts } = useSuspenseQuery(postQueries.list());
  return <ul>{posts.map((post) => <li key={post.id}>{post.title}</li>)}</ul>;
}
```

### Validation

Load a server-rendered page and check in the network panel that the client does not refetch hydrated queries immediately.
Check that each request creates its own `QueryClient`.

A page that fetches only on the client, with no server rendering of that data, does not need dehydration.
